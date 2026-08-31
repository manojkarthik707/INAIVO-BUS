import xml.etree.ElementTree as ET
import random

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

def find_all_circuits_from_edge(start_edge, min_len=4, max_len=14, limit=10):
    circuits = []
    def dfs(curr, path):
        if len(circuits) >= limit:
            return
        if len(path) > max_len:
            return
        for nxt in connections.get(curr, []):
            if nxt == start_edge and len(path) >= min_len:
                circuits.append(path)
            elif nxt not in path:
                rev = curr[1:] if curr.startswith('-') else ('-' + curr)
                if nxt != rev:
                    dfs(nxt, path + [nxt])
    dfs(start_edge, [start_edge])
    return circuits

all_diverse_circuits = {}
for edge in all_edges:
    c_list = find_all_circuits_from_edge(edge)
    all_diverse_circuits[edge] = c_list
    print(f"Edge '{edge}': found {len(c_list)} distinct route circuits.")
