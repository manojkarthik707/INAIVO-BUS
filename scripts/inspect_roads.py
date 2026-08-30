import re

path = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

roads = re.findall(r'(StraightRoadSegment|CurvedRoadSegment)\s*\{([^}]+)\}', text)
print(f"Total road objects: {len(roads)}")
for rtype, body in roads:
    rid = re.search(r'id "(\d+)"', body)
    name = re.search(r'name "([^"]+)"', body)
    trans = re.search(r'translation ([-\d\.]+\s+[-\d\.]+\s+[-\d\.]+)', body)
    start_j = re.search(r'startJunction "([^"]+)"', body)
    end_j = re.search(r'endJunction "([^"]+)"', body)
    length = re.search(r'length ([\d\.]+)', body)
    radius = re.search(r'curvatureRadius ([\d\.]+)', body)
    
    r_id_str = rid.group(1) if rid else "?"
    name_str = name.group(1) if name else "?"
    trans_str = trans.group(1) if trans else "?"
    start_str = start_j.group(1) if start_j else "?"
    end_str = end_j.group(1) if end_j else "?"
    len_str = f"len={length.group(1)}" if length else (f"rad={radius.group(1)}" if radius else "")
    
    print(f"Road id={r_id_str:<3} {rtype:<18} {len_str:<10} trans=[{trans_str}] startJ={start_str} endJ={end_str}")
