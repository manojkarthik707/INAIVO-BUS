import xml.etree.ElementTree as ET
import subprocess
import random

CON_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\plain.con.xml"
CFG_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\plain.netccfg"
NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"
ROU_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.rou.xml"

# 1. Update plain.con.xml for explicit Free-Left priority on shortcut
tree_con = ET.parse(CON_PATH)
root_con = tree_con.getroot()

for c in list(root_con.findall('connection')):
    f = c.get('from', '')
    t = c.get('to', '')
    if 'shortcut' in f or 'shortcut' in t:
        root_con.remove(c)

shortcut_conns = [
    # Junction 41 (Left End of Shortcut):
    # Free-Left into shortcut from South (8 -> shortcut_east)
    {'from': '8', 'to': 'shortcut_east', 'fromLane': '0', 'toLane': '0', 'pass': 'true'},
    # Turn into shortcut from North (23 -> shortcut_east)
    {'from': '23', 'to': 'shortcut_east', 'fromLane': '1', 'toLane': '0'},
    # Free-Left exiting shortcut to South (shortcut_west -> -23)
    {'from': 'shortcut_west', 'to': '-23', 'fromLane': '0', 'toLane': '0', 'pass': 'true'},
    # Turn exiting shortcut to North (shortcut_west -> -8)
    {'from': 'shortcut_west', 'to': '-8', 'fromLane': '0', 'toLane': '1'},

    # Junction 43 (Right End of Shortcut):
    # Free-Left into shortcut from North (6 -> shortcut_west)
    {'from': '6', 'to': 'shortcut_west', 'fromLane': '0', 'toLane': '0', 'pass': 'true'},
    # Turn into shortcut from South (-5 -> shortcut_west)
    {'from': '-5', 'to': 'shortcut_west', 'fromLane': '1', 'toLane': '0'},
    # Free-Left exiting shortcut to South (shortcut_east -> 5)
    {'from': 'shortcut_east', 'to': '5', 'fromLane': '0', 'toLane': '0', 'pass': 'true'},
    # Turn exiting shortcut to North (shortcut_east -> -6)
    {'from': 'shortcut_east', 'to': '-6', 'fromLane': '0', 'toLane': '1'},
]

for sc in shortcut_conns:
    ET.SubElement(root_con, 'connection', sc)

tree_con.write(CON_PATH, encoding='utf-8', xml_declaration=True)

# 2. Recompile sumo.net.xml
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
print("Recompiled sumo.net.xml with Free-Left priority on shortcut.")

# 3. Generate balanced routes where shortcut vehicles take the smooth Left turn
# Natural Left-Flow Loops:
# Loop Shortcut West Free-Left: 6 -> shortcut_west -> -23 -> 24 -> 22 -> 21 -> 18 -> 19 -> 16 -> 20 -> 14 -> 11 -> 13 -> -outer_west -> -15 -> 15 -> outer_west -> -13 -> -11 -> -14 -> -20 -> -16 -> -19 -> -18 -> -21 -> -22 -> -24 -> 0 -> 7 -> 6
loop_sc_left_1 = ['6', 'shortcut_west', '-23', '24', '22', '21', '18', '19', '16', '12', '18', '21', '22', '-24', '0', '7', '6']

# Loop Shortcut East Free-Left: 8 -> shortcut_east -> 5 -> 4 -> -3 -> 2 -> -1 -> 0 -> 7 -> 6 -> 5 -> 4 -> -3 -> 2 -> -1 -> 0 -> 23 -> -8 -> 9 -> 8
loop_sc_left_2 = ['8', 'shortcut_east', '5', '4', '-3', '2', '-1', '0', '7', '6', '5', '4', '-3', '2', '-1', '0', '23', '-8', '9', '8']

# Main Curves & Arterials:
loop_curve_main = ['0', '7', '6', '5', '4', '-3', '2', '-1']
loop_arterial_main = ['23', '-8', '9', '4', '-3', '2', '-1', '0', '7', '6', '5', '-9', '8', '-23', '24', '22', '21', '18', '19', '16', '12', '18']
loop_outer_highway = ['15', 'outer_west', '-13', '-11', '-14', '-20', '-16', '-19', '16', '20', '14', '11', '13', '-outer_west']

N_REPEATS = 60

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

# 3 Buses
buses = [
    ('transit_bus_1', loop_curve_main),
    ('transit_bus_2', loop_arterial_main),
    ('transit_bus_3', loop_sc_left_1),
]

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
        loop = loop_curve_main
    elif idx < 75:
        loop = loop_arterial_main
    elif idx < 87:
        loop = loop_sc_left_1 if idx % 2 == 0 else loop_sc_left_2
    else:
        loop = loop_outer_highway

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
print(f"Generated 100-vehicle fleet with smooth Left-Flow on Shortcut Road in {ROU_PATH}")
