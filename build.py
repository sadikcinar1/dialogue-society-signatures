#!/usr/bin/env python3
"""Build every Dialogue Society signature deliverable.

    python3 build.py

Outputs:
    dist/site/               the whole site -- app plus both finished pages
    dist/app-preview.html    the app without the download button, for embedding
    dist/dialogue-society-signature-app-<VERSION>.zip
    docs/                    a copy of dist/site, which is what GitHub Pages serves

The site is one flat folder because the three pages link to each other by
relative name. Splitting the app and the finished pages into separate folders,
as this used to, meant neither could reach the other.

Nothing here defines the signature markup. That lives in src/template.js and
is rendered through Node, so there is exactly one source of truth for what a
Dialogue Society signature looks like.
"""
import base64, json, os, shutil, subprocess, sys, zipfile

sys.path.insert(0, 'src')
import theme                                        # noqa: E402
import app as app_page                              # noqa: E402
import pages as ready_made                          # noqa: E402

# Bump this whenever you ship. It appears in the page footer and the zip name,
# so you can always tell which build is actually deployed.
VERSION = 'v9'
LAYOUT  = 'logo left'
VLABEL  = '%s · %s' % (VERSION, LAYOUT)

ROOT   = os.path.dirname(os.path.abspath(__file__))
DIST   = os.path.join(ROOT, 'dist')
SITE   = os.path.join(DIST, 'site')
DOCS   = os.path.join(ROOT, 'docs')          # GitHub Pages serves this folder
ASSETS = os.path.join(ROOT, 'assets')


def mark_data_uri():
    """The 70x75 mark, embedded in every signature.

    Its natural size deliberately equals its display size. Apple Mail strips
    width and height attributes when it converts an embedded image, and then
    falls back to the file's own dimensions -- so a larger file renders huge.
    Do not swap this for a 2x asset without reading CLAUDE.md first.
    """
    png = open(os.path.join(ASSETS, 'ds-mark.png'), 'rb').read()
    return 'data:image/png;base64,' + base64.b64encode(png).decode()


def lockup_data_uri(name='ds-lockup-web.png'):
    """Masthead lockup, sized for display at 118x38 (3x for retina).

    assets/ds-lockup.png is the large version for print and slides; embedding
    that one would add ~150 KB of base64 to every page for no visible gain.

    ds-lockup-web-dark.png is the same lockup with the black wordmark lifted to
    the dark palette's ink. On a dark page the black one all but vanishes.
    """
    png = open(os.path.join(ASSETS, name), 'rb').read()
    return 'data:image/png;base64,' + base64.b64encode(png).decode()


def render(**data):
    """Render one signature by running src/template.js in Node."""
    out = subprocess.run(
        ['node', os.path.join(ROOT, 'src', 'render.js'), json.dumps(data)],
        capture_output=True, text=True)
    if out.returncode:
        raise SystemExit('render failed: ' + out.stderr.strip())
    return out.stdout


def main():
    shutil.rmtree(DIST, ignore_errors=True)
    shutil.rmtree(DOCS, ignore_errors=True)
    os.makedirs(SITE, exist_ok=True)

    mark   = mark_data_uri()
    lockup = lockup_data_uri()
    dark   = lockup_data_uri('ds-lockup-web-dark.png')

    ctx = dict(VERSION=VERSION, VLABEL=VLABEL, MARK=mark, LOCKUP=lockup,
               LOCKUP_DARK=dark, render=render, theme=theme)

    def write(name, text):
        open(os.path.join(SITE, name), 'w', encoding='utf-8').write(text)

    # ---- the staff app -------------------------------------------------
    hosted, preview = app_page.build(**ctx)
    write('index.html', hosted)
    open(os.path.join(DIST, 'app-preview.html'), 'w', encoding='utf-8').write(preview)

    # ---- the two finished pages ----------------------------------------
    for name, html in ready_made.build(**ctx).items():
        write(name, html)

    # ---- everything else the site needs --------------------------------
    shutil.copy(os.path.join(ASSETS, 'ds-mark.png'), os.path.join(SITE, 'ds-mark.png'))
    write('README.txt', app_page.readme(VERSION))
    # GitHub Pages runs Jekyll over the folder otherwise, which is harmless here
    # but only by luck -- one leading underscore in a filename and it disappears.
    write('.nojekyll', '')

    # ---- the deployable archive ----------------------------------------
    # Files sit at the archive root: Cloudflare Pages and Netlify serve the
    # archive root as the site root, so a nested folder pushes the app to a
    # subpath. The version is in the filename so downloads cannot collide.
    zipname = os.path.join(DIST, 'dialogue-society-signature-app-%s.zip' % VERSION)
    with zipfile.ZipFile(zipname, 'w', zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(SITE)):
            z.write(os.path.join(SITE, f), f)

    # ---- what GitHub Pages publishes -----------------------------------
    shutil.copytree(SITE, DOCS)

    print('built %s (%s)\n' % (VERSION, LAYOUT))
    for base in (DIST, DOCS):
        for root, _, files in os.walk(base):
            for f in sorted(files):
                p = os.path.join(root, f)
                print('  %-52s %7d' % (os.path.relpath(p, ROOT), os.path.getsize(p)))


if __name__ == '__main__':
    main()
