def generate_flawless_double_sided_billboard(name, tx, ty, rot_z):
    # Flawless double-sided billboard:
    # - Center pole goes strictly from Z=0 to Z=4.5m (height 4.5m, center Z=2.25m).
    # - Display housing sits on top from Z=4.5m to Z=11.5m (center Z=8.0m, height 7.0m).
    # - FRONT face (+Y) and REAR face (-Y) are 100% unobstructed with zero pole crossing!
    return f"""
# ==============================================================================
# INETRA FLAWLESS DOUBLE-SIDED BILLBOARD: {name}
# ==============================================================================
Solid {{
  name "{name}"
  translation {tx:.2f} {ty:.2f} 0.0
  rotation 0 0 1 {rot_z}
  children [
    # 1. Concrete Ground Foundation Pedestal (Z=0 to Z=0.5)
    Transform {{
      translation 0 0 0.25
      children [
        Shape {{
          appearance PBRAppearance {{
            baseColor 0.65 0.65 0.68
            roughness 0.9
            metalness 0.1
          }}
          geometry Cylinder {{
            height 0.5
            radius 1.1
          }}
        }}
      ]
    }}

    # 2. Steel Monopole Support Column (Z=0 to Z=4.5 - STOPS CLEANLY AT BOARD BASE)
    Transform {{
      translation 0 0 2.25
      children [
        Shape {{
          appearance PBRAppearance {{
            baseColor 0.15 0.18 0.22
            roughness 0.3
            metalness 0.8
          }}
          geometry Cylinder {{
            height 4.5
            radius 0.38
          }}
        }}
      ]
    }}

    # 3. Steel Mounting Flange Collar (Z=4.4 to Z=4.5)
    Transform {{
      translation 0 0 4.45
      children [
        Shape {{
          appearance PBRAppearance {{
            baseColor 0.1 0.12 0.16
            roughness 0.2
            metalness 0.9
          }}
          geometry Cylinder {{
            height 0.1
            radius 0.65
          }}
        }}
      ]
    }}

    # 4. Structural Housing Frame (Z=4.5 to Z=11.5, Center Z=8.0)
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
            size 7.3 0.30 7.3
          }}
        }}
      ]
    }}

    # 5. FRONT INETRA Display Face (Z=8.0, Y=+0.16) - 100% UNOBSTRUCTED
    Transform {{
      translation 0 0.16 8.0
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

    # 6. REAR INETRA Display Face (Z=8.0, Y=-0.16) - 100% UNOBSTRUCTED
    Transform {{
      translation 0 -0.16 8.0
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

    # 7. Top Solar & Lighting Trim (Z=11.7)
    Transform {{
      translation 0 0 11.7
      children [
        Shape {{
          appearance PBRAppearance {{
            baseColor 0.08 0.12 0.18
            roughness 0.2
            metalness 0.8
          }}
          geometry Box {{
            size 7.4 0.45 0.15
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
        radius 0.45
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
# Find start of billboard section
idx_start = content.find("Solid {\n  name \"inetra_billboard_j26\"")
if idx_start == -1:
    idx_start = content.find("# ==============================================================================\n# INETRA")

idx_tls = content.find("# ==============================================================================\n# SLEEK 4-WAY INDIAN TRAFFIC LIGHT POST")
if idx_tls == -1:
    idx_tls = content.find("# ==============================================================================\n# UNBLOCKED 5-ASPECT")

base_world = content[:idx_start].rstrip()
tls_section = content[idx_tls:]

billboards = [
    # Junction 26 Plaza (-30.0, 60.0), facing South-West towards intersection
    generate_flawless_double_sided_billboard("inetra_billboard_j26", -30.0, 60.0, -0.785398),
    # Junction 25 Plaza (30.0, -30.0), facing North-West towards intersection
    generate_flawless_double_sided_billboard("inetra_billboard_j25", 30.0, -30.0, 2.35619),
    # Junction 27 Plaza (120.0, 80.0), facing West towards intersection
    generate_flawless_double_sided_billboard("inetra_billboard_j27", 120.0, 80.0, 3.14159),
]

new_wbt = base_world + "\n\n" + "\n".join(billboards) + "\n\n" + tls_section

with open(WBT_PATH, 'w', encoding='utf-8') as f:
    f.write(new_wbt)

print(f"Successfully installed flawless double-sided billboards (both sides 100% visible) in {WBT_PATH}")
