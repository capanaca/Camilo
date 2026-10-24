# MACAI mobile açaí cart

| File | What it is |
|---|---|
| `MACAI_Acai_Cart_3D_Prompt.md` | Design brief: dimensions, materials, equipment, lighting, signage |
| `macai_cart.html` | Interactive 3D model built from the brief (Three.js, opens in any browser) |
| `model/macai_cart.glb` | Same model as glTF binary: meters, Y-up; Blender imports it natively (converts to Z-up) |
| `renders/` | Day, night, front, operator, end, plan, toppings, exploded, transport and dimension views |
| `src/` | Viewer template, logo extraction from the brand manual, build and render/export scripts |

Rebuild: `python3 src/extract_logos.py <pdf-pages-dir>` → `python3 src/build.py <logos.json>` → `node src/render_and_export.js <node_modules> macai_cart.html <out> all`.
