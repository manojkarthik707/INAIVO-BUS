import xml.etree.ElementTree as ET

NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"
tree = ET.parse(NET_PATH)
root = tree.getroot()

print("=== EDGES IN SUMO NET ===")
edge_ids = [e.get('id') for e in root.findall('edge')]
print("Total edges:", len(edge_ids))
print("Shortcut edges present?:", 'shortcut_east' in edge_ids, 'shortcut_west' in edge_ids)

print("\n=== CONNECTIONS AT JUNCTION 41 & 43 ===")
for conn in root.findall('connection'):
    f = conn.get('from', '')
    t = conn.get('to', '')
    if 'shortcut' in f or 'shortcut' in t or conn.get('tl') in ['41', '43']:
        print(f"Conn from {f}_{conn.get('fromLane')} -> to {t}_{conn.get('toLane')} dir={conn.get('dir')} tl={conn.get('tl')} link={conn.get('linkIndex')}")
