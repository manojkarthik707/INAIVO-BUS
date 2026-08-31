import re
import math

with open(r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt", 'r', encoding='utf-8') as f:
    text = f.read()

# Find all nodes near (-87.15, 82.0) within radius 50m
target_x, target_y = -87.1466, 81.9927

pattern = r'(\w+)\s*\{([^}]+(?:\{[^}]*\}[^}]*)*)\}'
for m in re.finditer(pattern, text):
    proto = m.group(1)
    body = m.group(2)
    tm = re.search(r'translation\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)', body)
    if tm:
        x, y, z = float(tm.group(1)), float(tm.group(2)), float(tm.group(3))
        d = math.hypot(x - target_x, y - target_y)
        if d < 60.0:
            name_m = re.search(r'name\s*"([^"]+)"', body)
            name = name_m.group(1) if name_m else proto
            print(f"Object {name} ({proto}) at ({x:.2f}, {y:.2f}, {z:.2f}) [d={d:.2f}m]")
