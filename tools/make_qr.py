#!/usr/bin/env python3
"""Make the flyer's QR code (assets/qr.svg) from the `url` in config.js.

The QR code is generated on your computer. No website is used.

Needs the free `segno` library once:   python3 -m pip install segno
Then, from the project folder, run:     python3 tools/make_qr.py
"""
import pathlib
import re
import sys

try:
    import segno
except ImportError:
    sys.exit("Install segno first:  python3 -m pip install segno")

root = pathlib.Path(__file__).resolve().parent.parent
config = (root / "config.js").read_text(encoding="utf-8")
match = re.search(r'url:\s*"([^"]+)"', config)
if not match:
    sys.exit('Could not find  url: "..."  in config.js')
url = match.group(1)

out = root / "assets" / "qr.svg"
qr = segno.make(url, error="q")  # "q" still scans if about a quarter of the code is smudged
qr.save(
    str(out),
    kind="svg",
    border=4,          # quiet zone that scanners need
    dark="#000000",
    light="#ffffff",
    xmldecl=False,
    omitsize=True,     # scales to whatever size the flyer gives it
    title="QR code for " + url,
)
print("Wrote %s for %s (version %s, error level %s)" % (out.relative_to(root), url, qr.version, qr.error))
