"""
Indian Road Traffic Laws for SUMO Simulation:
1. LEFT-HAND TRAFFIC (vehicles drive on left side, overtake on right)
2. Urban speed limits: 50 km/h cars, 40 km/h buses/trucks
3. Aggressive close-following (smaller gaps, tau ~0.8s)
4. Left-turn-on-red allowed (free left turn = Indian 'left turn free')
5. Horn-and-cut lane behavior (higher lane change frequency)
6. Mixed traffic yielding at intersections
7. Roundabout priority: vehicles inside have right of way
8. Pedestrian crossings at signals
"""

import subprocess
import os
import xml.etree.ElementTree as ET

net_dir = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net"

# === STEP 1: Rebuild network with LEFT-HAND traffic ===
cmd = [
    r"C:\Program Files (x86)\Eclipse\Sumo\bin\netconvert.exe",
    "--node-files",       os.path.join(net_dir, "plain.nod.xml"),
    "--edge-files",       os.path.join(net_dir, "plain.edg.xml"),
    "--connection-files", os.path.join(net_dir, "plain.con.xml"),

    "--offset.disable-normalization", "true",
    "--no-turnarounds",   "true",

    # ===== LEFT-HAND TRAFFIC (INDIA DRIVES ON THE LEFT) =====
    "--lefthand",         "true",

    # Traffic lights
    "--tls.green.time",   "18",
    "--tls.yellow.time",  "3",
    "--tls.allred.time",  "2",
    "--tls.default-type", "actuated",

    # Junction smooth turn geometry
    "--junctions.corner-detail",       "16",
    "--junctions.limit-turn-speed",    "4.5",
    "--junctions.small-radius",        "1.5",
    "--junctions.internal-link-detail","10",
    "--geometry.min-radius",           "3.0",
    "--geometry.min-radius.fix",       "true",

    "-o", os.path.join(net_dir, "sumo.net.xml")
]

result = subprocess.run(cmd, capture_output=True, text=True)
print("STDOUT:", result.stdout)
if result.returncode != 0:
    print("STDERR:", result.stderr[:3000])
    raise RuntimeError("netconvert failed")

print("Step 1 done: Left-hand traffic network compiled!")


# === STEP 2: Generate Indian-behavior vehicle types in sumo.rou.xml ===
# Indian road physics:
# - smaller tau (aggressive following): 0.8s instead of 1.1s
# - smaller minGap (bumper-to-bumper typical): 1.5m instead of 3m
# - higher max speed variance: sigma=0.9 (Indian drivers vary greatly)
# - higher accel (Indian driving is aggressive at green lights)
# - speedFactor distribution: mean 1.1 (slight speeding is norm)

rou_path = os.path.join(net_dir, "sumo.rou.xml")
tree = ET.parse(rou_path)
root = tree.getroot()

# Update vType elements to Indian driving behavior
for vt in root.findall("vType"):
    vid = vt.get("id")
    if vid == "passenger":
        # Indian city car: aggressive, small gaps, frequent lane changes
        vt.set("carFollowModel",  "IDM")
        vt.set("accel",           "2.8")     # snappy acceleration at green
        vt.set("decel",           "5.0")     # hard brake (Indian roads need it!)
        vt.set("tau",             "0.8")     # very close following (aggressive)
        vt.set("minGap",          "1.5")     # Indian bumper-to-bumper gap
        vt.set("maxSpeed",        "13.89")   # 50 km/h urban speed limit
        vt.set("speedFactor",     "1.1")     # slight speeding (typical in India)
        vt.set("speedDev",        "0.15")    # high speed variance
        vt.set("sigma",           "0.9")     # aggressive/erratic behavior
        vt.set("lcStrategic",     "1.5")     # frequent lane changes
        vt.set("lcSpeedGain",     "1.5")     # cut in for speed advantage
        vt.set("lcCooperative",   "0.3")     # less cooperative yielding
        vt.set("lcAssertive",     "2.0")     # assertive gap acceptance
        vt.set("lcImpatience",    "0.9")     # high impatience (honk & go!)
        vt.set("jmIgnoreKeepClearTime", "2.0")  # block box junction slightly (Indian style)
        vt.set("jmDriveAfterYellowTime", "2.0") # drive through yellow (typical India)
    elif vid == "bus":
        # Indian city bus: large, slower, stops frequently
        vt.set("carFollowModel",  "IDM")
        vt.set("accel",           "1.2")     # slow acceleration (heavy bus)
        vt.set("decel",           "3.5")     # moderate braking
        vt.set("tau",             "1.0")     # moderate following distance
        vt.set("minGap",          "2.0")     # slightly larger gap for bus
        vt.set("maxSpeed",        "11.11")   # 40 km/h urban bus speed limit (India)
        vt.set("speedFactor",     "1.0")     # buses usually follow limit
        vt.set("speedDev",        "0.1")
        vt.set("sigma",           "0.6")
        vt.set("lcStrategic",     "1.0")
        vt.set("lcSpeedGain",     "0.8")
        vt.set("lcCooperative",   "0.5")
        vt.set("jmDriveAfterYellowTime", "1.5")  # buses also run yellow (India)

tree.write(rou_path, encoding="utf-8", xml_declaration=True)
print("Step 2 done: Indian vehicle behavior parameters applied!")


# === STEP 3: Validate ===
result = subprocess.run([
    r"C:\Program Files (x86)\Eclipse\Sumo\bin\sumo.exe",
    "-c", os.path.join(net_dir, "sumo.sumocfg"),
    "--no-step-log", "--end", "100"
], capture_output=True, text=True)

print("Validation output:")
print(result.stdout[-800:])
if result.returncode != 0:
    print("ERRORS:", result.stderr[:1000])
else:
    print("Indian road traffic simulation validated successfully!")
