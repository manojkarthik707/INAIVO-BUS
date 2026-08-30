import subprocess
import os
import xml.etree.ElementTree as ET

net_dir = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net"

cmd = [
    r"C:\Program Files (x86)\Eclipse\Sumo\bin\netconvert.exe",
    "--node-files",       os.path.join(net_dir, "plain.nod.xml"),
    "--edge-files",       os.path.join(net_dir, "plain.edg.xml"),
    "--connection-files", os.path.join(net_dir, "plain.con.xml"),
    "--offset.disable-normalization", "true",
    "--no-turnarounds",   "true",
    "--lefthand",         "true",
    
    # Traffic lights: Add protected left-green (which means crossing turn)
    "--tls.green.time",   "18",
    "--tls.yellow.time",  "3",
    "--tls.allred.time",  "2",
    "--tls.left-green.time", "6",        # Protected turn phase to prevent yield deadlocks!
    "--tls.default-type", "static",

    # Increase junction radius to prevent intersecting turns and give buses space
    "--junctions.corner-detail",       "16",
    "--junctions.limit-turn-speed",    "5.5",  
    "--junctions.higher-speed",        "true",
    
    # The magical fix for intersecting left turns!
    "--default.junctions.radius",      "8.0",
    
    "-o", os.path.join(net_dir, "sumo.net.xml")
]

result = subprocess.run(cmd, capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)

# We also need to fix collisions. 
# Vehicles in sumo.rou.xml need collision.action="teleport" but let's change jmIgnoreKeepClearTime 
rou_path = os.path.join(net_dir, "sumo.rou.xml")
tree = ET.parse(rou_path)
root = tree.getroot()

for vt in root.findall("vType"):
    vid = vt.get("id")
    # Make sure we don't have -1 which might cause indefinite waiting in some junction geometries
    # Set to 0.1 so they don't block, but aren't perfectly strict
    vt.set("jmIgnoreKeepClearTime", "0.1")
    # Allow yielding vehicles to cross if gap is > 1.2
    vt.set("jmTimegapMinor", "1.2")
    vt.set("jmDriveAfterRedTime", "0.0")

tree.write(rou_path, encoding="utf-8", xml_declaration=True)
print("Updated sumo.rou.xml")

