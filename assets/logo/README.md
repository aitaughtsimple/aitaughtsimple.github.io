# AI Taught Simple logo

A green chat bubble with a white check mark, sitting on a tilted square of yellow paper, the same cut-paper look as the website. The wordmark is Bricolage Grotesque ExtraBold with a yellow marker stroke behind "Simple". The text in every file is converted to outlines, so the logo looks the same on any computer, printer, or app.

## Which file to use

| Where | File |
|---|---|
| Main logo: website, documents, flyers, slides (light background) | `ats-logo-compact.svg` or `ats-logo-compact-2000.png` |
| A wide, short space: email signature, letterhead, footer | `ats-logo-horizontal.svg` or `ats-logo-horizontal-2400.png` |
| Square spaces: poster, sign, title slide | `ats-logo-stacked.svg` or `ats-logo-stacked-1600.png` |
| On the club green or another dark color | any `-reversed` file (white text, no marker stroke) |
| Black-and-white printing | `ats-logo-compact-gray.svg`, `ats-logo-horizontal-gray.svg`, `ats-icon-gray.svg` |
| Profile picture (Gmail, Instagram, Google) | `ats-profile-1080.png` (full square on paper color, so circle crops keep the whole mark) |
| App icon or small badge | `ats-icon.svg`, `ats-icon-512.png`, `ats-icon-1024.png` |

Use the SVG files when the program accepts them (Canva and most design tools do). Use the PNGs everywhere else, including Google Docs and Slides. The PNGs have transparent backgrounds.

## Colors

| Name | Hex | Use |
|---|---|---|
| Club green | `#1D5C4B` | The bubble, buttons, links |
| Ink | `#1F2925` | Wordmark, body text |
| Sun | `#F6C453` | The paper square and the marker stroke. Never for text |
| Paper | `#FBF7F0` | Page background |
| White | `#FFFFFF` | Check mark, reversed text |

Fonts: Bricolage Grotesque for headings and the wordmark, Atkinson Hyperlegible Next for body text. Both are free on Google Fonts.

## Rules

- Leave clear space around the logo equal to at least a quarter of the icon's height.
- Smallest sizes: the compact logo 110 px wide on screen or 1 inch wide in print. The icon alone works down to 16 px.
- Don't stretch, straighten the paper, outline, shadow, or recolor it, and don't retype the name in another font.
- On a busy photo, put the logo on a solid paper or green panel.
- The icon alone is fine where the name already appears nearby, such as a browser tab or app icon.

## Rebuilding the files

`tools/build_logo.py` makes every SVG here from the Bricolage Grotesque variable font (free from the google/fonts repository on GitHub, `ofl/bricolagegrotesque`). It needs Python with `fonttools` and `uharfbuzz`:

```bash
python3 -m venv .logo-venv && .logo-venv/bin/pip install fonttools uharfbuzz
.logo-venv/bin/python tools/build_logo.py path/to/BricolageGrotesque.ttf assets/logo
```

The PNGs were rendered from the SVGs with headless Chrome. `assets/icon.svg` (the website icon) is a copy of `ats-icon.svg`. `tools/logo-board.html` shows the three directions that were considered.
