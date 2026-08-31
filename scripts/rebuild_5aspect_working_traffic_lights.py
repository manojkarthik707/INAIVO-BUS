import os

def generate_5aspect_face_vrml(j_id, direction_name, rotation_angle):
    d = direction_name.upper()
    
    # 5 aspects:
    # 1. Red (Top, Z=+0.46)
    # 2. Amber (Upper-mid, Z=+0.16)
    # 3. Straight Green Arrow (Center-mid, Z=-0.14)
    # 4. Left Green Arrow (Bottom-left, X=-0.18, Z=-0.44)
    # 5. Right Green Arrow (Bottom-right, X=+0.18, Z=-0.44)
    
    return f"""
        # --- FACE {direction_name.upper()} ---
        Transform {{
          translation 0 0 0
          rotation 0 0 1 {rotation_angle}
          children [
            Transform {{
              translation 0 0.35 3.9
              children [
                # Signal Housing
                Solid {{
                  name "tl{j_id}_{direction_name.lower()}_housing"
                  children [
                    # Main Black Polycarbonate Body
                    Shape {{
                      appearance PBRAppearance {{
                        baseColor 0.08 0.08 0.10
                        roughness 0.4
                        metalness 0.2
                      }}
                      geometry Box {{
                        size 0.62 0.16 1.25
                      }}
                    }}
                    # Yellow Border Trim
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
                            size 0.68 0.02 1.32
                          }}
                        }}
                      ]
                    }}
                    # 1. RED LENS (Top, Z=+0.44)
                    Transform {{
                      translation 0 0.08 0.44
                      rotation 1 0 0 1.5708
                      children [
                        Transform {{
                          translation 0 0.03 -0.03
                          rotation 1 0 0 0.2
                          children [
                            Shape {{
                              appearance PBRAppearance {{ baseColor 0.05 0.05 0.05 roughness 0.5 }}
                              geometry Cylinder {{ height 0.08 radius 0.11 }}
                            }}
                          ]
                        }}
                        Shape {{
                          appearance DEF MAT_{j_id}_{d}_RED PBRAppearance {{
                            baseColor 0.9 0.1 0.1
                            emissiveColor 1.0 0.1 0.1
                            roughness 0.1
                          }}
                          geometry Cylinder {{ height 0.02 radius 0.095 }}
                        }}
                      ]
                    }}
                    # 2. AMBER LENS (Upper Mid, Z=+0.16)
                    Transform {{
                      translation 0 0.08 0.16
                      rotation 1 0 0 1.5708
                      children [
                        Transform {{
                          translation 0 0.03 -0.03
                          rotation 1 0 0 0.2
                          children [
                            Shape {{
                              appearance PBRAppearance {{ baseColor 0.05 0.05 0.05 roughness 0.5 }}
                              geometry Cylinder {{ height 0.08 radius 0.11 }}
                            }}
                          ]
                        }}
                        Shape {{
                          appearance DEF MAT_{j_id}_{d}_AMBER PBRAppearance {{
                            baseColor 0.9 0.55 0.05
                            emissiveColor 0.1 0.05 0.0
                            roughness 0.1
                          }}
                          geometry Cylinder {{ height 0.02 radius 0.095 }}
                        }}
                      ]
                    }}
                    # 3. GREEN STRAIGHT ARROW (Center, Z=-0.14)
                    Transform {{
                      translation 0 0.08 -0.14
                      rotation 1 0 0 1.5708
                      children [
                        Transform {{
                          translation 0 0.03 -0.03
                          rotation 1 0 0 0.2
                          children [
                            Shape {{
                              appearance PBRAppearance {{ baseColor 0.05 0.05 0.05 roughness 0.5 }}
                              geometry Cylinder {{ height 0.08 radius 0.11 }}
                            }}
                          ]
                        }}
                        Shape {{
                          appearance DEF MAT_{j_id}_{d}_STRAIGHT PBRAppearance {{
                            baseColor 0.05 0.9 0.25
                            emissiveColor 0.1 1.0 0.3
                            roughness 0.1
                          }}
                          geometry Cylinder {{ height 0.02 radius 0.095 }}
                        }}
                        # Straight Arrow Symbol
                        Transform {{
                          translation 0 0.02 0
                          rotation 1 0 0 -1.5708
                          children [
                            Shape {{
                              appearance PBRAppearance {{ baseColor 0.02 0.02 0.02 roughness 0.9 }}
                              geometry Box {{ size 0.03 0.01 0.11 }}
                            }}
                          ]
                        }}
                      ]
                    }}
                    # 4. GREEN LEFT ARROW (Bottom Left, Z=-0.44) - 24/7 FREE LEFT
                    Transform {{
                      translation -0.18 0.08 -0.44
                      rotation 1 0 0 1.5708
                      children [
                        Transform {{
                          translation 0 0.03 -0.03
                          rotation 1 0 0 0.2
                          children [
                            Shape {{
                              appearance PBRAppearance {{ baseColor 0.05 0.05 0.05 roughness 0.5 }}
                              geometry Cylinder {{ height 0.08 radius 0.095 }}
                            }}
                          ]
                        }}
                        Shape {{
                          appearance DEF MAT_{j_id}_{d}_LEFT PBRAppearance {{
                            baseColor 0.05 0.95 0.25
                            emissiveColor 0.1 1.0 0.35
                            roughness 0.1
                          }}
                          geometry Cylinder {{ height 0.02 radius 0.08 }}
                        }}
                        # Left Arrow Symbol
                        Transform {{
                          translation 0 0.02 0
                          children [
                            Shape {{
                              appearance PBRAppearance {{ baseColor 0.02 0.02 0.02 roughness 0.9 }}
                              geometry Box {{ size 0.08 0.01 0.025 }}
                            }}
                          ]
                        }}
                      ]
                    }}
                    # 5. GREEN RIGHT ARROW (Bottom Right, Z=-0.44)
                    Transform {{
                      translation 0.18 0.08 -0.44
                      rotation 1 0 0 1.5708
                      children [
                        Transform {{
                          translation 0 0.03 -0.03
                          rotation 1 0 0 0.2
                          children [
                            Shape {{
                              appearance PBRAppearance {{ baseColor 0.05 0.05 0.05 roughness 0.5 }}
                              geometry Cylinder {{ height 0.08 radius 0.095 }}
                            }}
                          ]
                        }}
                        Shape {{
                          appearance DEF MAT_{j_id}_{d}_RIGHT PBRAppearance {{
                            baseColor 0.05 0.95 0.25
                            emissiveColor 0.0 0.1 0.02
                            roughness 0.1
                          }}
                          geometry Cylinder {{ height 0.02 radius 0.08 }}
                        }}
                        # Right Arrow Symbol
                        Transform {{
                          translation 0 0.02 0
                          children [
                            Shape {{
                              appearance PBRAppearance {{ baseColor 0.02 0.02 0.02 roughness 0.9 }}
                              geometry Box {{ size 0.08 0.01 0.025 }}
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

def generate_5aspect_4way_traffic_light_vrml(name, j_id, wx, wy):
    faces = [
        generate_5aspect_face_vrml(j_id, "North", 0.0),
        generate_5aspect_face_vrml(j_id, "West", 1.570796),
        generate_5aspect_face_vrml(j_id, "South", 3.1415926),
        generate_5aspect_face_vrml(j_id, "East", -1.570796),
    ]
    
    return f"""
# ==============================================================================
# 5-ASPECT 4-WAY INDIAN TRAFFIC LIGHT TOWER: {name} (Junction {j_id})
# Red, Amber, Straight Green Arrow, Free Left Green Arrow, Right Green Arrow
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
    # 2. Main Center Steel Mast
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
        # Top Mast Finial Cap
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
    # 3. 4-Way Central Mounting Collar
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
    generate_5aspect_4way_traffic_light_vrml("TRAFFIC_LIGHT_JUNCTION_25", "25", 45.0, -45.0),
    generate_5aspect_4way_traffic_light_vrml("TRAFFIC_LIGHT_JUNCTION_26", "26", -45.0, 45.0),
    generate_5aspect_4way_traffic_light_vrml("TRAFFIC_LIGHT_JUNCTION_27", "27", 105.0, 93.0),
]

new_content = content.rstrip() + "\n\n" + "\n".join(tls_nodes) + "\n"

with open(WBT_PATH, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Generated 5-aspect Indian Traffic Light Towers with live PBR DEF materials in {WBT_PATH}")
