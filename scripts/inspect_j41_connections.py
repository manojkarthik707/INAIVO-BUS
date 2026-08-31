import xml.etree.ElementTree as ET

NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"
tree = ET.parse(NET_PATH)
root = tree.getroot()

print("=== JUNCTION 41 CONNECTIONS ===")
for conn in root.findall('connection'):
    if conn.get('tl') == '41' or conn.get('from') in ['8', '-8', '23', '-23'] or conn.get('to') in ['8', '-8', '23', '-23']:
        f = conn.get('from')
        t = conn.get('to')
        from_lane = conn.get('fromLane')
        to_lane = conn.get('toLane')
        tl = conn.get('tl')
        link_idx = conn.get('linkIndex')
        dir_ = conn.get('dir')
        state = conn.get('state')
        print(f"Conn from {f}_{from_lane} -> to {t}_{to_lane} | dir={dir_} tl={tl} linkIndex={link_idx} state={state}")

print("\n=== TL LOGIC FOR 41 ===")
for tl in root.findall('tlLogic'):
    if tl.get('id') == '41':
        print(ET.tostring(tl, encoding='unicode'))
