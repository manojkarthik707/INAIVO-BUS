with open(r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt", "r", encoding="utf-8") as f:
    content = f.read()

import re
matches = re.finditer(r'(DEF\s+\w+\s+)?(GenericTrafficLight|CrossRoadsTrafficLight|HighwayPole|CautionSign|OrderSign|StopSign|SpeedLimitSign|YieldSign)\s*\{([^}]+)\}', content)

for m in matches:
    name = m.group(2)
    body = m.group(3)
    trans = re.search(r'translation\s+([-\d\.\s]+)', body)
    trans_str = trans.group(1).strip() if trans else "no translation"
    print(f"Node: {name} | Translation: {trans_str}")
