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

# In-memory frame store and pub/sub queues for live video streaming
frame_store: dict[str, bytes] = {}
frame_subscribers: dict[str, set[asyncio.Queue]] = {}

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
 
@app.on_event("startup")
async def on_startup():
    manager.set_loop(asyncio.get_running_loop())

# Global real-time traffic heatmap cache
latest_traffic_data: dict = {
    "type": "TRAFFIC_HEATMAP",
    "timestamp": datetime.now(timezone.utc).timestamp(),
    "total_vehicles": 0,
    "hotspots": [],
    "vehicles": []
}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/api/traffic/heatmap")
def get_traffic_heatmap():
    return latest_traffic_data

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
async def update_bus_telemetry(bus_id: str, payload: dict):
    
    # Decode the base64 frame and dispatch to memory & subscriber queues
    if "frame" in payload:
        import base64
        try:
            raw_bytes = base64.b64decode(payload["frame"])
            frame_store[bus_id] = raw_bytes
            for q in list(frame_subscribers.get(bus_id, [])):
                if q.full():
                    try:
                        q.get_nowait()
                    except Exception:
                        pass
                try:
                    q.put_nowait(raw_bytes)
                except Exception:
                    pass
        except Exception:
            pass
    
    # Broadcast telemetry including frame over WebSocket for seamless instant display
    event_payload = {
        "type": "TELEMETRY",
        "bus_id": bus_id,
        "latitude": payload.get("latitude", 0),
        "longitude": payload.get("longitude", 0),
        "sim_x": payload.get("sim_x", 0),
        "sim_y": payload.get("sim_y", 0),
        "speed": payload.get("speed", 0)
    }
    if "frame" in payload:
        event_payload["frame"] = payload["frame"]
        
    await manager.broadcast_event(event_payload)
    return {"status": "updated"}


@app.get("/api/buses/{bus_id}/frame.jpg")
async def get_bus_frame(bus_id: str):
    """Return the latest single JPEG frame for this bus."""
    from fastapi.responses import Response
    frame = frame_store.get(bus_id)
    if frame:
        return Response(content=frame, media_type="image/jpeg", headers={"Cache-Control": "no-cache"})
    raise HTTPException(status_code=404, detail="No frame available yet")

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
