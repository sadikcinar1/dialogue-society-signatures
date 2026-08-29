#!/usr/bin/env python3
"""Regenerate the PNG assets from the vector original.

    python3 tools/make-assets.py

Needs poppler (pdftocairo) and Pillow. Not part of the normal build -- the
derived PNGs are committed, so `python3 build.py` needs neither.

ds-mark.png is 70x75 on purpose: its natural size must equal its display size,
or Apple Mail renders it at the file's size when it strips the sizing. See
CLAUDE.md.
"""
import io, os, subprocess, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, 'assets')
PDF = os.path.join(ASSETS, 'ds-logo.pdf')

if not os.path.exists(PDF):
    sys.exit('missing ' + PDF)

subprocess.run(['pdftocairo', '-svg', PDF, os.path.join(ASSETS, 'ds-logo.svg')], check=True)
subprocess.run(['pdftocairo', '-png', '-transp', '-r', '600', '-singlefile',
                PDF, os.path.join(ASSETS, '_full')], check=True)

full = Image.open(os.path.join(ASSETS, '_full.png'))
full = full.crop(full.getbbox())
w, h = full.size
mark = full.crop((0, 0, 1917, 2050))     # the blue mark; the wordmark starts at x=2088


def save(im, name, colors=48):
    q = im.convert('RGBA').quantize(colors=colors, method=Image.FASTOCTREE)
    b = io.BytesIO(); q.save(b, 'PNG', optimize=True)
    open(os.path.join(ASSETS, name), 'wb').write(b.getvalue())
    print('%-22s %s  %d bytes' % (name, im.size, len(b.getvalue())))


def darken_wordmark(im, ink=(230, 235, 239)):
    """A lockup that reads on a dark page.

    The wordmark is black, so on the dark palette it all but disappears; the
    mark beside it is saturated blue and must not move. Neutral pixels are
    remapped towards --ink in proportion to how dark they are, which lifts the
    letters and their antialiasing while leaving every blue pixel untouched.
    """
    im = im.convert('RGBA').copy()
    px = im.load()
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            r, g, b, a = px[x, y]
            if not a or max(r, g, b) - min(r, g, b) >= 40:
                continue                      # transparent, or part of the blue mark
            f = 1.0 - (r + g + b) / 765.0
            px[x, y] = (int(r + (ink[0] - r) * f), int(g + (ink[1] - g) * f),
                        int(b + (ink[2] - b) * f), a)
    return im


save(mark.resize((70, 75), Image.LANCZOS), 'ds-mark.png')
save(mark.resize((600, 643), Image.LANCZOS), 'ds-mark-600.png')
web = full.resize((354, 115), Image.LANCZOS)
save(web, 'ds-lockup-web.png', 64)
save(darken_wordmark(web), 'ds-lockup-web-dark.png', 64)
full.resize((1600, 521), Image.LANCZOS).save(os.path.join(ASSETS, 'ds-lockup.png'))
print('ds-lockup.png          (1600, 521)')
os.remove(os.path.join(ASSETS, '_full.png'))
