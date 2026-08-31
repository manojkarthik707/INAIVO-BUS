import xml.etree.ElementTree as ET

NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"
tree = ET.parse(NET_PATH)
root = tree.getroot()

print("=== JUNCTION 41 CONNECTIONS ===")
for c in root.findall('connection'):
    f = c.get('from', '')
    t = c.get('to', '')
    if 'shortcut' in f or 'shortcut' in t or f in ['23', '8', '-23', '-8']:
        print(f"From {f}_{c.get('fromLane')} -> To {t}_{c.get('toLane')} dir={c.get('dir')} state={c.get('state')} pass={c.get('pass')}")

print("\n=== JUNCTION 43 CONNECTIONS ===")
for c in root.findall('connection'):
    f = c.get('from', '')
    t = c.get('to', '')
    if 'shortcut' in f or 'shortcut' in t or f in ['5', '-5', '6', '-6']:
        print(f"From {f}_{c.get('fromLane')} -> To {t}_{c.get('toLane')} dir={c.get('dir')} state={c.get('state')} pass={c.get('pass')}")
