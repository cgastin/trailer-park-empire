#!/usr/bin/env python3
"""
Trailer Park Empire — Isometric Sprite Generator
Cartoon pixel-art style (Stardew Valley / SimCity mobile aesthetic).

Canvas sizes:
  lot_empty.png   128×96  — drawn at Rect2(c.x-64, c.y-32, 128, 96)
                             diamond: top=(64,0) left=(0,32) right=(128,32) south=(64,64)
                             front face: y=64-96

  trailer_l*.png  128×96  — drawn at Rect2(c.x-64, c.y-64, 128, 96)
                             diamond: top=(64,32) left=(0,64) right=(128,64) south=(64,96)
                             box body: y=0-64

  icon_lock.png   32×32
"""

from PIL import Image, ImageDraw
import os
import random

SPRITES_DIR = os.path.join(os.path.dirname(__file__), "../game/assets/sprites")
UI_DIR      = os.path.join(os.path.dirname(__file__), "../game/assets/ui")

# ── Palette ───────────────────────────────────────────────────────────────────
TRANSPARENT   = (0,   0,   0,   0)
OUTLINE       = (20,  15,  8,   255)

# Grass / ground (shared across all sprites)
GRASS_LT      = (120, 185, 80,  255)
GRASS_MID     = (95,  158, 60,  255)
GRASS_DK      = (65,  120, 42,  255)
GROUND_FL     = (78,  115, 48,  255)   # front-face of tile
GROUND_FL_DK  = (55,  88,  32,  255)

# L1 trailer — beat-up single-wide
L1_ROOF       = (139, 115, 85,  255)   # #8B7355 dull gray-brown
L1_ROOF_LT    = (162, 138, 105, 255)
L1_SIDE       = (196, 163, 90,  255)   # #C4A35A tan/rust left face
L1_SIDE_DK    = (172, 140, 72,  255)
L1_FRONT      = (184, 149, 90,  255)   # #B8955A slightly darker right face
L1_FRONT_DK   = (158, 125, 68,  255)
L1_SKIRT      = (74,  92,  42,  255)   # #4A5C2A dark green-brown skirting

# L2 trailer — clean double-wide
L2_ROOF       = (232, 232, 232, 255)   # #E8E8E8 white-gray
L2_ROOF_LT    = (248, 248, 248, 255)
L2_SIDE       = (245, 240, 224, 255)   # #F5F0E0 white/cream
L2_SIDE_DK    = (215, 208, 185, 255)
L2_FRONT      = (238, 232, 215, 255)
L2_FRONT_DK   = (208, 200, 178, 255)
L2_SKIRT      = (180, 175, 160, 255)
L2_AWNING     = (192, 57,  43,  255)   # #C0392B red awning
L2_AWNING_DK  = (140, 38,  28,  255)

# Shared details
WINDOW_FRAME  = (40,  30,  15,  255)
WINDOW_BLUE   = (135, 200, 235, 255)
WINDOW_DK     = (75,  145, 185, 255)
CRACK_DK      = (30,  22,  10,  255)
DOOR_BROWN    = (105, 72,  38,  255)
DOOR_LT       = (138, 100, 58,  255)
KNOB_GOLD     = (210, 170, 30,  255)
FLOWER_RED    = (210, 55,  55,  255)
FLOWER_PINK   = (230, 125, 125, 255)
FLOWER_GREEN  = (70,  128, 50,  255)
FLOWER_SOIL   = (88,  58,  28,  255)
ANTENNA       = (105, 100, 88,  255)
DISH_GRAY     = (160, 155, 145, 255)
DISH_DK       = (105, 100, 90,  255)

# Lock
LOCK_GRAY     = (88,  88,  98,  255)
LOCK_LT       = (165, 165, 180, 255)
LOCK_DK       = (55,  55,  65,  255)
LOCK_GOLD     = (208, 168, 28,  255)
LOCK_GOLD_LT  = (248, 218, 82,  255)


# ── Drawing helpers ────────────────────────────────────────────────────────────

def px(draw, x, y, c):
    draw.point((x, y), fill=c)

def hline(draw, x1, x2, y, c):
    if x2 >= x1:
        draw.line([(x1, y), (x2, y)], fill=c)

def vline(draw, x, y1, y2, c):
    if y2 >= y1:
        draw.line([(x, y1), (x, y2)], fill=c)

def rect(draw, x1, y1, x2, y2, c):
    draw.rectangle([x1, y1, x2, y2], fill=c)

def grad_rect(draw, x1, y1, x2, y2, c_top, c_bot):
    h = max(y2 - y1, 1)
    for y in range(y1, y2 + 1):
        t = (y - y1) / h
        c = tuple(int(c_top[i] + (c_bot[i] - c_top[i]) * t) for i in range(4))
        hline(draw, x1, x2, y, c)

def poly(draw, pts, fill, outline=None):
    draw.polygon(pts, fill=fill)
    if outline:
        draw.polygon(pts, outline=outline)


# ── Grass diamond fill (reusable) ─────────────────────────────────────────────

def draw_grass_diamond(draw, cx, cy, hw, hh, rng_seed=7):
    """Fill the isometric diamond top-face with grass checkerboard."""
    rng = random.Random(rng_seed)
    for row in range(hh + 1):
        t = row / max(hh, 1)
        span = int(row * hw / hh)
        c = tuple(int(GRASS_LT[i] + (GRASS_MID[i] - GRASS_LT[i]) * t) for i in range(4))
        hline(draw, cx - span, cx + span, cy - hh + row, c)
        if row > 0:
            hline(draw, cx - span, cx + span, cy + hh - row, c)
    hline(draw, cx, cx, cy + hh, GRASS_MID)  # south vertex row
    # Texture spots
    for _ in range(55):
        sx = rng.randint(cx - hw + 5, cx + hw - 5)
        sy = rng.randint(cy - hh + 3, cy + hh - 3)
        dx = abs(sx - cx) / hw
        dy = abs(sy - cy) / hh
        if dx + dy <= 0.88:
            spot = GRASS_DK if rng.random() > 0.5 else (130, 195, 88, 255)
            draw.point((sx, sy), fill=spot)


def draw_front_faces(draw, cx, cy, hw, hh, face_h):
    """Draw the two front-face parallelograms below the south vertex."""
    south_y = cy + hh
    for fy in range(face_h):
        t = fy / max(face_h - 1, 1)
        c = tuple(int(GROUND_FL[i] + (GROUND_FL_DK[i] - GROUND_FL[i]) * t) for i in range(4))
        # Left front face
        lx = cx - int(fy * hw / face_h)
        hline(draw, lx, cx, south_y + fy, c)
        # Right front face
        rx = cx + int((face_h - fy) * hw / face_h)
        if rx > cx:
            hline(draw, cx, rx, south_y + fy, c)


# ── 1. lot_empty.png — 128×96 ─────────────────────────────────────────────────
# Rendered at Rect2(c.x-64, c.y-32, 128, 96)
# Diamond: top=(64,0) left=(0,32) right=(128,32) south=(64,64)

def generate_lot_empty():
    W, H = 128, 96
    img = Image.new("RGBA", (W, H), TRANSPARENT)
    draw = ImageDraw.Draw(img)

    cx, cy = 64, 32   # diamond center in sprite coords
    hw, hh = 64, 32

    draw_grass_diamond(draw, cx, cy, hw, hh, rng_seed=7)

    # Dirt/mud patches near edges
    rng = random.Random(42)
    for _ in range(12):
        ex = rng.randint(cx - hw + 2, cx + hw - 2)
        ey = rng.randint(cy - hh + 2, cy + hh - 2)
        dx = abs(ex - cx) / hw
        dy = abs(ey - cy) / hh
        if 0.65 < dx + dy < 0.90:
            for ddx in range(-1, 2):
                for ddy in range(-1, 2):
                    nx, ny = ex + ddx, ey + ddy
                    ndx = abs(nx - cx) / hw
                    ndy = abs(ny - cy) / hh
                    if ndx + ndy <= 0.92:
                        draw.point((nx, ny), fill=(88, 62, 35, 200))

    draw_front_faces(draw, cx, cy, hw, hh, face_h=32)

    # Diamond outline
    pts = [(cx, cy - hh), (cx + hw, cy), (cx, cy + hh), (cx - hw, cy), (cx, cy - hh)]
    draw.line(pts, fill=OUTLINE, width=1)

    img.save(os.path.join(SPRITES_DIR, "lot_empty.png"))
    print("Generated: lot_empty.png  128×96")


# ── 2. trailer_l1.png — 128×96 beat-up single-wide ───────────────────────────
# Rendered at Rect2(c.x-64, c.y-64, 128, 96)
# Diamond: top=(64,32) left=(0,64) right=(128,64) south=(64,96)
# Box body: occupies y=0-64

def generate_trailer_l1():
    W, H = 128, 96
    img = Image.new("RGBA", (W, H), TRANSPARENT)
    draw = ImageDraw.Draw(img)

    # --- Grass diamond (centered at 64,64 with hw=64,hh=32) ---
    cx, cy = 64, 64   # diamond center
    hw, hh = 64, 32
    draw_grass_diamond(draw, cx, cy, hw, hh, rng_seed=13)
    # No front face — south vertex is at bottom of canvas (64,96)

    # --- Isometric box definition ---
    # Box sits on the diamond top surface.
    # Front base: left=(0,64), right=(128,64)  [at diamond equator]
    # Back base:  left=(40,52), right=(88,52)  [on the diamond's top face]
    # Box height (screen): 28px
    BOX_H = 28
    FL = (0,   64)    # front-left base
    FR = (128, 64)    # front-right base
    BL = (40,  52)    # back-left base
    BR = (88,  52)    # back-right base

    fl_t = (FL[0], FL[1] - BOX_H)   # (0,  36)
    fr_t = (FR[0], FR[1] - BOX_H)   # (128,36)
    bl_t = (BL[0], BL[1] - BOX_H)   # (40, 24)
    br_t = (BR[0], BR[1] - BOX_H)   # (88, 24)

    # --- Left face (left side of trailer) ---
    left_pts = [FL, fl_t, bl_t, BL]
    poly(draw, left_pts, L1_SIDE)
    # Horizontal siding lines
    for y in range(fl_t[1] + 2, FL[1], 3):
        # Interpolate x bounds at this y
        t_side = (y - fl_t[1]) / max(FL[1] - fl_t[1], 1)
        lx = int(FL[0] + (BL[0] - FL[0]) * t_side)
        rx_top = int(fl_t[0] + (bl_t[0] - fl_t[0]) * (y - fl_t[1]) / max(FL[1] - fl_t[1], 1))
        # left edge x of this scan line
        x_left = int(FL[0] * (1 - t_side) + BL[0] * t_side)
        x_right = int(fl_t[0] * (1 - t_side) + bl_t[0] * t_side)
        hline(draw, x_left, x_right, y, L1_SIDE_DK)

    # Window on left face (cracked)
    # Face roughly: left edge x=0..40, y=36..64
    # Window at y=40-48, x=8-18
    ww_x1, ww_y1, ww_x2, ww_y2 = 8, 40, 20, 50
    rect(draw, ww_x1 - 1, ww_y1 - 1, ww_x2 + 1, ww_y2 + 1, WINDOW_FRAME)
    rect(draw, ww_x1, ww_y1, ww_x2, ww_y2, WINDOW_BLUE)
    # Cracked pane
    draw.line([(ww_x1 + 1, ww_y1 + 1), (ww_x2 - 2, ww_y2 - 2)], fill=CRACK_DK)
    draw.line([(ww_x1 + 4, ww_y1 + 1), (ww_x1 + 1, ww_y2 - 2)], fill=CRACK_DK)

    poly(draw, left_pts, None, OUTLINE)

    # --- Right face (front of trailer) ---
    right_pts = [FR, fr_t, br_t, BR]
    poly(draw, right_pts, L1_FRONT)
    # Horizontal siding lines
    for y in range(fr_t[1] + 2, FR[1], 3):
        t_side = (y - fr_t[1]) / max(FR[1] - fr_t[1], 1)
        x_left = int(fr_t[0] + (br_t[0] - fr_t[0]) * t_side)
        x_right = int(FR[0] + (BR[0] - FR[0]) * t_side)
        hline(draw, x_left, x_right, y, L1_FRONT_DK)

    # Window on right face at y=40-48, x=100-112
    rw_x1, rw_y1, rw_x2, rw_y2 = 100, 40, 112, 50
    rect(draw, rw_x1 - 1, rw_y1 - 1, rw_x2 + 1, rw_y2 + 1, WINDOW_FRAME)
    rect(draw, rw_x1, rw_y1, rw_x2, rw_y2, WINDOW_BLUE)
    vline(draw, (rw_x1 + rw_x2) // 2, rw_y1, rw_y2, WINDOW_FRAME)

    # Door on right face, roughly x=108-120, y=50-64
    dr_x1, dr_y1, dr_x2, dr_y2 = 108, 50, 120, 64
    rect(draw, dr_x1 - 1, dr_y1 - 1, dr_x2 + 1, dr_y2, DOOR_BROWN)
    grad_rect(draw, dr_x1, dr_y1, dr_x2, dr_y2, DOOR_LT, DOOR_BROWN)
    px(draw, dr_x1 + 2, (dr_y1 + dr_y2) // 2, KNOB_GOLD)

    poly(draw, right_pts, None, OUTLINE)

    # --- Roof face ---
    roof_pts = [fl_t, bl_t, br_t, fr_t]
    poly(draw, roof_pts, L1_ROOF)
    # Slight dent / variation
    mid_y = (fl_t[1] + bl_t[1]) // 2
    hline(draw, fl_t[0] + 5, fr_t[0] - 5, mid_y + 2, L1_ROOF_LT)
    hline(draw, fl_t[0] + 8, fr_t[0] - 8, mid_y + 4, L1_SIDE_DK)
    poly(draw, roof_pts, None, OUTLINE)

    # Uneven roofline (1-2px variance)
    for x in range(fl_t[0] + 2, fr_t[0] - 2, 4):
        px(draw, x, fl_t[1] - 1 + (x % 3 == 0), L1_ROOF_LT)

    # Antenna
    vline(draw, 72, fl_t[1] - 7, fl_t[1], ANTENNA)
    hline(draw, 68, 76, fl_t[1] - 5, ANTENNA)

    # --- Skirting strip at base of faces ---
    # Left face bottom 4px
    for fy in range(4):
        t = (FL[1] - 4 + fy - fl_t[1]) / max(FL[1] - fl_t[1], 1)
        lx = int(FL[0] * (1 - t) + BL[0] * t)
        rx = int(fl_t[0] * (1 - t) + bl_t[0] * t)
        hline(draw, lx, rx, FL[1] - 4 + fy, L1_SKIRT)
    # Right face bottom 4px
    for fy in range(4):
        t = (FR[1] - 4 + fy - fr_t[1]) / max(FR[1] - fr_t[1], 1)
        lx = int(fr_t[0] * (1 - t) + br_t[0] * t)
        rx = int(FR[0] * (1 - t) + BR[0] * t)
        hline(draw, lx, rx, FR[1] - 4 + fy, L1_SKIRT)

    # Diamond outline
    dpts = [(cx, cy - hh), (cx + hw, cy), (cx, cy + hh), (cx - hw, cy), (cx, cy - hh)]
    draw.line(dpts, fill=OUTLINE, width=1)

    img.save(os.path.join(SPRITES_DIR, "trailer_l1.png"))
    print("Generated: trailer_l1.png  128×96")


# ── 3. trailer_l2.png — 128×96 clean double-wide ─────────────────────────────

def generate_trailer_l2():
    W, H = 128, 96
    img = Image.new("RGBA", (W, H), TRANSPARENT)
    draw = ImageDraw.Draw(img)

    cx, cy = 64, 64
    hw, hh = 64, 32
    draw_grass_diamond(draw, cx, cy, hw, hh, rng_seed=13)

    # Slightly taller box (32px) — double-wide
    BOX_H = 32
    FL = (0,   64)
    FR = (128, 64)
    BL = (40,  52)
    BR = (88,  52)

    fl_t = (FL[0], FL[1] - BOX_H)   # (0,  32)
    fr_t = (FR[0], FR[1] - BOX_H)   # (128,32)
    bl_t = (BL[0], BL[1] - BOX_H)   # (40, 20)
    br_t = (BR[0], BR[1] - BOX_H)   # (88, 20)

    # --- Left face ---
    left_pts = [FL, fl_t, bl_t, BL]
    poly(draw, left_pts, L2_SIDE)
    # Vertical siding lines (cleaner than L1)
    for x in range(6, 38, 6):
        y_top = int(fl_t[1] + (bl_t[1] - fl_t[1]) * x / 40)
        y_bot = int(FL[1] + (BL[1] - FL[1]) * x / 40)
        vline(draw, x, y_top, y_bot, L2_SIDE_DK)

    # Two windows on left face
    for wx, wy1 in [(6, 38), (18, 38)]:
        wy2 = wy1 + 9
        rect(draw, wx - 1, wy1 - 1, wx + 7, wy2 + 1, OUTLINE)
        rect(draw, wx, wy1, wx + 6, wy2, WINDOW_BLUE)
        vline(draw, wx + 3, wy1, wy2, WINDOW_FRAME)
        px(draw, wx + 1, wy1 + 1, (200, 235, 255, 255))

    poly(draw, left_pts, None, OUTLINE)

    # --- Right face ---
    right_pts = [FR, fr_t, br_t, BR]
    poly(draw, right_pts, L2_FRONT)
    # Clean vertical lines
    for xi in range(3):
        x = 96 + xi * 10
        t = (x - 88) / 40.0
        y_top = int(fr_t[1] + (br_t[1] - fr_t[1]) * t)
        y_bot = int(FR[1] + (BR[1] - FR[1]) * t)
        vline(draw, x, y_top, y_bot, L2_FRONT_DK)

    # Window on right face
    rw_x1, rw_y1, rw_x2, rw_y2 = 92, 38, 102, 48
    rect(draw, rw_x1 - 1, rw_y1 - 1, rw_x2 + 1, rw_y2 + 1, OUTLINE)
    rect(draw, rw_x1, rw_y1, rw_x2, rw_y2, WINDOW_BLUE)
    vline(draw, (rw_x1 + rw_x2) // 2, rw_y1, rw_y2, WINDOW_FRAME)
    px(draw, rw_x1 + 1, rw_y1 + 1, (200, 235, 255, 255))

    # Door with red awning on right face
    dr_x1, dr_y1, dr_x2, dr_y2 = 110, 50, 122, 64
    rect(draw, dr_x1 - 1, dr_y1 - 1, dr_x2 + 1, dr_y2, OUTLINE)
    grad_rect(draw, dr_x1, dr_y1, dr_x2, dr_y2, (210, 185, 110, 255), DOOR_BROWN)
    px(draw, dr_x1 + 2, (dr_y1 + dr_y2) // 2, KNOB_GOLD)
    # Awning
    awning_pts = [(dr_x1 - 3, dr_y1 - 1), (dr_x2 + 3, dr_y1 - 1),
                  (dr_x2 + 1, dr_y1 - 5), (dr_x1 - 1, dr_y1 - 5)]
    poly(draw, awning_pts, L2_AWNING, OUTLINE)
    for sx in range(dr_x1 - 2, dr_x2 + 3, 3):
        vline(draw, sx, dr_y1 - 5, dr_y1 - 1, L2_AWNING_DK)

    # Flower box below left window
    fb_y = 49
    rect(draw, 5, fb_y, 26, fb_y + 5, OUTLINE)
    rect(draw, 6, fb_y + 1, 25, fb_y + 4, FLOWER_SOIL)
    for i, fc in enumerate([FLOWER_RED, FLOWER_PINK, FLOWER_RED, FLOWER_PINK]):
        fx = 7 + i * 4
        px(draw, fx, fb_y + 1, fc)
        px(draw, fx, fb_y + 2, FLOWER_GREEN)

    poly(draw, right_pts, None, OUTLINE)

    # --- Roof face ---
    roof_pts = [fl_t, bl_t, br_t, fr_t]
    poly(draw, roof_pts, L2_ROOF)
    # Clean highlight near ridge
    mid_y = (fl_t[1] + bl_t[1]) // 2
    hline(draw, fl_t[0] + 4, fr_t[0] - 4, mid_y + 1, L2_ROOF_LT)
    poly(draw, roof_pts, None, OUTLINE)

    # Satellite dish on roof
    dish_cx, dish_cy = 55, 24
    draw.ellipse([dish_cx - 4, dish_cy - 2, dish_cx + 4, dish_cy + 2], fill=DISH_GRAY, outline=DISH_DK)
    vline(draw, dish_cx, dish_cy + 2, dish_cy + 5, DISH_DK)

    # Diamond outline
    dpts = [(cx, cy - hh), (cx + hw, cy), (cx, cy + hh), (cx - hw, cy), (cx, cy - hh)]
    draw.line(dpts, fill=OUTLINE, width=1)

    img.save(os.path.join(SPRITES_DIR, "trailer_l2.png"))
    print("Generated: trailer_l2.png  128×96")


# ── 4. icon_lock.png — 32×32 ──────────────────────────────────────────────────

def generate_icon_lock():
    img = Image.new("RGBA", (32, 32), TRANSPARENT)
    draw = ImageDraw.Draw(img)

    # Body
    rect(draw, 5, 15, 26, 28, LOCK_GRAY)
    draw.rectangle([5, 15, 26, 28], outline=OUTLINE)
    # Highlight edge
    hline(draw, 6, 25, 16, LOCK_LT)
    vline(draw, 6, 16, 27, LOCK_LT)

    # Keyhole
    draw.ellipse([12, 19, 18, 25], fill=LOCK_DK)
    rect(draw, 14, 23, 16, 27, LOCK_DK)

    # Shackle (gold arc)
    vline(draw, 10, 6, 15, LOCK_GOLD)
    vline(draw, 11, 6, 15, LOCK_GOLD)
    vline(draw, 20, 6, 15, LOCK_GOLD)
    vline(draw, 21, 6, 15, LOCK_GOLD)
    # Arc top
    for pt in [(12, 4), (13, 3), (14, 3), (15, 3), (16, 3), (17, 3), (18, 4), (19, 5)]:
        draw.point(pt, fill=LOCK_GOLD)
    for pt in [(12, 3), (13, 2), (14, 2), (15, 2), (16, 2), (17, 2), (18, 3), (19, 4)]:
        draw.point(pt, fill=LOCK_GOLD)
    # Highlight
    vline(draw, 10, 6, 13, LOCK_GOLD_LT)
    # Outline shackle
    for y in range(5, 15):
        draw.point((9, y), fill=OUTLINE)
        draw.point((22, y), fill=OUTLINE)
    for pt in [(10, 1), (11, 1), (12, 1), (13, 1), (14, 1),
               (15, 1), (16, 1), (17, 1), (18, 1), (19, 2), (20, 3), (21, 4)]:
        draw.point(pt, fill=OUTLINE)
    draw.point((9, 2), fill=OUTLINE)

    img.save(os.path.join(SPRITES_DIR, "icon_lock.png"))
    print("Generated: icon_lock.png  32×32")


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    os.makedirs(SPRITES_DIR, exist_ok=True)
    os.makedirs(UI_DIR, exist_ok=True)

    print("Generating Trailer Park Empire sprites...")
    generate_lot_empty()
    generate_trailer_l1()
    generate_trailer_l2()
    generate_icon_lock()

    print("\nVerifying output:")
    for fname in ["lot_empty.png", "trailer_l1.png", "trailer_l2.png", "icon_lock.png"]:
        path = os.path.join(SPRITES_DIR, fname)
        if os.path.exists(path):
            im = Image.open(path)
            size = os.path.getsize(path)
            print(f"  OK  {fname:25s} {im.size[0]}×{im.size[1]}  ({size:,} bytes)")
        else:
            print(f"  MISSING: {fname}")
