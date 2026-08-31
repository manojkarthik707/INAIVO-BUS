import xml.etree.ElementTree as ET
import subprocess

CON_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\plain.con.xml"
CFG_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\plain.netccfg"
NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"

tree_con = ET.parse(CON_PATH)
root_con = tree_con.getroot()

for c in list(root_con.findall('connection')):
    f = c.get('from', '')
    t = c.get('to', '')
    if f == f"-{t}" or t == f"-{f}" or 'shortcut' in f or 'shortcut' in t:
        root_con.remove(c)

# Exact Indian LHD lane connections:
# Lane 0 is Left-most (driving lane). Lane 1 is Right (passing/turning lane).
shortcut_conns = [
    # Junction 41 (Left End):
    # - 8 (coming from South): Lane 0 (outer left) turns left into shortcut_east (lane 0)
    {'from': '8', 'to': 'shortcut_east', 'fromLane': '0', 'toLane': '0'},
    # - 23 (coming from North): Lane 1 (inner right) turns right into shortcut_east (lane 0)
    {'from': '23', 'to': 'shortcut_east', 'fromLane': '1', 'toLane': '0'},
    # - shortcut_west (coming from East): Lane 0 turns left into -23 (lane 0) and right into -8 (lane 1)
    {'from': 'shortcut_west', 'to': '-23', 'fromLane': '0', 'toLane': '0'},
    {'from': 'shortcut_west', 'to': '-8', 'fromLane': '0', 'toLane': '1'},

    # Junction 43 (Right End):
    # - 6 (coming from North): Lane 0 (outer left) turns left into shortcut_west (lane 0)
    {'from': '6', 'to': 'shortcut_west', 'fromLane': '0', 'toLane': '0'},
    # - -5 (coming from South): Lane 1 (inner right) turns right into shortcut_west (lane 0)
    {'from': '-5', 'to': 'shortcut_west', 'fromLane': '1', 'toLane': '0'},
    # - shortcut_east (coming from West): Lane 0 turns left into 5 (lane 0) and right into -6 (lane 1)
    {'from': 'shortcut_east', 'to': '5', 'fromLane': '0', 'toLane': '0'},
    {'from': 'shortcut_east', 'to': '-6', 'fromLane': '0', 'toLane': '1'},
]

for sc in shortcut_conns:
    ET.SubElement(root_con, 'connection', sc)

tree_con.write(CON_PATH, encoding='utf-8', xml_declaration=True)

cmd = [
    r"C:\Program Files (x86)\Eclipse\Sumo\bin\netconvert.exe",
    "-c", CFG_PATH,
    "--lefthand", "true",
    "--no-turnarounds", "true",
    "--no-turnarounds.tls", "true",
    "--tls.ignore-internal-junction-jam", "true",
    "-o", NET_PATH
]
res = subprocess.run(cmd, capture_output=True, text=True)
print("netconvert output:\n", res.stdout, res.stderr)

tree_net = ET.parse(NET_PATH)
root_net = tree_net.getroot()
for lane in root_net.findall('.//lane'):
    if not lane.get('id', '').startswith(':'):
        ET.SubElement(lane, 'stopOffset', {'value': '6.0'})

for conn in list(root_net.findall('connection')):
    if conn.get('dir') in ['t', 'T']:
        root_net.remove(conn)

tree_net.write(NET_PATH, encoding='utf-8', xml_declaration=True)
print("Updated Indian LHD connections and compiled sumo.net.xml successfully!")
