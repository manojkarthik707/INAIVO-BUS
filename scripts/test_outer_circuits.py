import xml.etree.ElementTree as ET

tree = ET.parse(r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml")
root = tree.getroot()

clean_connections = {}
for conn in root.findall('connection'):
    f = conn.get('from')
    t = conn.get('to')
    d = conn.get('dir')
    if f and t and not f.startswith(':') and not t.startswith(':'):
        clean_connections.setdefault(f, set()).add(t)

print("Connections from outer edges:")
outer_edges = ['13', '-13', '15', '-15', '16', '-16', '18', '-18', '21', '-21', '22', '-22', '19', '-19', '11', '-11', '14', '-14', '20', '-20']
for oe in outer_edges:
    print(f"Edge {oe} -> {clean_connections.get(oe, set())}")
