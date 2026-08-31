import xml.etree.ElementTree as ET

ROU_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.rou.xml"

tree = ET.parse(ROU_PATH)
root = tree.getroot()

veh_ids = [v.get('id') for v in root.findall('vehicle')]
print(f"Total vehicles in sumo.rou.xml: {len(veh_ids)}")

INDIAN_STATES = ["TN", "KA", "MH", "DL", "TS", "GJ", "KL", "AP", "WB", "HR"]
SERIES = ["AB", "CD", "EF", "GH", "JK", "LM", "NP", "QR", "ST", "UV", "WX", "YZ"]

def generate_plate_for_id(veh_id, global_idx):
    state = INDIAN_STATES[global_idx % len(INDIAN_STATES)]
    rto = f"{(global_idx * 3 + 1) % 99 + 1:02d}"
    series = SERIES[(global_idx // len(INDIAN_STATES)) % len(SERIES)]
    num = f"{(global_idx * 127 + 1001) % 9000 + 1000:04d}"
    return f"{state} {rto} {series} {num}"

assigned_plates = {}
for idx, v_id in enumerate(veh_ids):
    plate = generate_plate_for_id(v_id, idx)
    assigned_plates[v_id] = plate

# Verify 100% uniqueness
unique_set = set(assigned_plates.values())
print(f"Unique plates count: {len(unique_set)} / {len(veh_ids)}")
assert len(unique_set) == len(veh_ids), "Duplicate license plates detected!"

print("\nSample Assigned Number Plates across Fleet:")
for v_id in veh_ids[:15]:
    print(f"  Vehicle '{v_id:15s}' -> {assigned_plates[v_id]}")
for v_id in veh_ids[-10:]:
    print(f"  Vehicle '{v_id:15s}' -> {assigned_plates[v_id]}")
