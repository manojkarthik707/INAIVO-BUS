import carla
import logging
import threading
import time
import requests
import uuid
import datetime
import random
import numpy as np
from ai.detector import ObjectDetector
from ai.pedestrian_risk import PedestrianRiskEngine

logger = logging.getLogger(__name__)

class CarlaSimulatorAdapter:
    def __init__(self, backend_url="http://localhost:8000"):
        self.backend_url = backend_url
        self.running = False
        self.bus_id = "BUS_01"
        self.client = None
        self.world = None
        self.vehicle = None
        self.camera = None
        
        self.detector = ObjectDetector()
        self.risk_engine = PedestrianRiskEngine()

    def start(self):
        try:
            self.client = carla.Client('127.0.0.1', 2000)
            self.client.set_timeout(60.0)
            self.world = self.client.get_world()
            logger.info("Connected to CARLA simulator.")
            self._setup_bus()
            
            self.running = True
            self.thread = threading.Thread(target=self._run_loop)
            self.thread.daemon = True
            self.thread.start()
        except Exception as e:
            logger.error(f"Failed to connect to CARLA: {e}")
            raise e

    def _setup_bus(self):
        blueprint_library = self.world.get_blueprint_library()
        bus_bp = blueprint_library.filter('vehicle.volkswagen.t2_2021')[0] # Using T2 as substitute bus if real bus not available
        spawn_point = random.choice(self.world.get_map().get_spawn_points())
        self.vehicle = self.world.spawn_actor(bus_bp, spawn_point)
        self.vehicle.set_autopilot(True)
        
        # Setup Camera
        camera_bp = blueprint_library.find('sensor.camera.rgb')
        camera_bp.set_attribute('image_size_x', '800')
        camera_bp.set_attribute('image_size_y', '600')
        camera_bp.set_attribute('fov', '90')
        
        camera_transform = carla.Transform(carla.Location(x=1.5, z=2.4))
        self.camera = self.world.spawn_actor(camera_bp, camera_transform, attach_to=self.vehicle)
        self.camera.listen(lambda image: self._process_camera_frame(image))
        logger.info("Bus and Camera spawned.")

    def _process_camera_frame(self, image):
        if not self.running:
            return
            
        # Convert CARLA raw image to numpy array
        array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
        array = np.reshape(array, (image.height, image.width, 4))
        array = array[:, :, :3] # Remove alpha
        
        # AI Detection
        detections = self.detector.detect(array)
        
        # Risk Evaluation
        risk = self.risk_engine.evaluate(detections)
        if risk:
            severity, confidence = risk
            self.trigger_event("PEDESTRIAN_RISK", severity, confidence)

    def stop(self):
        self.running = False
        if hasattr(self, 'thread'):
            self.thread.join(timeout=2.0)
            
        if self.camera:
            self.camera.stop()
            self.camera.destroy()
        if self.vehicle:
            self.vehicle.destroy()
        logger.info("CARLA Adapter stopped.")

    def _run_loop(self):
        while self.running:
            if self.vehicle:
                t = self.vehicle.get_transform()
                v = self.vehicle.get_velocity()
                speed_kmh = 3.6 * np.sqrt(v.x**2 + v.y**2 + v.z**2)
                
                try:
                    requests.post(f"{self.backend_url}/api/buses/{self.bus_id}/telemetry", json={
                        "latitude": t.location.x,  # Mapping CARLA coordinate to latitude for MVP
                        "longitude": t.location.y,
                        "speed": speed_kmh,
                        "status": "MOVING"
                    })
                except Exception as e:
                    logger.error(f"Telemetry failed: {e}")
            time.sleep(2)

    def trigger_event(self, event_type="PEDESTRIAN_RISK", severity="HIGH", confidence=0.9):
        if not self.vehicle:
            return
            
        t = self.vehicle.get_transform()
        event_payload = {
            "event_id": str(uuid.uuid4()),
            "event_type": event_type,
            "severity": severity,
            "confidence": confidence,
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "location": {
                "latitude": t.location.x,
                "longitude": t.location.y
            },
            "source": {
                "type": "BUS_CAMERA",
                "bus_id": self.bus_id,
                "camera_id": "FRONT"
            },
            "metadata": {"simulated": False},
            "evidence_image": ""
        }
        try:
            requests.post(f"{self.backend_url}/api/events", json=event_payload)
        except Exception as e:
            pass
