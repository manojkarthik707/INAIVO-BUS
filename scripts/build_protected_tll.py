import xml.etree.ElementTree as ET

TLL_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\plain.tll.xml"

# Exact 28s 4-stage cycles for Junction 25, 26, 27
# Junction 25 (20 links):
# Stage 0 (5s G + 2s Y): East
# Stage 1 (5s G + 2s Y): North
# Stage 2 (5s G + 2s Y): West
# Stage 3 (5s G + 2s Y): South
tl25_phases = [
    {'duration': '5', 'state': 'GGGGggrrrrgrrrrgrrrr'},
    {'duration': '2', 'state': 'yyyyygrrrrgrrrrgrrrr'},
    {'duration': '5', 'state': 'grrrrGGGGggrrrrgrrrr'},
    {'duration': '2', 'state': 'grrrryyyyygrrrrgrrrr'},
    {'duration': '5', 'state': 'grrrrgrrrrGGGGggrrrr'},
    {'duration': '2', 'state': 'grrrrgrrrryyyyygrrrr'},
    {'duration': '5', 'state': 'grrrrgrrrrgrrrrGGGGg'},
    {'duration': '2', 'state': 'grrrrgrrrrgrrrryyyyy'},
]

# Junction 26 & 27 (20 links):
# Stage 0: South
# Stage 1: East
# Stage 2: North
# Stage 3: West
tl26_27_phases = [
    {'duration': '5', 'state': 'GGGGggrrrrgrrrrgrrrr'},
    {'duration': '2', 'state': 'yyyyygrrrrgrrrrgrrrr'},
    {'duration': '5', 'state': 'grrrrGGGGggrrrrgrrrr'},
    {'duration': '2', 'state': 'grrrryyyyygrrrrgrrrr'},
    {'duration': '5', 'state': 'grrrrgrrrrGGGGggrrrr'},
    {'duration': '2', 'state': 'grrrrgrrrryyyyygrrrr'},
    {'duration': '5', 'state': 'grrrrgrrrrgrrrrGGGGg'},
    {'duration': '2', 'state': 'grrrrgrrrrgrrrryyyyy'},
]

root = ET.Element('tlLogics', {'version': '1.20'})

# TL 25
tl25 = ET.SubElement(root, 'tlLogic', {'id': '25', 'type': 'static', 'programID': '0', 'offset': '0'})
for p in tl25_phases:
    ET.SubElement(tl25, 'phase', p)

# TL 26
tl26 = ET.SubElement(root, 'tlLogic', {'id': '26', 'type': 'static', 'programID': '0', 'offset': '0'})
for p in tl26_27_phases:
    ET.SubElement(tl26, 'phase', p)

# TL 27
tl27 = ET.SubElement(root, 'tlLogic', {'id': '27', 'type': 'static', 'programID': '0', 'offset': '0'})
for p in tl26_27_phases:
    ET.SubElement(tl27, 'phase', p)

tree = ET.ElementTree(root)
tree.write(TLL_PATH, encoding='utf-8', xml_declaration=True)
print(f"Populated protected 28s cycles in {TLL_PATH}")
