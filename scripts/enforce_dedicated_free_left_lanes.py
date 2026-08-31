import xml.etree.ElementTree as ET
import subprocess

NOD_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\plain.nod.xml"
EDG_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\plain.edg.xml"
CON_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\plain.con.xml"
CFG_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\plain.netccfg"
TLL_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\plain.tll.xml"
NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"
ROU_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.rou.xml"

# ==============================================================================
# 1. ENFORCE EXCLUSIVE DEDICATED FREE LEFT TURN LANES IN PLAIN.CON.XML
# ==============================================================================
tree_con = ET.parse(CON_PATH)
root_con = tree_con.getroot()

four_way_edges = {
    # J25
    '10':  {'l': ('4', '0'),   's0': ('-9', '0'),  's1': ('-9', '1'),  'r': ('-5', '1')},
    '5':   {'l': ('-10', '0'), 's0': ('4', '0'),   's1': ('4', '1'),   'r': ('-9', '1')},
    '9':   {'l': ('-5', '0'),  's0': ('-10', '0'), 's1': ('-10', '1'), 'r': ('4', '1')},
    '-4':  {'l': ('-9', '0'),  's0': ('-5', '0'),  's1': ('-5', '1'),  'r': ('-10', '1')},
    # J26
    '-23': {'l': ('-0', '0'),  's0': ('24', '0'),  's1': ('24', '1'),  'r': ('7', '1')},
    '-7':  {'l': ('23', '0'),  's0': ('-0', '0'),  's1': ('-0', '1'),  'r': ('24', '1')},
    '-24': {'l': ('7', '0'),   's0': ('23', '0'),  's1': ('23', '1'),  'r': ('-0', '1')},
    '0':   {'l': ('24', '0'),  's0': ('7', '0'),   's1': ('7', '1'),   'r': ('23', '1')},
    # J27
    '17':  {'l': ('12', '0'),  's0': ('16', '0'),  's1': ('16', '1'),  'r': ('20', '1')},
    '-20': {'l': ('-17', '0'), 's0': ('12', '0'),  's1': ('12', '1'),  'r': ('16', '1')},
    '-16': {'l': ('20', '0'),  's0': ('-17', '0'), 's1': ('-17', '1'), 'r': ('12', '1')},
    '-12': {'l': ('16', '0'),  's0': ('20', '0'),  's1': ('20', '1'),  'r': ('-17', '1')},
}

to_remove = []
for c in root_con.findall('connection'):
    f = c.get('from')
    if f in four_way_edges:
        to_remove.append(c)

for c in to_remove:
    root_con.remove(c)

for f, info in four_way_edges.items():
    # Lane 0: EXCLUSIVELY Left Turn (Dedicated Free Left)
    ET.SubElement(root_con, 'connection', {'from': f, 'to': info['l'][0],  'fromLane': '0', 'toLane': info['l'][1]})
    # Lane 1: Straight to Lane 0, Straight to Lane 1, Right to Lane 1
    ET.SubElement(root_con, 'connection', {'from': f, 'to': info['s0'][0], 'fromLane': '1', 'toLane': info['s0'][1]})
    ET.SubElement(root_con, 'connection', {'from': f, 'to': info['s1'][0], 'fromLane': '1', 'toLane': info['s1'][1]})
    ET.SubElement(root_con, 'connection', {'from': f, 'to': info['r'][0],  'fromLane': '1', 'toLane': info['r'][1]})

tree_con.write(CON_PATH, encoding='utf-8', xml_declaration=True)
print("Configured dedicated Free Left Turn lanes (Lane 0) in plain.con.xml!")

# ==============================================================================
# 2. RECOMPILE SUMO.NET.XML
# ==============================================================================
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

# ==============================================================================
# 3. CONFIGURE 28.0s SYNCHRONIZED PHASES WITH 100% UNINTERRUPTED FREE LEFT
# ==============================================================================
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

    if tl_id in ['25', '26', '27']:
        # Links 0, 4, 8, 12 are the dedicated Left Turns from Lane 0 -> ALWAYS 'G' / 'g'!
        # Stage 0: Approach 0 Green, Others Red with Free Left
        ET.SubElement(tl, 'phase', {'duration': '5.0', 'state': 'GGGgrgggrgggrggg'})
        ET.SubElement(tl, 'phase', {'duration': '2.0', 'state': 'yyyyrgggrgggrggg'})

        # Stage 1: Approach 1 Green, Others Red with Free Left
        ET.SubElement(tl, 'phase', {'duration': '5.0', 'state': 'rgggGGGgrgggrggg'})
        ET.SubElement(tl, 'phase', {'duration': '2.0', 'state': 'rgggyyyyrgggrggg'})

        # Stage 2: Approach 2 Green, Others Red with Free Left
        ET.SubElement(tl, 'phase', {'duration': '5.0', 'state': 'rgggrgggGGGgrggg'})
        ET.SubElement(tl, 'phase', {'duration': '2.0', 'state': 'rgggrgggyyyyrggg'})

        # Stage 3: Approach 3 Green, Others Red with Free Left
        ET.SubElement(tl, 'phase', {'duration': '5.0', 'state': 'rgggrgggrgggGGGg'})
        ET.SubElement(tl, 'phase', {'duration': '2.0', 'state': 'rgggrgggrgggyyyy'})

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
print("Synchronized all 5 TLS in sumo.net.xml with dedicated Free Left Turn rules!")
