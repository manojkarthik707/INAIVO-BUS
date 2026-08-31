import xml.etree.ElementTree as ET

NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"

tree = ET.parse(NET_PATH)
root = tree.getroot()

# 1. Enforce stopOffset=4.0 on all physical approach lanes so stop line is strictly respected
stopoffset_count = 0
for edge in root.findall('edge'):
    if not edge.get('id', '').startswith(':'):
        for lane in edge.findall('lane'):
            # Check if stopOffset already exists
            so = lane.find('stopOffset')
            if so is None:
                so = ET.SubElement(lane, 'stopOffset')
                so.set('value', '4.0')
                stopoffset_count += 1
            else:
                so.set('value', '4.0')

# 2. Enforce keepClear="1" on all junction connections (Yellow Box Junction Rule: NEVER enter intersection unless exit is clear)
kc_count = 0
for conn in root.findall('connection'):
    conn.set('keepClear', '1')
    kc_count += 1

tree.write(NET_PATH, encoding='utf-8', xml_declaration=True)
print(f"Added stopOffset=4.0 to {stopoffset_count} lanes and keepClear=1 to {kc_count} connections.")
