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

# Parse SUMO net to build forward-only, NO U-TURN circuits
net_tree = ET.parse(r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml")
net_root = net_tree.getroot()

clean_connections = {}
for conn in net_root.findall('connection'):
    f = conn.get('from')
    t = conn.get('to')
    d = conn.get('dir')
    if f and t and not f.startswith(':') and not t.startswith(':'):
        rev = f[1:] if f.startswith('-') else ('-' + f)
        # STRICT NO U-TURNS: never allow immediate reverse or turnaround direction
        if t != rev and d != 't':
            clean_connections.setdefault(f, set()).add(t)

def find_forward_circuits(min_len=6, max_len=14):
    valid = []
    def dfs(start, path):
        if len(path) >= max_len:
            return
        curr = path[-1]
        for nxt in clean_connections.get(curr, []):
            if nxt == start:
                if len(path) >= min_len:
                    valid.append(path)
            elif nxt not in path:
                rev = curr[1:] if curr.startswith('-') else ('-' + curr)
                if nxt != rev:
                    dfs(start, path + [nxt])

    for edge in clean_connections.keys():
        dfs(edge, [edge])
    
    unique = []
    seen = set()
    for c in valid:
        min_i = c.index(min(c))
        norm = tuple(c[min_i:] + c[:min_i])
        if norm not in seen:
            seen.add(norm)
            unique.append(c)
    return unique

smooth_circuits = find_forward_circuits(6, 14)
print(f"Found {len(smooth_circuits)} smooth, NO-U-TURN closed city circuits!")

if not smooth_circuits:
    raise RuntimeError("No smooth circuits found!")

# Build sumo.rou.xml
output_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>\n',
    '<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">\n',
    f'    <vType id="bus" vClass="bus" accel="1.2" decel="3.5" length="9.5" minGap="{min_gap}" maxSpeed="{max_speed_bus}" tau="1.6"/>\n',
    f'    <vType id="passenger" vClass="passenger" accel="2.2" decel="4.0" length="4.5" minGap="{min_gap}" maxSpeed="{max_speed_car}" tau="1.6"/>\n\n'
]

# Assign each vehicle in the fleet to a smooth continuous circuit without any U-turns
for vid in range(num_vehicles):
    circuit = smooth_circuits[vid % len(smooth_circuits)]
    # Repeat the smooth forward circuit 50 times
    loop_edges = " ".join(circuit * 50)
    vtype = "bus" if (vid % bus_ratio == 0) else "passenger"
    # All vehicles start at t=0.00 distributed smoothly across different circuits
    output_lines.append(f'    <vehicle id="{vid}" type="{vtype}" depart="0.00">\n')
    output_lines.append(f'        <route edges="{loop_edges}"/>\n')
    output_lines.append(f'    </vehicle>\n')

output_lines.append('</routes>\n')

rou_path = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.rou.xml"
with open(rou_path, "w", encoding="utf-8") as f:
    f.writelines(output_lines)

print(f"Successfully configured {num_vehicles} vehicles on smooth forward-flowing closed circuits with ZERO U-TURNS!")
