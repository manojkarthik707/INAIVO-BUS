import asyncio

import pytest

from backend.app.schemas import ScenarioOptions
from simulation.mock_adapter import MockSimulatorAdapter


@pytest.mark.asyncio
async def test_mock_simulator_moves_bus_and_emits_event():
    buses, events, statuses = [], [], []

    async def on_bus(data): buses.append(data)
    async def on_event(data): events.append(data)
    async def on_status(data): statuses.append(data)

    adapter = MockSimulatorAdapter(on_bus, on_event, on_status)
    await adapter.start()
    initial_longitude = buses[-1]["longitude"]
    await adapter.run_scenario("pedestrian_crossing", ScenarioOptions())
    await asyncio.sleep(2.2)
    await adapter.stop()
    assert len(buses) >= 2
    assert buses[-1]["longitude"] != initial_longitude
    assert events[0].event_type == "PEDESTRIAN_RISK"
    assert events[0].simulation_ground_truth["pedestrian_present"] is True
    assert events[0].ai_prediction["risk"] is True

