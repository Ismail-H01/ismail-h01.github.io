#!/usr/bin/env python3
"""Build assets/img/og-image.png (1200x630), the preview shown when the site link is shared.

Usage:  python tools/build_og.py      (edit TITLE / LINE below first)
"""
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent.parent / "assets" / "img" / "og-image.png"
NAME = ("Ismail", "Hussain")
TITLE = "Graduate Electrical Engineer"
LINE = "First Class BEng (Hons)  |  MIET"
URL = "ismail-h01.github.io"
FONT_DIR = Path("/usr/share/fonts/opentype/inter")


def font(name, size):
    for p in (FONT_DIR / name, Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")):
        if p.exists():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


def build():
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), "#0a1120")
    d = ImageDraw.Draw(img)
    random.seed(7)
    for _ in range(16):  # faint PCB-style traces with chamfered corners
        x, y = random.randrange(560, 1240, 28), random.randrange(-20, 650, 28)
        pts, horiz = [(x, y)], random.random() < .5
        for _ in range(4):
            step = 28 * random.randint(3, 8) * random.choice((-1, 1))
            x, y = (x + step, y) if horiz else (x, y + step)
            pts.append((x, y)); horiz = not horiz
        d.line(pts, fill="#1b2a47", width=3, joint="curve")
        for px, py in (pts[0], pts[-1]):
            d.ellipse((px - 6, py - 6, px + 6, py + 6), outline="#22355a", width=3)
    bold, semi, reg = font("Inter-ExtraBold.otf", 118), font("Inter-SemiBold.otf", 44), font("Inter-Medium.otf", 30)
    d.text((80, 120), NAME[0], font=bold, fill="#e8eef9")
    # gradient surname
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).text((80, 245), NAME[1], font=bold, fill=255)
    grad = Image.new("RGB", (W, H))
    gd = ImageDraw.Draw(grad)
    for i in range(W):
        t = min(i / 700, 1)
        c = tuple(int(a + (b - a) * t) for a, b in ((0x35, 0x5b), (0xd0, 0x9d), (0xc0, 0xff)))
        gd.line([(i, 0), (i, H)], fill=c)
    img.paste(grad, (0, 0), mask)
    d.text((84, 400), TITLE, font=semi, fill="#e8eef9")
    d.text((84, 462), LINE, font=reg, fill="#35d0c0")
    d.rectangle((84, 540, 132, 544), fill="#35d0c0")
    d.text((148, 524), URL, font=reg, fill="#9fb0cc")
    img.save(OUT, optimize=True)
    print("wrote", OUT)


if __name__ == "__main__":
    build()
