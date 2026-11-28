#!/usr/bin/env python3
"""Build the 1200x630 link-preview images: og-image.png (engineering site) and og-sales.png (sales page).

Usage:  python tools/build_og.py      (edit the VARIANTS below first)
"""
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

IMG = Path(__file__).resolve().parent.parent / "assets" / "img"
NAME = ("Ismail", "Hussain")
VARIANTS = [
    # file, title, line, url, background, trace colour, gradient from, gradient to, accent
    ("og-image.png", "Graduate Electrical Engineer", "First Class BEng (Hons)  |  MIET", "ismail-h01.github.io",
     "#0a1120", "#1b2a47", (0x35, 0xd0, 0xc0), (0x5b, 0x9d, 0xff), "#35d0c0"),
    ("og-sales.png", "Engineer moving into sales", "First Class BEng (Hons)  |  MIET", "ismail-h01.github.io/sales",
     "#0b0f1a", "#242b3d", (0xf4, 0xb7, 0x40), (0xff, 0x8a, 0x5c), "#f4b740"),
]
FONT_DIR = Path("/usr/share/fonts/opentype/inter")


def font(name, size):
    for p in (FONT_DIR / name, Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")):
        if p.exists():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


def build(fname, TITLE, LINE, URL, bg, trace, g0, g1, accent):
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(img)
    random.seed(7)
    for _ in range(16):  # faint PCB-style traces with chamfered corners
        x, y = random.randrange(560, 1240, 28), random.randrange(-20, 650, 28)
        pts, horiz = [(x, y)], random.random() < .5
        for _ in range(4):
            step = 28 * random.randint(3, 8) * random.choice((-1, 1))
            x, y = (x + step, y) if horiz else (x, y + step)
            pts.append((x, y)); horiz = not horiz
        d.line(pts, fill=trace, width=3, joint="curve")
        for px, py in (pts[0], pts[-1]):
            d.ellipse((px - 6, py - 6, px + 6, py + 6), outline=trace, width=3)
    bold, semi, reg = font("Inter-ExtraBold.otf", 118), font("Inter-SemiBold.otf", 44), font("Inter-Medium.otf", 30)
    d.text((80, 120), NAME[0], font=bold, fill="#e8eef9")
    # gradient surname
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).text((80, 245), NAME[1], font=bold, fill=255)
    grad = Image.new("RGB", (W, H))
    gd = ImageDraw.Draw(grad)
    for i in range(W):
        t = min(i / 700, 1)
        c = tuple(int(a + (b - a) * t) for a, b in zip(g0, g1))
        gd.line([(i, 0), (i, H)], fill=c)
    img.paste(grad, (0, 0), mask)
    d.text((84, 400), TITLE, font=semi, fill="#e8eef9")
    d.text((84, 462), LINE, font=reg, fill=accent)
    d.rectangle((84, 540, 132, 544), fill=accent)
    d.text((148, 524), URL, font=reg, fill="#9fb0cc")
    img.save(IMG / fname, optimize=True)
    print("wrote", IMG / fname)


if __name__ == "__main__":
    for v in VARIANTS:
        build(*v)
