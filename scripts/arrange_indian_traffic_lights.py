import re
import math

# Webots uses Z-up. 
# Z is rotation axis.

# T-junctions have 3 incoming roads, 4-ways have 4.
# We will place a GenericTrafficLight on the LEFT side of each incoming road.
# Distance from center = 9 meters out, 7.5 meters left.
# Arm length of GenericTrafficLight is usually ~5-8 meters.

JUNCTIONS = {
    "25": {"pos": (45.0, -45.0), "type": "4-way"},
    "26": {"pos": (-45.0, 45.0), "type": "4-way"},
    "27": {"pos": (105.0, 93.0), "type": "4-way"},
    "41": {"pos": (-45.0, -4.5), "type": "T-way", "missing": "W"}, # inner left T-junction, road goes N, S, E
    "43": {"pos": (45.0, 4.5), "type": "T-way", "missing": "N"},   # inner center T-junction, road goes S, E, W
    "44": {"pos": (4.5, 45.0), "type": "T-way", "missing": "E"},   # inner center-left T-junction, road goes N, S, W
    "45": {"pos": (105.0, -4.5), "type": "T-way", "missing": "W"}, # inner right T-junction, road goes N, S, E
}

# The GenericTrafficLight arm extends to the right when facing it.
# So if placed on the left side of the road, the arm correctly hangs over the road.
# Facing directions (angle around Z-axis):
# If road comes from South (heading North), light should face South.
# Rotation angle to face South: if default faces South, angle = 0.
# Let's assume default rotation (0) faces North, so arm is along X.
# If it faces North, the pole is at origin, arm is at +X (East). Wait, if facing North, right is East.
# Let's use standard angles.
# Incoming from South (faces South): 
# pos: cx - 7.5 (left), cy - 9 (back)
# rot: pi

# Wait, let's just generate the nodes.
wbt_path = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt"

with open(wbt_path, "r") as f:
    content = f.read()

# Generate new TLS string
tls_out = "# === TRAFFIC LIGHT SYSTEM (Indian road - Left-hand traffic) ===\n"

def get_light_str(name, cx, cy, direction, offset_phase):
    # offset_phase = TRUE if it should start green, FALSE for red
    # direction is where the traffic is COMING FROM.
    # So the light faces that direction.
    
    # Left side of the road means:
    # If traffic comes from South (heading North): Left is West (cx - 7.5), Back is South (cy - 9)
    if direction == "S":
        px = cx - 7.5
        py = cy - 9.0
        rot = 3.14159  # face South
    elif direction == "N":
        px = cx + 7.5
        py = cy + 9.0
        rot = 0.0      # face North
    elif direction == "E":
        px = cx + 9.0
        py = cy - 7.5
        rot = 1.5708   # face East
    elif direction == "W":
        px = cx - 9.0
        py = cy + 7.5
        rot = -1.5708  # face West
        
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
        # N/S get phase 1 (starts green), E/W get phase 2 (starts red)
        # Or vice versa depending on the junction to stagger them
        offset = (d in ["N", "S"])
        # For junctions 43, 45 let's invert phase to create a green wave
        if jid in ["43", "45", "26"]:
            offset = not offset
            
        name = f"tls_j{jid}_{d}"
        tls_out += get_light_str(name, cx, cy, d, offset)

# Replace in file
import re
new_content = re.sub(
    r"# === TRAFFIC LIGHT SYSTEM \(Indian road - Left-hand traffic\) ===.*?(?=\n\n|\Z)",
    tls_out.strip(),
    content,
    flags=re.DOTALL
)

with open(wbt_path, "w") as f:
    f.write(new_content)

print("Traffic lights arranged for Indian roads (left side placement).")
