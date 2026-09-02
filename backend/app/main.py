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

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import base64
import os

# Ensure evidence directory exists
os.makedirs("evidence", exist_ok=True)
app.mount("/evidence", StaticFiles(directory="evidence"), name="evidence")

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

@app.delete("/api/events")
async def clear_events(db: Session = Depends(database.get_db)):
    deleted_count = db.query(models.Event).delete()
    db.commit()

    import time
    # Touch reset trigger file so camera_streamer controllers wipe their in-memory deduplication history
    trigger_paths = [
        "reset_trigger.txt",
        os.path.join("..", "simulation", "webots", "controllers", "camera_streamer", "reset_trigger.txt"),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "simulation", "webots", "controllers", "camera_streamer", "reset_trigger.txt")),
    ]
    for p in trigger_paths:
        try:
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w") as f:
                f.write(str(time.time()))
        except Exception:
            pass

    # Broadcast CLEAR_EVENTS to all connected WebSocket clients
    await manager.broadcast_event({"type": "CLEAR_EVENTS"})

    return {
        "status": "cleared",
        "deleted_count": deleted_count,
        "message": "All registered pothole events wiped. Simulation reset to fresh state."
    }

@app.get("/api/evidence/{event_id}")
def get_evidence_image(event_id: str):
    file_path = os.path.join("evidence", f"{event_id}.jpg")
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="image/jpeg", headers={"Access-Control-Allow-Origin": "*"})
    raise HTTPException(status_code=404, detail="Evidence image not found")

@app.post("/api/events")
async def create_event(event: schemas.EventCreate, db: Session = Depends(database.get_db)):
    raw_evidence = event.evidence_image
    evidence_url = raw_evidence
    
    # Save a local disk copy for static archival
    if raw_evidence and raw_evidence.startswith("data:image"):
        try:
            header, data = raw_evidence.split(",", 1)
            img_bytes = base64.b64decode(data)
            file_name = f"{event.event_id}.jpg"
            file_path = os.path.join("evidence", file_name)
            with open(file_path, "wb") as f:
                f.write(img_bytes)
            evidence_url = f"/api/evidence/{event.event_id}"
        except Exception as e:
            logger.debug(f"Failed to save evidence image to disk: {e}")

    event_meta = dict(event.metadata or {})
    # Keep full data URI in metadata if present so browser renders with zero network blockages
    event_meta["evidence_image"] = raw_evidence or evidence_url

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
        event_metadata=event_meta,
        evidence_path=evidence_url
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    
    # Broadcast to websocket
    broadcast_data = json.loads(event.model_dump_json())
    broadcast_data["evidence_image"] = raw_evidence or evidence_url
    if "metadata" in broadcast_data and isinstance(broadcast_data["metadata"], dict):
        broadcast_data["metadata"]["evidence_image"] = raw_evidence or evidence_url
    await manager.broadcast_event(broadcast_data)
    return {"status": "received", "evidence_url": evidence_url}

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
