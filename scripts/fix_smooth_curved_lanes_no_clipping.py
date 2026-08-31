import xml.etree.ElementTree as ET
import subprocess
import random

NOD_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\plain.nod.xml"
EDG_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\plain.edg.xml"
CON_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\plain.con.xml"
CFG_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\plain.netccfg"
TLL_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\plain.tll.xml"
NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"
ROU_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.rou.xml"

# ==============================================================================
# 1. CONFIGURE NETCCFG WITH SMOOTH CORNER BEZIER CURVES
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
        <junctions.corner-detail value="5"/>
        <junctions.internal-link-detail value="5"/>
        <junctions.limit-turn-speed value="-1.00"/>
    </junctions>
</netconvertConfiguration>
"""
with open(CFG_PATH, 'w', encoding='utf-8') as f:
    f.write(cfg_content)

# ==============================================================================
# 2. RECOMPILE SUMO.NET.XML WITH SMOOTH BEZIER TURNING GEOMETRY
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

# ==============================================================================
# 3. SYNCHRONIZE 28s EXACT PHASES FOR ALL 5 TLS (25, 26, 27, 41, 43)
# ==============================================================================
tree = ET.parse(NET_PATH)
root = tree.getroot()

for lane in root.findall('.//lane'):
    for so in list(lane.findall('stopOffset')):
        lane.remove(so)

for conn in root.findall('connection'):
    conn.set('keepClear', '1')

for tl in root.findall('tlLogic'):
    tl_id = tl.get('id')
    for p in list(tl.findall('phase')):
        tl.remove(p)

    if tl_id == '25':
        ET.SubElement(tl, 'phase', {'duration': '5.0', 'state': 'GGGgrrrrrrrrrrrr'})
        ET.SubElement(tl, 'phase', {'duration': '2.0', 'state': 'yyyyrrrrrrrrrrrr'})
        ET.SubElement(tl, 'phase', {'duration': '5.0', 'state': 'rrrrGGGgrrrrrrrr'})
        ET.SubElement(tl, 'phase', {'duration': '2.0', 'state': 'rrrryyyyrrrrrrrr'})
        ET.SubElement(tl, 'phase', {'duration': '5.0', 'state': 'rrrrrrrrGGGgrrrr'})
        ET.SubElement(tl, 'phase', {'duration': '2.0', 'state': 'rrrrrrrryyyyrrrr'})
        ET.SubElement(tl, 'phase', {'duration': '5.0', 'state': 'rrrrrrrrrrrrGGGg'})
        ET.SubElement(tl, 'phase', {'duration': '2.0', 'state': 'rrrrrrrrrrrryyyy'})

    elif tl_id in ['26', '27']:
        ET.SubElement(tl, 'phase', {'duration': '5.0', 'state': 'GGGgrrrrrrrrrrrr'})
        ET.SubElement(tl, 'phase', {'duration': '2.0', 'state': 'yyyyrrrrrrrrrrrr'})
        ET.SubElement(tl, 'phase', {'duration': '5.0', 'state': 'rrrrGGGgrrrrrrrr'})
        ET.SubElement(tl, 'phase', {'duration': '2.0', 'state': 'rrrryyyyrrrrrrrr'})
        ET.SubElement(tl, 'phase', {'duration': '5.0', 'state': 'rrrrrrrrGGGgrrrr'})
        ET.SubElement(tl, 'phase', {'duration': '2.0', 'state': 'rrrrrrrryyyyrrrr'})
        ET.SubElement(tl, 'phase', {'duration': '5.0', 'state': 'rrrrrrrrrrrrGGGg'})
        ET.SubElement(tl, 'phase', {'duration': '2.0', 'state': 'rrrrrrrrrrrryyyy'})

    elif tl_id == '41':
        ET.SubElement(tl, 'phase', {'duration': '12.0', 'state': 'GGgrrGGg'})
        ET.SubElement(tl, 'phase', {'duration': '2.0',  'state': 'yyyrryyy'})
        ET.SubElement(tl, 'phase', {'duration': '12.0', 'state': 'rrrGGrrr'})
        ET.SubElement(tl, 'phase', {'duration': '2.0',  'state': 'rrryyrrr'})

    elif tl_id == '43':
        ET.SubElement(tl, 'phase', {'duration': '12.0', 'state': 'gGGGGgrr'})
        ET.SubElement(tl, 'phase', {'duration': '2.0',  'state': 'yyyyyyrr'})
        ET.SubElement(tl, 'phase', {'duration': '12.0', 'state': 'rrrrrrGG'})
        ET.SubElement(tl, 'phase', {'duration': '2.0',  'state': 'rrrrrryy'})

tree.write(NET_PATH, encoding='utf-8', xml_declaration=True)
print("Configured smooth curved bezier junction network in sumo.net.xml!")

# ==============================================================================
# 4. REGENERATE 100-VEHICLE FLEET WITH SAFE LATERAL GAP (ZERO CLIPPING / ZERO OVERLAPPING)
# ==============================================================================
adj = {}
for conn in root.findall('connection'):
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

print(f"Total discovered valid loops: {len(all_loops)}")

sc_loops = [l for l in all_loops if 'shortcut_east' in l or 'shortcut_west' in l]
curve_loops = [l for l in all_loops if any(e in l for e in ['0', '7', '6', '5', '4', '-3', '2', '-1']) and 'shortcut_east' not in l and 'shortcut_west' not in l]
arterial_loops = [l for l in all_loops if any(e in l for e in ['23', '-8', '9', '-10', '17', '12', '-18', '21', '22', '24']) and 'shortcut_east' not in l and 'shortcut_west' not in l]

rou_root = ET.Element('routes')

# Multi-modal types with zero clipping:
# - minGap: 2.8m (cars), 2.5m (bikes)
# - lcPushy: 0.0 (prevents forcing into occupied space)
# - lcAssertive: 1.0 (smooth, polite lane changes)
# - lcSpeedGain: 1.0
proto_vtypes = [
    {'id': 'MotorbikeSimple',             'vClass': 'motorcycle', 'guiShape': 'motorcycle', 'length': '2.2', 'width': '0.9', 'minGap': '2.5', 'maxSpeed': '16.0'},
    {'id': 'ScooterSimple',               'vClass': 'moped',      'guiShape': 'motorcycle', 'length': '1.9', 'width': '0.8', 'minGap': '2.5', 'maxSpeed': '14.0'},
    {'id': 'BusSimple',                   'vClass': 'bus',        'guiShape': 'bus',        'length': '10.5','width': '2.6', 'minGap': '3.5', 'maxSpeed': '14.0'},
    {'id': 'MercedesBenzSprinterSimple',  'vClass': 'delivery',   'guiShape': 'delivery',   'length': '6.0', 'width': '2.1', 'minGap': '2.8', 'maxSpeed': '15.0'},
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
        'lcSpeedGain': '1.0',
        'lcAssertive': '1.0',
        'lcPushy': '0.0', # Zero physical clipping/overlapping
        'lcOvertakeRight': '0.0',
        'tau': '0.7',
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
print(f"Generated 100-vehicle fleet with zero clipping and safe gap margins in {ROU_PATH}")
