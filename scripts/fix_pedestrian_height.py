import re

WBT_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt"
CTRL_PATH = r"f:\VEHDEMO\simulation\webots\controllers\pedestrian_controller\pedestrian_controller.py"

# 1. Update sih_mvp_traffic.wbt default pedestrian Z heights to 1.27m
with open(WBT_PATH, 'r', encoding='utf-8') as f:
    wbt = f.read()

# Replace translation on all PED_J* nodes
wbt = re.sub(r'(DEF\s+PED_J\w+\s+Pedestrian\s*\{\s*translation\s+[-0-9.]+\s+[-0-9.]+)\s+[-0-9.]+',
             r'\1 1.27', wbt)

with open(WBT_PATH, 'w', encoding='utf-8') as f:
    f.write(wbt)

print("Updated pedestrian initial Z translations to 1.27m in sih_mvp_traffic.wbt")

# 2. Update pedestrian_controller.py runtime Z position to 1.27m
with open(CTRL_PATH, 'r', encoding='utf-8') as f:
    ctrl = f.read()

ctrl = ctrl.replace("0.05", "1.27")

with open(CTRL_PATH, 'w', encoding='utf-8') as f:
    f.write(ctrl)

print("Updated pedestrian_controller.py to set Z=1.27m on all position updates.")
