import xml.etree.ElementTree as ET
import os

NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"
ROU_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.rou.xml"

tree = ET.parse(NET_PATH)
root = tree.getroot()

all_edges = set([e.get('id') for e in root.findall('edge') if not e.get('id', '').startswith(':')])

connections = {}
for conn in root.findall('connection'):
    f = conn.get('from')
    t = conn.get('to')
    d = conn.get('dir')
    if f and t and not f.startswith(':') and not t.startswith(':'):
        rev = f[1:] if f.startswith('-') else ('-' + f)
        if t != rev and d != 't':
            connections.setdefault(f, set()).add(t)

def find_forward_circuit(start_edge, min_len=6, max_len=18):
    valid = []
    def dfs(curr, path):
        if len(path) >= max_len:
            return
        for nxt in connections.get(curr, []):
            if nxt == start_edge and len(path) >= min_len:
                valid.append(path)
                return
            elif nxt not in path:
                rev = curr[1:] if curr.startswith('-') else ('-' + curr)
                if nxt != rev:
                    dfs(nxt, path + [nxt])
    dfs(start_edge, [start_edge])
    return valid[0] if valid else None

circuits = []
for edge in sorted(list(all_edges)):
    c = find_forward_circuit(edge)
    if c:
        circuits.append(c)

print(f"Found {len(circuits)} clean forward loop routes across the city network.")

def make_infinite_loop(circuit, repeat=50):
    return " ".join(circuit * repeat)

elements = []

# 1. Commercial Test Buses (BUS_01, BUS_02, BUS_03)
bus_circuits = [circuits[0], circuits[len(circuits)//3], circuits[2*len(circuits)//3]]
for i in range(3):
    route_str = make_infinite_loop(bus_circuits[i])
    elements.append({
        'tag': 'vehicle',
        'id': str(i),
        'type': 'bus',
        'time': 0.0,
        'departPos': 'base',
        'departLane': '0',
        'departSpeed': 'max',
        'route': route_str
    })

# 2. Uniformly pre-populate vehicles across all 52 circuits at t=0
# Alternating lane 0 and lane 1 with random valid positions
initial_veh_id = 3
for c_idx, circ in enumerate(circuits):
    route_str = make_infinite_loop(circ)
    v_type = "bus" if initial_veh_id % 6 == 0 else ("delivery" if initial_veh_id % 3 == 0 else "passenger")
    assigned_lane = str(initial_veh_id % 2)
    
    elements.append({
        'tag': 'vehicle',
        'id': str(initial_veh_id),
        'type': v_type,
        'time': 0.0,
        'departPos': 'random',
        'departLane': assigned_lane,
        'departSpeed': 'max',
        'route': route_str
    })
    initial_veh_id += 1

# 3. Steady continuous flows with uniform harmonic intervals
for c_idx, circ in enumerate(circuits):
    route_str = make_infinite_loop(circ)
    flow_id = f"flow_{c_idx}"
    begin_val = 1.0 + c_idx * 0.35
    period_val = 16.0  # Steady harmonic renewal
    
    v_type = "bus" if c_idx % 6 == 0 else ("delivery" if c_idx % 3 == 0 else "passenger")
    
    elements.append({
        'tag': 'flow',
        'id': flow_id,
        'type': v_type,
        'time': begin_val,
        'end': '99999',
        'period': f"{period_val:.1f}",
        'departLane': 'best',
        'departPos': 'base',
        'departSpeed': 'max',
        'route': route_str
    })

# Sort all elements chronologically by departure / begin time
elements.sort(key=lambda x: x['time'])

output_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>\n',
    '<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">\n\n',
    '    <!-- UNIFORM HARMONIC CITY TRAFFIC (speedFactor=1.0, speedDev=0.0 to eliminate shockwave clumping and irregular gaps) -->\n',
    '    <!-- BusSimple (length=9.8m, width=2.6m, minGap=2.5m) -->\n',
    '    <vType id="bus" vClass="bus" carFollowModel="Krauss" accel="2.0" decel="4.5" length="9.8" width="2.6" minGap="2.5" maxSpeed="12.5" speedFactor="1.0" speedDev="0.0" tau="1.0" laneChangeModel="LC2013" lcStrategic="2.0" lcCooperative="1.0" lcSpeedGain="3.0" lcKeepRight="0.0" lcOvertakeRight="1.0" jmIgnoreKeepClearTime="-1" jmTimegapMinor="1.0" />\n\n',
    '    <!-- Mercedes Sprinter Delivery Van (length=7.0m, width=2.2m, minGap=2.2m) -->\n',
    '    <vType id="delivery" vClass="delivery" carFollowModel="Krauss" accel="2.5" decel="4.8" length="7.0" width="2.2" minGap="2.2" maxSpeed="12.5" speedFactor="1.0" speedDev="0.0" tau="1.0" laneChangeModel="LC2013" lcStrategic="2.0" lcCooperative="1.0" lcSpeedGain="3.0" lcKeepRight="0.0" lcOvertakeRight="1.0" jmIgnoreKeepClearTime="-1" jmTimegapMinor="0.9" />\n\n',
    '    <!-- Passenger Sedans & SUVs (length=5.0m, width=2.0m, minGap=2.0m) -->\n',
    '    <vType id="passenger" vClass="passenger" carFollowModel="Krauss" accel="2.8" decel="5.0" length="5.0" width="2.0" minGap="2.0" maxSpeed="12.5" speedFactor="1.0" speedDev="0.0" tau="1.0" laneChangeModel="LC2013" lcStrategic="2.0" lcCooperative="1.0" lcSpeedGain="3.0" lcKeepRight="0.0" lcOvertakeRight="1.0" jmIgnoreKeepClearTime="-1" jmTimegapMinor="0.8" />\n\n'
]

for el in elements:
    if el['tag'] == 'vehicle':
        output_lines.append(f'    <vehicle id="{el["id"]}" type="{el["type"]}" depart="{el["time"]:.2f}" departPos="{el["departPos"]}" departLane="{el["departLane"]}" departSpeed="{el["departSpeed"]}">\n')
        output_lines.append(f'        <route edges="{el["route"]}" />\n')
        output_lines.append('    </vehicle>\n')
    elif el['tag'] == 'flow':
        output_lines.append(f'    <flow id="{el["id"]}" type="{el["type"]}" begin="{el["time"]:.2f}" end="{el["end"]}" period="{el["period"]}" departLane="{el["departLane"]}" departPos="{el["departPos"]}" departSpeed="{el["departSpeed"]}">\n')
        output_lines.append(f'        <route edges="{el["route"]}" />\n')
        output_lines.append('    </flow>\n')

output_lines.append('</routes>\n')

with open(ROU_PATH, 'w', encoding='utf-8') as f:
    f.writelines(output_lines)

print(f"Generated uniform harmonic spacing traffic into {ROU_PATH}")
