import xml.etree.ElementTree as ET

NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"
tree = ET.parse(NET_PATH)
root = tree.getroot()

for j in root.findall('junction'):
    if j.get('id') in ['41', '43']:
        print(ET.tostring(j, encoding='unicode'))
