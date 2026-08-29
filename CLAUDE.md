# Dialogue Society email signatures

A three-page static site that produces the organisation's email signatures,
plus two finished signature pages. No backend, no database, no framework.

```
python3 build.py          # rebuild into dist/ and docs/
node test/verify.mjs      # 50 invariant checks against a real browser
```

Published from `docs/` by GitHub Pages, and deployable anywhere else by
uploading `dist/dialogue-society-signature-app-<VERSION>.zip`.

`docs/` is generated, not hand-edited, but it **is** committed — it is what
Pages serves. A change that skips `python3 build.py` ships nothing.

---

## Read this before changing the signature

Almost every decision in `src/template.js` is there because something broke in
a real mail client. The comments say what; this says why, and what will happen
if you undo it.

**Apple Mail rewrites pasted signatures.** Observed directly, on the user's own
machine, over several rounds:

| What it does | Consequence |
|---|---|
| Strips `width` / `height` attributes **and** the matching CSS | An image falls back to its file's natural size |
| Strips `font-size` / `line-height` | Anything relying on a 1px font to stay thin inflates |
| Leaves **borders** completely alone | Borders are the only reliable way to draw a line |
| Reflows the table if its pane is narrower than the signature | Cells get squeezed; the social row wraps |
| Promotes a data-URI image to a `cid:` attachment as it pastes | An attachment cannot live in a table cell, so the image is hoisted out of the layout |

Four rules follow, and the test suite enforces all four.

**1. The logo file's natural size must equal its display size.**
`assets/ds-mark.png` is exactly 70×75 and is displayed at 70×75. It was once a
240px file displayed at 70px; Apple Mail dropped the sizing and rendered it at
240px, wrecking the layout. A 2× asset would look marginally crisper on Retina
and would break the same way. Don't.

**2. Lines are borders, never thin filled cells.**
The divider above the charity line was a 1px-tall cell with a grey background.
A filled cell needs a `&nbsp;` to hold its height; when Apple Mail stripped the
`font-size:1px`, that space grew to the inherited size and the hairline
rendered as an 18px grey bar. It is now `border-top` on the charity cell. The
blue rule was likewise a 4px cell that got squeezed to **zero width**; it is now
`border-left` on the text cell.

**3. Fewer cells in the row is better.**
The layout is two cells — logo, then text-with-left-border — not three. Three
cells gave the narrow-pane reflow more to push around. A narrow pane squeezes
the text column until the social row wraps; the mitigation is in the Apple Mail
instructions (widen the Settings window), not more markup.

**The logo landing above the text is a different bug, and not a reflow at all.**
It was once recorded here as narrow-pane wrapping. It is not: table cells cannot
wrap onto separate lines, and the Cocoa text engine keeps them side by side down
to a 74px pane. What actually happens is in rule 4.

**4. What reaches the clipboard must be a document, not a selection fragment.**
Mail converts the data-URI logo into a `cid:` attachment as it pastes, and an
attachment cannot stay inside a table cell — so Mail cuts the markup at the
image and re-opens the document there. Read out of Mail's own
`~/Library/Mobile Documents/com~apple~mail/Data/V4/Signatures/*.mailsignature`,
a broken paste looks like this:

```html
<table width="378"><tbody><tr></td></tr></tbody></table>   <!-- logo cell, emptied -->
<SPAN class="Apple-string-attachment"><OBJECT ... data="cid:..."></OBJECT></SPAN>
<head><meta charset="UTF-8"></head>                        <!-- the seam -->
<table width="378"><tbody><tr><td width="264">…text…</td></tr></tbody></table>
```

The seam is a stray `<head>`. `document.execCommand('copy')` serialises the
*selection*, and Safari prefixes that fragment with `<head><meta charset>` — a
`<head>` is invalid outside a document, and it is exactly where Mail re-opened.
The same signature pasted correctly earlier the same day, as a single-part
`text/html` with a proper `<head></head><body dir="auto">` and the `<img>` still
in its cell.

So `copyNode` in `src/theme.py` writes a complete document through
`ClipboardItem` and keeps `execCommand` only as a fallback. That also stops the
page's own computed styles — `IBM Plex Sans`, `caret-color`, `box-sizing` on
every node — from being baked into the signature, which is what selection
copying did. Browsers sanitise clipboard HTML on the way through, so the test
asserts the invariant that matters (no `<head>` outside a document, the `<img>`
still inside a `<td>`, no page chrome) rather than the exact wrapper.

There is a `layout: 'stacked'` branch in `template.js` — single column, immune
to reflow. It was built, shipped, and rejected: the user wants the logo on the
left. Don't quietly switch back to it to fix a client bug.

---

## Colour

Sampled from the organisation's own logo, then checked against WCAG AA.

| Token | Hex | Used for | Contrast on white |
|---|---|---|---|
| Brand blue | `#008AC4` | Logo and the vertical rule — **graphics only** | 3.87:1 |
| Text blue | `#007AAD` | Links, organisation line, branch lead line | 4.79:1 AA |
| Brand grey | `#424242` | Name, contact values, address | 10.05:1 AA |
| Soft grey | `#6E6E6E` | Job title, second line, charity line | 5.10:1 AA |
| Hairline | `#DCDCDC` | The rule above the charity line | — |

Brand blue is the real logo colour but only reaches 3.87:1, so it never carries
text. Text blue is the same hue darkened until it passes.

**`#0797C8` must never come back.** That was the blue in the signatures this
project replaced. It matches neither the logo nor the contrast standard. The
test suite fails if it appears. The same goes for the invented navy `#183B5B`
and slate `#5B6F82` from those older signatures.

---

## Layout

The signature is 378px wide: 70px logo + 22px gap + 4px border + 18px padding +
264px text.

264px is not arbitrary — the social row needs 259.4px on one line, and the
column was once set to exactly 259, which made it wrap. Narrowing the text
column will wrap the social row before anything else shows a problem.

Border and padding sit **outside** a declared cell width in the email box
model. The text cell declares `width:264px` and occupies 286px. Getting this
wrong makes the table wider than the number in the `width` attribute.

---

## Layout of the code

```
build.py              one command; writes dist/ and docs/
src/template.js       THE signature. Plain ES5, no dependencies.
src/render.js         runs template.js under Node so the build needs no browser
src/theme.py          CSS, fonts, <head>, nav, clipboard helpers, instructions
src/app.py            the staff app (Personal / Branch form)
src/pages.py          the two finished signature pages
assets/               logo masters and derived PNGs
tools/make-assets.py  regenerate the PNGs from the vector original
test/verify.mjs       the invariants above, checked in a real browser
docs/                 generated; the copy GitHub Pages serves
```

The site is **one flat folder**. The three pages link to each other by relative
name, so the app and the finished pages cannot live in separate directories --
they used to, and neither could reach the other.

`src/template.js` is the single source of truth for signature markup. The build
renders through it, and the app inlines the same file to redraw the preview as
someone types, so the two can never drift.

`app.py` returns two variants of the page. The **preview** variant has the
Outlook download button and all of its code removed, because an artifact viewer
cannot start a download and a button that silently does nothing is worse than
no button.

---

## The page chrome

Three things in `src/theme.py` are load-bearing and easy to undo:

**The masthead lockup ships in two files.** `ds-lockup-web.png` has a black
wordmark; on the dark palette it drops to about 1.5:1 and is unreadable. The
`<picture>` in `theme.lockup()` swaps in `ds-lockup-web-dark.png` under
`prefers-color-scheme: dark`. `tools/make-assets.py` derives the second file by
lifting only the *neutral* pixels — the blue mark is left exactly as it is.

**The preview sits above the form on a phone.** In one column the form comes
first and the preview lands below all of it, so nothing you type is on screen
while you type it. `.sticky{order:-1}` under 800px is what fixes that.

**The signature is wider than a phone.** `.stage` scrolls, and the fading right
edge is the only cue that it does. It is painted with
`background-attachment:local` so it travels with the content.

## Shipping a change

1. Edit, then `python3 build.py`.
2. `node test/verify.mjs` — all 50 must pass.
3. **Bump `VERSION` in `build.py`.** It shows in the page footer and the zip
   filename.
4. Commit `docs/` along with the source. Pages serves that folder.

That version stamp exists for a concrete reason: every zip once shared the same
filename, an older one got deployed by mistake, and the resulting "the layout is
wrong again" took a round trip to diagnose. The footer tells you what is
actually live; the filename stops the collision.

---

## The logo, embedded vs linked

The mark is embedded as a data URI by default, so a signature has no external
dependency and cannot lose its logo when a host lapses or a file moves. Gmail
re-hosts the image on its own servers as you paste and Apple Mail attaches it,
so the embedded copy doesn't actually travel with sent mail.

`LOGO_URL` at the top of the built `index.html` switches to a linked logo. If
you use it, the URL must be on `dialoguesociety.org` and never on whatever host
serves the app — it gets written into every signature made from that point and
stays in mail already sent, so it has to outlive the hosting.

---

## Two forms

**Personal** — name in grey caps leads, organisation underneath in blue.

**Branch** — nobody is named, so the organisation moves up into the lead
position at 15px, with an optional second line under it for a motto. For shared
inboxes (`info@`, branch addresses, bookings), newsletters, and regional
branches. A region typed into the form is appended: *Dialogue Society
Birmingham*. Over ~45 characters the second line wraps, and the app warns.
