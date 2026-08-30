"""
Comprehensive SUMO Traffic System Overhaul:
1. Proper traffic lights at all 4-way intersections (25, 26, 27) with real phases
2. Proper junction corner detail for smooth turn radius
3. Turn speed limits to prevent vehicles from taking turns too fast
4. Junction type fixes for 2-way merges (should be 'priority' not causing conflicts)
"""

import subprocess
import os
import math
import xml.etree.ElementTree as ET

net_dir = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net"

# === STEP 1: Fix node types — mark 4-way intersections as traffic_light ===
nod_path = os.path.join(net_dir, "plain.nod.xml")
tree_nod = ET.parse(nod_path)
root_nod = tree_nod.getroot()

# The 3 true 4-way intersections
TRAFFIC_LIGHT_JUNCTIONS = {"25", "26", "27", "43", "44", "45", "41"}
PRIORITY_JUNCTIONS = {"28", "29", "30", "31", "32", "33", "34", "35",
                      "36", "37", "38", "39", "40", "42"}

for node in root_nod.findall("node"):
    nid = node.get("id")
    if nid in TRAFFIC_LIGHT_JUNCTIONS:
        node.set("type", "traffic_light")
    elif nid in PRIORITY_JUNCTIONS:
        node.set("type", "priority")
    elif nid in ("Custom21", "Custom22"):
        node.set("type", "priority")

tree_nod.write(nod_path, encoding="utf-8", xml_declaration=True)
print("Step 1 done: Updated junction types in plain.nod.xml")


# === STEP 2: Compile network with aggressive traffic light + turn radius settings ===
cmd = [
    r"C:\Program Files (x86)\Eclipse\Sumo\bin\netconvert.exe",
    "--node-files", os.path.join(net_dir, "plain.nod.xml"),
    "--edge-files", os.path.join(net_dir, "plain.edg.xml"),
    "--connection-files", os.path.join(net_dir, "plain.con.xml"),
    "--offset.disable-normalization", "true",
    "--no-turnarounds", "true",

    # Traffic light settings
    "--tls.green.time", "18",           # 18-second generous green wave
    "--tls.yellow.time", "3",           # 3-second yellow clearance
    "--tls.allred.time", "2",           # 2-second all-red gap before cross traffic
    "--tls.left-green.time", "6",       # Left turn protected phase
    "--tls.default-type", "actuated",   # Actuated = responds to real vehicle demand

    # Junction geometry - smooth turn radius
    "--junctions.corner-detail", "16",       # 16-point smooth Bezier corners
    "--junctions.limit-turn-speed", "4.5",   # Max 4.5 m/s (~16 km/h) for 90° turns
    "--junctions.small-radius", "1.5",       # Small radius minimum tightening
    "--junctions.internal-link-detail", "10", # 10-point internal junction lane curves

    # Lane change and geometry
    "--geometry.min-radius", "3.0",          # Minimum road curve radius
    "--geometry.min-radius.fix", "true",     # Fix curves tighter than 3m
    "--no-internal-links", "false",          # Use internal junction links for smooth turns

    "-o", os.path.join(net_dir, "sumo.net.xml")
]

result = subprocess.run(cmd, capture_output=True, text=True)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr[:2000] if result.stderr else "")
if result.returncode != 0:
    raise RuntimeError(f"netconvert failed with code {result.returncode}")

print("\nStep 2 done: Compiled network with smooth turn radii and proper traffic lights!")
