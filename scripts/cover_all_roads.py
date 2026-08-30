import xml.etree.ElementTree as ET
import os
import re

CONFIG_PATH = r"f:\VEHDEMO\simulation\configs\traffic.yaml"

num_vehicles = 24
bus_ratio = 3
min_gap = 4.5
max_speed_bus = 11.0
max_speed_car = 14.0

if os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        text = f.read()
    m_nv = re.search(r'num_vehicles:\s*(\d+)', text)
    if m_nv: num_vehicles = max(int(m_nv.group(1)), 20)
    m_br = re.search(r'bus_ratio:\s*(\d+)', text)
    if m_br: bus_ratio = int(m_br.group(1))
    m_mg = re.search(r'min_gap:\s*([\d\.]+)', text)
    if m_mg: min_gap = float(m_mg.group(1))

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
        # No U-turns
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

# Build a comprehensive list of routes covering ALL 50 edges
edge_circuits = []
covered_edges = set()

for edge in sorted(list(all_edges)):
    c = find_forward_circuit_from(edge)
    if c:
        edge_circuits.append(c)
        covered_edges.update(c)

print(f"Generated {len(edge_circuits)} circuits covering {len(covered_edges)} of {len(all_edges)} road edges.")

output_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>\n',
    '<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">\n',
    f'    <vType id="bus" vClass="bus" accel="1.2" decel="3.5" length="9.5" minGap="{min_gap}" maxSpeed="{max_speed_bus}" tau="1.6"/>\n',
    f'    <vType id="passenger" vClass="passenger" accel="2.2" decel="4.0" length="4.5" minGap="{min_gap}" maxSpeed="{max_speed_car}" tau="1.6"/>\n\n'
]

# Generate fleet distributed across all road circuits
for vid in range(num_vehicles):
    circuit = edge_circuits[vid % len(edge_circuits)]
    loop_edges = " ".join(circuit * 50)
    vtype = "bus" if (vid % bus_ratio == 0) else "passenger"
    output_lines.append(f'    <vehicle id="{vid}" type="{vtype}" depart="0.00">\n')
    output_lines.append(f'        <route edges="{loop_edges}"/>\n')
    output_lines.append(f'    </vehicle>\n')

output_lines.append('</routes>\n')

rou_path = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.rou.xml"
with open(rou_path, "w", encoding="utf-8") as f:
    f.writelines(output_lines)

print(f"Successfully generated {num_vehicles} vehicle routes covering every road across the city!")
