import xml.etree.ElementTree as ET
import os

net_dir = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net"
net_path = os.path.join(net_dir, "sumo.net.xml")

tree = ET.parse(net_path)
root = tree.getroot()

for tl in root.findall("tlLogic"):
    tid = tl.get("id")
    if tid in ["25", "26", "27"]:
        # Find the length of the state string
        num_links = len(tl.find("phase").get("state"))
        
        # Clear existing phases
        for phase in tl.findall("phase"):
            tl.remove(phase)
            
        # We assume edges are grouped in blocks of (num_links / 4) because it's a 4-way intersection
        block = num_links // 4
        
        # Create 4 split phases
        for i in range(4):
            # Green phase
            state_g = ["r"] * num_links
            for j in range(block):
                state_g[i * block + j] = "G"
            
            p_g = ET.SubElement(tl, "phase")
            p_g.set("duration", "15")
            p_g.set("state", "".join(state_g))
            
            # Yellow phase
            state_y = ["r"] * num_links
            for j in range(block):
                state_y[i * block + j] = "y"
                
            p_y = ET.SubElement(tl, "phase")
            p_y.set("duration", "3")
            p_y.set("state", "".join(state_y))

tree.write(net_path, encoding="utf-8", xml_declaration=True)
print("Injected split phases for junctions 25, 26, 27!")
