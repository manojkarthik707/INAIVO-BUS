import re

WBT_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt"

with open(WBT_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the start of the billboard section before traffic lights
idx_clean = content.find("# ==============================================================================\n# INETRA PREMIUM MONOPOLE BILLBOARD")
if idx_clean == -1:
    idx_clean = content.find("# ==============================================================================\n# SLEEK 4-WAY INDIAN TRAFFIC LIGHT POST")
if idx_clean == -1:
    idx_clean = content.find("# ==============================================================================\n# UNBLOCKED 5-ASPECT")

# Everything up to before the duplicate billboards
base_world = content[:content.find("Solid {\n  name \"inetra_billboard_j26\"")]
if not base_world:
    base_world = content[:idx_clean]

# Generate exact single copy of the 3 pristine billboards
from upgrade_billboard_display_geometry import generate_pristine_inetra_billboard

billboards = [
    generate_pristine_inetra_billboard("inetra_billboard_j26", -30.0, 60.0, -0.785398),
    generate_pristine_inetra_billboard("inetra_billboard_j25", 30.0, -30.0, 2.35619),
    generate_pristine_inetra_billboard("inetra_billboard_j27", 120.0, 80.0, 3.14159),
]

# Find where traffic light posts start
tls_idx = content.find("# ==============================================================================\n# SLEEK 4-WAY INDIAN TRAFFIC LIGHT POST")
if tls_idx == -1:
    tls_idx = content.find("# ==============================================================================\n# UNBLOCKED 5-ASPECT")

tls_section = content[tls_idx:]

new_wbt = base_world.rstrip() + "\n\n" + "\n".join(billboards) + "\n\n" + tls_section

with open(WBT_PATH, 'w', encoding='utf-8') as f:
    f.write(new_wbt)

print(f"Purged duplicate billboard nodes and kept single pristine copy in {WBT_PATH}")
