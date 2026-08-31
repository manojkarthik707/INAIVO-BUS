import re

with open(r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt", 'r', encoding='utf-8') as f:
    text = f.read()

# Find roads connected to startJunction or endJunction 26, 25, 27
for m in re.finditer(r'(CurvedRoadSegment|StraightRoadSegment|RoadIntersection|Crossroad)\s*\{([^}]+(?:\{[^}]*\}[^}]*)*)\}', text):
    block = m.group(0)
    if '26' in block or '25' in block or '27' in block:
        print("-----------------------------------------")
        print(block[:300])
        if 'cross' in block.lower() or 'line' in block.lower():
            print("LINES/CROSSING FOUND in block:")
            lines_m = re.findall(r'(lines|crosswalk|RoadLine)[^\]\}]*', block, re.DOTALL)
            for lm in lines_m:
                print(lm[:200])
