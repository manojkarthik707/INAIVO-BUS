import xml.etree.ElementTree as ET
import random
import os

net_dir = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net"
rou_path = os.path.join(net_dir, "sumo.rou.xml")

tree = ET.parse(rou_path)
root = tree.getroot()

# Just loop through and change 80% of buses to passenger cars
for vt in root.findall("vehicle"):
    if vt.get("type") == "bus":
        if random.random() < 0.8:  # 80% chance to become a car
            vt.set("type", "passenger")

tree.write(rou_path, encoding="utf-8", xml_declaration=True)
print("Bus count drastically reduced!")
