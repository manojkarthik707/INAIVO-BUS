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
# 1. RESTORE CLEAN STANDARD PLAIN.NETCCFG (INTERNAL LINKS ENABLED)
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
# 2. RECOMPILE SUMO.NET.XML WITH PROPER INTERNAL JUNCTION LANES
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
print("Restored standard clean internal links with 28s TLS in sumo.net.xml")

# ==============================================================================
# 4. REGENERATE 1-VEHICLE-PER-EDGE PRELOADED FLEET
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

loops_by_start_edge = {}
for loop in all_loops:
    for i, e in enumerate(loop):
        shifted = loop[i:] + loop[:i]
        if e not in loops_by_start_edge:
            loops_by_start_edge[e] = []
        loops_by_start_edge[e].append(shifted)

all_unique_edges = sorted(list(loops_by_start_edge.keys()))

rou_root = ET.Element('routes')

proto_vtypes = [
    {'id': 'MotorbikeSimple',             'vClass': 'motorcycle', 'guiShape': 'motorcycle', 'length': '2.2', 'width': '0.9', 'minGap': '3.5', 'maxSpeed': '16.0'},
    {'id': 'ScooterSimple',               'vClass': 'moped',      'guiShape': 'motorcycle', 'length': '1.9', 'width': '0.8', 'minGap': '3.5', 'maxSpeed': '14.0'},
    {'id': 'BusSimple',                   'vClass': 'bus',        'guiShape': 'bus',        'length': '6.8', 'width': '2.2', 'minGap': '4.5', 'maxSpeed': '14.0'},
    {'id': 'MercedesBenzSprinterSimple',  'vClass': 'delivery',   'guiShape': 'delivery',   'length': '5.8', 'width': '2.0', 'minGap': '4.0', 'maxSpeed': '15.0'},
    {'id': 'TeslaModel3Simple',           'vClass': 'passenger',  'guiShape': 'passenger',  'length': '4.6', 'width': '1.8', 'minGap': '4.0', 'maxSpeed': '16.0'},
    {'id': 'ToyotaPriusSimple',           'vClass': 'passenger',  'guiShape': 'passenger',  'length': '4.4', 'width': '1.7', 'minGap': '4.0', 'maxSpeed': '15.0'},
    {'id': 'CitroenCZeroSimple',          'vClass': 'passenger',  'guiShape': 'passenger',  'length': '3.5', 'width': '1.5', 'minGap': '3.5', 'maxSpeed': '14.0'},
    {'id': 'BmwX5Simple',                 'vClass': 'passenger',  'guiShape': 'passenger',  'length': '4.8', 'width': '1.9', 'minGap': '4.0', 'maxSpeed': '16.0'},
]

for vt in proto_vtypes:
    ET.SubElement(rou_root, 'vType', {
        'id': vt['id'],
        'vClass': vt['vClass'],
        'guiShape': vt['guiShape'],
        'accel': '2.8',
        'decel': '4.5',
        'emergencyDecel': '9.0',
        'sigma': '0.0',
        'length': vt['length'],
        'width': vt['width'],
        'minGap': vt['minGap'],
        'maxSpeed': vt['maxSpeed'],
        'lcStrategic': '1.0',
        'lcCooperative': '1.0',
        'lcSpeedGain': '1.0',
        'lcAssertive': '1.0',
        'lcPushy': '0.0',
        'lcOvertakeRight': '0.0',
        'tau': '1.5',
    })

N_REPEATS = 60

random.seed(42)
selected_edges = list(all_unique_edges)
random.shuffle(selected_edges)

bus_edges = ['0', '23', 'shortcut_east']
for b_idx, b_edge in enumerate(bus_edges):
    b_id = f"transit_bus_{b_idx+1}"
    loop = loops_by_start_edge[b_edge][0]
    p_edges = " ".join(loop * N_REPEATS)
    r_id = f"route_{b_id}"
    ET.SubElement(rou_root, 'route', {'id': r_id, 'edges': p_edges})
    ET.SubElement(rou_root, 'vehicle', {
        'id': b_id,
        'type': 'BusSimple',
        'route': r_id,
        'depart': '0.00',
        'departLane': 'best',
        'departPos': 'base',
        'departSpeed': 'max',
        'color': '1.0,0.7,0.1'
    })
    if b_edge in selected_edges:
        selected_edges.remove(b_edge)

proto_pool = (
    ['MotorbikeSimple'] * 12 +
    ['ScooterSimple'] * 10 +
    ['TeslaModel3Simple'] * 7 +
    ['ToyotaPriusSimple'] * 7 +
    ['CitroenCZeroSimple'] * 5 +
    ['BmwX5Simple'] * 5 +
    ['MercedesBenzSprinterSimple'] * 4
)

random.shuffle(proto_pool)

for idx, (proto_type, start_edge) in enumerate(zip(proto_pool, selected_edges)):
    loop = random.choice(loops_by_start_edge[start_edge])
    p_edges = " ".join(loop * N_REPEATS)
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
        'departPos': 'base',
        'departSpeed': 'max',
        'color': col
    })

rou_tree = ET.ElementTree(rou_root)
rou_tree.write(ROU_PATH, encoding='utf-8', xml_declaration=True)
print(f"Generated clean preloaded fleet in {ROU_PATH}")
