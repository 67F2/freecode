#!/usr/bin/env python3
"""Render assets/avatar.txt -> assets/avatar.png (1024x1024 CRT-style).

Requires Pillow: pip install pillow
Usage: python3 tools/render_avatar.py
"""

import pathlib

from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "avatar.txt"
OUT = ROOT / "assets" / "avatar.png"
SIZE = 1024
BG = (5, 8, 5)
BORDER = (18, 60, 32)

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "/usr/share/fonts/TTF/DejaVuSansMono.ttf",
    "/usr/share/fonts/dejavu/DejaVuSansMono.ttf",
    "/Library/Fonts/Menlo.ttc",
    "C:/Windows/Fonts/consola.ttf",
]

RAMP = " .:-=+*#%@"


def load_font(px):
    for path in FONT_CANDIDATES:
        try:
            return ImageFont.truetype(path, px)
        except OSError:
            continue
    return ImageFont.load_default()


def fit_font(lines, max_w, max_h):
    for px in range(40, 8, -1):
        font = load_font(px)
        widest = max(font.getbbox(line)[2] - font.getbbox(line)[0] for line in lines)
        height = len(lines) * px
        if widest <= max_w and height <= max_h:
            return font, px
    return load_font(10), 10


def main():
    lines = SRC.read_text().rstrip("\n").splitlines()
    img = Image.new("RGB", (SIZE, SIZE), BG)
    d = ImageDraw.Draw(img)

    d.rectangle([12, 12, SIZE - 13, SIZE - 13], outline=BORDER, width=3)

    font, px = fit_font(lines, SIZE - 120, SIZE - 140)
    line_h = px
    widths = [d.textlength(line, font=font) for line in lines]
    block_w = max(widths)
    x0 = (SIZE - block_w) // 2
    y0 = (SIZE - len(lines) * line_h) // 2

    for i, line in enumerate(lines):
        y = y0 + i * line_h
        for j, ch in enumerate(line):
            if ch == " ":
                continue
            idx = RAMP.find(ch)
            L = 1.0 if idx == -1 else 1.0 - idx / (len(RAMP) - 1)
            color = (
                int(6 + 50 * L),
                int(70 + 185 * L),
                int(24 + 66 * L),
            )
            x = x0 + d.textlength(line[:j], font=font)
            d.text((x, y), ch, font=font, fill=color)

    OUT.write_bytes(b"")
    img.save(OUT)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
