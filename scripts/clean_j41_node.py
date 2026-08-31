from build_complete_shortcut_and_sumo_net import generate_custom_3way_tower

WBT_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt"

with open(WBT_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the end of TRAFFIC_LIGHT_JUNCTION_27
idx_j27 = content.find('name "traffic_light_junction_27"')
if idx_j27 != -1:
    # Find the closing brace of junction 27 node
    idx_end = content.find('locked TRUE\n}', idx_j27)
    if idx_end != -1:
        base_world = content[:idx_end + len('locked TRUE\n}')]
    else:
        idx_end = content.find('}', idx_j27)
        base_world = content[:idx_end + 1]
else:
    base_world = content

# Generate pristine single copy of TRAFFIC_LIGHT_JUNCTION_41
post_41 = generate_custom_3way_tower("TRAFFIC_LIGHT_JUNCTION_41", "41", -45.0, 4.5)

new_wbt = base_world.rstrip() + "\n\n" + post_41.strip() + "\n"

with open(WBT_PATH, 'w', encoding='utf-8') as f:
    f.write(new_wbt)

print(f"Cleanly appended pristine TRAFFIC_LIGHT_JUNCTION_41 in {WBT_PATH}")
