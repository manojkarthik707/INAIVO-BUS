import re

with open(r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt", 'r', encoding='utf-8') as f:
    text = f.read()

# Find all nodes with sign, board, panel, display, or texture
matches = re.findall(r'(\w+)\s*\{[^}]*(?:sign|board|panel|texture|display)[^}]*\}', text, re.IGNORECASE)
print(f"Found {len(matches)} matching node blocks:")
for m in set(matches):
    print(" -", m)

# Search specifically for any occurrence of 'AdvertisingBoard', 'HighwaySign', 'CautionSign', 'OrderSign'
for proto in ['AdvertisingBoard', 'HighwaySign', 'CautionSign', 'OrderSign', 'CautionPanel', 'OrderPanel', 'SpeedLimitSign', 'SpeedLimitPanel']:
    count = len(re.findall(r'\b' + proto + r'\b', text))
    print(f"Proto {proto}: {count} occurrences")
