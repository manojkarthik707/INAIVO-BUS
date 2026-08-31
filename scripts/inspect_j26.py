import xml.etree.ElementTree as ET

tree = ET.parse(r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml")
root = tree.getroot()

print("--- JUNCTION 26 CONNECTIONS ---")
for conn in root.findall('connection'):
    tl = conn.get('tl', '')
    via = conn.get('via', '')
    if tl == '26' or ':26' in via:
        f = conn.get('from')
        fl = conn.get('fromLane')
        t = conn.get('to')
        tl_lane = conn.get('toLane')
        d = conn.get('dir')
        print(f"from {f}_{fl} -> to {t}_{tl_lane} (dir: {d}, via: {via})")

print("\n--- JUNCTION 25 CONNECTIONS ---")
for conn in root.findall('connection'):
    tl = conn.get('tl', '')
    via = conn.get('via', '')
    if tl == '25' or ':25' in via:
        f = conn.get('from')
        fl = conn.get('fromLane')
        t = conn.get('to')
        tl_lane = conn.get('toLane')
        d = conn.get('dir')
        print(f"from {f}_{fl} -> to {t}_{tl_lane} (dir: {d}, via: {via})")
