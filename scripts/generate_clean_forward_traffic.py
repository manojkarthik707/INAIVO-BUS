import xml.etree.ElementTree as ET

tree = ET.parse(r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml")
root = tree.getroot()

clean_connections = {}
for conn in root.findall('connection'):
    f = conn.get('from')
    t = conn.get('to')
    d = conn.get('dir')
    if f and t and not f.startswith(':') and not t.startswith(':'):
        rev = f[1:] if f.startswith('-') else ('-' + f)
        # STRICT NO U-TURNS: forbid reverse edge and turnaround direction
        if t != rev and d != 't':
            clean_connections.setdefault(f, set()).add(t)

# Find natural forward loops covering ALL available road edges without ANY U-turns
def find_pure_forward_circuits():
    circuits = []
    def dfs(start, path, max_len=16):
        if len(path) >= max_len:
            return
        curr = path[-1]
        for nxt in clean_connections.get(curr, []):
            if nxt == start and len(path) >= 6:
                circuits.append(path)
            elif nxt not in path:
                rev = curr[1:] if curr.startswith('-') else ('-' + curr)
                if nxt != rev:
                    dfs(start, path + [nxt], max_len)

    for edge in clean_connections.keys():
        dfs(edge, [edge], 16)

    # Deduplicate
    unique = []
    seen = set()
    for c in circuits:
        min_i = c.index(min(c))
        norm = tuple(c[min_i:] + c[:min_i])
        if norm not in seen:
            seen.add(norm)
            unique.append(c)
    return unique

forward_circuits = find_pure_forward_circuits()
print(f"Found {len(forward_circuits)} PURE FORWARD NO-U-TURN circuits:")
for i, c in enumerate(forward_circuits):
    print(f"Circuit {i+1} (len {len(c)}): {' '.join(c)}")

NUM_BUSES = 20
NUM_CARS = 100
TOTAL_VEHICLES = NUM_BUSES + NUM_CARS
MIN_GAP = 4.5

output_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>\n',
    '<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">\n',
    f'    <vType id="bus" vClass="bus" accel="1.2" decel="3.5" length="9.5" minGap="{MIN_GAP}" maxSpeed="11.0" tau="1.6"/>\n',
    f'    <vType id="passenger" vClass="passenger" accel="2.2" decel="4.0" length="4.5" minGap="{MIN_GAP}" maxSpeed="14.0" tau="1.6"/>\n\n'
]

vehicle_types = []
for b in range(NUM_BUSES):
    vehicle_types.append("bus")
    for c in range(5):
        vehicle_types.append("passenger")

for vid, vtype in enumerate(vehicle_types):
    circuit = forward_circuits[vid % len(forward_circuits)]
    shift = (vid * 3) % len(circuit)
    shifted_circuit = circuit[shift:] + circuit[:shift]
    loop_edges = " ".join(shifted_circuit * 40)
    output_lines.append(f'    <vehicle id="{vid}" type="{vtype}" depart="0.00">\n')
    output_lines.append(f'        <route edges="{loop_edges}"/>\n')
    output_lines.append(f'    </vehicle>\n')

output_lines.append('</routes>\n')

rou_path = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.rou.xml"
with open(rou_path, "w", encoding="utf-8") as f:
    f.writelines(output_lines)

print(f"Successfully generated {TOTAL_VEHICLES} vehicles on 100% forward circuits with ZERO U-TURNS!")
