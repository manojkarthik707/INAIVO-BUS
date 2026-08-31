import xml.etree.ElementTree as ET

NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"
tree = ET.parse(NET_PATH)
root = tree.getroot()

# Remove tlLogic 41 and 43 from sumo.net.xml
for tl in list(root.findall('tlLogic')):
    if tl.get('id') in ['41', '43']:
        root.remove(tl)

# Set junction 41 and 43 type to priority and remove fixed request table so SUMO computes them dynamically
for j in root.findall('junction'):
    jid = j.get('id')
    if jid in ['41', '43']:
        j.set('type', 'priority')
        for req in list(j.findall('request')):
            j.remove(req)

# Remove tl and linkIndex attributes from connections at 41 and 43
for conn in root.findall('connection'):
    if conn.get('tl') in ['41', '43']:
        del conn.attrib['tl']
        if 'linkIndex' in conn.attrib:
            del conn.attrib['linkIndex']

tree.write(NET_PATH, encoding='utf-8', xml_declaration=True)
print(f"Configured Junction 41 & 43 as dynamic priority junctions in {NET_PATH}")
