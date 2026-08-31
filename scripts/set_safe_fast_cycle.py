import xml.etree.ElementTree as ET

NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"

tree = ET.parse(NET_PATH)
root = tree.getroot()

# Update lane speed limits to 20.0 m/s (72 km/h)
for lane in root.findall('.//lane'):
    lane.set('speed', '20.0')

# Safe, fast 28s cycle: 5s Green + 2s Yellow per stage
for tl in root.findall('tlLogic'):
    tl_id = tl.get('id')
    if tl_id in ['25', '26', '27']:
        for p in tl.findall('phase'):
            dur = p.get('duration')
            if dur in ['4', '8', '14']:
                p.set('duration', '5')
            elif dur in ['1', '2', '3']:
                p.set('duration', '2')

tree.write(NET_PATH, encoding='utf-8', xml_declaration=True)
print(f"Set 20 m/s speed limits and 28s safe synchronized cycle in {NET_PATH}")
