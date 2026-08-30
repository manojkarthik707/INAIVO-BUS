from __future__ import annotations


def detect_red_light_violation(signal_state: str, crossed_stop_line: bool, speed_kmh: float) -> dict:
    violation = signal_state.upper() == "RED" and crossed_stop_line and speed_kmh > 1
    confidence = 0.97 if violation else 0.05
    return {
        "violation": violation,
        "confidence": confidence,
        "signal_state": signal_state.upper(),
        "crossed_stop_line": crossed_stop_line,
        "speed_kmh": speed_kmh,
    }

