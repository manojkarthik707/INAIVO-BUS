from datetime import datetime, timezone


def sample_event():
    return {
        "event_type": "POTHOLE",
        "severity": "HIGH",
        "confidence": 0.89,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "location": {"latitude": 11.0168, "longitude": 76.9558},
        "source": {"type": "BUS_CAMERA", "bus_id": "BUS_01", "camera_id": "FRONT"},
        "metadata": {"pothole_id": "TEST_01"},
        "simulation_ground_truth": {"road_hazard_present": True},
        "ai_prediction": {"detected": True},
    }


def test_health_and_bus_api(client):
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["simulation"]["mode"] == "mock"
    buses = client.get("/api/buses").json()
    assert any(bus["id"] == "BUS_01" for bus in buses)


def test_event_api_persists_event(client):
    created = client.post("/api/events", json=sample_event())
    assert created.status_code == 201
    event_id = created.json()["event_id"]
    assert client.get(f"/api/events/{event_id}").json()["event_type"] == "POTHOLE"
    assert client.get("/api/events").json()[0]["simulation_ground_truth"]["road_hazard_present"] is True


def test_websocket_receives_new_event(client):
    with client.websocket_connect("/ws/events") as socket:
        status = socket.receive_json()
        assert status["type"] == "simulation_status"
        response = client.post("/api/events", json=sample_event())
        assert response.status_code == 201
        message = socket.receive_json()
        assert message["type"] == "event"
        assert message["data"]["event_type"] == "POTHOLE"


def test_scenario_api_starts_pedestrian_scenario(client):
    response = client.post(
        "/api/scenarios/pedestrian_crossing/run",
        json={"traffic_density": "medium", "weather": "clear"},
    )
    assert response.status_code == 202
    assert response.json()["status"]["scenario_id"] == "pedestrian_crossing"

