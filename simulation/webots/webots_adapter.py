import os, sys, time, math, threading, logging, base64
from collections import deque
import requests
import cv2
import numpy as np
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
    def __init__(self, backend_url="http://127.0.0.1:8000"):
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
        self.session      = requests.Session()

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
        self._bus_nodes = []  # cached bus nodes, scanned once
        # NOTE: cameras are handled by dedicated camera_streamer Robot controllers
        # in the .wbt file (CAM_ROBOT_1/2/3). No camera devices needed here.

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

            except Exception as e:
                logger.debug(f"Run-loop step transient: {e}")
                time.sleep(0.01)

    # ── Bus Node Scanner (called every 5s to handle late spawns) ─────────────
    def _scan_buses(self):
        """Scan all SUMO vehicles to find buses by model, name, or PROTO. Guarantees 3 distinct vehicles."""
        found = []
        candidates = []
        for j in range(200):
            try:
                node = self.supervisor.getFromDef(f"SUMO_VEHICLE{j}")
                if not node:
                    continue
                candidates.append(node)
                
                # Check model field, name field, and typeName
                model_str = ""
                name_str = ""
                type_str = ""
                try:
                    model_field = node.getField("model")
                    if model_field:
                        model_str = model_field.getSFString().lower()
                except Exception:
                    pass
                
                try:
                    name_field = node.getField("name")
                    if name_field:
                        name_str = name_field.getSFString().lower()
                except Exception:
                    pass
                
                try:
                    type_str = node.getTypeName().lower()
                except Exception:
                    pass
                
                is_bus = ("bus" in model_str) or ("bus" in name_str) or ("bus" in type_str)
                if is_bus:
                    found.append(node)
                    if len(found) == 3:
                        break
            except Exception:
                continue
        
        # If not enough buses found yet, fill with distinct active vehicles so cameras NEVER duplicate
        for cand in candidates:
            if len(found) >= 3:
                break
            if cand not in found:
                found.append(cand)
                
        # Final safety pad if very few vehicles spawned yet
        fallback_idx = 0
        while len(found) < 3:
            try:
                fb = self.supervisor.getFromDef(f"SUMO_VEHICLE{fallback_idx}")
                found.append(fb)
            except Exception:
                found.append(None)
            fallback_idx += 1
        
        self._bus_nodes = found[:3]
        logger.info(f"Bus scan: attached to {[n.getDef() if n else 'None' for n in self._bus_nodes]}")

    def _send_telem_async(self, bus_id, telem):
        try:
            self.session.post(f"{self.backend_url}/api/buses/{bus_id}/telemetry", json=telem, timeout=0.20)
        except Exception:
            pass

    # ── Real-Time Camera Mount & Bus Telemetry Broadcast ──────────────────────
    def _step_bus(self):
        """Mount AI cameras and broadcast real-time bus positions. Ultra-fast, non-blocking."""
        if not self._bus_nodes:
            return
        try:
            cam_defs = ["CAM_ROBOT_1", "CAM_ROBOT_2", "CAM_ROBOT_3"]
            bus_ids  = ["BUS_01", "BUS_02", "BUS_03"]
            now = time.time()
            send_telem = (now - getattr(self, "_last_bus_telem", 0.0)) >= 0.20
            if send_telem:
                self._last_bus_telem = now

            for i, leader in enumerate(self._bus_nodes[:3]):
                if not leader:
                    continue
                cam_robot = self.supervisor.getFromDef(cam_defs[i])
                pos = leader.getField("translation").getSFVec3f()
                rot = leader.getField("rotation").getSFRotation()
                if abs(pos[0]) < 5000 and abs(pos[1]) < 5000 and pos[2] > -5.0:
                    if cam_robot:
                        cam_robot.getField("translation").setSFVec3f(pos)
                        cam_robot.getField("rotation").setSFRotation(rot)
                    if i == 0:
                        self.bus_heading = self._extract_yaw(rot)
                    
                    if send_telem:
                        bus_id = bus_ids[i]
                        telem = {
                            "bus_id": bus_id,
                            "timestamp": now,
                            "sim_x": float(pos[0]),
                            "sim_y": float(pos[1]),
                            "latitude": 11.0168 + pos[0] * 0.0001,
                            "longitude": 76.9558 + pos[1] * 0.0001,
                            "speed": 35.0,
                            "status": "active"
                        }
                        self._executor.submit(self._send_telem_async, bus_id, telem)
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

    # ── Background Frame Processing Worker (executed in thread pool) ──────────
    def _process_frame(self, bus_id, img_array, location, run_ai):
        try:
            bgr = img_array[:, :, :3]
            _, buf = cv2.imencode(".jpg", bgr, [cv2.IMWRITE_JPEG_QUALITY, 90])
            frame_b64 = base64.b64encode(buf).decode("utf-8")
            
            telemetry = {
                "bus_id": bus_id,
                "timestamp": time.time(),
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "speed": 30.0,
                "status": "active",
                "frame": frame_b64
            }
            
            try:
                self.session.post(f"{self.backend_url}/api/buses/{bus_id}/telemetry", json=telemetry, timeout=1.0)
            except Exception as post_err:
                logger.debug(f"Telemetry post error: {post_err}")
                
            if run_ai and bgr is not None:
                try:
                    import uuid
                    from datetime import datetime, timezone
                    for det in self.detector.detect(bgr):
                        if det.class_name in ["person", "car", "motorcycle", "bicycle", "bus", "truck"]:
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
                            try:
                                self.session.post(f"{self.backend_url}/api/events", timeout=1.0, json=payload)
                            except Exception as ev_err:
                                logger.debug(f"Event post error: {ev_err}")
                except Exception as e:
                    logger.debug(f"YOLO detection error for {bus_id}: {e}")
        except Exception as e:
            logger.debug(f"_process_frame error for {bus_id}: {e}")

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
