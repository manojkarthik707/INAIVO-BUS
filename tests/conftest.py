from __future__ import annotations

import os
from pathlib import Path

os.environ["SIMULATION_MODE"] = "mock"
os.environ["DATABASE_URL"] = "sqlite:///./backend/data/test_urban_intelligence.db"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete

from backend.app.database import SessionLocal, engine
from backend.app.main import app
from backend.app.models import Event, ScenarioRun


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        with SessionLocal() as session:
            session.execute(delete(Event))
            session.execute(delete(ScenarioRun))
            session.commit()
        yield test_client


def pytest_sessionfinish(session, exitstatus):
    engine.dispose()
    Path("backend/data/test_urban_intelligence.db").unlink(missing_ok=True)
