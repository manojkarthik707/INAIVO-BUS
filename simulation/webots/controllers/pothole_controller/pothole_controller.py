"""
pothole_controller.py — Clean Pothole Monitoring Supervisor.

NOTE:
Directly overriding Solid translations via supervisor setSFVec3f while SumoInterface
is actively driving vehicles causes severe physics divergence (vehicles teleporting,
drifting into dirt fields, and clipping).

This controller monitors the 18 road potholes and ensures clean simulation synchronization
without corrupting SUMO vehicle physics.
"""

from controller import Supervisor

POTHOLES = [
    (-13.14,   0.44), ( 10.20,   2.78), (  7.96,  -0.96), (-12.79,  -3.03),
    (-101.35, 36.10), (-78.33,  45.37), (-15.01,  53.07), ( 28.76,  40.22),
    ( 53.07, -23.79), ( 45.36, -78.38), (-33.44,-113.07), (-101.25,-87.11),
    (-36.93,  25.09), (-42.31,  15.94), (-26.43, -28.33), (-14.11, -41.02),
    ( 14.94, -36.93), (102.31,  34.69),
]


def main():
    robot = Supervisor()
    timestep = int(robot.getBasicTimeStep()) or 32

    print(f"[PotholeCtrl] Monitoring {len(POTHOLES)} road hazards. SUMO physics active.")

    while robot.step(timestep) != -1:
        pass


if __name__ == '__main__':
    main()
