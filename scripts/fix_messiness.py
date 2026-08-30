"""
Fix the messiness (traffic jams & gridlocks)
1. Recompile network with static traffic lights (actuated causes starvation on small dense grids)
2. Enforce strict box-junction rules (jmIgnoreKeepClearTime = -1)
3. Relax the aggressive Indian driving behavior slightly to prevent bumper-locking
"""

import subprocess
import os
import xml.etree.ElementTree as ET

net_dir = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net"

# 1. Recompile with static lights
cmd = [
    r"C:\Program Files (x86)\Eclipse\Sumo\bin\netconvert.exe",
    "--node-files",       os.path.join(net_dir, "plain.nod.xml"),
    "--edge-files",       os.path.join(net_dir, "plain.edg.xml"),
    "--connection-files", os.path.join(net_dir, "plain.con.xml"),
    "--offset.disable-normalization", "true",
    "--no-turnarounds",   "true",
    "--lefthand",         "true",
    
    # Static traffic lights (more predictable, no starvation)
    "--tls.green.time",   "20",
    "--tls.yellow.time",  "4",
    "--tls.allred.time",  "3",
    "--tls.default-type", "static",

    # Smooth turns
    "--junctions.corner-detail",       "16",
    "--junctions.limit-turn-speed",    "4.5",
    "--junctions.small-radius",        "1.5",
    "--junctions.internal-link-detail","10",
    "--geometry.min-radius",           "3.0",
    "--geometry.min-radius.fix",       "true",
    "-o", os.path.join(net_dir, "sumo.net.xml")
]

subprocess.run(cmd, check=True)
print("Network recompiled with static traffic lights.")

# 2. Fix driving behavior in sumo.rou.xml
rou_path = os.path.join(net_dir, "sumo.rou.xml")
tree = ET.parse(rou_path)
root = tree.getroot()

for vt in root.findall("vType"):
    vid = vt.get("id")
    # Strict Keep-Clear: -1 means NEVER enter a blocked junction
    vt.set("jmIgnoreKeepClearTime", "-1")
    vt.set("jmDriveAfterRedTime", "0.0")
    
    if vid == "passenger":
        vt.set("tau", "1.2")         # Relaxed gap
        vt.set("minGap", "2.5")      # Better bumper gap
        vt.set("speedFactor", "1.0") # No speeding
        vt.set("sigma", "0.5")       # Less erratic
        vt.set("lcStrategic", "1.0") # Normal lane changes
        vt.set("jmTimegapMinor", "1.5")
    elif vid == "bus":
        vt.set("tau", "1.5")
        vt.set("minGap", "3.0")
        vt.set("sigma", "0.2")

tree.write(rou_path, encoding="utf-8", xml_declaration=True)
print("Driving parameters relaxed to prevent gridlocks.")

# 3. Increase teleport time in sumocfg to let jams resolve naturally
cfg_path = os.path.join(net_dir, "sumo.sumocfg")
cfg_tree = ET.parse(cfg_path)
cfg_root = cfg_tree.getroot()
for child in cfg_root.find("processing"):
    if child.tag == "time-to-teleport":
        child.set("value", "90")
cfg_tree.write(cfg_path, encoding="utf-8", xml_declaration=True)
print("sumo.sumocfg updated.")
