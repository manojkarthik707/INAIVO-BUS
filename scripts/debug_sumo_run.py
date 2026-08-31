import subprocess

cmd = [
    r"C:\Program Files (x86)\Eclipse\Sumo\bin\sumo.exe",
    "-c", r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic_net\sumo.sumocfg",
    "--step-length", "0.032",
    "-e", "60",
    "-v"
]

res = subprocess.run(cmd, capture_output=True, text=True)
print("Return code:", res.returncode)
print("=== STDOUT ===")
print(res.stdout)
print("=== STDERR ===")
print(res.stderr)
