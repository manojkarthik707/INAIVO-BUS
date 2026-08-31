import re

with open(r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt", 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines in wbt: {len(lines)}")

for i, line in enumerate(lines):
    if any(k in line.lower() for k in ['cross', 'yellow', 'texture', 'url', 'startline', 'roadline', 'startroads']):
        print(f"L{i+1:5d}: {line.strip()}")
