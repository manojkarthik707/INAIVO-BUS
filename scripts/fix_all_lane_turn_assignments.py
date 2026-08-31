import xml.etree.ElementTree as ET

NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"

tree = ET.parse(NET_PATH)
root = tree.getroot()

# Fix lane turn connections for left-hand traffic (India / UK rules):
# In Left-Hand Traffic:
# Lane 0 (outer left): LEFT turns (dir="l") and STRAIGHT (dir="s") ONLY.
# Lane 1 (inner right next to divider): RIGHT turns (dir="r"), STRAIGHT (dir="s"), and U-turns (dir="T") ONLY.

modified_count = 0
for conn in root.findall('connection'):
    f = conn.get('from', '')
    t = conn.get('to', '')
    d = conn.get('dir', '')
    fl = conn.get('fromLane', '')
    tl = conn.get('toLane', '')
    
    if not f.startswith(':') and not t.startswith(':'):
        # If turning right ('r') from Lane 0 -> Move to Lane 1!
        if d == 'r' and fl == '0':
            conn.set('fromLane', '1')
            conn.set('toLane', '1')
            modified_count += 1
        # If turning left ('l') from Lane 1 -> Move to Lane 0!
        elif d == 'l' and fl == '1':
            conn.set('fromLane', '0')
            conn.set('toLane', '0')
            modified_count += 1

print(f"Fixed {modified_count} cross-lane turning conflicts in sumo.net.xml")
tree.write(NET_PATH, encoding='utf-8', xml_declaration=True)
