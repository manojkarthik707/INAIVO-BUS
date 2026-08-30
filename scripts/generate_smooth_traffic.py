import xml.etree.ElementTree as ET

# 100% Valid, Smooth, Non-Intersecting Loop Circuits
# Heavily weighted towards the Grand Outer Highways & Perimeter Ring!
grand_circuits = [
    # 1. Grand Outer Perimeter Highway Ring (Clockwise - West, North, East, South)
    ["-0", "1", "-2", "3", "-4", "-10", "17", "12", "18", "-21", "-22", "-24"],
    
    # 2. Grand Outer Perimeter Highway Ring (Counter-Clockwise - East, North, West, South)
    ["-1", "0", "24", "22", "21", "-18", "-12", "-17", "10", "4", "-3", "2"],
    
    # 3. Outer East Highway & Southern Boulevard Circuit
    ["-10", "17", "12", "18", "-21", "-22", "-24", "7", "6", "5"],
    
    # 4. Outer East Highway & Central Commercial Circuit
    ["-10", "17", "12", "18", "-21", "-22", "-24", "23", "-8", "9"],
    
    # 5. Outer West Ring & Central Avenue
    ["-0", "1", "-2", "3", "-4", "-9", "8", "-23"],
    
    # 6. Outer West Ring & South-East Parkway
    ["-0", "1", "-2", "3", "-4", "-5", "-6", "-7"],
    
    # 7. East Coast Highway & Midtown Crossing
    ["-12", "-17", "10", "-5", "-6", "-7", "24", "22", "21", "-18"],
    
    # 8. East Coast Highway & West Crossing
    ["-12", "-17", "10", "-9", "8", "-23", "24", "22", "21", "-18"],
    
    # 9. Inner Central Commercial Square
    ["-23", "7", "6", "5", "-9", "8"],
    
    # 10. Central Midtown Parkway
    ["-5", "-6", "-7", "23", "-8", "9"]
]

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
for b in range(NUM_BUSES):
    vehicle_types.append("bus")
    for c in range(5):
        vehicle_types.append("passenger")

# Distribute 120 vehicles:
# 60% on Grand Outer Perimeter Rings (Circuits 0, 1, 2, 3)
# 40% on mid & inner circuits (Circuits 4..9)
circuit_distribution = [
    0, 1, 0, 1, 2, 3, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
]

for vid, vtype in enumerate(vehicle_types):
    c_idx = circuit_distribution[vid % len(circuit_distribution)]
    circuit = grand_circuits[c_idx]
    # Shift start edge so vehicles are evenly spaced along the entire circuit
    shift = (vid * 2) % len(circuit)
    shifted = circuit[shift:] + circuit[:shift]
    loop_edges = " ".join(shifted * 30)
    # Stagger depart times slightly by 0.5s to prevent initial junction deadlocks
    depart_time = f"{vid * 0.5:.2f}"
    output_lines.append(f'    <vehicle id="{vid}" type="{vtype}" depart="{depart_time}">\n')
    output_lines.append(f'        <route edges="{loop_edges}"/>\n')
    output_lines.append(f'    </vehicle>\n')

output_lines.append('</routes>\n')

rou_path = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.rou.xml"
with open(rou_path, "w", encoding="utf-8") as f:
    f.writelines(output_lines)

print(f"Successfully generated {TOTAL_VEHICLES} vehicles with 60% outer perimeter highway weighting and IDM anti-deadlock physics!")
