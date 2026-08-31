import xml.etree.ElementTree as ET
import re

NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"
tree = ET.parse(NET_PATH)
root = tree.getroot()

# 1. Clean existing shortcut edges/connections
for edge in list(root.findall('edge')):
    if edge.get('id') in ['shortcut_east', 'shortcut_west']:
        root.remove(edge)

for conn in list(root.findall('connection')):
    f = conn.get('from', '')
    t = conn.get('to', '')
    if 'shortcut' in f or 'shortcut' in t:
        root.remove(conn)

# 2. Add shortcut_east (from 41 to 43) and shortcut_west (from 43 to 41)
edge_east = ET.Element('edge', {
    'id': 'shortcut_east',
    'from': '41',
    'to': '43',
    'priority': '10',
    'type': 'highway.city'
})
ET.SubElement(edge_east, 'lane', {
    'id': 'shortcut_east_0',
    'index': '0',
    'speed': '18.00',
    'length': '90.00',
    'width': '3.75',
    'shape': '132.50,181.50 217.50,190.50'
})
ET.SubElement(edge_east, 'lane', {
    'id': 'shortcut_east_1',
    'index': '1',
    'speed': '18.00',
    'length': '90.00',
    'width': '3.75',
    'shape': '132.50,184.75 217.50,193.75'
})

edge_west = ET.Element('edge', {
    'id': 'shortcut_west',
    'from': '43',
    'to': '41',
    'priority': '10',
    'type': 'highway.city'
})
ET.SubElement(edge_west, 'lane', {
    'id': 'shortcut_west_0',
    'index': '0',
    'speed': '18.00',
    'length': '90.00',
    'width': '3.75',
    'shape': '217.50,193.50 132.50,184.50'
})
ET.SubElement(edge_west, 'lane', {
    'id': 'shortcut_west_1',
    'index': '1',
    'speed': '18.00',
    'length': '90.00',
    'width': '3.75',
    'shape': '217.50,190.25 132.50,181.25'
})

# Insert edges before tlLogics/junctions
first_junc_idx = None
for i, child in enumerate(root):
    if child.tag in ['junction', 'tlLogic']:
        first_junc_idx = i
        break

insert_idx = first_junc_idx if first_junc_idx is not None else len(root)
root.insert(insert_idx, edge_east)
root.insert(insert_idx + 1, edge_west)

# 3. Add direct connections at Junction 41 & 43
# Junction 41 (Left End):
# - 8_1 -> shortcut_east_1 (turn right into shortcut)
# - 23_0 -> shortcut_east_0 (turn left into shortcut)
# - shortcut_west_0 -> -8_0 (turn left south)
# - shortcut_west_1 -> -23_1 (turn right north)
conns = [
    {'from': '8', 'to': 'shortcut_east', 'fromLane': '1', 'toLane': '1', 'dir': 'r', 'state': 'M'},
    {'from': '23', 'to': 'shortcut_east', 'fromLane': '0', 'toLane': '0', 'dir': 'l', 'state': 'M'},
    {'from': 'shortcut_west', 'to': '-8', 'fromLane': '0', 'toLane': '0', 'dir': 'l', 'state': 'M'},
    {'from': 'shortcut_west', 'to': '-23', 'fromLane': '1', 'toLane': '1', 'dir': 'r', 'state': 'M'},

    # Junction 43 (Right End):
    # - shortcut_east_0 -> 6_0 (turn left north onto 6)
    # - shortcut_east_1 -> -5_1 (turn right south onto -5)
    # - -5_0 -> shortcut_west_0 (turn left into shortcut)
    # - 6_1 -> shortcut_west_1 (turn right into shortcut)
    {'from': 'shortcut_east', 'to': '6', 'fromLane': '0', 'toLane': '0', 'dir': 'l', 'state': 'M'},
    {'from': 'shortcut_east', 'to': '-5', 'fromLane': '1', 'toLane': '1', 'dir': 'r', 'state': 'M'},
    {'from': '-5', 'to': 'shortcut_west', 'fromLane': '0', 'toLane': '0', 'dir': 'l', 'state': 'M'},
    {'from': '6', 'to': 'shortcut_west', 'fromLane': '1', 'toLane': '1', 'dir': 'r', 'state': 'M'},
]

for c in conns:
    ET.SubElement(root, 'connection', c)

tree.write(NET_PATH, encoding='utf-8', xml_declaration=True)
print(f"Successfully integrated shortcut road edges and connections into {NET_PATH}")
