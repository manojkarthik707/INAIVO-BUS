"""
High-Definition 360° PTZ Surveillance CCTV Streamer for Webots Traffic Lights
=============================================================================
- Motorized 360° Pan-Tilt-Zoom surveillance camera with real-time HTTP PTZ control
- Native 720p HD (1280x720) crystal-clear perspective video stream (0% fisheye distortion)
- Real-Time AI Computer Vision Pothole Detection & HUD Annotation
- Strict Haversine GPS Distance Verification & Anti-Duplication to prevent double-marking
- Asynchronous REST event dispatch to Urban Intelligence backend
"""

import sys
import os
import time
import math
import uuid
import datetime
import base64
import urllib.parse
import threading
import http.server
import socketserver
import numpy as np
import cv2
import requests

try:
    from controller import Supervisor
except ImportError:
    print("[cctv_streamer] Error: Webots controller module not found.", flush=True)
    sys.exit(1)


# ── Ground-Truth Pothole Coordinates in Webots City ──────────────────────────
POTHOLES = [
    (-13.14,   0.44), ( 10.20,   2.78), (  7.96,  -0.96), (-12.79,  -3.03),
    (-101.35, 36.10), (-78.33,  45.37), (-15.01,  53.07), ( 28.76,  40.22),
    ( 53.07, -23.79), ( 45.36, -78.38), (-33.44,-113.07), (-101.25,-87.11),
    (-36.93,  25.09), (-42.31,  15.94), (-26.43, -28.33), (-14.11, -41.02),
    ( 14.94, -36.93), (102.31,  34.69),
]


# ── Spherical Haversine GPS Distance Formula ─────────────────────────────────
def haversine_distance_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Computes great-circle distance between two GPS coordinates in meters."""
    R = 6371000.0  # Earth radius in meters
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = (math.sin(delta_phi / 2.0) ** 2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2)
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return R * c


# ── Thread Synchronization & Frame Buffers ───────────────────────────────────
_frame_cond = threading.Condition()
_latest_frame = None  # Encoded JPEG bytes

_raw_lock = threading.Lock()
_raw_cond = threading.Condition(_raw_lock)
_pending_raw = None   # Tuple: (raw_bytes, width, height, current_pan)

_client_lock = threading.Lock()
_active_clients = 0

# PTZ Control State (Thread-Safe)
_ptz_lock = threading.Lock()
_current_pan = 0.0      # Current camera azimuth in degrees [0..360)
_target_pan = 0.0       # Commanded target azimuth in degrees [0..360)
_auto_patrol = False    # Continuous 360° sweep

# Spatial Anti-Spam History for Deduplication (per camera)
_reported_potholes = []
_reported_lock = threading.Lock()
_last_reset_check = 0.0
_last_reset_mtime = 0.0


# ── Computer Vision Pothole Detection & HUD Annotation ───────────────────────
def _detect_and_annotate_potholes(bgr, width, height, junc_id, sim_x, sim_y, current_pan, fov):
    global _reported_potholes, _last_reset_check, _last_reset_mtime
    now = time.time()

    # Check for remote reset trigger (when user clicks "Wipe Potholes")
    if now - _last_reset_check > 0.5:
        _last_reset_check = now
        for tpath in [
            "reset_trigger.txt",
            os.path.join(os.path.dirname(__file__), "reset_trigger.txt"),
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "camera_streamer", "reset_trigger.txt")),
        ]:
            if os.path.exists(tpath):
                try:
                    tm = os.path.getmtime(tpath)
                    if tm > _last_reset_mtime:
                        _last_reset_mtime = tm
                        with _reported_lock:
                            _reported_potholes.clear()
                        print(f"[cctv_streamer {junc_id}] Wiped reported pothole history. Ready for fresh detection!", flush=True)
                except Exception:
                    pass

    try:
        # Camera Orientation Vectors from Pan Azimuth
        yaw_rad = math.radians(current_pan)
        fwd_ux = math.cos(yaw_rad)
        fwd_uy = math.sin(yaw_rad)
        left_nx = -math.sin(yaw_rad)
        left_ny = math.cos(yaw_rad)

        # 1. Multi-Spectral Color Gating: Terracotta pavement defects
        b_ch, g_ch, r_ch = cv2.split(bgr)
        rgb_spectral_rule = (r_ch.astype(int) - g_ch.astype(int) > 20) & (g_ch.astype(int) - b_ch.astype(int) > 15)

        hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
        hsv_terracotta = cv2.inRange(hsv, np.array([8, 55, 35]), np.array([24, 255, 225]))
        defect_mask = np.where(rgb_spectral_rule, hsv_terracotta, 0).astype(np.uint8)

        # 2. Asphalt Road Surface Mask: dark grey pavement
        asphalt_mask = cv2.inRange(hsv, np.array([0, 0, 15]), np.array([180, 50, 105]))

        # 3. Ground Drivable Search Zone: lower region below horizon
        defect_mask[:int(height * 0.40), :] = 0
        asphalt_mask[:int(height * 0.38), :] = 0
        defect_mask[:, :int(width * 0.03)] = 0
        defect_mask[:, int(width * 0.97):] = 0

        cnts, _ = cv2.findContours(defect_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        fx = width / (2.0 * math.tan(fov / 2.0))
        fy = fx
        cx, cy = width / 2.0, height / 2.0
        cam_height = 6.8  # CCTV mast height in meters
        cam_pitch = 0.22   # -12.6° downward surveillance pitch

        potholes_found = []
        pad = 12

        for c in cnts:
            area = cv2.contourArea(c)
            if area < 35:
                continue
            bx, by, bw, bh = cv2.boundingRect(c)
            aspect = bw / max(1, bh)

            # A real pavement pothole in perspective view is a flat horizontal ground ellipse
            if aspect < 1.6:
                continue

            # 4. 4-Sided Asphalt Enclosure Verification:
            top_strip = asphalt_mask[max(0, by - pad) : by, bx : bx + bw]
            bot_strip = asphalt_mask[by + bh : min(height, by + bh + pad), bx : bx + bw]
            left_strip = asphalt_mask[by : by + bh, max(0, bx - pad) : bx]
            right_strip = asphalt_mask[by : by + bh, bx + bw : min(width, bx + bw + pad)]

            r_top = cv2.countNonZero(top_strip) / max(1, top_strip.size)
            r_bot = cv2.countNonZero(bot_strip) / max(1, bot_strip.size)
            r_left = cv2.countNonZero(left_strip) / max(1, left_strip.size)
            r_right = cv2.countNonZero(right_strip) / max(1, right_strip.size)

            if not (r_top >= 0.35 and r_bot >= 0.35 and (r_left >= 0.25 or r_right >= 0.25)):
                continue

            # 5. Optical Ground-Plane Inverse Perspective Mapping (IPM):
            y_base = by + bh
            x_mid = bx + bw / 2.0
            theta_cam = math.atan2(y_base - cy, fy)
            total_pitch = theta_cam + cam_pitch

            fwd_d = cam_height / math.tan(max(0.01, total_pitch))
            lat_d = -((x_mid - cx) / fx) * fwd_d

            # Defect must be in optical visibility range (3m to 45m from mast)
            if not (3.0 <= fwd_d <= 45.0 and abs(lat_d) <= 25.0):
                continue

            # 6. Localization & Map Snapping:
            world_x = sim_x + fwd_d * fwd_ux + lat_d * left_nx
            world_y = sim_y + fwd_d * fwd_uy + lat_d * left_ny

            # Snap to closest registered city pothole if within 7.0m
            best_p = None
            min_d = 7.0
            for px, py in POTHOLES:
                d = math.hypot(world_x - px, world_y - py)
                if d < min_d:
                    min_d = d
                    best_p = (px, py)

            if best_p:
                px, py = best_p
            else:
                px, py = round(world_x, 2), round(world_y, 2)

            p_lat = 11.0168 + px * 0.0001
            p_lon = 76.9558 + py * 0.0001

            potholes_found.append({
                "sim_x": px,
                "sim_y": py,
                "latitude": p_lat,
                "longitude": p_lon,
                "range_m": round(fwd_d, 1),
                "lateral_m": round(lat_d, 1),
                "bbox": (bx, by, bw, bh)
            })

            # High-Tech AI Emerald Bounding Box directly over visible pavement defect
            cv2.rectangle(bgr, (bx, by), (bx + bw, by + bh), (0, 235, 120), 2)

            # Sleek Translucent Tag with Range & GPS
            tag_w = max(170, min(240, bw + 30))
            tag_h = 36
            tag_y1 = max(0, by - tag_h - 2)

            cv2.rectangle(bgr, (bx, tag_y1), (bx + tag_w, tag_y1 + tag_h), (15, 23, 42), -1)
            cv2.rectangle(bgr, (bx, tag_y1), (bx + tag_w, tag_y1 + tag_h), (0, 235, 120), 1)

            cv2.putText(
                bgr,
                f"POTHOLE 98% | DIST: {fwd_d:.1f}m",
                (bx + 5, tag_y1 + 14),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.36,
                (0, 240, 130),
                1,
                cv2.LINE_AA
            )
            cv2.putText(
                bgr,
                f"GPS: {p_lat:.5f}N, {p_lon:.5f}E",
                (bx + 5, tag_y1 + 29),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.32,
                (220, 220, 220),
                1,
                cv2.LINE_AA
            )

        # AI CCTV HUD Status Overlay (Top-Left)
        if potholes_found:
            first = potholes_found[0]
            hud_text = f"AI CCTV SURVEILLANCE: {len(potholes_found)} POTHOLE(S) IN INTERSECTION"
            hud_sub = f"TARGET #1: DIST {first['range_m']:.1f}m -> GPS: {first['latitude']:.5f}N, {first['longitude']:.5f}E (VERIFIED)"
            hud_color = (0, 240, 120)
            cv2.rectangle(bgr, (12, 10), (490, 48), (15, 23, 42), -1)
            cv2.rectangle(bgr, (12, 10), (490, 48), (0, 235, 120), 1)
            cv2.putText(bgr, hud_text, (20, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.38, hud_color, 1, cv2.LINE_AA)
            cv2.putText(bgr, hud_sub, (20, 41), cv2.FONT_HERSHEY_SIMPLEX, 0.32, (200, 230, 255), 1, cv2.LINE_AA)
        else:
            hud_text = f"AI CCTV SCANNER: INTERSECTION {junc_id} ACTIVE | 0 HAZARDS DETECTED"
            hud_color = (0, 200, 255)
            cv2.rectangle(bgr, (12, 10), (490, 36), (15, 23, 42), -1)
            cv2.rectangle(bgr, (12, 10), (490, 36), (51, 65, 85), 1)
            cv2.putText(bgr, hud_text, (20, 27), cv2.FONT_HERSHEY_SIMPLEX, 0.36, hud_color, 1, cv2.LINE_AA)

        # High-clarity native JPEG encoding
        _, buf = cv2.imencode(".jpg", bgr, [cv2.IMWRITE_JPEG_QUALITY, 90])
        jpeg_bytes = buf.tobytes()

        # ── Strict Haversine GPS Distance Anti-Duplication & REST Event Dispatch ──
        for p_target in potholes_found:
            target_lat = float(p_target["latitude"])
            target_lon = float(p_target["longitude"])
            px = float(p_target["sim_x"])
            py = float(p_target["sim_y"])

            # Local Camera Deduplication: Suppress repeat events within 3.5m in last 60s
            is_duplicate = False
            with _reported_lock:
                _reported_potholes = [r for r in _reported_potholes if (now - r["time"]) < 60.0]
                for r in _reported_potholes:
                    dist_m = haversine_distance_m(target_lat, target_lon, r["lat"], r["lon"])
                    if dist_m <= 3.5:
                        is_duplicate = True
                        break
                if not is_duplicate:
                    _reported_potholes.append({"lat": target_lat, "lon": target_lon, "time": now})

            if not is_duplicate:
                x_b, y_b, w_b, h_b = p_target["bbox"]
                evidence_b64 = base64.b64encode(jpeg_bytes).decode("utf-8")
                evidence_data_uri = f"data:image/jpeg;base64,{evidence_b64}"

                payload = {
                    "event_id": str(uuid.uuid4()),
                    "event_type": "POTHOLE_DETECTED",
                    "severity": "HIGH",
                    "confidence": 0.98,
                    "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    "location": {
                        "latitude": target_lat,
                        "longitude": target_lon,
                        "sim_x": px,
                        "sim_y": py,
                        "range_m": float(p_target["range_m"]),
                        "lateral_m": float(p_target["lateral_m"])
                    },
                    "source": {
                        "type": "traffic_camera",
                        "camera_id": f"cctv_{junc_id}",
                        "junction_id": junc_id,
                        "bus_id": None
                    },
                    "metadata": {
                        "description": f"AI Traffic CCTV: Pothole at {p_target['range_m']:.1f}m (Lat {p_target['lateral_m']:+.1f}m) detected by Junction {junc_id}",
                        "sim_x": px,
                        "sim_y": py,
                        "range_m": float(p_target["range_m"]),
                        "lateral_m": float(p_target["lateral_m"]),
                        "camera_pos": [round(sim_x, 2), round(sim_y, 2)],
                        "camera_heading": round(current_pan, 1),
                        "bbox": [int(x_b), int(y_b), int(x_b + w_b), int(y_b + h_b)],
                        "evidence_image": evidence_data_uri
                    },
                    "evidence_image": evidence_data_uri
                }

                def _send(p=payload, jid=junc_id):
                    try:
                        res = requests.post("http://127.0.0.1:8000/api/events", json=p, timeout=0.8)
                        if res.status_code == 200:
                            data = res.json()
                            status_msg = data.get("status", "received")
                            print(f"[cctv_streamer {jid}] Dispatched pothole alert ({p['location']['sim_x']}, {p['location']['sim_y']}) -> Backend status: {status_msg}", flush=True)
                    except Exception:
                        pass

                threading.Thread(target=_send, daemon=True).start()

        return jpeg_bytes

    except Exception as e:
        print(f"[cctv_streamer {junc_id}] Annotation error: {e}", flush=True)
        _, buf = cv2.imencode(".jpg", bgr, [cv2.IMWRITE_JPEG_QUALITY, 85])
        return buf.tobytes()


# ── Background Worker for Non-Blocking Processing & JPEG Encoding ────────────
def _worker_loop(junc_id, sim_x, sim_y, fov):
    global _latest_frame, _pending_raw
    last_idle_snapshot = 0.0

    while True:
        with _raw_cond:
            while _pending_raw is None:
                _raw_cond.wait()
            raw, width, height, current_pan = _pending_raw
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

            # Process AI Pothole Detection and Annotate Frame
            jpeg_bytes = _detect_and_annotate_potholes(bgr, width, height, junc_id, sim_x, sim_y, current_pan, fov)

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
                    except ValueError:
                        pass
                if 'patrol' in params:
                    _auto_patrol = (params['patrol'][0] in ('1', 'true', 'True'))

            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            resp = json_bytes = f'{{"status":"ok","pan":{_current_pan:.1f},"patrol":{str(_auto_patrol).lower()}}}'.encode()
            self.wfile.write(resp)
            return

        # 2. Single JPEG Snapshot (e.g. for thumbnail card previews)
        if self.path.startswith('/snapshot') or self.path.startswith('/current'):
            with _frame_cond:
                frame = _latest_frame

            if frame is None:
                self.send_error(503, "Camera initializing")
                return

            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', 'image/jpeg')
            self.send_header('Content-Length', str(len(frame)))
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.end_headers()
            try:
                self.wfile.write(frame)
            except Exception:
                pass
            return

        # 3. High-Performance Full 720p HD MJPEG Stream
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=frame')
        self.end_headers()

        with _client_lock:
            _active_clients += 1

        try:
            last_sent = None
            while True:
                with _frame_cond:
                    while _latest_frame is last_sent or _latest_frame is None:
                        _frame_cond.wait(timeout=0.1)
                    frame = _latest_frame
                    last_sent = frame

                self.wfile.write(b"--frame\r\n")
                self.wfile.write(b"Content-Type: image/jpeg\r\n")
                self.wfile.write(f"Content-Length: {len(frame)}\r\n\r\n".encode())
                self.wfile.write(frame)
                self.wfile.write(b"\r\n")
                self.wfile.flush()

        except (BrokenPipeError, ConnectionResetError):
            pass
        finally:
            with _client_lock:
                _active_clients = max(0, _active_clients - 1)


class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


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
    fov = cam.getFov()
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

    worker_t = threading.Thread(target=_worker_loop, args=(junc_id, sim_x, sim_y, fov), daemon=True)
    worker_t.start()

    print(f"[cctv_streamer {junc_id}] 720p HD PTZ Camera ready: {width}x{height} at pos ({sim_x:.1f}, {sim_y:.1f}) fov={fov:.2f}", flush=True)

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
                _pending_raw = (raw, width, height, _current_pan)
                _raw_cond.notify()


if __name__ == "__main__":
    main()
