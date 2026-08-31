import xml.etree.ElementTree as ET

NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"
tree = ET.parse(NET_PATH)
root = tree.getroot()

# Find all connections for junction 41
j41_conns = []
for conn in list(root.findall('connection')):
    f = conn.get('from', '')
    t = conn.get('to', '')
    if conn.get('tl') == '41' or f in ['8', '23', 'shortcut_west'] or t in ['-8', '-23', 'shortcut_east']:
        root.remove(conn)

# Define exact clean set of 6 links for Junction 41:
# Link 0: 8_0 -> -23_0 (Straight North)
# Link 1: 8_1 -> -23_1 (Straight North)
# Link 2: 8_1 -> shortcut_east_1 (Right Turn East into shortcut)
# Link 3: 23_0 -> -8_0 (Straight South)
# Link 4: 23_1 -> -8_1 (Straight South)
# Link 5: shortcut_west_0 -> -8_0 (Left Turn South - Free Left on Red 'g')
conns_41 = [
    {'from': '8', 'to': '-23', 'fromLane': '0', 'toLane': '0', 'dir': 's', 'state': 'M', 'tl': '41', 'linkIndex': '0'},
    {'from': '8', 'to': '-23', 'fromLane': '1', 'toLane': '1', 'dir': 's', 'state': 'M', 'tl': '41', 'linkIndex': '1'},
    {'from': '8', 'to': 'shortcut_east', 'fromLane': '1', 'toLane': '1', 'dir': 'r', 'state': 'M', 'tl': '41', 'linkIndex': '2'},
    {'from': '23', 'to': '-8', 'fromLane': '0', 'toLane': '0', 'dir': 's', 'state': 'M', 'tl': '41', 'linkIndex': '3'},
    {'from': '23', 'to': '-8', 'fromLane': '1', 'toLane': '1', 'dir': 's', 'state': 'M', 'tl': '41', 'linkIndex': '4'},
    {'from': 'shortcut_west', 'to': '-8', 'fromLane': '0', 'toLane': '0', 'dir': 'l', 'state': 'M', 'tl': '41', 'linkIndex': '5'},
]

for c in conns_41:
    ET.SubElement(root, 'connection', c)

# Update tlLogic 41 phases with exact 6 characters matching links 0..5
for tl in list(root.findall('tlLogic')):
    if tl.get('id') == '41':
        root.remove(tl)

first_junc = None
for i, child in enumerate(root):
    if child.tag == 'junction':
        first_junc = i
        break

tl41 = ET.Element('tlLogic', {
    'id': '41',
    'type': 'static',
    'programID': '0',
    'offset': '0'
})
# State chars: 0: 8_s, 1: 8_s, 2: 8_r, 3: 23_s, 4: 23_s, 5: shortcut_west_l (Free Left 'g')
ET.SubElement(tl41, 'phase', {'duration': '12', 'state': 'GGgGGg'}) # Main North-South GREEN + Shortcut Free-Left 'g'
ET.SubElement(tl41, 'phase', {'duration': '2',  'state': 'yygGGg'}) # Yellow transition
ET.SubElement(tl41, 'phase', {'duration': '12', 'state': 'rrgGGg'}) # Shortcut GREEN
ET.SubElement(tl41, 'phase', {'duration': '2',  'state': 'yygGGg'}) # Yellow transition

root.insert(first_junc if first_junc is not None else 0, tl41)

tree.write(NET_PATH, encoding='utf-8', xml_declaration=True)
print(f"Re-indexed Junction 41 with 6 clean link indices (0..5) in {NET_PATH}")
