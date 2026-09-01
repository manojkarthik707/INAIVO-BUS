"""
restore_instant_preloading.py — Preload 100 vehicles + 3 buses at t = 0.00s across all loops.

KEY FEATURES:
1. All 100 vehicles preloaded simultaneously at t = 0.00s with multi-loop routing.
2. departLane="free", departPos="random_free" prevents vehicle spawn overlap.
3. Natural multi-lane flow with lcKeepRight="0.0", lcStrategic="1.2", lcSpeedGain="1.0".
"""

import xml.etree.ElementTree as ET
import random

NET_FILE = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"
ROU_FILE = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.rou.xml"

tree = ET.parse(NET_FILE)
root = tree.getroot()

adj = {}
for conn in root.findall('connection'):
    frm = conn.get('from')
    to  = conn.get('to')
    if frm and to and not frm.startswith(':') and not to.startswith(':'):
        adj.setdefault(frm, set()).add(to)

edges = list(adj.keys())

def find_loops(max_loops=8, max_len=14):
    found = []
    for start in edges:
        queue = [[start]]
        while queue and len(found) < max_loops:
            path = queue.pop(0)
            curr = path[-1]
            if len(path) > 3 and curr == start:
                found.append(path[:-1])
                continue
            if len(path) >= max_len:
                continue
            for nxt in sorted(adj.get(curr, [])):
                if nxt == start or nxt not in path:
                    queue.append(path + [nxt])
    return found

all_loops = find_loops(max_loops=12, max_len=12)
if not all_loops:
    all_loops = [[e] for e in edges[:4]]

curve_loops = [lp for lp in all_loops if any("outer" in e or "13" in e for e in lp)]
arterial_loops = [lp for lp in all_loops if any("1" in e or "2" in e for e in lp)]
sc_loops = [lp for lp in all_loops if lp not in curve_loops and lp not in arterial_loops]

rou_root = ET.Element('routes')

proto_vtypes = [
    {'id': 'MotorbikeSimple',             'vClass': 'motorcycle', 'guiShape': 'motorcycle', 'length': '2.2', 'width': '0.9', 'minGap': '3.0', 'maxSpeed': '16.0'},
    {'id': 'ScooterSimple',               'vClass': 'moped',      'guiShape': 'motorcycle', 'length': '1.9', 'width': '0.8', 'minGap': '3.0', 'maxSpeed': '14.0'},
    {'id': 'BusSimple',                   'vClass': 'bus',        'guiShape': 'bus',        'length': '10.5','width': '2.6', 'minGap': '4.5', 'maxSpeed': '14.0'},
    {'id': 'MercedesBenzSprinterSimple',  'vClass': 'delivery',   'guiShape': 'delivery',   'length': '6.0', 'width': '2.1', 'minGap': '3.8', 'maxSpeed': '15.0'},
    {'id': 'TeslaModel3Simple',           'vClass': 'passenger',  'guiShape': 'passenger',  'length': '4.7', 'width': '1.8', 'minGap': '3.5', 'maxSpeed': '16.0'},
    {'id': 'ToyotaPriusSimple',           'vClass': 'passenger',  'guiShape': 'passenger',  'length': '4.5', 'width': '1.7', 'minGap': '3.5', 'maxSpeed': '16.0'},
    {'id': 'CitroenCZeroSimple',          'vClass': 'passenger',  'guiShape': 'passenger',  'length': '3.5', 'width': '1.5', 'minGap': '3.0', 'maxSpeed': '15.0'},
    {'id': 'BmwX5Simple',                 'vClass': 'passenger',  'guiShape': 'passenger',  'length': '4.9', 'width': '2.0', 'minGap': '3.5', 'maxSpeed': '16.0'},
]

for vt in proto_vtypes:
    ET.SubElement(rou_root, 'vType', {
        'id': vt['id'],
        'vClass': vt['vClass'],
        'guiShape': vt['guiShape'],
        'accel': '2.6',
        'decel': '4.5',
        'emergencyDecel': '9.0',
        'sigma': '0.1',
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

buses = [
    ('transit_bus_1', curve_loops[0] if curve_loops else all_loops[0]),
    ('transit_bus_2', arterial_loops[0] if arterial_loops else all_loops[1]),
    ('transit_bus_3', sc_loops[0] if sc_loops else all_loops[2]),
]

N_REPEATS = 60

# 100% Simultaneous Preloading at t = 0.00s across the whole city
for b_idx, (b_id, b_loop) in enumerate(buses):
    r_id = f"route_{b_id}"
    p_edges = " ".join(b_loop * N_REPEATS)
    ET.SubElement(rou_root, 'route', {'id': r_id, 'edges': p_edges})
    ET.SubElement(rou_root, 'vehicle', {
        'id': b_id,
        'type': 'BusSimple',
        'route': r_id,
        'depart': '0.00',
        'departLane': 'best',
        'departPos': 'random_free',
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

for v_idx in range(97):
    v_id = f"traffic_veh_{v_idx+1:03d}"
    lp = all_loops[v_idx % len(all_loops)]
    r_id = f"route_{v_id}"
    p_edges = " ".join(lp * N_REPEATS)
    v_type = proto_pool[v_idx % len(proto_pool)]

    ET.SubElement(rou_root, 'route', {'id': r_id, 'edges': p_edges})
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
        for subelem in elem:
            indent(subelem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

indent(rou_root)
tree_out = ET.ElementTree(rou_root)
tree_out.write(ROU_FILE, encoding="utf-8", xml_declaration=True)
print(f"Preloaded 100 vehicles (3 buses + 97 mixed fleet) safely with departLane=free.")
