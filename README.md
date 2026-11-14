# AI Taught Simple website

Free, hands-on AI classes for older adults, run by students at Glenelg High School (Howard County, MD).

Live site: https://aitaughtsimple.github.io/
Printable flyer: https://aitaughtsimple.github.io/flyer/

Plain HTML and CSS with a little JavaScript. No framework, no build step. GitHub Pages publishes whatever is on the `main` branch, usually within a minute of a push.

## What's where

| File | What it is |
| --- | --- |
| `config.js` | **The one place to change the name, email, web address, team names, and first-class date.** |
| `index.html` | The main page (hero, what we teach, how a class works, hosting, about, upcoming, FAQ, contact) |
| `flyer/index.html` | One-page printable flyer with the QR code |
| `assets/styles.css` | Main page design |
| `assets/flyer.css` | Flyer design and print settings (US letter, one sheet) |
| `assets/site.js` | Fills pages with the values from `config.js`, builds email links, copy button |
| `assets/qr.svg` | QR code pointing at the site (made locally by `tools/make_qr.py`) |
| `assets/og-image.png` | Picture shown when the link is texted or emailed (made from `tools/og-card.html`) |
| `404.html` | Shown for broken links |
| `thanks/index.html` | "Message sent" page (only used if a visitor's browser has JavaScript off) |
| `robots.txt`, `sitemap.xml` | Help Google find and list the site |

## Common edits

**Edit the About section.** In `index.html`, find `<!-- 5. About us -->`. The two paragraphs and the two name cards (Jaiden, Shubh) are plain text you can change.

## Contact form

Messages from the Contact form are emailed to the address in `config.js` through [FormSubmit](https://formsubmit.co) (free, no account). Each message arrives as a table with the topic, name, email, organization, and message, and the sender gets an automatic "we got your message" email.

- **First-time setup:** the very first message triggers an "Activate Form" email from FormSubmit to the club inbox. Click the button in that email once. Until then, messages are held, not delivered.
- **Replying:** just press Reply in Gmail. It goes to the person who wrote in.
- **Spam:** a hidden trap box blocks most bots without making visitors solve a puzzle.
- **If you change the email** in `config.js`, the form follows it automatically, and the new address will get its own one-time activation email.

**Add class dates.** In `index.html`, find the `Upcoming classes` section and replace the paragraph under "First classes coming..." with the date, time, and place.

**Change the club name.** Edit `name` in `config.js`. Then update the lines marked `RENAME` at the top of `index.html` and `flyer/index.html` (apps that show link previews don't run `config.js`). Remake the preview picture with the command at the top of `tools/og-card.html` after changing the name there too.

**Change the web address.** Edit `url` in `config.js`, update `og:url` and `og:image` in `index.html`, then remake the QR code:

```bash
python3 -m pip install segno
python3 tools/make_qr.py
```

Reprint any flyers after the address changes. Old QR codes will point to the old address.

**Cache note.** Pages load `config.js`, `site.js`, and the stylesheets with a `?v=...` tag. After changing any of those files, bump the tag in the HTML files (any new value works, for example the latest commit id) so visitors get the new version right away instead of a saved older copy.

## Printing the flyer

Open `/flyer/`, press **Print this flyer**, and choose US Letter. If the browser adds a web address or date in the corners, turn off "Headers and footers" in the print window. The "Date / Time / Place" lines are for writing in details by hand for a specific class.

## Rules this site follows

- No made-up stats, testimonials, partner logos, or partnership claims.
- No phone numbers or home addresses. First names only.
- Text and background colors meet WCAG AAA contrast (7:1 or better). Body text is 19 to 20px. Buttons are at least 48px tall.
