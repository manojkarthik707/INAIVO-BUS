with open(r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt", 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'Robot {' in line or 'name "BUS_' in line:
        print(f"Line {i+1}: {line.strip()}")
