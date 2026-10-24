# MACAI · Healthy Bites — Mobile Açaí Bowl Cart
## 3D Modeling & Architectural/Industrial Design Prompt (CAD · SketchUp · Blender)

> **Source of truth for brand:** *Manual de Uso – Logo MACAI* (15 pp.).
> Hex values below were sampled from the manual's color page; final production must match the **Pantone** references with physical swatches (powder coat, vinyl, acrylic and paint vendors will each need their own color match).
> **Units:** millimetres. **Up axis:** Z. **Tolerance:** ±1 mm in modeling, ±3 mm stated for fabrication unless noted.

---

## 0. Ready-to-paste master prompt (condensed)

Use this block as-is for an AI 3D tool, a render brief or the first message to a 3D modeler. Sections 1–12 are the full specification behind it.

```text
Model a premium mobile açaí bowl cart for the brand "macai – HEALTHY BITES" at real-world scale in millimetres, Z-up.
Overall body 2400 L x 800 D mm, finished worktop at Z=920, customer transaction ledge at Z=1100, removable cantilever
canopy with top at Z=2400. The body is three bolt-together modules along X (customer's left to right):
M1 Blender Station 700 mm | M2 Refrigerated Topping Bar 1000 mm | M3 POS & Handwash 700 mm.
Structure: AISI 304 stainless tube chassis on 4 concealed Ø100 mm locking casters behind a 135 mm recessed black plinth.
Customer front: three separate fascia panels with 6 mm shadow gaps. Center panel is matte deep-purple (Pantone 2627 C,
#371C4B, 10–15 GU) carrying the primary stacked macai logo in coral (Pantone 1635 C, #F4755E) as 25 mm deep halo-lit
letters, 520 mm tall. Side front panels: vertical natural white-oak slats 45x20 mm at 65 mm centres over a purple backer.
End panels: oak slats with a recessed Ø480 mm sage-green (Pantone 7494 C, #96B07C) disc holding the circular badge logo
in cream (Pantone 9060 C, #F5F3D4). Operator side: sage-green matte cabinet doors and drawers, black recessed pulls.
Worktop: 12 mm warm-cream solid surface with 40 mm drop edge and integral coved 100 mm rear upstand.
Ledge: 40 mm solid white oak, matte oil finish, 300 mm deep, 150 mm overhang to the customer.
M2: drop-in refrigerated cold well in brushed #4 AISI 304 stainless, cut-out 900x345 mm, ten GN 1/6 x 100 mm pans
(2 rows x 5) of colorful fruit, granola, coconut, chia, honey; hinged stainless night lid; angled 8 mm tempered glass
sneeze guard with brushed stainless standoffs and an LED-lit top shelf.
M1: two commercial blenders in sound enclosures on the rear worktop, a Ø160 mm integrated pitcher rinser, under-counter
freezer drawer for açaí packs.
M3: swivel tablet POS and card terminal on the ledge facing the customer, thermal receipt printer and cash drawer on the
operator side, Ø300 mm stainless hand-wash basin with knee-operated valve, fresh/grey water tanks below.
Canopy: two 60x60 mm purple powder-coated posts at the rear, 2500x1100 mm canopy, 300 mm fascia in matte purple with the
horizontal macai logo halo-lit in coral; canopy end profiles laser-cut as the three concentric arcs of the macai symbol
in coral. Warm LED lighting everywhere: 3000 K CRI≥95 linear lights under the canopy and the sneeze-guard shelf,
2700 K grazing light under the ledge onto the fascia, 2700 K toe-kick glow making the cart look like it floats.
Style: clean, contemporary, tropical-premium; matte finishes, natural wood warmth, food-grade stainless where food is.
No glossy plastic, no chrome, no distorted or recolored logos.
```

---

## 1. Brand constraints extracted from the manual

### 1.1 Color palette

| Role | Pantone | Sampled HEX | Approx. RGB | Use on the cart |
|---|---|---|---|---|
| Primary 1 — deep açaí purple | **2627 C** | `#371C4B` | 55 · 28 · 75 | Main fascia panels, canopy fascia, posts, ledge brackets |
| Primary 2 — coral | **1635 C** | `#F4755E` | 244 · 117 · 94 | Logo letters on purple, canopy arc profiles, small accents only |
| Primary 3 — sage green | **7494 C** | `#96B07C` | 150 · 176 · 124 | Operator-side cabinetry, end-panel badge discs |
| Secondary — red | 7417 C | `#E83731` | 232 · 55 · 49 | **Not on the structure.** Allowed only in printed menu highlights |
| Secondary — lilac | 2577 C | `#A76ABB` | 167 · 106 · 187 | Menu graphics, cups, napkins (not structural) |
| Secondary — cream | **9060 C** | `#F5F3D4` | 245 · 243 · 212 | Logo on sage, menu board background, worktop color target |
| White 100% | — | `#FFFFFF` | — | Interior of refrigerated equipment only |
| Black 100% | — | `#13100E` | — | Plinth / toe-kick, pulls, cable management |

**Color proportion target (visible exterior, customer side):** purple 55% · natural oak 30% · sage 7% · coral 5% · cream/stainless 3%.

### 1.2 Approved logo / background pairings (only these are allowed on the cart)

| Background | Logo color | Where used |
|---|---|---|
| Purple 2627 C | Coral 1635 C | Center front fascia, canopy fascia |
| Coral 1635 C | Purple 2627 C | Optional: staff aprons, cups (not structure) |
| Sage 7494 C | Cream 9060 C | End-panel badge discs |
| Cream 9060 C | Sage 7494 C | Menu board header |
| White | Purple 2627 C | Stickers on clear containers |
| Black | White | Not used on the cart |

### 1.3 Logo versions and proportions (measure from the vector file before final placement)

| Version | Description | Approx. W:H ratio | Cart location |
|---|---|---|---|
| **Primary (stacked)** | Symbol over script "macai" over "HEALTHY BITES" | **1.41 : 1** | Center front fascia (M2) |
| **Horizontal** | Symbol left, wordmark + tagline right | **4.2 : 1** | Canopy front fascia (and rear fascia) |
| **Circular badge** | "MACAI" arched top, symbol center, "HEALTHY BITES" arched bottom | **1 : 1** | End panels X=0 and X=2400 |
| **Stacked "ma/cai"** | Two-line script with "HEALTHY BITES" on an arc | 1.3 : 1 | Menu board, glass decals (optional) |
| **Symbol only** | Three concentric arcs + drop (roots + M + açaí palm) | — | Canopy end profiles, pill decal "SIN AZÚCARES Añadidos" |

### 1.4 Hard rules (from "Usos incorrectos")

1. **Clear zone (área de reserva):** keep a margin **x** on all four sides, where **x = width of the smallest (innermost) arc of the symbol ≈ 0.17 × lockup height** for the primary logo. No panel joint, slat, screw, vent, hinge, decal or light fixture may enter it.
2. Never stretch, compress or skew the logo; scale proportionally only.
3. Never alter the symbol-to-wordmark ratio or remove elements (e.g., dropping "HEALTHY BITES" from the primary lockup).
4. Never place the logo on non-palette colors or on busy textures. **The logo may NOT sit directly on the wood slats** — it always sits on a solid palette-color plate.
5. Typography: **Demo Brucken** (script) for titles/short words, **lowercase or sentence case only, never all caps**. **Lato** for body copy, prices and all small text.

---

## 2. Coordinate system, units and file setup

```
Origin (0,0,0) = floor level, at the front-left corner of the cart body as seen by the CUSTOMER.
+X  = length, customer's left → right        (body spans X 0 … 2400)
+Y  = depth, customer side → operator side   (body spans Y 0 … 800; ledge overhangs to Y −150)
+Z  = height, floor → up                     (canopy top at Z 2400)
```

| Setting | CAD (AutoCAD / Revit / Rhino) | SketchUp | Blender |
|---|---|---|---|
| Units | mm, 1 drawing unit = 1 mm | Model Info → Units: mm, precision 0 mm, length snapping 1 mm | Scene → Unit System Metric, Unit Scale 0.001, Length mm |
| Up axis | Z | Z (blue) | Z |
| Naming | Layers `MAC-<SYSTEM>-<ELEMENT>` | Tags with same names, every part a **Component** | Collections with same names, object names `MAC_<Module>_<Part>` |
| Export | DWG 2018, STEP AP214 for fabrication, PDF drawings 1:10 / 1:20 | .skp 2021+, export DAE/FBX for render | .blend + FBX/GLB (apply transforms, +Z up, −Y forward) |

**Layer / tag / collection list**

```
MAC-STR-CHASSIS        stainless tube frame, base plate, casters, levelling feet
MAC-STR-CANOPY         posts, spigots, canopy frame
MAC-PNL-FASCIA         customer front panels (3)
MAC-PNL-END            end panels (2) + slats + badge discs
MAC-PNL-OPERATOR       operator-side doors, drawers, plinth
MAC-TOP-WORKTOP        solid surface worktop, upstand, cut-outs
MAC-TOP-LEDGE          oak transaction ledge + brackets
MAC-EQP-REFRIG         cold well, GN pans, night lid, refrigerated base, freezer drawer
MAC-EQP-BLENDER        blenders, enclosures, pitcher rinser
MAC-EQP-POS            tablet POS, card terminal, printer, cash drawer
MAC-EQP-WATER          hand-wash basin, valve, tanks, pump, heater
MAC-GLS-SNEEZEGUARD    tempered glass, standoffs, shelf
MAC-LGT-LED            all LED profiles, drivers (show as emissive in render)
MAC-SGN-BRAND          logos, decals, menu board, QR plaque
MAC-MEP-ELEC           inlet, sub-panel, sockets, cable trays (hidden in render)
MAC-DIM-ANNOT          dimensions, notes (CAD only)
```

---

## 3. Overall envelope

| Item | Value |
|---|---|
| Body length (X) | **2400** |
| Body depth (Y) | **800** (Y 0–800) |
| Depth incl. ledge overhang | **950** (Y −150 to 800) — ledge is bolt-on and removable for transport |
| Finished worktop height (operator) | **Z = 920** |
| Transaction ledge top (customer) | **Z = 1100** |
| Sneeze guard top | **Z = 1450** |
| Canopy top | **Z = 2400**; canopy underside **Z = 2100** |
| Transport height (canopy + posts removed) | **1450** (fits through standard 2100 mm doors and elevators) |
| Transport width | 800 (ledge removed) — passes 900 mm door leaves |
| Floor clearance under plinth | 15 |
| Target empty weight | ≤ 380 kg |

### Module split (along X)

| Module | X range | Width | Function |
|---|---|---|---|
| **M1** | 0 – 700 | 700 | Blender station + açaí freezer |
| **M2** | 700 – 1700 | 1000 | Refrigerated topping bar + bowl assembly + hand-off point |
| **M3** | 1700 – 2400 | 700 | POS / payment + hand-wash station + water system |

Each module is a self-supporting stainless sub-frame joined to its neighbor with **4 × M8 stainless bolts + alignment dowels** through 5 mm flat bar flanges at each shared face. Worktop is **one continuous piece** (seams, if any, at X 700 and X 1700, chemically fused, invisible).

**Service flow (operator):** order & pay at M3 → prepare base at M1 → top at M2 → hand off at the M2 ledge "pick-up" point (marked by an engraved symbol in the oak).

---

## 4. Structure (chassis, plinth, casters)

| Element | Specification | Modeling geometry |
|---|---|---|
| Chassis | AISI 304 square tube **40 × 40 × 2 mm**, TIG-welded, pickled/passivated; perimeter frame at Z 150 and Z 880, verticals at every module corner and at max 600 mm c/c | Model as tube solids, 2 mm wall, mitred corners |
| Base deck | 3 mm AISI 304 sheet, fully welded, with Ø20 drain holes at low points | Plane 2400 × 800, top at Z 150 |
| Casters | 4 × **Ø100 mm** polyurethane, swivel, total-lock brake, 150 kg each; inset 120 mm from ends and 80 mm from front/back | Wheel Ø100 × 32, fork, plate 90 × 90; mounting plate underside at Z 130 |
| Levelling / anti-roll feet | 2 × screw jacks at M1 and M3 centers, foot Ø60, stroke 30 | Cylinder Ø60 × 15 at Z 0–15 |
| Plinth / toe-kick | **Z 15 – 150**, recessed **60 mm** from all four faces, 1.5 mm stainless powder-coated **matte black** | Box ring, outer faces at Y 60 / 740, X 60 / 2340 |
| Push handle | Removable stainless tube Ø32 handle sockets on M3 end, handle at Z 1000 | Hidden in hero render |

---

## 5. Panels and finishes (customer side, ends, operator side)

### 5.1 Customer front (plane Y = 0, Z 150 – 1060)

Three independent panels, one per module, separated by **6 mm black shadow gaps** (vertical reveals at X 700 and X 1700). Panels hang on concealed Z-clips (removable for service).

| Panel | Size (W × H) | Build-up | Finish |
|---|---|---|---|
| **F1** (M1) | 697 × 910 | 4 mm aluminum composite backer in purple + **vertical solid white-oak slats 45 W × 20 D**, **65 mm c/c** (20 mm gaps), slats run full height, 5 mm radius on front edges | Slats: matte hard-wax oil, 10–15 GU, clear; backer: purple 2627 C matte |
| **F2** (M2) | 994 × 910 | 4 mm aluminum composite panel (ACM), PVDF or polyester powder, **purple 2627 C**, gloss **10–15 GU @60°**, anti-graffiti clear coat | Carries the **primary logo** (see §9) |
| **F3** (M3) | 697 × 910 | Same as F1 | Same as F1 |

Bottom edge of all panels at Z 150 (flush with base deck), top edge tucked 20 mm under the oak ledge.

### 5.2 End panels (planes X = 0 and X = 2400, Y 0 – 800, Z 150 – 1060)

- Full-height oak slats as F1/F3, running vertically, 45 × 20 at 65 c/c.
- **Recessed circular plate Ø480**, 3 mm aluminum, **sage 7494 C matte**, set 10 mm proud of the backer and flush with the slat faces; slats are cut around it with a 6 mm reveal.
- Plate center at **Y 400, Z 640**.
- Circular badge logo **Ø400** in **cream 9060 C** (cut vinyl or 2 mm routed acrylic, flush), giving a 40 mm clear zone.

### 5.3 Operator side (plane Y = 800)

- Cabinet doors and drawer fronts: **19 mm moisture-resistant MDF/HPL or 1.2 mm stainless with powder coat**, finish **sage green 7494 C, matte 10 GU**; door gaps 3 mm; recessed black aluminum J-profile pulls (no protruding handles).
- Interior of cabinets: white food-safe HPL or stainless.
- Ventilation louvers for refrigeration: stainless grille 400 × 150 at M1 and M2 plinth level (operator side) and matching 400 × 150 grilles on the front panels hidden *behind the slat gaps* of F1 (no louver visible on F2).
- Rear upstand: integral solid-surface coved upstand **100 mm** high along Y 800.

### 5.4 Material schedule (master)

| Code | Material | Spec | Finish / color | Where |
|---|---|---|---|---|
| **MT-01** | Stainless steel | AISI 304 (18/8), 1.2–1.5 mm sheet, 40×40×2 tube | Brushed **No. 4 / Scotch-Brite**, grain along X | Chassis, food zone, cold well, sneeze guard hardware |
| **MT-02** | Aluminum composite panel | 4 mm, FR core | Powder/PVDF **Pantone 2627 C**, **10–15 GU** | F2, slat backers, canopy fascia |
| **MT-03** | Powder-coated steel | 60×60×3 tube | **Pantone 2627 C**, textured matte | Canopy posts, ledge brackets |
| **MT-04** | Natural wood | FSC solid **white oak** (alt.: teak for outdoor use) | Hard-wax oil, matte, no stain | Slats, transaction ledge |
| **MT-05** | Solid surface | 12 mm acrylic solid surface, 40 mm built-up drop edge, thermoformed coved upstand, non-porous | Warm cream close to **Pantone 9060 C**, matte (sanded to 400 grit) | Worktop, integral sink bowl option |
| **MT-06** | Cabinet panels | 19 mm MR-MDF + HPL, or powder-coated SS | **Pantone 7494 C**, matte | Operator doors, drawers |
| **MT-07** | Tempered glass | 8 mm low-iron, polished edges, 10 mm corner radii | Clear | Sneeze guard + shelf |
| **MT-08** | Cast acrylic | 10 mm face / 3 mm returns | **Pantone 1635 C**, satin | Halo-lit logo letters |
| **MT-09** | Laser-cut aluminum | 4 mm, 5052 | **Pantone 1635 C** powder, matte | Canopy end arcs |
| **MT-10** | Black hardware | Aluminum / SS | Matte black RAL 9005 | Plinth, pulls, shadow gaps |

---

## 6. Worktop and transaction ledge

### 6.1 Worktop (MT-05)

- Top surface **Z 920**, underside **Z 880**, span X −10 to 2410, Y 20 to 800 (10 mm side overhangs; front edge sits 20 mm behind the fascia line, hidden under the raised fascia).
- Front portion Y 20–200 is the **base of the sneeze guard / fascia return**, not working surface.
- Rear coved upstand 100 mm (Z 920–1020) along Y 790–800, coves R 15.

**Cut-outs (plan view, X/Y of cut-out edges):**

| Cut-out | X | Y | Size | Notes |
|---|---|---|---|---|
| Pitcher rinser (M1) | center X 620 | center Y 640 | Ø160 | Stainless rinser, drain to grey tank |
| Topping cold well (M2) | 750 – 1650 | 230 – 575 | **900 × 345** | Fits 2 rows × 5 **GN 1/6** (176 × 162) with adaptor bars |
| Hand-wash basin (M3) | center X 2180 | center Y 600 | Ø300 under-mount bowl | Knee valve below |
| Cable grommets | X 380, X 2050 | Y 760 | Ø60 | Blender + POS power, stainless caps |

### 6.2 Transaction ledge (MT-04)

- Solid white oak, **40 mm thick**, top **Z 1100**, underside Z 1060.
- Plan: X 0 – 2400 (one piece or 3 pieces jointed at X 700/1700 with hidden dowels), Y **−150 to 150** (300 deep).
- Front edge: 3 mm radius top, **15° chamfer underside** (thin, floating look).
- Supported by **3 hidden purple flat-bar brackets** (8 mm steel, MT-03) at X 350, 1200, 2050 bolted to the chassis.
- Engraved **symbol** (Ø60, 1 mm deep) at X 1200, Y 0 = pick-up point.

---

## 7. Equipment by module

> Equipment is modeled as **envelopes** (boxes with key features) unless a manufacturer model is selected. Verify against the final equipment's cut sheet before releasing fabrication drawings.

### 7.1 M1 — Blender station (X 0–700)

| Item | Position | Envelope | Notes |
|---|---|---|---|
| Blender A | on worktop, X 40–270, Y 470–780 | **230 W × 310 D × 470 H** incl. sound enclosure | Commercial 1.5 kW high-performance blender with acoustic cover (e.g., Vitamix *The Quiet One* / Blendtec *Stealth* class) |
| Blender B | X 290–520, Y 470–780 | same | |
| Pitcher rinser | Ø160 at X 620, Y 640 | flush | Push-activated, cold water |
| Prep zone | X 20–700, Y 200–460 | clear | Cutting board 400 × 300 PE, cream |
| Under-counter **freezer drawer** | X 40–660, Y 100–780, Z 160–860 | **620 W × 680 D × 700 H** | −18 °C, R290 self-contained, for açaí pulp packs; rear/side ventilation to louvers |
| Duplex socket strip | rear upstand, X 150 and X 400 | | Each blender on its **own 20 A circuit** |

### 7.2 M2 — Refrigerated topping bar (X 700–1700)

| Item | Specification |
|---|---|
| Cold well | Drop-in **refrigerated cold-wall well**, AISI 304 brushed No. 4, insulated (50 mm PU), cut-out 900 × 345, well depth 165, operating **+1 to +4 °C** (food must hold ≤ 5 °C), NSF/ANSI 7 or equivalent certification, R290 refrigerant |
| Pans | **10 × GN 1/6 × 100 mm** AISI 304 (2 rows × 5), with 2 longitudinal + 8 transverse adaptor bars, 1 mm; optional reconfiguration to 2 × GN 1/3 + 4 × GN 1/6 |
| Lids | Hinged **roll-top or flip stainless night cover** over the full well, closed in "off-hours" renders |
| Topping content (render) | Row 1 (customer side): banana slices, strawberries, blueberries, kiwi, mango. Row 2: granola, coconut flakes, chia, peanut butter, honey (squeeze bottle) |
| Refrigerated base | Below the well, X 720–1680, Y 100–780, Z 160–860: **2 refrigerated drawers**, each holding 2 × GN 1/3 × 150 (backup toppings). Shares condensing unit with the well (≈ ¼ HP), ventilation front via F1 slat gaps / rear grille |
| Bowl assembly zone | Worktop Y 600–790 (operator side of the well) |
| Bowl / cup dispensers | 2 × vertical tube dispensers Ø130 recessed in the operator side face of the refrigerated base's left end (or wall-mounted inside M2 door) |
| Sneeze guard | 8 mm low-iron tempered glass, **front pane** rising from the fascia top line at Y 150 / Z 1100 to Z 1450, **tilted 10° toward the operator**; **top shelf** 8 mm glass, 1000 × 250, at Z 1450 on 4 brushed stainless Ø25 standoffs; 3000 K LED strip under the shelf. Check local rules (NSF/ANSI 2 standard for guards; Colombia: Res. 2674/2013, Res. 604/1993 for street-food carts) |

### 7.3 M3 — POS & hand-wash (X 1700–2400)

| Item | Position | Specification |
|---|---|---|
| Tablet POS | On the ledge, center X 2050, Y 0 | 10–11" tablet in a **360° swivel stand**, matte black, base Ø120; screen faces customer for confirmation/tip, swivels to operator |
| Card terminal (datáfono) | Ledge, X 2250, Y 0 | Cradle 90 × 180, black, on short tether |
| QR payment plaque | Ledge front edge, X 1850 | 100 × 140 cream acrylic, purple Lato text (for local wallet QR payments) |
| Receipt printer | Worktop, X 1760–1900, Y 620–780 | 80 mm thermal printer envelope 145 × 195 × 145 |
| Cash drawer | Under worktop, X 1720–2130, Y 360–780, Z 760–860 | 410 × 420 × 100, keyed, under-counter mount |
| Hand-wash basin | Ø300 under-mount, X 2180 / Y 600 | AISI 304, **knee-operated** valve on operator face, gooseneck spout; soap + paper towel dispensers on the inside of the canopy post above |
| Water system | Below basin, Z 160–720 | **Fresh tank 25 L**, **grey tank 30 L** (grey ≥ 1.2 × fresh), 12 V demand pump, optional 3 L point-of-use heater; tanks on pull-out tray for refill |
| Waste | Pull-out bin 30 L, X 1720–2130, Z 160–700 | Soft-close slide, sage door front |
| Electrical sub-panel | Inside M3 end, X 2350 | See §10 |

---

## 8. Canopy

| Element | Specification |
|---|---|
| Posts | 2 × **60 × 60 × 3 mm** steel tube, purple 2627 C textured matte, at **X 60 and X 2340, Y 730**, from worktop spigot sockets (Z 920) to Z 2100. Sockets are stainless sleeves welded to the chassis; posts lock with one hidden M10 pin each |
| Canopy frame | Aluminum 40 × 40 perimeter + ribs, plan **2500 × 1100** (X −50 to 2450, Y −250 to 850) — cantilevered toward the customer to shade the ledge |
| Fascia | **300 mm** tall band (Z 2100–2400) on front, back and ends, MT-02 purple 2627 C |
| Canopy end profile | Each end fascia (Y–Z plane) is overlaid by **4 mm laser-cut coral aluminum (MT-09)** forming the **three concentric arcs of the macai symbol**, mirrored, arc stroke width = 1/10 of the end fascia height (30 mm); arcs spring from the bottom edge |
| Soffit | 4 mm ACM, **cream 9060 C matte**, with 2 recessed LED profiles (see §11) |
| Top | Sealed 2 mm aluminum, 1° fall to the rear, hidden gutter |
| Transport | Canopy lifts off the posts (4 × M8 knobs), posts pull out of sockets — two people, no tools |

---

## 9. Brand signage placement (exact)

All placements must respect the clear zone **x ≈ 0.17 × logo height** (primary) or the equivalent from the vector file. Every logo is produced from the **original vector master**, never redrawn.

| ID | Logo version | Surface | Center point (X, Y, Z) | Size | Execution | Clear-zone check |
|---|---|---|---|---|---|---|
| **S-01** | **Primary stacked**, coral on purple | Front fascia F2 (plane Y = 0) | **(1200, 0, 610)** | **H 520 × W 733** | 10 mm coral cast acrylic faces + 3 mm returns = **25 mm deep**, mounted 25 mm off the panel on hidden studs, **halo-lit** with 3000 K LED modules behind | x = 88 → required area 909 × 696; F2 is 994 × 910 ✔ |
| **S-02** | **Horizontal**, coral on purple | Canopy front fascia (plane Y = −250) | **(1200, −250, 2250)** | **H 180 × W 756** | Same halo-lit construction, 20 mm deep | x ≈ 36 → 828 × 252 inside a 2500 × 300 band ✔ |
| **S-03** | Horizontal, coral on purple | Canopy rear fascia (plane Y = 850) | (1200, 850, 2250) | H 150 × W 630 | Non-illuminated cut vinyl or routed flat acrylic | ✔ |
| **S-04 / S-05** | **Circular badge**, cream on sage | End panels X = 0 and X = 2400 | **(0 / 2400, 400, 640)** | **Ø400** on Ø480 sage disc | 2 mm flush-routed cream acrylic or cast vinyl | 40 mm ring ✔ |
| **S-06** | Pill decal **"SIN AZÚCARES Añadidos"** (symbol + Lato bold), as on manual p. 15 | Inside face of sneeze-guard front glass, readable from customer side | (900, 150, 1380) | 260 × 70 | Cream/purple printed vinyl, reverse-applied | Clear of food view line |
| **S-07** | **Menu board** | Hung from the canopy soffit on 2 stainless rods in front of the left post, facing customer | (300, −50, 1850) | **600 W × 400 H** | 6 mm cream 9060 C composite panel; header "nuestros bowls" in **Demo Brucken lowercase**, sage or purple; items/prices in **Lato**; small stacked "ma/cai" logo top-right | Logo with its own clear zone |
| **S-08** | QR plaque | Ledge, M3 | (1850, −60, 1100) | 100 × 140 | Cream acrylic, Lato | — |
| **S-09** | Engraved symbol "pick-up" | Ledge top, M2 | (1200, 0, 1100) | Ø60 | Laser-engraved 1 mm | — |

**Do not place** any logo on: the oak slats, the stainless equipment, the glass shelf, the plinth, or across any panel joint.

---

## 10. MEP (for modeling envelopes and routing; detail by licensed installer)

| System | Specification |
|---|---|
| Power inlet | 1 × IP67 twist-lock inlet on M3 end, lower corner (X 2400, Y 700, Z 300) |
| Supply | Designed for **120 V / 60 Hz** (Colombian standard) with a **240 V split-phase or 220 V option**; installer to confirm the venue's supply |
| Sub-panel | In M3, with RCD/GFCI protection; circuits: **C1** blender A 20 A · **C2** blender B 20 A · **C3** refrigeration (well + base + freezer) 20 A · **C4** lighting + signage + POS 15 A · **C5** water pump/heater 15 A |
| Estimated load | Blenders 2 × 1.5 kW · refrigeration ≈ 0.9 kW · heater 1.5 kW (optional) · LED ≈ 0.15 kW · POS 0.05 kW → peak ≈ 5.6 kW; diversity-managed ≈ 4 kW |
| Battery option | 24 V LiFePO4 1 kWh for lighting, signage and POS only (keeps the cart lit during set-up/transport) |
| Cable routing | Stainless cable tray along the chassis at Z 860, operator side; canopy feed through one post (internal conduit) with a quick connector at the spigot |
| Plumbing | Food-grade PE hose, quick-disconnect couplings on tanks; grey tank with level indicator and ¾" drain valve |
| Ventilation | Refrigeration intake/exhaust ≥ 150 cm² free area each per condensing unit, separated to avoid short-circuiting hot air |

---

## 11. Integrated warm LED lighting

All LEDs: **24 V DC**, **CRI ≥ 95, R9 ≥ 50** (food reds and açaí purples render correctly), MacAdam ≤ 3-step, **dimmable (0-10 V or PWM)**, IP65 where exposed to splash; aluminum channel profiles with opal diffusers (no visible dots).

| ID | Location | CCT | Output | Geometry for modeling | Target |
|---|---|---|---|---|---|
| **L-01** | Canopy soffit, 2 recessed linear profiles | **3000 K** | 14 W/m | 2 × 2300 long, 20 × 10 channel, at Y 150 and Y 550, Z 2100 | **500–700 lux** on worktop & ledge |
| **L-02** | Under sneeze-guard shelf, front edge | **3000 K** | 10 W/m | 950 × 10 × 8, Z 1442 | 800 lux on toppings (merchandising) |
| **L-03** | Halo lighting behind S-01 and S-02 | **3000 K** | LED modules 0.5 W @ 50 mm grid | Planes 20 mm behind letters | Soft glow ring ~40 mm around letters on purple |
| **L-04** | Grazing light under the oak ledge onto F1–F3 | **2700 K** | 9.6 W/m | 2380 × 12 × 8, Z 1055, Y 10, aimed down | Grazes slats, creates rhythm of shadows |
| **L-05** | Toe-kick (all 4 sides) | **2700 K** | 4.8 W/m, 30% dim | Ring at Z 30 behind plinth face | "Floating" effect, no visible source |
| **L-06** | Menu board top edge | 3000 K | 4.8 W/m | 600 long, hidden lip | Even wash ≥ 300 lux |
| **L-07** | Operator task light inside canopy rear | 3000 K | 10 W/m | 2300, Y 800 | Cash/POS area 500 lux |

**Render-light settings (Blender Cycles / V-Ray / Enscape):** use Kelvin/blackbody values above; L-01 at ~1800 lm per profile; L-02 ~500 lm; L-04 ~900 lm; L-05 ~150 lm; halo 6–10 W emission per logo. Exposure set so the purple fascia reads as `#371C4B` under L-04 — not blown out.

---

## 12. PBR material values (for Blender Principled BSDF / SketchUp + render engine)

| Material | Base color (sRGB) | Metallic | Roughness | Other |
|---|---|---|---|---|
| Purple powder coat (MT-02/03) | `#371C4B` | 0.0 | 0.60 | Fine noise bump 0.02 (orange-peel), Sheen 0 |
| Coral acrylic (MT-08) | `#F4755E` | 0.0 | 0.25 | Subsurface 0.05 for halo glow edge, Coat 0.2 |
| Coral aluminum (MT-09) | `#F4755E` | 0.0 | 0.55 | — |
| Sage panels (MT-06) | `#96B07C` | 0.0 | 0.65 | — |
| Cream solid surface (MT-05) | `#F2EEDA` | 0.0 | 0.35 | Very subtle speckle texture, Coat 0.1 |
| Cream soffit / menu | `#F5F3D4` | 0.0 | 0.70 | — |
| White oak, oiled (MT-04) | oak diffuse map (light, straight grain, quarter-sawn) | 0.0 | 0.50 | Grain **vertical** on slats, **along X** on ledge; normal map strength 0.3 |
| Brushed stainless (MT-01) | `#C8CACC` | 1.0 | 0.30 | Anisotropic 0.7, rotation aligned to X |
| Matte black (MT-10) | `#13100E` | 0.0 | 0.70 | — |
| Glass (MT-07) | `#FFFFFF` | 0.0 | 0.02 | Transmission 1.0, IOR 1.52, thin-wall off; edge tint `#E6F2EE` |
| LED diffuser | `#FFFFFF` | 0.0 | 0.40 | Emission blackbody 2700/3000 K |

**Bevels:** every exterior edge gets a real bevel or a Bevel modifier — panels 1 mm, oak 3–5 mm, solid surface 3 mm, stainless 0.5 mm. No knife-sharp CG edges.

---

## 13. Required deliverables / views

1. **Plan (top) 1:20** — worktop layout with all cut-outs and equipment envelopes dimensioned to the origin.
2. **Front elevation (customer) 1:20** — panels, slats, logo S-01 with clear-zone box, ledge, sneeze guard, canopy fascia with S-02.
3. **Rear elevation (operator) 1:20** — doors, drawers, louvers, equipment heights.
4. **Side elevations (both ends) 1:20** — badge disc, canopy arc profiles, transport-height line at Z 1450.
5. **Section A-A through M2** (Y–Z plane at X 1200) — cold well, refrigerated base, sneeze guard, ledge bracket, lighting positions.
6. **Section B-B through M1** — blender, rinser, freezer drawer, ventilation path.
7. **Exploded axonometric** — modules M1/M2/M3 separated by 300 mm along X, canopy lifted 400 mm, ledge lifted 150 mm.
8. **Renders:** hero 3/4 customer view at eye level (camera Z 1600, 35 mm lens, 3.5 m away, 30° from the front axis); operator view; night view with only L-01…L-06 on; close-up of the topping bar.
9. **Transport configuration** model state (canopy, posts, ledge, menu removed).

---

## 14. Parametric data block (copy into a script, Grasshopper, Dynamo or SketchUp/Blender add-on)

```yaml
units: mm
up_axis: Z
origin: front_left_floor_customer_view
body:        {length: 2400, depth: 800, plinth_top: 150, plinth_recess: 60, floor_clearance: 15}
modules:     [{id: M1, x0: 0, x1: 700}, {id: M2, x0: 700, x1: 1700}, {id: M3, x0: 1700, x1: 2400}]
worktop:     {top_z: 920, thickness: 40, solid_surface: 12, upstand: 100, color: "#F2EEDA"}
ledge:       {top_z: 1100, thickness: 40, y0: -150, y1: 150, material: white_oak}
fascia:      {z0: 150, z1: 1060, gap: 6, F2_color: "#371C4B", slats: {w: 45, d: 20, pitch: 65}}
sneeze_guard:{glass: 8, z_top: 1450, tilt_deg: 10, shelf: {w: 1000, d: 250}}
cold_well:   {x0: 750, x1: 1650, y0: 230, y1: 575, depth: 165, pans: {gn: "1/6", depth: 100, rows: 2, cols: 5}, temp_c: [1, 4]}
blenders:    [{x0: 40, x1: 270, y0: 470, y1: 780, h: 470}, {x0: 290, x1: 520, y0: 470, y1: 780, h: 470}]
rinser:      {cx: 620, cy: 640, d: 160}
handwash:    {cx: 2180, cy: 600, d: 300}
pos:         {tablet: {cx: 2050, cy: 0, z: 1100}, terminal: {cx: 2250, cy: 0, z: 1100}}
canopy:      {posts: [{x: 60, y: 730}, {x: 2340, y: 730}], post_section: 60, x0: -50, x1: 2450, y0: -250, y1: 850, z0: 2100, z1: 2400}
casters:     {d: 100, inset_x: 120, inset_y: 80}
colors:      {purple: "#371C4B", coral: "#F4755E", sage: "#96B07C", cream: "#F5F3D4", black: "#13100E"}
signage:
  S01: {version: primary, center: [1200, 0, 610], h: 520, w: 733, clear: 88, color: coral, lit: halo_3000K}
  S02: {version: horizontal, center: [1200, -250, 2250], h: 180, w: 756, color: coral, lit: halo_3000K}
  S04: {version: badge, center: [0, 400, 640], d: 400, plate_d: 480, color: cream, plate: sage}
  S05: {version: badge, center: [2400, 400, 640], d: 400, plate_d: 480, color: cream, plate: sage}
lighting:
  L01: {cct: 3000, w_per_m: 14, z: 2100, y: [150, 550], length: 2300}
  L02: {cct: 3000, w_per_m: 10, z: 1442}
  L04: {cct: 2700, w_per_m: 9.6, z: 1055}
  L05: {cct: 2700, w_per_m: 4.8, z: 30, dim: 0.3}
```

---

## 15. QA checklist before release

- [ ] All logos imported from vector master; aspect ratio locked; clear-zone boxes drawn on layer `MAC-DIM-ANNOT` and not intersected.
- [ ] Only approved logo/background pairings used (§1.2); no logo on wood or stainless.
- [ ] Demo Brucken used only in lowercase/sentence case; all small text in Lato.
- [ ] Worktop at 920, ledge at 1100, transport height ≤ 1450, transport width ≤ 800.
- [ ] Every food-contact surface is AISI 304 or certified food-grade solid surface; no exposed wood in the food zone.
- [ ] Cold well holds ≤ 5 °C; freezer −18 °C; hand-wash basin with hot/cold or tempered water and knee valve; grey tank > fresh tank.
- [ ] Each blender on a dedicated circuit; refrigeration ventilation paths unobstructed.
- [ ] All LEDs 2700–3000 K, CRI ≥ 95; no visible LED dots; no cool-white sources anywhere.
- [ ] Equipment envelopes replaced or verified against the selected manufacturers' cut sheets.
- [ ] Local health and fire approvals checked (Colombia: INVIMA / Secretaría de Salud — Res. 2674 de 2013, Res. 604 de 1993; mall operator's tenant design criteria if placed in a shopping center).
