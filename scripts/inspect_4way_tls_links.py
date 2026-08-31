import xml.etree.ElementTree as ET

NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"
tree = ET.parse(NET_PATH)
root = tree.getroot()

for tl in root.findall('tlLogic'):
    tl_id = tl.get('id')
    if tl_id in ['25', '26', '27']:
        print(f"\n=== TLS {tl_id} ===")
        conns = []
        for c in root.findall('connection'):
            if c.get('tl') == tl_id:
                conns.append((int(c.get('linkIndex', 0)), c.get('from'), c.get('to'), c.get('fromLane'), c.get('toLane'), c.get('dir'), c.get('state')))
        conns.sort(key=lambda x: x[0])
        for idx, f, t, fL, tL, d, s in conns:
            print(f"  Link {idx:2d}: from {f}_{fL} -> {t}_{tL} dir={d} (state={s})")
