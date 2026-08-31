import os

def generate_unblocked_5aspect_face(j_id, direction_name, rotation_angle):
    d = direction_name.upper()
    
    # 5 unblocked forward-facing LED lenses (Proper Driver Perspective):
    # From driver looking at the face:
    # Top: Red (Z = +0.42)
    # Upper-Mid: Amber (Z = +0.14)
    # Center-Mid: Straight Green Arrow (Z = -0.14)
    # Bottom-Left (Driver's Left): Left Green Arrow (X = +0.18, Z = -0.42) -> 24/7 FREE LEFT
    # Bottom-Right (Driver's Right): Right Green Arrow (X = -0.18, Z = -0.42)
    
    return f"""
        # --- FACE {direction_name.upper()} ---
        Transform {{
          translation 0 0 0
          rotation 0 0 1 {rotation_angle}
          children [
            Transform {{
              translation 0 0.36 3.9
              children [
                # Signal Housing Box
                Solid {{
                  name "tl{j_id}_{direction_name.lower()}_housing"
                  children [
                    # Main Black Polycarbonate Body
                    Shape {{
                      appearance PBRAppearance {{
                        baseColor 0.08 0.08 0.10
                        roughness 0.5
                        metalness 0.1
                      }}
                      geometry Box {{
                        size 0.64 0.16 1.28
                      }}
                    }}
                    # Yellow Border Frame
                    Transform {{
                      translation 0 -0.01 0
                      children [
                        Shape {{
                          appearance PBRAppearance {{
                            baseColor 0.95 0.75 0.05
                            roughness 0.3
                            metalness 0.2
                          }}
                          geometry Box {{
                            size 0.70 0.02 1.34
                          }}
                        }}
                      ]
                    }}
                    # 1. RED LENS (Top, Z=+0.42)
                    Transform {{
                      translation 0 0.085 0.42
                      rotation 1 0 0 1.5708
                      children [
                        # Visor Cap
                        Transform {{
                          translation 0 0.10 -0.04
                          rotation 1 0 0 -0.35
                          children [
                            Shape {{
                              appearance PBRAppearance {{ baseColor 0.05 0.05 0.05 roughness 0.5 }}
                              geometry Box {{ size 0.22 0.12 0.02 }}
                            }}
                          ]
                        }}
                        Shape {{
                          appearance DEF MAT_{j_id}_{d}_RED PBRAppearance {{
                            baseColor 1.0 0.1 0.1
                            emissiveColor 1.0 0.1 0.1
                            roughness 0.1
                          }}
                          geometry Cylinder {{ height 0.03 radius 0.095 }}
                        }}
                      ]
                    }}
                    # 2. AMBER LENS (Upper Mid, Z=+0.14)
                    Transform {{
                      translation 0 0.085 0.14
                      rotation 1 0 0 1.5708
                      children [
                        Transform {{
                          translation 0 0.10 -0.04
                          rotation 1 0 0 -0.35
                          children [
                            Shape {{
                              appearance PBRAppearance {{ baseColor 0.05 0.05 0.05 roughness 0.5 }}
                              geometry Box {{ size 0.22 0.12 0.02 }}
                            }}
                          ]
                        }}
                        Shape {{
                          appearance DEF MAT_{j_id}_{d}_AMBER PBRAppearance {{
                            baseColor 1.0 0.65 0.05
                            emissiveColor 0.1 0.05 0.0
                            roughness 0.1
                          }}
                          geometry Cylinder {{ height 0.03 radius 0.095 }}
                        }}
                      ]
                    }}
                    # 3. GREEN STRAIGHT ARROW (Center, Z=-0.14)
                    Transform {{
                      translation 0 0.085 -0.14
                      rotation 1 0 0 1.5708
                      children [
                        Transform {{
                          translation 0 0.10 -0.04
                          rotation 1 0 0 -0.35
                          children [
                            Shape {{
                              appearance PBRAppearance {{ baseColor 0.05 0.05 0.05 roughness 0.5 }}
                              geometry Box {{ size 0.22 0.12 0.02 }}
                            }}
                          ]
                        }}
                        Shape {{
                          appearance DEF MAT_{j_id}_{d}_STRAIGHT PBRAppearance {{
                            baseColor 0.1 1.0 0.3
                            emissiveColor 0.1 1.0 0.3
                            roughness 0.1
                          }}
                          geometry Cylinder {{ height 0.03 radius 0.095 }}
                        }}
                        # Straight Arrow Emblem
                        Transform {{
                          translation 0 0.02 0
                          rotation 1 0 0 -1.5708
                          children [
                            Shape {{
                              appearance PBRAppearance {{ baseColor 0.02 0.02 0.02 roughness 0.9 }}
                              geometry Box {{ size 0.035 0.01 0.11 }}
                            }}
                          ]
                        }}
                      ]
                    }}
                    # 4. GREEN LEFT ARROW (Driver's Left: X=+0.18, Z=-0.42) - 24/7 FREE LEFT
                    Transform {{
                      translation 0.18 0.085 -0.42
                      rotation 1 0 0 1.5708
                      children [
                        Transform {{
                          translation 0 0.09 -0.04
                          rotation 1 0 0 -0.35
                          children [
                            Shape {{
                              appearance PBRAppearance {{ baseColor 0.05 0.05 0.05 roughness 0.5 }}
                              geometry Box {{ size 0.18 0.11 0.02 }}
                            }}
                          ]
                        }}
                        Shape {{
                          appearance DEF MAT_{j_id}_{d}_LEFT PBRAppearance {{
                            baseColor 0.1 1.0 0.35
                            emissiveColor 0.1 1.0 0.35
                            roughness 0.1
                          }}
                          geometry Cylinder {{ height 0.03 radius 0.08 }}
                        }}
                        # Left Arrow Horizontal Stem
                        Transform {{
                          translation 0 0.02 0
                          children [
                            Shape {{
                              appearance PBRAppearance {{ baseColor 0.02 0.02 0.02 roughness 0.9 }}
                              geometry Box {{ size 0.08 0.01 0.03 }}
                            }}
                          ]
                        }}
                      ]
                    }}
                    # 5. GREEN RIGHT ARROW (Driver's Right: X=-0.18, Z=-0.42)
                    Transform {{
                      translation -0.18 0.085 -0.42
                      rotation 1 0 0 1.5708
                      children [
                        Transform {{
                          translation 0 0.09 -0.04
                          rotation 1 0 0 -0.35
                          children [
                            Shape {{
                              appearance PBRAppearance {{ baseColor 0.05 0.05 0.05 roughness 0.5 }}
                              geometry Box {{ size 0.18 0.11 0.02 }}
                            }}
                          ]
                        }}
                        Shape {{
                          appearance DEF MAT_{j_id}_{d}_RIGHT PBRAppearance {{
                            baseColor 0.1 1.0 0.35
                            emissiveColor 0.0 0.05 0.01
                            roughness 0.1
                          }}
                          geometry Cylinder {{ height 0.03 radius 0.08 }}
                        }}
                        # Right Arrow Horizontal Stem
                        Transform {{
                          translation 0 0.02 0
                          children [
                            Shape {{
                              appearance PBRAppearance {{ baseColor 0.02 0.02 0.02 roughness 0.9 }}
                              geometry Box {{ size 0.08 0.01 0.03 }}
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

def generate_clean_4way_vrml(name, j_id, wx, wy):
    faces = [
        generate_unblocked_5aspect_face(j_id, "North", 0.0),
        generate_unblocked_5aspect_face(j_id, "West", 1.570796),
        generate_unblocked_5aspect_face(j_id, "South", 3.1415926),
        generate_unblocked_5aspect_face(j_id, "East", -1.570796),
    ]
    
    return f"""
# ==============================================================================
# UNBLOCKED 5-ASPECT 4-WAY INDIAN TRAFFIC LIGHT TOWER: {name} (Junction {j_id})
# ==============================================================================
DEF {name} Robot {{
  translation {wx:.2f} {wy:.2f} 0.0
  children [
    # 1. Roundabout Island Base
    Solid {{
      name "tl{j_id}_island"
      translation 0 0 0.15
      children [
        Shape {{
          appearance PBRAppearance {{
            baseColor 0.95 0.75 0.05
            roughness 0.6
            metalness 0.1
          }}
          geometry Cylinder {{
            height 0.30
            radius 0.85
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
                radius 0.78
              }}
            }}
          ]
        }}
      ]
    }}
    # 2. Center Steel Mast
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
            radius 0.10
          }}
        }}
        Transform {{
          translation 0 0 2.32
          children [
            Shape {{
              appearance PBRAppearance {{
                baseColor 0.95 0.75 0.05
                roughness 0.2
                metalness 0.5
              }}
              geometry Sphere {{
                radius 0.16
              }}
            }}
          ]
        }}
      ]
    }}
    # 3. Central Mounting Collar
    Solid {{
      name "tl{j_id}_collar"
      translation 0 0 3.9
      children [
        Shape {{
          appearance PBRAppearance {{
            baseColor 0.15 0.16 0.18
            roughness 0.3
            metalness 0.8
          }}
          geometry Cylinder {{
            height 0.35
            radius 0.18
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
    radius 0.85
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
    generate_clean_4way_vrml("TRAFFIC_LIGHT_JUNCTION_25", "25", 45.0, -45.0),
    generate_clean_4way_vrml("TRAFFIC_LIGHT_JUNCTION_26", "26", -45.0, 45.0),
    generate_clean_4way_vrml("TRAFFIC_LIGHT_JUNCTION_27", "27", 105.0, 93.0),
]

new_content = content.rstrip() + "\n\n" + "\n".join(tls_nodes) + "\n"

with open(WBT_PATH, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Corrected Left/Right arrow positions for driver perspective in {WBT_PATH}")
