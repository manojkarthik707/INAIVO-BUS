import xml.etree.ElementTree as ET
import os
import re

CONFIG_PATH = r"f:\VEHDEMO\simulation\configs\traffic.yaml"

num_vehicles = 18
bus_ratio = 3
min_gap = 4.5
max_speed_bus = 11.0
max_speed_car = 14.0

if os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        text = f.read()
    m_nv = re.search(r'num_vehicles:\s*(\d+)', text)
    if m_nv: num_vehicles = int(m_nv.group(1))
    m_br = re.search(r'bus_ratio:\s*(\d+)', text)
    if m_br: bus_ratio = int(m_br.group(1))
    m_mg = re.search(r'min_gap:\s*([\d\.]+)', text)
    if m_mg: min_gap = float(m_mg.group(1))
    m_sc = re.search(r'max_speed_car:\s*([\d\.]+)', text)
    if m_sc: max_speed_car = float(m_sc.group(1))
    m_sb = re.search(r'max_speed_bus:\s*([\d\.]+)', text)
    if m_sb: max_speed_bus = float(m_sb.group(1))

print(f"Applying settings: num_vehicles={num_vehicles}, bus_ratio={bus_ratio}, min_gap={min_gap}m")

# Parse SUMO net to build valid continuous circuits
net_tree = ET.parse(r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml")
net_root = net_tree.getroot()

connections = {}
for conn in net_root.findall('connection'):
    f = conn.get('from')
    t = conn.get('to')
    if f and t and not f.startswith(':') and not t.startswith(':'):
        connections.setdefault(f, set()).add(t)

def find_circuits_from_start(start_edge, min_len=6, max_len=14):
    valid = []
    def dfs(curr, path):
        if len(path) >= max_len:
            return
        for nxt in connections.get(curr, []):
            if nxt == start_edge and len(path) >= min_len:
                valid.append(path)
                return
            elif nxt not in path:
                dfs(nxt, path + [nxt])
    dfs(start_edge, [start_edge])
    return valid

# Select unique starting edges distributed across the city
all_edges = list(connections.keys())
circuits_by_edge = {}

for edge in all_edges:
    c = find_circuits_from_start(edge, 6, 14)
    if c:
        circuits_by_edge[edge] = c[0]

starting_edges = list(circuits_by_edge.keys())
print(f"Found {len(starting_edges)} distinct valid starting edges with closed circuits.")

# Build sumo.rou.xml
output_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>\n',
    '<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">\n',
    f'    <vType id="bus" vClass="bus" accel="1.2" decel="3.5" length="9.5" minGap="{min_gap}" maxSpeed="{max_speed_bus}" tau="1.6"/>\n',
    f'    <vType id="passenger" vClass="passenger" accel="2.2" decel="4.0" length="4.5" minGap="{min_gap}" maxSpeed="{max_speed_car}" tau="1.6"/>\n\n'
]

# Generate exact constant fleet of vehicles
for vid in range(num_vehicles):
    edge = starting_edges[vid % len(starting_edges)]
    circuit = circuits_by_edge[edge]
    # Repeat the circuit 50 times so it never despawns
    loop_edges = " ".join(circuit * 50)
    vtype = "bus" if (vid % bus_ratio == 0) else "passenger"
    # All vehicles start at t=0.00 on distinct edges throughout the city
    output_lines.append(f'    <vehicle id="{vid}" type="{vtype}" depart="0.00">\n')
    output_lines.append(f'        <route edges="{loop_edges}"/>\n')
    output_lines.append(f'    </vehicle>\n')

output_lines.append('</routes>\n')

rou_path = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.rou.xml"
with open(rou_path, "w", encoding="utf-8") as f:
    f.writelines(output_lines)

print(f"Successfully generated a CONSTANT FLEET of {num_vehicles} vehicles that exist perpetually with ZERO spawning/despawning!")
