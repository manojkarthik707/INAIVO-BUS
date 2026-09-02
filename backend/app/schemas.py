from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Location(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    sim_x: float | None = None
    sim_y: float | None = None


class EventSource(BaseModel):
    type: str
    bus_id: str | None = None
    camera_id: str | None = None


class EventCreate(BaseModel):
    event_id: UUID = Field(default_factory=uuid4)
    event_type: str = Field(min_length=2, max_length=64)
    severity: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    confidence: float = Field(ge=0, le=1)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    location: Location
    source: EventSource
    metadata: dict[str, Any] = Field(default_factory=dict)
    evidence_image: str | None = None
    simulation_ground_truth: dict[str, Any] = Field(default_factory=dict)
    ai_prediction: dict[str, Any] = Field(default_factory=dict)

    @field_validator("timestamp")
    @classmethod
    def timestamp_must_be_timezone_aware(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("timestamp must include a timezone")
        return value


class EventRead(EventCreate):
    model_config = ConfigDict(from_attributes=True)


class BusRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    latitude: float
    longitude: float
    speed: float
    status: str
    updated_at: datetime


class ScenarioOptions(BaseModel):
    traffic_density: Literal["low", "medium", "high"] = "medium"
    weather: Literal["clear", "rain"] = "clear"


class Detection(BaseModel):
    class_name: str
    confidence: float = Field(ge=0, le=1)
    bbox: tuple[int, int, int, int]
    track_id: str | None = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

