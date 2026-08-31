import xml.etree.ElementTree as ET

NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"
tree = ET.parse(NET_PATH)
root = tree.getroot()

for j in root.findall('junction'):
    if j.get('id') in ['41', '43']:
        j.set('type', 'priority')
        j.set('intLanes', '')
        for r in list(j.findall('request')):
            j.remove(r)

# Also remove connection elements that have via=":41_..." or via=":43_..."
for conn in list(root.findall('connection')):
    f = conn.get('from', '')
    via = conn.get('via', '')
    if ':41_' in f or ':43_' in f or ':41_' in via or ':43_' in via:
        root.remove(conn)

tree.write(NET_PATH, encoding='utf-8', xml_declaration=True)
print(f"Cleaned internal lanes for 41 and 43 in {NET_PATH}")
