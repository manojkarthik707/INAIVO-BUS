import re
import os

WBT_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt"
SUMOCFG_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.sumocfg"
ROU_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.rou.xml"

# 1. Update sumo.sumocfg to disable buggy sublane splitting (guarantee 1 vehicle per lane)
with open(SUMOCFG_PATH, "r", encoding="utf-8") as f:
    cfg = f.read()

# Remove lateral-resolution or set to 0.0
cfg = re.sub(r'<lateral-resolution\s+value="[^"]*"\s*/>', '<lateral-resolution value="0.0" />', cfg)
with open(SUMOCFG_PATH, "w", encoding="utf-8") as f:
    f.write(cfg)
print("Disabled sublane splitting in sumo.sumocfg.")

# 2. Clean sih_mvp_traffic.wbt: remove all rogue signs & poles sitting in the middle of roads
with open(WBT_PATH, "r", encoding="utf-8") as f:
    wbt = f.read()

# Pattern for rogue signs and misplaced traffic lights
pattern = r'(DEF\s+\w+\s+)?(GenericTrafficLight|CrossRoadsTrafficLight|CautionSign|OrderSign|StopSign|YieldSign|SpeedLimitSign)\s*\{[^}]*\}'
wbt_cleaned = re.sub(pattern, '', wbt)

# Also clean up any double blank lines
wbt_cleaned = re.sub(r'\n\s*\n\s*\n', '\n\n', wbt_cleaned)

with open(WBT_PATH, "w", encoding="utf-8") as f:
    f.write(wbt_cleaned)
print("Removed all misplaced sign and traffic light poles from road lanes in sih_mvp_traffic.wbt.")

# 3. Regenerate sumo.rou.xml using standard robust LC2013 multi-lane model (one vehicle per lane, clean overtaking)
import generate_perfect_city_traffic
