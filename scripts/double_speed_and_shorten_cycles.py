import xml.etree.ElementTree as ET

NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"

tree = ET.parse(NET_PATH)
root = tree.getroot()

# 1. Double the speed limit on all lanes from 13.89 m/s (50 km/h) to 27.78 m/s (100 km/h)
for lane in root.findall('.//lane'):
    lane.set('speed', '27.78')

# 2. Shorten traffic light stages to fast snappy 4s Green + 1s Yellow (20s total cycle)
for tl in root.findall('tlLogic'):
    tl_id = tl.get('id')
    if tl_id in ['25', '26', '27']:
        for p in tl.findall('phase'):
            dur = p.get('duration')
            if dur in ['8', '14']:
                p.set('duration', '4')
                p.set('minDur', '2')
                p.set('maxDur', '8')
            elif dur in ['2', '3']:
                p.set('duration', '1')

tree.write(NET_PATH, encoding='utf-8', xml_declaration=True)
print(f"Doubled speed limits to 100 km/h and reduced stage cycle to 20s in {NET_PATH}")
