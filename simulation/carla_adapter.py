from __future__ import annotations

from .base import SimulatorAdapter


class CarlaSimulatorAdapter(SimulatorAdapter):
    async def start(self) -> None:
        try:
            import carla  # noqa: F401
        except ImportError as exc:
            raise RuntimeError("CARLA UNAVAILABLE — RUNNING MOCK MODE requires SIMULATION_MODE=mock") from exc
        raise RuntimeError("CARLA Python API found, but the host integration is not configured yet")

    async def stop(self) -> None: pass
    async def run_scenario(self, scenario_id, options): raise RuntimeError("CARLA adapter not active")
    async def stop_scenario(self) -> None: pass
    def status(self) -> dict: return {"mode": "carla", "available": False, "running": False}
    def get_camera_frame(self) -> bytes: return b""

