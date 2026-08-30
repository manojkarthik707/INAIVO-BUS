import xml.etree.ElementTree as ET

tree = ET.parse(r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml")
root = tree.getroot()

x_off, y_off = 175.00, 187.51

# A complete, closed, seamless loop through all major avenues
edge_seq = [
    "-7", "-0", "1", "-2", "3", "-4", "-10", "17", "12", "18", 
    "-21", "-22", "-24", "7", "6", "5", "-5", "-6"
]

waypoints = []
for eid in edge_seq:
    for edge_el in root.findall("edge"):
        if edge_el.get("id") == eid:
            lane = edge_el.find("lane")
            if lane is not None:
                shape_str = lane.get("shape", "")
                for pt in shape_str.strip().split():
                    if "," in pt:
                        sx, sy = map(float, pt.split(","))
                        wx = round(sx - x_off, 2)
                        wy = round(sy - y_off, 2)
                        if not waypoints or (abs(waypoints[-1][0]-wx) > 1.5 or abs(waypoints[-1][1]-wy) > 1.5):
                            waypoints.append((wx, wy))

print(f"Extracted {len(waypoints)} precise road waypoints:")
print(waypoints)
