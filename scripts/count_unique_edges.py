import xml.etree.ElementTree as ET

NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"
tree = ET.parse(NET_PATH)
root = tree.getroot()

edges = [e.get('id') for e in root.findall('edge') if not e.get('id', '').startswith(':')]
print(f"Total non-internal edges in network: {len(edges)}")
print("Edges:", edges)
