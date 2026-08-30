from __future__ import annotations


def calculate_congestion(vehicle_count: int, average_speed_kmh: float, occupancy: float) -> dict:
    normalized_count = min(max(vehicle_count / 30, 0), 1)
    speed_pressure = 1 - min(max(average_speed_kmh / 50, 0), 1)
    occupancy = min(max(occupancy, 0), 1)
    score = round(100 * (0.4 * normalized_count + 0.35 * speed_pressure + 0.25 * occupancy))
    level = "LOW" if score <= 30 else "MEDIUM" if score <= 70 else "HIGH"
    return {"score": score, "level": level, "vehicle_count": vehicle_count, "average_speed_kmh": average_speed_kmh}

