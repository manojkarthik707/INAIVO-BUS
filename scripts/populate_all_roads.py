import xml.etree.ElementTree as ET

tree = ET.parse(r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml")
root = tree.getroot()

connections = {}
for conn in root.findall('connection'):
    f = conn.get('from')
    t = conn.get('to')
    if f and t and not f.startswith(':') and not t.startswith(':'):
        connections.setdefault(f, set()).add(t)

grand_circuits = [
    # 1. Grand Outer Perimeter Highway (Top Highway 15, East 18/-21/-22, West -0/1/-2/3/-4, Midtown 17/16)
    ["16", "-19", "15", "-15", "19", "-16", "12", "18", "-21", "-22", "-24", "-0", "1", "-2", "3", "-4", "-10", "17"],
    
    # 2. Grand Southern Highway & Top Highway Combo (Covers South 13/-13, 11, 14, 20, East 21/22, North 15)
    ["20", "14", "11", "13", "-13", "-11", "-14", "-20", "12", "18", "-21", "-22", "-24", "7", "6", "5", "-10", "17", "16", "-19", "15", "-15", "19", "-16"],
    
    # 3. Full North-South & East Outer Circuit
    ["-16", "12", "18", "-21", "-22", "-24", "23", "-8", "9", "-10", "17", "16", "-19", "15", "-15", "19"],
    
    # 4. South Highway + West Ring
    ["-0", "1", "-2", "3", "-4", "-10", "17", "20", "14", "11", "13", "-13", "-11", "-14", "-20", "12", "18", "-21", "-22", "-24"],
    
    # 5. East Coastline Highway
    ["18", "-21", "-22", "-24", "7", "6", "5", "-10", "17", "12"],
    
    # 6. Central Business District & Inner Rings
    ["-10", "17", "12", "18", "-21", "-22", "-24", "23", "-8", "9"],
    
    # 7. Midtown Boulevard Loop
    ["-12", "-17", "10", "-5", "-6", "-7", "24", "22", "21", "-18"],
    
    # 8. South-West Scenic Ring
    ["-23", "7", "6", "5", "-9", "8"],
    
    # 9. North-West Parkway
    ["-0", "1", "-2", "3", "-4", "-9", "8", "-23"],
    
    # 10. Central Commercial Crossing
    ["-5", "-6", "-7", "23", "-8", "9"]
]

# Verify all transitions
errors = 0
for i, c in enumerate(grand_circuits):
    for j in range(len(c)):
        curr = c[j]
        nxt = c[(j + 1) % len(c)]
        if nxt not in connections.get(curr, set()):
            print(f"ERROR: Circuit {i+1} invalid transition {curr} -> {nxt}")
            errors += 1

if errors == 0:
    print("ALL 10 CIRCUITS ARE 100% VALID!")
else:
    raise RuntimeError(f"Found {errors} errors in circuits!")

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
    circuit = grand_circuits[vid % len(grand_circuits)]
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

print(f"Successfully generated {TOTAL_VEHICLES} vehicles with heavy outer highway traffic!")
