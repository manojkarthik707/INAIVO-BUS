import os, sys, time, math, threading, logging
from collections import deque
import requests
from concurrent.futures import ThreadPoolExecutor

webots_home = os.environ.get("WEBOTS_HOME", r"C:\Users\Moghul Kannan N\AppData\Local\Programs\Webots")
if "WEBOTS_HOME" not in os.environ:
    os.environ["WEBOTS_HOME"] = webots_home
webots_python_path = os.path.join(webots_home, "lib", "controller", "python")
if os.path.exists(webots_python_path) and webots_python_path not in sys.path:
    sys.path.append(webots_python_path)

try:
    from controller import Supervisor
    HAS_SUPERVISOR = True
except ImportError:
    HAS_SUPERVISOR = False
    logging.warning("Webots Supervisor module not found.")

from ai.detector import ObjectDetector
from ai.pedestrian_risk import PedestrianRiskEngine

logger = logging.getLogger(__name__)

# ─── SUMO Lane-Sampled Precise Route Waypoints (Full City Loop) ──────────────
BUS_ROUTE = [
    (4.36, 53.21), (-34.25, 53.21), (-55.75, 53.65), (-69.28, 52.99), (-74.01, 52.28), 
    (-78.64, 51.12), (-83.15, 49.51), (-87.47, 47.47), (-91.57, 45.01), (-95.41, 42.16), 
    (-98.95, 38.95), (-102.16, 35.41), (-105.01, 31.57), (-107.47, 27.47), (-109.51, 23.14), 
    (-111.12, 18.64), (-112.29, 14.0), (-112.99, 9.27), (-113.2, 5.04), (-113.21, -64.36), 
    (-112.99, -69.28), (-112.29, -74.01), (-111.12, -78.64), (-109.51, -83.15), (-107.47, -87.47), 
    (-105.01, -91.57), (-102.16, -95.41), (-98.95, -98.95), (-95.41, -102.16), (-91.57, -105.01), 
    (-87.47, -107.47), (-83.15, -109.51), (-78.64, -111.13), (-74.01, -112.29), (-69.28, -112.99), 
    (-65.04, -113.2), (4.36, -113.21), (9.28, -112.99), (14.0, -112.29), (18.64, -111.13), 
    (23.14, -109.52), (27.47, -107.47), (31.57, -105.01), (35.41, -102.16), (38.95, -98.95), 
    (42.16, -95.41), (45.01, -91.57), (47.47, -87.47), (49.51, -83.15), (51.12, -78.65), 
    (52.29, -74.01), (52.99, -69.28), (53.65, -55.75), (55.75, -53.65), (69.28, -52.99), 
    (74.0, -52.29), (78.64, -51.13), (83.14, -49.52), (87.47, -47.47), (91.57, -45.01), 
    (95.41, -42.16), (98.95, -38.95), (102.16, -35.41), (105.01, -31.57), (107.47, -27.47), 
    (109.51, -23.15), (111.12, -18.65), (112.29, -14.01), (112.99, -9.28), (113.2, -5.04), 
    (113.21, 82.25), (94.25, 101.21), (76.64, 101.21), (73.34, 101.38), (70.2, 101.84), 
    (67.13, 102.61), (64.15, 103.68), (61.29, 105.03), (58.57, 106.66), (56.02, 108.55), 
    (53.68, 110.67), (51.55, 113.02), (49.66, 115.56), (48.03, 118.28), (46.68, 121.15), 
    (45.61, 124.13), (44.84, 127.2), (44.38, 130.33), (44.2, 133.9), (43.99, 138.27), 
    (43.29, 143.0), (42.12, 147.64), (40.51, 152.14), (38.47, 156.47), (36.01, 160.57), 
    (33.16, 164.41), (29.95, 167.95), (26.41, 171.16), (22.57, 174.01), (18.47, 176.47), 
    (14.15, 178.51), (9.64, 180.12), (5.01, 181.28), (0.28, 181.99), (-3.56, 182.17), 
    (-5.44, 182.17), (-9.28, 181.99), (-14.01, 181.28), (-18.64, 180.12), (-23.15, 178.51), 
    (-27.47, 176.47), (-31.57, 174.01), (-35.41, 171.16), (-38.95, 167.95), (-42.16, 164.41), 
    (-45.01, 160.57), (-47.47, 156.47), (-49.51, 152.14), (-51.12, 147.64), (-52.29, 143.0), 
    (-52.99, 138.27), (-53.2, 134.04), (-53.21, 55.75), (-34.25, 36.79), (4.36, 36.79), 
    (7.66, 36.62), (10.8, 36.16), (13.87, 35.39), (16.85, 34.32), (19.72, 32.96), 
    (22.43, 31.34), (24.98, 29.45), (27.32, 27.32), (29.45, 24.97), (31.34, 22.43), 
    (32.97, 19.71), (34.32, 16.85), (35.39, 13.87), (36.16, 10.8), (36.62, 7.66), 
    (36.79, 4.23), (36.79, -34.25), (53.21, -34.25), (53.21, 4.36), (52.99, 9.27), 
    (52.29, 14.0), (51.12, 18.64), (49.51, 23.14), (47.47, 27.47), (45.01, 31.57), 
    (42.16, 35.41), (38.95, 38.95), (35.41, 42.16), (31.57, 45.01), (27.47, 47.47), 
    (23.15, 49.51), (18.64, 51.12), (14.01, 52.28), (9.28, 52.99), (5.04, 53.19)
]

BUS_SPEED = 0.28    # metres per 32ms step (~32 km/h realistic urban bus speed)

def _bearing(x0,y0,x1,y1):
    return math.atan2(y1-y0, x1-x0)

def _dist(x0,y0,x1,y1):
    return math.hypot(x1-x0, y1-y0)


class WebotsSimulatorAdapter:
    def __init__(self, backend_url="http://localhost:8000"):
        self.backend_url  = backend_url
        self.running      = False
        self.supervisor   = None
        self.camera       = None
        self.gps          = None
        self.time_step    = 32
        self.bus_heading  = math.pi
        self._wp_idx      = 0
        self._executor    = ThreadPoolExecutor(max_workers=2)
        self.detector     = ObjectDetector()
        self.risk_engine  = PedestrianRiskEngine()

    # ── Lifecycle ─────────────────────────────────────────────────────────────
    def start(self):
        if not HAS_SUPERVISOR:
            raise RuntimeError("Webots Python API not available.")
        self.running = True
        # Connect ONCE here — Supervisor cannot be recreated per process
        try:
            self._connect()
        except SystemExit:
            logger.error("Could not connect to Webots. Is Webots running on port 2345?")
            self.running = False
            return
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if hasattr(self, "thread"):
            self.thread.join(timeout=2.0)

    # ── Connection (called once) ───────────────────────────────────────────────
    def _connect(self):
        logger.info("Connecting to Webots on port 2345...")
        os.environ["WEBOTS_ROBOT_NAME"] = "BUS_01"
        self.supervisor = Supervisor()
        self.time_step = int(self.supervisor.getBasicTimeStep())
        
        self.cams = {}
        self.gps_nodes = {}
        self._bus_nodes = []  # cached bus nodes, scanned once
        self._cam_robots = []  # cached CAM_ solid nodes
        
        for i in range(1, 4):
            cam = self.supervisor.getDevice(f"FRONT_RGB_CAMERA_{i}")
            if cam:
                cam.enable(self.time_step)
                self.cams[f"BUS_0{i}"] = cam
                logger.info(f"Camera {i} enabled ({cam.getWidth()}x{cam.getHeight()})")
                
            gps = self.supervisor.getDevice(f"GPS_{i}")
            if gps:
                gps.enable(self.time_step)
                self.gps_nodes[f"BUS_0{i}"] = gps
                logger.info(f"GPS {i} enabled")
        
        # Pre-cache CAM solid nodes
        for i in range(1, 4):
            node = self.supervisor.getFromDef(f"CAM_{i}")
            self._cam_robots.append(node)

    # ── Main loop ─────────────────────────────────────────────────────────────
    def _run_loop(self):
        last_ai = 0.0
        last_frame = 0.0
        last_bus_scan = 0.0
        
        # Increase workers to handle 30 FPS streaming across 3 buses
        self._executor = ThreadPoolExecutor(max_workers=12)
        
        # Run at basicTimeStep (32ms = ~31 FPS sim) — perfectly synced with SUMO stepSize=32
        sim_step = self.time_step  # 32ms
        
        while self.running:
            try:
                ret = self.supervisor.step(sim_step)
                if ret == -1:
                    logger.warning("Webots simulation stopped.")
                    break

                now = time.time()
                
                # Re-scan for bus nodes every 5 seconds (cheap, handles late spawns)
                if now - last_bus_scan >= 5.0 or not self._bus_nodes:
                    self._scan_buses()
                    last_bus_scan = now

                # Mount cameras onto bus positions every tick (fast, uses cached nodes)
                self._step_bus()

                # Video & Telemetry at 30 FPS (approx 0.033s)
                if now - last_frame >= 0.033:
                    run_ai = (now - last_ai >= 0.25)  # AI at 4 FPS to reduce load
                    if run_ai:
                        last_ai = now
                    
                    self._executor.submit(self._background_frame, run_ai)
                    last_frame = now

            except Exception as e:
                logger.error(f"Run-loop: {e}")
                self.supervisor = None
                time.sleep(3)

    # ── Bus Node Scanner (called every 5s to handle late spawns) ─────────────
    def _scan_buses(self):
        """Scan all SUMO vehicles to find buses by PROTO type. Cached to avoid per-tick overhead."""
        found = []
        for j in range(300):
            node = self.supervisor.getFromDef(f"SUMO_VEHICLE{j}")
            if node and "bus" in node.getTypeName().lower():
                found.append(node)
                if len(found) == 3:
                    break
        
        # Pad to always have 3 entries
        fallback = self.supervisor.getFromDef("SUMO_VEHICLE0")
        while len(found) < 3:
            found.append(fallback)
        
        self._bus_nodes = found
        logger.info(f"Bus scan: found {len([n for n in found if n])} buses")

    # ── Real-Time Sensor Mount on Lead Bus ────────────────────────────────────
    def _step_bus(self):
        """Mount the AI cameras onto cached bus node positions. Ultra-fast, no scanning."""
        if not self._bus_nodes:
            return
        try:
            import math
            for i, leader in enumerate(self._bus_nodes[:3]):
                cam_robot = self._cam_robots[i] if i < len(self._cam_robots) else None
                if not cam_robot or not leader:
                    continue

                pos = leader.getField("translation").getSFVec3f()
                rot = leader.getField("rotation").getSFRotation()
                if abs(pos[0]) < 5000 and abs(pos[1]) < 5000 and pos[2] > -5.0:
                    yaw = self._extract_yaw(rot)
                    offset_x = 9.5 * math.cos(yaw)
                    offset_y = 9.5 * math.sin(yaw)
                    cam_robot.getField("translation").setSFVec3f([pos[0] + offset_x, pos[1] + offset_y, pos[2] + 4.5])
                    cam_robot.getField("rotation").setSFRotation(rot)
                    if i == 0:
                        self.bus_heading = yaw
        except Exception as e:
            logger.debug(f"Sensor mount step: {e}")

    def _extract_yaw(self, rot):
        """Extract yaw angle from Webots axis-angle rotation."""
        if len(rot) >= 4:
            ax, ay, az, angle = rot[0], rot[1], rot[2], rot[3]
            if abs(az) > 0.5:
                return angle if az > 0 else -angle
            elif abs(ay) > 0.5:
                return angle if ay > 0 else -angle
        return self.bus_heading

    def _step_traffic(self):
        """Hide static dummy cars. SUMO natively handles all other traffic."""
        try:
            for car_def in ["CAR_1", "CAR_2", "CAR_3"]:
                node = self.supervisor.getFromDef(car_def)
                if node:
                    tf  = node.getField("translation")
                    pos = tf.getSFVec3f()
                    if pos[2] > -5:
                        tf.setSFVec3f([pos[0], pos[1], -10.0])
        except Exception as e:
            logger.debug(f"Traffic hide: {e}")

    # ── Background AI + telemetry (non-blocking) ──────────────────────────────
    def _background_frame(self, run_ai=True):
        try:
            import base64, cv2, numpy as np
            
            for bus_id in [f"BUS_0{i}" for i in range(1, 4)]:
                try:
                    cam = self.cams.get(bus_id)
                    gps = self.gps_nodes.get(bus_id)
                    
                    if not cam:
                        continue
                        
                    gps_vals = gps.getValues() if gps else None
                    location = {"latitude": 11.0168, "longitude": 76.9558}
                    if gps_vals and len(gps_vals) >= 3:
                        location = {
                            "latitude":  11.0168 + gps_vals[0] * 0.0001,
                            "longitude": 76.9558 + gps_vals[2] * 0.0001,
                        }
                        
                    frame_b64, bgr = None, None
                    raw = cam.getImage()
                    if raw:
                        h,w = cam.getHeight(), cam.getWidth()
                        img = np.frombuffer(raw, np.uint8).reshape((h,w,4))
                        bgr = img[:,:,:3]
                        _, buf = cv2.imencode(".jpg", bgr, [cv2.IMWRITE_JPEG_QUALITY, 95])
                        frame_b64 = base64.b64encode(buf).decode("utf-8")
                        
                    telemetry = {
                        "bus_id": bus_id, "timestamp": time.time(),
                        "latitude": location["latitude"], "longitude": location["longitude"],
                        "speed": round(BUS_SPEED*50, 1) if 'BUS_SPEED' in globals() else 30.0, "status": "active",
                    }
                    if frame_b64:
                        telemetry["frame"] = frame_b64
                        
                    def _post_telemetry(url=f"{self.backend_url}/api/buses/{bus_id}/telemetry", data=telemetry):
                        try:
                            requests.post(url, json=data, timeout=0.5)
                        except Exception:
                            pass
                            
                    self._executor.submit(_post_telemetry)
                        
                    if run_ai and bgr is not None:
                        try:
                            import uuid
                            from datetime import datetime, timezone
                            for det in self.detector.detect(bgr):
                                if det.class_name in ["person","car","motorcycle","bicycle"]:
                                    payload = {
                                        "event_id": str(uuid.uuid4()),
                                        "event_type": f"{det.class_name.upper()}_DETECTED",
                                        "severity": "MEDIUM",
                                        "confidence": float(det.confidence),
                                        "timestamp": datetime.now(timezone.utc).isoformat(),
                                        "location": location,
                                        "source": {
                                            "type": "camera",
                                            "bus_id": bus_id,
                                            "camera_id": f"front_rgb_{bus_id}"
                                        },
                                        "metadata": {
                                            "description": f"YOLOv11: {det.class_name} @ {det.confidence:.2f}",
                                            "bbox": det.bbox,
                                            "track_id": det.track_id
                                        },
                                        "evidence_image": "mock_camera_frame.jpg"
                                    }
                                    
                                    def _post_event(p=payload):
                                        try:
                                            requests.post(f"{self.backend_url}/api/events", timeout=0.5, json=p)
                                        except Exception:
                                            pass
                                            
                                    self._executor.submit(_post_event)
                        except Exception as e:
                            logger.error(f"YOLO Event POST failed: {e}")
                except Exception as inner_e:
                    logger.debug(f"background_frame bus {bus_id}: {inner_e}")
                    
        except Exception as e:
            logger.debug(f"background_frame: {e}")

    # ── Scenario trigger ──────────────────────────────────────────────────────
    def trigger_event(self, event_type, severity):
        logger.info(f"Triggered {event_type}")
        if event_type == "PEDESTRIAN_RISK" and self.supervisor:
            try:
                ped = self.supervisor.getFromDef("PEDESTRIAN_01")
                bus = self.supervisor.getSelf()
                if ped and bus:
                    pos = list(bus.getPosition())
                    pos[0] += math.cos(self.bus_heading) * 12
                    pos[1] += math.sin(self.bus_heading) * 12
                    pos[2] += 0.5
                    ped.getField("translation").setSFVec3f(pos)
                    logger.info(f"Pedestrian teleported to {pos}")
            except Exception as e:
                logger.error(f"trigger_event: {e}")
