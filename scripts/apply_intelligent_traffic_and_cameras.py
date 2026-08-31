import xml.etree.ElementTree as ET

NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"
tree = ET.parse(NET_PATH)
root = tree.getroot()

# For T-junctions 41, 43, 44, 45: Make them uninterrupted green priority links (never stop traffic)
for tl_id in ['41', '43', '44', '45']:
    existing = [tl for tl in root.findall('tlLogic') if tl.get('id') == tl_id]
    if not existing:
        tl = ET.SubElement(root, 'tlLogic')
        tl.set('id', tl_id)
        tl.set('type', 'static')
        tl.set('programID', '0')
        tl.set('offset', '0')
        p = ET.SubElement(tl, 'phase')
        p.set('duration', '99999')
        p.set('state', 'GGGGGG')
    else:
        tl = existing[0]
        tl.set('type', 'static')
        for p in list(tl.findall('phase')):
            tl.remove(p)
        p = ET.SubElement(tl, 'phase')
        p.set('duration', '99999')
        p.set('state', 'GGGGGG')

# For 4-way Junctions 25, 26, 27: Make them Intelligent Actuated Adaptive Traffic Lights
for tl_id in ['25', '26', '27']:
    tls = [tl for tl in root.findall('tlLogic') if tl.get('id') == tl_id]
    if tls:
        tl = tls[0]
        tl.set('type', 'actuated')
        tl.set('programID', 'actuated_smart')
        
        # Clear existing phases
        for p in list(tl.findall('phase')):
            tl.remove(p)
            
        # Exactly 20 connections per 4-way junction
        # Phase 0: North-South Green (Dual direction concurrent green)
        p0 = ET.SubElement(tl, 'phase')
        p0.set('duration', '14')
        p0.set('minDur', '4')
        p0.set('maxDur', '22')
        p0.set('state', 'GGGGGGrrrrGGGGGGrrrr')
        
        # Phase 1: North-South Yellow
        p1 = ET.SubElement(tl, 'phase')
        p1.set('duration', '2')
        p1.set('state', 'yyyyyyrrrryyyyyyrrrr')
        
        # Phase 2: East-West Green (Dual direction concurrent green)
        p2 = ET.SubElement(tl, 'phase')
        p2.set('duration', '14')
        p2.set('minDur', '4')
        p2.set('maxDur', '22')
        p2.set('state', 'rrrrGGGGGGrrrrGGGGGG')
        
        # Phase 3: East-West Yellow
        p3 = ET.SubElement(tl, 'phase')
        p3.set('duration', '2')
        p3.set('state', 'rrrrrryyyyrrrrrryyyy')

# Ensure junctions are tagged appropriately
for j in root.findall('junction'):
    j_id = j.get('id')
    if j_id in ['25', '26', '27', '41', '43', '44', '45']:
        j.set('type', 'traffic_light')

tree.write(NET_PATH, encoding='utf-8', xml_declaration=True)
print("Configured all junctions and intelligent actuated traffic lights successfully.")
