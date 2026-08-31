import xml.etree.ElementTree as ET

tree = ET.parse(r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml")
root = tree.getroot()

for j_id in ['25', '26', '27']:
    print(f"\n================ JUNCTION {j_id} ================")
    j_node = [j for j in root.findall('junction') if j.get('id') == j_id][0]
    inc_lanes = j_node.get('incLanes').split()
    print("Incoming lanes:", inc_lanes)
    
    # Check edges
    inc_edges = sorted(list(set([l.split('_')[0] for l in inc_lanes])))
    for e_id in inc_edges:
        e_node = [e for e in root.findall('edge') if e.get('id') == e_id][0]
        l0 = e_node.find('lane')
        shape = l0.get('shape').split()
        p_start = [float(x) for x in shape[0].split(',')]
        p_end = [float(x) for x in shape[-1].split(',')]
        dx = p_end[0] - p_start[0]
        dy = p_end[1] - p_start[1]
        
        # Heading:
        if abs(dy) > abs(dx):
            heading = "Going NORTH (South Approach)" if dy > 0 else "Going SOUTH (North Approach)"
        else:
            heading = "Going EAST (West Approach)" if dx > 0 else "Going WEST (East Approach)"
        
        # Check connection link indices
        links = []
        for conn in root.findall('connection'):
            if conn.get('tl') == j_id and conn.get('from') == e_id:
                links.append((conn.get('linkIndex'), conn.get('dir'), conn.get('to')))
        print(f"Edge {e_id:6s}: {heading:30s} -> Links: {links}")
