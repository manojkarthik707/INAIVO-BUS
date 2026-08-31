import xml.etree.ElementTree as ET

tree = ET.parse(r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml")
root = tree.getroot()

for tl_id in ['25', '26', '27']:
    print(f"\n--- TL {tl_id} CONNECTIONS & LINK INDICES ---")
    for conn in root.findall('connection'):
        if conn.get('tl') == tl_id:
            f = conn.get('from')
            fl = conn.get('fromLane')
            t = conn.get('to')
            tl_lane = conn.get('toLane')
            idx = conn.get('linkIndex')
            d = conn.get('dir')
            print(f"linkIndex={idx}: from {f}_{fl} -> to {t}_{tl_lane} (dir: {d})")
