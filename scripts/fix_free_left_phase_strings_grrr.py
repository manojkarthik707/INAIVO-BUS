import xml.etree.ElementTree as ET

NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"

tree = ET.parse(NET_PATH)
root = tree.getroot()

# Update TLS 25, 26, 27 with correct 'grrr' pattern:
# 'GGGg' = Active Green Approach (Left, Through, Through, Right Green)
# 'yyyy' = Active Amber Approach
# 'grrr' = Red Approach with Free Left (Link 0 is 'g' Green, Links 1-3 are 'r' Red)
for tl in root.findall('tlLogic'):
    tl_id = tl.get('id')
    if tl_id in ['25', '26', '27']:
        for p in list(tl.findall('phase')):
            tl.remove(p)

        # Stage 0: Approach 0 Green, Approaches 1, 2, 3 Red with Free Left
        ET.SubElement(tl, 'phase', {'duration': '5.0', 'state': 'GGGggrrrgrrrgrrr'})
        ET.SubElement(tl, 'phase', {'duration': '2.0', 'state': 'yyyygrrrgrrrgrrr'})

        # Stage 1: Approach 1 Green, Approaches 0, 2, 3 Red with Free Left
        ET.SubElement(tl, 'phase', {'duration': '5.0', 'state': 'grrrGGGggrrrgrrr'})
        ET.SubElement(tl, 'phase', {'duration': '2.0', 'state': 'grrryyyygrrrgrrr'})

        # Stage 2: Approach 2 Green, Approaches 0, 1, 3 Red with Free Left
        ET.SubElement(tl, 'phase', {'duration': '5.0', 'state': 'grrrgrrrGGGggrrr'})
        ET.SubElement(tl, 'phase', {'duration': '2.0', 'state': 'grrrgrrryyyygrrr'})

        # Stage 3: Approach 3 Green, Approaches 0, 1, 2 Red with Free Left
        ET.SubElement(tl, 'phase', {'duration': '5.0', 'state': 'grrrgrrrgrrrGGGg'})
        ET.SubElement(tl, 'phase', {'duration': '2.0', 'state': 'grrrgrrrgrrryyyy'})

tree.write(NET_PATH, encoding='utf-8', xml_declaration=True)
print("Configured correct 'grrr' Free Left phases in sumo.net.xml for TLS 25, 26, 27!")
