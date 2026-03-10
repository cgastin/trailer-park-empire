# GRAPHICS_PROMPT.md

Guidance for art agents generating sprites and UI assets for **Trailer Park Empire**.

---

## Art Style

**Pixel art, top-down isometric-lite (flat top-down, not true isometric).**

References: Stardew Valley, early FarmVille, Tiny Tower.

- Clean, chunky pixels — 16×16 or 32×32 base tile size scaled up
- Warm, slightly desaturated palette — dusty Southern US trailer park aesthetic
- Outlines: 1px dark outline on all sprites
- Lighting: flat (no dynamic shadows); baked highlight on top-left corner
- Mood: charming and a little run-down, not grim — think comedy, not tragedy

---

## Color Palette

| Name | Hex | Usage |
|---|---|---|
| Dirt ground | `#C4A882` | Empty lot background |
| Dry grass | `#8BAD6A` | Lot border / park perimeter |
| Trailer cream | `#F2E6C5` | Level 1 trailer body |
| Trailer gold | `#FFCC40` | Level 2 trailer body |
| Trailer trim | `#665A3F` | Trailer outline / trim |
| Window blue | `#8DC8EB` | Trailer windows |
| Lock shadow | `#00000099` | Locked lot overlay (55% black) |
| UI tan | `#D4B896` | Panel backgrounds |
| UI dark | `#3D2B1A` | Text, button borders |
| Coin yellow | `#FFD700` | Currency icon |

Art agents may extend this palette with 2–3 complementary accent colors, but must not stray into neon or high-saturation tones.

---

## Grid

The lot grid is **10 columns × 8 rows**, each cell **64×64 px** (world space).
All lot sprites must fit within 64×64 px including any border/padding.

Internal padding used by the current placeholder renderer: **5 px** on all sides,
leaving a **54×54 px** interior for the trailer body. Match this footprint.

---

## Visual States — Lot Cells

Each lot is always in exactly one of these states. Art must be unambiguous at a glance.

### 1. Empty Lot (unlocked, no trailer)
- Bare dirt rectangle with faint grid lines
- Subtle texture: cracked dry ground, maybe a tuft of dead grass in one corner
- No structure present

### 2. Empty Lot — Hover
- Same as empty lot with a soft white glow / highlight rim (30% white overlay)
- Indicates "click to place a trailer here"

### 3. Invalid Placement Flash
- Bright red tint (50% red overlay) — displayed for 0.3 seconds on failed placement
- No additional art needed; this is an overlay applied in code

### 4. Level 1 Trailer (occupied)
- Single-wide mobile home, cream/beige body (`#F2E6C5`)
- Dark brown trim/outline (`#665A3F`), 2 px border
- Two small rectangular windows, blue (`#8DC8EB`), positioned upper-left and upper-right of body
- Optional details: a small door, a skirt/skirting panel at the base, a tiny TV antenna
- Weathered, a little worn — chipped paint is fine

### 5. Level 1 Trailer — Upgrade Hover
- Same as Level 1 but with a gold/yellow glow rim (35% gold overlay)
- Indicates "click to upgrade"
- No hover shown on maxed trailers

### 6. Level 2 Trailer (upgraded)
- Same footprint as Level 1 but body color is warm gold (`#FFCC40`)
- Slightly more polished look: cleaner lines, a small flower box under one window,
  a new awning or carport shade over the door
- Visually distinct from Level 1 at a glance — color is the primary signal

### 7. Locked Lot
- Dark semi-transparent overlay (55% black) over the dirt background
- A padlock icon centered in the cell — simple, 16×16 px
- No trailer visible underneath

---

## Sprites Needed (Priority Order)

| Asset | Size | Notes |
|---|---|---|
| `lot_empty.png` | 64×64 | Dirt ground tile |
| `trailer_l1.png` | 54×54 | Level 1 trailer body (placed inside 5 px padding) |
| `trailer_l2.png` | 54×54 | Level 2 trailer body |
| `icon_lock.png` | 24×24 | Padlock for locked lots |
| `icon_coin.png` | 24×24 | Currency icon (shown next to currency label) |
| `bg_park.png` | 640×512 | Park background (sits behind the grid) |
| `icon_account.png` | 32×32 | Account/profile button icon |
| `icon_quest.png` | 24×24 | Quest indicator icon |

---

## Background (`bg_park.png`)

640×512 px — fills the entire play area behind the lot grid.

- Flat dirt/scrubby grass ground
- Chain-link fence or weathered wood fence along the perimeter
- A few background elements outside the fence: a water tower, a distant highway,
  maybe a single dead palm tree — low detail, muted colors so they don't compete
  with the active grid
- Sky: none (pure top-down); or a very subtle vignette if the style calls for it

---

## UI Elements

The game UI overlays the game view. UI assets use a flat, slightly distressed style
consistent with the lot art — no gradients, no gloss.

### Currency Label
- Prefix with `icon_coin.png` (24×24)
- Font: chunky pixel font (e.g., Press Start 2P or similar), white with 1 px dark drop shadow
- Example: 🪙 1,250

### Status Label
- Small text below currency — shows placement feedback and sync status
- Same font, smaller size, light gray

### Quest Label
- Prefix with `icon_quest.png`
- Shows current quest title and progress (e.g., "Place 3 trailers: 2/3")

### Account Button
- Top-right corner
- `icon_account.png` in a small rounded square button
- Two states: anonymous (gray silhouette icon) and signed-in (colored silhouette)

### Auth Screen (modal)
- Centered panel, semi-transparent dark background behind it
- Panel background: `#D4B896` (UI tan) with `#3D2B1A` border, 4 px rounded corners
- Title: "Welcome to Trailer Park Empire" in pixel font
- Buttons: flat rectangles, dark border, hover state is slightly lighter fill
- No gradients, no drop shadows on buttons

---

## Animation (Future — Milestone 5+)

Do not animate sprites yet. Note these for later:

- **Income tick**: coin icon floats up from trailer and fades (+10, +18)
- **Placement**: trailer drops in with a brief squash-and-stretch
- **Upgrade**: brief golden flash, then swap L1 → L2 sprite
- **Quest complete**: banner slides in from top

---

## Export Requirements

- Format: PNG, transparent background (except `bg_park.png` and `lot_empty.png`)
- Scale: 1× pixel art (do not pre-scale; Godot scales via `texture_filter = Nearest`)
- Naming: snake_case, as listed in the Sprites table above
- Destination: `game/assets/sprites/` (lots/trailers) and `game/assets/ui/` (icons/UI)
- Color depth: 32-bit RGBA
