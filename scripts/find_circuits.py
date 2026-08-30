import xml.etree.ElementTree as ET

tree = ET.parse(r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml")
root = tree.getroot()

connections = {}
for conn in root.findall('connection'):
    from_edge = conn.get('from')
    to_edge = conn.get('to')
    if from_edge and to_edge and not from_edge.startswith(':') and not to_edge.startswith(':'):
        connections.setdefault(from_edge, set()).add(to_edge)

def find_closed_circuits(min_len=6, max_len=14):
    valid_circuits = []
    def dfs(start, current_path):
        if len(current_path) >= max_len:
            return
        curr = current_path[-1]
        for nxt in connections.get(curr, []):
            if nxt == start:
                if len(current_path) >= min_len:
                    valid_circuits.append(current_path)
            elif nxt not in current_path:
                dfs(start, current_path + [nxt])

    for edge in connections.keys():
        dfs(edge, [edge])
    
    unique = []
    seen = set()
    for c in valid_circuits:
        min_i = c.index(min(c))
        norm = tuple(c[min_i:] + c[:min_i])
        if norm not in seen:
            seen.add(norm)
            unique.append(c)
    return unique

circuits = find_closed_circuits(6, 12)
print(f"Found {len(circuits)} unique major closed circuits!")
for i, c in enumerate(circuits[:15]):
    edge_str = " ".join(c)
    print(f"Loop {i+1} (len {len(c)}): {edge_str}")
