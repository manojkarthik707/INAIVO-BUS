import xml.etree.ElementTree as ET
import subprocess

NOD_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\plain.nod.xml"
CFG_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\plain.netccfg"
NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"

tree_nod = ET.parse(NOD_PATH)
root_nod = tree_nod.getroot()

for n in root_nod.findall('node'):
    if n.get('id') in ['41', '43']:
        n.set('type', 'priority')

tree_nod.write(NOD_PATH, encoding='utf-8', xml_declaration=True)

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
print("Configured nodes 41 and 43 as priority junctions and compiled sumo.net.xml successfully!")
