"""
Fix lefthand traffic route validation - the circuit connections may be reversed.
In left-hand traffic the edge IDs may still be the same but connections change.
We also need to lower teleports by adding turn-on-red allowance at key junctions.
"""

import subprocess
import os
import xml.etree.ElementTree as ET

net_dir = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net"

# Read actual connection topology from the lefthand-compiled network
tree = ET.parse(os.path.join(net_dir, "sumo.net.xml"))
root = tree.getroot()

connections = {}
for conn in root.findall("connection"):
    f = conn.get("from")
    t = conn.get("to")
    if f and t and not f.startswith(":") and not t.startswith(":"):
        connections.setdefault(f, set()).add(t)

# Re-validate circuits
grand_circuits = [
    ["16", "-19", "15", "outer_west", "-13", "-11", "-14", "-20", "12", "18", "-21", "-22", "-24", "7", "6", "5", "-10", "17"],
    ["20", "14", "11", "13", "-outer_west", "-15", "19", "-16", "12", "18", "-21", "-22", "-24", "-0", "1", "-2", "3", "-4", "-10", "17"],
    ["16", "-19", "15", "outer_west", "-13", "-11", "-14", "-20", "12", "18", "-21", "-22", "-24", "23", "-8", "9", "-10", "17"],
    ["-0", "1", "-2", "3", "-4", "-10", "17", "16", "-19", "15", "outer_west", "-13", "-11", "-14", "-20", "12", "18", "-21", "-22", "-24"],
    ["-10", "17", "12", "18", "-21", "-22", "-24", "7", "6", "5"],
    ["-0", "1", "-2", "3", "-4", "-10", "17", "12", "18", "-21", "-22", "-24"],
    ["-0", "1", "-2", "3", "-4", "-9", "8", "-23"],
    ["-12", "-17", "10", "-5", "-6", "-7", "24", "22", "21", "-18"],
    ["-23", "7", "6", "5", "-9", "8"],
    ["-10", "17", "12", "18", "-21", "-22", "-24", "7", "6", "5"],
]

errors = 0
for i, c in enumerate(grand_circuits):
    for j in range(len(c)):
        curr = c[j]
        nxt = c[(j + 1) % len(c)]
        if nxt not in connections.get(curr, set()):
            print(f"ERROR: Circuit {i+1} - {curr} -> {nxt} NOT connected")
            errors += 1

if errors == 0:
    print("All circuits VALID for lefthand network!")
else:
    # Print all edges that have connections from the error edges
    problematic = set()
    for i, c in enumerate(grand_circuits):
        for j in range(len(c)):
            curr = c[j]
            nxt = c[(j + 1) % len(c)]
            if nxt not in connections.get(curr, set()):
                problematic.add(curr)
    for e in sorted(problematic):
        print(f"  Edge {e} connects to: {sorted(connections.get(e, set()))}")
