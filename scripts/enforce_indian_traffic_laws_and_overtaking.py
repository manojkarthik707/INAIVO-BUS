import xml.etree.ElementTree as ET
import subprocess
import random

EDG_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\plain.edg.xml"
CON_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\plain.con.xml"
CFG_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\plain.netccfg"
TLL_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\plain.tll.xml"
NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"
ROU_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.rou.xml"

# ==============================================================================
# 1. NETCCFG: INDIAN LEFTHAND DRIVING
# ==============================================================================
cfg_content = """<?xml version="1.0" encoding="UTF-8"?>
<netconvertConfiguration xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/netconvertConfiguration.xsd">
    <input>
        <node-files value="f:\\VEHDEMO\\simulation\\webots\\worlds\\sih_mvp_traffic_net\\plain.nod.xml"/>
        <edge-files value="f:\\VEHDEMO\\simulation\\webots\\worlds\\sih_mvp_traffic_net\\plain.edg.xml"/>
        <connection-files value="f:\\VEHDEMO\\simulation\\webots\\worlds\\sih_mvp_traffic_net\\plain.con.xml"/>
        <tllogic-files value="f:\\VEHDEMO\\simulation\\webots\\worlds\\sih_mvp_traffic_net\\plain.tll.xml"/>
    </input>
    <processing>
        <geometry.min-radius.fix.railways value="false"/>
        <geometry.avoid-overlap value="false"/>
        <geometry.max-grade.fix value="false"/>
        <offset.disable-normalization value="true"/>
        <lefthand value="true"/>
    </processing>
    <junctions>
        <no-turnarounds value="true"/>
        <junctions.corner-detail value="0"/>
        <junctions.limit-turn-speed value="-1.00"/>
    </junctions>
</netconvertConfiguration>
"""
with open(CFG_PATH, 'w', encoding='utf-8') as f:
    f.write(cfg_content)

# ==============================================================================
# 2. PLAIN.CON.XML: STRICT LANE PRIORITY (LANE 0 LEFT TURNS, LANE 1 RIGHT TURNS)
# ==============================================================================
res_con = subprocess.run(["git", "show", "V0:simulation/webots/worlds/sih_mvp_traffic_net/plain.con.xml"], capture_output=True, text=True)
con_tree = ET.fromstring(res_con.stdout)

# Purge U-turns and old shortcut connections
for c in list(con_tree.findall('connection')):
    f = c.get('from', '')
    t = c.get('to', '')
    if f == f"-{t}" or t == f"-{f}" or 'shortcut' in f or 'shortcut' in t:
        con_tree.remove(c)

# Indian LHD Lane Discipline:
# - Left-turning vehicles ALWAYS use Lane 0 (outer curb lane)
# - Right-turning vehicles ALWAYS use Lane 1 (inner median lane)
# - Free-Left turns have pass="true" (yield & turn continuously)
shortcut_conns = [
    # Junction 41 (Left End of Shortcut):
    # - 8 (coming from South): Lane 0 (outer left) Free-Left turns into shortcut_east (lane 0)
    {'from': '8', 'to': 'shortcut_east', 'fromLane': '0', 'toLane': '0', 'pass': 'true'},
    # - 23 (coming from North): Lane 1 (inner right) turns right into shortcut_east (lane 0)
    {'from': '23', 'to': 'shortcut_east', 'fromLane': '1', 'toLane': '0'},
    # - shortcut_west (coming from East): Lane 0 Free-Left turns into -23 (lane 0), Lane 0 turns right into -8 (lane 1)
    {'from': 'shortcut_west', 'to': '-23', 'fromLane': '0', 'toLane': '0', 'pass': 'true'},
    {'from': 'shortcut_west', 'to': '-8', 'fromLane': '0', 'toLane': '1'},

    # Junction 43 (Right End of Shortcut):
    # - 6 (coming from North): Lane 0 (outer left) Free-Left turns into shortcut_west (lane 0)
    {'from': '6', 'to': 'shortcut_west', 'fromLane': '0', 'toLane': '0', 'pass': 'true'},
    # - -5 (coming from South): Lane 1 (inner right) turns right into shortcut_west (lane 0)
    {'from': '-5', 'to': 'shortcut_west', 'fromLane': '1', 'toLane': '0'},
    # - shortcut_east (coming from West): Lane 0 Free-Left turns into 5 (lane 0), Lane 0 turns right into -6 (lane 1)
    {'from': 'shortcut_east', 'to': '5', 'fromLane': '0', 'toLane': '0', 'pass': 'true'},
    {'from': 'shortcut_east', 'to': '-6', 'fromLane': '0', 'toLane': '1'},
]

for sc in shortcut_conns:
    ET.SubElement(con_tree, 'connection', sc)

# Enable pass="true" on all natural left turns across the city for genuine Free-Left logic
for c in con_tree.findall('connection'):
    fL = c.get('fromLane')
    tL = c.get('toLane')
    if fL == '0' and tL == '0':
        c.set('pass', 'true')

con_tree_obj = ET.ElementTree(con_tree)
con_tree_obj.write(CON_PATH, encoding='utf-8', xml_declaration=True)

# ==============================================================================
# 3. COMPILE SUMO.NET.XML WITH LEFTHAND
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
print("Compiled pure Indian Left-Hand Drive sumo.net.xml with Free-Left logic!")

# ==============================================================================
# 4. GENERATE MULTI-MODAL FLEET WITH INDIAN OVERTAKING & LANE PRIORITY
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
    if len(path) > 12:
        return []
    loops = []
    for nxt in adj.get(curr, []):
        if nxt == start and len(path) >= 3:
            loops.append(list(path))
        elif nxt not in visited and len(path) < 12:
            visited.add(nxt)
            path.append(nxt)
            loops.extend(find_loops(start, nxt, path, visited))
            path.pop()
            visited.remove(nxt)
    return loops

all_loops = []
for edge in list(adj.keys()):
    all_loops.extend(find_loops(edge, edge, [edge], {edge}))

curve_loops = [l for l in all_loops if any(e in l for e in ['0', '7', '6', '5', '4', '-3', '2', '-1', '-6', '-7', '-5', '-4', '8', '-8', '9', '-9', '10', '-10']) and 'shortcut_east' not in l and 'shortcut_west' not in l]
arterial_loops = [l for l in all_loops if any(e in l for e in ['23', '-23', '24', '-24', '22', '-22', '21', '-21', '18', '-18', '19', '-19', '16', '-16', '12', '-12', '17', '-17', '20', '-20', '14', '-14', '11', '-11', '13', '-13', 'outer_west', '-outer_west']) and 'shortcut_east' not in l and 'shortcut_west' not in l]
shortcut_loops = [l for l in all_loops if 'shortcut_east' in l or 'shortcut_west' in l]

rou_root = ET.Element('routes')

# Multi-modal types with Indian overtaking and filtering parameters:
# - lcStrategic="1.0": takes left lane early when making a left turn
# - lcSpeedGain="2.0": aggressively overtakes slower vehicles in the right lane
# - lcAssertive="1.5", lcPushy="0.5": agile lane filtering
# - lcOvertakeRight="false": strictly overtakes on the RIGHT in LHD
proto_vtypes = [
    # 🏍️ Motorbikes
    {'id': 'MotorbikeSimple',             'vClass': 'motorcycle', 'guiShape': 'motorcycle', 'length': '2.2', 'width': '0.9', 'minGap': '2.0', 'maxSpeed': '18.0', 'speedGain': '2.5', 'assertive': '1.8', 'pushy': '0.8'},
    # 🛵 Scooters
    {'id': 'ScooterSimple',               'vClass': 'moped',      'guiShape': 'motorcycle', 'length': '1.9', 'width': '0.8', 'minGap': '2.0', 'maxSpeed': '14.0', 'speedGain': '2.0', 'assertive': '1.5', 'pushy': '0.7'},
    # 🚌 Transit Buses
    {'id': 'BusSimple',                   'vClass': 'bus',        'guiShape': 'bus',        'length': '10.5','width': '2.6', 'minGap': '3.2', 'maxSpeed': '14.0', 'speedGain': '1.0', 'assertive': '1.0', 'pushy': '0.0'},
    # 🚐 Delivery Sprinters
    {'id': 'MercedesBenzSprinterSimple',  'vClass': 'delivery',   'guiShape': 'delivery',   'length': '6.0', 'width': '2.1', 'minGap': '2.6', 'maxSpeed': '15.0', 'speedGain': '1.5', 'assertive': '1.2', 'pushy': '0.2'},
    # 🚗 Passenger Cars
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
        'lcOvertakeRight': '0.0', # strictly overtake on the right (passing lane)
        'tau': '0.6',
    })

buses = [
    ('transit_bus_1', curve_loops[0] if curve_loops else all_loops[0]),
    ('transit_bus_2', arterial_loops[0] if arterial_loops else all_loops[1]),
    ('transit_bus_3', shortcut_loops[0] if shortcut_loops else all_loops[2]),
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
        loop = shortcut_loops[(idx - 85) % len(shortcut_loops)] if shortcut_loops else all_loops[idx % len(all_loops)]

    start_offset = idx % len(loop)
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
print(f"Generated 100-vehicle fleet with Indian Free-Left, Left Lane Priority & Overtaking in {ROU_PATH}")
