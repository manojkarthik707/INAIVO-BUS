import xml.etree.ElementTree as ET
import subprocess

EDG_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\plain.edg.xml"
CON_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\plain.con.xml"
CFG_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\plain.netccfg"
NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"

# 1. Update plain.edg.xml
tree_edg = ET.parse(EDG_PATH)
root_edg = tree_edg.getroot()

for e in list(root_edg.findall('edge')):
    if e.get('id') in ['shortcut_east', 'shortcut_west']:
        root_edg.remove(e)

ET.SubElement(root_edg, 'edge', {
    'id': 'shortcut_east',
    'from': '41',
    'to': '43',
    'priority': '-1',
    'numLanes': '2',
    'speed': '13.90',
    'width': '5.38'
})
ET.SubElement(root_edg, 'edge', {
    'id': 'shortcut_west',
    'from': '43',
    'to': '41',
    'priority': '-1',
    'numLanes': '2',
    'speed': '13.90',
    'width': '5.38'
})
tree_edg.write(EDG_PATH, encoding='utf-8', xml_declaration=True)

# 2. Update plain.con.xml with exact valid from/to edges at 41 and 43
tree_con = ET.parse(CON_PATH)
root_con = tree_con.getroot()

for c in list(root_con.findall('connection')):
    f = c.get('from', '')
    t = c.get('to', '')
    if 'shortcut' in f or 'shortcut' in t:
        root_con.remove(c)

conns = [
    # Junction 41 (Left End):
    # Enters 41: 8 (from South), 23 (from North), shortcut_west (from East)
    # Leaves 41: -23 (to North), -8 (to South), shortcut_east (to East)
    {'from': '8', 'to': 'shortcut_east', 'fromLane': '1', 'toLane': '1'},
    {'from': '23', 'to': 'shortcut_east', 'fromLane': '0', 'toLane': '0'},
    {'from': 'shortcut_west', 'to': '-8', 'fromLane': '0', 'toLane': '0'},
    {'from': 'shortcut_west', 'to': '-23', 'fromLane': '1', 'toLane': '1'},

    # Junction 43 (Right End):
    # Enters 43: -5 (from South), 6 (from North), shortcut_east (from West)
    # Leaves 43: 5 (to South), -6 (to North), shortcut_west (to West)
    {'from': 'shortcut_east', 'to': '-6', 'fromLane': '0', 'toLane': '0'},
    {'from': 'shortcut_east', 'to': '5', 'fromLane': '1', 'toLane': '1'},
    {'from': '-5', 'to': 'shortcut_west', 'fromLane': '0', 'toLane': '0'},
    {'from': '6', 'to': 'shortcut_west', 'fromLane': '1', 'toLane': '1'},
]

for c in conns:
    ET.SubElement(root_con, 'connection', c)

tree_con.write(CON_PATH, encoding='utf-8', xml_declaration=True)

# 3. Run netconvert
cmd = [
    r"C:\Program Files (x86)\Eclipse\Sumo\bin\netconvert.exe",
    "-c", CFG_PATH,
    "-o", NET_PATH
]
res = subprocess.run(cmd, capture_output=True, text=True)
print("netconvert output:\n", res.stdout, res.stderr)

# 4. Patch stopOffsets into sumo.net.xml for safe crosswalk clearance
tree_net = ET.parse(NET_PATH)
root_net = tree_net.getroot()
for lane in root_net.findall('.//lane'):
    if not lane.get('id', '').startswith(':'):
        ET.SubElement(lane, 'stopOffset', {'value': '6.0'})

tree_net.write(NET_PATH, encoding='utf-8', xml_declaration=True)
print("Cleanly compiled and patched sumo.net.xml with netconvert!")
