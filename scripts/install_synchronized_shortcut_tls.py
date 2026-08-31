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
# 1. SET NODE 41 & 43 TO TYPE="TRAFFIC_LIGHT" IN PLAIN.NOD.XML
# ==============================================================================
tree_nod = ET.parse(NOD_PATH)
root_nod = tree_nod.getroot()

for n in root_nod.findall('node'):
    if n.get('id') in ['41', '43']:
        n.set('type', 'traffic_light')

tree_nod.write(NOD_PATH, encoding='utf-8', xml_declaration=True)
print("Updated Junctions 41 & 43 to type='traffic_light' in plain.nod.xml")

# ==============================================================================
# 2. CONFIGURE 28s SYNCHRONIZED TRAFFIC LIGHT PROGRAMS IN PLAIN.TLL.XML
# ==============================================================================
# Clear plain.tll.xml so netconvert builds default clean links, then we customize
tll_content = """<?xml version="1.0" encoding="UTF-8"?>
<tlLogics version="1.20" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/tllogic_file.xsd">
</tlLogics>
"""
with open(TLL_PATH, 'w', encoding='utf-8') as f:
    f.write(tll_content)

# ==============================================================================
# 3. COMPILE SUMO.NET.XML WITH NETCONVERT
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
# 4. INSPECT TLS LINKS AT 41 & 43 AND INJECT 28s REALISTIC PHASES WITHOUT STOPOFFSET
# ==============================================================================
tree_net = ET.parse(NET_PATH)
root_net = tree_net.getroot()

# Remove all stopOffset so vehicles pull up right to the front stop line
for lane in root_net.findall('.//lane'):
    for so in list(lane.findall('stopOffset')):
        lane.remove(so)

for conn in root_net.findall('connection'):
    conn.set('keepClear', '1')

# Configure TLS 41 and TLS 43
# Let's inspect the link indices for TLS 41 and TLS 43
for tl in root_net.findall('tlLogic'):
    tl_id = tl.get('id')
    if tl_id in ['41', '43']:
        # Find connections controlled by this tlLogic
        conns = []
        for c in root_net.findall('connection'):
            if c.get('tl') == tl_id:
                conns.append((int(c.get('linkIndex', 0)), c.get('from'), c.get('to')))
        conns.sort(key=lambda x: x[0])
        num_links = len(conns)
        print(f"\nTLS {tl_id} controls {num_links} links:")
        for idx, f, t in conns:
            print(f"  Link {idx}: from {f} to {t}")

        # Build 28s cycle:
        # Phase 0 (12s): Main Road GREEN (links from 23, 8, -5, 6 are 'G'/'g'), Shortcut is 'r'
        # Phase 1 (2s):  Main Road AMBER (links from 23, 8, -5, 6 are 'y'), Shortcut is 'r'
        # Phase 2 (12s): Shortcut Road GREEN (links from shortcut are 'G'/'g'), Main Road is 'r'
        # Phase 3 (2s):  Shortcut Road AMBER (links from shortcut are 'y'), Main Road is 'r'

        state_phase0 = []
        state_phase1 = []
        state_phase2 = []
        state_phase3 = []

        for idx, f, t in conns:
            if 'shortcut' in f:
                # Shortcut approach
                state_phase0.append('r')
                state_phase1.append('r')
                state_phase2.append('G')
                state_phase3.append('y')
            else:
                # Main Road approach
                state_phase0.append('G')
                state_phase1.append('y')
                state_phase2.append('r')
                state_phase3.append('r')

        p0_str = "".join(state_phase0)
        p1_str = "".join(state_phase1)
        p2_str = "".join(state_phase2)
        p3_str = "".join(state_phase3)

        # Clear existing phases
        for p in list(tl.findall('phase')):
            tl.remove(p)

        ET.SubElement(tl, 'phase', {'duration': '12.0', 'state': p0_str})
        ET.SubElement(tl, 'phase', {'duration': '2.0',  'state': p1_str})
        ET.SubElement(tl, 'phase', {'duration': '12.0', 'state': p2_str})
        ET.SubElement(tl, 'phase', {'duration': '2.0',  'state': p3_str})

        print(f"Injected 28s TLS Logic for {tl_id}:")
        print(f"  Phase 0 (12s Main Green): {p0_str}")
        print(f"  Phase 1 (2s Main Amber):  {p1_str}")
        print(f"  Phase 2 (12s SC Green):   {p2_str}")
        print(f"  Phase 3 (2s SC Amber):    {p3_str}")

tree_net.write(NET_PATH, encoding='utf-8', xml_declaration=True)
print("\nSaved synchronized SUMO net with active TLS at Junctions 41 and 43!")
