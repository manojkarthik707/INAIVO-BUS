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

# ─── SUMO-mapped waypoints (netOffset 175.0, 187.51 applied) ─────────────────
# Bus starts at Webots (-55, 45.88) confirmed from BUS_01 translation in .wbt
# Route traces real road edges from sumo.net.xml

BUS_ROUTE = [
    (-55.00,  45.88),   # start (Edge -7 begin)
    (-34.25,  53.21),   # Edge -7 end
    (  9.28,  52.99),   # Edge -6 mid
    ( 36.79,   4.36),   # Edge 5 start
    ( 36.79, -34.25),   # Edge 5 end / -9 area
    ( -4.36, -36.79),   # Edge -9 end
    ( -4.36, -53.21),   # Edge 9 start
    ( 37.21, -55.75),   # Edge 4 start
    (  4.23, -96.79),   # Edge 4 end / -3 area
    (-64.36, -96.79),   # Edge -3 end
    (-96.79, -64.23),   # Edge 2 end
    (-113.21,  4.36),   # Edge 1 mid
    (-96.79,  37.21),   # Edge 0 mid
    (-55.75,  53.65),   # Edge -0 start -> loop back
]

# Traffic cars — simple back-and-forth on nearby straight segments
CAR1_ROUTE = [(-34.25, 53.21), (9.28, 52.99), (36.79, 4.36)]
CAR2_ROUTE = [(36.79, 4.36), (36.79, -34.25), (-4.36, -36.79)]
CAR3_ROUTE = [(-64.36, -96.79), (-4.36, -96.79), (37.21, -55.75)]

BUS_SPEED = 1.5    # metres per step  (smooth at 32ms timestep)
CAR_SPEED = 1.0

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
        self._leader_idx  = None
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
        self.camera = (self.supervisor.getDevice("FRONT_RGB_CAMERA")
                       or self.supervisor.getDevice("camera"))
        if self.camera:
            self.camera.enable(self.time_step)
            logger.info(f"Camera enabled ({self.camera.getWidth()}x{self.camera.getHeight()})")
        self.gps = (self.supervisor.getDevice("GPS")
                    or self.supervisor.getDevice("gps"))
        if self.gps:
            self.gps.enable(self.time_step)
            logger.info("GPS enabled")

    # ── Main loop ─────────────────────────────────────────────────────────────
    def _run_loop(self):
        last_ai = 0.0
        while self.running:
            try:
                ret = self.supervisor.step(self.time_step)
                if ret == -1:
                    logger.warning("Webots simulation stopped.")
                    break

                # Sync bus to SUMO traffic engine in real time
                self._step_bus()

                # AI + telemetry at 5 FPS in background thread
                now = time.time()
                if now - last_ai >= 0.2:
                    self._executor.submit(self._background_frame)
                    last_ai = now

            except Exception as e:
                logger.error(f"Run-loop: {e}")
                self.supervisor = None
                time.sleep(3)

    # ── Real-Time SUMO Vehicle Sync ──────────────────────────────────────────
    def _step_bus(self):
        """Sync BUS_01 directly to SUMO traffic simulation so it obeys all roads,
        lanes, turns, speed limits, and traffic lights natively."""
        try:
            bus = self.supervisor.getFromDef("BUS_01")
            if not bus:
                return

            leader = None
            if self._leader_idx is not None:
                node = self.supervisor.getFromDef(f"SUMO_VEHICLE{self._leader_idx}")
                if node:
                    pos = node.getField("translation").getSFVec3f()
                    # Active SUMO vehicles are inside city bounds (< 5000) and above ground
                    if abs(pos[0]) < 5000 and abs(pos[1]) < 5000 and pos[2] > -5.0:
                        leader = node

            # If no active leader or current leader finished its route, lock onto next active vehicle
            if not leader:
                for i in range(100):
                    node = self.supervisor.getFromDef(f"SUMO_VEHICLE{i}")
                    if node:
                        pos = node.getField("translation").getSFVec3f()
                        if abs(pos[0]) < 5000 and abs(pos[1]) < 5000 and pos[2] > -5.0:
                            leader = node
                            self._leader_idx = i
                            logger.info(f"BUS_01 locked onto SUMO_VEHICLE{i}")
                            break

            if leader:
                lp = leader.getField("translation").getSFVec3f()
                lr = leader.getField("rotation").getSFRotation()

                # Sync BUS_01 to the exact SUMO vehicle location on the road
                bus.getField("translation").setSFVec3f([lp[0], lp[1], 0.55])
                bus.getField("rotation").setSFRotation(lr)
                bus.resetPhysics()

                # Update heading
                self.bus_heading = self._extract_yaw(lr)

        except Exception as e:
            logger.debug(f"Bus sync step: {e}")

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
    def _background_frame(self):
        try:
            import base64, cv2, numpy as np
            gps_vals = self.gps.getValues() if self.gps else None
            location = {"latitude": 11.0168, "longitude": 76.9558}
            if gps_vals and len(gps_vals) >= 3:
                location = {
                    "latitude":  11.0168 + gps_vals[0] * 0.0001,
                    "longitude": 76.9558 + gps_vals[2] * 0.0001,
                }
            frame_b64, bgr = None, None
            if self.camera:
                raw = self.camera.getImage()
                if raw:
                    h,w = self.camera.getHeight(), self.camera.getWidth()
                    img = np.frombuffer(raw, np.uint8).reshape((h,w,4))
                    bgr = img[:,:,:3]
                    _, buf = cv2.imencode(".jpg", bgr, [cv2.IMWRITE_JPEG_QUALITY,55])
                    frame_b64 = base64.b64encode(buf).decode("utf-8")
            telemetry = {
                "bus_id":"BUS_01", "timestamp":time.time(),
                "latitude":location["latitude"], "longitude":location["longitude"],
                "speed": round(BUS_SPEED*50,1), "status":"active",
            }
            if frame_b64:
                telemetry["frame"] = frame_b64
            try:
                requests.post(f"{self.backend_url}/api/buses/BUS_01/telemetry",
                              json=telemetry, timeout=0.5)
            except Exception:
                pass
            if bgr is not None:
                try:
                    for det in self.detector.detect(bgr):
                        if det.class_name in ["person","car","motorcycle","bicycle"]:
                            requests.post(f"{self.backend_url}/api/events", timeout=0.5, json={
                                "bus_id":"BUS_01","timestamp":time.time(),"location":location,
                                "event_type":f"{det.class_name.upper()}_DETECTED",
                                "severity":"medium",
                                "description":f"YOLOv11: {det.class_name} @ {det.confidence:.2f}",
                                "image_url":"mock_camera_frame.jpg",
                            })
                except Exception:
                    pass
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
