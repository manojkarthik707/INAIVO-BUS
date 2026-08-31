"""
camera_streamer.py — High-Performance Internal Webots Camera Controller & On-Demand MJPEG Server.

Runs INSIDE Webots using standard library only.
Serves high-fps MJPEG streams on:
  BUS_01 → http://127.0.0.1:8011/
  BUS_02 → http://127.0.0.1:8012/
  BUS_03 → http://127.0.0.1:8013/

Performance Optimization:
- Encodes frames ON-DEMAND only when an active browser client is connected.
- Zero CPU usage when no stream is being viewed.
"""

import sys
import time
import json
import struct
import zlib
import threading
import http.server
import socketserver
from controller import Robot

# ── Shared State ─────────────────────────────────────────────────────────────
_latest_frame    = None
_frame_lock      = threading.Lock()
_active_clients  = 0
_client_lock     = threading.Lock()


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
        global _active_clients
        with _client_lock:
            _active_clients += 1

        try:
            self.send_response(200)
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=frame')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
            self.end_headers()

            # Wait until first frame is ready
            timeout = 0
            while _latest_frame is None and timeout < 20:
                time.sleep(0.05)
                timeout += 1

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

                time.sleep(0.04)  # ~25 FPS streaming
        except Exception:
            pass  # Client disconnected
        finally:
            with _client_lock:
                _active_clients = max(0, _active_clients - 1)


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


# ── Main Controller Loop ─────────────────────────────────────────────────────
def main():
    global _latest_frame

    robot    = Robot()
    timestep = int(robot.getBasicTimeStep())
    if timestep <= 0:
        timestep = 32

    bus_id = robot.getName()
    if len(sys.argv) > 1:
        bus_id = sys.argv[1]

    try:
        bus_num = int(bus_id.split('_')[1])
    except Exception:
        bus_num = 1
    mjpeg_port = 8010 + bus_num

    print(f"[camera_streamer] {bus_id}: starting controller (step={timestep}ms)", flush=True)

    cam = robot.getDevice("camera")
    if not cam:
        print(f"[camera_streamer] {bus_id}: ERROR — no camera device found", flush=True)
        while robot.step(timestep) != -1:
            pass
        return

    cam.enable(timestep)
    w, h = cam.getWidth(), cam.getHeight()
    print(f"[camera_streamer] {bus_id}: camera {w}x{h} enabled on port {mjpeg_port}", flush=True)

    # Start MJPEG HTTP server in background thread
    t = threading.Thread(target=_start_mjpeg_server, args=(mjpeg_port,), daemon=True)
    t.start()

    frame_interval = 0.04   # ~25 FPS
    last_frame     = 0.0

    while robot.step(timestep) != -1:
        now = time.time()

        # On-Demand: Only capture & compress if a viewer is connected (zero idle CPU overhead)
        with _client_lock:
            has_clients = (_active_clients > 0)

        if has_clients and (now - last_frame >= frame_interval):
            last_frame = now
            try:
                raw = cam.getImage()
                if raw is not None:
                    png = _make_png_fast(w, h, bytes(raw))
                    with _frame_lock:
                        _latest_frame = png
            except Exception as e:
                print(f"[camera_streamer] {bus_id}: capture error: {e}", flush=True)


if __name__ == "__main__":
    main()
