"""
camera_streamer.py — Internal Webots camera controller.

Runs INSIDE the Webots process using Webots' bundled Python.
Uses ONLY Python stdlib (no requests, no cv2, no numpy) so it works
in Webots' isolated Python environment without any pip installs.

Each CAM_ROBOT node uses this as its controller with:
  controllerArgs ["BUS_01"]  (or BUS_02, BUS_03)
"""

import sys
import time
import base64
import json
import struct
import zlib
import urllib.request

from controller import Robot

BACKEND_URL = "http://127.0.0.1:8000"


# ---------------------------------------------------------------------------
# Minimal PNG encoder — stdlib only, no Pillow/cv2/numpy needed
# ---------------------------------------------------------------------------

def _make_png(width, height, bgra_bytes):
    """Encode raw BGRA bytes to a minimal PNG file in pure Python."""
    def chunk(tag, data):
        c = zlib.crc32(tag + data) & 0xFFFFFFFF
        return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', c)

    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    ihdr = chunk(b'IHDR', ihdr_data)

    raw_rows = bytearray()
    for y in range(height):
        raw_rows.append(0)  # filter type None
        for x in range(width):
            base = (y * width + x) * 4
            raw_rows.append(bgra_bytes[base + 2])  # R
            raw_rows.append(bgra_bytes[base + 1])  # G
            raw_rows.append(bgra_bytes[base])      # B

    idat = chunk(b'IDAT', zlib.compress(bytes(raw_rows), 1))
    iend = chunk(b'IEND', b'')
    return b'\x89PNG\r\n\x1a\n' + ihdr + idat + iend


# ---------------------------------------------------------------------------
# Nearest-neighbour scale down
# ---------------------------------------------------------------------------

def _scale_bgra(bgra_bytes, src_w, src_h, dst_w, dst_h):
    out = bytearray(dst_w * dst_h * 4)
    x_ratio = src_w / dst_w
    y_ratio = src_h / dst_h
    for dy in range(dst_h):
        sy = int(dy * y_ratio)
        for dx in range(dst_w):
            sx = int(dx * x_ratio)
            src_pos = (sy * src_w + sx) * 4
            dst_pos = (dy * dst_w + dx) * 4
            out[dst_pos:dst_pos + 4] = bgra_bytes[src_pos:src_pos + 4]
    return bytes(out)


def post_telemetry(bus_id, frame_b64, location):
    payload = json.dumps({
        "bus_id":    bus_id,
        "timestamp": time.time(),
        "latitude":  location["latitude"],
        "longitude": location["longitude"],
        "speed":     30.0,
        "status":    "active",
        "frame":     frame_b64,
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{BACKEND_URL}/api/buses/{bus_id}/telemetry",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=1.0) as resp:
            return resp.status
    except Exception:
        return None


def main():
    robot = Robot()
    timestep = int(robot.getBasicTimeStep())

    bus_id = robot.getName()
    if len(sys.argv) > 1:
        bus_id = sys.argv[1]

    print(f"[camera_streamer] {bus_id}: starting, timestep={timestep}ms", flush=True)

    cam = robot.getDevice("camera")
    gps = robot.getDevice("gps")

    if not cam:
        print(f"[camera_streamer] {bus_id}: ERROR - no 'camera' device found", flush=True)
        while robot.step(timestep) != -1:
            pass
        return

    cam.enable(timestep)
    if gps:
        gps.enable(timestep)

    w = cam.getWidth()
    h = cam.getHeight()
    print(f"[camera_streamer] {bus_id}: camera enabled {w}x{h}", flush=True)

    # Pure-Python PNG encode is slow — 10 FPS is plenty for a dashboard
    frame_interval = 0.1
    last_post = 0.0
    frame_count = 0
    error_count = 0

    while robot.step(timestep) != -1:
        now = time.time()
        if now - last_post < frame_interval:
            continue
        last_post = now

        try:
            # getImage() returns raw BGRA bytes — no MMF, direct C-API
            raw = cam.getImage()
            if raw is None:
                continue

            location = {"latitude": 11.0168, "longitude": 76.9558}
            if gps:
                try:
                    v = gps.getValues()
                    if v and len(v) >= 3:
                        location = {
                            "latitude":  11.0168 + v[0] * 0.0001,
                            "longitude": 76.9558 + v[2] * 0.0001,
                        }
                except Exception:
                    pass

            bgra_bytes = bytes(raw)

            # Scale to 160x90 for fast pure-Python PNG encode
            dst_w, dst_h = min(w, 160), min(h, 90)
            if w != dst_w or h != dst_h:
                bgra_bytes = _scale_bgra(bgra_bytes, w, h, dst_w, dst_h)

            png_bytes = _make_png(dst_w, dst_h, bgra_bytes)
            frame_b64 = base64.b64encode(png_bytes).decode("utf-8")

            status = post_telemetry(bus_id, frame_b64, location)
            if status:
                frame_count += 1
                if frame_count % 50 == 0:
                    print(f"[camera_streamer] {bus_id}: {frame_count} frames sent OK", flush=True)
            else:
                error_count += 1
                if error_count % 30 == 1:
                    print(f"[camera_streamer] {bus_id}: POST failed (backend down?)", flush=True)

        except Exception as e:
            print(f"[camera_streamer] {bus_id}: frame error: {e}", flush=True)


if __name__ == "__main__":
    main()
