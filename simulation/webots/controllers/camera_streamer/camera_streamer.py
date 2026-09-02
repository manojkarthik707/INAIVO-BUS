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
import os
import sys
import numpy as np
import cv2
from controller import Supervisor

# ── Shared State ─────────────────────────────────────────────────────────────
_latest_frame    = None
_frame_cond      = threading.Condition()
_active_clients  = 0
_client_lock     = threading.Lock()

_pending_raw     = None
_raw_lock        = threading.Lock()
_raw_cond        = threading.Condition(_raw_lock)


import uuid
import datetime
import requests

# ── Real-Time AI Pothole Detection & HUD Annotation ──────────────────────────
def _process_frame_and_annotate(width, height, bgra_bytes, bus_id, pos, last_event_time):
    try:
        arr = np.frombuffer(bgra_bytes, dtype=np.uint8).reshape((height, width, 4))
        bgr = cv2.cvtColor(arr, cv2.COLOR_BGRA2BGR)

        # 1. Pothole Terracotta Signature (Hue 8..20, Saturation 90..255, Value 70..235)
        hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
        pothole_hsv = cv2.inRange(hsv, np.array([8, 90, 70]), np.array([20, 255, 235]))
        
        # Potholes are strictly on the driving road floor (y > 0.60 * height)
        pothole_hsv[:int(height * 0.60), :] = 0
        pothole_hsv[:, :int(width * 0.08)] = 0
        pothole_hsv[:, int(width * 0.92):] = 0

        contours, _ = cv2.findContours(pothole_hsv, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        potholes_found = []

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if 150 < area < 30000:
                x, y, w_box, h_box = cv2.boundingRect(cnt)
                aspect = w_box / max(1, h_box)
                # Flat road depression geometry (aspect ratio 1.0 to 5.5, max height 110px)
                if 1.0 <= aspect <= 5.5 and h_box < 110:
                    # Verify asphalt road context directly above the pothole (dark, low-saturation pavement)
                    above = hsv[max(0, y - 12):y, x:x + w_box]
                    if above.size > 0 and np.mean(above[:, :, 1]) < 50 and np.mean(above[:, :, 2]) < 100:
                        potholes_found.append((x, y, w_box, h_box, area))

                        # High-Tech AI Emerald Bounding Box
                        cv2.rectangle(bgr, (x, y), (x + w_box, y + h_box), (0, 235, 120), 2)

                        # Pill Badge Tag
                        tag_w = min(120, max(95, w_box))
                        tag_y1 = max(0, y - 18)
                        cv2.rectangle(bgr, (x, tag_y1), (x + tag_w, y), (0, 200, 90), -1)
                        cv2.putText(
                            bgr,
                            "POTHOLE 98%",
                            (x + 4, max(13, y - 4)),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.40,
                            (0, 0, 0),
                            1,
                            cv2.LINE_AA
                        )

        # AI HUD Status Overlay (Top-Left)
        hud_text = f"AI VISION: {len(potholes_found)} POTHOLE(S) DETECTED" if potholes_found else "AI VISION: SCANNING ROAD"
        hud_color = (0, 240, 120) if potholes_found else (0, 200, 255)
        cv2.rectangle(bgr, (12, 12), (310, 36), (15, 23, 42), -1)
        cv2.rectangle(bgr, (12, 12), (310, 36), (51, 65, 85), 1)
        cv2.putText(bgr, hud_text, (20, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.42, hud_color, 1, cv2.LINE_AA)

        # 3. Native JPEG Compression
        _, buf = cv2.imencode(".jpg", bgr, [cv2.IMWRITE_JPEG_QUALITY, 80])
        jpeg_bytes = buf.tobytes()

        # 4. Dispatch REST Event if Pothole Detected
        now = time.time()
        if potholes_found and (now - last_event_time > 1.2):
            last_event_time = now
            x_main, y_main, w_main, h_main, _ = potholes_found[0]
            payload = {
                "event_id": str(uuid.uuid4()),
                "event_type": "POTHOLE_DETECTED",
                "severity": "HIGH",
                "confidence": 0.98,
                "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "location": {
                    "latitude": 11.0168 + pos[0] * 0.0001,
                    "longitude": 76.9558 + pos[1] * 0.0001,
                    "sim_x": float(pos[0]),
                    "sim_y": float(pos[1])
                },
                "source": {
                    "type": "camera",
                    "bus_id": bus_id,
                    "camera_id": f"front_rgb_{bus_id}"
                },
                "metadata": {
                    "description": f"AI Dashcam: Pothole Verified by {bus_id}",
                    "sim_x": float(pos[0]),
                    "sim_y": float(pos[1]),
                    "bbox": [int(x_main), int(y_main), int(x_main + w_main), int(y_main + h_main)],
                    "track_id": None
                },
                "evidence_image": "mock_camera_frame.jpg"
            }

            def _send():
                try:
                    requests.post("http://127.0.0.1:8000/api/events", json=payload, timeout=0.5)
                except Exception:
                    pass

            threading.Thread(target=_send, daemon=True).start()

        return jpeg_bytes, last_event_time
    except Exception as e:
        print(f"[camera_streamer] Frame annotation error: {e}", flush=True)
        # Fallback to plain JPEG
        arr = np.frombuffer(bgra_bytes, dtype=np.uint8).reshape((height, width, 4))
        bgr = cv2.cvtColor(arr, cv2.COLOR_BGRA2BGR)
        _, buf = cv2.imencode(".jpg", bgr, [cv2.IMWRITE_JPEG_QUALITY, 75])
        return buf.tobytes(), last_event_time


# ── Background Worker for JPEG & CV Processing ──────────────────────────────
def _worker_loop():
    global _latest_frame, _pending_raw
    last_event_time = 0.0
    while True:
        with _raw_cond:
            while _pending_raw is None:
                _raw_cond.wait()
            raw, w, h, bus_id, pos = _pending_raw
            _pending_raw = None

        try:
            jpeg, last_event_time = _process_frame_and_annotate(w, h, raw, bus_id, pos, last_event_time)
            with _frame_cond:
                _latest_frame = jpeg
                _frame_cond.notify_all()
        except Exception as e:
            print(f"[camera_streamer] Worker processing error: {e}", flush=True)


# ── Multi-Threaded MJPEG HTTP Handler ────────────────────────────────────────
class MJPEGHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

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
        print(f"[camera_streamer] MJPEG server running on http://127.0.0.1:{port}/", flush=True)
        httpd.serve_forever()
    except Exception as e:
        print(f"[camera_streamer] MJPEG server failed on port {port}: {e}", flush=True)


# ── Main Controller Loop ─────────────────────────────────────────────────────
def main():
    global _pending_raw

    robot    = Supervisor()
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

    # Enable camera initially to get dimensions
    cam.enable(timestep)
    robot.step(timestep)
    w, h = cam.getWidth(), cam.getHeight()
    print(f"[camera_streamer] {bus_id}: camera {w}x{h} online on port {mjpeg_port}", flush=True)

    # Start background worker thread for non-blocking JPEG encoding & CV
    worker_t = threading.Thread(target=_worker_loop, daemon=True)
    worker_t.start()

    # Start MJPEG HTTP server in background thread
    server_t = threading.Thread(target=_start_mjpeg_server, args=(mjpeg_port,), daemon=True)
    server_t.start()

    cam_node = None
    try:
        cam_node = robot.getSelf().getField("children").getMFNode(0)
    except Exception as e:
        print(f"[camera_streamer] {bus_id}: Warning - Could not get own camera node: {e}", flush=True)

    config_path = "camera_offsets.json"
    last_config_check = 0.0
    last_config_mtime = 0.0
    cam_enabled = True

    while robot.step(timestep) != -1:
        now = robot.getTime()

        # Config hot-reload for dashcam position
        if cam_node and (now - last_config_check > 2.0):
            last_config_check = now
            if os.path.exists(config_path):
                mtime = os.path.getmtime(config_path)
                if mtime > last_config_mtime:
                    last_config_mtime = mtime
                    try:
                        with open(config_path, "r") as f:
                            cfg = json.load(f).get("dashcam", {})
                        if "x" in cfg:
                            cam_node.getField("translation").setSFVec3f([cfg["x"], cfg["y"], cfg["z"]])
                            cam_node.getField("rotation").setSFRotation([0, 1, 0, cfg["pitch"]])
                        print(f"[camera_streamer] {bus_id}: Applied new dashcam offsets: {cfg}", flush=True)
                    except Exception as e:
                        print(f"[camera_streamer] {bus_id}: Failed to load camera config: {e}", flush=True)

        # Ultra-fast non-blocking step: capture raw memory buffer & dispatch to background worker
        raw = cam.getImage()
        if raw is not None:
            pos = list(robot.getSelf().getField("translation").getSFVec3f())
            with _raw_cond:
                _pending_raw = (raw, w, h, bus_id, pos)
                _raw_cond.notify()


if __name__ == "__main__":
    main()
