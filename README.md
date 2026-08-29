# Dialogue Society email signatures

A three-page static site that produces the organisation's email signatures —
personal or branch — plus two finished signature pages that need no form
filling.

No backend, no database, no build framework. Every page does all of its work in
the visitor's browser.

| Page | What it is |
|---|---|
| `index.html` | the signature maker: fill in a form, copy the result |
| `personal.html` | a finished personal signature |
| `branch.html` | a finished branch signature, with a regional example |

## Build

```bash
npm install          # once, for the test browser
npm run check        # build, then verify
```

or the two steps separately:

```bash
python3 build.py        # writes dist/ and docs/
node test/verify.mjs    # checks the signature survives what mail clients do to it
```

The build needs only Python 3 and Node. The test suite needs Playwright;
`tools/make-assets.py` additionally needs Pillow and poppler, but you only run
that if you change the logo.

Set `PW_CHROMIUM` if your Chromium is somewhere Playwright would not look for
it; otherwise the suite uses Playwright's own download.

## Deploy

**GitHub Pages.** `docs/` holds a built copy of the site and is committed, so
publishing is Settings → Pages → *Deploy from a branch* → `main` / `/docs`.
After that, every `python3 build.py` + push redeploys.

**Cloudflare Pages, Netlify.** Upload
`dist/dialogue-society-signature-app-v7.zip`. Files sit at the archive root, so
the site lands at the root of your address — which matters, because the three
pages link to each other by relative name.

After deploying, check the footer of the live page. It names the version.

## What's in dist/

| Path | What it is |
|---|---|
| `site/` | the whole site, ready to upload to any static host |
| `app-preview.html` | the maker without the download button, for embedding |
| `dialogue-society-signature-app-v7.zip` | the deployable archive |

## Before you change anything

Read **CLAUDE.md**. The signature markup looks over-specified in places, and
each of those places is a mail client bug that took a round trip to find.
