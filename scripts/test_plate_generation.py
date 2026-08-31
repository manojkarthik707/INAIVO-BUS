import math

INDIAN_STATES = ["TN", "KA", "MH", "DL", "TS", "GJ", "KL", "AP", "WB", "HR"]
SERIES = ["AB", "CD", "EF", "GH", "JK", "LM", "NP", "QR", "ST", "UV", "WX", "YZ"]

def get_unique_indian_plate(vehicle_idx):
    state = INDIAN_STATES[vehicle_idx % len(INDIAN_STATES)]
    rto = f"{(vehicle_idx * 3 + 1) % 99 + 1:02d}"
    series = SERIES[(vehicle_idx // len(INDIAN_STATES)) % len(SERIES)]
    num = f"{(vehicle_idx * 127 + 1001) % 9000 + 1000:04d}"
    return f"{state} {rto} {series} {num}"

for i in range(10):
    print(f"Vehicle {i:2d} -> {get_unique_indian_plate(i)}")
