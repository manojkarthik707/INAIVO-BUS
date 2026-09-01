import sys
import re

wbt_file = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt"

with open(wbt_file, "r", encoding="utf-8") as f:
    content = f.read()

# First, let's aggressively wipe out ANY existing pre-defined SUMO_VEHICLEs to avoid duplicates
# A pre-defined vehicle looks like: DEF SUMO_VEHICLEx BmwX5Simple { ... }
content = re.sub(r'DEF SUMO_VEHICLE\d+ [a-zA-Z0-9_]+ \{.*?^\}', '', content, flags=re.MULTILINE | re.DOTALL)

vehicles = []

# 3 Buses (0, 1, 2)
for i in range(3):
    vehicles.append(f"""
DEF SUMO_VEHICLE{i} BusSimple {{
  translation 10000 0 0
  name "SUMO_VEHICLE{i}"
}}""")

# 7 Bikes (3..9)
for i in range(3, 10):
    vehicles.append(f"""
DEF SUMO_VEHICLE{i} MotorbikeSimple {{
  translation 10000 0 0
  name "SUMO_VEHICLE{i}"
}}""")

# 10 Cars (10..19)
for i in range(10, 20):
    vehicles.append(f"""
DEF SUMO_VEHICLE{i} BmwX5Simple {{
  translation 10000 0 0
  name "SUMO_VEHICLE{i}"
}}""")

content += "\n" + "\n".join(vehicles) + "\n"

with open(wbt_file, "w", encoding="utf-8") as f:
    f.write(content)

print("Vehicles successfully pre-injected into sih_mvp_traffic.wbt")
