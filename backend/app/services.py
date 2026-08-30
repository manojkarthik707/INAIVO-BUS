from __future__ import annotations

from datetime import timezone

from sqlalchemy import select

from .database import SessionLocal
from .models import Bus, Event
from .schemas import BusRead, EventCreate, EventRead
from .websocket import manager


def event_to_schema(row: Event) -> EventRead:
    timestamp = row.timestamp
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)
    return EventRead(
        event_id=row.id,
        event_type=row.event_type,
        severity=row.severity,
        confidence=row.confidence,
        timestamp=timestamp,
        location={"latitude": row.latitude, "longitude": row.longitude},
        source={"type": row.source_type, "bus_id": row.bus_id, "camera_id": row.camera_id},
        metadata=row.event_metadata or {},
        evidence_image=row.evidence_path,
        simulation_ground_truth=row.simulation_ground_truth or {},
        ai_prediction=row.ai_prediction or {},
    )


async def persist_event(event: EventCreate, broadcast: bool = True) -> EventRead:
    row = Event(
        id=str(event.event_id),
        event_type=event.event_type,
        severity=event.severity,
        confidence=event.confidence,
        latitude=event.location.latitude,
        longitude=event.location.longitude,
        timestamp=event.timestamp,
        source_type=event.source.type,
        bus_id=event.source.bus_id,
        camera_id=event.source.camera_id,
        event_metadata=event.metadata,
        evidence_path=event.evidence_image,
        simulation_ground_truth=event.simulation_ground_truth,
        ai_prediction=event.ai_prediction,
    )
    with SessionLocal() as session:
        session.add(row)
        session.commit()
    result = event_to_schema(row)
    if broadcast:
        await manager.broadcast({"type": "event", "data": result.model_dump(mode="json")})
    return result


def list_events(limit: int = 100) -> list[EventRead]:
    with SessionLocal() as session:
        rows = session.scalars(select(Event).order_by(Event.timestamp.desc()).limit(limit)).all()
        return [event_to_schema(row) for row in rows]


def get_event(event_id: str) -> EventRead | None:
    with SessionLocal() as session:
        row = session.get(Event, event_id)
        return event_to_schema(row) if row else None


def list_buses() -> list[BusRead]:
    with SessionLocal() as session:
        rows = session.scalars(select(Bus).order_by(Bus.id)).all()
        return [BusRead.model_validate(row) for row in rows]
