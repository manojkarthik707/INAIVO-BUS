# SUMO to Webots coordinate conversion (Webots uses Z-up ENU):
# Webots X = SUMO_x - 175.0
# Webots Y = SUMO_y - 187.51
# Webots Z = 0.0

TLS_JUNCTIONS = {
    "25": (220.00, 142.51),   # Inner top-right 4-way
    "26": (130.00, 232.51),   # Inner top-left 4-way
    "27": (280.00, 280.51),   # Inner right 4-way
    "41": (130.00, 183.01),   # T-junction inner left
    "43": (220.00, 192.01),   # T-junction inner center
    "44": (179.50, 232.51),   # T-junction inner center-left
    "45": (280.00, 183.01),   # T-junction inner right
}

NET_OFFSET_X = 175.00
NET_OFFSET_Y = 187.51

print("Correct Webots coordinates for TrafficLight placement:")
for jid, (sx, sy) in TLS_JUNCTIONS.items():
    wx = sx - NET_OFFSET_X
    wy = sy - NET_OFFSET_Y
    print(f"Junction {jid}: translation {wx:.2f} {wy:.2f} 0.0")
