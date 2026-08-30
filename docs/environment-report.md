# SIH26124 Environment Report

**Date:** 2026-08-30
**Hardware Target:** NVIDIA RTX 2050 (4GB VRAM), 16GB RAM, Windows 11

## Inspection Results
- **OS:** Windows 11
- **CPU:** Intel64 Family 6 Model 141 Stepping 1
- **Python:** 3.12.13 - AVAILABLE
- **GPU:** NVIDIA GeForce RTX 2050, 4096 MiB - AVAILABLE
- **Git:** AVAILABLE
- **Node.js:** AVAILABLE
- **npm:** MISSING (Accessible via Vite/dev processes but direct npm command check failed)
- **Webots:** AVAILABLE (Installed at `C:\Users\Moghul Kannan N\AppData\Local\Programs\Webots\msys64\mingw64\bin\webotsw.exe`)
- **SUMO:** MISSING
- **SUMO_HOME:** MISSING

## Constraints & Recommendations
- **Hardware Profile:** LOW. The 4GB VRAM is a strict bottleneck.
- **Simulation Strategy:** Mock mode first. Webots will be used instead of CARLA.
- **SUMO Installation:** SUMO needs to be downloaded and installed. `SUMO_HOME` must be set.
- **Python Version:** Python 3.12 is compatible with modern AI (`ultralytics`), avoiding the dependency hell seen in previous CARLA 0.9.15 attempts. Webots officially supports Python 3.7 to 3.12 natively on Windows.
