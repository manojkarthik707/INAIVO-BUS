import xml.etree.ElementTree as ET
import subprocess

NOD_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\plain.nod.xml"
EDG_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\plain.edg.xml"
CON_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\plain.con.xml"
CFG_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\plain.netccfg"
TLL_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\plain.tll.xml"
NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"

# ==============================================================================
# 1. CLEAN PLAIN.CON.XML (REMOVE INVALID ATTRIBUTES)
# ==============================================================================
tree_con = ET.parse(CON_PATH)
root_con = tree_con.getroot()

for c in root_con.findall('connection'):
    if 'cont' in c.attrib:
        del c.attrib['cont']

tree_con.write(CON_PATH, encoding='utf-8', xml_declaration=True)

# ==============================================================================
# 2. CONFIGURE NO-INTERNAL-LINKS IN PLAIN.NETCCFG
# ==============================================================================
cfg_content = """<?xml version="1.0" encoding="UTF-8"?>
<netconvertConfiguration xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/netconvertConfiguration.xsd">
    <input>
        <node-files value="f:\\VEHDEMO\\simulation\\webots\\worlds\\sih_mvp_traffic_net\\plain.nod.xml"/>
        <edge-files value="f:\\VEHDEMO\\simulation\\webots\\worlds\\sih_mvp_traffic_net\\plain.edg.xml"/>
        <connection-files value="f:\\VEHDEMO\\simulation\\webots\\worlds\\sih_mvp_traffic_net\\plain.con.xml"/>
        <tllogic-files value="f:\\VEHDEMO\\simulation\\webots\\worlds\\sih_mvp_traffic_net\\plain.tll.xml"/>
    </input>
    <processing>
        <geometry.min-radius.fix.railways value="false"/>
        <geometry.avoid-overlap value="false"/>
        <geometry.max-grade.fix value="false"/>
        <offset.disable-normalization value="true"/>
        <lefthand value="true"/>
    </processing>
    <junctions>
        <no-internal-links value="true"/>
        <no-turnarounds value="true"/>
        <junctions.corner-detail value="0"/>
        <junctions.limit-turn-speed value="-1.00"/>
    </junctions>
</netconvertConfiguration>
"""
with open(CFG_PATH, 'w', encoding='utf-8') as f:
    f.write(cfg_content)

# ==============================================================================
# 3. RECOMPILE SUMO.NET.XML WITH NO-INTERNAL-LINKS
# ==============================================================================
cmd = [
    r"C:\Program Files (x86)\Eclipse\Sumo\bin\netconvert.exe",
    "-c", CFG_PATH,
    "--lefthand", "true",
    "--no-internal-links", "true",
    "--no-turnarounds", "true",
    "--no-turnarounds.tls", "true",
    "--tls.ignore-internal-junction-jam", "true",
    "-o", NET_PATH
]
res = subprocess.run(cmd, capture_output=True, text=True)
print("netconvert output:\n", res.stdout, res.stderr)

# ==============================================================================
# 4. SYNCHRONIZE EXACT 28s PHASES ACROSS ALL 5 TLS
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
print("Configured clean SUMO net with no-internal-links: ZERO mid-junction stops guaranteed!")
