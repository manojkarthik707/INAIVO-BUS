import xml.etree.ElementTree as ET

NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"

tree = ET.parse(NET_PATH)
root = tree.getroot()

# 1. For 4-way Junctions 25, 26, 27: Smart Actuated Adaptive Controllers
for tl in root.findall('tlLogic'):
    tl_id = tl.get('id')
    if tl_id in ['25', '26', '27']:
        tl.set('type', 'actuated')
        tl.set('programID', 'smart_actuated')
        for p in tl.findall('phase'):
            dur = p.get('duration')
            if dur == '42':
                p.set('duration', '14')
                p.set('minDur', '4')
                p.set('maxDur', '24')
            elif dur == '3':
                p.set('duration', '2')
    elif tl_id in ['41', '43', '44', '45']:
        tl.set('type', 'static')
        for p in list(tl.findall('phase')):
            tl.remove(p)
        p = ET.SubElement(tl, 'phase')
        p.set('duration', '99999')
        p.set('state', 'GGgGGg')

tree.write(NET_PATH, encoding='utf-8', xml_declaration=True)
print("Configured smart actuated adaptive lights onto mathematically smooth netconvert road network.")
