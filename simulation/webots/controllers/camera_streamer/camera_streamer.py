"""
camera_streamer.py — Internal Webots camera controller with MJPEG server.

Runs INSIDE the Webots process (Webots' bundled Python).
Serves a live MJPEG HTTP stream on:
  BUS_01 → http://127.0.0.1:8011/
  BUS_02 → http://127.0.0.1:8012/
  BUS_03 → http://127.0.0.1:8013/

The browser <img src="http://127.0.0.1:8011/"> receives the stream natively.
No WebSocket, no base64, no backend dependency for video.

Dependencies: stdlib only (threading, http.server, socketserver, zlib, struct)
"""

import sys
import time
import base64
import json
import struct
import zlib
import threading
import urllib.request
import http.server
import socketserver
from controller import Robot

BACKEND_URL = "http://127.0.0.1:8000"

# ── Shared state (main loop → HTTP server thread) ──────────────────────────
_latest_frame = None   # raw PNG bytes
_frame_lock   = threading.Lock()


# ── Minimal PNG encoder (stdlib, no cv2/Pillow) ────────────────────────────

def _make_png(width, height, bgra_bytes):
    def chunk(tag, data):
        c = zlib.crc32(tag + data) & 0xFFFFFFFF
        return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', c)

    ihdr = chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0))

    raw_rows = bytearray()
    for y in range(height):
        raw_rows.append(0)  # filter: None
        row_base = y * width * 4
        for x in range(width):
            b4 = row_base + x * 4
            raw_rows.append(bgra_bytes[b4 + 2])  # R
            raw_rows.append(bgra_bytes[b4 + 1])  # G
            raw_rows.append(bgra_bytes[b4])       # B

    idat = chunk(b'IDAT', zlib.compress(bytes(raw_rows), 1))
    iend = chunk(b'IEND', b'')
    return b'\x89PNG\r\n\x1a\n' + ihdr + idat + iend


# ── Nearest-neighbour scale ─────────────────────────────────────────────────

def _scale_bgra(bgra_bytes, sw, sh, dw, dh):
    out = bytearray(dw * dh * 4)
    xr = sw / dw
    yr = sh / dh
    for dy in range(dh):
        sy = int(dy * yr)
        for dx in range(dw):
            sx = int(dx * xr)
            s = (sy * sw + sx) * 4
            d = (dy * dw + dx) * 4
            out[d:d + 4] = bgra_bytes[s:s + 4]
    return bytes(out)


# ── MJPEG HTTP handler ──────────────────────────────────────────────────────

BOUNDARY = b'--frame'

class MJPEGHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass  # suppress access logs

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type',
                         'multipart/x-mixed-replace; boundary=frame')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache')
        self.end_headers()

        try:
            while True:
                with _frame_lock:
                    frame = _latest_frame

                if frame:
                    header = (
                        b'--frame\r\n'
                        b'Content-Type: image/png\r\n'
                        b'Content-Length: ' + str(len(frame)).encode() + b'\r\n'
                        b'\r\n'
                    )
                    self.wfile.write(header + frame + b'\r\n')
                    self.wfile.flush()

                time.sleep(0.1)  # ~10 FPS
        except Exception:
            pass  # client disconnected


def _start_mjpeg_server(port):
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(('0.0.0.0', port), MJPEGHandler) as httpd:
        print(f"[camera_streamer] MJPEG server → http://127.0.0.1:{port}/", flush=True)
        httpd.serve_forever()


# ── Telemetry POST (location + speed only, no frame) ───────────────────────

def _post_telemetry(bus_id, location):
    payload = json.dumps({
        "bus_id":    bus_id,
        "timestamp": time.time(),
        "latitude":  location["latitude"],
        "longitude": location["longitude"],
        "speed":     30.0,
        "status":    "active",
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{BACKEND_URL}/api/buses/{bus_id}/telemetry",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=0.5):
            pass
    except Exception:
        pass


# ── Main ───────────────────────────────────────────────────────────────────

def main():
    global _latest_frame

    robot    = Robot()
    timestep = int(robot.getBasicTimeStep())

    bus_id = robot.getName()
    if len(sys.argv) > 1:
        bus_id = sys.argv[1]

    # BUS_01 → 8011, BUS_02 → 8012, BUS_03 → 8013
    try:
        bus_num = int(bus_id.split('_')[1])
    except Exception:
        bus_num = 1
    mjpeg_port = 8010 + bus_num

    print(f"[camera_streamer] {bus_id}: starting (timestep={timestep}ms)", flush=True)

    cam = robot.getDevice("camera")
    gps = robot.getDevice("gps")

    if not cam:
        print(f"[camera_streamer] {bus_id}: ERROR — no 'camera' device", flush=True)
        while robot.step(timestep) != -1:
            pass
        return

    cam.enable(timestep)
    if gps:
        gps.enable(timestep)

    w, h = cam.getWidth(), cam.getHeight()
    print(f"[camera_streamer] {bus_id}: camera {w}x{h} enabled", flush=True)

    # Start MJPEG server in daemon thread
    t = threading.Thread(target=_start_mjpeg_server, args=(mjpeg_port,), daemon=True)
    t.start()

    # Encode at smaller resolution for smooth streaming
    dw, dh = min(w, 320), min(h, 180)

    frame_interval  = 0.10   # encode rate  ~10 FPS
    telem_interval  = 0.50   # telemetry POST ~2/s
    last_frame      = 0.0
    last_telem      = 0.0
    frame_count     = 0

    while robot.step(timestep) != -1:
        now = time.time()

        # ── Capture + encode frame ──────────────────────────────────────────
        if now - last_frame >= frame_interval:
            last_frame = now
            try:
                raw = cam.getImage()
                if raw is not None:
                    bgra = bytes(raw)
                    if w != dw or h != dh:
                        bgra = _scale_bgra(bgra, w, h, dw, dh)
                    png = _make_png(dw, dh, bgra)
                    with _frame_lock:
                        _latest_frame = png
                    frame_count += 1
                    if frame_count % 100 == 0:
                        print(f"[camera_streamer] {bus_id}: {frame_count} frames encoded", flush=True)
            except Exception as e:
                print(f"[camera_streamer] {bus_id}: capture error: {e}", flush=True)

        # ── Telemetry POST (location/speed, no frame) ───────────────────────
        if now - last_telem >= telem_interval:
            last_telem = now
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
            threading.Thread(target=_post_telemetry, args=(bus_id, location),
                             daemon=True).start()


if __name__ == "__main__":
    main()
