import xml.etree.ElementTree as ET

tree = ET.parse(r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml")
root = tree.getroot()

for e in root.findall('edge'):
    eid = e.get('id', '')
    if eid in ['15', '-15', '13', '-13', '19', '-19', '16', '-16']:
        lane = e.find('lane')
        shape = lane.get('shape') if lane is not None else ''
        print(f"Edge {eid}: from={e.get('from')} to={e.get('to')} shape={shape[:50]}...")
