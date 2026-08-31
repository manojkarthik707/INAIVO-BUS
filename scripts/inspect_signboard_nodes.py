import re

with open(r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt", 'r', encoding='utf-8') as f:
    text = f.read()

for m in re.finditer(r'(AdvertisingBoard|HighwaySign|CautionSign|OrderSign)\s*\{([^}]+(?:\{[^}]*\}[^}]*)*)\}', text):
    print("==================================================")
    print(m.group(0))
