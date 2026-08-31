import xml.etree.ElementTree as ET
import os

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

print(f"Constructed diverse multi-route library across all {len(circuit_library)} edges.")

def make_infinite_loop(circuit, repeat=200):
    return " ".join(circuit * repeat)

elements = []

# 1. Commercial Test Buses (BUS_01, BUS_02, BUS_03)
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

# 2. Exactly 52 Circulating City Vehicles (IDs 3..54)
veh_id = 3
for edge_idx, edge in enumerate(all_edges):
    routes = circuit_library[edge]
    chosen_route = routes[edge_idx % len(routes)]
    route_str = make_infinite_loop(chosen_route)
    
    v_type = "bus" if veh_id % 7 == 0 else "passenger"
    assigned_lane = str(veh_id % 2)
    staggered_pos = "10.0" if veh_id % 2 == 0 else "5.0"
    
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

output_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>\n',
    '<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">\n\n',
    '    <!-- HIGH-SPEED URBAN FLEET: maxSpeed=25.0 m/s (90 km/h), rapid acceleration, zero-latency response -->\n',
    '    <!-- BusSimple (Commercial Transit Bus: length=9.8m, width=2.6m, minGap=2.5m) -->\n',
    '    <vType id="bus" vClass="bus" carFollowModel="Krauss" accel="3.8" decel="6.5" emergencyDecel="10.0" length="9.8" width="2.6" minGap="2.5" maxSpeed="25.0" speedFactor="1.0" speedDev="0.0" tau="0.75" laneChangeModel="LC2013" lcStrategic="1.5" lcCooperative="1.0" lcSpeedGain="10.0" lcKeepRight="0.0" lcOvertakeRight="1.0" lcPushy="1.0" lcAssertive="3.0" lcSpeedGainLookahead="5.0" lcLookaheadLeft="5.0" jmStoplineGap="4.0" jmIgnoreKeepClearTime="-1" jmDriveAfterRedTime="0" jmDriveAfterYellowTime="0" jmTimegapMinor="1.0" />\n\n',
    '    <!-- Passenger City Cars (Sedans, SUVs, Hatchbacks: length=5.0m, width=2.0m, minGap=2.2m) -->\n',
    '    <vType id="passenger" vClass="passenger" carFollowModel="Krauss" accel="4.8" decel="7.5" emergencyDecel="11.0" length="5.0" width="2.0" minGap="2.2" maxSpeed="25.0" speedFactor="1.0" speedDev="0.0" tau="0.70" laneChangeModel="LC2013" lcStrategic="1.5" lcCooperative="1.0" lcSpeedGain="12.0" lcKeepRight="0.0" lcOvertakeRight="1.0" lcPushy="1.0" lcAssertive="3.5" lcSpeedGainLookahead="6.0" lcLookaheadLeft="6.0" jmStoplineGap="4.0" jmIgnoreKeepClearTime="-1" jmDriveAfterRedTime="0" jmDriveAfterYellowTime="0" jmTimegapMinor="0.8" />\n\n'
]

for el in elements:
    output_lines.append(f'    <vehicle id="{el["id"]}" type="{el["type"]}" depart="{el["time"]:.2f}" departPos="{el["departPos"]}" departLane="{el["departLane"]}" departSpeed="{el["departSpeed"]}">\n')
    output_lines.append(f'        <route edges="{el["route"]}" />\n')
    output_lines.append('    </vehicle>\n')

output_lines.append('</routes>\n')

with open(ROU_PATH, 'w', encoding='utf-8') as f:
    f.writelines(output_lines)

print(f"Generated 2X high-speed fleet of {len(elements)} vehicles into {ROU_PATH}")
