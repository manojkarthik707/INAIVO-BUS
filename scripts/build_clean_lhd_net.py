import xml.etree.ElementTree as ET
import subprocess

CON_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\plain.con.xml"
CFG_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\plain.netccfg"
NET_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.net.xml"

# Build pristine plain.con.xml with standard connections + shortcut connections
# Standard non-shortcut connections:
standard_conns = [
    # 26:
    {'from': '-0', 'to': '-1'},
    {'from': '-24', 'to': '-7'},
    {'from': '-24', 'to': '23'},
    {'from': '-24', 'to': '-0'},
    {'from': '-7', 'to': '23'},
    {'from': '0', 'to': '-7'},
    {'from': '0', 'to': '24'},
    {'from': '0', 'to': '23'},
    {'from': '-23', 'to': '24'},
    {'from': '-23', 'to': '-7'},
    {'from': '-23', 'to': '-0'},
    {'from': '7', 'to': '-0'},
    
    # 25:
    {'from': '-10', 'to': '17'},
    {'from': '10', 'to': '4'},
    {'from': '10', 'to': '-5'},
    {'from': '10', 'to': '9'},
    {'from': '-4', 'to': '-5'},
    {'from': '4', 'to': '10'},
    {'from': '4', 'to': '9'},
    {'from': '5', 'to': '4'},
    {'from': '5', 'to': '10'},
    {'from': '5', 'to': '9'},
    {'from': '-9', 'to': '4'},
    {'from': '-9', 'to': '-5'},
    {'from': '-9', 'to': '10'},
    {'from': '9', 'to': '-5'},

    # 27:
    {'from': '-12', 'to': '-18'},
    {'from': '-16', 'to': '20'},
    {'from': '-16', 'to': '-17'},
    {'from': '-16', 'to': '12'},
    {'from': '-17', 'to': '-18'},
    {'from': '17', 'to': '16'},
    {'from': '17', 'to': '20'},
    {'from': '17', 'to': '12'},
    {'from': '-20', 'to': '16'},
    {'from': '-20', 'to': '-17'},
    {'from': '-20', 'to': '12'},
    {'from': '12', 'to': '-17'},

    # Arterials (41, 42, 43, 44, outer curves):
    {'from': '8', 'to': '-23'},
    {'from': '23', 'to': '-8'},
    {'from': '-5', 'to': '-6'},
    {'from': '6', 'to': '5'},
    {'from': '7', 'to': '6'},
    {'from': '-6', 'to': '-7'},
    {'from': '-8', 'to': '9'},
    {'from': '-9', 'to': '8'},
    {'from': '-2', 'to': '3'},
    {'from': '-3', 'to': '2'},
    {'from': '-1', 'to': '2'},
    {'from': '-2', 'to': '1'},
    {'from': '24', 'to': '22'},
    {'from': '-22', 'to': '-24'},
    {'from': '22', 'to': '21'},
    {'from': '-21', 'to': '-22'},
    {'from': '21', 'to': '18'},
    {'from': '-18', 'to': '-21'},
    {'from': '18', 'to': '19'},
    {'from': '-19', 'to': '-18'},
    {'from': '19', 'to': '16'},
    {'from': '-16', 'to': '-19'},
    {'from': '20', 'to': '14'},
    {'from': '-14', 'to': '-20'},
    {'from': '14', 'to': '11'},
    {'from': '-11', 'to': '-14'},
    {'from': '11', 'to': '13'},
    {'from': '-13', 'to': '-11'},

    # Shortcut road:
    {'from': '8', 'to': 'shortcut_east'},
    {'from': '23', 'to': 'shortcut_east'},
    {'from': 'shortcut_west', 'to': '-8'},
    {'from': 'shortcut_west', 'to': '-23'},
    {'from': 'shortcut_east', 'to': '5'},
    {'from': 'shortcut_east', 'to': '-6'},
    {'from': '-5', 'to': 'shortcut_west'},
    {'from': '6', 'to': 'shortcut_west'},
]

root_con = ET.Element('connections', {'version': '1.20'})
for c in standard_conns:
    ET.SubElement(root_con, 'connection', c)

tree_con = ET.ElementTree(root_con)
tree_con.write(CON_PATH, encoding='utf-8', xml_declaration=True)

cmd = [
    r"C:\Program Files (x86)\Eclipse\Sumo\bin\netconvert.exe",
    "-c", CFG_PATH,
    "--lefthand", "true",
    "--no-turnarounds", "true",
    "--no-turnarounds.tls", "true",
    "--tls.ignore-internal-junction-jam", "true",
    "-o", NET_PATH
]
res = subprocess.run(cmd, capture_output=True, text=True)
print("netconvert output:\n", res.stdout, res.stderr)

tree_net = ET.parse(NET_PATH)
root_net = tree_net.getroot()
for lane in root_net.findall('.//lane'):
    if not lane.get('id', '').startswith(':'):
        ET.SubElement(lane, 'stopOffset', {'value': '6.0'})

for conn in root_net.findall('connection'):
    conn.set('keepClear', '1')

tree_net.write(NET_PATH, encoding='utf-8', xml_declaration=True)
print("Built pristine Indian LHD network with full throughput!")
