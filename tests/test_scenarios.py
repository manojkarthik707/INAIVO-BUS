from pathlib import Path

import pytest

from simulation.scenarios.loader import ScenarioConfigurationError, load_all_scenarios, load_scenario


def test_all_mvp_scenarios_load():
    scenarios = load_all_scenarios()
    assert set(scenarios) == {"pedestrian_crossing", "red_light", "congestion", "pothole"}


def test_invalid_scenario_is_rejected(tmp_path: Path):
    path = tmp_path / "invalid.yaml"
    path.write_text("environment: {}", encoding="utf-8")
    with pytest.raises(ScenarioConfigurationError):
        load_scenario(path)

