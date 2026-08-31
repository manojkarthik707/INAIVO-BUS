import xml.etree.ElementTree as ET
import subprocess
import random

EDG_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\plain.edg.xml"
CON_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\plain.con.xml"
TLL_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\plain.tll.xml"
CFG_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\plain.netccfg"
NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"
ROU_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.rou.xml"

# ==============================================================================
# 1. PLAIN.EDG.XML: STRICT 2-LANE SHORTCUT (1 Lane East + 1 Lane West)
# ==============================================================================
tree_edg = ET.parse(EDG_PATH)
root_edg = tree_edg.getroot()

for e in list(root_edg.findall('edge')):
    if e.get('id') in ['shortcut_east', 'shortcut_west']:
        root_edg.remove(e)

ET.SubElement(root_edg, 'edge', {
    'id': 'shortcut_east',
    'from': '41',
    'to': '43',
    'priority': '-1',
    'numLanes': '1',
    'speed': '13.90',
    'width': '3.50'
})
ET.SubElement(root_edg, 'edge', {
    'id': 'shortcut_west',
    'from': '43',
    'to': '41',
    'priority': '-1',
    'numLanes': '1',
    'speed': '13.90',
    'width': '3.50'
})
tree_edg.write(EDG_PATH, encoding='utf-8', xml_declaration=True)

# ==============================================================================
# 2. PLAIN.CON.XML: CLEAN ZERO-U-TURN CONNECTIONS
# ==============================================================================
tree_con = ET.parse(CON_PATH)
root_con = tree_con.getroot()

for c in list(root_con.findall('connection')):
    f = c.get('from', '')
    t = c.get('to', '')
    if f == f"-{t}" or t == f"-{f}" or 'shortcut' in f or 'shortcut' in t:
        root_con.remove(c)

shortcut_conns = [
    # Junction 41 (Left End)
    {'from': '8', 'to': 'shortcut_east', 'fromLane': '0', 'toLane': '0'},
    {'from': '23', 'to': 'shortcut_east', 'fromLane': '0', 'toLane': '0'},
    {'from': 'shortcut_west', 'to': '-8', 'fromLane': '0', 'toLane': '0'},
    {'from': 'shortcut_west', 'to': '-23', 'fromLane': '0', 'toLane': '0'},

    # Junction 43 (Right End)
    {'from': 'shortcut_east', 'to': '-6', 'fromLane': '0', 'toLane': '0'},
    {'from': 'shortcut_east', 'to': '5', 'fromLane': '0', 'toLane': '0'},
    {'from': '-5', 'to': 'shortcut_west', 'fromLane': '0', 'toLane': '0'},
    {'from': '6', 'to': 'shortcut_west', 'fromLane': '0', 'toLane': '0'},
]

for sc in shortcut_conns:
    ET.SubElement(root_con, 'connection', sc)

tree_con.write(CON_PATH, encoding='utf-8', xml_declaration=True)

# ==============================================================================
# 3. PLAIN.TLL.XML: EXACT 16-LINK 4-PHASE CYCLE
# ==============================================================================
# 4 stages * (5s Green + 2s Yellow) = 28s cycle
tl_phases = [
    {'duration': '5', 'state': 'GGGGgrrrgrrrgrrr'},
    {'duration': '2', 'state': 'yyyygrrrgrrrgrrr'},
    {'duration': '5', 'state': 'grrrGGGGgrrrgrrr'},
    {'duration': '2', 'state': 'grrryyyygrrrgrrr'},
    {'duration': '5', 'state': 'grrrgrrrGGGGgrrr'},
    {'duration': '2', 'state': 'grrrgrrryyyygrrr'},
    {'duration': '5', 'state': 'grrrgrrrgrrrGGGG'},
    {'duration': '2', 'state': 'grrrgrrrgrrryyyy'},
]

root_tll = ET.Element('tlLogics', {'version': '1.20'})
for jid in ['25', '26', '27']:
    tl = ET.SubElement(root_tll, 'tlLogic', {'id': jid, 'type': 'static', 'programID': '0', 'offset': '0'})
    for p in tl_phases:
        ET.SubElement(tl, 'phase', p)

tree_tll = ET.ElementTree(root_tll)
tree_tll.write(TLL_PATH, encoding='utf-8', xml_declaration=True)

# ==============================================================================
# 4. COMPILE SUMO.NET.XML VIA NETCONVERT
# ==============================================================================
cmd = [
    r"C:\Program Files (x86)\Eclipse\Sumo\bin\netconvert.exe",
    "-c", CFG_PATH,
    "--no-turnarounds", "true",
    "--no-turnarounds.tls", "true",
    "--tls.ignore-internal-junction-jam", "true",
    "-o", NET_PATH
]
res = subprocess.run(cmd, capture_output=True, text=True)
print("netconvert output:\n", res.stdout, res.stderr)

# Patch stopOffsets into sumo.net.xml
tree_net = ET.parse(NET_PATH)
root_net = tree_net.getroot()
for lane in root_net.findall('.//lane'):
    if not lane.get('id', '').startswith(':'):
        ET.SubElement(lane, 'stopOffset', {'value': '6.0'})

# Remove any residual U-turns
for conn in list(root_net.findall('connection')):
    if conn.get('dir') in ['t', 'T']:
        root_net.remove(conn)

tree_net.write(NET_PATH, encoding='utf-8', xml_declaration=True)
print("Compiled flawless sumo.net.xml!")

# ==============================================================================
# 5. GENERATE 100-VEHICLE FLEET WITH EXACT PROTO BINDINGS & ZERO U-TURNS
# ==============================================================================
adj = {}
for conn in root_net.findall('connection'):
    f = conn.get('from')
    t = conn.get('to')
    dir_ = conn.get('dir')
    if dir_ not in ['t', 'T'] and f != f"-{t}" and t != f"-{f}":
        if f not in adj:
            adj[f] = set()
        adj[f].add(t)

all_circuits = []

def find_cycles(start_edge, current_edge, path, visited):
    if len(path) > 12:
        return
    for nxt in adj.get(current_edge, []):
        if nxt == start_edge and len(path) >= 4:
            all_circuits.append(list(path))
        elif nxt not in visited and len(path) < 12:
            visited.add(nxt)
            path.append(nxt)
            find_cycles(start_edge, nxt, path, visited)
            path.pop()
            visited.remove(nxt)

for edge in list(adj.keys()):
    find_cycles(edge, edge, [edge], {edge})

shortcut_circuits = [c for c in all_circuits if 'shortcut_east' in c or 'shortcut_west' in c]
standard_circuits = [c for c in all_circuits if 'shortcut_east' not in c and 'shortcut_west' not in c]

print(f"Discovered {len(all_circuits)} circuits (Shortcut: {len(shortcut_circuits)}, Arterial: {len(standard_circuits)})")

rou_root = ET.Element('routes')

proto_vtypes = [
    # 🏍️ Motorbikes
    {'id': 'MotorbikeSimple',             'vClass': 'motorcycle', 'guiShape': 'motorcycle', 'length': '2.2', 'width': '0.9', 'minGap': '2.5', 'maxSpeed': '16.0'},
    # 🛵 Scooters
    {'id': 'ScooterSimple',               'vClass': 'moped',      'guiShape': 'motorcycle', 'length': '1.9', 'width': '0.8', 'minGap': '2.5', 'maxSpeed': '13.0'},
    # 🚌 Transit Buses
    {'id': 'BusSimple',                   'vClass': 'bus',        'guiShape': 'bus',        'length': '10.5','width': '2.6', 'minGap': '3.2', 'maxSpeed': '14.0'},
    # 🚐 Delivery Sprinters
    {'id': 'MercedesBenzSprinterSimple',  'vClass': 'delivery',   'guiShape': 'delivery',   'length': '6.0', 'width': '2.1', 'minGap': '2.8', 'maxSpeed': '15.0'},
    # 🚗 Passenger Cars
    {'id': 'TeslaModel3Simple',           'vClass': 'passenger',  'guiShape': 'passenger',  'length': '4.7', 'width': '1.8', 'minGap': '2.8', 'maxSpeed': '16.0'},
    {'id': 'ToyotaPriusSimple',           'vClass': 'passenger',  'guiShape': 'passenger',  'length': '4.5', 'width': '1.7', 'minGap': '2.8', 'maxSpeed': '16.0'},
    {'id': 'CitroenCZeroSimple',          'vClass': 'passenger',  'guiShape': 'passenger',  'length': '3.5', 'width': '1.5', 'minGap': '2.5', 'maxSpeed': '15.0'},
    {'id': 'BmwX5Simple',                 'vClass': 'passenger',  'guiShape': 'passenger',  'length': '4.9', 'width': '2.0', 'minGap': '2.8', 'maxSpeed': '16.0'},
]

for vt in proto_vtypes:
    ET.SubElement(rou_root, 'vType', {
        'id': vt['id'],
        'vClass': vt['vClass'],
        'guiShape': vt['guiShape'],
        'accel': '2.8',
        'decel': '4.5',
        'sigma': '0.2',
        'length': vt['length'],
        'width': vt['width'],
        'minGap': vt['minGap'],
        'maxSpeed': vt['maxSpeed'],
        'lcStrategic': '1.0',
        'lcCooperative': '1.0',
        'lcPushy': '0.0',
        'lcAssertive': '1.0',
        'tau': '0.65',
    })

# 3 Buses
bus_routes = [
    standard_circuits[0],
    shortcut_circuits[0],
    standard_circuits[1 % len(standard_circuits)],
]

for idx, b_circ in enumerate(bus_routes):
    r_id = f"route_bus_{idx+1}"
    ET.SubElement(rou_root, 'route', {'id': r_id, 'edges': " ".join(b_circ)})
    ET.SubElement(rou_root, 'vehicle', {
        'id': f"BUS_0{idx+1}",
        'type': 'BusSimple',
        'route': r_id,
        'depart': '0.00',
        'departLane': 'best',
        'departPos': 'random',
        'departSpeed': 'max',
        'reroute': 'true',
        'color': '1.0,0.7,0.1'
    })

proto_pool = (
    ['MotorbikeSimple'] * 25 +
    ['ScooterSimple'] * 20 +
    ['TeslaModel3Simple'] * 12 +
    ['ToyotaPriusSimple'] * 12 +
    ['CitroenCZeroSimple'] * 11 +
    ['BmwX5Simple'] * 10 +
    ['MercedesBenzSprinterSimple'] * 7
)

random.seed(42)
random.shuffle(proto_pool)

circuits_by_start = {}
for c in shortcut_circuits + standard_circuits:
    s = c[0]
    if s not in circuits_by_start:
        circuits_by_start[s] = []
    circuits_by_start[s].append(c)

start_edge_list = list(circuits_by_start.keys())

for idx, proto_type in enumerate(proto_pool):
    start_edge = start_edge_list[idx % len(start_edge_list)]
    avail = circuits_by_start[start_edge]
    circ = avail[idx % len(avail)]

    r_id = f"route_{idx}"
    ET.SubElement(rou_root, 'route', {'id': r_id, 'edges': " ".join(circ)})

    if 'Motorbike' in proto_type:
        colors = ['0.9,0.1,0.1', '0.1,0.8,0.8', '0.9,0.8,0.1', '0.5,0.1,0.8', '0.1,0.2,0.9']
    elif 'Scooter' in proto_type:
        colors = ['0.2,0.8,0.3', '0.9,0.5,0.1', '0.8,0.1,0.5', '0.1,0.7,0.9', '0.7,0.7,0.1']
    elif 'Sprinter' in proto_type:
        colors = ['0.95,0.95,0.95', '0.8,0.7,0.2', '0.2,0.3,0.5']
    else:
        colors = ['0.1,0.5,0.9', '0.85,0.15,0.15', '0.92,0.92,0.92', '0.12,0.12,0.12', '0.2,0.7,0.4', '0.95,0.65,0.1']

    col = random.choice(colors)

    ET.SubElement(rou_root, 'vehicle', {
        'id': str(idx),
        'type': proto_type,
        'route': r_id,
        'depart': '0.00',
        'departLane': 'random',
        'departPos': 'random',
        'departSpeed': 'max',
        'reroute': 'true',
        'color': col
    })

rou_tree = ET.ElementTree(rou_root)
rou_tree.write(ROU_PATH, encoding='utf-8', xml_declaration=True)
print(f"Generated 100-vehicle fleet with 45 motorbikes/scooters and ZERO U-turns in {ROU_PATH}")
