import xml.etree.ElementTree as ET

net_path = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"
tree = ET.parse(net_path)
root = tree.getroot()

tl_logics = root.findall('tlLogic')
print(f"Found {len(tl_logics)} tlLogic elements:")
for tl in tl_logics:
    tl_id = tl.get('id')
    tl_type = tl.get('type')
    program_id = tl.get('programID')
    phases = tl.findall('phase')
    print(f"TL ID: {tl_id}, type: {tl_type}, program: {program_id}, num_phases: {len(phases)}")
    for p in phases:
        print(f"  duration: {p.get('duration')}, state: {p.get('state')}")

print("\nJunctions with type='traffic_light':")
for j in root.findall('junction'):
    if j.get('type') == 'traffic_light':
        print(f"Junction ID: {j.get('id')}, type: {j.get('type')}, x: {j.get('x')}, y: {j.get('y')}")
