"""
camera_streamer.py — Internal Webots camera controller.

This runs INSIDE the Webots process (not as an extern controller).
Direct C-API access to the camera: no MMF, no IPC, no Windows handle leaks.

Each CAM_ROBOT_1 / CAM_ROBOT_2 / CAM_ROBOT_3 node uses this as its
controller with controllerArgs ["BUS_01"], ["BUS_02"], ["BUS_03"].

The script grabs camera frames and HTTP POSTs them to the backend.
"""

import sys
import time
import base64
import requests
import numpy as np

# Webots controller API (available inside Webots process)
from controller import Robot

BACKEND_URL = "http://127.0.0.1:8000"

def main():
    robot = Robot()
    timestep = int(robot.getBasicTimeStep())

    # Bus ID is passed via controllerArgs, e.g. "BUS_01"
    bus_id = robot.getName()  # robot name IS the bus id
    if sys.argv and len(sys.argv) > 1:
        bus_id = sys.argv[1]

    print(f"[camera_streamer] {bus_id}: starting, timestep={timestep}ms", flush=True)

    # Get devices
    cam = robot.getDevice("camera")
    gps = robot.getDevice("gps")

    if not cam:
        print(f"[camera_streamer] {bus_id}: ERROR - no 'camera' device found", flush=True)
        while robot.step(timestep) != -1:
            pass
        return

    cam.enable(timestep)
    if gps:
        gps.enable(timestep)

    print(f"[camera_streamer] {bus_id}: camera enabled {cam.getWidth()}x{cam.getHeight()}", flush=True)

    session = requests.Session()
    frame_interval = 0.033   # ~30 FPS
    last_post = 0.0
    frame_count = 0
    error_count = 0

    while robot.step(timestep) != -1:
        now = time.time()
        if now - last_post < frame_interval:
            continue
        last_post = now

        try:
            raw = cam.getImage()
            if raw is None:
                continue

            h = cam.getHeight()
            w = cam.getWidth()

            # BGRA → BGR numpy array
            arr = np.frombuffer(raw, dtype=np.uint8).reshape((h, w, 4)).copy()
            bgr = arr[:, :, :3]

            # JPEG encode
            import cv2
            ok, buf = cv2.imencode(".jpg", bgr, [cv2.IMWRITE_JPEG_QUALITY, 85])
            if not ok:
                continue

            frame_b64 = base64.b64encode(buf).decode("utf-8")

            location = {"latitude": 11.0168, "longitude": 76.9558}
            if gps:
                try:
                    v = gps.getValues()
                    if v and len(v) >= 3:
                        location = {
                            "latitude":  11.0168 + v[0] * 0.0001,
                            "longitude": 76.9558 + v[2] * 0.0001,
                        }
                except Exception:
                    pass

            telemetry = {
                "bus_id":    bus_id,
                "timestamp": now,
                "latitude":  location["latitude"],
                "longitude": location["longitude"],
                "speed":     30.0,
                "status":    "active",
                "frame":     frame_b64,
            }

            try:
                session.post(
                    f"{BACKEND_URL}/api/buses/{bus_id}/telemetry",
                    json=telemetry,
                    timeout=0.5,
                )
                frame_count += 1
                if frame_count % 100 == 0:
                    print(f"[camera_streamer] {bus_id}: {frame_count} frames sent", flush=True)
            except Exception as e:
                error_count += 1
                if error_count % 30 == 1:
                    print(f"[camera_streamer] {bus_id}: POST error: {e}", flush=True)

        except Exception as e:
            print(f"[camera_streamer] {bus_id}: frame error: {e}", flush=True)

if __name__ == "__main__":
    main()
