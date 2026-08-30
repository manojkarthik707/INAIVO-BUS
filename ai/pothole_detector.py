from __future__ import annotations


def detect_pothole(road_hazard_visible: bool, hazard_severity: str) -> dict:
    return {
        "detected": road_hazard_visible,
        "confidence": 0.89 if road_hazard_visible else 0.08,
        "hazard_severity": hazard_severity,
        "method": "mock_road_hazard_adapter",
    }

