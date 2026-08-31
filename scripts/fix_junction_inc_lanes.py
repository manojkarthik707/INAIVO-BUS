import xml.etree.ElementTree as ET

NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"
tree = ET.parse(NET_PATH)
root = tree.getroot()

for j in root.findall('junction'):
    jid = j.get('id')
    if jid == '41':
        j.set('incLanes', '8_0 8_1 23_0 23_1 shortcut_west_0 shortcut_west_1')
    elif jid == '43':
        j.set('incLanes', '-5_0 -5_1 6_0 6_1 shortcut_east_0 shortcut_east_1')

tree.write(NET_PATH, encoding='utf-8', xml_declaration=True)
print(f"Updated junction incLanes in {NET_PATH}")
