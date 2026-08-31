with open(r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt", 'r', encoding='utf-8') as f:
    wbt = f.read()

import re

# Find all Robot, Supervisor, Camera, Display, SumoInterface nodes
controllers = re.findall(r'controller\s+"([^"]+)"', wbt)
supervisors = re.findall(r'supervisor\s+(TRUE|FALSE)', wbt)
cameras = re.findall(r'Camera\s*\{', wbt)
displays = re.findall(r'Display\s*\{', wbt)
sumo_interface = re.findall(r'SumoInterface\s*\{[^}]*\}', wbt)

print(f"Active controllers in WBT: {controllers}")
print(f"Total cameras in WBT: {len(cameras)}")
print(f"Total displays in WBT: {len(displays)}")
print(f"SumoInterface config: {sumo_interface}")
