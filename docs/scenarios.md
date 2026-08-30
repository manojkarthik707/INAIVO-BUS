# Scenarios

Scenario files are under `simulation/configs`. Each declares environment, traffic, bus, incident and sensor settings.

- `pedestrian_crossing`: a person enters the road region while BUS_01 approaches.
- `red_light`: VEHICLE_17 crosses a stop line while the signal is red.
- `congestion`: high occupancy and low average speed produce a congestion score.
- `pothole`: a configured road hazard enters the bus camera region.

Mock scenarios run for several seconds and emit one deterministic validation event. CARLA implementations can reuse the same configuration and output contract.

