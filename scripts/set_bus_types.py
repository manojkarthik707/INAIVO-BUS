import re

path = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.rou.xml"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

text = re.sub(r'<vehicle id="0" type="[^"]+"', '<vehicle id="0" type="bus"', text, count=1)
text = re.sub(r'<vehicle id="1" type="[^"]+"', '<vehicle id="1" type="bus"', text, count=1)
text = re.sub(r'<vehicle id="2" type="[^"]+"', '<vehicle id="2" type="bus"', text, count=1)

with open(path, "w", encoding="utf-8") as f:
    f.write(text)

print("Updated vehicle 0, 1, 2 to type='bus' successfully!")
