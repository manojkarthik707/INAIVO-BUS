with open(r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt", 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Find all StraightRoadSegment nodes
roads = re.findall(r'DEF\s+(\w+)\s+StraightRoadSegment\s*\{([^}]*)\}', text)
print(f"Total StraightRoadSegments: {len(roads)}")
for name, body in roads:
    trans = re.search(r'translation\s+([^\n]+)', body)
    rot = re.search(r'rotation\s+([^\n]+)', body)
    length = re.search(r'length\s+([^\n]+)', body)
    print(f"Road {name}: trans={trans.group(1) if trans else '0 0 0'} rot={rot.group(1) if rot else '0 0 1 0'} len={length.group(1) if length else 'N/A'}")

# Find all Robot nodes
robots = re.findall(r'DEF\s+(\w+)\s+Robot\s*\{([^}]*)\}', text)
print(f"\nTotal Robots: {len(robots)}")
for name, body in robots:
    trans = re.search(r'translation\s+([^\n]+)', body)
    print(f"Robot {name}: trans={trans.group(1) if trans else '0 0 0'}")
