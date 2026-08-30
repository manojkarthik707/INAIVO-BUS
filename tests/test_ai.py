from backend.app.schemas import Detection
from ai.pedestrian_risk import assess_pedestrian_risk
from ai.red_light import detect_red_light_violation
from ai.traffic_analyzer import calculate_congestion


def test_pedestrian_risk_requires_road_context_and_motion():
    person = Detection(class_name="person", confidence=0.94, bbox=(280, 90, 340, 320))
    assert assess_pedestrian_risk([person], 30)["risk"] is True
    assert assess_pedestrian_risk([person], 0)["risk"] is False
    sidewalk_person = Detection(class_name="person", confidence=0.9, bbox=(10, 90, 80, 320))
    assert assess_pedestrian_risk([sidewalk_person], 30)["risk"] is False


def test_congestion_score_boundaries():
    low = calculate_congestion(2, 45, 0.1)
    high = calculate_congestion(28, 7, 0.88)
    assert low["level"] == "LOW"
    assert high["level"] == "HIGH"
    assert 0 <= high["score"] <= 100


def test_red_light_rule_correlates_all_inputs():
    assert detect_red_light_violation("RED", True, 34)["violation"] is True
    assert detect_red_light_violation("GREEN", True, 34)["violation"] is False
    assert detect_red_light_violation("RED", False, 34)["violation"] is False

