import logging
from typing import List, Tuple, Optional
from backend.app.schemas import Detection

logger = logging.getLogger(__name__)

class PedestrianRiskEngine:
    def __init__(self, frame_width=800, frame_height=600):
        self.frame_width = frame_width
        self.frame_height = frame_height
        
        # Define a "danger zone" (e.g., center to bottom of the frame representing the road ahead)
        self.danger_zone_y_min = int(frame_height * 0.4)  # Lower 60% of the screen
        self.danger_zone_x_min = int(frame_width * 0.2)   # Central 60% horizontally
        self.danger_zone_x_max = int(frame_width * 0.8)

    def evaluate(self, detections: List[Detection]) -> Optional[Tuple[str, float]]:
        """
        Evaluates risk based on pedestrian detections.
        Returns (severity, confidence) if a risk is detected, else None.
        """
        for det in detections:
            if det.class_name == "person":
                x1, y1, x2, y2 = det.bbox
                cx = (x1 + x2) / 2
                cy = (y1 + y2) / 2
                width = x2 - x1
                height = y2 - y1
                
                # Heuristic 1: Is the pedestrian in the danger zone?
                in_danger_zone = (
                    self.danger_zone_x_min < cx < self.danger_zone_x_max and
                    cy > self.danger_zone_y_min
                )
                
                # Heuristic 2: How close are they? (using bounding box height as proxy)
                # A bounding box taking up > 30% of frame height means they are very close
                is_close = height > (self.frame_height * 0.3)
                
                if in_danger_zone:
                    if is_close:
                        return ("HIGH", round(det.confidence * 0.95, 2))
                    elif det.confidence > 0.6:
                        return ("MEDIUM", round(det.confidence * 0.8, 2))
                        
        return None
