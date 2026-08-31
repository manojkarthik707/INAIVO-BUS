with open(r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt", 'r', encoding='utf-8') as f:
    text = f.read()

import re

for m in re.finditer(r'(StraightRoadSegment|CurvedRoadSegment)\s*\{', text):
    start = m.start()
    # find matching block
    snippet = text[start:start+400]
    print(snippet[:snippet.find('lines [')].strip())
    print("-" * 50)
