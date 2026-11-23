# AI Taught Simple logo

A green rounded square holding a white chat bubble with an AI spark. The wordmark is Bricolage Grotesque ExtraBold, with "Simple" in green. The text in every file is converted to outlines, so the logo looks the same on any computer, printer, or app.

## Which file to use

| Where | File |
|---|---|
| Website, documents, flyers (light background) | `ats-logo-horizontal.svg` or `ats-logo-horizontal-2400.png` |
| On the club green or another dark color | `ats-logo-horizontal-reversed.svg` or `ats-logo-horizontal-reversed-2400.png` |
| Black-and-white printing | `ats-logo-horizontal-mono.svg` |
| On a dark photo | `ats-logo-horizontal-white.svg` |
| Square spaces: slide title, poster, sign | `ats-logo-stacked.svg` or `ats-logo-stacked-1600.png` (`-reversed` on dark) |
| Profile picture (Gmail, Instagram, Google) | `ats-profile-1080.png` (full square, so circle crops still show the whole bubble) |
| App icon or small badge | `ats-icon.svg`, `ats-icon-512.png`, `ats-icon-1024.png` |
| Icon in one color | `ats-icon-mono.svg` (dark) or `ats-icon-white.svg` (light on dark) |

Use the SVG files when the program accepts them (Google Docs, Slides and Canva do). Use the PNGs everywhere else. The PNGs have transparent backgrounds.

## Colors

| Name | Hex | Use |
|---|---|---|
| Club green | `#1D5C4B` | Icon, "Simple", buttons |
| Ink | `#1F2925` | Wordmark, body text |
| Sun | `#F6C453` | The small dot in the bubble, highlights. Never for text |
| Paper | `#FBF7F0` | Page background |
| White | `#FFFFFF` | Bubble, reversed text |

Fonts: Bricolage Grotesque for headings and the wordmark, Atkinson Hyperlegible Next for body text. Both are free on Google Fonts.

## Rules

- Leave clear space around the logo equal to at least a quarter of the icon's height.
- Smallest sizes: the horizontal logo 120 px wide on screen or 1 inch wide in print. The icon alone works down to 16 px.
- Don't stretch, rotate, outline, shadow, or recolor it, and don't retype the name in another font.
- On a busy photo, use the white version, or put the logo on a solid panel.
- The icon alone is fine where the name already appears nearby, such as a browser tab or app icon.

## Rebuilding the files

`tools/build_logo.py` makes every SVG here from the Bricolage Grotesque variable font (free from the google/fonts repository on GitHub, `ofl/bricolagegrotesque`). It needs Python with `fonttools` and `uharfbuzz`:

```bash
python3 -m venv .logo-venv && .logo-venv/bin/pip install fonttools uharfbuzz
.logo-venv/bin/python tools/build_logo.py path/to/BricolageGrotesque.ttf assets/logo
```

The PNGs were rendered from the SVGs with headless Chrome. `assets/icon.svg` (the website icon) is a copy of `ats-icon.svg`.
