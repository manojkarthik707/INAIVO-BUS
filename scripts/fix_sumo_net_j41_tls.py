import xml.etree.ElementTree as ET

NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"
tree = ET.parse(NET_PATH)
root = tree.getroot()

# 1. Update junction 41 type to traffic_light
for j in root.findall('junction'):
    if j.get('id') == '41':
        j.set('type', 'traffic_light')

# 2. Ensure tlLogic id="41" exists before first junction
for tl in list(root.findall('tlLogic')):
    if tl.get('id') == '41':
        root.remove(tl)

first_junction_idx = None
for i, child in enumerate(root):
    if child.tag == 'junction':
        first_junction_idx = i
        break

if first_junction_idx is None:
    first_junction_idx = len(root)

tl41 = ET.Element('tlLogic', {
    'id': '41',
    'type': 'static',
    'programID': '0',
    'offset': '0'
})
ET.SubElement(tl41, 'phase', {'duration': '12', 'state': 'GGgGGg'})
ET.SubElement(tl41, 'phase', {'duration': '2',  'state': 'yygyyg'})
ET.SubElement(tl41, 'phase', {'duration': '12', 'state': 'rrgrrg'})
ET.SubElement(tl41, 'phase', {'duration': '2',  'state': 'yygyyg'})

root.insert(first_junction_idx, tl41)

# 3. Clean up connections for Junction 41 (0..5) and Junction 43 (0..5)
for conn in list(root.findall('connection')):
    f = conn.get('from', '')
    t = conn.get('to', '')
    if 'shortcut' in f or 'shortcut' in t:
        root.remove(conn)

# J41: Links 0..5
# Links 0,1: 8->-23, Link 2: 8->shortcut_east, Link 3,4: 23->-8, Link 5: shortcut_west->-8
j41_conns = [
    {'from': '8', 'to': '-23', 'fromLane': '0', 'toLane': '0', 'dir': 's', 'state': 'M', 'tl': '41', 'linkIndex': '0'},
    {'from': '8', 'to': '-23', 'fromLane': '1', 'toLane': '1', 'dir': 's', 'state': 'M', 'tl': '41', 'linkIndex': '1'},
    {'from': '8', 'to': 'shortcut_east', 'fromLane': '1', 'toLane': '1', 'dir': 'r', 'state': 'M', 'tl': '41', 'linkIndex': '2'},
    {'from': '23', 'to': '-8', 'fromLane': '0', 'toLane': '0', 'dir': 's', 'state': 'M', 'tl': '41', 'linkIndex': '3'},
    {'from': '23', 'to': '-8', 'fromLane': '1', 'toLane': '1', 'dir': 's', 'state': 'M', 'tl': '41', 'linkIndex': '4'},
    {'from': 'shortcut_west', 'to': '-8', 'fromLane': '0', 'toLane': '0', 'dir': 'l', 'state': 'M', 'tl': '41', 'linkIndex': '5'},
]

# J43: Priority merging connections without tl conflict
j43_conns = [
    {'from': 'shortcut_east', 'to': '6', 'fromLane': '0', 'toLane': '0', 'dir': 'l', 'state': 'M'},
    {'from': 'shortcut_east', 'to': '-5', 'fromLane': '1', 'toLane': '1', 'dir': 'r', 'state': 'M'},
    {'from': '-5', 'to': 'shortcut_west', 'fromLane': '0', 'toLane': '0', 'dir': 'l', 'state': 'M'},
    {'from': '6', 'to': 'shortcut_west', 'fromLane': '1', 'toLane': '1', 'dir': 'r', 'state': 'M'},
]

for c in j41_conns + j43_conns:
    ET.SubElement(root, 'connection', c)

tree.write(NET_PATH, encoding='utf-8', xml_declaration=True)
print(f"Properly configured tlLogic 41 and link indices in {NET_PATH}")
