import math
import xml.etree.ElementTree as ET
import subprocess
import os

net_dir = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net"

# 1. Update Custom21 position in plain.nod.xml to (39.50, 0.01)
nod_path = os.path.join(net_dir, "plain.nod.xml")
tree_nod = ET.parse(nod_path)
root_nod = tree_nod.getroot()
for n in root_nod.findall("node"):
    if n.get("id") == "Custom21":
        n.set("x", "39.50")
        n.set("y", "0.01")
tree_nod.write(nod_path, encoding='utf-8', xml_declaration=True)

# 2. Compute exact smooth 16-point circular arc for Top-Left Curve
# Center: (39.50, 378.01), Radius: 40.5, theta from 90 deg down to 180 deg
top_curve_pts = []
for i in range(17):
    theta = (math.pi / 2) + i * (math.pi / 2) / 16
    x = 39.50 + 40.5 * math.cos(theta)
    y = 378.01 + 40.5 * math.sin(theta)
    top_curve_pts.append(f"{x:.2f},{y:.2f}")

# 3. Compute exact smooth 16-point circular arc for Bottom-Left Curve
# Center: (39.50, 40.51), Radius: 40.5, theta from 180 deg down to 270 deg
bottom_curve_pts = []
for i in range(17):
    theta = math.pi + i * (math.pi / 2) / 16
    x = 39.50 + 40.5 * math.cos(theta)
    y = 40.51 + 40.5 * math.sin(theta)
    bottom_curve_pts.append(f"{x:.2f},{y:.2f}")

full_outer_west_shape = " ".join(top_curve_pts + ["-1.00,200.00"] + bottom_curve_pts)
full_rev_outer_west_shape = " ".join(reversed(top_curve_pts + ["-1.00,200.00"] + bottom_curve_pts))

# 4. Update edge shapes in plain.edg.xml
edg_path = os.path.join(net_dir, "plain.edg.xml")
tree_edg = ET.parse(edg_path)
root_edg = tree_edg.getroot()

for e in root_edg.findall("edge"):
    if e.get("id") == "outer_west":
        e.set("shape", full_outer_west_shape)
    elif e.get("id") == "-outer_west":
        e.set("shape", full_rev_outer_west_shape)
    elif e.get("id") == "13":
        e.set("shape", "250.00,0.01 39.50,0.01")
    elif e.get("id") == "-13":
        e.set("shape", "39.50,0.01 250.00,0.01")

tree_edg.write(edg_path, encoding='utf-8', xml_declaration=True)

# 5. Recompile sumo.net.xml with netconvert
cmd = [
    r"C:\Program Files (x86)\Eclipse\Sumo\bin\netconvert.exe",
    "--node-files", os.path.join(net_dir, "plain.nod.xml"),
    "--edge-files", os.path.join(net_dir, "plain.edg.xml"),
    "--connection-files", os.path.join(net_dir, "plain.con.xml"),
    "--offset.disable-normalization", "true",
    "--no-turnarounds", "true",
    "--tls.guess", "true",
    "--tls.green.time", "15",
    "--tls.yellow.time", "3",
    "--tls.allred.time", "1",
    "-o", os.path.join(net_dir, "sumo.net.xml")
]

subprocess.run(cmd, check=True)
print("Successfully compiled mathematically perfect smooth circular curves in sumo.net.xml!")
