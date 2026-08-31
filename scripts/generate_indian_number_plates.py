"""
number_plate_manager.py — Deterministic Indian License Plate Generator.

Format:
[State Code 2-letters] [RTO Code 2-digits] [Series 2-letters] [Vehicle Number 4-digits]
Examples:
  TN 07 AB 1001
  KA 05 CD 2024
  MH 12 EF 3055
  DL 08 GH 4099
  TS 09 JK 5123
  GJ 01 LM 6789
  KL 07 NP 7410
  AP 03 QR 8521
  WB 02 ST 9632
  HR 26 UV 1593
"""

INDIAN_STATES = ["TN", "KA", "MH", "DL", "TS", "GJ", "KL", "AP", "WB", "HR"]
SERIES = ["AB", "CD", "EF", "GH", "JK", "LM", "NP", "QR", "ST", "UV", "WX", "YZ"]

def get_unique_indian_plate(vehicle_index):
    state = INDIAN_STATES[vehicle_index % len(INDIAN_STATES)]
    rto = f"{(vehicle_index * 3 + 1) % 99 + 1:02d}"
    series = SERIES[(vehicle_index // len(INDIAN_STATES)) % len(SERIES)]
    num = f"{(vehicle_index * 127 + 1001) % 9000 + 1000:04d}"
    return f"{state} {rto} {series} {num}"

if __name__ == "__main__":
    for i in range(100):
        print(f"Vehicle {i:3d}: {get_unique_indian_plate(i)}")
