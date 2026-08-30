import xml.etree.ElementTree as ET
tree = ET.parse(r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml")
root = tree.getroot()
tls = root.findall("tlLogic")
print(f"Traffic light controllers installed: {len(tls)}")
for t in tls:
    phases = t.findall("phase")
    tls_id = t.get("id")
    tls_type = t.get("type")
    print(f"  TLS {tls_id} ({tls_type}): {len(phases)} phases")
    for p in phases:
        print(f"    dur={p.get('duration')}s state={p.get('state')}")

# Check junction types
junctions = [(j.get("id"), j.get("type")) for j in root.findall("junction") 
             if j.get("type") not in ["dead_end","internal"]]
print("\nJunction types:")
for jid, jtype in junctions:
    print(f"  {jid}: {jtype}")
