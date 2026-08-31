def generate_pristine_inetra_billboard(name, tx, ty, rot_z):
    # Perfect billboard architecture:
    # 1. Monopole goes from Z=0 to Z=4.5 (STOPS AT THE BOTTOM OF THE BOARD)
    # 2. Display frame spans from Z=4.5 to Z=11.5 (Center Z=8.0)
    # Result: 100% UNBLOCKED on BOTH sides!
    return f"""
# ==============================================================================
# INETRA PREMIUM MONOPOLE BILLBOARD: {name}
# ==============================================================================
Solid {{
  name "{name}"
  translation {tx:.2f} {ty:.2f} 0.0
  rotation 0 0 1 {rot_z}
  children [
    # 1. Concrete Ground Foundation Pedestal (Z=0 to Z=0.6)
    Transform {{
      translation 0 0 0.3
      children [
        Shape {{
          appearance PBRAppearance {{
            baseColor 0.65 0.65 0.68
            roughness 0.9
            metalness 0.1
          }}
          geometry Cylinder {{
            height 0.6
            radius 1.2
          }}
        }}
      ]
    }}

    # 2. Heavy-Duty Steel Center Column (Z=0.6 to Z=4.5 - STOPS CLEANLY AT BOARD BASE)
    Transform {{
      translation 0 0 2.55
      children [
        Shape {{
          appearance PBRAppearance {{
            baseColor 0.15 0.18 0.22
            roughness 0.3
            metalness 0.8
          }}
          geometry Cylinder {{
            height 3.9
            radius 0.45
          }}
        }}
      ]
    }}

    # 3. Steel Mounting Flange Collar (Z=4.4 to Z=4.6)
    Transform {{
      translation 0 0 4.5
      children [
        Shape {{
          appearance PBRAppearance {{
            baseColor 0.1 0.12 0.16
            roughness 0.2
            metalness 0.9
          }}
          geometry Cylinder {{
            height 0.3
            radius 0.75
          }}
        }}
      ]
    }}

    # 4. Structural Display Housing Box (Z=4.5 to Z=11.5, Center Z=8.0)
    Transform {{
      translation 0 0 8.0
      children [
        Shape {{
          appearance PBRAppearance {{
            baseColor 0.06 0.12 0.22
            roughness 0.3
            metalness 0.7
          }}
          geometry Box {{
            size 7.3 0.35 7.3
          }}
        }}
      ]
    }}

    # 5. Front Crystal-Clear INETRA Display Face (Z=8.0, Y=+0.185) - 100% UNOBSTRUCTED
    Transform {{
      translation 0 0.185 8.0
      children [
        Shape {{
          appearance PBRAppearance {{
            baseColor 1 1 1
            baseColorMap ImageTexture {{
              url [ "textures/custom_signboard_logo.png" ]
            }}
            roughness 0.3
            metalness 0.0
          }}
          geometry Box {{
            size 7.0 0.02 7.0
          }}
        }}
      ]
    }}

    # 6. Rear Crystal-Clear INETRA Display Face (Z=8.0, Y=-0.185) - 100% UNOBSTRUCTED
    Transform {{
      translation 0 -0.185 8.0
      children [
        Shape {{
          appearance PBRAppearance {{
            baseColor 1 1 1
            baseColorMap ImageTexture {{
              url [ "textures/custom_signboard_logo.png" ]
            }}
            roughness 0.3
            metalness 0.0
          }}
          geometry Box {{
            size 7.0 0.02 7.0
          }}
        }}
      ]
    }}

    # 7. Top Solar Panel & Lighting Trim (Z=11.75)
    Transform {{
      translation 0 0 11.75
      children [
        Shape {{
          appearance PBRAppearance {{
            baseColor 0.08 0.12 0.18
            roughness 0.2
            metalness 0.8
          }}
          geometry Box {{
            size 7.4 0.5 0.2
          }}
        }}
      ]
    }}
  ]
  boundingObject Transform {{
    translation 0 0 2.25
    children [
      Cylinder {{
        height 4.5
        radius 0.5
      }}
    ]
  }}
  locked TRUE
}}
"""

WBT_PATH = r"f:\VEHDEMO\simulation\webots\worlds\sih_mvp_traffic.wbt"

with open(WBT_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

import re
# Remove old billboard nodes
content = re.sub(r'# ==============================================================================\n# INETRA PREMIUM MONOPOLE BILLBOARD:[^#]*', '', content)

billboards = [
    # Junction 26 Plaza (-30.0, 60.0), facing South-West towards intersection
    generate_pristine_inetra_billboard("inetra_billboard_j26", -30.0, 60.0, -0.785398),
    # Junction 25 Plaza (30.0, -30.0), facing North-West towards intersection
    generate_pristine_inetra_billboard("inetra_billboard_j25", 30.0, -30.0, 2.35619),
    # Junction 27 Plaza (120.0, 80.0), facing West towards intersection
    generate_pristine_inetra_billboard("inetra_billboard_j27", 120.0, 80.0, 3.14159),
]

idx = content.find("# ==============================================================================\n# SLEEK 4-WAY INDIAN TRAFFIC LIGHT POST")
if idx == -1:
    idx = content.find("# ==============================================================================\n# UNBLOCKED 5-ASPECT")
if idx == -1:
    idx = content.find("# ==============================================================================")

if idx != -1:
    new_wbt = content[:idx] + "\n".join(billboards) + "\n\n" + content[idx:]
else:
    new_wbt = content + "\n\n" + "\n".join(billboards)

with open(WBT_PATH, 'w', encoding='utf-8') as f:
    f.write(new_wbt)

print(f"Engineered unobstructed billboard support architecture in {WBT_PATH}")
