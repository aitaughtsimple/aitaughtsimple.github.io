"""Build the AI Taught Simple logo files (paper cut-out: yellow paper, green bubble, check mark).

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

INK, GREEN, SUN, WHITE, GRAY = "#1F2925", "#1D5C4B", "#F6C453", "#FFFFFF", "#C8C8C8"
LOC = {"wght": 800, "opsz": 36, "wdth": 100}

inst = instantiateVariableFont(TTFont(FONT), LOC)
UPM = inst["head"].unitsPerEm
GS = inst.getGlyphSet()
ORDER = inst.getGlyphOrder()
CMAP = inst.getBestCmap()
hbfont = hb.Font(hb.Face(hb.Blob.from_file_path(FONT)))
hbfont.set_variations(LOC)
TRACK = -0.02 * UPM


def bounds(ch):
    bp = BoundsPen(GS)
    GS[CMAP[ord(ch)]].draw(bp)
    return bp.bounds


CAP = bounds("H")[3]
DESC = -bounds("g")[1]


def shape_paths(text, size, x0, baseline, accent_from=None):
    """Outline `text`. Returns (paths, accent_paths, width, accent_x0, accent_x1)."""
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(hbfont, buf, {"kern": True, "liga": True})
    s = size / UPM
    x = 0.0
    main, accent = [], []
    ax0 = ax1 = None
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        gx = x0 + (x + pos.x_offset) * s
        pen = SVGPathPen(GS, ntos=lambda v: ("%.2f" % v).rstrip("0").rstrip("."))
        GS[ORDER[info.codepoint]].draw(TransformPen(pen, (s, 0, 0, -s, gx, baseline - pos.y_offset * s)))
        d = pen.getCommands()
        is_accent = accent_from is not None and info.cluster >= accent_from
        if d:
            (accent if is_accent else main).append(d)
        if is_accent:
            ax0 = gx if ax0 is None else ax0
            ax1 = x0 + (x + pos.x_advance) * s
        x += pos.x_advance + TRACK
    return main, accent, (x - TRACK) * s, ax0, ax1


def highlight(x0, x1, baseline, size):
    """Yellow marker stroke behind the lower half of a word."""
    top, bot = baseline - 0.36 * size, baseline + 0.05 * size
    cx, cy = (x0 + x1) / 2, (top + bot) / 2
    return (f'<rect x="{x0 - 0.08 * size:.2f}" y="{top:.2f}" width="{x1 - x0 + 0.2 * size:.2f}" '
            f'height="{bot - top:.2f}" rx="{0.1 * size:.2f}" fill="{SUN}" transform="rotate(-1.5 {cx:.2f} {cy:.2f})"/>')


# Icon artwork in a 64-unit box (the translate recentres the tilted paper's bounds)
PAPER = '<rect x="5" y="9" width="50" height="48" rx="8" transform="rotate(-8 30 33)" fill="{c}"/>'
BUBBLE = "M22 12h26a8 8 0 0 1 8 8v14a8 8 0 0 1-8 8H34l-10 9v-9h-2a8 8 0 0 1-8-8V20a8 8 0 0 1 8-8z"
CHECK = "M26 27.5l5.5 5.5 10.5-11"


def icon(style, x=0.0, y=0.0):
    paper, bubble, check = {"color": (SUN, GREEN, WHITE), "reversed": (SUN, WHITE, GREEN),
                            "gray": (GRAY, INK, WHITE)}[style]
    return (f'<g transform="translate({x + 2:.2f} {y - 1:.2f})">' + PAPER.format(c=paper) +
            f'<path d="{BUBBLE}" fill="{bubble}"/>'
            f'<path d="{CHECK}" fill="none" stroke="{check}" stroke-width="4.4" stroke-linecap="round" stroke-linejoin="round"/></g>')


def icon_square(bg):
    """Full-bleed square (profile pictures, Apple touch icon): artwork scaled to survive a circle crop."""
    return (f'<rect width="64" height="64" fill="{bg}"/>'
            f'<g transform="translate(32 32) scale(0.78) translate(-32 -32)">{icon("color")}</g>')


def svg(w, h, inner, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.2f} {h:.2f}" width="{w:.0f}" height="{h:.0f}" '
            f'role="img" aria-label="{label}"><title>{label}</title>{inner}</svg>\n')


def write(name, content):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(content)
    print("wrote", name)


LABEL = "AI Taught Simple"
TEXT_COLOR = {"color": INK, "reversed": WHITE, "gray": INK}

for style, name in [("color", "ats-icon.svg"), ("reversed", "ats-icon-reversed.svg"), ("gray", "ats-icon-gray.svg")]:
    write(name, svg(64, 64, icon(style), LABEL + " icon"))
write("ats-icon-square.svg", svg(64, 64, icon_square("#FBF7F0"), LABEL + " icon"))

# 1. Horizontal: icon + one line, marker behind "Simple"
size = 64 * 0.37 * UPM / CAP
base = 32 + CAP * size / UPM / 2
for style in ["color", "reversed", "gray"]:
    main, acc, w, ax0, ax1 = shape_paths(LABEL, size, 80, base, accent_from=len("AI Taught "))
    mark = highlight(ax0, ax1, base, size) if style != "reversed" else ""
    c = TEXT_COLOR[style]
    inner = icon(style) + mark + f'<path d="{" ".join(main + acc)}" fill="{c}"/>'
    write("ats-logo-horizontal" + ("" if style == "color" else "-" + style) + ".svg", svg(80 + w + 4, 64, inner, LABEL))

# 2. Compact: icon + two lines ("AI Taught" / "Simple"), the website-style lockup
size2 = 64 * 0.31 * UPM / CAP
lh = 0.95 * size2
cap2 = CAP * size2 / UPM
b1 = 32 - (cap2 + lh) / 2 + cap2
b2 = b1 + lh
for style in ["color", "reversed", "gray"]:
    m1, _, w1, _, _ = shape_paths("AI Taught", size2, 78, b1)
    m2, _, w2, _, _ = shape_paths("Simple", size2, 78, b2)
    mark = highlight(78, 78 + w2, b2, size2) if style != "reversed" else ""
    c = TEXT_COLOR[style]
    h = max(64.0, b2 + DESC * size2 / UPM)
    inner = icon(style) + mark + f'<path d="{" ".join(m1 + m2)}" fill="{c}"/>'
    write("ats-logo-compact" + ("" if style == "color" else "-" + style) + ".svg", svg(78 + max(w1, w2) + 4, h, inner, LABEL))

# 3. Stacked: icon centered above one line
size3 = 64 * 0.34 * UPM / CAP
_, _, w3, _, _ = shape_paths(LABEL, size3, 0, 0)
W = max(64.0, w3) + 6
b3 = 64 + 16 + CAP * size3 / UPM
H = b3 + DESC * size3 / UPM
for style in ["color", "reversed"]:
    main, acc, _, ax0, ax1 = shape_paths(LABEL, size3, (W - w3) / 2, b3, accent_from=len("AI Taught "))
    mark = highlight(ax0, ax1, b3, size3) if style != "reversed" else ""
    c = TEXT_COLOR[style]
    inner = icon(style, (W - 64) / 2, 0) + mark + f'<path d="{" ".join(main + acc)}" fill="{c}"/>'
    write("ats-logo-stacked" + ("" if style == "color" else "-" + style) + ".svg", svg(W, H, inner, LABEL))
