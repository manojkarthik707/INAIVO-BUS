from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    simulation_mode: str = os.getenv("SIMULATION_MODE", "mock").lower()
    database_url: str = os.getenv(
        "DATABASE_URL", "sqlite:///./urban_intelligence.db"
    )
    carla_host: str = os.getenv("CARLA_HOST", "127.0.0.1")
    carla_port: int = int(os.getenv("CARLA_PORT", "2000"))


settings = Settings()

