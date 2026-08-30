from fastapi import FastAPI, Depends, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
import json
import logging
import uuid
import asyncio
from datetime import datetime, timezone

from app import database, models, schemas
from app.api.websocket import router as ws_router, manager

# In-memory frame store and push notifications
frame_store: dict[str, bytes] = {}
frame_events: dict[str, asyncio.Event] = {}

# Initialize Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Urban Intelligence MVP")

# Allow CORS for Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ws_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/api/buses")
def get_buses(db: Session = Depends(database.get_db)):
    return db.query(models.Bus).all()

@app.get("/api/events")
def get_events(db: Session = Depends(database.get_db)):
    return db.query(models.Event).order_by(models.Event.timestamp.desc()).limit(100).all()

@app.post("/api/events")
async def create_event(event: schemas.EventCreate, db: Session = Depends(database.get_db)):
    db_event = models.Event(
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
        evidence_path=event.evidence_image
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    
    # Broadcast to websocket
    await manager.broadcast_event(json.loads(event.model_dump_json()))
    return {"status": "received"}

@app.post("/api/buses/{bus_id}/telemetry")
async def update_bus_telemetry(bus_id: str, payload: dict, db: Session = Depends(database.get_db)):
    # Very simple dict payload to avoid creating a new schema
    bus = db.query(models.Bus).filter(models.Bus.id == bus_id).first()
    if not bus:
        bus = models.Bus(id=bus_id, name=f"Bus {bus_id}", latitude=payload["latitude"], longitude=payload["longitude"], speed=payload["speed"], status=payload["status"])
        db.add(bus)
    else:
        bus.latitude = payload["latitude"]
        bus.longitude = payload["longitude"]
        bus.speed = payload["speed"]
        bus.status = payload["status"]
    
    db.commit()
    
    # Decode the base64 frame and store it in memory (bypasses DB for video)
    if "frame" in payload:
        import base64
        try:
            frame_store[bus_id] = base64.b64decode(payload["frame"])
            ev = frame_events.get(bus_id)
            if ev:
                ev.set()
        except Exception:
            pass
    
    # Broadcast telemetry WITHOUT the heavy frame payload to keep WebSocket lean
    event_payload = {
        "type": "TELEMETRY",
        "bus_id": bus_id,
        "latitude": payload.get("latitude", 0),
        "longitude": payload.get("longitude", 0),
        "speed": payload.get("speed", 0)
    }
    await manager.broadcast_event(event_payload)
    return {"status": "updated"}


async def _mjpeg_generator(bus_id: str):
    """Async generator that yields MJPEG frames with zero polling delay as soon as new frames arrive."""
    boundary = b"--frame"
    ev = asyncio.Event()
    frame_events[bus_id] = ev
    
    try:
        while True:
            try:
                await asyncio.wait_for(ev.wait(), timeout=0.1)
                ev.clear()
            except asyncio.TimeoutError:
                pass
            frame = frame_store.get(bus_id)
            if frame:
                yield (
                    boundary + b"\r\n"
                    b"Content-Type: image/jpeg\r\n"
                    b"Content-Length: " + str(len(frame)).encode() + b"\r\n"
                    b"\r\n" + frame + b"\r\n"
                )
    finally:
        if bus_id in frame_events and frame_events[bus_id] is ev:
            del frame_events[bus_id]


@app.get("/api/buses/{bus_id}/stream")
async def stream_bus_video(bus_id: str):
    """MJPEG stream endpoint — the browser renders this natively at full speed."""
    return StreamingResponse(
        _mjpeg_generator(bus_id),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from simulation.scenarios.manager import ScenarioManager

manager_sim = ScenarioManager()
manager_sim.start_simulation()

@app.post("/api/scenarios/{scenario_id}/run")
async def run_scenario(scenario_id: str, background_tasks: BackgroundTasks):
    logger.info(f"Starting scenario: {scenario_id}")
    background_tasks.add_task(manager_sim.run_scenario, scenario_id)
    return {"status": "starting", "scenario": scenario_id}

# Trigger reload

# Trigger reload for Bus connection

# Trigger reload for bugfix

# Hot reload for Kinematics

# Trigger reload for final kinematic simulation

# Hot reload for auto-reconnect

# Hot reload for pure-Supervisor kinematics

# Hot reload for smooth waypoint kinematics

# Hot reload SUMO-mapped waypoints

# Hot reload for SUMO vehicle mirroring

# Hot reload heading-only SUMO mirror

# Hot reload sticky leader tracking

# Hot reload position trail follower

# Hot reload resetPhysics fix

# Hot reload smooth pursuit

# Hot reload extra buses

# Hot reload distance snapping

# Hot reload static routes

# Hot reload circle bug fix

# Hot reload direct SUMO sync
