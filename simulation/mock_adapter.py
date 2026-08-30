from __future__ import annotations

import asyncio
import html
import logging
import math
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from ai.detector import MockDetector
from ai.pedestrian_risk import assess_pedestrian_risk
from ai.pothole_detector import detect_pothole
from ai.red_light import detect_red_light_violation
from ai.traffic_analyzer import calculate_congestion
from backend.app.schemas import EventCreate, EventSource, Location, ScenarioOptions

from .base import SimulatorAdapter
from .scenarios.manager import ScenarioManager

logger = logging.getLogger("SIMULATION")
EVIDENCE_DIR = Path(__file__).resolve().parents[1] / "backend" / "data" / "evidence"


class MockSimulatorAdapter(SimulatorAdapter):
    def __init__(self, on_bus, on_event, on_status) -> None:
        super().__init__(on_bus, on_event, on_status)
        self.manager = ScenarioManager()
        self.detector = MockDetector()
        self._running = False
        self._ticker_task: asyncio.Task | None = None
        self._scenario_task: asyncio.Task | None = None
        self._scenario_id: str | None = None
        self._phase = "IDLE"
        self._traffic = "medium"
        self._weather = "clear"
        self._tick = 0
        self._bus = {
            "id": "BUS_01",
            "name": "Mobile Urban Sensor 01",
            "latitude": 11.0168,
            "longitude": 76.9558,
            "speed": 24.0,
            "status": "ACTIVE",
        }

    async def start(self) -> None:
        if self._running:
            return
        self._running = True
        self._ticker_task = asyncio.create_task(self._ticker(), name="mock-bus-ticker")
        await self.on_bus(self._bus.copy())
        logger.info("mock_adapter_started bus_id=BUS_01")

    async def stop(self) -> None:
        self._running = False
        await self.stop_scenario()
        if self._ticker_task:
            self._ticker_task.cancel()
            await asyncio.gather(self._ticker_task, return_exceptions=True)
        logger.info("mock_adapter_stopped")

    async def _ticker(self) -> None:
        while self._running:
            self._tick += 1
            angle = self._tick / 24
            self._bus["latitude"] = 11.0168 + math.sin(angle) * 0.0021
            self._bus["longitude"] = 76.9558 + math.cos(angle) * 0.0028
            self._bus["speed"] = 8.0 if self._scenario_id == "congestion" else 24.0
            await self.on_bus(self._bus.copy())
            await asyncio.sleep(1)

    async def run_scenario(self, scenario_id: str, options: ScenarioOptions) -> dict:
        config = self.manager.get(scenario_id)
        await self.stop_scenario()
        self._scenario_id = scenario_id
        self._phase = "PREPARING"
        self._traffic = options.traffic_density
        self._weather = options.weather
        self._scenario_task = asyncio.create_task(
            self._execute_scenario(config), name=f"scenario-{scenario_id}"
        )
        await self._broadcast_status()
        logger.info("scenario_started id=%s traffic=%s weather=%s", scenario_id, self._traffic, self._weather)
        return self.status()

    async def stop_scenario(self) -> None:
        task = self._scenario_task
        self._scenario_task = None
        if task and task is not asyncio.current_task() and not task.done():
            task.cancel()
            await asyncio.gather(task, return_exceptions=True)
        self._scenario_id = None
        self._phase = "IDLE"
        await self._broadcast_status()

    async def _execute_scenario(self, config: dict) -> None:
        try:
            await asyncio.sleep(1.0)
            self._phase = "INCIDENT_ACTIVE"
            await self._broadcast_status()
            await asyncio.sleep(1.0)
            event = self._build_event(config)
            self._write_evidence(event)
            await self.on_event(event)
            self._phase = "EVENT_DETECTED"
            await self._broadcast_status()
            await asyncio.sleep(3.0)
            self._phase = "COMPLETED"
            await self._broadcast_status()
        except asyncio.CancelledError:
            raise

    def _build_event(self, config: dict) -> EventCreate:
        scenario_id = config["scenario"]["id"]
        location = Location(latitude=self._bus["latitude"], longitude=self._bus["longitude"])
        base = {
            "event_id": uuid4(),
            "timestamp": datetime.now(timezone.utc),
            "location": location,
            "source": EventSource(type="BUS_CAMERA", bus_id="BUS_01", camera_id="FRONT"),
        }
        if scenario_id == "pedestrian_crossing":
            detections = self.detector.detect(
                None, {"detected_class": "person", "confidence": 0.94, "bbox": (270, 90, 350, 320), "track_id": "P_01"}
            )
            prediction = assess_pedestrian_risk(detections, bus_speed_kmh=30)
            return EventCreate(
                **base,
                event_type="PEDESTRIAN_RISK",
                severity="HIGH",
                confidence=prediction["confidence"],
                metadata={"distance_estimate_m": 12, "detections": [d.model_dump(mode="json") for d in detections]},
                simulation_ground_truth={"pedestrian_present": True, "inside_road_region": True, "distance_m": 12},
                ai_prediction=prediction,
            )
        if scenario_id == "red_light":
            prediction = detect_red_light_violation("RED", True, 34)
            red_light_base = {**base, "source": EventSource(type="FIXED_CCTV", camera_id="CCTV_01")}
            return EventCreate(
                **red_light_base,
                event_type="RED_LIGHT_VIOLATION",
                severity="HIGH",
                confidence=prediction["confidence"],
                metadata={"vehicle_id": "VEHICLE_17", "stop_line": "JUNCTION_04_NORTH"},
                simulation_ground_truth={"signal_state": "RED", "crossed_stop_line": True, "simulator_vehicle_id": "VEHICLE_17"},
                ai_prediction=prediction,
            )
        if scenario_id == "congestion":
            traffic = config["traffic"]
            prediction = calculate_congestion(traffic["vehicle_count"], traffic["average_speed_kmh"], traffic["occupancy"])
            return EventCreate(
                **base,
                event_type="CONGESTION",
                severity=prediction["level"],
                confidence=0.93,
                metadata={"road_segment": config["incident"]["road_segment"], "congestion_score": prediction["score"]},
                simulation_ground_truth={"vehicle_count": 28, "average_speed_kmh": 7, "occupancy": 0.88},
                ai_prediction=prediction,
            )
        incident = config["incident"]
        prediction = detect_pothole(True, incident["severity"])
        return EventCreate(
            **base,
            event_type="POTHOLE",
            severity=incident["severity"],
            confidence=prediction["confidence"],
            metadata={"pothole_id": incident["pothole_id"], "dimensions_m": incident["dimensions_m"]},
            simulation_ground_truth={"road_hazard_present": True, **incident},
            ai_prediction=prediction,
        )

    def _write_evidence(self, event: EventCreate) -> None:
        EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
        filename = f"{event.event_id}.svg"
        event.evidence_image = f"/evidence/{filename}"
        (EVIDENCE_DIR / filename).write_bytes(self.get_camera_frame())

    async def _broadcast_status(self) -> None:
        await self.on_status({"type": "simulation_status", "data": self.status()})

    def status(self) -> dict:
        return {
            "mode": "mock",
            "available": True,
            "running": self._running,
            "scenario_id": self._scenario_id,
            "phase": self._phase,
            "traffic_density": self._traffic,
            "weather": self._weather,
            "message": "CARLA UNAVAILABLE — RUNNING MOCK MODE",
        }

    def get_camera_frame(self) -> bytes:
        scenario = self._scenario_id or "normal_traffic"
        phase = self._phase
        overlays = ""
        actors = ""
        if scenario == "pedestrian_crossing" and phase != "IDLE":
            actors = '<circle cx="310" cy="135" r="14" fill="#f2c6a0"/><path d="M310 149 L310 225 M310 170 L280 205 M310 170 L340 205 M310 225 L285 290 M310 225 L335 290" stroke="#f7f9fb" stroke-width="10" stroke-linecap="round"/>'
            overlays = '<rect x="264" y="112" width="92" height="190" fill="none" stroke="#52f7b8" stroke-width="3"/><text x="264" y="103" fill="#52f7b8">PERSON 94%</text>'
        elif scenario == "red_light" and phase != "IDLE":
            actors = '<rect x="245" y="188" width="150" height="62" rx="12" fill="#db3157"/><circle cx="275" cy="254" r="15" fill="#111827"/><circle cx="365" cy="254" r="15" fill="#111827"/><circle cx="485" cy="82" r="18" fill="#ff365c"/>'
            overlays = '<rect x="235" y="175" width="170" height="90" fill="none" stroke="#ffcf5a" stroke-width="3"/><text x="235" y="165" fill="#ffcf5a">CAR · VEHICLE_17</text>'
        elif scenario == "congestion" and phase != "IDLE":
            actors = ''.join(f'<rect x="{80 + (i % 5) * 105}" y="{155 + (i // 5) * 55}" width="72" height="34" rx="6" fill="#{color}"/>' for i, color in enumerate(["e45a73","f2b84b","4fc3f7","8be28b","a78bfa","f97316","60a5fa","f43f5e","22c55e","eab308","38bdf8","fb7185","84cc16","c084fc","f59e0b"]))
            overlays = '<text x="28" y="74" fill="#ffcf5a" font-size="22">CONGESTION SCORE 88 · HIGH</text>'
        elif scenario == "pothole" and phase != "IDLE":
            actors = '<ellipse cx="330" cy="276" rx="76" ry="24" fill="#171a1f"/><ellipse cx="330" cy="272" rx="52" ry="13" fill="#090b0e"/>'
            overlays = '<rect x="245" y="236" width="170" height="70" fill="none" stroke="#ffcf5a" stroke-width="3"/><text x="245" y="226" fill="#ffcf5a">POTHOLE 89%</text>'
        label = html.escape(scenario.replace("_", " ").upper())
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="640" height="360" viewBox="0 0 640 360">
        <defs><linearGradient id="sky" x2="0" y2="1"><stop stop-color="#14314b"/><stop offset="1" stop-color="#4d7186"/></linearGradient></defs>
        <rect width="640" height="360" fill="url(#sky)"/><rect y="118" width="640" height="242" fill="#29323a"/>
        <path d="M265 118 L85 360 M375 118 L555 360" stroke="#f1f5f9" stroke-width="5" opacity=".75"/>
        <path d="M320 130 L320 350" stroke="#f4c64c" stroke-width="4" stroke-dasharray="24 20"/>
        <rect x="0" y="0" width="640" height="44" fill="#08131d" opacity=".9"/><text x="18" y="29" fill="#e8f3f8" font-family="monospace" font-size="17">BUS_01 · FRONT · {label}</text>
        {actors}{overlays}<text x="18" y="340" fill="#b7c9d4" font-family="monospace" font-size="14">MOCK CAMERA · {html.escape(phase)}</text></svg>'''
        return svg.encode("utf-8")
