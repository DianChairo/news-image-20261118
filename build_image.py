#!/usr/bin/env python3
"""Render a 1024x1024 editorial front page summing up Wednesday 18 November 2026.

Pure Pillow shapes and text -- no photos, no network, no randomness, no
timestamps. Running this script always produces the same bytes.
"""

import textwrap
from dataclasses import dataclass

from PIL import Image, ImageDraw, ImageFont

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"

# Palette: deep teal + amber + cream.
TEAL_DARK = (9, 58, 62)
TEAL = (14, 92, 96)
TEAL_LIGHT = (31, 128, 133)
AMBER = (233, 163, 44)
AMBER_SOFT = (246, 201, 107)
CREAM = (250, 244, 228)
CREAM_DIM = (238, 229, 206)
INK = (24, 34, 33)
WHITE = (255, 255, 255)
TEAL_PALE = (206, 230, 228)

WIDTH = 1024
HEIGHT = 1024


@dataclass(frozen=True)
class Story:
    kicker: str
    headline: str
    body: str
    accent: tuple


STORIES = [
    Story(
        kicker="DIPLOMACY  /  ASIA",
        headline="Trump lands in Manila for Quad talks ahead of China visit",
        body="The US president arrives in the Philippines for Quad talks, "
        "then travels on to China to meet Xi and Putin.",
        accent=AMBER,
    ),
    Story(
        kicker="UKRAINE  /  WAR",
        headline="Ukraine hits Kerch Bridge for a second day",
        body="Kyiv strikes the Crimean bridge again as Russia pounds "
        "bridges in the Ukrainian capital.",
        accent=AMBER,
    ),
    Story(
        kicker="GULF  /  SECURITY",
        headline="Iran hits US radar in Bahrain as drones reported over Kuwait",
        body="Tehran says a tanker carrying two million barrels of oil sank "
        "in the Strait of Hormuz.",
        accent=TEAL_LIGHT,
    ),
    Story(
        kicker="TRADE  /  APEC",
        headline="Canada and China extend trade deals",
        body="Xi meets Carney ahead of the APEC summit as Ottawa and Beijing "
        "agree to deepen trade ties.",
        accent=TEAL_LIGHT,
    ),
    Story(
        kicker="BRITAIN  /  MIDDLE EAST",
        headline="Britain sanctions Israeli settlement firms",
        body="London moves against settlement-linked companies in a push to "
        "protect the two-state solution.",
        accent=AMBER,
    ),
    Story(
        kicker="CRICKET  /  INDIA",
        headline="Dhoni retires from the IPL, becomes CSK mentor",
        body="MS Dhoni ends his IPL playing career and takes up a mentor "
        "role at Chennai Super Kings.",
        accent=AMBER_SOFT,
    ),
]


def load(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(FONT_DIR + name, size)


def wrap_text(draw, text, font, max_width):
    """Greedy word wrap using the real rendered width of each candidate line."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(draw, x, y, text, font, fill, max_width, leading):
    lines = wrap_text(draw, text, font, max_width)
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def draw_kicker(draw, x, y, story, font):
    draw.text((x, y), story.kicker, font=font, fill=story.accent)
    draw.rectangle([x, y + 22, x + 44, y + 26], fill=story.accent)


def draw_lead(canvas, story, box):
    """Full-width lead panel: big headline, amber rule, two-column body."""
    x0, y0, x1, y1 = box
    canvas.rectangle(box, fill=TEAL)
    canvas.rectangle([x0, y0, x1, y0 + 4], fill=AMBER)
    draw_kicker(canvas, x0 + 28, y0 + 24, story, load(19, bold=True))
    y = draw_wrapped(
        canvas, x0 + 28, y0 + 62, story.headline,
        load(44, bold=True), WHITE, x1 - x0 - 56, 52,
    )
    canvas.rectangle([x0 + 28, y + 8, x0 + 72, y + 12], fill=AMBER)
    draw_wrapped(
        canvas, x0 + 28, y + 22, story.body,
        load(21), CREAM, x1 - x0 - 56, 26,
    )
    canvas.text(
        (x1 - 28, y0 + 24), "01", font=load(26, bold=True),
        fill=AMBER_SOFT, anchor="ra",
    )


def draw_cell(canvas, story, box, number):
    """One of the four middle grid cells on a cream card."""
    x0, y0, x1, y1 = box
    canvas.rounded_rectangle(box, radius=10, fill=CREAM, outline=TEAL_PALE, width=2)
    canvas.rectangle([x0, y0, x0 + 6, y1], fill=story.accent)
    draw_kicker(canvas, x0 + 24, y0 + 18, story, load(15, bold=True))
    y = draw_wrapped(
        canvas, x0 + 24, y0 + 50, story.headline,
        load(25, bold=True), INK, x1 - x0 - 48, 31,
    )
    draw_wrapped(
        canvas, x0 + 24, y + 6, story.body,
        load(17), (58, 74, 72), x1 - x0 - 48, 23,
    )
    canvas.text(
        (x1 - 44, y1 - 36), number, font=load(20, bold=True), fill=TEAL_LIGHT,
    )


def draw_strip(canvas, story, box):
    """Full-width bottom strip: amber band with the final story."""
    x0, y0, x1, y1 = box
    canvas.rectangle(box, fill=AMBER)
    canvas.rectangle([x0, y0, x1, y0 + 4], fill=TEAL_DARK)
    canvas.text(
        (x0 + 28, y0 + 16), story.kicker, font=load(16, bold=True), fill=TEAL_DARK,
    )
    canvas.text(
        (x0 + 28, y0 + 42), story.headline, font=load(27, bold=True), fill=INK,
    )
    draw_wrapped(
        canvas, x0 + 28, y0 + 84, story.body,
        load(17), (58, 44, 8), x1 - x0 - 150, 22,
    )
    canvas.ellipse([x1 - 100, y0 + 26, x1 - 36, y0 + 90], outline=TEAL_DARK, width=3)
    canvas.text((x1 - 78, y0 + 42), "06", font=load(24, bold=True), fill=TEAL_DARK)


def render():
    img = Image.new("RGB", (WIDTH, HEIGHT), CREAM)
    draw = ImageDraw.Draw(img)

    # Masthead.
    draw.rectangle([0, 0, WIDTH, 118], fill=TEAL_DARK)
    draw.rectangle([0, 118, WIDTH, 122], fill=AMBER)
    draw.text((36, 18), "THE WORLD IN ONE PAGE", font=load(46, bold=True), fill=WHITE)
    draw.text(
        (36, 76), "WEDNESDAY 18 NOVEMBER 2026  |  SIX STORIES, ONE DAY",
        font=load(18, bold=True), fill=AMBER_SOFT,
    )
    draw.text((WIDTH - 36, 76), "No. 322", font=load(18), fill=CREAM_DIM, anchor="ra")

    # Lead story, full width.
    draw_lead(draw, STORIES[0], (24, 140, WIDTH - 24, 392))

    # Stories 2-5 in a two-column grid.
    grid_top = 410
    cell_w = (WIDTH - 24 * 2 - 16) // 2
    cell_h = 218
    for idx, story in enumerate(STORIES[1:5]):
        col = idx % 2
        row = idx // 2
        x0 = 24 + col * (cell_w + 16)
        y0 = grid_top + row * (cell_h + 16)
        draw_cell(draw, story, (x0, y0, x0 + cell_w, y0 + cell_h), "0%d" % (idx + 2))

    # Story 6 as a full-width bottom strip.
    draw_strip(draw, STORIES[5], (24, 878, WIDTH - 24, 1000))

    # Footer.
    draw.text(
        (36, 1006 - 4), "Compiled from verified reports  |  One image, six stories",
        font=load(13), fill=(110, 122, 120),
    )
    return img


def main():
    image = render()
    image.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
