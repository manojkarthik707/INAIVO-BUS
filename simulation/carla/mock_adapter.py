import time
import requests
import uuid
import datetime
import random
import threading
import logging

logger = logging.getLogger(__name__)

class MockSimulatorAdapter:
    def __init__(self, backend_url="http://localhost:8000"):
        self.backend_url = backend_url
        self.running = False
        self.bus_id = "BUS_01"
        self.latitude = 11.0168
        self.longitude = 76.9558
        self.speed = 30.0

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._run_loop)
        self.thread.daemon = True
        self.thread.start()
        logger.info("Mock Simulator Adapter started.")

    def stop(self):
        self.running = False
        if hasattr(self, 'thread'):
            self.thread.join()

    def _run_loop(self):
        while self.running:
            # Simulate bus moving slightly
            self.latitude += 0.0001
            self.longitude += 0.0001
            
            # Send telemetry
            try:
                requests.post(f"{self.backend_url}/api/buses/{self.bus_id}/telemetry", json={
                    "latitude": self.latitude,
                    "longitude": self.longitude,
                    "speed": self.speed,
                    "status": "MOVING"
                })
            except Exception as e:
                logger.error(f"Failed to send telemetry: {e}")
            
            time.sleep(2) # Send telemetry every 2 seconds

    def trigger_event(self, event_type="PEDESTRIAN_RISK", severity="HIGH"):
        event_payload = {
            "event_id": str(uuid.uuid4()),
            "event_type": event_type,
            "severity": severity,
            "confidence": round(random.uniform(0.85, 0.99), 2),
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "location": {
                "latitude": self.latitude,
                "longitude": self.longitude
            },
            "source": {
                "type": "BUS_CAMERA",
                "bus_id": self.bus_id,
                "camera_id": "FRONT"
            },
            "metadata": {"simulated": True},
            "evidence_image": "" # Optional for now
        }
        try:
            res = requests.post(f"{self.backend_url}/api/events", json=event_payload)
            if res.status_code == 200:
                logger.info(f"Triggered {event_type} event successfully.")
        except Exception as e:
            logger.error(f"Failed to trigger event: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    adapter = MockSimulatorAdapter()
    adapter.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        adapter.stop()
