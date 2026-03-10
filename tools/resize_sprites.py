#!/usr/bin/env python3
"""
Trailer Park Empire — AI Sprite Post-Processor

Usage:
    python3 tools/resize_sprites.py

Drop AI-generated images into tools/generated/ with these exact filenames:
    lot_empty.png     → resized to 128×96
    trailer_l1.png    → resized to 128×96
    trailer_l2.png    → resized to 128×96
    icon_lock.png     → resized to 32×32

The script:
  1. Flood-fills background from corners (removes DALL-E checkerboard artifacts)
  2. Resizes to exact game dimensions with LANCZOS
  3. Thresholds near-transparent edge pixels to fully transparent
  4. Saves to game/assets/sprites/

After running, reimport in Godot:
    godot --path game/ --headless --import
"""

import os
import sys
from PIL import Image

SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
GENERATED    = os.path.join(SCRIPT_DIR, "generated")
SPRITES_OUT  = os.path.join(SCRIPT_DIR, "..", "game", "assets", "sprites")

# Target sizes: filename → (width, height)
TARGETS = {
    "lot_empty.png":   (128, 96),
    "trailer_l1.png":  (128, 96),
    "trailer_l2.png":  (128, 96),
    "icon_lock.png":   (32,  32),
}


def remove_background(img: Image.Image, tolerance: int = 80) -> Image.Image:
    """
    Flood-fill background removal from all four corners.

    DALL-E images with 'transparent' backgrounds often have opaque gray/white
    checkerboard pixels (alpha=255) rather than real alpha=0 transparency.
    Tolerance 80 is large enough to bridge across the two checkerboard shades
    (~153 and ~204) without eating into tile edge pixels.
    """
    img = img.convert("RGBA")
    w, h = img.size
    px = img.load()

    # Sample background color from 8×8-pixel corner patches
    r = min(8, w // 4, h // 4)
    corners = [(0, 0), (w - r, 0), (0, h - r), (w - r, h - r)]
    samples = [
        px[cx + dx, cy + dy][:3]
        for cx, cy in corners
        for dx in range(r)
        for dy in range(r)
    ]
    bg = [sum(s[i] for s in samples) // len(samples) for i in range(3)]

    # Iterative flood fill (avoids Python recursion limit)
    visited = bytearray(w * h)
    stack = [0, w - 1, (h - 1) * w, (h - 1) * w + w - 1]

    while stack:
        idx = stack.pop()
        if visited[idx]:
            continue
        x, y = idx % w, idx // w
        rv, gv, bv, _ = px[x, y]
        if max(abs(rv - bg[0]), abs(gv - bg[1]), abs(bv - bg[2])) > tolerance:
            continue
        visited[idx] = 1
        px[x, y] = (0, 0, 0, 0)
        if x > 0:     stack.append(idx - 1)
        if x < w - 1: stack.append(idx + 1)
        if y > 0:     stack.append(idx - w)
        if y < h - 1: stack.append(idx + w)

    return img


def process_sprite(filename: str, target_w: int, target_h: int) -> bool:
    src = os.path.join(GENERATED, filename)
    dst = os.path.join(SPRITES_OUT, filename)

    if not os.path.exists(src):
        print(f"  SKIP   {filename:25s} (not found in tools/generated/)")
        return False

    img = Image.open(src).convert("RGBA")
    src_w, src_h = img.size

    print(f"  Removing background from {filename} ({src_w}×{src_h})...", end=" ", flush=True)
    img = remove_background(img)
    print("done")

    if (src_w, src_h) == (target_w, target_h):
        img.save(dst)
        print(f"  COPY   {filename:25s} already {src_w}×{src_h}")
        return True

    resized = img.resize((target_w, target_h), Image.LANCZOS)

    # Threshold semi-transparent edge pixels left by LANCZOS anti-aliasing
    pixels = resized.load()
    for y in range(target_h):
        for x in range(target_w):
            rv, gv, bv, av = pixels[x, y]
            if av < 20:
                pixels[x, y] = (0, 0, 0, 0)

    resized.save(dst)
    print(f"  OK     {filename:25s} {src_w}×{src_h} → {target_w}×{target_h}")
    return True


def main():
    os.makedirs(SPRITES_OUT, exist_ok=True)

    print("Trailer Park Empire — AI Sprite Resizer")
    print(f"Source : {GENERATED}")
    print(f"Output : {os.path.normpath(SPRITES_OUT)}")
    print()

    processed = 0
    for fname, (w, h) in TARGETS.items():
        if process_sprite(fname, w, h):
            processed += 1

    print()
    if processed == 0:
        print("Nothing to do — place AI-generated images in tools/generated/")
        print("Expected filenames:", ", ".join(TARGETS.keys()))
        sys.exit(1)

    print(f"Done. {processed}/{len(TARGETS)} sprites written to game/assets/sprites/")
    print()
    print("Next step — reimport in Godot:")
    print("    godot --path game/ --headless --import")


if __name__ == "__main__":
    main()
