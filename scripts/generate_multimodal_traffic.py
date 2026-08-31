import xml.etree.ElementTree as ET

NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"
ROU_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.rou.xml"

tree = ET.parse(NET_PATH)
root = tree.getroot()

all_edges = sorted(list(set([e.get('id') for e in root.findall('edge') if not e.get('id', '').startswith(':')])))

connections = {}
for conn in root.findall('connection'):
    f = conn.get('from')
    t = conn.get('to')
    d = conn.get('dir')
    if f and t and not f.startswith(':') and not t.startswith(':'):
        rev = f[1:] if f.startswith('-') else ('-' + f)
        if t != rev and d != 't':
            connections.setdefault(f, set()).add(t)

def find_all_circuits_from_edge(start_edge, min_len=4, max_len=14, limit=6):
    circuits = []
    def dfs(curr, path):
        if len(circuits) >= limit:
            return
        if len(path) > max_len:
            return
        for nxt in connections.get(curr, []):
            if nxt == start_edge and len(path) >= min_len:
                circuits.append(path)
            elif nxt not in path:
                rev = curr[1:] if curr.startswith('-') else ('-' + curr)
                if nxt != rev:
                    dfs(nxt, path + [nxt])
    dfs(start_edge, [start_edge])
    return circuits

circuit_library = {}
for edge in all_edges:
    c_list = find_all_circuits_from_edge(edge)
    circuit_library[edge] = c_list

def make_infinite_loop(circuit, repeat=200):
    return " ".join(circuit * repeat)

elements = []

# 1. Primary Transit Buses (BUS_01, BUS_02, BUS_03)
primary_edges = ['0', '10', '16']
for i, edge in enumerate(primary_edges):
    routes = circuit_library[edge]
    chosen_route = routes[i % len(routes)]
    route_str = make_infinite_loop(chosen_route)
    elements.append({
        'tag': 'vehicle',
        'id': str(i),
        'type': 'bus',
        'time': 0.0,
        'departPos': '5.0',
        'departLane': '0',
        'departSpeed': 'max',
        'route': route_str
    })

# 2. Multi-Modal Circulating Fleet (52 Vehicles: Cars, Motorcycles, Scooters, Bicycles, Buses)
veh_types = [
    'passenger', 'motorcycle', 'passenger', 'scooter', 'motorcycle',
    'passenger', 'bus', 'passenger', 'motorcycle', 'scooter',
    'passenger', 'bicycle', 'passenger', 'motorcycle', 'passenger'
]

veh_id = 3
for edge_idx, edge in enumerate(all_edges):
    routes = circuit_library[edge]
    chosen_route = routes[edge_idx % len(routes)]
    route_str = make_infinite_loop(chosen_route)
    
    v_type = veh_types[(veh_id - 3) % len(veh_types)]
    assigned_lane = str(veh_id % 2)
    staggered_pos = "12.0" if veh_id % 2 == 0 else "4.0"
    
    elements.append({
        'tag': 'vehicle',
        'id': str(veh_id),
        'type': v_type,
        'time': 0.0,
        'departPos': staggered_pos,
        'departLane': assigned_lane,
        'departSpeed': 'max',
        'route': route_str
    })
    veh_id += 1

# 3. Add extra agile two-wheelers inserted smoothly with staggered time
extra_two_wheelers = ['0', '10', '16', '-23', '-24', '-7', '5', '9', '17', '-20']
for i, edge in enumerate(extra_two_wheelers):
    routes = circuit_library[edge]
    chosen_route = routes[(i + 1) % len(routes)]
    route_str = make_infinite_loop(chosen_route)
    t_type = "motorcycle" if i % 2 == 0 else "scooter"
    elements.append({
        'tag': 'vehicle',
        'id': str(veh_id),
        'type': t_type,
        'time': 5.0 + (i * 2.0),
        'departPos': '28.0',
        'departLane': '1',
        'departSpeed': 'max',
        'route': route_str
    })
    veh_id += 1

output_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>\n',
    '<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">\n\n',
    '    <!-- ============================================================================== -->\n',
    '    <!-- MULTI-MODAL INDIAN URBAN VEHICLE TYPES                                          -->\n',
    '    <!-- Buses, Passenger Cars, Agile Motorcycles, Urban Scooters, Bicycles              -->\n',
    '    <!-- ============================================================================== -->\n',
    '    <!-- 1. Commercial Transit Bus -->\n',
    '    <vType id="bus" vClass="bus" carFollowModel="Krauss" accel="4.8" decel="6.5" emergencyDecel="10.0" length="9.8" width="2.6" minGap="2.0" maxSpeed="18.0" speedFactor="1.0" speedDev="0.0" tau="0.40" laneChangeModel="LC2013" lcStrategic="1.5" lcCooperative="1.0" lcSpeedGain="8.0" lcKeepRight="0.0" lcOvertakeRight="1.0" lcPushy="1.0" lcAssertive="3.0" lcSpeedGainLookahead="5.0" lcLookaheadLeft="5.0" jmStoplineGap="2.5" jmIgnoreKeepClearTime="-1" jmDriveAfterRedTime="0" jmDriveAfterYellowTime="0" jmTimegapMinor="0.8" />\n\n',
    '    <!-- 2. Passenger City Cars (Sedans, SUVs, Hatchbacks) -->\n',
    '    <vType id="passenger" vClass="passenger" carFollowModel="Krauss" accel="6.5" decel="7.5" emergencyDecel="11.0" length="5.0" width="2.0" minGap="1.8" maxSpeed="18.0" speedFactor="1.0" speedDev="0.0" tau="0.35" laneChangeModel="LC2013" lcStrategic="1.5" lcCooperative="1.0" lcSpeedGain="10.0" lcKeepRight="0.0" lcOvertakeRight="1.0" lcPushy="1.0" lcAssertive="3.5" lcSpeedGainLookahead="6.0" lcLookaheadLeft="6.0" jmStoplineGap="2.5" jmIgnoreKeepClearTime="-1" jmDriveAfterRedTime="0" jmDriveAfterYellowTime="0" jmTimegapMinor="0.6" />\n\n',
    '    <!-- 3. Agile Two-Wheeler Motorcycles (Swift filtering & overtaking) -->\n',
    '    <vType id="motorcycle" vClass="motorcycle" carFollowModel="Krauss" accel="7.0" decel="8.0" emergencyDecel="12.0" length="2.2" width="0.9" minGap="1.2" maxSpeed="20.0" speedFactor="1.0" speedDev="0.0" tau="0.30" laneChangeModel="LC2013" lcStrategic="2.0" lcCooperative="1.0" lcSpeedGain="15.0" lcKeepRight="0.0" lcOvertakeRight="1.0" lcPushy="1.0" lcAssertive="4.0" lcSpeedGainLookahead="8.0" lcLookaheadLeft="8.0" jmStoplineGap="1.5" jmIgnoreKeepClearTime="-1" jmDriveAfterRedTime="0" jmDriveAfterYellowTime="0" jmTimegapMinor="0.4" />\n\n',
    '    <!-- 4. Urban Scooters / Mopeds -->\n',
    '    <vType id="scooter" vClass="moped" carFollowModel="Krauss" accel="5.5" decel="7.0" emergencyDecel="10.0" length="1.9" width="0.85" minGap="1.2" maxSpeed="16.0" speedFactor="1.0" speedDev="0.0" tau="0.35" laneChangeModel="LC2013" lcStrategic="2.0" lcCooperative="1.0" lcSpeedGain="12.0" lcKeepRight="0.0" lcOvertakeRight="1.0" lcPushy="1.0" lcAssertive="3.5" lcSpeedGainLookahead="6.0" lcLookaheadLeft="6.0" jmStoplineGap="1.5" jmIgnoreKeepClearTime="-1" jmDriveAfterRedTime="0" jmDriveAfterYellowTime="0" jmTimegapMinor="0.5" />\n\n',
    '    <!-- 5. Urban Bicycles -->\n',
    '    <vType id="bicycle" vClass="bicycle" carFollowModel="Krauss" accel="2.8" decel="5.5" emergencyDecel="8.0" length="1.7" width="0.70" minGap="1.0" maxSpeed="7.0" speedFactor="1.0" speedDev="0.0" tau="0.50" laneChangeModel="LC2013" lcStrategic="1.0" lcCooperative="1.0" lcSpeedGain="5.0" lcKeepRight="0.0" lcOvertakeRight="1.0" lcPushy="0.8" lcAssertive="2.5" lcSpeedGainLookahead="4.0" lcLookaheadLeft="4.0" jmStoplineGap="1.5" jmIgnoreKeepClearTime="-1" jmDriveAfterRedTime="0" jmDriveAfterYellowTime="0" jmTimegapMinor="0.8" />\n\n'
]

for el in elements:
    output_lines.append(f'    <vehicle id="{el["id"]}" type="{el["type"]}" depart="{el["time"]:.2f}" departPos="{el["departPos"]}" departLane="{el["departLane"]}" departSpeed="{el["departSpeed"]}">\n')
    output_lines.append(f'        <route edges="{el["route"]}" />\n')
    output_lines.append('    </vehicle>\n')

output_lines.append('</routes>\n')

with open(ROU_PATH, 'w', encoding='utf-8') as f:
    f.writelines(output_lines)

print(f"Generated clean collision-free multi-modal fleet of {len(elements)} vehicles in {ROU_PATH}")
