import logging
import cv2
import numpy as np
from datetime import datetime, timezone
from ultralytics import YOLO
from backend.app.schemas import Detection

logger = logging.getLogger(__name__)

class ObjectDetector:
    def __init__(self, model_name="yolo11n.pt"):
        logger.info(f"Loading YOLO model: {model_name}")
        # YOLO auto-downloads the model if it doesn't exist locally
        self.model = YOLO(model_name)
        # Filter classes: 0:person, 1:bicycle, 2:car, 3:motorcycle, 5:bus, 7:truck
        self.classes = [0, 1, 2, 3, 5, 7]
        self.class_names = self.model.names

    def detect(self, frame: np.ndarray) -> list[Detection]:
        """
        Runs object detection on an RGB frame and returns a list of Detections.
        """
        results = self.model.track(source=frame, classes=self.classes, conf=0.10, persist=True, verbose=False)
        detections = []
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                cls_id = int(box.cls[0].item())
                conf = float(box.conf[0].item())
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                
                # YOLO tracking could supply IDs if we used track() instead of predict()
                track_id = str(int(box.id[0].item())) if box.id is not None else None
                
                det = Detection(
                    class_name=self.class_names[cls_id],
                    confidence=conf,
                    bbox=(int(x1), int(y1), int(x2), int(y2)),
                    track_id=track_id,
                    timestamp=datetime.now(timezone.utc)
                )
                detections.append(det)
                
        return detections
