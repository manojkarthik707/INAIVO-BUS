import xml.etree.ElementTree as ET

NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"
tree = ET.parse(NET_PATH)
root = tree.getroot()

all_edges = sorted(list(set([e.get('id') for e in root.findall('edge') if not e.get('id', '').startswith(':')])))

connections = {}
for conn in root.findall('connection'):
    f = conn.get('from')
    t = conn.get('to')
    d = conn.get('dir')
    if f and t and not f.startswith(':') and not t.startswith(':'):
        rev = f[1:] if f.startswith('-') else ('-' + f)
        if t != rev and d != 't':
            connections.setdefault(f, set()).add(t)

def find_forward_circuit(start_edge, min_len=6, max_len=18):
    valid = []
    def dfs(curr, path):
        if len(path) >= max_len:
            return
        for nxt in connections.get(curr, []):
            if nxt == start_edge and len(path) >= min_len:
                valid.append(path)
                return
            elif nxt not in path:
                rev = curr[1:] if curr.startswith('-') else ('-' + curr)
                if nxt != rev:
                    dfs(nxt, path + [nxt])
    dfs(start_edge, [start_edge])
    return valid[0] if valid else None

found_circuits = {}
for edge in all_edges:
    c = find_forward_circuit(edge)
    if c:
        found_circuits[edge] = c
    else:
        print(f"NO CIRCUIT starting from edge: {edge}")

print(f"Total edges with circuits: {len(found_circuits)} / {len(all_edges)}")
