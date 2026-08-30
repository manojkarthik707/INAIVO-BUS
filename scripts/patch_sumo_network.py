import xml.etree.ElementTree as ET

net_path = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"
tree = ET.parse(net_path)
root = tree.getroot()

# Check if already added
existing_edges = [e.get('id') for e in root.findall('edge')]
if 'outer_west' not in existing_edges:
    # 1. Create edge outer_west (from Custom22 to Custom21)
    edge_ow = ET.Element('edge', {
        'id': 'outer_west',
        'from': 'Custom22',
        'to': 'Custom21',
        'priority': '-1',
        'shape': '39.50,418.51 -1.00,378.01 -1.00,40.50 0.00,0.00'
    })
    lane_ow0 = ET.SubElement(edge_ow, 'lane', {
        'id': 'outer_west_0',
        'index': '0',
        'speed': '13.90',
        'length': '420.0',
        'width': '5.38',
        'shape': '39.50,426.73 -9.21,378.01 -9.21,40.50 0.00,-8.21'
    })
    lane_ow1 = ET.SubElement(edge_ow, 'lane', {
        'id': 'outer_west_1',
        'index': '1',
        'speed': '13.90',
        'length': '420.0',
        'width': '5.38',
        'shape': '39.50,421.25 -3.74,378.01 -3.74,40.50 0.00,-2.74'
    })

    # 2. Create edge -outer_west (from Custom21 to Custom22)
    edge_now = ET.Element('edge', {
        'id': '-outer_west',
        'from': 'Custom21',
        'to': 'Custom22',
        'priority': '-1',
        'shape': '0.00,0.00 -1.00,40.50 -1.00,378.01 39.50,418.51'
    })
    lane_now0 = ET.SubElement(edge_now, 'lane', {
        'id': '-outer_west_0',
        'index': '0',
        'speed': '13.90',
        'length': '420.0',
        'width': '5.38',
        'shape': '0.00,8.21 7.21,40.50 7.21,378.01 39.50,410.30'
    })
    lane_now1 = ET.SubElement(edge_now, 'lane', {
        'id': '-outer_west_1',
        'index': '1',
        'speed': '13.90',
        'length': '420.0',
        'width': '5.38',
        'shape': '0.00,2.74 1.74,40.50 1.74,378.01 39.50,415.78'
    })

    # Add edges before connection elements
    first_conn = root.find('connection')
    idx = list(root).index(first_conn) if first_conn is not None else len(root)
    root.insert(idx, edge_ow)
    root.insert(idx + 1, edge_now)

    # 3. Add seamless connections
    # 15 -> outer_west
    root.append(ET.Element('connection', {'from': '15', 'to': 'outer_west', 'fromLane': '0', 'toLane': '0', 'dir': 's', 'state': 'M'}))
    root.append(ET.Element('connection', {'from': '15', 'to': 'outer_west', 'fromLane': '1', 'toLane': '1', 'dir': 's', 'state': 'M'}))
    
    # outer_west -> -13
    root.append(ET.Element('connection', {'from': 'outer_west', 'to': '-13', 'fromLane': '0', 'toLane': '0', 'dir': 's', 'state': 'M'}))
    root.append(ET.Element('connection', {'from': 'outer_west', 'to': '-13', 'fromLane': '1', 'toLane': '1', 'dir': 's', 'state': 'M'}))

    # 13 -> -outer_west
    root.append(ET.Element('connection', {'from': '13', 'to': '-outer_west', 'fromLane': '0', 'toLane': '0', 'dir': 's', 'state': 'M'}))
    root.append(ET.Element('connection', {'from': '13', 'to': '-outer_west', 'fromLane': '1', 'toLane': '1', 'dir': 's', 'state': 'M'}))

    # -outer_west -> -15
    root.append(ET.Element('connection', {'from': '-outer_west', 'to': '-15', 'fromLane': '0', 'toLane': '0', 'dir': 's', 'state': 'M'}))
    root.append(ET.Element('connection', {'from': '-outer_west', 'to': '-15', 'fromLane': '1', 'toLane': '1', 'dir': 's', 'state': 'M'}))

    tree.write(net_path, encoding='utf-8', xml_declaration=True)
    print("Successfully patched sumo.net.xml with outer_west and -outer_west highway edges!")
else:
    print("sumo.net.xml already contains outer_west edges.")
