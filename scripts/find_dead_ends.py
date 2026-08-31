import xml.etree.ElementTree as ET

NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"
tree = ET.parse(NET_PATH)
root = tree.getroot()

all_edges = set()
for e in root.findall('edge'):
    eid = e.get('id', '')
    if not eid.startswith(':'):
        all_edges.add(eid)

from_edges = set()
to_edges = set()
for c in root.findall('connection'):
    f = c.get('from', '')
    t = c.get('to', '')
    if f and not f.startswith(':'):
        from_edges.add(f)
    if t and not t.startswith(':'):
        to_edges.add(t)

dead_ends = all_edges - from_edges
unreachable = all_edges - to_edges

print(f"Total edges: {len(all_edges)}")
print(f"Dead-end edges (vehicles vanish here!): {dead_ends}")
print(f"Unreachable edges: {unreachable}")
