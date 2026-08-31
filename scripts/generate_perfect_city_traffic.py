import xml.etree.ElementTree as ET
import os
import random

NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"
ROU_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.rou.xml"

tree = ET.parse(NET_PATH)
root = tree.getroot()

# Extract all valid non-internal edges
all_edges = set([e.get('id') for e in root.findall('edge') if not e.get('id', '').startswith(':')])

# Build forward connectivity graph (no U-turns)
connections = {}
for conn in root.findall('connection'):
    f = conn.get('from')
    t = conn.get('to')
    d = conn.get('dir')
    if f and t and not f.startswith(':') and not t.startswith(':'):
        rev = f[1:] if f.startswith('-') else ('-' + f)
        if t != rev and d != 't':
            connections.setdefault(f, set()).add(t)

# DFS to find forward closed loops
def find_forward_circuit(start_edge, min_len=6, max_len=20):
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

# Collect loops starting from every edge
circuits = []
for edge in sorted(list(all_edges)):
    c = find_forward_circuit(edge)
    if c:
        circuits.append(c)

print(f"Found {len(circuits)} forward loop routes across the city network.")

# Build 100 loops repeated so vehicles never stop and continuous traffic flows forever
def make_infinite_loop(circuit, repeat=35):
    return " ".join(circuit * repeat)

NUM_TOTAL_VEHICLES = 90
output_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>\n',
    '<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">\n\n',
    '    <!-- Realistic Multi-Lane Urban Vehicle Types with Active Overtaking & Lane Balancing -->\n',
    '    <vType id="bus" vClass="bus" carFollowModel="IDM" accel="2.2" decel="4.0" length="9.5" minGap="3.5" maxSpeed="15.0" speedFactor="1.3" speedDev="0.05" tau="1.0" laneChangeModel="LC2013" lcStrategic="1.2" lcCooperative="1.0" lcSpeedGain="1.5" lcKeepRight="0.0" lcOvertakeRight="0.5" />\n',
    '    <vType id="passenger" vClass="passenger" carFollowModel="IDM" accel="3.2" decel="5.0" length="4.5" minGap="2.5" maxSpeed="20.0" speedFactor="1.4" speedDev="0.1" tau="0.9" laneChangeModel="LC2013" lcStrategic="1.5" lcCooperative="1.0" lcSpeedGain="2.5" lcKeepRight="0.0" lcOvertakeRight="0.8" />\n\n'
]

# Vehicle 0, 1, 2 are dedicated Commercial Buses (BUS_01, BUS_02, BUS_03)
# Placed on 3 distinct major routes with clean spacing
bus_routes = [circuits[0], circuits[len(circuits)//3], circuits[2*len(circuits)//3]]
for i in range(3):
    route_str = make_infinite_loop(bus_routes[i])
    depart_time = f"{i * 0.8:.2f}"
    output_lines.append(f'    <vehicle id="{i}" type="bus" depart="{depart_time}" departLane="0" departSpeed="max">\n')
    output_lines.append(f'        <route edges="{route_str}" />\n')
    output_lines.append(f'    </vehicle>\n')

# Populate 87 cars evenly distributed across all road circuits
# Using departLane="random" so cars fill BOTH lanes (inner & outer) evenly
# Staggered departures across all entrance nodes to eliminate bunches & gaps
for v_id in range(3, NUM_TOTAL_VEHICLES):
    c_idx = (v_id - 3) % len(circuits)
    route_str = make_infinite_loop(circuits[c_idx])
    depart_time = f"{(v_id - 3) * 0.5:.2f}"
    depart_lane = "random"  # Fills both lane 0 and lane 1
    
    # 1 out of 6 vehicles is a transit bus, remainder are passenger cars
    v_type = "bus" if (v_id % 6 == 0) else "passenger"
    
    output_lines.append(f'    <vehicle id="{v_id}" type="{v_type}" depart="{depart_time}" departLane="{depart_lane}" departSpeed="max">\n')
    output_lines.append(f'        <route edges="{route_str}" />\n')
    output_lines.append(f'    </vehicle>\n')

output_lines.append('</routes>\n')

with open(ROU_PATH, 'w', encoding='utf-8') as f:
    f.writelines(output_lines)

print(f"Generated {NUM_TOTAL_VEHICLES} vehicles with multi-lane distribution and LC2013 overtaking into {ROU_PATH}")
