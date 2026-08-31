import xml.etree.ElementTree as ET
import subprocess
import random

EDG_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\plain.edg.xml"
CON_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\plain.con.xml"
CFG_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\plain.netccfg"
NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"
ROU_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.rou.xml"

# ==============================================================================
# 1. STRICT 2-LANE ROAD (1 LANE EASTBOUND + 1 LANE WESTBOUND)
# ==============================================================================
tree_edg = ET.parse(EDG_PATH)
root_edg = tree_edg.getroot()

for e in list(root_edg.findall('edge')):
    if e.get('id') in ['shortcut_east', 'shortcut_west']:
        root_edg.remove(e)

# Exactly 1 lane each direction, 3.5m width each = 7.0m total width, 100% on asphalt!
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
# 2. CONFIGURE 1-LANE CONNECTIONS IN PLAIN.CON.XML
# ==============================================================================
tree_con = ET.parse(CON_PATH)
root_con = tree_con.getroot()

for c in list(root_con.findall('connection')):
    f = c.get('from', '')
    t = c.get('to', '')
    if 'shortcut' in f or 'shortcut' in t:
        root_con.remove(c)

shortcut_conns = [
    # Junction 41 (Left End of Shortcut):
    # - Main Road 8 (from South): Left Lane 0 turns LEFT into Shortcut (Lane 0)
    {'from': '8', 'to': 'shortcut_east', 'fromLane': '0', 'toLane': '0', 'pass': 'true'},
    # - Main Road 23 (from North): Right Lane 1 turns RIGHT into Shortcut (Lane 0)
    {'from': '23', 'to': 'shortcut_east', 'fromLane': '1', 'toLane': '0'},

    # - Exiting Shortcut (shortcut_west, 1 lane):
    #   * Free-Left turn onto -23 (South)
    {'from': 'shortcut_west', 'to': '-23', 'fromLane': '0', 'toLane': '0', 'pass': 'true'},
    #   * Right turn onto -8 (North)
    {'from': 'shortcut_west', 'to': '-8', 'fromLane': '0', 'toLane': '1'},

    # Junction 43 (Right End of Shortcut):
    # - Main Road 6 (from North): Left Lane 0 turns LEFT into Shortcut (Lane 0)
    {'from': '6', 'to': 'shortcut_west', 'fromLane': '0', 'toLane': '0', 'pass': 'true'},
    # - Main Road -5 (from South): Right Lane 1 turns RIGHT into Shortcut (Lane 0)
    {'from': '-5', 'to': 'shortcut_west', 'fromLane': '1', 'toLane': '0'},

    # - Exiting Shortcut (shortcut_east, 1 lane):
    #   * Free-Left turn onto 5 (South)
    {'from': 'shortcut_east', 'to': '5', 'fromLane': '0', 'toLane': '0', 'pass': 'true'},
    #   * Right turn onto -6 (North)
    {'from': 'shortcut_east', 'to': '-6', 'fromLane': '0', 'toLane': '1'},
]

for sc in shortcut_conns:
    ET.SubElement(root_con, 'connection', sc)

tree_con.write(CON_PATH, encoding='utf-8', xml_declaration=True)

# ==============================================================================
# 3. COMPILE SUMO.NET.XML WITH NETCONVERT --LEFTHAND
# ==============================================================================
cmd = [
    r"C:\Program Files (x86)\Eclipse\Sumo\bin\netconvert.exe",
    "-c", CFG_PATH,
    "--lefthand", "true",
    "--no-turnarounds", "true",
    "--no-turnarounds.tls", "true",
    "--tls.ignore-internal-junction-jam", "true",
    "-o", NET_PATH
]
res = subprocess.run(cmd, capture_output=True, text=True)
print("netconvert output:\n", res.stdout, res.stderr)

tree_net = ET.parse(NET_PATH)
root_net = tree_net.getroot()
for lane in root_net.findall('.//lane'):
    if not lane.get('id', '').startswith(':'):
        ET.SubElement(lane, 'stopOffset', {'value': '6.0'})

for conn in root_net.findall('connection'):
    conn.set('keepClear', '1')

tree_net.write(NET_PATH, encoding='utf-8', xml_declaration=True)
print("Compiled clean 2-lane shortcut road in sumo.net.xml (100% on asphalt)!")

# ==============================================================================
# 4. GENERATE 100-VEHICLE FLEET ON STRICT 2-LANE SHORTCUT
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

def find_loops(start, curr, path, visited):
    if len(path) > 14:
        return []
    loops = []
    for nxt in adj.get(curr, []):
        if nxt == start and len(path) >= 3:
            loops.append(list(path))
        elif nxt not in visited and len(path) < 14:
            visited.add(nxt)
            path.append(nxt)
            loops.extend(find_loops(start, nxt, path, visited))
            path.pop()
            visited.remove(nxt)
    return loops

all_loops = []
for edge in list(adj.keys()):
    all_loops.extend(find_loops(edge, edge, [edge], {edge}))

print(f"Total discovered contiguous loops: {len(all_loops)}")

sc_loops = [l for l in all_loops if 'shortcut_east' in l or 'shortcut_west' in l]
curve_loops = [l for l in all_loops if any(e in l for e in ['0', '7', '6', '5', '4', '-3', '2', '-1']) and 'shortcut_east' not in l and 'shortcut_west' not in l]
arterial_loops = [l for l in all_loops if any(e in l for e in ['23', '-8', '9', '-10', '17', '12', '-18', '21', '22', '24']) and 'shortcut_east' not in l and 'shortcut_west' not in l]

print(f"Shortcut loops: {len(sc_loops)}")
print(f"Curve loops: {len(curve_loops)}")
print(f"Arterial loops: {len(arterial_loops)}")

rou_root = ET.Element('routes')

proto_vtypes = [
    {'id': 'MotorbikeSimple',             'vClass': 'motorcycle', 'guiShape': 'motorcycle', 'length': '2.2', 'width': '0.9', 'minGap': '2.0', 'maxSpeed': '18.0', 'speedGain': '2.5', 'assertive': '1.8', 'pushy': '0.8'},
    {'id': 'ScooterSimple',               'vClass': 'moped',      'guiShape': 'motorcycle', 'length': '1.9', 'width': '0.8', 'minGap': '2.0', 'maxSpeed': '14.0', 'speedGain': '2.0', 'assertive': '1.5', 'pushy': '0.7'},
    {'id': 'BusSimple',                   'vClass': 'bus',        'guiShape': 'bus',        'length': '10.5','width': '2.6', 'minGap': '3.2', 'maxSpeed': '14.0', 'speedGain': '1.0', 'assertive': '1.0', 'pushy': '0.0'},
    {'id': 'MercedesBenzSprinterSimple',  'vClass': 'delivery',   'guiShape': 'delivery',   'length': '6.0', 'width': '2.1', 'minGap': '2.6', 'maxSpeed': '15.0', 'speedGain': '1.5', 'assertive': '1.2', 'pushy': '0.2'},
    {'id': 'TeslaModel3Simple',           'vClass': 'passenger',  'guiShape': 'passenger',  'length': '4.7', 'width': '1.8', 'minGap': '2.5', 'maxSpeed': '17.0', 'speedGain': '2.0', 'assertive': '1.4', 'pushy': '0.3'},
    {'id': 'ToyotaPriusSimple',           'vClass': 'passenger',  'guiShape': 'passenger',  'length': '4.5', 'width': '1.7', 'minGap': '2.5', 'maxSpeed': '16.0', 'speedGain': '1.8', 'assertive': '1.3', 'pushy': '0.2'},
    {'id': 'CitroenCZeroSimple',          'vClass': 'passenger',  'guiShape': 'passenger',  'length': '3.5', 'width': '1.5', 'minGap': '2.2', 'maxSpeed': '15.0', 'speedGain': '1.8', 'assertive': '1.4', 'pushy': '0.4'},
    {'id': 'BmwX5Simple',                 'vClass': 'passenger',  'guiShape': 'passenger',  'length': '4.9', 'width': '2.0', 'minGap': '2.6', 'maxSpeed': '17.0', 'speedGain': '2.0', 'assertive': '1.5', 'pushy': '0.3'},
]

for vt in proto_vtypes:
    ET.SubElement(rou_root, 'vType', {
        'id': vt['id'],
        'vClass': vt['vClass'],
        'guiShape': vt['guiShape'],
        'accel': '3.0',
        'decel': '4.5',
        'sigma': '0.2',
        'length': vt['length'],
        'width': vt['width'],
        'minGap': vt['minGap'],
        'maxSpeed': vt['maxSpeed'],
        'lcStrategic': '1.0',
        'lcCooperative': '1.0',
        'lcSpeedGain': vt['speedGain'],
        'lcAssertive': vt['assertive'],
        'lcPushy': vt['pushy'],
        'lcOvertakeRight': '0.0',
        'tau': '0.6',
    })

buses = [
    ('transit_bus_1', curve_loops[0] if curve_loops else all_loops[0]),
    ('transit_bus_2', arterial_loops[0] if arterial_loops else all_loops[1]),
    ('transit_bus_3', sc_loops[0] if sc_loops else all_loops[2]),
]

N_REPEATS = 60

for b_id, b_loop in buses:
    r_id = f"route_{b_id}"
    p_edges = " ".join(b_loop * N_REPEATS)
    ET.SubElement(rou_root, 'route', {'id': r_id, 'edges': p_edges})
    ET.SubElement(rou_root, 'vehicle', {
        'id': b_id,
        'type': 'BusSimple',
        'route': r_id,
        'depart': '0.00',
        'departLane': 'best',
        'departPos': 'random',
        'departSpeed': 'max',
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

for idx, proto_type in enumerate(proto_pool):
    if idx < 50:
        loop = curve_loops[idx % len(curve_loops)] if curve_loops else all_loops[idx % len(all_loops)]
    elif idx < 85:
        loop = arterial_loops[(idx - 50) % len(arterial_loops)] if arterial_loops else all_loops[idx % len(all_loops)]
    else:
        # Shortcut Parkway (Only 12 vehicles, strictly 1 lane per direction, 100% on asphalt)
        loop = sc_loops[(idx - 85) % len(sc_loops)] if sc_loops else all_loops[idx % len(all_loops)]

    start_offset = (idx * 2) % len(loop)
    shifted = loop[start_offset:] + loop[:start_offset]
    p_edges = " ".join(shifted * N_REPEATS)

    r_id = f"route_{idx}"
    ET.SubElement(rou_root, 'route', {'id': r_id, 'edges': p_edges})

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
        'id': f"veh_{idx}",
        'type': proto_type,
        'route': r_id,
        'depart': '0.00',
        'departLane': 'best',
        'departPos': 'random',
        'departSpeed': 'max',
        'color': col
    })

rou_tree = ET.ElementTree(rou_root)
rou_tree.write(ROU_PATH, encoding='utf-8', xml_declaration=True)
print(f"Generated 100-vehicle fleet with strictly 2-lane shortcut road (100% on asphalt) in {ROU_PATH}")
