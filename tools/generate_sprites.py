#!/usr/bin/env python3
"""
Trailer Park Empire — Isometric Sprite Generator (FarmVille cartoon style)
All sprites drawn with Pillow. Smooth gradients, bold outlines, saturated colors.

Isometric tile: 128×64 px diamond
Trailer sprites: 128×160 px (sits above the diamond, south-anchored)
"""

from PIL import Image, ImageDraw
import os
import math
import random

SPRITES_DIR = "/Users/chrisgastin/dev/trailer-park-empire/game/assets/sprites"
UI_DIR      = "/Users/chrisgastin/dev/trailer-park-empire/game/assets/ui"

# ── Palette ──────────────────────────────────────────────────────────────────
OUTLINE       = (30,  20,  10,  255)
WHITE         = (255, 255, 255, 255)
BLACK         = (0,   0,   0,   255)
TRANSPARENT   = (0,   0,   0,   0)

# Grass / ground
GRASS_TOP     = (110, 175, 75,  255)
GRASS_MID     = (85,  148, 55,  255)
GRASS_DARK    = (60,  115, 38,  255)
GROUND_FRONT  = (75,  110, 45,  255)   # front face of iso tile
GROUND_FL_DK  = (55,  85,  30,  255)   # darker front face edge

# Trailer L1 — cream
CREAM         = (242, 225, 175, 255)
CREAM_LT      = (255, 245, 210, 255)
CREAM_DK      = (195, 175, 125, 255)
WALL_LEFT     = (210, 190, 140, 255)   # left face (in shadow)
WALL_FRONT    = (185, 160, 110, 255)   # front face

# Trailer L2 — gold
GOLD          = (255, 200, 50,  255)
GOLD_LT       = (255, 230, 120, 255)
GOLD_DK       = (210, 155, 20,  255)
GOLD_LEFT     = (230, 170, 35,  255)
GOLD_FRONT    = (190, 130, 15,  255)

# Shared trailer details
TRIM          = (60,  45,  20,  255)
ROOF_GRAY     = (140, 130, 115, 255)
ROOF_LT       = (175, 165, 148, 255)
WINDOW_BLUE   = (130, 195, 230, 255)
WINDOW_DK     = (70,  140, 180, 255)
WINDOW_FRAME  = (45,  35,  18,  255)
DOOR_BROWN    = (130, 95,  55,  255)
DOOR_LT       = (165, 128, 78,  255)
SKIRTING      = (90,  78,  55,  255)
AWNING_RED    = (195, 60,  40,  255)
AWNING_DK     = (140, 38,  22,  255)
FLOWER_RED    = (215, 60,  60,  255)
FLOWER_PINK   = (235, 130, 130, 255)
FLOWER_GREEN  = (75,  130, 55,  255)
ANTENNA       = (110, 105, 90,  255)

# Lock
LOCK_GRAY     = (85,  85,  95,  255)
LOCK_LT       = (170, 170, 185, 255)
LOCK_DK       = (55,  55,  65,  255)
LOCK_GOLD     = (205, 165, 28,  255)
LOCK_GOLD_LT  = (245, 215, 80,  255)
LOCK_GOLD_DK  = (155, 125, 18,  255)

# UI / coins
COIN_YELLOW   = (255, 215, 0,   255)
COIN_ORANGE   = (220, 165, 0,   255)
COIN_LT       = (255, 238, 130, 255)
UI_TAN        = (212, 184, 150, 255)
UI_DARK       = (61,  43,  26,  255)

# Background
BG_GRASS      = (100, 165, 68,  255)
BG_GRASS_DK   = (72,  128, 48,  255)
BG_GRASS_LT   = (130, 195, 90,  255)
FENCE_WOOD    = (160, 128, 80,  255)
FENCE_DK      = (110, 84,  48,  255)
FENCE_LT      = (195, 160, 110, 255)
POST_BROWN    = (95,  65,  32,  255)


# ── Low-level drawing helpers ─────────────────────────────────────────────────

def px(draw, x, y, color):
    draw.point((x, y), fill=color)


def rect(draw, x1, y1, x2, y2, color):
    draw.rectangle([x1, y1, x2, y2], fill=color)


def hline(draw, x1, x2, y, color):
    for x in range(x1, x2 + 1):
        draw.point((x, y), fill=color)


def vline(draw, x, y1, y2, color):
    for y in range(y1, y2 + 1):
        draw.point((x, y), fill=color)


def gradient_rect(draw, x1, y1, x2, y2, color_top, color_bot):
    """Vertical gradient over a rectangle."""
    h = y2 - y1
    if h <= 0:
        return
    for y in range(y1, y2 + 1):
        t = (y - y1) / h
        c = tuple(int(color_top[i] + (color_bot[i] - color_top[i]) * t) for i in range(4))
        hline(draw, x1, x2, y, c)


def draw_circle_filled(draw, cx, cy, r, color):
    for y in range(cy - r, cy + r + 1):
        for x in range(cx - r, cx + r + 1):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                draw.point((x, y), fill=color)


def draw_circle_outline(draw, cx, cy, r, color, thickness=1.5):
    for y in range(cy - r - 1, cy + r + 2):
        for x in range(cx - r - 1, cx + r + 2):
            d2 = (x - cx) ** 2 + (y - cy) ** 2
            if r * r < d2 <= (r + thickness) * (r + thickness):
                draw.point((x, y), fill=color)


# ── 1. lot_empty.png — 128×64 isometric grass tile ───────────────────────────
def generate_lot_empty():
    W, H = 128, 96   # extra height for front face
    img = Image.new("RGBA", (W, H), TRANSPARENT)
    draw = ImageDraw.Draw(img)

    hw, hh = 64, 32   # half tile width/height for the diamond top face

    # Diamond top face — grass gradient (light north → dark south)
    # Build by filling horizontal spans
    for row in range(hh + 1):
        t = row / hh
        span = int(row * (hw / hh))
        c = tuple(int(GRASS_TOP[i] + (GRASS_MID[i] - GRASS_TOP[i]) * t) for i in range(4))
        # upper half
        hline(draw, hw - span, hw + span, hh - row, c)
        # lower half
        hline(draw, hw - span, hw + span, hh + row, c)

    # Grass texture variation — random darker/lighter spots
    rng = random.Random(7)
    for _ in range(60):
        sx = rng.randint(20, 108)
        sy = rng.randint(5, 58)
        dx = abs(sx - hw) / hw
        dy = abs(sy - hh) / hh
        if dx + dy <= 0.92:
            spot_c = GRASS_DARK if rng.random() > 0.5 else BG_GRASS_LT
            draw.point((sx, sy), fill=spot_c)

    # Front left face (parallelogram below west–south edge)
    face_h = 32
    for fy in range(face_h):
        t = fy / face_h
        c = tuple(int(GROUND_FRONT[i] + (GROUND_FL_DK[i] - GROUND_FRONT[i]) * t) for i in range(4))
        left_x  = hw - int(fy * hw / face_h)
        right_x = hw
        if left_x <= right_x:
            hline(draw, left_x, right_x, hh + hh + fy, c)

    # Front right face (parallelogram below south–east edge)
    for fy in range(face_h):
        t = fy / face_h
        c = tuple(int(GROUND_FRONT[i] + (GROUND_FL_DK[i] - GROUND_FRONT[i]) * t) for i in range(4))
        left_x  = hw
        right_x = hw + int((face_h - fy) * hw / face_h)
        if left_x <= right_x:
            hline(draw, left_x, right_x, hh + hh + fy, c)

    # Diamond outline
    pts = [(hw, 0), (W - 1, hh), (hw, hh * 2), (0, hh), (hw, 0)]
    draw.line(pts, fill=OUTLINE, width=2)

    img.save(os.path.join(SPRITES_DIR, "lot_empty.png"))
    print("Generated: lot_empty.png (128×96)")


# ── 2. trailer_l1.png — 128×160 isometric Level 1 trailer ────────────────────
def generate_trailer_l1():
    W, H = 128, 160
    img = Image.new("RGBA", (W, H), TRANSPARENT)
    draw = ImageDraw.Draw(img)

    # Layout (south-anchored — bottom of image = south vertex of diamond)
    # Dimensions of the body on top face
    body_top_y  = 20    # top of roof
    body_bot_y  = 115   # bottom of body / top of front face
    body_left   = 16    # left edge of top face
    body_right  = 112   # right edge of top face
    bw = body_right - body_left  # 96

    # ── Roof (top face, cream-ish) ──
    gradient_rect(draw, body_left, body_top_y, body_right, body_top_y + 12, ROOF_LT, ROOF_GRAY)
    draw.rectangle([body_left, body_top_y, body_right, body_top_y + 12], outline=OUTLINE)

    # Antenna
    vline(draw, 88, body_top_y - 14, body_top_y, ANTENNA)
    hline(draw, 83, 93, body_top_y - 12, ANTENNA)
    hline(draw, 83, 93, body_top_y - 10, ANTENNA)

    # ── Main wall — top face (front-facing, lighter) ──
    gradient_rect(draw, body_left, body_top_y + 12, body_right, body_bot_y, CREAM_LT, CREAM)

    # Left window
    wx1, wy1, wx2, wy2 = body_left + 6, body_top_y + 18, body_left + 30, body_top_y + 40
    rect(draw, wx1 - 2, wy1 - 2, wx2 + 2, wy2 + 2, WINDOW_FRAME)
    gradient_rect(draw, wx1, wy1, wx2, wy2, WINDOW_BLUE, WINDOW_DK)
    vline(draw, (wx1 + wx2) // 2, wy1, wy2, WINDOW_FRAME)
    hline(draw, wx1, wx2, (wy1 + wy2) // 2, WINDOW_FRAME)
    px(draw, wx1 + 1, wy1 + 1, WHITE)
    px(draw, wx1 + 2, wy1 + 1, WHITE)
    px(draw, wx1 + 1, wy1 + 2, WHITE)

    # Right window
    wx1r, wx2r = body_right - 30, body_right - 6
    rect(draw, wx1r - 2, wy1 - 2, wx2r + 2, wy2 + 2, WINDOW_FRAME)
    gradient_rect(draw, wx1r, wy1, wx2r, wy2, WINDOW_BLUE, WINDOW_DK)
    vline(draw, (wx1r + wx2r) // 2, wy1, wy2, WINDOW_FRAME)
    hline(draw, wx1r, wx2r, (wy1 + wy2) // 2, WINDOW_FRAME)
    px(draw, wx1r + 1, wy1 + 1, WHITE)
    px(draw, wx1r + 2, wy1 + 1, WHITE)

    # Door
    dx1, dx2 = 54, 74
    dy1, dy2 = body_top_y + 55, body_bot_y
    rect(draw, dx1 - 2, dy1 - 2, dx2 + 2, dy2, TRIM)
    gradient_rect(draw, dx1, dy1, dx2, dy2, DOOR_LT, DOOR_BROWN)
    px(draw, dx2 - 3, (dy1 + dy2) // 2, COIN_YELLOW)

    # Small awning
    draw.polygon([(dx1 - 4, dy1 - 2), (dx2 + 4, dy1 - 2), (dx2 + 2, dy1 - 8), (dx1 - 2, dy1 - 8)], fill=TRIM)

    # Skirting at base
    rect(draw, body_left, body_bot_y, body_right, body_bot_y + 8, SKIRTING)
    for sx in range(body_left + 8, body_right, 12):
        vline(draw, sx, body_bot_y, body_bot_y + 8, TRIM)

    # Body outline
    draw.rectangle([body_left, body_top_y + 12, body_right, body_bot_y + 8], outline=OUTLINE)

    # ── Left side face (darker, shadowed) ──
    # Parallelogram: from (body_left, body_top_y+12) slanting left and down
    side_depth = 20
    pts_left = [
        (body_left,              body_top_y + 12),
        (body_left - side_depth, body_top_y + 12 + side_depth // 2),
        (body_left - side_depth, body_bot_y + 8  + side_depth // 2),
        (body_left,              body_bot_y + 8),
    ]
    draw.polygon(pts_left, fill=WALL_LEFT)
    draw.polygon(pts_left, outline=OUTLINE)

    # ── Front base face ──
    pts_front = [
        (body_left,              body_bot_y + 8),
        (body_left - side_depth, body_bot_y + 8 + side_depth // 2),
        (body_right - side_depth, body_bot_y + 8 + side_depth // 2),
        (body_right,             body_bot_y + 8),
    ]
    draw.polygon(pts_front, fill=WALL_FRONT)
    draw.polygon(pts_front, outline=OUTLINE)

    img.save(os.path.join(SPRITES_DIR, "trailer_l1.png"))
    print("Generated: trailer_l1.png (128×160)")


# ── 3. trailer_l2.png — 128×160 isometric Level 2 trailer (gold) ─────────────
def generate_trailer_l2():
    W, H = 128, 160
    img = Image.new("RGBA", (W, H), TRANSPARENT)
    draw = ImageDraw.Draw(img)

    body_top_y  = 20
    body_bot_y  = 115
    body_left   = 16
    body_right  = 112

    # ── Roof ──
    gradient_rect(draw, body_left, body_top_y, body_right, body_top_y + 12, ROOF_LT, ROOF_GRAY)
    draw.rectangle([body_left, body_top_y, body_right, body_top_y + 12], outline=OUTLINE)

    # Antenna
    vline(draw, 88, body_top_y - 14, body_top_y, ANTENNA)
    hline(draw, 83, 93, body_top_y - 12, ANTENNA)
    hline(draw, 83, 93, body_top_y - 10, ANTENNA)

    # ── Main wall — gold ──
    gradient_rect(draw, body_left, body_top_y + 12, body_right, body_bot_y, GOLD_LT, GOLD)

    # Left window (white trim)
    wx1, wy1, wx2, wy2 = body_left + 6, body_top_y + 18, body_left + 30, body_top_y + 40
    rect(draw, wx1 - 2, wy1 - 2, wx2 + 2, wy2 + 2, WHITE)
    gradient_rect(draw, wx1, wy1, wx2, wy2, WINDOW_BLUE, WINDOW_DK)
    vline(draw, (wx1 + wx2) // 2, wy1, wy2, WHITE)
    hline(draw, wx1, wx2, (wy1 + wy2) // 2, WHITE)
    px(draw, wx1 + 1, wy1 + 1, WHITE)
    px(draw, wx1 + 2, wy1 + 1, WHITE)

    # Flower box under left window
    rect(draw, wx1 - 2, wy2 + 2, wx2 + 2, wy2 + 10, TRIM)
    rect(draw, wx1 - 1, wy2 + 3, wx2 + 1, wy2 + 9, (90, 60, 30, 255))
    for i, fc in enumerate([FLOWER_RED, FLOWER_PINK, FLOWER_RED, FLOWER_PINK, FLOWER_RED]):
        fx = wx1 + 2 + i * 4
        px(draw, fx, wy2 + 4, fc)
        px(draw, fx, wy2 + 5, fc)
        px(draw, fx, wy2 + 6, FLOWER_GREEN)

    # Right window
    wx1r, wx2r = body_right - 30, body_right - 6
    rect(draw, wx1r - 2, wy1 - 2, wx2r + 2, wy2 + 2, WHITE)
    gradient_rect(draw, wx1r, wy1, wx2r, wy2, WINDOW_BLUE, WINDOW_DK)
    vline(draw, (wx1r + wx2r) // 2, wy1, wy2, WHITE)
    hline(draw, wx1r, wx2r, (wy1 + wy2) // 2, WHITE)
    px(draw, wx1r + 1, wy1 + 1, WHITE)
    px(draw, wx1r + 2, wy1 + 1, WHITE)

    # Door
    dx1, dx2 = 54, 74
    dy1, dy2 = body_top_y + 55, body_bot_y
    rect(draw, dx1 - 2, dy1 - 2, dx2 + 2, dy2, TRIM)
    gradient_rect(draw, dx1, dy1, dx2, dy2, (195, 170, 90, 255), DOOR_BROWN)
    px(draw, dx2 - 3, (dy1 + dy2) // 2, COIN_YELLOW)

    # Red striped awning
    draw.polygon([(dx1 - 6, dy1 - 2), (dx2 + 6, dy1 - 2), (dx2 + 3, dy1 - 10), (dx1 - 3, dy1 - 10)], fill=AWNING_RED)
    for sx in range(dx1 - 4, dx2 + 6, 4):
        vline(draw, sx, dy1 - 10, dy1 - 2, AWNING_DK)
    draw.polygon([(dx1 - 6, dy1 - 2), (dx2 + 6, dy1 - 2), (dx2 + 3, dy1 - 10), (dx1 - 3, dy1 - 10)], outline=OUTLINE)

    # Skirting
    rect(draw, body_left, body_bot_y, body_right, body_bot_y + 8, (140, 115, 58, 255))
    for sx in range(body_left + 8, body_right, 10):
        vline(draw, sx, body_bot_y, body_bot_y + 8, TRIM)

    draw.rectangle([body_left, body_top_y + 12, body_right, body_bot_y + 8], outline=OUTLINE)

    # Left face
    side_depth = 20
    pts_left = [
        (body_left,              body_top_y + 12),
        (body_left - side_depth, body_top_y + 12 + side_depth // 2),
        (body_left - side_depth, body_bot_y + 8  + side_depth // 2),
        (body_left,              body_bot_y + 8),
    ]
    draw.polygon(pts_left, fill=GOLD_LEFT)
    draw.polygon(pts_left, outline=OUTLINE)

    # Front base face
    pts_front = [
        (body_left,              body_bot_y + 8),
        (body_left - side_depth, body_bot_y + 8 + side_depth // 2),
        (body_right - side_depth, body_bot_y + 8 + side_depth // 2),
        (body_right,             body_bot_y + 8),
    ]
    draw.polygon(pts_front, fill=GOLD_FRONT)
    draw.polygon(pts_front, outline=OUTLINE)

    img.save(os.path.join(SPRITES_DIR, "trailer_l2.png"))
    print("Generated: trailer_l2.png (128×160)")


# ── 4. icon_lock.png — 32×32 padlock ─────────────────────────────────────────
def generate_icon_lock():
    img = Image.new("RGBA", (32, 32), TRANSPARENT)
    draw = ImageDraw.Draw(img)

    # Body
    rect(draw, 4, 14, 27, 28, LOCK_GRAY)
    hline(draw, 5, 26, 14, LOCK_LT)
    vline(draw, 4, 15, 27, LOCK_LT)
    hline(draw, 5, 27, 28, LOCK_DK)
    vline(draw, 27, 15, 28, LOCK_DK)
    draw.rectangle([4, 14, 27, 28], outline=OUTLINE)

    # Keyhole
    draw_circle_filled(draw, 15, 20, 3, LOCK_DK)
    rect(draw, 13, 22, 17, 26, LOCK_DK)

    # Shackle (gold U)
    vline(draw, 9,  5, 14, LOCK_GOLD)
    vline(draw, 10, 5, 14, LOCK_GOLD)
    vline(draw, 21, 5, 14, LOCK_GOLD)
    vline(draw, 22, 5, 14, LOCK_GOLD)
    for pt in [(11, 4), (12, 3), (13, 3), (14, 3), (15, 3), (16, 3), (17, 3), (18, 3), (19, 4), (20, 5)]:
        draw.point(pt, fill=LOCK_GOLD)
    for pt in [(11, 3), (12, 2), (13, 2), (14, 2), (15, 2), (16, 2), (17, 2), (18, 2), (19, 3), (20, 4)]:
        draw.point(pt, fill=LOCK_GOLD)
    # Highlight
    vline(draw, 9, 5, 13, LOCK_GOLD_LT)
    # Outline shackle
    for pt in [(8, 5), (8, 6), (8, 7), (8, 8), (8, 9), (8, 10), (8, 11), (8, 12), (8, 13), (8, 14)]:
        draw.point(pt, fill=OUTLINE)
    for pt in [(23, 5), (23, 6), (23, 7), (23, 8), (23, 9), (23, 10), (23, 11), (23, 12), (23, 13), (23, 14)]:
        draw.point(pt, fill=OUTLINE)
    for pt in [(10, 1), (11, 1), (12, 1), (13, 1), (14, 1), (15, 1), (16, 1), (17, 1), (18, 1), (19, 1), (20, 2), (21, 3)]:
        draw.point(pt, fill=OUTLINE)
    draw.point((9, 2), fill=OUTLINE)

    img.save(os.path.join(SPRITES_DIR, "icon_lock.png"))
    print("Generated: icon_lock.png (32×32)")


# ── 5. icon_coin.png — 24×24 gold coin ───────────────────────────────────────
def generate_icon_coin():
    img = Image.new("RGBA", (24, 24), TRANSPARENT)
    draw = ImageDraw.Draw(img)
    cx, cy, r = 12, 12, 10
    draw_circle_filled(draw, cx, cy, r, COIN_YELLOW)
    # Shading
    for y in range(24):
        for x in range(24):
            dx = x - cx; dy = y - cy
            if dx * dx + dy * dy <= r * r:
                if dx + dy > 5:
                    draw.point((x, y), fill=COIN_ORANGE)
    # Rim
    for y in range(24):
        for x in range(24):
            dx = x - cx; dy = y - cy
            d2 = dx * dx + dy * dy
            if (r - 2) * (r - 2) < d2 <= r * r:
                draw.point((x, y), fill=COIN_ORANGE)
    # Highlight
    for y in range(24):
        for x in range(24):
            dx = x - cx; dy = y - cy
            if dx * dx + dy * dy <= (r - 3) * (r - 3) and dx + dy < -2:
                draw.point((x, y), fill=COIN_LT)
    # $ symbol
    dollar = [
        (10, 5),(11, 5),(12, 5),(13, 5),(14, 5),(9, 6),
        (9, 7),(10, 7),(11, 7),(12, 7),(13, 7),(14, 7),(15, 7),(15, 8),
        (15, 9),(14, 9),(13, 9),(12, 9),(11, 9),(10, 9),(9, 9),(9, 10),
        (9, 11),(10, 11),(11, 11),(12, 11),(13, 11),(14, 11),(15, 11),(15, 12),(14, 13),
        (12, 3),(12, 4),(12, 5),(12, 6),(12, 7),(12, 8),(12, 9),(12, 10),(12, 11),(12, 12),(12, 13),(12, 14),(12, 15),
    ]
    for (sx, sy) in dollar:
        if 0 <= sx < 24 and 0 <= sy < 24:
            draw.point((sx, sy), fill=COIN_ORANGE)
    draw_circle_outline(draw, cx, cy, r, OUTLINE)
    img.save(os.path.join(UI_DIR, "icon_coin.png"))
    print("Generated: icon_coin.png (24×24)")


# ── 6. icon_account.png — 32×32 person silhouette ────────────────────────────
def generate_icon_account():
    img = Image.new("RGBA", (32, 32), TRANSPARENT)
    draw = ImageDraw.Draw(img)
    PERSON    = (130, 130, 145, 255)
    PERSON_DK = (90,  90,  105, 255)
    PERSON_LT = (175, 175, 190, 255)
    # Head
    draw_circle_filled(draw, 16, 10, 6, PERSON)
    for y in range(32):
        for x in range(32):
            dx = x - 16; dy = y - 10
            if dx * dx + dy * dy <= 36 and dx + dy < -3:
                draw.point((x, y), fill=PERSON_LT)
    draw_circle_outline(draw, 16, 10, 6, OUTLINE)
    # Body
    body = [(7, 30), (25, 30), (23, 18), (9, 18)]
    draw.polygon(body, fill=PERSON)
    vline(draw, 9, 19, 29, PERSON_LT)
    vline(draw, 24, 19, 29, PERSON_DK)
    draw.polygon(body, outline=OUTLINE)
    # Neck
    rect(draw, 13, 16, 19, 19, PERSON)
    vline(draw, 13, 16, 18, OUTLINE)
    vline(draw, 19, 16, 18, OUTLINE)
    img.save(os.path.join(UI_DIR, "icon_account.png"))
    print("Generated: icon_account.png (32×32)")


# ── 7. icon_quest.png — 24×24 scroll ─────────────────────────────────────────
def generate_icon_quest():
    img = Image.new("RGBA", (24, 24), TRANSPARENT)
    draw = ImageDraw.Draw(img)
    SCROLL  = (220, 190, 140, 255)
    SCROLL_DK = (170, 135, 85, 255)
    SCROLL_LT = (245, 225, 185, 255)
    EDGE    = (140, 100, 55,  255)
    INK     = (60,  40,  15,  255)
    STAR_Y  = (255, 210, 30,  255)
    rect(draw, 4, 3, 19, 20, SCROLL)
    rect(draw, 3, 2, 20, 4, EDGE)
    rect(draw, 3, 19, 20, 21, EDGE)
    hline(draw, 4, 19, 2, SCROLL_LT)
    hline(draw, 4, 19, 20, SCROLL_DK)
    vline(draw, 4, 3, 20, SCROLL_LT)
    vline(draw, 19, 3, 20, SCROLL_DK)
    draw.rectangle([3, 2, 20, 21], outline=OUTLINE)
    for ly in [7, 10, 13, 16]:
        hline(draw, 6, 17, ly, INK)
    hline(draw, 6, 13, 16, INK)
    star = [(17,0),(18,2),(20,2),(19,4),(20,6),(17,5),(14,6),(15,4),(14,2),(16,2)]
    draw.polygon(star, fill=STAR_Y)
    draw.polygon(star, outline=OUTLINE)
    img.save(os.path.join(UI_DIR, "icon_quest.png"))
    print("Generated: icon_quest.png (24×24)")


# ── 8. bg_park.png — 1280×720 isometric grass field ──────────────────────────
def generate_bg_park():
    W, H = 1280, 720
    img = Image.new("RGBA", (W, H), TRANSPARENT)
    draw = ImageDraw.Draw(img)

    # Base grass fill
    gradient_rect(draw, 0, 0, W - 1, H - 1, BG_GRASS_LT, BG_GRASS_DK)

    # Grass texture variation
    rng = random.Random(99)
    for _ in range(400):
        gx = rng.randint(0, W - 20)
        gy = rng.randint(0, H - 15)
        gw = rng.randint(5, 22)
        gh = rng.randint(4, 12)
        c = BG_GRASS_DK if rng.random() > 0.5 else BG_GRASS_LT
        rect(draw, gx, gy, gx + gw, gy + gh, c)

    # Perimeter fence
    FENCE_W = 14
    OFF = 5
    # Top
    rect(draw, OFF, OFF, W - OFF, OFF + FENCE_W, FENCE_WOOD)
    hline(draw, OFF, W - OFF, OFF, FENCE_LT)
    hline(draw, OFF, W - OFF, OFF + FENCE_W, FENCE_DK)
    for fpx in range(OFF, W, 48):
        rect(draw, fpx, OFF - 3, fpx + 5, OFF + FENCE_W + 3, POST_BROWN)
        vline(draw, fpx, OFF - 3, OFF + FENCE_W + 3, FENCE_LT)
    # Bottom
    rect(draw, OFF, H - OFF - FENCE_W, W - OFF, H - OFF, FENCE_WOOD)
    hline(draw, OFF, W - OFF, H - OFF - FENCE_W, FENCE_LT)
    hline(draw, OFF, W - OFF, H - OFF, FENCE_DK)
    for fpx in range(OFF, W, 48):
        rect(draw, fpx, H - OFF - FENCE_W - 3, fpx + 5, H - OFF + 3, POST_BROWN)
    # Left
    rect(draw, OFF, OFF + FENCE_W, OFF + FENCE_W, H - OFF - FENCE_W, FENCE_WOOD)
    for fpy in range(OFF + FENCE_W, H, 48):
        rect(draw, OFF - 3, fpy, OFF + FENCE_W + 3, fpy + 5, POST_BROWN)
    # Right
    rect(draw, W - OFF - FENCE_W, OFF + FENCE_W, W - OFF, H - OFF - FENCE_W, FENCE_WOOD)
    for fpy in range(OFF + FENCE_W, H, 48):
        rect(draw, W - OFF - FENCE_W - 3, fpy, W - OFF + 3, fpy + 5, POST_BROWN)

    # Fence outlines
    draw.rectangle([OFF, OFF, W - OFF, OFF + FENCE_W], outline=OUTLINE)
    draw.rectangle([OFF, H - OFF - FENCE_W, W - OFF, H - OFF], outline=OUTLINE)

    # Water tower (top-right background)
    WT_GRAY = (120, 115, 108, 255)
    WT_DK   = (85,  80,  73,  255)
    WT_LT   = (160, 155, 148, 255)
    WT_ROOF = (95,  88,  75,  255)
    wtx, wty = 1160, 30
    for lx in [wtx + 10, wtx + 18, wtx + 28, wtx + 36]:
        vline(draw, lx, wty + 45, wty + 80, WT_DK)
    for by in [wty + 52, wty + 64, wty + 76]:
        hline(draw, wtx + 10, wtx + 36, by, WT_DK)
    rect(draw, wtx + 6, wty + 14, wtx + 44, wty + 46, WT_GRAY)
    hline(draw, wtx + 7, wtx + 43, wty + 14, WT_LT)
    vline(draw, wtx + 6, wty + 15, wty + 45, WT_LT)
    draw.polygon([(wtx + 25, wty + 4), (wtx + 5, wty + 15), (wtx + 45, wty + 15)], fill=WT_ROOF)
    draw.rectangle([wtx + 6, wty + 14, wtx + 44, wty + 46], outline=OUTLINE)

    # Palm tree (top-left)
    TRUNK   = (130, 100, 60, 255)
    TRUNK_DK= (95,  70,  35, 255)
    LEAF    = (85,  140, 55, 255)
    LEAF_DK = (55,  100, 35, 255)
    tx, ty = 60, 50
    for i in range(55):
        w = 5 if i < 35 else 4
        col_ = TRUNK if i % 3 != 0 else TRUNK_DK
        hline(draw, tx, tx + w, ty + i, col_)
    for (fx, fy) in [(-22, -28), (22, -28), (-10, -22), (12, -22), (2, -32)]:
        for s in range(18):
            fpx = tx + 3 + (fx * s) // 18
            fpy = ty + (fy * s) // 18 + s // 2
            lc = LEAF if s < 15 else LEAF_DK
            if 0 <= fpx < W and 0 <= fpy < H:
                draw.point((fpx, fpy), fill=lc)
                draw.point((fpx + 1, fpy), fill=lc)

    img.save(os.path.join(SPRITES_DIR, "bg_park.png"))
    print("Generated: bg_park.png (1280×720)")


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    os.makedirs(SPRITES_DIR, exist_ok=True)
    os.makedirs(UI_DIR, exist_ok=True)

    print("Generating Trailer Park Empire isometric sprites...")
    generate_lot_empty()
    generate_trailer_l1()
    generate_trailer_l2()
    generate_icon_lock()
    generate_icon_coin()
    generate_icon_account()
    generate_icon_quest()
    generate_bg_park()

    print("\nVerifying output files:")
    all_files = [
        (SPRITES_DIR, "lot_empty.png"),
        (SPRITES_DIR, "trailer_l1.png"),
        (SPRITES_DIR, "trailer_l2.png"),
        (SPRITES_DIR, "icon_lock.png"),
        (UI_DIR,      "icon_coin.png"),
        (UI_DIR,      "icon_account.png"),
        (UI_DIR,      "icon_quest.png"),
        (SPRITES_DIR, "bg_park.png"),
    ]
    for (d, f) in all_files:
        path = os.path.join(d, f)
        if os.path.exists(path):
            im = Image.open(path)
            size = os.path.getsize(path)
            print(f"  OK  {f:25s} {im.size[0]}×{im.size[1]}  ({size:,} bytes)")
        else:
            print(f"  MISSING: {f}")
