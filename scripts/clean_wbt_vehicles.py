import re

WBT_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt"
with open(WBT_PATH, 'r', encoding='utf-8') as f:
    wbt = f.read()

# Remove all temporary serialized DEF SUMO_VEHICLE nodes
wbt = re.sub(r'DEF\s+SUMO_VEHICLE\d+\s+Solid\s*\{[\s\S]*?\n\}\n?', '', wbt)

with open(WBT_PATH, 'w', encoding='utf-8') as f:
    f.write(wbt)

print("Cleaned all temporary spawned SUMO_VEHICLE nodes from sih_mvp_traffic.wbt")
