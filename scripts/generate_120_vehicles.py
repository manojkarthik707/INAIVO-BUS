import xml.etree.ElementTree as ET
import os
import random

NUM_BUSES = 20
NUM_CARS = 100
TOTAL_VEHICLES = NUM_BUSES + NUM_CARS
MIN_GAP = 4.5

# Parse SUMO net to build forward-only connections
net_tree = ET.parse(r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml")
net_root = net_tree.getroot()

all_edges = set([e.get('id') for e in net_root.findall('edge') if not e.get('id', '').startswith(':')])

clean_connections = {}
for conn in net_root.findall('connection'):
    f = conn.get('from')
    t = conn.get('to')
    d = conn.get('dir')
    if f and t and not f.startswith(':') and not t.startswith(':'):
        rev = f[1:] if f.startswith('-') else ('-' + f)
        # Strict NO U-turns
        if t != rev and d != 't':
            clean_connections.setdefault(f, set()).add(t)

# Find forward loops starting from all edges
def find_forward_circuit_from(start_edge, min_len=4, max_len=18):
    valid = []
    def dfs(curr, path):
        if len(path) >= max_len:
            return
        for nxt in clean_connections.get(curr, []):
            if nxt == start_edge and len(path) >= min_len:
                valid.append(path)
                return
            elif nxt not in path:
                rev = curr[1:] if curr.startswith('-') else ('-' + curr)
                if nxt != rev:
                    dfs(nxt, path + [nxt])
    dfs(start_edge, [start_edge])
    return valid[0] if valid else None

# Build a comprehensive list of routes covering all available road edges
edge_circuits = []
for edge in sorted(list(all_edges)):
    c = find_forward_circuit_from(edge)
    if c:
        edge_circuits.append(c)

print(f"Generated {len(edge_circuits)} distinct forward circuits.")

output_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>\n',
    '<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">\n',
    f'    <vType id="bus" vClass="bus" accel="1.2" decel="3.5" length="9.5" minGap="{MIN_GAP}" maxSpeed="11.0" tau="1.6"/>\n',
    f'    <vType id="passenger" vClass="passenger" accel="2.2" decel="4.0" length="4.5" minGap="{MIN_GAP}" maxSpeed="14.0" tau="1.6"/>\n\n'
]

# Create vehicle list: 20 buses + 100 cars evenly interleaved
vehicle_types = []
# 1 bus every 5 cars (20 buses + 100 cars = 120 total)
for b in range(NUM_BUSES):
    vehicle_types.append("bus")
    for c in range(5):
        vehicle_types.append("passenger")

print(f"Total fleet size: {len(vehicle_types)} ({vehicle_types.count('bus')} buses, {vehicle_types.count('passenger')} cars)")

# Assign each vehicle to a perpetual loop
for vid, vtype in enumerate(vehicle_types):
    circuit = edge_circuits[vid % len(edge_circuits)]
    loop_edges = " ".join(circuit * 50)
    output_lines.append(f'    <vehicle id="{vid}" type="{vtype}" depart="0.00">\n')
    output_lines.append(f'        <route edges="{loop_edges}"/>\n')
    output_lines.append(f'    </vehicle>\n')

output_lines.append('</routes>\n')

rou_path = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.rou.xml"
with open(rou_path, "w", encoding="utf-8") as f:
    f.writelines(output_lines)

print(f"Successfully generated {TOTAL_VEHICLES} vehicles (20 buses + 100 cars) across all city circuits!")
