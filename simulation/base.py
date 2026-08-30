from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable

from backend.app.schemas import EventCreate, ScenarioOptions

BusCallback = Callable[[dict], Awaitable[None]]
EventCallback = Callable[[EventCreate], Awaitable[None]]
StatusCallback = Callable[[dict], Awaitable[None]]


class SimulatorAdapter(ABC):
    def __init__(self, on_bus: BusCallback, on_event: EventCallback, on_status: StatusCallback) -> None:
        self.on_bus = on_bus
        self.on_event = on_event
        self.on_status = on_status

    @abstractmethod
    async def start(self) -> None: ...

    @abstractmethod
    async def stop(self) -> None: ...

    @abstractmethod
    async def run_scenario(self, scenario_id: str, options: ScenarioOptions) -> dict: ...

    @abstractmethod
    async def stop_scenario(self) -> None: ...

    @abstractmethod
    def status(self) -> dict: ...

    @abstractmethod
    def get_camera_frame(self) -> bytes: ...

