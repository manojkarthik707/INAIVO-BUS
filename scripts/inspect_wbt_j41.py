with open(r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt", 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = list(re.finditer(r'DEF\s+TRAFFIC_LIGHT_JUNCTION_41\s+Robot\s*\{', text))
print(f"Total TRAFFIC_LIGHT_JUNCTION_41 occurrences: {len(matches)}")
for m in matches:
    print(f"Found at index {m.start()}")
    print(text[m.start():m.start()+1200])
