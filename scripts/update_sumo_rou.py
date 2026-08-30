import re

path = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.rou.xml"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

vtypes = """    <vType id="bus" vClass="bus" accel="1.5" decel="3.0" length="9.5" minGap="2.5" maxSpeed="15.0"/>
    <vType id="passenger" vClass="passenger" accel="2.6" decel="4.5" length="4.5" minGap="2.5" maxSpeed="20.0"/>
"""

# remove existing vType if any
content = re.sub(r'^\s*<vType.*?>\n', '', content, flags=re.MULTILINE)

# insert vtypes
content = content.replace(
    '<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">',
    '<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">\n' + vtypes
)

# replace vehicles
def repl(m):
    vid = int(m.group(1))
    vtype = "bus" if vid % 4 == 0 else "passenger"
    return f'<vehicle id="{vid}" type="{vtype}" depart="{m.group(2)}"'

content = re.sub(r'<vehicle id="(\d+)"(?:\s+type="[^"]*")?\s+depart="([0-9.]+)"', repl, content)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully updated sumo.rou.xml!")
