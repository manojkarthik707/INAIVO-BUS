import xml.etree.ElementTree as ET

NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"
tree = ET.parse(NET_PATH)
root = tree.getroot()

# Ensure tlLogic 41 and 43 have clean static phases
for tl in root.findall('tlLogic'):
    if tl.get('id') in ['41', '43']:
        for p in list(tl.findall('phase')):
            tl.remove(p)
        ET.SubElement(tl, 'phase', {'duration': '12', 'state': 'GGgGGg'})
        ET.SubElement(tl, 'phase', {'duration': '2',  'state': 'yygGGg'})
        ET.SubElement(tl, 'phase', {'duration': '12', 'state': 'rrgGGg'})
        ET.SubElement(tl, 'phase', {'duration': '2',  'state': 'yygGGg'})

# Remove any previous shortcut connections
for conn in list(root.findall('connection')):
    f = conn.get('from', '')
    t = conn.get('to', '')
    if 'shortcut' in f or 'shortcut' in t:
        root.remove(conn)

# Add clean priority connections for shortcut edges (without tl attributes so they don't clash with tl link array)
shortcut_conns = [
    # Junction 41 (Left End)
    {'from': '8', 'to': 'shortcut_east', 'fromLane': '1', 'toLane': '1', 'dir': 'r', 'state': 'M'},
    {'from': '23', 'to': 'shortcut_east', 'fromLane': '0', 'toLane': '0', 'dir': 'l', 'state': 'M'},
    {'from': 'shortcut_west', 'to': '-8', 'fromLane': '0', 'toLane': '0', 'dir': 'l', 'state': 'M'},
    {'from': 'shortcut_west', 'to': '-23', 'fromLane': '1', 'toLane': '1', 'dir': 'r', 'state': 'M'},

    # Junction 43 (Right End)
    {'from': 'shortcut_east', 'to': '6', 'fromLane': '0', 'toLane': '0', 'dir': 'l', 'state': 'M'},
    {'from': 'shortcut_east', 'to': '-5', 'fromLane': '1', 'toLane': '1', 'dir': 'r', 'state': 'M'},
    {'from': '-5', 'to': 'shortcut_west', 'fromLane': '0', 'toLane': '0', 'dir': 'l', 'state': 'M'},
    {'from': '6', 'to': 'shortcut_west', 'fromLane': '1', 'toLane': '1', 'dir': 'r', 'state': 'M'},
]

for c in shortcut_conns:
    ET.SubElement(root, 'connection', c)

tree.write(NET_PATH, encoding='utf-8', xml_declaration=True)
print(f"Cleaned up shortcut connections in {NET_PATH}")
