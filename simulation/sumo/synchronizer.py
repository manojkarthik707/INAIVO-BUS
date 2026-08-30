from __future__ import annotations


class SumoSynchronizer:
    """Boundary for future TraCI synchronization; no simulator imports at module load."""

    def __init__(self, host: str = "127.0.0.1", port: int = 8813) -> None:
        self.host = host
        self.port = port

    def availability(self) -> dict:
        try:
            import traci  # noqa: F401
        except ImportError:
            return {"available": False, "reason": "TraCI is not installed"}
        return {"available": True}

