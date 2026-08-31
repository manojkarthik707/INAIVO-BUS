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
# 1. RESTORE V0.1 PLAIN.NETCCFG (STANDARD WEBOTS-SUMO COORDINATES)
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
# 2. RESTORE V0.1 PLAIN.EDG.XML + 2-LANE SHORTCUT
# ==============================================================================
res = subprocess.run(["git", "show", "V0.1:simulation/webots/worlds/sih_mvp_traffic_net/plain.edg.xml"], capture_output=True, text=True)
edg_text = res.stdout

# Add shortcut edges
tree_edg = ET.fromstring(edg_text)
for e in list(tree_edg.findall('edge')):
    if e.get('id') in ['shortcut_east', 'shortcut_west']:
        tree_edg.remove(e)

ET.SubElement(tree_edg, 'edge', {
    'id': 'shortcut_east',
    'from': '41',
    'to': '43',
    'priority': '-1',
    'numLanes': '1',
    'speed': '13.90',
    'width': '3.50'
})
ET.SubElement(tree_edg, 'edge', {
    'id': 'shortcut_west',
    'from': '43',
    'to': '41',
    'priority': '-1',
    'numLanes': '1',
    'speed': '13.90',
    'width': '3.50'
})

tree_edg_obj = ET.ElementTree(tree_edg)
tree_edg_obj.write(EDG_PATH, encoding='utf-8', xml_declaration=True)

# ==============================================================================
# 3. RESTORE V0.1 PLAIN.CON.XML + SHORTCUT CONNECTIONS
# ==============================================================================
res_con = subprocess.run(["git", "show", "V0.1:simulation/webots/worlds/sih_mvp_traffic_net/plain.con.xml"], capture_output=True, text=True)
con_tree = ET.fromstring(res_con.stdout)

# Purge U-turn turnarounds and existing shortcut connections
for c in list(con_tree.findall('connection')):
    f = c.get('from', '')
    t = c.get('to', '')
    if f == f"-{t}" or t == f"-{f}" or 'shortcut' in f or 'shortcut' in t:
        con_tree.remove(c)

shortcut_conns = [
    # Junction 41 (Left End)
    {'from': '23', 'to': 'shortcut_east', 'fromLane': '0', 'toLane': '0'},
    {'from': '8', 'to': 'shortcut_east', 'fromLane': '1', 'toLane': '0'},
    {'from': 'shortcut_west', 'to': '-8', 'fromLane': '0', 'toLane': '0'},
    {'from': 'shortcut_west', 'to': '-23', 'fromLane': '0', 'toLane': '1'},

    # Junction 43 (Right End)
    {'from': '6', 'to': 'shortcut_west', 'fromLane': '0', 'toLane': '0'},
    {'from': '-5', 'to': 'shortcut_west', 'fromLane': '1', 'toLane': '0'},
    {'from': 'shortcut_east', 'to': '5', 'fromLane': '0', 'toLane': '0'},
    {'from': 'shortcut_east', 'to': '-6', 'fromLane': '0', 'toLane': '1'},
]

for sc in shortcut_conns:
    ET.SubElement(con_tree, 'connection', sc)

con_tree_obj = ET.ElementTree(con_tree)
con_tree_obj.write(CON_PATH, encoding='utf-8', xml_declaration=True)

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

tree_net = ET.parse(NET_PATH)
root_net = tree_net.getroot()
for lane in root_net.findall('.//lane'):
    if not lane.get('id', '').startswith(':'):
        ET.SubElement(lane, 'stopOffset', {'value': '6.0'})

for conn in root_net.findall('connection'):
    conn.set('keepClear', '1')

tree_net.write(NET_PATH, encoding='utf-8', xml_declaration=True)
print("Compiled clean V0.1-based sumo.net.xml successfully!")

# ==============================================================================
# 5. GENERATE LONG-RUNNING 100-VEHICLE MULTI-MODAL FLEET
# ==============================================================================
# In V0.1, the primary loops are:
# Loop 1 (Outer Central Clockwise): 0 -> 7 -> 6 -> 5 -> 4 -> -3 -> 2 -> -1
loop_main = ['0', '7', '6', '5', '4', '-3', '2', '-1']

# Loop 2 (Central Figure-8 / Bypass): -23 -> 24 -> 22 -> 21 -> 18 -> 19 -> 16 -> 20 -> 14 -> 11 -> 13 -> -outer_west -> -15 -> 15 -> outer_west -> -13 -> -11 -> -14 -> -20 -> -16 -> -19 -> -18 -> -21 -> -22 -> -24 -> 23 -> -8 -> 9 -> -10 -> 17 -> 12 -> 18
loop_arterial = ['23', '-8', '9', '4', '-3', '2', '-1', '0', '7', '6', '5', '-9', '8', '-23', '24', '22', '21', '18', '19', '16', '12', '18']

# Loop 3 (Outer Highway Loop): 15 -> outer_west -> -13 -> -11 -> -14 -> -20 -> -16 -> -19 -> 16 -> 20 -> 14 -> 11 -> 13 -> -outer_west
loop_outer = ['15', 'outer_west', '-13', '-11', '-14', '-20', '-16', '-19', '16', '20', '14', '11', '13', '-outer_west']

# Loop 4 (Shortcut Parkway loops):
# - 23 -> shortcut_east -> 5 -> 4 -> -3 -> 2 -> -1 -> 0 -> 7 -> 6 -> shortcut_west -> -23 -> 24 -> 22 -> 21 -> 18 -> 19 -> 16 -> 12 -> 18
loop_shortcut_1 = ['23', 'shortcut_east', '5', '4', '-3', '2', '-1', '0', '7', '6', 'shortcut_west', '-23', '24', '22', '21', '18', '19', '16', '12', '18']
loop_shortcut_2 = ['8', 'shortcut_east', '-6', '-7', '23', 'shortcut_east', '5', '-9', '8']

# Repeat sequences 60 times (over 30 minutes of non-stop continuous driving!)
N_REPEATS = 60

path_main = loop_main * N_REPEATS
path_arterial = loop_arterial * N_REPEATS
path_outer = loop_outer * N_REPEATS
path_shortcut_1 = loop_shortcut_1 * N_REPEATS
path_shortcut_2 = loop_shortcut_2 * N_REPEATS

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

# 3 Buses: 1 on Main Loop, 1 on Arterial, 1 on Shortcut
buses = [
    ('transit_bus_1', path_main),
    ('transit_bus_2', path_arterial),
    ('transit_bus_3', path_shortcut_1),
]

for b_id, b_path in buses:
    r_id = f"route_{b_id}"
    ET.SubElement(rou_root, 'route', {'id': r_id, 'edges': " ".join(b_path)})
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

# 97 multi-modal vehicles:
# 50 on Main Curve Loop (50%)
# 25 on Arterial / Outer Highway (25%)
# 12 on Shortcut (12%)
# 10 on Outer Loop (10%)
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
        # Offset start inside path_main for distributed positions
        start_offset = (idx * 2) % len(loop_main)
        sub_path = loop_main[start_offset:] + loop_main[:start_offset]
        p_edges = sub_path * N_REPEATS
    elif idx < 75:
        start_offset = (idx * 3) % len(loop_arterial)
        sub_path = loop_arterial[start_offset:] + loop_arterial[:start_offset]
        p_edges = sub_path * N_REPEATS
    elif idx < 87:
        p_edges = path_shortcut_1 if idx % 2 == 0 else path_shortcut_2
    else:
        start_offset = (idx * 2) % len(loop_outer)
        sub_path = loop_outer[start_offset:] + loop_outer[:start_offset]
        p_edges = sub_path * N_REPEATS

    r_id = f"route_{idx}"
    ET.SubElement(rou_root, 'route', {'id': r_id, 'edges': " ".join(p_edges)})

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
        'departLane': 'random',
        'departPos': 'random',
        'departSpeed': 'max',
        'color': col
    })

rou_tree = ET.ElementTree(rou_root)
rou_tree.write(ROU_PATH, encoding='utf-8', xml_declaration=True)
print(f"Generated 100-vehicle fleet based on V0.1 routing logic in {ROU_PATH}")
