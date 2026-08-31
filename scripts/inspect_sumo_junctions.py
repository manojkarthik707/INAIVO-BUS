import xml.etree.ElementTree as ET

NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"
tree = ET.parse(NET_PATH)
root = tree.getroot()

print("=== JUNCTIONS IN SUMO NET ===")
for j in root.findall('junction'):
    jid = j.get('id')
    x = float(j.get('x', 0))
    y = float(j.get('y', 0))
    t = j.get('type')
    inc = j.get('incLanes')
    print(f"Junction {jid:5s} at ({x:7.2f}, {y:7.2f}) type={t} incLanes={inc}")
