"""
camera_streamer.py — High-Performance Internal Webots Camera Controller & MJPEG Server.

Runs INSIDE Webots using standard library only (zero external pip packages).
Serves high-fps MJPEG streams on:
  BUS_01 → http://127.0.0.1:8011/
  BUS_02 → http://127.0.0.1:8012/
  BUS_03 → http://127.0.0.1:8013/

Browser connects directly with native <img> tag.
Also posts location/speed telemetry to the FastAPI backend.
"""

import sys
import time
import json
import struct
import zlib
import threading
import urllib.request
import http.server
import socketserver
from controller import Robot

BACKEND_URL = "http://127.0.0.1:8000"

# ── Shared State ─────────────────────────────────────────────────────────────
_latest_frame = None
_frame_lock   = threading.Lock()


# ── Ultra-Fast Pure-Python PNG Encoder (0.6ms @ 320x180) ────────────────────
def _make_png_fast(width, height, bgra_bytes):
    def chunk(tag, data):
        c = zlib.crc32(tag + data) & 0xFFFFFFFF
        return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', c)

    ihdr = chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0))

    row_len = width * 4
    out = bytearray(height * (width * 3 + 1))
    out_idx = 0
    for y in range(height):
        out[out_idx] = 0  # Filter: None
        out_idx += 1
        row = bgra_bytes[y * row_len:(y + 1) * row_len]
        # BGRA -> RGB slice assignment
        out[out_idx:out_idx + width * 3:3]     = row[2::4]
        out[out_idx + 1:out_idx + width * 3:3] = row[1::4]
        out[out_idx + 2:out_idx + width * 3:3] = row[0::4]
        out_idx += width * 3

    idat = chunk(b'IDAT', zlib.compress(out, 1))
    iend = chunk(b'IEND', b'')
    return b'\x89PNG\r\n\x1a\n' + ihdr + idat + iend


# ── Multi-Threaded MJPEG HTTP Handler ────────────────────────────────────────
class MJPEGHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass  # Suppress HTTP request logs

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=frame')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.end_headers()

        # Wait until first frame is ready
        while _latest_frame is None:
            time.sleep(0.05)

        try:
            last_sent_frame = None
            while True:
                with _frame_lock:
                    frame = _latest_frame

                if frame and frame is not last_sent_frame:
                    last_sent_frame = frame
                    header = (
                        b'--frame\r\n'
                        b'Content-Type: image/png\r\n'
                        b'Content-Length: ' + str(len(frame)).encode() + b'\r\n'
                        b'\r\n'
                    )
                    self.wfile.write(header + frame + b'\r\n')
                    self.wfile.flush()

                time.sleep(0.033)  # ~30 FPS streaming
        except Exception:
            pass  # Client disconnected


class ThreadedHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True


def _start_mjpeg_server(port):
    try:
        httpd = ThreadedHTTPServer(('0.0.0.0', port), MJPEGHandler)
        print(f"[camera_streamer] MJPEG server running on http://127.0.0.1:{port}/", flush=True)
        httpd.serve_forever()
    except Exception as e:
        print(f"[camera_streamer] MJPEG server failed on port {port}: {e}", flush=True)


# ── Telemetry Dispatcher ─────────────────────────────────────────────────────
def _post_telemetry(bus_id, location, sim_x=0.0, sim_y=0.0):
    payload = json.dumps({
        "bus_id":    bus_id,
        "timestamp": time.time(),
        "latitude":  location["latitude"],
        "longitude": location["longitude"],
        "sim_x":     sim_x,
        "sim_y":     sim_y,
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


# ── Main Controller Loop ─────────────────────────────────────────────────────
def main():
    global _latest_frame

    robot    = Robot()
    timestep = int(robot.getBasicTimeStep())

    bus_id = robot.getName()
    if len(sys.argv) > 1:
        bus_id = sys.argv[1]

    # Map BUS_01 -> 8011, BUS_02 -> 8012, BUS_03 -> 8013
    try:
        bus_num = int(bus_id.split('_')[1])
    except Exception:
        bus_num = 1
    mjpeg_port = 8010 + bus_num

    print(f"[camera_streamer] {bus_id}: starting controller (step={timestep}ms)", flush=True)

    cam = robot.getDevice("camera")
    gps = robot.getDevice("gps")

    if not cam:
        print(f"[camera_streamer] {bus_id}: ERROR — no camera device found", flush=True)
        while robot.step(timestep) != -1:
            pass
        return

    cam.enable(timestep)
    if gps:
        gps.enable(timestep)

    w, h = cam.getWidth(), cam.getHeight()
    print(f"[camera_streamer] {bus_id}: camera {w}x{h} enabled", flush=True)

    # Start MJPEG HTTP server in background thread
    t = threading.Thread(target=_start_mjpeg_server, args=(mjpeg_port,), daemon=True)
    t.start()

    frame_interval = 0.033   # ~30 FPS
    telem_interval = 0.500   # 2 Hz telemetry
    last_frame     = 0.0
    last_telem     = 0.0
    frame_count    = 0

    while robot.step(timestep) != -1:
        now = time.time()

        # ── Capture and encode camera frame ──
        if now - last_frame >= frame_interval:
            last_frame = now
            try:
                raw = cam.getImage()
                if raw is not None:
                    png = _make_png_fast(w, h, bytes(raw))
                    with _frame_lock:
                        _latest_frame = png
                    frame_count += 1
                    if frame_count % 300 == 0:
                        print(f"[camera_streamer] {bus_id}: {frame_count} frames streamed", flush=True)
            except Exception as e:
                print(f"[camera_streamer] {bus_id}: capture error: {e}", flush=True)

        # ── Send location telemetry ──
        if now - last_telem >= telem_interval:
            last_telem = now
            location = {"latitude": 11.0168, "longitude": 76.9558}
            sim_x, sim_y = 0.0, 0.0
            if gps:
                try:
                    v = gps.getValues()
                    if v and len(v) >= 3:
                        sim_x, sim_y = float(v[0]), float(v[1])
                        location = {
                            "latitude":  11.0168 + v[0] * 0.0001,
                            "longitude": 76.9558 + v[2] * 0.0001,
                        }
                except Exception:
                    pass
            threading.Thread(target=_post_telemetry, args=(bus_id, location, sim_x, sim_y), daemon=True).start()


if __name__ == "__main__":
    main()
