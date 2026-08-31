with open(r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt", 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = list(re.finditer(r'(DEF\s+(\w+)\s+)?Robot\s*\{', text))
print(f"Total Robot nodes: {len(matches)}")
for m in matches:
    start = m.start()
    snippet = text[start:start+250]
    name_m = re.search(r'name\s+"([^"]+)"', snippet)
    ctrl_m = re.search(r'controller\s+"([^"]+)"', snippet)
    print(f"Robot at {start}: DEF={m.group(2)} name={name_m.group(1) if name_m else 'N/A'} ctrl={ctrl_m.group(1) if ctrl_m else 'N/A'}")
