import re

wbt_path = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt"

JUNCTIONS = {
    "25": {"pos": (45.0, -45.0), "type": "4-way"},
    "26": {"pos": (-45.0, 45.0), "type": "4-way"},
    "27": {"pos": (105.0, 93.0), "type": "4-way"},
    "41": {"pos": (-45.0, -4.5), "type": "T-way", "missing": "W"},
    "43": {"pos": (45.0, 4.5), "type": "T-way", "missing": "N"},
    "44": {"pos": (4.5, 45.0), "type": "T-way", "missing": "E"},
    "45": {"pos": (105.0, -4.5), "type": "T-way", "missing": "W"},
}

with open(wbt_path, "r") as f:
    content = f.read()

tls_out = "# === TRAFFIC LIGHT SYSTEM (Indian road - Left-hand traffic) ===\n"

def get_light_str(name, cx, cy, direction, offset_phase):
    # Place pole in the MEDIAN so the arm extends LEFT over the correct driving lanes
    if direction == "S":
        px = cx
        py = cy - 9.0
        rot = 3.14159  # faces South
    elif direction == "N":
        px = cx
        py = cy + 9.0
        rot = 0.0      # faces North
    elif direction == "E":
        px = cx + 9.0
        py = cy
        rot = -1.5708  # faces East
    elif direction == "W":
        px = cx - 9.0
        py = cy
        rot = 1.5708   # faces West
        
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

new_content = re.sub(
    r"# === TRAFFIC LIGHT SYSTEM \(Indian road - Left-hand traffic\) ===.*?(?=\n\n|\Z)",
    tls_out.strip(),
    content,
    flags=re.DOTALL
)

with open(wbt_path, "w") as f:
    f.write(new_content)

print("Traffic lights correctly aligned using Median placement for Left-Hand Traffic.")
