import re

WBT_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt"
with open(WBT_PATH, 'r', encoding='utf-8') as f:
    wbt = f.read()

# 1. Optimize SumoInterface node in WBT
# Default SumoInterface { gui FALSE step 16 } -> optimize to step 32 with smooth interpolation
old_sumo = re.search(r'SumoInterface\s*\{[^}]*\}', wbt)
if old_sumo:
    new_sumo = """SumoInterface {
  gui FALSE
  step 32
  enableHeight FALSE
  publishVehicles FALSE
}"""
    wbt = wbt[:old_sumo.start()] + new_sumo + wbt[old_sumo.end():]
    print("Optimized SumoInterface node.")

# 2. Optimize WorldInfo basicTimeStep to 32 for ODE physics efficiency
wbt = re.sub(r'basicTimeStep\s+16', 'basicTimeStep 32', wbt)
print("Updated WorldInfo basicTimeStep to 32ms.")

with open(WBT_PATH, 'w', encoding='utf-8') as f:
    f.write(wbt)

print(f"Applied Webots performance optimizations to {WBT_PATH}")
