import xml.etree.ElementTree as ET
import os

net_dir = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net"
rou_path = os.path.join(net_dir, "sumo.rou.xml")

tree = ET.parse(rou_path)
root = tree.getroot()

for vt in root.findall("vType"):
    vid = vt.get("id")
    # -1 means NEVER enter an intersection unless you can fully clear it
    vt.set("jmIgnoreKeepClearTime", "-1")
    # Strictly respect right-of-way
    vt.set("jmIgnoreJunctionFoeProb", "0.0")
    # Minimum time gap to accept crossing
    vt.set("jmTimegapMinor", "1.5")
    # Lower acceleration to prevent snappy entry into blocked junctions
    vt.set("accel", "1.5")
    
    if vid == "bus":
        vt.set("accel", "1.0")
        vt.set("jmTimegapMinor", "2.0")

tree.write(rou_path, encoding="utf-8", xml_declaration=True)
print("Updated sumo.rou.xml with strict keep-clear logic")
