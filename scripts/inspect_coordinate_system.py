import xml.etree.ElementTree as ET

NOD_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\plain.nod.xml"
NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"

tree_nod = ET.parse(NOD_PATH)
root_nod = tree_nod.getroot()
print("=== Nodes from plain.nod.xml ===")
for n in root_nod.findall('node'):
    print(f"Node {n.get('id')}: x={n.get('x')}, y={n.get('y')}")

tree_net = ET.parse(NET_PATH)
root_net = tree_net.getroot()
loc = root_net.find('location')
if loc is not None:
    print("\n=== Location in sumo.net.xml ===")
    print("netOffset:", loc.get('netOffset'))
    print("convBoundary:", loc.get('convBoundary'))
    print("origBoundary:", loc.get('origBoundary'))
