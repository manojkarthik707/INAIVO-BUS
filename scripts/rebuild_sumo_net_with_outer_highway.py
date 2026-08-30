import xml.etree.ElementTree as ET
import subprocess
import os

net_dir = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net"

# 1. Export plain files using netconvert
subprocess.run([
    r"C:\Program Files (x86)\Eclipse\Sumo\bin\netconvert.exe",
    "-s", os.path.join(net_dir, "sumo.net.xml"),
    "--plain-output-prefix", os.path.join(net_dir, "plain")
], check=True)

# 2. Modify plain.edg.xml
edg_path = os.path.join(net_dir, "plain.edg.xml")
tree_edg = ET.parse(edg_path)
root_edg = tree_edg.getroot()

# Check if outer_west already exists
if not any(e.get('id') == 'outer_west' for e in root_edg.findall('edge')):
    edge_ow = ET.Element('edge', {
        'id': 'outer_west',
        'from': 'Custom22',
        'to': 'Custom21',
        'priority': '-1',
        'numLanes': '2',
        'speed': '13.90',
        'width': '5.38',
        'shape': '39.50,418.51 -1.00,378.01 -1.00,40.50 0.00,0.00'
    })
    edge_now = ET.Element('edge', {
        'id': '-outer_west',
        'from': 'Custom21',
        'to': 'Custom22',
        'priority': '-1',
        'numLanes': '2',
        'speed': '13.90',
        'width': '5.38',
        'shape': '0.00,0.00 -1.00,40.50 -1.00,378.01 39.50,418.51'
    })
    root_edg.append(edge_ow)
    root_edg.append(edge_now)
    tree_edg.write(edg_path, encoding='utf-8', xml_declaration=True)
    print("Added outer_west edges to plain.edg.xml")

# 3. Modify plain.con.xml
con_path = os.path.join(net_dir, "plain.con.xml")
tree_con = ET.parse(con_path)
root_con = tree_con.getroot()

# Add connections for outer_west
new_conns = [
    ('15', 'outer_west', '0', '0'),
    ('15', 'outer_west', '1', '1'),
    ('outer_west', '-13', '0', '0'),
    ('outer_west', '-13', '1', '1'),
    ('13', '-outer_west', '0', '0'),
    ('13', '-outer_west', '1', '1'),
    ('-outer_west', '-15', '0', '0'),
    ('-outer_west', '-15', '1', '1')
]

for f, t, fl, tl in new_conns:
    root_con.append(ET.Element('connection', {'from': f, 'to': t, 'fromLane': fl, 'toLane': tl}))

tree_con.write(con_path, encoding='utf-8', xml_declaration=True)
print("Added outer highway connections to plain.con.xml")

# 4. Rebuild sumo.net.xml using netconvert
subprocess.run([
    r"C:\Program Files (x86)\Eclipse\Sumo\bin\netconvert.exe",
    "--node-files", os.path.join(net_dir, "plain.nod.xml"),
    "--edge-files", os.path.join(net_dir, "plain.edg.xml"),
    "--connection-files", os.path.join(net_dir, "plain.con.xml"),
    "--tllogic-files", os.path.join(net_dir, "plain.tll.xml"),
    "--offset.disable-normalization", "true",
    "--no-turnarounds", "true",
    "-o", os.path.join(net_dir, "sumo.net.xml")
], check=True)

print("Successfully compiled pristine new sumo.net.xml with outer perimeter highways!")
