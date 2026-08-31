import re

WBT_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt"
with open(WBT_PATH, 'r', encoding='utf-8') as f:
    text = f.read()

# Find roads connected to junction 26
print("--- ROADS AT JUNCTION 26 ---")
for m in re.finditer(r'(StraightRoadSegment|CurvedRoadSegment)\s*\{([^}]+)\}', text):
    block = m.group(2)
    if '26' in block:
        name = re.search(r'name\s+"([^"]+)"', block)
        n_str = name.group(1) if name else "unnamed"
        trans = re.search(r'translation\s+([-\d\.\s]+)', block)
        t_str = trans.group(1) if trans else "no trans"
        rot = re.search(r'rotation\s+([-\d\.\s]+)', block)
        r_str = rot.group(1) if rot else "no rot"
        id_m = re.search(r'id\s+"([^"]+)"', block)
        id_str = id_m.group(1) if id_m else "no id"
        print(f"Road {n_str:20s} (id={id_str}): translation={t_str:20s} rotation={r_str}")
