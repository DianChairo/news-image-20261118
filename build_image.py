#!/usr/bin/env python3
"""Build entry.png: a 1024x1024 editorial front-page infographic summing up
the world news of Wednesday, 18 November 2026. Pure Pillow drawing, no
photographic material, no network, fully deterministic. Run: python3 build_image.py"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 28

PAPER = (250, 247, 240)   # warm newsprint
INK = (17, 17, 17)
NAVY = (27, 58, 92)
RED = (176, 42, 30)
GREY = (90, 86, 80)
WHITE = (255, 255, 255)
PANEL = (255, 255, 255)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
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


def draw_globe(d, x, y, s, c):
    # globe: circle, meridians, equator
    d.ellipse([x, y, x + s, y + s], outline=c, width=4)
    d.ellipse([x + 0.28 * s, y, x + 0.72 * s, y + s], outline=c, width=3)
    d.line([(x, y + 0.5 * s), (x + s, y + 0.5 * s)], fill=c, width=3)
    d.arc([x, y + 0.18 * s, x + s, y + 0.82 * s], 200, 340, fill=c, width=3)
    d.arc([x, y + 0.18 * s, x + s, y + 0.82 * s], 20, 160, fill=c, width=3)


def draw_bridge(d, x, y, s, c):
    # suspension bridge with a broken span
    d.line([(x, y + 0.62 * s), (x + s, y + 0.62 * s)], fill=c, width=4)
    d.line([(x + 0.22 * s, y + 0.15 * s), (x + 0.22 * s, y + 0.62 * s)], fill=c, width=4)
    d.line([(x + 0.78 * s, y + 0.15 * s), (x + 0.78 * s, y + 0.62 * s)], fill=c, width=4)
    d.line([(x + 0.22 * s, y + 0.15 * s), (x + 0.5 * s, y + 0.62 * s)], fill=c, width=2)
    d.line([(x + 0.78 * s, y + 0.15 * s), (x + 0.5 * s, y + 0.62 * s)], fill=c, width=2)
    d.line([(x + 0.44 * s, y + 0.62 * s), (x + 0.44 * s, y + 0.78 * s)], fill=c, width=3)
    d.line([(x + 0.56 * s, y + 0.62 * s), (x + 0.56 * s, y + 0.78 * s)], fill=c, width=3)
    d.line([(x, y + 0.85 * s), (x + s, y + 0.85 * s)], fill=c, width=3)


def draw_drone(d, x, y, s, c):
    # quadcopter drone: body + four rotor arms
    d.rectangle([x + 0.34 * s, y + 0.40 * s, x + 0.66 * s, y + 0.60 * s], fill=c)
    for cx, cy in ((0.16, 0.20), (0.84, 0.20), (0.16, 0.80), (0.84, 0.80)):
        d.line([(x + 0.5 * s, y + 0.5 * s), (x + cx * s, y + cy * s)], fill=c, width=3)
        d.ellipse([x + (cx - 0.14) * s, y + (cy - 0.06) * s,
                   x + (cx + 0.14) * s, y + (cy + 0.06) * s], outline=c, width=3)
    d.line([(x + 0.5 * s, y + 0.60 * s), (x + 0.5 * s, y + 0.78 * s)], fill=c, width=3)


def draw_handshake(d, x, y, s, c):
    # two clasped hands: two angled blocks meeting in the middle
    d.polygon([(x + 0.05 * s, y + 0.30 * s), (x + 0.42 * s, y + 0.30 * s),
               (x + 0.55 * s, y + 0.55 * s), (x + 0.18 * s, y + 0.55 * s)], fill=c)
    d.polygon([(x + 0.95 * s, y + 0.45 * s), (x + 0.58 * s, y + 0.45 * s),
               (x + 0.45 * s, y + 0.70 * s), (x + 0.82 * s, y + 0.70 * s)], fill=c)
    d.rectangle([x + 0.18 * s, y + 0.55 * s, x + 0.82 * s, y + 0.78 * s],
                outline=c, width=3)
    for i in range(3):
        fx = 0.30 + 0.18 * i
        d.line([(x + fx * s, y + 0.55 * s), (x + fx * s, y + 0.78 * s)], fill=c, width=2)


def draw_gavel(d, x, y, s, c):
    # gavel: head + handle, angled
    d.rectangle([x + 0.10 * s, y + 0.10 * s, x + 0.62 * s, y + 0.38 * s], fill=c)
    d.line([(x + 0.36 * s, y + 0.38 * s), (x + 0.85 * s, y + 0.85 * s)], fill=c, width=6)
    d.line([(x + 0.05 * s, y + 0.92 * s), (x + 0.95 * s, y + 0.92 * s)], fill=c, width=4)


def draw_cricket(d, x, y, s, c):
    # cricket bat + ball
    d.polygon([(x + 0.30 * s, y + 0.02 * s), (x + 0.52 * s, y + 0.02 * s),
               (x + 0.52 * s, y + 0.55 * s), (x + 0.30 * s, y + 0.55 * s)], fill=c)
    d.polygon([(x + 0.34 * s, y + 0.55 * s), (x + 0.48 * s, y + 0.55 * s),
               (x + 0.62 * s, y + 0.92 * s), (x + 0.20 * s, y + 0.92 * s)], fill=c)
    d.ellipse([x + 0.68 * s, y + 0.62 * s, x + 0.98 * s, y + 0.92 * s],
              outline=c, width=4)
    d.arc([x + 0.68 * s, y + 0.62 * s, x + 0.98 * s, y + 0.92 * s], 300, 60,
          fill=c, width=2)


STORIES = [
    {
        "tag": "ASIA-PACIFIC",
        "color": (27, 94, 122),
        "icon": draw_globe,
        "headline": "Trump lands in Manila for Quad talks",
        "summary": "The U.S. president arrives for Quad talks ahead of a China visit and a meeting with Xi and Putin.",
    },
    {
        "tag": "EUROPE  ·  WAR",
        "color": (140, 43, 43),
        "icon": draw_bridge,
        "headline": "Kerch Bridge struck for a second day",
        "summary": "Ukraine hit the Crimean bridge again, as Russia pounded bridges in Kyiv in reply.",
    },
    {
        "tag": "MIDDLE EAST",
        "color": (138, 90, 0),
        "icon": draw_drone,
        "headline": "Iran hits U.S. radar in Bahrain",
        "summary": "Drones hit a U.S. radar in Bahrain; Kuwait also reported drone attacks, and Iran said a tanker with 2 million barrels of oil sank in Hormuz.",
    },
    {
        "tag": "TRADE  ·  APEC",
        "color": (31, 107, 58),
        "icon": draw_handshake,
        "headline": "Canada and China extend trade deals",
        "summary": "Xi meets Carney as the two countries extend trade deals ahead of the APEC summit.",
    },
    {
        "tag": "UNITED KINGDOM",
        "color": (46, 58, 89),
        "icon": draw_gavel,
        "headline": "Britain sanctions Israeli settlement firms",
        "summary": "London blacklists settlement-linked companies in a push to protect the two-state solution.",
    },
    {
        "tag": "SPORT",
        "color": (91, 58, 140),
        "icon": draw_cricket,
        "headline": "Dhoni retires from the IPL",
        "summary": "MS Dhoni calls time on his playing career and becomes Chennai Super Kings mentor.",
    },
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    title_f = font(SERIF_B, 46)
    d.text((W // 2, 34), "THE WORLD IN ONE PICTURE", font=title_f,
           fill=NAVY, anchor="ma")
    d.line([(MARGIN, 96), (W - MARGIN, 96)], fill=INK, width=2)

    # Date band
    d.rectangle([MARGIN, 108, W - MARGIN, 164], fill=NAVY)
    date_f = font(SANS_B, 36)
    d.text((W // 2, 136), "WEDNESDAY, 18 NOVEMBER 2026", font=date_f,
           fill=WHITE, anchor="mm")

    sub_f = font(SERIF, 21)
    d.text((W // 2, 188), "Six stories that defined the day — from Manila to the Gulf",
           font=sub_f, fill=GREY, anchor="ma")

    # ---- Story grid: 2 cols x 3 rows ----
    gap = 16
    pw = (W - 2 * MARGIN - gap) // 2          # 476
    ph = 236
    gx, gy = MARGIN, 214
    tag_f = font(SANS_B, 15)
    head_f = font(SANS_B, 26)
    body_f = font(SANS, 19)

    for i, st in enumerate(STORIES):
        col, row = i % 2, i // 2
        x0 = gx + col * (pw + gap)
        y0 = gy + row * (ph + gap)
        x1, y1 = x0 + pw, y0 + ph

        d.rectangle([x0, y0, x1, y1], fill=PANEL, outline=INK, width=2)
        d.rectangle([x0, y0, x1, y0 + 6], fill=st["color"])

        # tag chip
        tw = d.textlength(st["tag"], font=tag_f)
        chip_w = int(tw) + 22
        d.rounded_rectangle([x0 + 16, y0 + 18, x0 + 16 + chip_w, y0 + 46],
                            radius=6, fill=st["color"])
        d.text((x0 + 27, y0 + 32), st["tag"], font=tag_f, fill=WHITE, anchor="lm")

        # icon, top right
        st["icon"](d, x1 - 78, y0 + 16, 56, st["color"])

        # headline, up to 2 lines (fail loudly rather than truncate text)
        inner = pw - 32
        lines = wrap(d, st["headline"], head_f, inner)
        assert len(lines) <= 2, f"headline too long: {st['headline']!r} -> {lines}"
        hy = y0 + 62
        for ln in lines:
            d.text((x0 + 16, hy), ln, font=head_f, fill=INK)
            hy += 32

        # summary, up to 3 lines (fail loudly rather than truncate text)
        slines = wrap(d, st["summary"], body_f, inner)
        assert len(slines) <= 3, f"summary too long: {st['summary']!r} -> {slines}"
        sy = y0 + 62 + len(lines) * 32 + 8
        for ln in slines:
            d.text((x0 + 16, sy), ln, font=body_f, fill=(51, 51, 51))
            sy += 25

    # ---- Footer: sources ----
    foot_f = font(SANS, 15)
    d.text((W // 2, 990),
           "Sources: BBC · Reuters · Al Jazeera · The Guardian · AP — all reported 18 November 2026",
           font=foot_f, fill=GREY, anchor="ms")

    img.save("entry.png", format="PNG", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
