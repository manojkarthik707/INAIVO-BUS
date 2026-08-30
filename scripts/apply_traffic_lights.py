import subprocess
import os

net_dir = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net"

cmd = [
    r"C:\Program Files (x86)\Eclipse\Sumo\bin\netconvert.exe",
    "--node-files", os.path.join(net_dir, "plain.nod.xml"),
    "--edge-files", os.path.join(net_dir, "plain.edg.xml"),
    "--connection-files", os.path.join(net_dir, "plain.con.xml"),
    "--offset.disable-normalization", "true",
    "--no-turnarounds", "true",
    "--tls.guess", "true",               # Automatically signalize all intersections
    "--tls.green.time", "15",            # 15-second green time per direction
    "--tls.yellow.time", "3",            # 3-second yellow clearance
    "--tls.allred.time", "1",            # 1-second all-red intersection clearance
    "-o", os.path.join(net_dir, "sumo.net.xml")
]

subprocess.run(cmd, check=True)
print("Successfully generated fully signalized, coordinated traffic light network in sumo.net.xml!")
