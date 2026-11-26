#!/usr/bin/env python3
"""news-image-20261126: "The World in One Day" -- Thursday 26 November 2026.

Draws a newspaper front page summing up 26 November 2026's world news
entirely in code (Pillow, standard shapes + DejaVu fonts). No network,
no timestamps, no randomness: running it twice writes byte-identical PNG.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (247, 243, 232)
INK = (26, 26, 26)
NAVY = (20, 33, 61)
RED = (179, 38, 30)
BLUE = (31, 78, 121)
GOLD = (201, 162, 39)
GREY = (90, 90, 90)
LIGHT = (255, 255, 255)
PANEL_BG = (255, 255, 255)
GREEN = (34, 139, 34)
SAFFRON = (255, 153, 51)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def f_serif_b(s):
    return font("DejaVuSerif-Bold.ttf", s)


def f_sans_b(s):
    return font("DejaVuSans-Bold.ttf", s)


def f_sans(s):
    return font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.25)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def draw_ship(draw, x, y, w, h):
    """Container ship on waves, with tariff '%' badges above it."""
    hull_top = y + h * 0.58
    # containers: two neat rows on the deck
    cols = [RED, BLUE, GOLD, GREEN, NAVY]
    cw = w * 0.17
    for i, c in enumerate(cols):
        cx = x + w * 0.03 + i * cw
        ch = h * 0.26 if i % 2 == 0 else h * 0.18
        draw.rectangle([cx, hull_top - ch, cx + cw - 5, hull_top - 2],
                       fill=c, outline=INK, width=2)
        draw.line([cx, hull_top - ch / 2, cx + cw - 5, hull_top - ch / 2],
                  fill=INK, width=1)
    # bridge tower at the stern
    bx = x + w * 0.86
    draw.rectangle([bx, hull_top - h * 0.46, bx + w * 0.11, hull_top - 2],
                   fill=LIGHT, outline=INK, width=2)
    draw.rectangle([bx + 2, hull_top - h * 0.55, bx + w * 0.11 - 2,
                    hull_top - h * 0.46], fill=RED, outline=INK, width=2)
    # hull
    draw.polygon([(x, hull_top), (x + w, hull_top),
                  (x + w * 0.94, hull_top + h * 0.18),
                  (x + w * 0.06, hull_top + h * 0.18)], fill=NAVY,
                 outline=INK)
    draw.rectangle([x, hull_top, x + w, hull_top + 4], fill=RED)
    # waves
    for i in range(2):
        wy = hull_top + h * 0.24 + i * 14
        draw.arc([x + 6, wy, x + w * 0.32, wy + 18], 180, 360, fill=BLUE,
                 width=3)
        draw.arc([x + w * 0.38, wy, x + w * 0.68, wy + 18], 180, 360,
                 fill=BLUE, width=3)
    # '%' badges floating above the cargo
    for bx2, by2, txt in ((x + w * 0.06, y + 2, "20%"),
                          (x + w * 0.55, y + 10, "15%")):
        draw.ellipse([bx2, by2, bx2 + 62, by2 + 62], fill=RED, outline=INK,
                     width=3)
        draw.text((bx2 + 31, by2 + 31), txt, font=f_sans_b(23), fill=LIGHT,
                  anchor="mm")


def draw_oil(draw, x, y, w, h):
    """Oil barrel with flame (left) and a rising price line (right)."""
    # rising chart, right half only
    pts = [(x + w * 0.50, y + h * 0.72), (x + w * 0.62, y + h * 0.66),
           (x + w * 0.74, y + h * 0.70), (x + w * 0.86, y + h * 0.46),
           (x + w * 0.97, y + h * 0.26)]
    draw.line(pts, fill=RED, width=5, joint="curve")
    draw.polygon([(pts[-1][0] - 15, pts[-1][1] + 2), (pts[-1][0] + 2,
                  pts[-1][1] + 15), (pts[-1][0] + 2, pts[-1][1] - 15)],
                 fill=RED)
    draw.text((x + w * 0.74, y + h * 0.90), "$94", font=f_sans_b(26),
              fill=RED, anchor="mm")
    # barrel, left half
    bx, by, bw, bh = x + w * 0.06, y + h * 0.28, w * 0.34, h * 0.66
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=10,
                           fill=(60, 60, 60), outline=INK, width=3)
    draw.rectangle([bx, by + bh * 0.26, bx + bw, by + bh * 0.34],
                   fill=INK)
    draw.rectangle([bx, by + bh * 0.62, bx + bw, by + bh * 0.70],
                   fill=INK)
    draw.text((bx + bw / 2, by + bh / 2), "OIL", font=f_sans_b(26),
              fill=LIGHT, anchor="mm")
    # flame above the barrel
    fx, fy = bx + bw / 2, by - 4
    draw.polygon([(fx - 20, fy), (fx, fy - 42), (fx + 20, fy),
                  (fx + 7, fy - 7), (fx, fy - 14), (fx - 7, fy - 7)],
                 fill=(255, 140, 0), outline=(200, 60, 0))
    draw.polygon([(fx - 9, fy - 2), (fx, fy - 24), (fx + 9, fy - 2)],
                 fill=(255, 220, 0))


def draw_markets(draw, x, y, w, h):
    """Falling chart (left) over a microchip (right)."""
    # faint grid first
    for gy in (0.30, 0.55, 0.80):
        draw.line([x + 4, y + h * gy, x + w * 0.56, y + h * gy],
                  fill=(205, 205, 205), width=1)
    # falling chart, left half only
    pts = [(x + 6, y + h * 0.22), (x + w * 0.16, y + h * 0.28),
           (x + w * 0.28, y + h * 0.24), (x + w * 0.40, y + h * 0.58),
           (x + w * 0.54, y + h * 0.86)]
    draw.line(pts, fill=RED, width=5, joint="curve")
    draw.polygon([(pts[-1][0] - 15, pts[-1][1] - 2), (pts[-1][0] + 2,
                  pts[-1][1] - 15), (pts[-1][0] + 2, pts[-1][1] + 15)],
                 fill=RED)
    # chip, right half
    cx, cy, cw, chh = x + w * 0.62, y + h * 0.22, w * 0.32, h * 0.60
    for i in range(3):
        px = cx + 10 + i * (cw - 20) / 2
        draw.line([px, cy - 14, px, cy], fill=INK, width=4)
        draw.line([px, cy + chh, px, cy + chh + 14], fill=INK, width=4)
    draw.rectangle([cx, cy, cx + cw, cy + chh], fill=NAVY, outline=INK,
                   width=3)
    draw.rectangle([cx + cw * 0.22, cy + chh * 0.22, cx + cw * 0.78,
                    cy + chh * 0.78], fill=LIGHT, outline=INK, width=2)
    draw.text((cx + cw / 2, cy + chh / 2), "AI", font=f_sans_b(28),
              fill=NAVY, anchor="mm")


def draw_chess(draw, x, y, w, h):
    """Chessboard with a king and a queen."""
    s = min(w, h) / 4.4
    ox, oy = x + (w - s * 4) / 2, y + (h - s * 4) / 2
    for r in range(4):
        for c in range(4):
            col = LIGHT if (r + c) % 2 == 0 else NAVY
            draw.rectangle([ox + c * s, oy + r * s, ox + (c + 1) * s,
                            oy + (r + 1) * s], fill=col, outline=INK,
                           width=1)
    for (r, c, label, fill) in ((3, 1, "K", GOLD), (1, 2, "Q", RED)):
        cx, cy = ox + (c + 0.5) * s, oy + (r + 0.5) * s
        draw.ellipse([cx - s * 0.34, cy - s * 0.34, cx + s * 0.34,
                      cy + s * 0.34], fill=fill, outline=INK, width=2)
        draw.text((cx, cy), label, font=f_sans_b(int(s * 0.52)), fill=INK,
                  anchor="mm")


def draw_book(draw, x, y, w, h):
    """Open book under a saffron-white-green ribbon with a chakra wheel."""
    draw.rectangle([x, y + h * 0.08, x + w, y + h * 0.20], fill=SAFFRON)
    draw.rectangle([x, y + h * 0.20, x + w, y + h * 0.32], fill=LIGHT,
                   outline=INK, width=1)
    draw.rectangle([x, y + h * 0.32, x + w, y + h * 0.44], fill=GREEN)
    cx, cy, r = x + w / 2, y + h * 0.26, h * 0.05
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY, width=3)
    for k in range(12):
        a = math.pi * 2 * k / 12
        draw.line([cx, cy, cx + r * math.cos(a), cy + r * math.sin(a)],
                  fill=NAVY, width=2)
    # open book
    bx, by, bw, bh = x + w * 0.10, y + h * 0.52, w * 0.80, h * 0.42
    draw.polygon([(bx, by), (bx + bw / 2, by + bh * 0.18),
                  (bx + bw / 2, by + bh), (bx, by + bh * 0.82)],
                 fill=LIGHT, outline=INK, width=3)
    draw.polygon([(bx + bw, by), (bx + bw / 2, by + bh * 0.18),
                  (bx + bw / 2, by + bh), (bx + bw, by + bh * 0.82)],
                 fill=(235, 230, 215), outline=INK, width=3)
    for i in range(3):
        ly = by + bh * 0.30 + i * bh * 0.18
        draw.line([bx + 8, ly, bx + bw / 2 - 8, ly + bh * 0.06],
                  fill=GREY, width=2)
        draw.line([bx + bw / 2 + 8, ly + bh * 0.06, bx + bw - 8, ly],
                  fill=GREY, width=2)


def panel_top(draw, x, y, w, h, kicker, headline, caption, art):
    """Panel with the illustration on top, text below."""
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=PANEL_BG,
                           outline=INK, width=2)
    inner = 14
    art(draw, x + inner, y + inner, w - 2 * inner, h * 0.40)
    ty = y + inner + h * 0.40 + 8
    draw.text((x + inner, ty), kicker, font=f_sans_b(16), fill=RED)
    ty += 23
    lines = wrap(draw, headline, f_sans_b(27), w - 2 * inner)
    ty = text_block(draw, x + inner, ty, lines, f_sans_b(27), INK, 31)
    cap = wrap(draw, caption, f_sans(19), w - 2 * inner)
    text_block(draw, x + inner, ty + 4, cap, f_sans(19), GREY, 23)


def panel_side(draw, x, y, w, h, kicker, headline, caption, art):
    """Panel with the illustration on the left, text on the right."""
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=PANEL_BG,
                           outline=INK, width=2)
    inner = 14
    aw = int(w * 0.36)
    art(draw, x + inner, y + inner, aw, h - 2 * inner)
    tx = x + inner + aw + 12
    tw = w - inner - aw - 12 - inner
    ty = y + 18
    draw.text((tx, ty), kicker, font=f_sans_b(16), fill=RED)
    ty += 23
    lines = wrap(draw, headline, f_sans_b(27), tw)
    ty = text_block(draw, tx, ty, lines, f_sans_b(27), INK, 31)
    cap = wrap(draw, caption, f_sans(19), tw)
    text_block(draw, tx, ty + 4, cap, f_sans(19), GREY, 23)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.text((W / 2, 26), "THE WORLD IN ONE DAY", font=f_serif_b(30),
           fill=GOLD, anchor="mt")
    d.text((W / 2, 62), "THURSDAY  26  NOVEMBER  2026",
           font=f_sans_b(52), fill=LIGHT, anchor="mt")
    d.rectangle([0, 148, W, 154], fill=RED)

    # ---- lead story: US tariffs ----
    lx, ly, lw, lh = 24, 168, 976, 324
    d.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=10,
                        fill=PANEL_BG, outline=INK, width=2)
    d.text((lx + 20, ly + 14), "LEAD  •  TRADE WAR", font=f_sans_b(18),
           fill=RED)
    draw_ship(d, lx + 20, ly + 48, 400, 250)
    tx = lx + 450
    head = wrap(d, "US unveils new tariffs on 14 partners",
                f_sans_b(42), lw - 470)
    ty = text_block(d, tx, ly + 44, head, f_sans_b(42), INK, 48)
    sub = wrap(d, "China faces up to 20%, the EU 15% — Asia wakes to "
               "the plan as Taiwan confirms its rate and markets reel.",
               f_sans(24), lw - 470)
    text_block(d, tx, ty + 8, sub, f_sans(24), GREY, 30)

    # ---- row 2: oil + markets ----
    panel_top(d, 24, 506, 476, 228, "ENERGY  •  MIDDLE EAST",
              "Oil jumps: Brent tops $94",
              "Gulf attacks stoke supply fears; crude climbs 3.6% in a day.",
              draw_oil)
    panel_top(d, 524, 506, 476, 228, "MARKETS  •  ASIA",
              "Asian tech shares slide again",
              "Chip stocks tumble for a second day as doubts over the AI "
              "boom spread.", draw_markets)

    # ---- row 3: chess + India (side art, roomier) ----
    panel_side(d, 24, 748, 476, 228, "SPORT  •  GENEVA",
               "World Chess: Game 3 today",
               "Gukesh and Sindarov level at 1–1 after two draws; Game 3 "
               "starts at 15:00 CET.", draw_chess)
    panel_side(d, 524, 748, 476, 228, "INDIA  •  26 NOVEMBER",
               "India marks Constitution Day",
               "The nation celebrates Samvidhan Divas, the day its "
               "Constitution was adopted.", draw_book)

    # ---- footer ticker ----
    d.rectangle([0, 990, W, H], fill=NAVY)
    d.text((W / 2, 1007),
           "ALSO TODAY:  Asia Cup Rising Stars semi-finals in Doha  •  "
           "Brent $94.65  •  ASX tech –2.3%",
           font=f_sans_b(16), fill=LIGHT, anchor="mm")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    img.save(os.path.join(out_dir, "entry.png"), "PNG")


if __name__ == "__main__":
    main()
