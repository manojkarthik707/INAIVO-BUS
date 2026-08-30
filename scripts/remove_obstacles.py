import re

path = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Remove DEF STONES Solid
text = re.sub(r'DEF STONES Solid \{[\s\S]*?name "solid\(2\)"[\s\S]*?boundingObject USE STONES_GROUP\s*\}\n', '', text)

# 2. Remove all TrafficCone blocks
text = re.sub(r'TrafficCone \{[\s\S]*?\}\n', '', text)

with open(path, "w", encoding="utf-8") as f:
    f.write(text)

print("Successfully removed all traffic cones, stones, and road obstacles!")
