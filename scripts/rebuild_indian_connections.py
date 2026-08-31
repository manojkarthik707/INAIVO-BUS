import xml.etree.ElementTree as ET
import os
import subprocess

CON_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\plain.con.xml"
NETCCFG_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\plain.netccfg"
NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"

# We will read sumo.net.xml to inspect the exact relative turning angle/direction for each (from_edge, to_edge) pair
tree = ET.parse(NET_PATH)
root = tree.getroot()

# Map each (from, to) connection to its spatial turn direction
edge_directions = {}
for conn in root.findall('connection'):
    f = conn.get('from', '')
    t = conn.get('to', '')
    d = conn.get('dir', '')
    if not f.startswith(':') and not t.startswith(':'):
        edge_directions[(f, t)] = d

print(f"Mapped {len(edge_directions)} edge-to-edge directional pairs.")

# Now rebuild plain.con.xml with the STRICT Indian road system:
# Left lane (fromLane="0"): LEFT (dir="l") and STRAIGHT (dir="s") ONLY.
# Right lane (fromLane="1"): RIGHT (dir="r"), STRAIGHT (dir="s"), and U-TURN (dir="t"/"T") ONLY.

con_root = ET.Element('connections')
con_root.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
con_root.set('version', '1.20')
con_root.set('xsi:noNamespaceSchemaLocation', 'http://sumo.dlr.de/xsd/connections_file.xsd')

# Group by from_edge
edges_from = {}
for (f, t), d in edge_directions.items():
    edges_from.setdefault(f, []).append((t, d))

for f, targets in sorted(edges_from.items()):
    for t, d in targets:
        # Left Turn -> fromLane 0 to toLane 0
        if d in ['l', 'L', 'left']:
            c = ET.SubElement(con_root, 'connection')
            c.set('from', f)
            c.set('to', t)
            c.set('fromLane', '0')
            c.set('toLane', '0')
        # Right Turn -> fromLane 1 to toLane 1
        elif d in ['r', 'R', 'right']:
            c = ET.SubElement(con_root, 'connection')
            c.set('from', f)
            c.set('to', t)
            c.set('fromLane', '1')
            c.set('toLane', '1')
        # U-Turn -> fromLane 1 to toLane 1
        elif d in ['t', 'T', 'turn']:
            c = ET.SubElement(con_root, 'connection')
            c.set('from', f)
            c.set('to', t)
            c.set('fromLane', '1')
            c.set('toLane', '1')
        # Straight -> fromLane 0 -> toLane 0 AND fromLane 1 -> toLane 1
        elif d in ['s', 'S', 'straight']:
            c0 = ET.SubElement(con_root, 'connection')
            c0.set('from', f)
            c0.set('to', t)
            c0.set('fromLane', '0')
            c0.set('toLane', '0')
            
            c1 = ET.SubElement(con_root, 'connection')
            c1.set('from', f)
            c1.set('to', t)
            c1.set('fromLane', '1')
            c1.set('toLane', '1')

# Format XML with indentation
tree_out = ET.ElementTree(con_root)
ET.indent(tree_out, space="    ")
tree_out.write(CON_PATH, encoding='utf-8', xml_declaration=True)
print(f"Rebuilt {CON_PATH} with strict Indian Left-Hand Traffic lane rules.")

# Run netconvert to generate the new sumo.net.xml
netconvert_exe = r"C:\Program Files (x86)\Eclipse\Sumo\bin\netconvert.exe"
cmd = [netconvert_exe, "-c", NETCCFG_PATH, "--lefthand", "true", "-o", NET_PATH]
res = subprocess.run(cmd, capture_output=True, text=True)
print("netconvert output:\n", res.stdout, res.stderr)
