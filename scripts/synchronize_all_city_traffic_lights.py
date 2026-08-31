import xml.etree.ElementTree as ET
import subprocess

NOD_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\plain.nod.xml"
CFG_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\plain.netccfg"
TLL_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\plain.tll.xml"
NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"

# 1. Update plain.nod.xml
tree_nod = ET.parse(NOD_PATH)
root_nod = tree_nod.getroot()

for n in root_nod.findall('node'):
    n_id = n.get('id')
    if n_id in ['25', '26', '27', '41', '43']:
        n.set('type', 'traffic_light')
    elif n_id in ['44', '45']:
        n.set('type', 'priority')

tree_nod.write(NOD_PATH, encoding='utf-8', xml_declaration=True)
print("Updated node types in plain.nod.xml")

# 2. Compile netconvert
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

# 3. Synchronize exact 28s phases
tree = ET.parse(NET_PATH)
root = tree.getroot()

for lane in root.findall('.//lane'):
    for so in list(lane.findall('stopOffset')):
        lane.remove(so)

for conn in root.findall('connection'):
    conn.set('keepClear', '1')

for tl in root.findall('tlLogic'):
    tl_id = tl.get('id')
    for p in list(tl.findall('phase')):
        tl.remove(p)

    if tl_id == '25':
        ET.SubElement(tl, 'phase', {'duration': '5.0', 'state': 'GGGgrrrrrrrrrrrr'})
        ET.SubElement(tl, 'phase', {'duration': '2.0', 'state': 'yyyyrrrrrrrrrrrr'})
        ET.SubElement(tl, 'phase', {'duration': '5.0', 'state': 'rrrrGGGgrrrrrrrr'})
        ET.SubElement(tl, 'phase', {'duration': '2.0', 'state': 'rrrryyyyrrrrrrrr'})
        ET.SubElement(tl, 'phase', {'duration': '5.0', 'state': 'rrrrrrrrGGGgrrrr'})
        ET.SubElement(tl, 'phase', {'duration': '2.0', 'state': 'rrrrrrrryyyyrrrr'})
        ET.SubElement(tl, 'phase', {'duration': '5.0', 'state': 'rrrrrrrrrrrrGGGg'})
        ET.SubElement(tl, 'phase', {'duration': '2.0', 'state': 'rrrrrrrrrrrryyyy'})

    elif tl_id in ['26', '27']:
        ET.SubElement(tl, 'phase', {'duration': '5.0', 'state': 'GGGgrrrrrrrrrrrr'})
        ET.SubElement(tl, 'phase', {'duration': '2.0', 'state': 'yyyyrrrrrrrrrrrr'})
        ET.SubElement(tl, 'phase', {'duration': '5.0', 'state': 'rrrrGGGgrrrrrrrr'})
        ET.SubElement(tl, 'phase', {'duration': '2.0', 'state': 'rrrryyyyrrrrrrrr'})
        ET.SubElement(tl, 'phase', {'duration': '5.0', 'state': 'rrrrrrrrGGGgrrrr'})
        ET.SubElement(tl, 'phase', {'duration': '2.0', 'state': 'rrrrrrrryyyyrrrr'})
        ET.SubElement(tl, 'phase', {'duration': '5.0', 'state': 'rrrrrrrrrrrrGGGg'})
        ET.SubElement(tl, 'phase', {'duration': '2.0', 'state': 'rrrrrrrrrrrryyyy'})

    elif tl_id == '41':
        ET.SubElement(tl, 'phase', {'duration': '12.0', 'state': 'GGgrrGGg'})
        ET.SubElement(tl, 'phase', {'duration': '2.0',  'state': 'yyyrryyy'})
        ET.SubElement(tl, 'phase', {'duration': '12.0', 'state': 'rrrGGrrr'})
        ET.SubElement(tl, 'phase', {'duration': '2.0',  'state': 'rrryyrrr'})

    elif tl_id == '43':
        ET.SubElement(tl, 'phase', {'duration': '12.0', 'state': 'gGGGGgrr'})
        ET.SubElement(tl, 'phase', {'duration': '2.0',  'state': 'yyyyyyrr'})
        ET.SubElement(tl, 'phase', {'duration': '12.0', 'state': 'rrrrrrGG'})
        ET.SubElement(tl, 'phase', {'duration': '2.0',  'state': 'rrrrrryy'})

tree.write(NET_PATH, encoding='utf-8', xml_declaration=True)
print("Configured clean 28.0s synchronized TLS in SUMO net for all 5 junctions.")
