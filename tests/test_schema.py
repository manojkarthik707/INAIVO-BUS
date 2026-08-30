from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from backend.app.schemas import EventCreate


def test_event_schema_accepts_common_contract():
    event = EventCreate(
        event_type="PEDESTRIAN_RISK",
        severity="HIGH",
        confidence=0.94,
        timestamp=datetime.now(timezone.utc),
        location={"latitude": 11.0168, "longitude": 76.9558},
        source={"type": "BUS_CAMERA", "bus_id": "BUS_01", "camera_id": "FRONT"},
        simulation_ground_truth={"pedestrian_present": True},
        ai_prediction={"risk": True},
    )
    assert event.source.bus_id == "BUS_01"
    assert event.simulation_ground_truth != event.ai_prediction


def test_event_schema_rejects_invalid_confidence():
    with pytest.raises(ValidationError):
        EventCreate(
            event_type="POTHOLE",
            severity="HIGH",
            confidence=1.4,
            location={"latitude": 11.0, "longitude": 77.0},
            source={"type": "BUS_CAMERA"},
        )

