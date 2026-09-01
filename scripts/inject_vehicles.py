import sys
import re

wbt_file = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt"

with open(wbt_file, "r", encoding="utf-8") as f:
    content = f.read()

# First, let's aggressively wipe out ANY existing pre-defined SUMO_VEHICLEs to avoid duplicates
# A pre-defined vehicle looks like: DEF SUMO_VEHICLEx BmwX5Simple { ... }
content = re.sub(r'DEF SUMO_VEHICLE\d+ [a-zA-Z0-9_]+ \{.*?^\}', '', content, flags=re.MULTILINE | re.DOTALL)

vehicles = []

# 20 Buses (0..19)
for i in range(20):
    vehicles.append(f"""
DEF SUMO_VEHICLE{i} BusSimple {{
  translation 10000 0 0
  name "SUMO_VEHICLE{i}"
}}""")

# 30 Bikes (20..49)
for i in range(20, 50):
    vehicles.append(f"""
DEF SUMO_VEHICLE{i} MotorbikeSimple {{
  translation 10000 0 0
  name "SUMO_VEHICLE{i}"
}}""")

# 40 Cars (50..89)
for i in range(50, 90):
    vehicles.append(f"""
DEF SUMO_VEHICLE{i} BmwX5Simple {{
  translation 10000 0 0
  name "SUMO_VEHICLE{i}"
}}""")

content += "\n" + "\n".join(vehicles) + "\n"

with open(wbt_file, "w", encoding="utf-8") as f:
    f.write(content)

print("Vehicles successfully pre-injected into sih_mvp_traffic.wbt")
