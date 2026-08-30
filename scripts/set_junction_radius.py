import xml.etree.ElementTree as ET
import os

net_dir = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net"
nod_path = os.path.join(net_dir, "plain.nod.xml")

tree = ET.parse(nod_path)
root = tree.getroot()

for node in root.findall("node"):
    nid = node.get("id")
    if nid in ["25", "26", "27"]:
        node.set("radius", "10.0")  # Huge radius to prevent intersecting turns
    elif node.get("type") == "traffic_light":
        node.set("radius", "8.0")

tree.write(nod_path, encoding="utf-8", xml_declaration=True)
print("Updated plain.nod.xml with explicit radius!")
