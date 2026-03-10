# GRAPHICS_PROMPT.md

Guidance for art agents generating sprites and UI assets for **Trailer Park Empire**.

---

## Art Style

**Isometric cartoon (FarmVille style) — smooth gradients, bold outlines, implied 3D depth.**

References: FarmVille 2, Hay Day, Township.

- True isometric projection: 2:1 width-to-height diamond tiles
- Smooth shading with gradient fills (no hard pixel-art steps)
- 1–2 px dark outline on all opaque shapes (`#1E140A`)
- Lighting: top-left light source; lighter top/right face, darker left/front face
- Colors: saturated, warm, cartoon-friendly — not neon, not desaturated
- Mood: cheerful Southern US trailer park — charming and a little run-down

---

## Isometric Grid Math

```
Tile diamond:  128 wide × 64 tall
Tile faces:    top face = 128×64 diamond
               left/front faces = visible below the top face

Grid origin (in LotGrid local space):  x=640, y=90   ← north tip of grid
Grid-to-screen:
  x = 640 + (col - row) * 64
  y =  90 + (col + row) * 32

Grid: 10 columns × 8 rows
Bounding box: 1152×576 px — centered in 1280×720 viewport
```

---

## Color Palette

| Name | Hex | Usage |
|---|---|---|
| Outline | `#1E140A` | All sprite outlines |
| Grass top | `#6EAF4B` | Lot tile top face |
| Grass mid | `#559137` | Lot tile gradient end |
| Ground front | `#4B6E2D` | Lot tile front face |
| Cream body | `#F2E1AF` | L1 trailer main face |
| Cream light | `#FFF5D2` | L1 top highlight |
| Cream dark | `#C3AF7D` | L1 shadow / left face |
| Gold body | `#FFC832` | L2 trailer main face |
| Gold light | `#FFE678` | L2 highlight |
| Gold dark | `#D29B14` | L2 shadow / left face |
| Window blue | `#82C3E6` | Trailer windows |
| Trim dark | `#3C2D14` | Trim, outlines |
| Roof gray | `#8C8273` | Roof surface |
| Awning red | `#C33C28` | L2 awning stripes |
| Coin yellow | `#FFD700` | Currency icon |
| UI tan | `#D4B896` | Panel backgrounds |
| UI dark | `#3D2B1A` | Text, button borders |

---

## Sprite Dimensions

| Asset | Canvas size | Notes |
|---|---|---|
| `lot_empty.png` | 128×96 | 128×64 top diamond + 32 px front face below |
| `trailer_l1.png` | 128×160 | South-anchored; bottom of image = south vertex of tile |
| `trailer_l2.png` | 128×160 | Same footprint as L1, gold body |
| `icon_lock.png` | 32×32 | Padlock centered on transparent bg |
| `bg_park.png` | 1280×720 | Full viewport grass field with fence/decor |
| `icon_coin.png` | 24×24 | Unchanged from M4 |
| `icon_account.png` | 32×32 | Unchanged from M4 |
| `icon_quest.png` | 24×24 | Unchanged from M4 |

---

## Sprite Placement in Code

LotGrid.gd draws trailers **south-anchored**:

```gdscript
# center = grid_to_screen(col, row)  ← center of the diamond
# south vertex = center + (0, tile_height/2) = center + (0, 32)
rect = Rect2(center.x - 64, center.y + 32 - sprite_h, 128, sprite_h)
draw_texture_rect(tex, rect, false)
```

So a 128×160 trailer sprite: the bottom 32 px form the front face and skirt;
the upper portion rises above the diamond.

---

## Visual States — Lot Cells

Each lot is always in exactly one state.

### 1. Empty Lot (unlocked, no trailer)
- Isometric diamond tile: bright grass top face, slightly darker front/left faces
- Subtle texture: grass color variation, a few darker patches
- `lot_empty.png` — 128×96 (extra 32 px for the front edge)

### 2. Empty Lot — Hover
- Same tile + 30% white overlay drawn on the diamond polygon
- No separate sprite needed — LotGrid draws `HOVER_COLOR` overlay in code

### 3. Invalid Placement Flash
- 50% red overlay on the diamond for 0.3 s — drawn in code only

### 4. Level 1 Trailer (occupied)
- Isometric single-wide mobile home
- Cream body (`#F2E1AF`), lighter top face, darker left face
- Roof: gray, slightly raised
- Windows: 2× blue-glass rectangles with white glint and cross divider
- Door: center with small awning above
- Skirting panel at base
- TV antenna on roof
- Weathered look: subtle gradient shading

### 5. Level 1 Trailer — Upgrade Hover
- Gold 35% overlay on the diamond — drawn in code, no separate sprite

### 6. Level 2 Trailer (upgraded)
- Same structure as L1 but gold body (`#FFC832`)
- Red striped awning over door
- Flower box under left window
- White window trim (vs dark trim on L1)
- Darker gold left face to emphasize depth

### 7. Locked Lot
- `LOCKED_OVERLAY_COLOR` (55% black) polygon drawn over tile in code
- `icon_lock.png` (32×32) centered on the diamond center

---

## Background (`bg_park.png`)

1280×720 px — fills the entire viewport behind the grid.

- Vertical green grass gradient (lighter top → darker bottom)
- Grass texture patches (random lighter/darker rectangles)
- Perimeter fence: weathered wood planks with darker posts every 48 px
- Background details (muted, low-contrast so they don't compete with grid):
  - Water tower — top-right corner
  - Palm tree — top-left corner

---

## Draw Order (Painter's Algorithm)

LotGrid draws in this order to achieve correct isometric depth:

```
for row in range(grid_rows):
  for col in range(grid_cols):
    draw ground tile (lot_empty texture)

for row in range(grid_rows):
  for col in range(grid_cols):
    draw locked overlay  (if locked)
    draw trailer sprite  (if occupied)
    draw hover overlay   (if hovered)
    draw flash overlay   (if flashing)
```

Front rows render on top of back rows — correct for isometric perspective.

---

## UI Elements

Consistent with isometric cartoon style.

### Currency Label
- Prefix with `icon_coin.png` (24×24)
- Bold chunky font, white with dark drop shadow

### Quest Label
- Prefix with `icon_quest.png` (24×24)

### Account Button
- `icon_account.png` in rounded square button, top-right corner
- Anonymous: gray silhouette; Signed-in: colored silhouette

### Auth Screen (modal)
- Semi-transparent dark overlay behind panel
- Panel: `#D4B896` fill, `#3D2B1A` border, 4 px rounded corners
- Buttons: flat rectangles, dark border, no gradients

---

## Export Requirements

- Format: PNG, RGBA 32-bit
- Transparent background (except `bg_park.png`)
- No pre-scaling — Godot handles display scale
- `texture_filter = Linear` (set in LotGrid._ready)
- Destination: `game/assets/sprites/` (lots/trailers/bg) and `game/assets/ui/` (icons)

---

## Animation (Future — Milestone 5+)

- Income tick: coin icon floats up from trailer, fades out
- Placement: trailer drops in with squash-and-stretch
- Upgrade: golden flash, L1 → L2 swap
- Quest complete: banner slides in from top
