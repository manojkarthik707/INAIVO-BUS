import xml.etree.ElementTree as ET
tree = ET.parse(r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml")
root = tree.getroot()
loc = root.find("location")
print("Net offset:", loc.get("netOffset"))
print("Conv boundary:", loc.get("convBoundary"))
for j in root.findall("junction"):
    if j.get("type") == "traffic_light":
        print(f"Junction {j.get('id')}: SUMO x={j.get('x')} y={j.get('y')}")
