import os

def generate_signal_face_vrml(j_id, direction_name, rotation_angle):
    d = direction_name.lower()
    
    return f"""
        # --- FACE {direction_name.upper()} ---
        Transform {{
          translation 0 0 0
          rotation 0 0 1 {rotation_angle}
          children [
            Transform {{
              translation 0 1.35 4.8
              children [
                # Signal Housing Box
                Solid {{
                  name "tl{j_id}_{d}_housing"
                  children [
                    # Main Housing
                    Shape {{
                      appearance PBRAppearance {{
                        baseColor 0.1 0.1 0.12
                        roughness 0.3
                        metalness 0.8
                      }}
                      geometry Box {{
                        size 0.75 0.28 1.45
                      }}
                    }}
                    # Yellow Border Frame (Indian Standard)
                    Shape {{
                      appearance PBRAppearance {{
                        baseColor 0.95 0.8 0.1
                        roughness 0.4
                        metalness 0.2
                      }}
                      geometry Box {{
                        size 0.82 0.02 1.52
                      }}
                    }}
                    # 1. RED LIGHT (Top)
                    LED {{
                      translation 0 0.15 0.48
                      rotation 1 0 0 1.5708
                      children [
                        Transform {{
                          translation 0 0.1 0.05
                          children [
                            Shape {{
                              appearance PBRAppearance {{ baseColor 0.05 0.05 0.05 roughness 0.2 }}
                              geometry Cylinder {{ height 0.15 radius 0.13 }}
                            }}
                          ]
                        }}
                        Shape {{
                          appearance DEF APP_RED_{j_id}_{d} PBRAppearance {{
                            baseColor 0.8 0.1 0.1
                            emissiveColor 1.0 0.1 0.1
                            roughness 0.1
                          }}
                          geometry Cylinder {{ height 0.04 radius 0.11 }}
                        }}
                      ]
                      name "tl{j_id}_{d}_red"
                      color [
                        0.15 0.02 0.02,
                        1.0 0.1 0.1
                      ]
                    }}
                    # 2. AMBER / ORANGE LIGHT (Upper Middle)
                    LED {{
                      translation 0 0.15 0.18
                      rotation 1 0 0 1.5708
                      children [
                        Transform {{
                          translation 0 0.1 0.05
                          children [
                            Shape {{
                              appearance PBRAppearance {{ baseColor 0.05 0.05 0.05 roughness 0.2 }}
                              geometry Cylinder {{ height 0.15 radius 0.13 }}
                            }}
                          ]
                        }}
                        Shape {{
                          appearance DEF APP_AMBER_{j_id}_{d} PBRAppearance {{
                            baseColor 0.85 0.5 0.05
                            emissiveColor 1.0 0.6 0.05
                            roughness 0.1
                          }}
                          geometry Cylinder {{ height 0.04 radius 0.11 }}
                        }}
                      ]
                      name "tl{j_id}_{d}_amber"
                      color [
                        0.15 0.08 0.01,
                        1.0 0.65 0.05
                      ]
                    }}
                    # 3. GREEN STRAIGHT ARROW (Center Lower)
                    LED {{
                      translation 0 0.15 -0.12
                      rotation 1 0 0 1.5708
                      children [
                        Transform {{
                          translation 0 0.1 0.05
                          children [
                            Shape {{
                              appearance PBRAppearance {{ baseColor 0.05 0.05 0.05 roughness 0.2 }}
                              geometry Cylinder {{ height 0.15 radius 0.13 }}
                            }}
                          ]
                        }}
                        Shape {{
                          appearance DEF APP_STRAIGHT_{j_id}_{d} PBRAppearance {{
                            baseColor 0.05 0.85 0.2
                            emissiveColor 0.1 1.0 0.3
                            roughness 0.1
                          }}
                          geometry Cylinder {{ height 0.04 radius 0.11 }}
                        }}
                        Transform {{
                          translation 0 0.03 0
                          rotation 1 0 0 -1.5708
                          children [
                            Shape {{
                              appearance PBRAppearance {{ baseColor 0.02 0.02 0.02 roughness 0.9 }}
                              geometry Box {{ size 0.035 0.01 0.12 }}
                            }}
                          ]
                        }}
                      ]
                      name "tl{j_id}_{d}_straight"
                      color [
                        0.01 0.12 0.03,
                        0.1 1.0 0.3
                      ]
                    }}
                    # 4. GREEN LEFT ARROW (Bottom Left - 24/7 Free Left)
                    LED {{
                      translation -0.22 0.15 -0.44
                      rotation 1 0 0 1.5708
                      children [
                        Transform {{
                          translation 0 0.1 0.05
                          children [
                            Shape {{
                              appearance PBRAppearance {{ baseColor 0.05 0.05 0.05 roughness 0.2 }}
                              geometry Cylinder {{ height 0.14 radius 0.10 }}
                            }}
                          ]
                        }}
                        Shape {{
                          appearance DEF APP_LEFT_{j_id}_{d} PBRAppearance {{
                            baseColor 0.05 0.95 0.25
                            emissiveColor 0.1 1.0 0.35
                            roughness 0.1
                          }}
                          geometry Cylinder {{ height 0.04 radius 0.085 }}
                        }}
                        Transform {{
                          translation 0 0.03 0
                          children [
                            Shape {{
                              appearance PBRAppearance {{ baseColor 0.02 0.02 0.02 roughness 0.9 }}
                              geometry Box {{ size 0.09 0.01 0.03 }}
                            }}
                          ]
                        }}
                      ]
                      name "tl{j_id}_{d}_left"
                      color [
                        0.01 0.12 0.03,
                        0.1 1.0 0.35
                      ]
                    }}
                    # 5. GREEN RIGHT ARROW (Bottom Right)
                    LED {{
                      translation 0.22 0.15 -0.44
                      rotation 1 0 0 1.5708
                      children [
                        Transform {{
                          translation 0 0.1 0.05
                          children [
                            Shape {{
                              appearance PBRAppearance {{ baseColor 0.05 0.05 0.05 roughness 0.2 }}
                              geometry Cylinder {{ height 0.14 radius 0.10 }}
                            }}
                          ]
                        }}
                        Shape {{
                          appearance DEF APP_RIGHT_{j_id}_{d} PBRAppearance {{
                            baseColor 0.05 0.95 0.25
                            emissiveColor 0.1 1.0 0.35
                            roughness 0.1
                          }}
                          geometry Cylinder {{ height 0.04 radius 0.085 }}
                        }}
                        Transform {{
                          translation 0 0.03 0
                          children [
                            Shape {{
                              appearance PBRAppearance {{ baseColor 0.02 0.02 0.02 roughness 0.9 }}
                              geometry Box {{ size 0.09 0.01 0.03 }}
                            }}
                          ]
                        }}
                      ]
                      name "tl{j_id}_{d}_right"
                      color [
                        0.01 0.12 0.03,
                        0.1 1.0 0.35
                      ]
                    }}
                  ]
                }}
              ]
            }}
          ]
        }}
    """

def generate_4way_traffic_light_vrml(name, j_id, wx, wy):
    faces = [
        generate_signal_face_vrml(j_id, "North", 0.0),
        generate_signal_face_vrml(j_id, "West", 1.570796),
        generate_signal_face_vrml(j_id, "South", 3.1415926),
        generate_signal_face_vrml(j_id, "East", -1.570796),
    ]
    
    return f"""
# ==============================================================================
# 4-WAY INDIAN TRAFFIC LIGHT TOWER: {name} (Junction {j_id})
# ==============================================================================
DEF {name} Robot {{
  translation {wx:.2f} {wy:.2f} 0.0
  children [
    # 1. Heavy Central Roundabout Island Base
    Solid {{
      name "tl{j_id}_island"
      translation 0 0 0.18
      children [
        Shape {{
          appearance PBRAppearance {{
            baseColor 0.95 0.8 0.1
            roughness 0.5
            metalness 0.1
          }}
          geometry Cylinder {{
            height 0.36
            radius 1.1
          }}
        }}
        Transform {{
          translation 0 0 0.19
          children [
            Shape {{
              appearance PBRAppearance {{
                baseColor 0.3 0.3 0.32
                roughness 0.8
              }}
              geometry Cylinder {{
                height 0.05
                radius 0.95
              }}
            }}
          ]
        }}
      ]
    }}
    # 2. Main Center Steel Mast
    Solid {{
      name "tl{j_id}_mast"
      translation 0 0 3.0
      children [
        Shape {{
          appearance PBRAppearance {{
            baseColor 0.15 0.16 0.18
            roughness 0.3
            metalness 0.85
          }}
          geometry Cylinder {{
            height 6.0
            radius 0.12
          }}
        }}
        Transform {{
          translation 0 0 3.15
          children [
            Shape {{
              appearance PBRAppearance {{
                baseColor 0.95 0.8 0.1
                roughness 0.2
                metalness 0.5
              }}
              geometry Sphere {{
                radius 0.22
              }}
            }}
          ]
        }}
      ]
    }}
    # 3. 4-Arm Cantilever Support Gantry
    Solid {{
      name "tl{j_id}_truss"
      translation 0 0 4.8
      children [
        Shape {{
          appearance PBRAppearance {{
            baseColor 0.2 0.2 0.22
            roughness 0.3
            metalness 0.8
          }}
          geometry Box {{
            size 0.1 2.8 0.1
          }}
        }}
        Shape {{
          appearance PBRAppearance {{
            baseColor 0.2 0.2 0.22
            roughness 0.3
            metalness 0.8
          }}
          geometry Box {{
            size 2.8 0.1 0.1
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
    height 6.0
    radius 1.1
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
    generate_4way_traffic_light_vrml("TRAFFIC_LIGHT_JUNCTION_25", "25", 45.0, -45.0),
    generate_4way_traffic_light_vrml("TRAFFIC_LIGHT_JUNCTION_26", "26", -45.0, 45.0),
    generate_4way_traffic_light_vrml("TRAFFIC_LIGHT_JUNCTION_27", "27", 105.0, 93.0),
]

new_content = content.rstrip() + "\n\n" + "\n".join(tls_nodes) + "\n"

with open(WBT_PATH, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Cleanly rebuilt 4-way Indian Traffic Light Towers with 100% unique Solid names in {WBT_PATH}")
