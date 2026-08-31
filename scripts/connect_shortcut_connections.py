import xml.etree.ElementTree as ET

NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"
tree = ET.parse(NET_PATH)
root = tree.getroot()

# Remove any existing shortcut connections to avoid duplicates
for conn in list(root.findall('connection')):
    f = conn.get('from', '')
    t = conn.get('to', '')
    if 'shortcut' in f or 'shortcut' in t:
        root.remove(conn)

# Add Junction 41 connections
j41_conns = [
    {'from': '8', 'to': 'shortcut_east', 'fromLane': '1', 'toLane': '1', 'dir': 'r', 'state': 'M', 'tl': '41', 'linkIndex': '3'},
    {'from': '23', 'to': 'shortcut_east', 'fromLane': '0', 'toLane': '0', 'dir': 'l', 'state': 'M', 'tl': '41', 'linkIndex': '4'},
    {'from': 'shortcut_west', 'to': '-8', 'fromLane': '0', 'toLane': '0', 'dir': 'l', 'state': 'M', 'tl': '41', 'linkIndex': '5'},
    {'from': 'shortcut_west', 'to': '-23', 'fromLane': '1', 'toLane': '1', 'dir': 'r', 'state': 'M', 'tl': '41', 'linkIndex': '6'},
]

# Add Junction 43 connections
j43_conns = [
    {'from': 'shortcut_east', 'to': '6', 'fromLane': '0', 'toLane': '0', 'dir': 'l', 'state': 'M', 'tl': '43', 'linkIndex': '3'},
    {'from': 'shortcut_east', 'to': '-5', 'fromLane': '1', 'toLane': '1', 'dir': 'r', 'state': 'M', 'tl': '43', 'linkIndex': '4'},
    {'from': '-5', 'to': 'shortcut_west', 'fromLane': '0', 'toLane': '0', 'dir': 'l', 'state': 'M', 'tl': '43', 'linkIndex': '5'},
    {'from': '6', 'to': 'shortcut_west', 'fromLane': '1', 'toLane': '1', 'dir': 'r', 'state': 'M', 'tl': '43', 'linkIndex': '6'},
]

for c in j41_conns + j43_conns:
    elem = ET.SubElement(root, 'connection', c)

tree.write(NET_PATH, encoding='utf-8', xml_declaration=True)
print(f"Successfully added shortcut connections in {NET_PATH}")
