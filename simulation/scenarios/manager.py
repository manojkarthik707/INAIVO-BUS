import time
import logging
import os
from simulation.carla.mock_adapter import MockSimulatorAdapter

# Fallback block to safely handle if WEBOTS package is missing
try:
    from simulation.webots.webots_adapter import WebotsSimulatorAdapter
except ImportError:
    WebotsSimulatorAdapter = None

logger = logging.getLogger(__name__)

class ScenarioManager:
    def __init__(self, backend_url="http://127.0.0.1:8000"):
        self.mode = os.getenv("SIMULATION_MODE", "mock").lower()
        if self.mode == "webots" and WebotsSimulatorAdapter:
            logger.info("Initializing REAL WEBOTS Simulator")
            self.simulator = WebotsSimulatorAdapter(backend_url)
        else:
            logger.info(f"Initializing MOCK Simulator (requested mode: {self.mode})")
            self.simulator = MockSimulatorAdapter(backend_url)
        
    def start_simulation(self):
        self.simulator.start()
        
    def stop_simulation(self):
        self.simulator.stop()
        
    def run_scenario(self, scenario_id: str):
        logger.info(f"Running scenario: {scenario_id}")
        
        # Simulating some delay before the event happens
        time.sleep(3)
        
        event_mapping = {
            "pedestrian_crossing": ("PEDESTRIAN_RISK", "HIGH"),
            "red_light": ("RED_LIGHT_VIOLATION", "HIGH"),
            "congestion": ("CONGESTION", "MEDIUM"),
            "pothole": ("POTHOLE", "HIGH")
        }
        
        event_type, severity = event_mapping.get(scenario_id, ("UNKNOWN_EVENT", "LOW"))
        
        self.simulator.trigger_event(event_type, severity)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    manager = ScenarioManager()
    manager.start_simulation()
    
    # Let it run for a bit
    time.sleep(2)
    manager.run_scenario("pedestrian_crossing")
    
    time.sleep(2)
    manager.stop_simulation()
