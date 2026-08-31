import os

def generate_sleek_face_vrml(j_id, direction_name, rotation_angle):
    d = direction_name.lower()
    
    # 4 clean vertical lenses per face:
    # 1. Red (Z = +0.38)
    # 2. Amber (Z = +0.13)
    # 3. Green Straight (Z = -0.13)
    # 4. Green Left Arrow (Z = -0.38) - 24/7 Free Left
    
    return f"""
        # --- FACE {direction_name.upper()} ---
        Transform {{
          translation 0 0 0
          rotation 0 0 1 {rotation_angle}
          children [
            Transform {{
              translation 0 0.28 3.8
              children [
                # Signal Housing
                Solid {{
                  name "tl{j_id}_{d}_housing"
                  children [
                    # Main Black Polycarbonate Body
                    Shape {{
                      appearance PBRAppearance {{
                        baseColor 0.1 0.1 0.12
                        roughness 0.4
                        metalness 0.1
                      }}
                      geometry Box {{
                        size 0.34 0.18 1.15
                      }}
                    }}
                    # Clean Yellow Border Trim
                    Transform {{
                      translation 0 -0.01 0
                      children [
                        Shape {{
                          appearance PBRAppearance {{
                            baseColor 0.95 0.75 0.1
                            roughness 0.3
                            metalness 0.2
                          }}
                          geometry Box {{
                            size 0.38 0.02 1.20
                          }}
                        }}
                      ]
                    }}
                    # 1. RED LENS (Top, Z=+0.38)
                    Transform {{
                      translation 0 0.09 0.38
                      rotation 1 0 0 1.5708
                      children [
                        # Visor Hood
                        Transform {{
                          translation 0 0.04 -0.04
                          rotation 1 0 0 0.2
                          children [
                            Shape {{
                              appearance PBRAppearance {{ baseColor 0.08 0.08 0.08 roughness 0.5 }}
                              geometry Cylinder {{ height 0.09 radius 0.12 }}
                            }}
                          ]
                        }}
                        LED {{
                          name "tl{j_id}_{d}_red"
                          color [
                            0.15 0.02 0.02, # OFF
                            1.0 0.08 0.08   # ON (Bright Red)
                          ]
                          children [
                            Shape {{
                              appearance DEF APP_RED_{j_id}_{d} PBRAppearance {{
                                baseColor 0.8 0.1 0.1
                                emissiveColor 0.15 0.02 0.02
                                roughness 0.2
                              }}
                              geometry Cylinder {{ height 0.02 radius 0.095 }}
                            }}
                          ]
                        }}
                      ]
                    }}
                    # 2. AMBER LENS (Z=+0.13)
                    Transform {{
                      translation 0 0.09 0.13
                      rotation 1 0 0 1.5708
                      children [
                        Transform {{
                          translation 0 0.04 -0.04
                          rotation 1 0 0 0.2
                          children [
                            Shape {{
                              appearance PBRAppearance {{ baseColor 0.08 0.08 0.08 roughness 0.5 }}
                              geometry Cylinder {{ height 0.09 radius 0.12 }}
                            }}
                          ]
                        }}
                        LED {{
                          name "tl{j_id}_{d}_amber"
                          color [
                            0.15 0.08 0.01, # OFF
                            1.0 0.65 0.05   # ON (Bright Amber)
                          ]
                          children [
                            Shape {{
                              appearance DEF APP_AMBER_{j_id}_{d} PBRAppearance {{
                                baseColor 0.85 0.55 0.05
                                emissiveColor 0.15 0.08 0.01
                                roughness 0.2
                              }}
                              geometry Cylinder {{ height 0.02 radius 0.095 }}
                            }}
                          ]
                        }}
                      ]
                    }}
                    # 3. GREEN STRAIGHT LENS (Z=-0.13)
                    Transform {{
                      translation 0 0.09 -0.13
                      rotation 1 0 0 1.5708
                      children [
                        Transform {{
                          translation 0 0.04 -0.04
                          rotation 1 0 0 0.2
                          children [
                            Shape {{
                              appearance PBRAppearance {{ baseColor 0.08 0.08 0.08 roughness 0.5 }}
                              geometry Cylinder {{ height 0.09 radius 0.12 }}
                            }}
                          ]
                        }}
                        LED {{
                          name "tl{j_id}_{d}_straight"
                          color [
                            0.01 0.12 0.03, # OFF
                            0.1 1.0 0.3     # ON (Bright Green)
                          ]
                          children [
                            Shape {{
                              appearance DEF APP_STRAIGHT_{j_id}_{d} PBRAppearance {{
                                baseColor 0.05 0.85 0.2
                                emissiveColor 0.01 0.12 0.03
                                roughness 0.2
                              }}
                              geometry Cylinder {{ height 0.02 radius 0.095 }}
                            }}
                          ]
                        }}
                      ]
                    }}
                    # 4. GREEN LEFT ARROW LENS (Bottom, Z=-0.38) - 24/7 FREE LEFT
                    Transform {{
                      translation 0 0.09 -0.38
                      rotation 1 0 0 1.5708
                      children [
                        Transform {{
                          translation 0 0.04 -0.04
                          rotation 1 0 0 0.2
                          children [
                            Shape {{
                              appearance PBRAppearance {{ baseColor 0.08 0.08 0.08 roughness 0.5 }}
                              geometry Cylinder {{ height 0.09 radius 0.12 }}
                            }}
                          ]
                        }}
                        LED {{
                          name "tl{j_id}_{d}_left"
                          color [
                            0.01 0.12 0.03, # OFF
                            0.1 1.0 0.35    # ON (Bright Green Left Arrow)
                          ]
                          children [
                            Shape {{
                              appearance DEF APP_LEFT_{j_id}_{d} PBRAppearance {{
                                baseColor 0.05 0.95 0.25
                                emissiveColor 0.1 1.0 0.35
                                roughness 0.2
                              }}
                              geometry Cylinder {{ height 0.02 radius 0.095 }}
                            }}
                          ]
                        }}
                      ]
                    }}
                  ]
                }}
              ]
            }}
          ]
        }}
    """

def generate_clean_4way_traffic_light_vrml(name, j_id, wx, wy):
    faces = [
        generate_sleek_face_vrml(j_id, "North", 0.0),
        generate_sleek_face_vrml(j_id, "West", 1.570796),
        generate_sleek_face_vrml(j_id, "South", 3.1415926),
        generate_sleek_face_vrml(j_id, "East", -1.570796),
    ]
    
    return f"""
# ==============================================================================
# SLEEK 4-WAY INDIAN TRAFFIC LIGHT POST: {name} (Junction {j_id})
# ==============================================================================
DEF {name} Robot {{
  translation {wx:.2f} {wy:.2f} 0.0
  children [
    # 1. Compact Central Roundabout Island Base
    Solid {{
      name "tl{j_id}_island"
      translation 0 0 0.15
      children [
        Shape {{
          appearance PBRAppearance {{
            baseColor 0.95 0.75 0.1
            roughness 0.6
            metalness 0.1
          }}
          geometry Cylinder {{
            height 0.30
            radius 0.75
          }}
        }}
        Transform {{
          translation 0 0 0.16
          children [
            Shape {{
              appearance PBRAppearance {{
                baseColor 0.25 0.25 0.28
                roughness 0.8
              }}
              geometry Cylinder {{
                height 0.04
                radius 0.68
              }}
            }}
          ]
        }}
      ]
    }}
    # 2. Sleek Central Steel Mast Pole
    Solid {{
      name "tl{j_id}_mast"
      translation 0 0 2.25
      children [
        Shape {{
          appearance PBRAppearance {{
            baseColor 0.18 0.19 0.22
            roughness 0.3
            metalness 0.85
          }}
          geometry Cylinder {{
            height 4.5
            radius 0.09
          }}
        }}
        # Top Mast Finial Cap
        Transform {{
          translation 0 0 2.32
          children [
            Shape {{
              appearance PBRAppearance {{
                baseColor 0.95 0.75 0.1
                roughness 0.2
                metalness 0.5
              }}
              geometry Sphere {{
                radius 0.14
              }}
            }}
          ]
        }}
      ]
    }}
    # 3. Compact 4-Way Center Mounting Collar
    Solid {{
      name "tl{j_id}_collar"
      translation 0 0 3.8
      children [
        Shape {{
          appearance PBRAppearance {{
            baseColor 0.15 0.16 0.18
            roughness 0.3
            metalness 0.8
          }}
          geometry Cylinder {{
            height 0.3
            radius 0.16
          }}
        }}
      ]
    }}
    {"".join(faces)}
  ]
  name "{name.lower()}"
  controller "traffic_light_controller"
  supervisor TRUE
  boundingObject Cylinder {{
    height 4.5
    radius 0.75
  }}
  locked TRUE
}}
"""

WBT_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt"

with open(WBT_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find("# ==============================================================================")
if idx != -1:
    content = content[:idx]

tls_nodes = [
    generate_clean_4way_traffic_light_vrml("TRAFFIC_LIGHT_JUNCTION_25", "25", 45.0, -45.0),
    generate_clean_4way_traffic_light_vrml("TRAFFIC_LIGHT_JUNCTION_26", "26", -45.0, 45.0),
    generate_clean_4way_traffic_light_vrml("TRAFFIC_LIGHT_JUNCTION_27", "27", 105.0, 93.0),
]

new_content = content.rstrip() + "\n\n" + "\n".join(tls_nodes) + "\n"

with open(WBT_PATH, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Cleanly built sleek, professional 4-way Indian Traffic Light Posts in {WBT_PATH}")
