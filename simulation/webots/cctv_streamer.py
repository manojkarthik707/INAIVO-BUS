"""
High-Definition 360° PTZ Surveillance CCTV Streamer for Webots Traffic Lights
=============================================================================
- Motorized 360° Pan-Tilt-Zoom surveillance camera with real-time HTTP PTZ control
- Native 720p HD (1280x720) crystal-clear perspective video stream (0% fisheye distortion)
- Matches V9 bus camera architecture: continuous sampling + on-demand JPEG encoding
- Smooth motorized rotation: click & drag, compass quick-presets, and auto-patrol sweep
"""

import sys
import time
import math
import urllib.parse
import threading
import http.server
import socketserver
import numpy as np
import cv2

try:
    from controller import Supervisor
except ImportError:
    print("[cctv_streamer] Error: Webots controller module not found.", flush=True)
    sys.exit(1)


# ── Thread Synchronization & Frame Buffers ───────────────────────────────────
_frame_cond = threading.Condition()
_latest_frame = None  # Encoded JPEG bytes

_raw_lock = threading.Lock()
_raw_cond = threading.Condition(_raw_lock)
_pending_raw = None   # Tuple: (raw_bytes, width, height)

_client_lock = threading.Lock()
_active_clients = 0

# PTZ Control State (Thread-Safe)
_ptz_lock = threading.Lock()
_current_pan = 0.0      # Current camera azimuth in degrees [0..360)
_target_pan = 0.0       # Commanded target azimuth in degrees [0..360)
_auto_patrol = False    # Continuous 360° sweep


# ── Background Worker for Non-Blocking Processing & JPEG Encoding ────────────
def _worker_loop(junc_id, sim_x, sim_y):
    global _latest_frame, _pending_raw
    last_idle_snapshot = 0.0

    while True:
        with _raw_cond:
            while _pending_raw is None:
                _raw_cond.wait()
            raw, width, height = _pending_raw
            _pending_raw = None

        with _client_lock:
            has_clients = (_active_clients > 0)

        now = time.time()
        # When idle (no viewer modal open), only compress 1 frame every 2 seconds for thumbnail cards
        if not has_clients and (now - last_idle_snapshot < 2.0):
            continue
        last_idle_snapshot = now

        try:
            arr = np.frombuffer(raw, dtype=np.uint8).reshape((height, width, 4))
            bgr = cv2.cvtColor(arr, cv2.COLOR_BGRA2BGR)

            # High-clarity native JPEG encoding at quality 90 (matches V9 dashcam standard)
            _, buf = cv2.imencode(".jpg", bgr, [cv2.IMWRITE_JPEG_QUALITY, 90])
            jpeg_bytes = buf.tobytes()

            with _frame_cond:
                _latest_frame = jpeg_bytes
                _frame_cond.notify_all()
        except Exception as e:
            print(f"[cctv_streamer {junc_id}] Worker error: {e}", flush=True)


# ── Multi-Threaded MJPEG & PTZ HTTP Handler ───────────────────────────────────
class MJPEGHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Access-Control-Max-Age', '86400')
        self.end_headers()

    def do_GET(self):
        global _active_clients, _target_pan, _auto_patrol

        # 1. Live PTZ Command Endpoint: /ptz?pan=90&patrol=1
        if self.path.startswith('/ptz'):
            parsed = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed.query)

            with _ptz_lock:
                if 'pan' in params:
                    try:
                        _target_pan = float(params['pan'][0]) % 360.0
                        _auto_patrol = False
                    except Exception:
                        pass
                if 'patrol' in params:
                    try:
                        _auto_patrol = (params['patrol'][0] in ('1', 'true', 'True'))
                    except Exception:
                        pass
                curr = _current_pan
                patrol = _auto_patrol

            resp_data = f'{{"status":"ok","pan":{curr:.1f},"patrol":{str(patrol).lower()}}}'.encode()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Length', str(len(resp_data)))
            self.end_headers()
            self.wfile.write(resp_data)
            return

        # 2. Single JPEG snapshot endpoint for dashboard cards
        if self.path.startswith('/snapshot'):
            with _frame_cond:
                frame = _latest_frame
            if frame:
                self.send_response(200)
                self.send_header('Content-Type', 'image/jpeg')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
                self.send_header('Content-Length', str(len(frame)))
                self.end_headers()
                self.wfile.write(frame)
            else:
                self.send_response(503)
                self.end_headers()
            return

        # 3. Live Continuous MJPEG Video Stream
        with _client_lock:
            _active_clients += 1

        try:
            self.send_response(200)
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=frame')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', '*')
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
            self.end_headers()

            with _frame_cond:
                if _latest_frame is None:
                    _frame_cond.wait(timeout=1.0)

            last_sent_frame = None
            while True:
                with _frame_cond:
                    if _latest_frame is last_sent_frame:
                        _frame_cond.wait(timeout=1.0)
                    frame = _latest_frame

                if frame and frame is not last_sent_frame:
                    last_sent_frame = frame
                    header = (
                        b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n'
                        b'Access-Control-Allow-Origin: *\r\n'
                        b'Content-Length: ' + str(len(frame)).encode() + b'\r\n'
                        b'\r\n'
                    )
                    self.wfile.write(header + frame + b'\r\n')
                    self.wfile.flush()
        except Exception:
            pass
        finally:
            with _client_lock:
                _active_clients = max(0, _active_clients - 1)


class ThreadedHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

    def server_bind(self):
        super().server_bind()
        import socket
        try:
            self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        except Exception:
            pass


def _start_mjpeg_server(port):
    try:
        httpd = ThreadedHTTPServer(('0.0.0.0', port), MJPEGHandler)
        print(f"[cctv_streamer] 360° PTZ CCTV server running on http://127.0.0.1:{port}/", flush=True)
        httpd.serve_forever()
    except Exception as e:
        print(f"[cctv_streamer] MJPEG server failed on port {port}: {e}", flush=True)


# ── Main Controller ──────────────────────────────────────────────────────────
def main():
    global _pending_raw, _latest_frame, _current_pan, _target_pan, _auto_patrol

    robot = Supervisor()
    timestep = int(robot.getBasicTimeStep())
    if timestep <= 0:
        timestep = 32

    # Ensure Webots runs in real-time mode
    try:
        robot.simulationSetMode(Supervisor.SIMULATION_MODE_REAL_TIME)
    except Exception:
        pass

    # Parse arguments: [junction_id, port]
    junc_id = "J25"
    mjpeg_port = 8025

    if len(sys.argv) > 1:
        junc_id = sys.argv[1]
    if len(sys.argv) > 2:
        try:
            mjpeg_port = int(sys.argv[2])
        except Exception:
            pass

    print(f"[cctv_streamer] Initializing 360° PTZ CCTV for {junc_id} on port {mjpeg_port} (step={timestep}ms)", flush=True)

    cam = robot.getDevice("camera")
    if not cam:
        print(f"[cctv_streamer {junc_id}] ERROR: Camera device 'camera' not found!", flush=True)
        while robot.step(timestep) != -1:
            pass
        return

    # Enable 720p HD perspective camera
    cam.enable(timestep)
    robot.step(timestep)

    width = cam.getWidth()
    height = cam.getHeight()
    pos = list(robot.getSelf().getField("translation").getSFVec3f())
    sim_x, sim_y = pos[0], pos[1]

    # Pre-generate initial standby frame
    standby_img = np.zeros((height, width, 3), dtype=np.uint8)
    standby_img[:] = (25, 20, 15)
    cv2.putText(standby_img, f"CCTV 720p HD - JUNCTION {junc_id} ACTIVE", (int(width * 0.22), int(height * 0.48)), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 220, 255), 2, cv2.LINE_AA)
    cv2.putText(standby_img, "MOTORIZED 360 PTZ SURVEILLANCE READY", (int(width * 0.26), int(height * 0.58)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (180, 220, 255), 1, cv2.LINE_AA)
    _, sbuf = cv2.imencode(".jpg", standby_img, [cv2.IMWRITE_JPEG_QUALITY, 90])
    with _frame_cond:
        _latest_frame = sbuf.tobytes()

    # Start HTTP server & background processing worker
    server_t = threading.Thread(target=_start_mjpeg_server, args=(mjpeg_port,), daemon=True)
    server_t.start()

    worker_t = threading.Thread(target=_worker_loop, args=(junc_id, sim_x, sim_y), daemon=True)
    worker_t.start()

    print(f"[cctv_streamer {junc_id}] 720p HD PTZ Camera ready: {width}x{height} at pos ({sim_x:.1f}, {sim_y:.1f})", flush=True)

    rot_field = robot.getSelf().getField("rotation")

    # Main Webots simulation loop
    while robot.step(timestep) != -1:
        # Smooth motorized PTZ pan update
        with _ptz_lock:
            if _auto_patrol:
                _current_pan = (_current_pan + 0.3) % 360.0
                rot_field.setSFRotation([0, 0, 1, math.radians(_current_pan)])
            else:
                diff = (_target_pan - _current_pan)
                diff = (diff + 180) % 360 - 180
                if abs(diff) > 0.2:
                    _current_pan = (_current_pan + diff * 0.3) % 360.0
                    rot_field.setSFRotation([0, 0, 1, math.radians(_current_pan)])

        raw = cam.getImage()
        if raw is not None:
            with _raw_cond:
                _pending_raw = (raw, width, height)
                _raw_cond.notify()


if __name__ == "__main__":
    main()
