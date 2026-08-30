import os
import sys
import platform
import subprocess
import json

def check_command(cmd, name):
    try:
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
        return "AVAILABLE"
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return "MISSING"

def get_gpu_info():
    try:
        res = subprocess.run(['nvidia-smi', '--query-gpu=name,memory.total', '--format=csv,noheader'], capture_output=True, text=True)
        if res.returncode == 0:
            return res.stdout.strip()
        return "NVIDIA GPU Not Found or nvidia-smi missing"
    except FileNotFoundError:
        return "MISSING"

report = {
    "OS": platform.system() + " " + platform.release(),
    "CPU": platform.processor(),
    "Python": sys.version.split(' ')[0],
    "GPU": get_gpu_info(),
    "Git": check_command(["git", "--version"], "Git"),
    "Node": check_command(["node", "--version"], "Node"),
    "npm": check_command(["npm", "--version"], "npm"),
    "Webots": check_command(["C:\\Users\\Moghul Kannan N\\AppData\\Local\\Programs\\Webots\\msys64\\mingw64\\bin\\webotsw.exe", "--version"], "Webots"),
    "SUMO": check_command(["sumo", "--version"], "SUMO"),
    "SUMO_HOME": os.environ.get("SUMO_HOME", "MISSING")
}

print(json.dumps(report, indent=2))
