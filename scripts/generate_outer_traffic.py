import xml.etree.ElementTree as ET
import subprocess

tree = ET.parse(r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml")
root = tree.getroot()

connections = {}
for conn in root.findall('connection'):
    f = conn.get('from')
    t = conn.get('to')
    if f and t and not f.startswith(':') and not t.startswith(':'):
        connections.setdefault(f, set()).add(t)

# Define flawless outer & inner circuits
grand_circuits = [
    # 1. Grand Outer Perimeter Highway (Clockwise: Top 15 -> Outer West -> Bottom -13 -> East 18/-21/-22 -> Midtown 17/16)
    ["16", "-19", "15", "outer_west", "-13", "-11", "-14", "-20", "12", "18", "-21", "-22", "-24", "7", "6", "5", "-10", "17"],
    
    # 2. Grand Outer Perimeter Highway (Counter-Clockwise: Bottom 13 -> Outer West -> Top -15 -> East 18/-21/-22 -> West -0/1/-2/3/-4)
    ["20", "14", "11", "13", "-outer_west", "-15", "19", "-16", "12", "18", "-21", "-22", "-24", "-0", "1", "-2", "3", "-4", "-10", "17"],
    
    # 3. Outer West Ring & Outer Top Loop
    ["16", "-19", "15", "outer_west", "-13", "-11", "-14", "-20", "12", "18", "-21", "-22", "-24", "23", "-8", "9", "-10", "17"],
    
    # 4. Outer West Ring & Outer Bottom Loop
    ["-0", "1", "-2", "3", "-4", "-10", "17", "16", "-19", "15", "outer_west", "-13", "-11", "-14", "-20", "12", "18", "-21", "-22", "-24"],
    
    # 5. Inner-Outer Figure-8 Ring
    ["-10", "17", "12", "18", "-21", "-22", "-24", "23", "-8", "9", "-10", "17", "16", "-19", "15", "outer_west", "-13", "-11", "-14", "-20", "12", "18", "-21", "-22", "-24", "7", "6", "5"],
    
    # 6. Outer East Coastline Highway & Central Square
    ["-10", "17", "12", "18", "-21", "-22", "-24", "7", "6", "5"],
    
    # 7. West Avenue & Midtown Loop
    ["-0", "1", "-2", "3", "-4", "-10", "17", "12", "18", "-21", "-22", "-24"],
    
    # 8. North-West Parkway & Central Avenue
    ["-0", "1", "-2", "3", "-4", "-9", "8", "-23"],
    
    # 9. Midtown Boulevard & Commercial Crossing
    ["-12", "-17", "10", "-5", "-6", "-7", "24", "22", "21", "-18"],
    
    # 10. Central Commercial Square
    ["-23", "7", "6", "5", "-9", "8"]
]

# Verify all transitions in all circuits
for i, c in enumerate(grand_circuits):
    for j in range(len(c)):
        curr = c[j]
        nxt = c[(j + 1) % len(c)]
        if nxt not in connections.get(curr, set()):
            print(f"ERROR: Circuit {i+1} invalid transition {curr} -> {nxt}")

print("Circuit validation complete.")

NUM_BUSES = 20
NUM_CARS = 100
TOTAL_VEHICLES = NUM_BUSES + NUM_CARS

output_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>\n',
    '<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">\n',
    '    <!-- Intelligent Driver Model (IDM) for smooth non-deadlocking traffic flow -->\n',
    '    <vType id="bus" vClass="bus" carFollowModel="IDM" accel="1.5" decel="3.5" length="9.5" minGap="3.5" maxSpeed="11.0" tau="1.2"/>\n',
    '    <vType id="passenger" vClass="passenger" carFollowModel="IDM" accel="2.5" decel="4.5" length="4.5" minGap="3.0" maxSpeed="15.0" tau="1.1"/>\n\n'
]

vehicle_types = []
        vehicle_types.append("passenger")

# 80% assigned to outer highway circuits!
circuit_weights = [
    0, 1, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
]

for vid, vtype in enumerate(vehicle_types):
    c_idx = circuit_weights[vid % len(circuit_weights)]
    circuit = grand_circuits[c_idx]
    shift = (vid * 2) % len(circuit)
    shifted = circuit[shift:] + circuit[:shift]
    loop_edges = " ".join(shifted * 30)
    depart_time = f"{vid * 0.4:.2f}"
    output_lines.append(f'    <vehicle id="{vid}" type="{vtype}" depart="{depart_time}">\n')
    output_lines.append(f'        <route edges="{loop_edges}"/>\n')
    output_lines.append(f'    </vehicle>\n')

output_lines.append('</routes>\n')

rou_path = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.rou.xml"
with open(rou_path, "w", encoding="utf-8") as f:
    f.writelines(output_lines)

print("Routes successfully written!")
