import xml.etree.ElementTree as ET

NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"
tree = ET.parse(NET_PATH)
root = tree.getroot()

for conn in root.findall('connection'):
    conn.set('keepClear', '1')

tree.write(NET_PATH, encoding='utf-8', xml_declaration=True)
print(f"Patched keepClear='1' across all connections in {NET_PATH}")
