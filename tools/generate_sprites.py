#!/usr/bin/env python3
"""
Trailer Park Empire — Pixel Art Sprite Generator
Generates all game sprites using Pillow (no anti-aliasing, hard pixel edges).
"""

from PIL import Image, ImageDraw
import os
import math
import random

SPRITES_DIR = "/Users/chrisgastin/dev/trailer-park-empire/game/assets/sprites"
UI_DIR = "/Users/chrisgastin/dev/trailer-park-empire/game/assets/ui"

# Palette
DIRT         = (196, 168, 130, 255)   # #C4A882
DIRT_DARK    = (170, 140, 100, 255)   # cracked earth lines
DIRT_LIGHT   = (215, 190, 155, 255)   # lighter dirt patches
DRY_GRASS    = (139, 173, 106, 255)   # #8BAD6A
DRY_GRASS_DK = (100, 130, 70, 255)    # darker grass
TRAILER_CREAM = (242, 230, 197, 255)  # #F2E6C5
TRAILER_GOLD  = (255, 204, 64, 255)   # #FFCC40
TRAILER_GOLD_DK = (220, 165, 30, 255) # shading
TRAILER_TRIM  = (102, 90, 63, 255)    # #665A3F
WINDOW_BLUE   = (141, 200, 235, 255)  # #8DC8EB
WINDOW_DK     = (80, 140, 180, 255)   # window shadow
OUTLINE       = (40, 28, 15, 255)     # near-black outline
WHITE         = (255, 255, 255, 255)
BLACK         = (0, 0, 0, 255)
TRANSPARENT   = (0, 0, 0, 0)
COIN_YELLOW   = (255, 215, 0, 255)    # #FFD700
COIN_ORANGE   = (220, 170, 0, 255)    # coin shading
COIN_LIGHT    = (255, 240, 140, 255)  # coin highlight
UI_TAN        = (212, 184, 150, 255)  # #D4B896
UI_DARK       = (61, 43, 26, 255)     # #3D2B1A
LOCK_GRAY     = (80, 80, 90, 255)
LOCK_GOLD     = (200, 165, 30, 255)
CREAM_SHADOW  = (210, 195, 158, 255)  # shadow on cream trailer
CREAM_LIGHT   = (252, 246, 225, 255)  # highlight on cream trailer
RED_RUST      = (160, 80, 50, 255)    # rust/weathering
SKIRTING      = (130, 115, 80, 255)   # skirting at base
AWNING_RED    = (180, 60, 40, 255)    # door awning
AWNING_RED_DK = (130, 40, 20, 255)
FLOWER_RED    = (200, 60, 60, 255)
FLOWER_PINK   = (230, 130, 130, 255)
FLOWER_GREEN  = (80, 130, 60, 255)
ANTENNA       = (120, 110, 95, 255)
PEBBLE_DARK   = (140, 118, 90, 255)
PEBBLE_LIGHT  = (220, 200, 168, 255)
FENCE_WOOD    = (160, 130, 90, 255)
FENCE_DK      = (110, 85, 55, 255)
GRASS_BG      = (110, 150, 80, 255)
GRASS_BG_DK   = (80, 115, 55, 255)
WATER_TOWER_GRAY = (140, 135, 128, 255)
WATER_TOWER_DK   = (100, 95, 88, 255)
SKY_NONE      = (0, 0, 0, 0)  # transparent
METAL_GRAY    = (150, 150, 160, 255)
CHAINLINK     = (170, 180, 175, 255)


def px(draw, x, y, color):
    """Draw a single pixel."""
    draw.point((x, y), fill=color)


def rect(draw, x1, y1, x2, y2, color):
    """Draw a filled rectangle (inclusive)."""
    draw.rectangle([x1, y1, x2, y2], fill=color)


def hline(draw, x1, x2, y, color):
    for x in range(x1, x2 + 1):
        draw.point((x, y), fill=color)


def vline(draw, x, y1, y2, color):
    for y in range(y1, y2 + 1):
        draw.point((x, y), fill=color)


def outline_rect(draw, x1, y1, x2, y2, fill, border):
    rect(draw, x1, y1, x2, y2, fill)
    draw.rectangle([x1, y1, x2, y2], outline=border)


# ─────────────────────────────────────────────
# 1. lot_empty.png — 64×64 dirt tile
# ─────────────────────────────────────────────
def generate_lot_empty():
    img = Image.new("RGBA", (64, 64), TRANSPARENT)
    draw = ImageDraw.Draw(img)

    # Base dirt fill
    rect(draw, 0, 0, 63, 63, DIRT)

    # Subtle variation patches (lighter dirt areas)
    light_patches = [
        (8, 5, 22, 14), (38, 8, 52, 18), (10, 42, 25, 52),
        (44, 44, 58, 55), (28, 25, 40, 35),
    ]
    for (x1, y1, x2, y2) in light_patches:
        rect(draw, x1, y1, x2, y2, DIRT_LIGHT)

    # Cracked earth lines
    crack_segs = [
        # (x1, y1, x2, y2) horizontal/vertical crack segments
        [(12, 20), (18, 20), (22, 21), (26, 23)],
        [(30, 38), (36, 37), (40, 38), (44, 40)],
        [(5, 50), (10, 49), (14, 51)],
        [(48, 12), (52, 13), (56, 12)],
        [(20, 55), (24, 54), (28, 56)],
        [(42, 28), (46, 27)],
    ]
    for seg in crack_segs:
        for i in range(len(seg) - 1):
            x1, y1 = seg[i]
            x2, y2 = seg[i + 1]
            # draw line pixel by pixel
            dx = x2 - x1; dy = y2 - y1
            steps = max(abs(dx), abs(dy))
            if steps == 0:
                continue
            for s in range(steps + 1):
                cx = x1 + round(dx * s / steps)
                cy = y1 + round(dy * s / steps)
                px(draw, cx, cy, DIRT_DARK)

    # Small pebbles (2×2 or 1×1)
    pebbles = [
        (7, 30, 2), (55, 22, 2), (32, 12, 1), (18, 48, 2),
        (50, 50, 1), (38, 57, 2), (4, 10, 1), (60, 40, 1),
    ]
    for (px_, py_, sz) in pebbles:
        rect(draw, px_, py_, px_ + sz - 1, py_ + sz - 1, PEBBLE_DARK)
        # highlight top-left of pebble
        draw.point((px_, py_), fill=PEBBLE_LIGHT)

    # Tuft of dry grass — bottom-right corner
    grass_tufts = [
        (52, 54), (54, 52), (56, 55), (53, 57), (57, 53),
        (55, 56), (58, 55), (51, 56),
    ]
    for (gx, gy) in grass_tufts:
        # blade = vertical 2-3 px line
        height = 3 if (gx + gy) % 2 == 0 else 2
        for dy in range(height):
            color = DRY_GRASS if dy < height - 1 else DRY_GRASS_DK
            if 0 <= gy - dy <= 63:
                draw.point((gx, gy - dy), fill=color)

    # Faint grid border (subtle inner border)
    c = DIRT_DARK
    for i in range(64):
        draw.point((i, 0), fill=c)
        draw.point((0, i), fill=c)
        draw.point((i, 63), fill=c)
        draw.point((63, i), fill=c)

    img.save(os.path.join(SPRITES_DIR, "lot_empty.png"))
    print("Generated: lot_empty.png")


# ─────────────────────────────────────────────
# 2. trailer_l1.png — 54×54 Level 1 trailer
# ─────────────────────────────────────────────
def generate_trailer_l1():
    img = Image.new("RGBA", (54, 54), TRANSPARENT)
    draw = ImageDraw.Draw(img)

    # Skirting / base (bottom strip)
    rect(draw, 2, 45, 51, 53, SKIRTING)
    # Skirting panels — vertical lines
    for sx in range(6, 51, 8):
        vline(draw, sx, 45, 53, TRAILER_TRIM)
    # Skirting outline
    rect(draw, 2, 45, 51, 45, OUTLINE)
    rect(draw, 2, 53, 51, 53, OUTLINE)
    rect(draw, 2, 45, 2, 53, OUTLINE)
    rect(draw, 51, 45, 51, 53, OUTLINE)

    # Main body
    rect(draw, 2, 8, 51, 44, TRAILER_CREAM)

    # Top-left highlight (baked lighting)
    for i in range(3):
        vline(draw, 2 + i, 8, 44, CREAM_LIGHT if i == 0 else TRAILER_CREAM)
    hline(draw, 2, 51, 8, CREAM_LIGHT)
    hline(draw, 2, 51, 9, CREAM_LIGHT)

    # Right + bottom shadow
    for i in range(2):
        vline(draw, 50 - i, 9, 44, CREAM_SHADOW)
    hline(draw, 3, 51, 43, CREAM_SHADOW)
    hline(draw, 3, 51, 44, CREAM_SHADOW)

    # Weathering / grime patches
    grime = [(15, 35, 20, 38), (35, 28, 38, 32), (8, 22, 10, 26)]
    for (x1, y1, x2, y2) in grime:
        rect(draw, x1, y1, x2, y2, CREAM_SHADOW)

    # Chipped paint spots
    chip_spots = [(22, 30), (42, 38), (12, 40), (38, 20)]
    for (cx, cy) in chip_spots:
        draw.point((cx, cy), fill=DIRT_DARK)
        draw.point((cx + 1, cy), fill=CREAM_SHADOW)

    # Roof
    rect(draw, 1, 4, 52, 8, TRAILER_TRIM)
    rect(draw, 2, 3, 51, 4, TRAILER_TRIM)
    # Roof highlight
    hline(draw, 2, 51, 3, (130, 115, 80, 255))

    # TV Antenna
    vline(draw, 38, 0, 3, ANTENNA)  # vertical mast
    hline(draw, 35, 41, 1, ANTENNA)  # horizontal cross
    draw.point((35, 1), fill=ANTENNA)
    draw.point((41, 1), fill=ANTENNA)
    draw.point((38, 0), fill=ANTENNA)

    # Window left
    rect(draw, 6, 14, 18, 26, WINDOW_BLUE)
    rect(draw, 6, 14, 18, 26, None)
    # Window frame
    rect(draw, 5, 13, 19, 27, TRAILER_TRIM)
    rect(draw, 6, 14, 18, 26, WINDOW_BLUE)
    # Window cross dividers
    vline(draw, 12, 14, 26, TRAILER_TRIM)
    hline(draw, 6, 18, 20, TRAILER_TRIM)
    # Window reflection/glint
    draw.point((7, 15), fill=WHITE)
    draw.point((8, 15), fill=WHITE)
    draw.point((7, 16), fill=WHITE)
    # Window shadow bottom-right
    rect(draw, 14, 22, 18, 26, WINDOW_DK)

    # Window right
    rect(draw, 33, 13, 47, 27, TRAILER_TRIM)
    rect(draw, 34, 14, 46, 26, WINDOW_BLUE)
    vline(draw, 40, 14, 26, TRAILER_TRIM)
    hline(draw, 34, 46, 20, TRAILER_TRIM)
    draw.point((35, 15), fill=WHITE)
    draw.point((36, 15), fill=WHITE)
    draw.point((35, 16), fill=WHITE)
    rect(draw, 42, 22, 46, 26, WINDOW_DK)

    # Door (center-right of body)
    rect(draw, 22, 30, 32, 44, TRAILER_TRIM)
    rect(draw, 23, 31, 31, 44, (180, 160, 120, 255))  # door fill
    # Door knob
    draw.point((30, 38), fill=COIN_YELLOW)
    draw.point((30, 39), fill=COIN_ORANGE)
    # Door shadow top
    hline(draw, 23, 31, 31, CREAM_SHADOW)

    # Small awning over door (simple L1 version — just a narrow visor)
    rect(draw, 20, 28, 34, 30, TRAILER_TRIM)
    hline(draw, 20, 34, 28, ANTENNA)

    # Body outline
    draw.rectangle([2, 8, 51, 44], outline=OUTLINE)
    draw.rectangle([1, 4, 52, 8], outline=OUTLINE)

    # Rust streaks (weathering)
    rust_lines = [(9, 28, 9, 33), (48, 15, 48, 20)]
    for (x1, y1, x2, y2) in rust_lines:
        for y in range(y1, y2 + 1):
            draw.point((x1, y), fill=RED_RUST)

    img.save(os.path.join(SPRITES_DIR, "trailer_l1.png"))
    print("Generated: trailer_l1.png")


# ─────────────────────────────────────────────
# 3. trailer_l2.png — 54×54 Level 2 trailer
# ─────────────────────────────────────────────
def generate_trailer_l2():
    img = Image.new("RGBA", (54, 54), TRANSPARENT)
    draw = ImageDraw.Draw(img)

    # Nicer skirting
    rect(draw, 2, 45, 51, 53, (160, 140, 90, 255))
    for sx in range(6, 51, 6):
        vline(draw, sx, 45, 53, (130, 110, 65, 255))
    rect(draw, 2, 45, 51, 45, OUTLINE)
    rect(draw, 2, 53, 51, 53, OUTLINE)
    rect(draw, 2, 45, 2, 53, OUTLINE)
    rect(draw, 51, 45, 51, 53, OUTLINE)

    # Main body — gold
    rect(draw, 2, 8, 51, 44, TRAILER_GOLD)

    # Highlight top-left
    GOLD_LIGHT = (255, 230, 120, 255)
    for i in range(3):
        vline(draw, 2 + i, 8, 44, GOLD_LIGHT if i == 0 else TRAILER_GOLD)
    hline(draw, 2, 51, 8, GOLD_LIGHT)
    hline(draw, 2, 51, 9, GOLD_LIGHT)

    # Right + bottom shadow
    for i in range(2):
        vline(draw, 50 - i, 9, 44, TRAILER_GOLD_DK)
    hline(draw, 3, 51, 43, TRAILER_GOLD_DK)
    hline(draw, 3, 51, 44, TRAILER_GOLD_DK)

    # Roof
    rect(draw, 1, 4, 52, 8, TRAILER_TRIM)
    rect(draw, 2, 3, 51, 4, TRAILER_TRIM)
    hline(draw, 2, 51, 3, (130, 115, 80, 255))

    # TV Antenna (still there, but cleaner)
    vline(draw, 38, 0, 3, ANTENNA)
    hline(draw, 35, 41, 1, ANTENNA)

    # Window left — nicer frame with white trim
    rect(draw, 5, 13, 19, 27, OUTLINE)
    rect(draw, 6, 14, 18, 26, WINDOW_BLUE)
    rect(draw, 6, 14, 18, 26, None)
    # White window trim
    draw.rectangle([5, 13, 19, 27], outline=WHITE)
    draw.rectangle([6, 14, 18, 26], fill=WINDOW_BLUE)
    vline(draw, 12, 14, 26, (200, 220, 240, 255))
    hline(draw, 6, 18, 20, (200, 220, 240, 255))
    draw.point((7, 15), fill=WHITE)
    draw.point((8, 15), fill=WHITE)
    draw.point((7, 16), fill=WHITE)
    draw.point((8, 16), fill=(230, 245, 255, 255))
    rect(draw, 14, 22, 18, 26, WINDOW_DK)

    # Window right
    draw.rectangle([33, 13, 47, 27], outline=WHITE)
    draw.rectangle([34, 14, 46, 26], fill=WINDOW_BLUE)
    vline(draw, 40, 14, 26, (200, 220, 240, 255))
    hline(draw, 34, 46, 20, (200, 220, 240, 255))
    draw.point((35, 15), fill=WHITE)
    draw.point((36, 15), fill=WHITE)
    draw.point((35, 16), fill=WHITE)
    rect(draw, 42, 22, 46, 26, WINDOW_DK)

    # Flower box under left window (L2 exclusive)
    rect(draw, 5, 28, 19, 31, TRAILER_TRIM)
    rect(draw, 6, 28, 18, 30, (120, 80, 40, 255))  # dirt in box
    # Flowers: alternating red and pink dots
    flower_colors = [FLOWER_RED, FLOWER_PINK, FLOWER_RED, FLOWER_PINK, FLOWER_RED, FLOWER_PINK]
    for i, fc in enumerate(flower_colors):
        fx = 7 + i * 2
        draw.point((fx, 28), fill=fc)
        draw.point((fx, 27), fill=(80, 160, 60, 255))  # stem leaf above
    # Green leaves in box
    for lx in range(6, 19, 3):
        draw.point((lx, 29), fill=FLOWER_GREEN)

    # Door
    rect(draw, 22, 30, 32, 44, OUTLINE)
    rect(draw, 23, 31, 31, 44, (200, 175, 90, 255))  # nicer door, gold-ish
    draw.point((30, 38), fill=COIN_YELLOW)
    draw.point((30, 39), fill=COIN_ORANGE)

    # Awning over door (L2 — proper red striped awning)
    rect(draw, 19, 26, 35, 30, AWNING_RED)
    # Stripes
    for sx in range(20, 35, 3):
        vline(draw, sx, 26, 30, AWNING_RED_DK)
    # Awning valance (bottom edge scallop — simplified)
    for sx in range(19, 36, 2):
        draw.point((sx, 30), fill=AWNING_RED_DK)
    rect(draw, 19, 26, 35, 26, OUTLINE)
    rect(draw, 19, 26, 19, 30, OUTLINE)
    rect(draw, 35, 26, 35, 30, OUTLINE)

    # Body outline
    draw.rectangle([2, 8, 51, 44], outline=OUTLINE)
    draw.rectangle([1, 4, 52, 8], outline=OUTLINE)

    img.save(os.path.join(SPRITES_DIR, "trailer_l2.png"))
    print("Generated: trailer_l2.png")


# ─────────────────────────────────────────────
# 4. icon_lock.png — 24×24 padlock
# ─────────────────────────────────────────────
def generate_icon_lock():
    img = Image.new("RGBA", (24, 24), TRANSPARENT)
    draw = ImageDraw.Draw(img)

    # Lock body — dark gray metal rectangle
    rect(draw, 3, 11, 20, 21, LOCK_GRAY)
    # Body highlight top-left
    hline(draw, 4, 19, 11, (180, 180, 190, 255))
    vline(draw, 3, 12, 20, (180, 180, 190, 255))
    # Body shadow bottom-right
    hline(draw, 4, 20, 21, (60, 60, 68, 255))
    vline(draw, 20, 12, 21, (60, 60, 68, 255))
    # Body outline
    draw.rectangle([3, 11, 20, 21], outline=OUTLINE)

    # Keyhole
    rect(draw, 10, 14, 13, 19, (40, 40, 45, 255))
    draw.point((11, 14), fill=(40, 40, 45, 255))
    draw.point((12, 14), fill=(40, 40, 45, 255))
    # Keyhole circle top
    for pt in [(10, 13), (11, 13), (12, 13), (13, 13),
               (9, 14), (14, 14), (9, 15), (14, 15),
               (10, 16), (11, 16), (12, 16), (13, 16)]:
        draw.point(pt, fill=(40, 40, 45, 255))

    # Gold shackle (U-shape)
    SHACKLE = LOCK_GOLD
    SHACKLE_DK = (160, 130, 20, 255)
    SHACKLE_LT = (240, 210, 80, 255)
    # Left vertical
    vline(draw, 7, 4, 11, SHACKLE)
    # Right vertical
    vline(draw, 16, 4, 11, SHACKLE)
    # Top arc (3 px wide arc)
    for pt in [(8, 3), (9, 2), (10, 2), (11, 2), (12, 2), (13, 2), (14, 3), (15, 4)]:
        draw.point(pt, fill=SHACKLE)
    draw.point((7, 5), fill=SHACKLE)
    draw.point((16, 5), fill=SHACKLE)
    # Shackle width — make it 2px thick
    vline(draw, 8, 4, 11, SHACKLE)
    vline(draw, 15, 4, 11, SHACKLE)
    for pt in [(9, 2), (10, 2), (11, 2), (12, 2), (13, 2), (14, 2)]:
        draw.point(pt, fill=SHACKLE)
    for pt in [(9, 3), (10, 3), (11, 3), (12, 3), (13, 3), (14, 3)]:
        draw.point(pt, fill=SHACKLE)
    # Shackle highlight
    vline(draw, 7, 4, 10, SHACKLE_LT)
    draw.point((8, 3), fill=SHACKLE_LT)
    # Shackle shadow
    vline(draw, 16, 4, 10, SHACKLE_DK)
    # Outline shackle
    for pt in [(6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (6, 9), (6, 10), (6, 11)]:
        draw.point(pt, fill=OUTLINE)
    for pt in [(17, 4), (17, 5), (17, 6), (17, 7), (17, 8), (17, 9), (17, 10), (17, 11)]:
        draw.point(pt, fill=OUTLINE)
    for pt in [(8, 1), (9, 1), (10, 1), (11, 1), (12, 1), (13, 1), (14, 1), (15, 1)]:
        draw.point(pt, fill=OUTLINE)
    draw.point((7, 2), fill=OUTLINE)
    draw.point((16, 2), fill=OUTLINE)

    img.save(os.path.join(SPRITES_DIR, "icon_lock.png"))
    print("Generated: icon_lock.png")


# ─────────────────────────────────────────────
# 5. icon_coin.png — 24×24 gold coin
# ─────────────────────────────────────────────
def generate_icon_coin():
    img = Image.new("RGBA", (24, 24), TRANSPARENT)
    draw = ImageDraw.Draw(img)

    # Coin circle (radius 10, centered at 12,12)
    cx, cy, r = 11, 12, 10
    # Draw filled circle
    for y in range(24):
        for x in range(24):
            dx = x - cx; dy = y - cy
            if dx * dx + dy * dy <= r * r:
                draw.point((x, y), fill=COIN_YELLOW)

    # Shading — darker on bottom-right
    for y in range(24):
        for x in range(24):
            dx = x - cx; dy = y - cy
            d2 = dx * dx + dy * dy
            if d2 <= r * r:
                # Bottom-right quadrant
                if dx + dy > 6:
                    draw.point((x, y), fill=COIN_ORANGE)

    # Rim — slightly darker ring
    for y in range(24):
        for x in range(24):
            dx = x - cx; dy = y - cy
            d2 = dx * dx + dy * dy
            if (r - 2) * (r - 2) < d2 <= r * r:
                draw.point((x, y), fill=COIN_ORANGE)

    # Highlight top-left arc
    HL = COIN_LIGHT
    for y in range(24):
        for x in range(24):
            dx = x - cx; dy = y - cy
            d2 = dx * dx + dy * dy
            if d2 <= (r - 3) * (r - 3) and dx + dy < -2:
                draw.point((x, y), fill=HL)

    # "$" symbol in center — pixel art
    # Draw a simple "$" using pixel lines (7×9 area centered at ~11,12)
    dollar = [
        # top arc
        (9, 5), (10, 5), (11, 5), (12, 5), (13, 5),
        (8, 6),
        (8, 7), (9, 7), (10, 7), (11, 7), (12, 7), (13, 7),
        (13, 8),
        (13, 9), (12, 9), (11, 9), (10, 9), (9, 9), (8, 9),
        (8, 10),
        (8, 11), (9, 11), (10, 11), (11, 11), (12, 11), (13, 11),
        (13, 12),
        (12, 13),
        # vertical bar through center
        (11, 3), (11, 4), (11, 5), (11, 6), (11, 7), (11, 8),
        (11, 9), (11, 10), (11, 11), (11, 12), (11, 13), (11, 14), (11, 15),
    ]
    for (sx, sy) in dollar:
        if 0 <= sx < 24 and 0 <= sy < 24:
            draw.point((sx, sy), fill=COIN_ORANGE)

    # Outline circle
    for y in range(24):
        for x in range(24):
            dx = x - cx; dy = y - cy
            d2 = dx * dx + dy * dy
            if r * r < d2 <= (r + 1.5) * (r + 1.5):
                draw.point((x, y), fill=OUTLINE)

    img.save(os.path.join(UI_DIR, "icon_coin.png"))
    print("Generated: icon_coin.png")


# ─────────────────────────────────────────────
# 6. icon_account.png — 32×32 profile silhouette
# ─────────────────────────────────────────────
def generate_icon_account():
    img = Image.new("RGBA", (32, 32), TRANSPARENT)
    draw = ImageDraw.Draw(img)

    PERSON = (130, 130, 145, 255)    # gray (anonymous state)
    PERSON_DK = (90, 90, 105, 255)
    PERSON_LT = (175, 175, 190, 255)

    # Head — circle, centered at (16, 10), radius 6
    hcx, hcy, hr = 16, 10, 6
    for y in range(32):
        for x in range(32):
            dx = x - hcx; dy = y - hcy
            if dx * dx + dy * dy <= hr * hr:
                draw.point((x, y), fill=PERSON)

    # Head highlight
    for y in range(32):
        for x in range(32):
            dx = x - hcx; dy = y - hcy
            if dx * dx + dy * dy <= hr * hr and dx + dy < -3:
                draw.point((x, y), fill=PERSON_LT)

    # Head outline
    for y in range(32):
        for x in range(32):
            dx = x - hcx; dy = y - hcy
            d2 = dx * dx + dy * dy
            if hr * hr < d2 <= (hr + 1.5) * (hr + 1.5):
                draw.point((x, y), fill=OUTLINE)

    # Body — trapezoid (shoulders wide, narrows down)
    # Shoulders: y=18 to y=30
    body_pts = [
        (7, 30), (25, 30), (23, 18), (9, 18)
    ]
    draw.polygon(body_pts, fill=PERSON)
    # Body highlight left edge
    vline(draw, 9, 19, 29, PERSON_LT)
    hline(draw, 10, 22, 19, PERSON_LT)
    # Body shadow right edge
    vline(draw, 24, 19, 29, PERSON_DK)
    # Body outline
    draw.polygon(body_pts, outline=OUTLINE)

    # Neck
    rect(draw, 13, 16, 19, 19, PERSON)
    rect(draw, 13, 16, 19, 19, None)
    vline(draw, 13, 16, 18, OUTLINE)
    vline(draw, 19, 16, 18, OUTLINE)

    img.save(os.path.join(UI_DIR, "icon_account.png"))
    print("Generated: icon_account.png")


# ─────────────────────────────────────────────
# 7. icon_quest.png — 24×24 scroll/quest icon
# ─────────────────────────────────────────────
def generate_icon_quest():
    img = Image.new("RGBA", (24, 24), TRANSPARENT)
    draw = ImageDraw.Draw(img)

    SCROLL_TAN = (220, 190, 140, 255)
    SCROLL_DK  = (170, 135, 85, 255)
    SCROLL_LT  = (245, 225, 185, 255)
    SCROLL_EDGE= (140, 100, 55, 255)
    INK        = (60, 40, 15, 255)
    STAR_Y     = (255, 210, 30, 255)
    STAR_DK    = (200, 160, 0, 255)

    # Scroll body
    rect(draw, 4, 3, 19, 20, SCROLL_TAN)
    # Top/bottom rolled edges
    rect(draw, 3, 2, 20, 4, SCROLL_EDGE)
    rect(draw, 3, 19, 20, 21, SCROLL_EDGE)
    # Rolled edge highlights
    hline(draw, 4, 19, 2, SCROLL_LT)
    hline(draw, 4, 19, 20, SCROLL_DK)
    # Left/right edge shadow
    vline(draw, 4, 3, 20, SCROLL_LT)
    vline(draw, 19, 3, 20, SCROLL_DK)
    # Body outline
    draw.rectangle([3, 2, 20, 21], outline=OUTLINE)
    # Inner highlight
    hline(draw, 5, 18, 4, SCROLL_LT)

    # Text lines on scroll (pixel art "lines of text")
    line_ys = [7, 10, 13, 16]
    for ly in line_ys:
        hline(draw, 6, 17, ly, INK)
    # Last line shorter (looks like real text)
    hline(draw, 6, 13, 16, INK)

    # Star badge — top-right corner (quest star)
    # 5-pointed pixel star, small, at (17, 3)
    star_pts = [
        (17, 0), (18, 2), (20, 2), (19, 4), (20, 6),
        (17, 5), (14, 6), (15, 4), (14, 2), (16, 2),
    ]
    draw.polygon(star_pts, fill=STAR_Y)
    draw.polygon(star_pts, outline=OUTLINE)
    # Star highlight
    draw.point((17, 1), fill=(255, 240, 100, 255))
    draw.point((17, 2), fill=(255, 240, 100, 255))

    img.save(os.path.join(UI_DIR, "icon_quest.png"))
    print("Generated: icon_quest.png")


# ─────────────────────────────────────────────
# 8. bg_park.png — 640×512 park background
# ─────────────────────────────────────────────
def generate_bg_park():
    img = Image.new("RGBA", (640, 512), TRANSPARENT)
    draw = ImageDraw.Draw(img)

    # Ground fill — muted dirt/scrubby grass
    BG_DIRT  = (180, 155, 110, 255)   # muted dirt, doesn't compete
    BG_GRASS = (120, 155, 88, 255)    # muted grass
    BG_GRASS_DK = (95, 125, 65, 255)

    # Fill base ground
    rect(draw, 0, 0, 639, 511, BG_DIRT)

    # Grass patches scattered across ground
    import random as rng
    rng.seed(42)
    for _ in range(180):
        gx = rng.randint(0, 635)
        gy = rng.randint(0, 507)
        gw = rng.randint(4, 18)
        gh = rng.randint(3, 10)
        alpha = rng.randint(60, 130)
        gc = (BG_GRASS[0], BG_GRASS[1], BG_GRASS[2], 255) if rng.random() > 0.4 else BG_GRASS_DK
        rect(draw, gx, gy, gx + gw, gy + gh, gc)

    # Dirt variation patches
    for _ in range(80):
        px_ = rng.randint(0, 620)
        py_ = rng.randint(0, 495)
        pw = rng.randint(8, 30)
        ph = rng.randint(5, 20)
        rect(draw, px_, py_, px_ + pw, py_ + ph, (195, 170, 125, 255))

    # Perimeter fence — weathered wood planks
    PLANK     = (155, 120, 75, 255)
    PLANK_DK  = (115, 85, 45, 255)
    PLANK_LT  = (190, 155, 105, 255)
    POST      = (100, 72, 38, 255)
    POST_LT   = (140, 105, 65, 255)
    FENCE_W = 12   # fence thickness (px)
    FENCE_OFF = 4  # offset from edge

    # Top fence
    rect(draw, FENCE_OFF, FENCE_OFF, 639 - FENCE_OFF, FENCE_OFF + FENCE_W, PLANK)
    # Bottom planks
    hline(draw, FENCE_OFF, 639 - FENCE_OFF, FENCE_OFF, PLANK_LT)
    hline(draw, FENCE_OFF, 639 - FENCE_OFF, FENCE_OFF + FENCE_W, PLANK_DK)
    # Horizontal rail lines
    hline(draw, FENCE_OFF, 639 - FENCE_OFF, FENCE_OFF + 4, PLANK_DK)
    hline(draw, FENCE_OFF, 639 - FENCE_OFF, FENCE_OFF + 8, PLANK_DK)
    # Vertical fence posts every 40px
    for fpx in range(FENCE_OFF, 640, 40):
        rect(draw, fpx, FENCE_OFF - 2, fpx + 4, FENCE_OFF + FENCE_W + 2, POST)
        vline(draw, fpx, FENCE_OFF - 2, FENCE_OFF + FENCE_W + 2, POST_LT)

    # Bottom fence
    rect(draw, FENCE_OFF, 511 - FENCE_OFF - FENCE_W, 639 - FENCE_OFF, 511 - FENCE_OFF, PLANK)
    hline(draw, FENCE_OFF, 639 - FENCE_OFF, 511 - FENCE_OFF - FENCE_W, PLANK_LT)
    hline(draw, FENCE_OFF, 639 - FENCE_OFF, 511 - FENCE_OFF, PLANK_DK)
    hline(draw, FENCE_OFF, 639 - FENCE_OFF, 511 - FENCE_OFF - FENCE_W + 4, PLANK_DK)
    hline(draw, FENCE_OFF, 639 - FENCE_OFF, 511 - FENCE_OFF - FENCE_W + 8, PLANK_DK)
    for fpx in range(FENCE_OFF, 640, 40):
        rect(draw, fpx, 511 - FENCE_OFF - FENCE_W - 2, fpx + 4, 511 - FENCE_OFF + 2, POST)
        vline(draw, fpx, 511 - FENCE_OFF - FENCE_W - 2, 511 - FENCE_OFF + 2, POST_LT)

    # Left fence
    rect(draw, FENCE_OFF, FENCE_OFF + FENCE_W, FENCE_OFF + FENCE_W, 511 - FENCE_OFF - FENCE_W, PLANK)
    for fpy in range(FENCE_OFF + FENCE_W, 512, 40):
        rect(draw, FENCE_OFF - 2, fpy, FENCE_OFF + FENCE_W + 2, fpy + 4, POST)
        hline(draw, FENCE_OFF - 2, FENCE_OFF + FENCE_W + 2, fpy, POST_LT)
    vline(draw, FENCE_OFF, FENCE_OFF + FENCE_W, 511 - FENCE_OFF - FENCE_W, PLANK_LT)
    vline(draw, FENCE_OFF + FENCE_W, FENCE_OFF + FENCE_W, 511 - FENCE_OFF - FENCE_W, PLANK_DK)

    # Right fence
    rect(draw, 639 - FENCE_OFF - FENCE_W, FENCE_OFF + FENCE_W, 639 - FENCE_OFF, 511 - FENCE_OFF - FENCE_W, PLANK)
    for fpy in range(FENCE_OFF + FENCE_W, 512, 40):
        rect(draw, 639 - FENCE_OFF - FENCE_W - 2, fpy, 639 - FENCE_OFF + 2, fpy + 4, POST)
        hline(draw, 639 - FENCE_OFF - FENCE_W - 2, 639 - FENCE_OFF + 2, fpy, POST_LT)
    vline(draw, 639 - FENCE_OFF - FENCE_W, FENCE_OFF + FENCE_W, 511 - FENCE_OFF - FENCE_W, PLANK_LT)
    vline(draw, 639 - FENCE_OFF, FENCE_OFF + FENCE_W, 511 - FENCE_OFF - FENCE_W, PLANK_DK)

    # Background element: WATER TOWER — top-right outside fence area
    # Position: far top-right background (muted, low detail)
    WT_GRAY   = (120, 115, 108, 255)
    WT_DK     = (85, 80, 73, 255)
    WT_LT     = (160, 155, 148, 255)
    WT_ROOF   = (95, 88, 75, 255)
    wtx, wty = 570, 20   # top-left of water tower bounding box
    # Legs (4 thin posts)
    for lx in [wtx + 8, wtx + 14, wtx + 22, wtx + 28]:
        vline(draw, lx, wty + 35, wty + 65, WT_DK)
    # Cross braces
    for by in [wty + 40, wty + 50, wty + 60]:
        hline(draw, wtx + 8, wtx + 28, by, WT_DK)
    # Tank — rounded rectangle
    rect(draw, wtx + 4, wty + 10, wtx + 36, wty + 36, WT_GRAY)
    rect(draw, wtx + 2, wty + 16, wtx + 38, wty + 32, WT_GRAY)
    # Tank highlight
    hline(draw, wtx + 5, wtx + 35, wty + 10, WT_LT)
    vline(draw, wtx + 4, wty + 11, wty + 35, WT_LT)
    # Tank shadow
    hline(draw, wtx + 5, wtx + 35, wty + 36, WT_DK)
    vline(draw, wtx + 36, wty + 11, wty + 35, WT_DK)
    # Cone roof
    roof_pts = [(wtx + 20, wty + 3), (wtx + 3, wty + 11), (wtx + 37, wty + 11)]
    draw.polygon(roof_pts, fill=WT_ROOF)
    draw.polygon(roof_pts, outline=(60, 55, 45, 255))
    # Outline tank
    draw.rectangle([wtx + 4, wty + 10, wtx + 36, wty + 36], outline=(60, 55, 45, 255))

    # Background element: DEAD PALM TREE — top-left area
    TRUNK = (130, 100, 60, 255)
    TRUNK_DK = (95, 70, 35, 255)
    LEAF = (95, 130, 65, 255)
    LEAF_DK = (65, 95, 40, 255)
    tx, ty = 55, 25   # base of trunk (top of image area)
    # Trunk — tapers slightly
    for i in range(45):
        w = 4 if i < 30 else 3
        off = i // 20
        hline(draw, tx + off, tx + off + w, ty + i, TRUNK if i % 3 != 0 else TRUNK_DK)
    # Palm fronds (dead/sparse — 4 drooping fronds)
    frond_angles = [(-20, -30), (20, -30), (-10, -25), (12, -26)]
    for (fx, fy) in frond_angles:
        # Draw frond as series of points drooping outward
        steps = 15
        for s in range(steps):
            fpx = tx + 2 + (fx * s) // steps
            fpy = ty + (fy * s) // steps + s // 2  # drooping
            lc = LEAF if s < steps - 3 else LEAF_DK
            if 0 <= fpx < 640 and 0 <= fpy < 512:
                draw.point((fpx, fpy), fill=lc)
                if s < steps - 2:
                    draw.point((fpx + 1, fpy), fill=lc)

    # Distant road/highway hint — very subtle horizontal strip far bottom
    # (muted gray strip near bottom outside fence)
    road_y = 500
    rect(draw, 0, road_y, 639, 511, (150, 145, 138, 255))
    hline(draw, 0, 639, road_y, (130, 125, 118, 255))
    # Road dashes (center line)
    for rx in range(20, 620, 40):
        hline(draw, rx, rx + 20, road_y + 5, (200, 195, 185, 255))

    # Subtle vignette darkening on outer edges (top-down style)
    VIGNETTE = (30, 20, 10, 60)  # very subtle dark overlay
    for edge_w in range(8):
        alpha = 50 - edge_w * 5
        if alpha <= 0:
            break
        vc = (20, 14, 6, alpha)
        hline(draw, 0, 639, edge_w, vc)
        hline(draw, 0, 639, 511 - edge_w, vc)
        vline(draw, edge_w, 0, 511, vc)
        vline(draw, 639 - edge_w, 0, 511, vc)

    # Fence outlines (on top)
    draw.rectangle([FENCE_OFF, FENCE_OFF, 639 - FENCE_OFF, FENCE_OFF + FENCE_W], outline=OUTLINE)
    draw.rectangle([FENCE_OFF, 511 - FENCE_OFF - FENCE_W, 639 - FENCE_OFF, 511 - FENCE_OFF], outline=OUTLINE)

    img.save(os.path.join(SPRITES_DIR, "bg_park.png"))
    print("Generated: bg_park.png")


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────
if __name__ == "__main__":
    os.makedirs(SPRITES_DIR, exist_ok=True)
    os.makedirs(UI_DIR, exist_ok=True)

    print("Generating Trailer Park Empire sprites...")
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
        (UI_DIR, "icon_coin.png"),
        (UI_DIR, "icon_account.png"),
        (UI_DIR, "icon_quest.png"),
        (SPRITES_DIR, "bg_park.png"),
    ]
    for (d, f) in all_files:
        path = os.path.join(d, f)
        if os.path.exists(path):
            im = Image.open(path)
            size = os.path.getsize(path)
            print(f"  OK  {f:25s} {im.size[0]}x{im.size[1]}  ({size:,} bytes)")
        else:
            print(f"  MISSING: {f}")
