import re

path = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Add Smart Traffic Light Poles with Camera Sensors and Dense City Buildings
new_elements = """
# ── SMART CITY TRAFFIC LIGHT POLES WITH CCTV CAMERAS ───────────────────
CrossRoadsTrafficLight {
  translation -4.5 45 0
  name "traffic_light_north_cross"
}

CrossRoadsTrafficLight {
  translation -45 -4.5 0
  name "traffic_light_west_cross"
}

CrossRoadsTrafficLight {
  translation 105 -4.5 0
  name "traffic_light_east_cross"
}

Solid {
  translation -34.5 56.5 0
  name "CCTV_POLE_01"
  children [
    HighwayPole {
      height 6.0
      length 4.0
    }
    Pose {
      translation 0 0 5.5
      rotation 0 0 1 -1.5708
      children [
        Camera {
          name "TRAFFIC_CAM_NORTH"
          width 320
          height 180
          fieldOfView 1.2
        }
      ]
    }
  ]
}

Solid {
  translation 46.5 -43.5 0
  name "CCTV_POLE_02"
  children [
    HighwayPole {
      height 6.0
      length 4.0
    }
    Pose {
      translation 0 0 5.5
      rotation 0 0 1 1.5708
      children [
        Camera {
          name "TRAFFIC_CAM_CENTRAL"
          width 320
          height 180
          fieldOfView 1.2
        }
      ]
    }
  ]
}

Solid {
  translation -103.5 6.0 0
  name "CCTV_POLE_03"
  children [
    HighwayPole {
      height 6.0
      length 4.0
    }
    Pose {
      translation 0 0 5.5
      rotation 0 0 1 0.0
      children [
        Camera {
          name "TRAFFIC_CAM_WEST"
          width 320
          height 180
          fieldOfView 1.2
        }
      ]
    }
  ]
}

# ── EXPANDED COMMERCIAL & FINANCIAL DISTRICT ───────────────────────────
BigGlassTower {
  translation -85.0 -15.0 0
  name "tower_west_fin"
}

TheThreeTowers {
  translation 120.0 40.0 0
  name "towers_east_plaza"
}

CyberboticsTower {
  translation -45.0 -85.0 0
  name "cyber_tower_south"
}

Hotel {
  translation 85.0 -45.0 0
  name "grand_hotel_downtown"
}

CommercialBuilding {
  translation -15.0 -15.0 0
  name "central_metro_mall"
}

UBuilding {
  translation 15.0 -85.0 0
  name "tech_hub_u_building"
}

HollowBuilding {
  translation -85.0 45.0 0
  name "civic_plaza_building"
}

Auditorium {
  translation 40.0 120.0 0
  name "city_auditorium_north"
}

Museum {
  translation -60.0 120.0 0
  name "metropolitan_museum"
}

ResidentialBuilding {
  translation 120.0 -45.0 0
  name "residential_park_east"
}

ResidentialBuilding {
  translation -120.0 -45.0 0
  name "residential_quarter_west"
}

FastFoodRestaurant {
  translation -35.0 15.0 0
  name "downtown_diner"
  brand "subway"
  height 4.3
  length 13
  width 12
}

FastFoodRestaurant {
  translation 15.0 85.0 0
  name "uptown_bistro"
  brand "subway"
  height 4.3
  length 13
  width 12
}

SimpleBuilding {
  translation -115.0 85.0 0
  name "highrise_northwest"
  wallType "glass highrise"
  floorNumber 12
}

SimpleBuilding {
  translation 115.0 85.0 0
  name "highrise_northeast"
  wallType "gray glass building"
  floorNumber 10
}

SimpleBuilding {
  translation -115.0 -85.0 0
  name "office_complex_southwest"
  wallType "classic building"
  floorNumber 8
}

SimpleBuilding {
  translation 115.0 -125.0 0
  name "corporate_park_southeast"
  wallType "highrise"
  floorNumber 14
}

SpeedLimitSign {
  translation -52.0 48.0 0
  signBoards [
    SpeedLimitPanel {
      speed "50"
    }
  ]
}

SpeedLimitSign {
  translation 32.0 8.0 0
  signBoards [
    SpeedLimitPanel {
      speed "30"
    }
  ]
}

CautionSign {
  translation -32.0 52.0 0
  signBoards [
    CautionPanel {
      type "pedestrian"
    }
  ]
}
"""

# Insert before DEF PEDESTRIAN_01
if "CCTV_POLE_01" not in content:
    target = "DEF PEDESTRIAN_01 Pedestrian"
    content = content.replace(target, new_elements + "\n" + target)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Expanded city map with smart traffic light poles, CCTV cameras, and dense architecture successfully!")
