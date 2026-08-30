# API

Base URL: `http://127.0.0.1:8000`

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Process, database and simulator health |
| GET | `/api/buses` | Current fleet state |
| GET | `/api/buses/{id}` | One bus |
| GET | `/api/events` | Newest stored events |
| GET | `/api/events/{id}` | One event |
| POST | `/api/events` | Ingest a common event |
| GET | `/api/scenarios` | Available scenario definitions |
| POST | `/api/scenarios/{id}/run` | Run with optional traffic/weather body |
| POST | `/api/scenarios/stop` | Stop the active scenario |
| GET | `/api/simulation/status` | Adapter/scenario status |
| GET | `/api/camera/frame.svg` | Current mock front-camera frame |
| WS | `/ws/events` | Event, bus, status and camera messages |

