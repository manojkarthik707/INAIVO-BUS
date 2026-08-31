def generate_pristine_inetra_billboard(name, tx, ty, rot_z):
    return f"""
# ==============================================================================
# INETRA PREMIUM MONOPOLE BILLBOARD: {name}
# ==============================================================================
Solid {{
  name "{name}"
  translation {tx:.2f} {ty:.2f} 0.0
  rotation 0 0 1 {rot_z}
  children [
    # 1. Concrete Ground Foundation Pedestal
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

    # 2. Heavy-Duty Steel Center Column (Placed behind display)
    Transform {{
      translation 0 -0.25 4.5
      children [
        Shape {{
          appearance PBRAppearance {{
            baseColor 0.2 0.22 0.25
            roughness 0.4
            metalness 0.8
          }}
          geometry Cylinder {{
            height 9.0
            radius 0.42
          }}
        }}
      ]
    }}

    # 3. Structural Display Outer Frame Housing (Z=8.0m)
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
            size 7.4 0.40 7.4
          }}
        }}
      ]
    }}

    # 4. Front Crystal-Clear INETRA Display Face (Z=8.0m, Y=+0.21m) - Robust 3D Box Geometry
    Transform {{
      translation 0 0.21 8.0
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

    # 5. Rear INETRA Display Face (Z=8.0m, Y=-0.21m)
    Transform {{
      translation 0 -0.21 8.0
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

    # 6. Overhead LED Floodlight Gantry Bar
    Transform {{
      translation 0 0.8 11.8
      children [
        Shape {{
          appearance PBRAppearance {{
            baseColor 0.15 0.18 0.22
            roughness 0.3
            metalness 0.8
          }}
          geometry Box {{
            size 6.5 0.15 0.15
          }}
        }}
      ]
    }}
  ]
  boundingObject Transform {{
    translation 0 0 4.5
    children [
      Cylinder {{
        height 9.0
        radius 0.6
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

print(f"Upgraded billboards with robust 3D Box display geometries and baseColor 1 1 1 in {WBT_PATH}")
