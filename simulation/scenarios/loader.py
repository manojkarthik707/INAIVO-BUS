from __future__ import annotations

from pathlib import Path

import yaml

CONFIG_DIR = Path(__file__).resolve().parents[1] / "configs"


class ScenarioConfigurationError(ValueError):
    pass


def load_scenario(path: str | Path) -> dict:
    scenario_path = Path(path)
    with scenario_path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict) or not isinstance(data.get("scenario"), dict):
        raise ScenarioConfigurationError("scenario configuration must contain a scenario object")
    for key in ("id", "type", "name"):
        if not data["scenario"].get(key):
            raise ScenarioConfigurationError(f"scenario.{key} is required")
    return data


def load_all_scenarios(config_dir: Path = CONFIG_DIR) -> dict[str, dict]:
    scenarios = {}
    for path in sorted(config_dir.glob("*.yaml")):
        config = load_scenario(path)
        scenarios[config["scenario"]["id"]] = config
    return scenarios

