import xml.etree.ElementTree as ET

NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"
tree = ET.parse(NET_PATH)
root = tree.getroot()

for conn in root.findall('connection'):
    if conn.get('tl') == '41':
        print(ET.tostring(conn, encoding='unicode'))
