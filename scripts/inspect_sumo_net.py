import xml.etree.ElementTree as ET

tree = ET.parse(r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml")
root = tree.getroot()

for j in root.findall("junction"):
    jid = j.get("id")
    if jid in ["Custom21", "Custom22", "32", "36"]:
        print(f"Junction {jid}: x={j.get('x')} y={j.get('y')} type={j.get('type')}")

print("\nEdges connected to these junctions:")
for e in root.findall("edge"):
    if e.get("from") in ["Custom21", "Custom22"] or e.get("to") in ["Custom21", "Custom22"]:
        print(f"Edge {e.get('id')}: from={e.get('from')} to={e.get('to')}")
