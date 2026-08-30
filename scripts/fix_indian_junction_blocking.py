"""
Fix junction 25 and 26 yield deadlocks.
The issue is Indian-style aggressive driving + high volume at 4-way intersections.
Solution: 
1. Increase greenTime at the hotspot junctions
2. Lower the jmIgnoreKeepClearTime - don't block box junction
3. Reduce volume through hotspot by splitting circuits
"""

import xml.etree.ElementTree as ET
import subprocess, os

net_dir = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net"
rou_path = os.path.join(net_dir, "sumo.rou.xml")

tree = ET.parse(rou_path)
root = tree.getroot()

for vt in root.findall("vType"):
    vid = vt.get("id")
    if vid == "passenger":
        # Fix box-junction blocking: reduce ignoreKeepClearTime
        vt.set("jmIgnoreKeepClearTime", "0.0")   # NEVER block box junction (Indian law MV Act 121)
        vt.set("jmDriveAfterYellowTime", "1.5")  # Drive through yellow (1.5s margin)
        vt.set("jmDriveAfterRedTime", "0.0")     # No running red lights
        vt.set("jmTimegapMinor", "1.2")           # Minimum gap when crossing
        vt.set("tau", "0.9")                      # Slightly more space (reduce jam)
        vt.set("minGap", "1.8")                   # Slightly more gap
    elif vid == "bus":
        vt.set("jmIgnoreKeepClearTime", "0.0")
        vt.set("jmDriveAfterYellowTime", "1.0")
        vt.set("jmTimegapMinor", "1.5")

tree.write(rou_path, encoding="utf-8", xml_declaration=True)
print("Fixed junction blocking behavior")

# Re-run to verify
result = subprocess.run([
    r"C:\Program Files (x86)\Eclipse\Sumo\bin\sumo.exe",
    "-c", os.path.join(net_dir, "sumo.sumocfg"),
    "--no-step-log", "--end", "300"
], capture_output=True, text=True)

lines = result.stdout.splitlines()
for l in lines:
    if any(k in l for k in ["Vehicles:", "Inserted", "Running", "Waiting", "Teleports", "Error", "Simulation ended"]):
        print(l)
