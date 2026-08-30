import re

wbt_path = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt"

with open(wbt_path, "r") as f:
    content = f.read()

# Remove old traffic lights block
content = re.sub(r'\n# === TRAFFIC LIGHT SYSTEM.*?\Z', '', content, flags=re.DOTALL)
content = content.strip()

JUNCTIONS = {
    "25": {"pos": (45.0, -45.0), "type": "4-way"},
    "26": {"pos": (-45.0, 45.0), "type": "4-way"},
    "27": {"pos": (105.0, 93.0), "type": "4-way"},
    "41": {"pos": (-45.0, -4.5), "type": "T-way", "missing": "W"},
    "43": {"pos": (45.0, 4.5), "type": "T-way", "missing": "N"},
    "44": {"pos": (4.5, 45.0), "type": "T-way", "missing": "E"},
    "45": {"pos": (105.0, -4.5), "type": "T-way", "missing": "W"},
}

tls_out = "\n\n# === TRAFFIC LIGHT SYSTEM (Indian road - Left-hand traffic) ===\n"

def get_light_str(name, cx, cy, direction, offset_phase):
    # Placement for left-hand traffic using vertical poles
    # Pole goes on the LEFT side of the approaching lanes
    if direction == "S":
        px = cx - 8.5  # West edge (Left)
        py = cy - 9.0  # South of center
        rot = 1.5708   # faces South
    elif direction == "N":
        px = cx + 8.5  # East edge (Left)
        py = cy + 9.0  # North of center
        rot = -1.5708  # faces North
    elif direction == "E":
        px = cx + 9.0  # East of center
        py = cy - 8.5  # South edge (Left)
        rot = 3.14159  # faces East
    elif direction == "W":
        px = cx - 9.0  # West of center
        py = cy + 8.5  # North edge (Left)
        rot = 0.0      # faces West
        
    start_green = "TRUE" if offset_phase else "FALSE"
    
    return f"""DEF {name} GenericTrafficLight {{
  translation {px:.2f} {py:.2f} 0.0
  rotation 0 0 1 {rot:.4f}
  name "{name}"
  startGreen {start_green}
}}
"""

for jid, data in JUNCTIONS.items():
    cx, cy = data["pos"]
    dirs = ["N", "S", "E", "W"]
    if data["type"] == "T-way":
        dirs.remove(data["missing"])
    
    tls_out += f"# Junction {jid} ({data['type']})\n"
    for d in dirs:
        offset = (d in ["N", "S"])
        if jid in ["43", "45", "26"]:
            offset = not offset
        name = f"tls_j{jid}_{d}"
        tls_out += get_light_str(name, cx, cy, d, offset)

with open(wbt_path, "w") as f:
    f.write(content + tls_out)

print("Traffic lights correctly placed on the left edge facing the traffic!")
