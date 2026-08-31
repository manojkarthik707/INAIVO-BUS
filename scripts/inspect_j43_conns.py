import xml.etree.ElementTree as ET

NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"
tree = ET.parse(NET_PATH)
root = tree.getroot()

for c in root.findall('connection'):
    f = c.get('from', '')
    t = c.get('to', '')
    via = c.get('via', '')
    if '43' in via or f in ['5', '-5', '6', '-6', 'shortcut_east', 'shortcut_west'] and t in ['5', '-5', '6', '-6', 'shortcut_east', 'shortcut_west']:
        print(f"Conn: from {f}_{c.get('fromLane')} -> to {t}_{c.get('toLane')} via {via} dir={c.get('dir')} state={c.get('state')}")
