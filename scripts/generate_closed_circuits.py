import xml.etree.ElementTree as ET
import random

# Load net to get valid closed circuits
net_tree = ET.parse(r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml")
net_root = net_tree.getroot()

connections = {}
for conn in net_root.findall('connection'):
    f = conn.get('from')
    t = conn.get('to')
    if f and t and not f.startswith(':') and not t.startswith(':'):
        connections.setdefault(f, set()).add(t)

def find_closed_circuits(min_len=6, max_len=12):
    valid_circuits = []
    def dfs(start, current_path):
        if len(current_path) >= max_len:
            return
        curr = current_path[-1]
        for nxt in connections.get(curr, []):
            if nxt == start:
                if len(current_path) >= min_len:
                    valid_circuits.append(current_path)
            elif nxt not in current_path:
                dfs(start, current_path + [nxt])

    for edge in connections.keys():
        dfs(edge, [edge])
    
    unique = []
    seen = set()
    for c in valid_circuits:
        min_i = c.index(min(c))
        norm = tuple(c[min_i:] + c[:min_i])
        if norm not in seen:
            seen.add(norm)
            unique.append(c)
    return unique

circuits = find_closed_circuits(6, 12)
print(f"Generated {len(circuits)} unique closed circuits.")

# Create sumo.rou.xml with continuous looping closed circuits
output_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>\n',
    '<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">\n',
    '    <vType id="bus" vClass="bus" accel="1.5" decel="3.0" length="9.5" minGap="2.5" maxSpeed="15.0"/>\n',
    '    <vType id="passenger" vClass="passenger" accel="2.6" decel="4.5" length="4.5" minGap="2.5" maxSpeed="20.0"/>\n\n'
]

# Generate 500 active vehicles on closed circuits with staggered departures
for vid in range(500):
    c = circuits[vid % len(circuits)]
    # Repeat the circuit 30 times so the vehicle drives continuously for hours
    loop_edges = " ".join(c * 30)
    vtype = "bus" if vid % 4 == 0 else "passenger"
    depart_time = round(vid * 1.5, 2)
    output_lines.append(f'    <vehicle id="{vid}" type="{vtype}" depart="{depart_time:.2f}">\n')
    output_lines.append(f'        <route edges="{loop_edges}"/>\n')
    output_lines.append(f'    </vehicle>\n')

output_lines.append('</routes>\n')

with open(r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.rou.xml", "w", encoding="utf-8") as f:
    f.writelines(output_lines)

print("Successfully converted all routes in sumo.rou.xml into continuous closed circuits!")
