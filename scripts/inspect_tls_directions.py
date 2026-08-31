import xml.etree.ElementTree as ET

NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"
tree = ET.parse(NET_PATH)
root = tree.getroot()

# Let's inspect nodes positions
nodes_pos = {}
for n in root.findall('junction'):
    nodes_pos[n.get('id')] = (float(n.get('x')), float(n.get('y')))

for tl_id in ['25', '26', '27']:
    jx, jy = nodes_pos[tl_id]
    print(f"\n=== JUNCTION {tl_id} at ({jx}, {jy}) ===")
    for c in root.findall('connection'):
        if c.get('tl') == tl_id and c.get('fromLane') == '0':
            f_edge = c.get('from')
            # find from node or edge shape
            for e in root.findall('edge'):
                if e.get('id') == f_edge:
                    from_node = e.get('from')
                    fx, fy = nodes_pos.get(from_node, (0,0))
                    dx = fx - jx
                    dy = fy - jy
                    if abs(dx) > abs(dy):
                        dir_str = "EAST" if dx > 0 else "WEST"
                    else:
                        dir_str = "NORTH" if dy > 0 else "SOUTH"
                    print(f"  Link {c.get('linkIndex')}: Edge {f_edge} approaches from {dir_str} (from node {from_node} at {fx}, {fy})")
                    break
