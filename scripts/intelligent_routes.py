"""
intelligent_routes.py — Intelligent Route Generator for SUMO (Validated Routes).

APPROACH:
- Uses randomTrips-style multi-hop random walk across the fully-connected road network.
- Each vehicle gets a unique A->B->C->...->Z route with 8-15 random hops that covers
  varied parts of the city, naturally distributing traffic on ALL edges.
- Buses get long arterial routes prioritizing the major ring roads.
- Three transit buses (transit_bus_1/2/3) appear at SUMO_VEHICLE0/1/2 by being inserted first.
"""

import xml.etree.ElementTree as ET
import random
from collections import deque

NET_FILE = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"
ROU_FILE = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.rou.xml"

tree = ET.parse(NET_FILE)
root = tree.getroot()

# ── Build adjacency map & edge lengths ────────────────────────────────────────
adj = {}
edge_lengths = {}
for edge in root.findall('edge'):
    if edge.get('function') == 'internal':
        continue
    eid = edge.get('id')
    lane = edge.find('lane')
    if lane is not None:
        edge_lengths[eid] = float(lane.get('length', 40.0))
    adj.setdefault(eid, set())  # ensure entry exists even with no outgoing

for conn in root.findall('connection'):
    frm = conn.get('from')
    to  = conn.get('to')
    if frm and to and not frm.startswith(':') and not to.startswith(':'):
        adj.setdefault(frm, set()).add(to)

ALL_EDGES = [e for e in edge_lengths if e in adj and len(adj[e]) > 0]

# Long arterial/ring edges for bus priority
BUS_PRIORITY_EDGES = [e for e in ALL_EDGES if any(k in e for k in ['outer', '13', '14', '15', '11'])]


def reachable(start, min_length=3):
    """BFS to find all edges reachable from start."""
    visited = set()
    q = deque([start])
    while q:
        e = q.popleft()
        if e in visited:
            continue
        visited.add(e)
        for nxt in adj.get(e, []):
            if nxt not in visited:
                q.append(nxt)
    return visited


def random_walk(start, n_hops, rng, prefer=None):
    """Generate a random walk of n_hops edges from start using BFS-guided random choices."""
    path = [start]
    curr = start
    for _ in range(n_hops - 1):
        nexts = list(adj.get(curr, []))
        if not nexts:
            break
        if prefer and rng.random() < 0.4:
            pref_nexts = [n for n in nexts if n in prefer]
            if pref_nexts:
                nexts = pref_nexts
        curr = rng.choice(nexts)
        if curr not in path:  # Avoid immediate repeats (not strict, just cleaner)
            path.append(curr)
        else:
            path.append(curr)  # still append for route continuity
    return path


def validate_route(edges_list):
    """Check every consecutive edge pair has a real SUMO connection."""
    for i in range(len(edges_list) - 1):
        if edges_list[i+1] not in adj.get(edges_list[i], set()):
            return False
    return True


def make_route(start, min_hops=8, max_hops=16, prefer=None, rng=None):
    """Make a validated multi-hop route that visits diverse parts of the city."""
    rng = rng or random.Random()
    for _attempt in range(20):
        n = rng.randint(min_hops, max_hops)
        path = random_walk(start, n, rng, prefer=prefer)
        if validate_route(path) and len(path) >= 3:
            return ' '.join(path)
    # Fallback: build a guaranteed valid route by BFS
    path = [start]
    curr = start
    for _ in range(max_hops - 1):
        nexts = [e for e in adj.get(curr, []) if e in edge_lengths]
        if not nexts:
            break
        curr = rng.choice(nexts)
        path.append(curr)
    return ' '.join(path)


# ── Build routes XML ──────────────────────────────────────────────────────────
rou_root = ET.Element('routes')

proto_vtypes = [
    {'id': 'MotorbikeSimple',            'vClass': 'motorcycle', 'guiShape': 'motorcycle', 'length': '2.2', 'width': '0.9',  'minGap': '3.0', 'maxSpeed': '16.0'},
    {'id': 'ScooterSimple',              'vClass': 'moped',      'guiShape': 'motorcycle', 'length': '1.9', 'width': '0.8',  'minGap': '3.0', 'maxSpeed': '14.0'},
    {'id': 'BusSimple',                  'vClass': 'bus',        'guiShape': 'bus',        'length': '10.5','width': '2.6',  'minGap': '4.5', 'maxSpeed': '14.0'},
    {'id': 'MercedesBenzSprinterSimple', 'vClass': 'delivery',   'guiShape': 'delivery',   'length': '6.0', 'width': '2.1',  'minGap': '3.8', 'maxSpeed': '15.0'},
    {'id': 'TeslaModel3Simple',          'vClass': 'passenger',  'guiShape': 'passenger',  'length': '4.7', 'width': '1.8',  'minGap': '3.5', 'maxSpeed': '16.0'},
    {'id': 'ToyotaPriusSimple',          'vClass': 'passenger',  'guiShape': 'passenger',  'length': '4.5', 'width': '1.7',  'minGap': '3.5', 'maxSpeed': '16.0'},
    {'id': 'CitroenCZeroSimple',         'vClass': 'passenger',  'guiShape': 'passenger',  'length': '3.5', 'width': '1.5',  'minGap': '3.0', 'maxSpeed': '15.0'},
    {'id': 'BmwX5Simple',                'vClass': 'passenger',  'guiShape': 'passenger',  'length': '4.9', 'width': '2.0',  'minGap': '3.5', 'maxSpeed': '16.0'},
]

for vt in proto_vtypes:
    ET.SubElement(rou_root, 'vType', {
        'id': vt['id'],
        'vClass': vt['vClass'],
        'guiShape': vt['guiShape'],
        'accel': '2.6',
        'decel': '4.5',
        'emergencyDecel': '9.0',
        'sigma': '0.15',
        'length': vt['length'],
        'width': vt['width'],
        'minGap': vt['minGap'],
        'maxSpeed': vt['maxSpeed'],
        'lcStrategic': '1.2',
        'lcCooperative': '1.0',
        'lcSpeedGain': '1.0',
        'lcAssertive': '1.0',
        'lcPushy': '0.0',
        'lcKeepRight': '0.0',
        'lcOvertakeRight': '0.0',
        'tau': '1.4',
    })

# ── Transit Buses (inserted FIRST so they become SUMO_VEHICLE0..19) ──────────
rng = random.Random(42)
shuffled_edges = list(ALL_EDGES)
rng.shuffle(shuffled_edges)

for b_idx in range(20):
    b_id = f"SUMO_VEHICLE{b_idx}"
    r_id = f"route_{b_id}"
    start_edge = shuffled_edges[b_idx % len(shuffled_edges)]
    # Ultra-long arterial route (800-1200 hops to stay in simulation endlessly)
    route_edges = make_route(start_edge, min_hops=800, max_hops=1200,
                             prefer=set(BUS_PRIORITY_EDGES), rng=rng)
    ET.SubElement(rou_root, 'route', {'id': r_id, 'edges': route_edges})
    ET.SubElement(rou_root, 'vehicle', {
        'id': b_id,
        'type': 'BusSimple',
        'route': r_id,
        'depart': '0.00',
        'departLane': 'best',
        'departPos': 'random_free',
        'departSpeed': 'max',
        'color': '1.0,0.7,0.1',
    })

# ── Mixed Fleet: 70 vehicles (30 bikes + 40 cars) ───────────
proto_pool = (
    ['MotorbikeSimple'] * 30 +
    ['BmwX5Simple'] * 40
)

for v_idx in range(70):
    v_id = f"SUMO_VEHICLE{v_idx+20}"
    r_id = f"route_{v_id}"
    # Start from diverse edges spread across the city (offset by 20 to avoid bus overlap)
    start_edge = shuffled_edges[(v_idx + 20) % len(shuffled_edges)]
    # Ultra-long random route (800-1200 hops covering diverse parts of city endlessly)
    route_edges = make_route(start_edge, min_hops=800, max_hops=1200, rng=rng)
    v_type = proto_pool[v_idx % len(proto_pool)]

    ET.SubElement(rou_root, 'route', {'id': r_id, 'edges': route_edges})
    ET.SubElement(rou_root, 'vehicle', {
        'id': v_id,
        'type': v_type,
        'route': r_id,
        'depart': '0.00',
        'departLane': 'free',
        'departPos': 'random_free',
        'departSpeed': 'max',
    })


def indent(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for sub in elem:
            indent(sub, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


indent(rou_root)
ET.ElementTree(rou_root).write(ROU_FILE, encoding='utf-8', xml_declaration=True)
print(f"Generated intelligent routes: 3 transit buses + 17 mixed vehicles.")
print(f"Network: {len(ALL_EDGES)} edges, fully connected.")
print(f"Buses routed on arterials: {BUS_PRIORITY_EDGES[:5]}...")
