import os

def create_arrow_mesh(direction="left"):
    # Returns Shape for arrow or lens
    pass

def generate_signal_face_vrml(direction_name, rotation_angle):
    # rotation_angle in radians around Z axis:
    # 0 = North (+Y), 1.5708 = West (-X), 3.14159 = South (-Y), -1.5708 = East (+X)
    
    # Each face is offset from center mast by 1.2m outwards and at height Z = 4.8m
    # 5 aspects:
    # 1. Red (Z = +0.6)
    # 2. Amber (Z = +0.3)
    # 3. Straight Green Arrow (Z = 0.0)
    # 4. Left Green Arrow (Z = -0.3, X = -0.2)
    # 5. Right Green Arrow (Z = -0.3, X = +0.2)
    
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
                    Transform {{
                      translation 0 0.15 0.48
                      rotation 1 0 0 1.5708
                      children [
                        # Visor Hood
                        Transform {{
                          translation 0 0.1 0.05
                          children [
                            Shape {{
                              appearance PBRAppearance {{ baseColor 0.05 0.05 0.05 roughness 0.2 }}
                              geometry Cylinder {{ height 0.15 radius 0.13 }}
                            }}
                          ]
                        }}
                        # Red Lens
                        Shape {{
                          appearance PBRAppearance {{
                            baseColor 0.9 0.1 0.1
                            emissiveColor 1.0 0.15 0.15
                            roughness 0.1
                          }}
                          geometry Cylinder {{ height 0.04 radius 0.11 }}
                        }}
                      ]
                    }}
                    # 2. AMBER / ORANGE LIGHT (Upper Middle)
                    Transform {{
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
                          appearance PBRAppearance {{
                            baseColor 0.95 0.6 0.05
                            emissiveColor 1.0 0.65 0.1
                            roughness 0.1
                          }}
                          geometry Cylinder {{ height 0.04 radius 0.11 }}
                        }}
                      ]
                    }}
                    # 3. GREEN STRAIGHT ARROW (Center Lower)
                    Transform {{
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
                        # Green Base Lens
                        Shape {{
                          appearance PBRAppearance {{
                            baseColor 0.05 0.85 0.2
                            emissiveColor 0.1 1.0 0.3
                            roughness 0.1
                          }}
                          geometry Cylinder {{ height 0.04 radius 0.11 }}
                        }}
                        # Black Arrow Mask (Straight Arrow)
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
                    }}
                    # 4. GREEN LEFT ARROW (Bottom Left - 24/7 Free Left)
                    Transform {{
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
                        # Glowing Green Lens
                        Shape {{
                          appearance PBRAppearance {{
                            baseColor 0.05 0.95 0.25
                            emissiveColor 0.1 1.0 0.35
                            roughness 0.1
                          }}
                          geometry Cylinder {{ height 0.04 radius 0.085 }}
                        }}
                        # Left Arrow Horizontal Stem
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
                    }}
                    # 5. GREEN RIGHT ARROW (Bottom Right)
                    Transform {{
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
                        # Glowing Green Lens
                        Shape {{
                          appearance PBRAppearance {{
                            baseColor 0.05 0.95 0.25
                            emissiveColor 0.1 1.0 0.35
                            roughness 0.1
                          }}
                          geometry Cylinder {{ height 0.04 radius 0.085 }}
                        }}
                        # Right Arrow Horizontal Stem
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
                    }}
                  ]
                }}
              ]
            }}
          ]
        }}
    """

def generate_4way_traffic_light_vrml(name, wx, wy):
    faces = [
        generate_signal_face_vrml("North", 0.0),
        generate_signal_face_vrml("West", 1.570796),
        generate_signal_face_vrml("South", 3.1415926),
        generate_signal_face_vrml("East", -1.570796),
    ]
    
    return f"""
# ==============================================================================
# 4-WAY INDIAN TRAFFIC LIGHT TOWER: {name} (Center of Intersection)
# Red, Amber, Green Straight Arrow, Green Left Arrow (Free Left), Green Right Arrow
# ==============================================================================
DEF {name} Solid {{
  translation {wx:.2f} {wy:.2f} 0.0
  children [
    # 1. Heavy Central Roundabout Island / Base
    Solid {{
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
        # Inner Concrete Cap
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
    # 2. Main Center Steel Mast / Pole
    Solid {{
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
        # Top Mast Finial Cap
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
    # 3. 4-Arm Cantilever Support Gantry Structure
    Solid {{
      translation 0 0 4.8
      children [
        # North-South Horizontal Steel Truss
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
        # East-West Horizontal Steel Truss
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

# Remove old empty traffic light comments at the bottom
idx = content.find("# Junction 25 (4-way)")
if idx != -1:
    content = content[:idx]

tls_nodes = [
    generate_4way_traffic_light_vrml("TRAFFIC_LIGHT_JUNCTION_25", 45.0, -45.0),
    generate_4way_traffic_light_vrml("TRAFFIC_LIGHT_JUNCTION_26", -45.0, 45.0),
    generate_4way_traffic_light_vrml("TRAFFIC_LIGHT_JUNCTION_27", 105.0, 93.0),
]

new_content = content.rstrip() + "\n\n" + "\n".join(tls_nodes) + "\n"

with open(WBT_PATH, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Successfully placed 4-way Indian Traffic Light Towers at Junctions 25, 26, 27 in {WBT_PATH}")
