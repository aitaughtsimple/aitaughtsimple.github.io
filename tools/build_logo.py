"""Build the AI Taught Simple logo files (direction A: chat bubble + AI spark).

Usage: python -I build_logo.py <variable-font.ttf> <output-dir>
Text is converted to outlines so the files render the same everywhere.
"""
import os
import sys

import uharfbuzz as hb
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

FONT, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)

INK, GREEN, SUN, WHITE = "#1F2925", "#1D5C4B", "#F6C453", "#FFFFFF"
LOC = {"wght": 800, "opsz": 36, "wdth": 100}
TEXT, SPLIT = "AI Taught Simple", len("AI Taught ")

inst = instantiateVariableFont(TTFont(FONT), LOC)
UPM = inst["head"].unitsPerEm
GS = inst.getGlyphSet()
ORDER = inst.getGlyphOrder()
CMAP = inst.getBestCmap()

hbfont = hb.Font(hb.Face(hb.Blob.from_file_path(FONT)))
hbfont.set_variations(LOC)
TRACK = -0.02 * UPM


def glyph_bounds(ch):
    bp = BoundsPen(GS)
    GS[CMAP[ord(ch)]].draw(bp)
    return bp.bounds  # xMin, yMin, xMax, yMax


CAP = glyph_bounds("H")[3]
DESC = -glyph_bounds("g")[1]


def text_paths(size, x0, baseline):
    """Return ([ink path data], [accent path data], width) for TEXT at size."""
    buf = hb.Buffer()
    buf.add_str(TEXT)
    buf.guess_segment_properties()
    hb.shape(hbfont, buf, {"kern": True, "liga": True})
    s = size / UPM
    x = 0.0
    first, second = [], []
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        pen = SVGPathPen(GS, ntos=lambda v: ("%.2f" % v).rstrip("0").rstrip("."))
        tp = TransformPen(pen, (s, 0, 0, -s, x0 + (x + pos.x_offset) * s, baseline - pos.y_offset * s))
        GS[ORDER[info.codepoint]].draw(tp)
        d = pen.getCommands()
        if d:
            (second if info.cluster >= SPLIT else first).append(d)
        x += pos.x_advance + TRACK
    return first, second, (x - TRACK) * s


BUBBLE = "M20 13h24a7 7 0 0 1 7 7v15a7 7 0 0 1-7 7H31l-9.5 8.5V42H20a7 7 0 0 1-7-7V20a7 7 0 0 1 7-7z"
SPARK = "M32 18.5Q33.3 26.2 41 27.5Q33.3 28.8 32 36.5Q30.7 28.8 23 27.5Q30.7 26.2 32 18.5Z"
SQUARE = "M16 0h32a16 16 0 0 1 16 16v32a16 16 0 0 1-16 16H16A16 16 0 0 1 0 48V16A16 16 0 0 1 16 0z"


def icon(style, x=0, y=0, k=1.0, square_corners=True):
    """Icon artwork in a 64-unit box, placed at (x, y) scaled by k."""
    g = f'<g transform="translate({x:g} {y:g}) scale({k:g})">'
    sq = SQUARE if square_corners else "M0 0h64v64H0z"
    if style == "color":
        body = (f'<path d="{sq}" fill="{GREEN}"/><path d="{BUBBLE}" fill="{WHITE}"/>'
                f'<path d="{SPARK}" fill="{GREEN}"/><circle cx="42.5" cy="19.5" r="2.4" fill="{SUN}"/>')
    elif style == "reversed":
        body = (f'<path d="{sq}" fill="{WHITE}"/><path d="{BUBBLE}" fill="{GREEN}"/>'
                f'<path d="{SPARK}" fill="{WHITE}"/><circle cx="42.5" cy="19.5" r="2.4" fill="{SUN}"/>')
    else:  # one-color: the bubble is cut out of the square, the spark sits in the hole
        c = INK if style == "mono" else WHITE
        body = f'<path d="{sq}{BUBBLE}" fill="{c}" fill-rule="evenodd"/><path d="{SPARK}" fill="{c}"/>'
    return g + body + "</g>"


def svg(w, h, inner, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.2f} {h:.2f}" '
            f'width="{w:.0f}" height="{h:.0f}" role="img" aria-label="{label}">'
            f"<title>{label}</title>{inner}</svg>\n")


def write(name, content):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(content)
    print("wrote", name)


LABEL = "AI Taught Simple"
TEXT_COLORS = {"color": (INK, GREEN), "reversed": (WHITE, WHITE), "mono": (INK, INK), "white": (WHITE, WHITE)}

# Icons
for style, name in [("color", "ats-icon.svg"), ("reversed", "ats-icon-reversed.svg"),
                    ("mono", "ats-icon-mono.svg"), ("white", "ats-icon-white.svg")]:
    write(name, svg(64, 64, icon(style), LABEL + " icon"))
write("ats-icon-square.svg", svg(64, 64, icon("color", square_corners=False), LABEL + " icon"))

# Horizontal lockup: icon 64, gap 14, wordmark sized so the cap height is 0.37 of the icon
SIZE_H = 64 * 0.37 * UPM / CAP
base_h = 32 + (CAP * SIZE_H / UPM) / 2
for style in ["color", "reversed", "mono", "white"]:
    a, b, w = text_paths(SIZE_H, 78, base_h)
    ca, cb = TEXT_COLORS[style]
    inner = icon(style) + f'<path d="{" ".join(a)}" fill="{ca}"/><path d="{" ".join(b)}" fill="{cb}"/>'
    suffix = "" if style == "color" else "-" + style
    write(f"ats-logo-horizontal{suffix}.svg", svg(78 + w, 64, inner, LABEL))

# Stacked lockup: icon on top, wordmark centered below
SIZE_S = 64 * 0.34 * UPM / CAP
_, _, w_s = text_paths(SIZE_S, 0, 0)
W = max(64.0, w_s)
base_s = 64 + 16 + CAP * SIZE_S / UPM
H = base_s + DESC * SIZE_S / UPM
for style in ["color", "reversed"]:
    a, b, _ = text_paths(SIZE_S, (W - w_s) / 2, base_s)
    ca, cb = TEXT_COLORS[style]
    inner = icon(style, (W - 64) / 2, 0) + f'<path d="{" ".join(a)}" fill="{ca}"/><path d="{" ".join(b)}" fill="{cb}"/>'
    suffix = "" if style == "color" else "-" + style
    write(f"ats-logo-stacked{suffix}.svg", svg(W, H, inner, LABEL))

print("cap", CAP, "desc", DESC, "upm", UPM)
