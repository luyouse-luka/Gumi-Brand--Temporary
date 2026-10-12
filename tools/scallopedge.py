#!/usr/bin/env python3
"""Is the scallop plate's edge vector-sharp, or a stretched raster?

  python3 tools/scallopedge.py [--live --password 1234]

The plate is drawn by .gb-scallop-box::before through a mask. Until r129 that
mask was a 320x320 PNG, and the boxes that use it are 520 (science disc) and 598
(how-gumi-works media) wide -- so the edge was a raster stretched 160-190%, which
is what read as blurry.

Measured, not eyeballed: render the mask the page actually resolves onto a flat
plate and count pixels that are neither the plate colour nor the page. A vector
edge only has the antialiasing of the curve itself.

  320 PNG stretched to 520 -> 1.33% soft
  the 520 SVG              -> 0.52% soft
"""
import argparse
import pathlib
import sys

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
LIVE = 'https://gumi.com.au'
PLATE = (245, 241, 233)     # $c-sand, the disc's own --box-bg
LIMIT = 1.0                 # % of ink allowed to be neither plate nor page

FIXTURE = """<style>body{margin:0;background:#fff}
div{width:520px;height:520px;background:#F5F1E9;
-webkit-mask:%s center / 100%% 100%% no-repeat;
mask:%s center / 100%% 100%% no-repeat}</style><div id=t></div>"""


def measure(png):
    im = Image.open(png).convert('RGB')
    px = im.load()
    filled = soft = 0
    box = [im.width, im.height, 0, 0]
    for y in range(im.height):
        for x in range(im.width):
            r, g, b = px[x, y]
            if r >= 250 and g >= 250 and b >= 250:
                continue                       # masked out, page shows through
            filled += 1
            box[0] = min(box[0], x); box[1] = min(box[1], y)
            box[2] = max(box[2], x); box[3] = max(box[3], y)
            if not (abs(r - PLATE[0]) <= 2 and abs(g - PLATE[1]) <= 2
                    and abs(b - PLATE[2]) <= 2):
                soft += 1
    return filled, soft, box


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--live', action='store_true')
    ap.add_argument('--password')
    a = ap.parse_args()
    url = (LIVE + '/pages/how-gumi-works') if a.live \
        else 'file://' + str(ROOT / 'how-gumi-works.html')

    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=CHROME)
        ctx = br.new_context(viewport={'width': 1440, 'height': 900})
        if a.live and a.password:
            ctx.request.post(LIVE + '/password', form={
                'form_type': 'storefront_password', 'utf8': '✓', 'password': a.password})
        pg = ctx.new_page()
        pg.goto(url, wait_until='load', timeout=60000)
        pg.wait_for_timeout(1800)
        mask = pg.evaluate(
            "() => { const b = document.querySelector('.gb-scallop-box');"
            "  if (!b) return null;"
            "  const cs = getComputedStyle(b, '::before');"
            "  return cs.maskImage || cs.webkitMaskImage; }")
        if not mask or mask == 'none':
            print('RED  no .gb-scallop-box mask resolved on', url)
            sys.exit(1)
        is_png = 'image/png' in mask
        fx = ctx.new_page()
        fx.set_content(FIXTURE % (mask, mask))
        fx.wait_for_timeout(300)
        shot = ROOT / 'tools' / '_scallopedge.png'
        fx.query_selector('#t').screenshot(path=str(shot))
        br.close()

    filled, soft, box = measure(shot)
    shot.unlink()                                # probes must not ride along
    pct = soft / max(filled, 1) * 100
    rows = [
        ('mask is not a raster', not is_png, 'PNG' if is_png else 'vector', 'vector'),
        ('edge is vector-sharp', pct < LIMIT, f'{pct:.2f}% soft', f'< {LIMIT:.2f}%'),
        ('plate fills its box', box == [0, 0, 519, 519], box, [0, 0, 519, 519]),
    ]
    red = 0
    for label, cond, got, want in rows:
        print(('  ok   ' if cond else '  RED  ') + f'{label}: {got}'
              + ('' if cond else f'  (want {want})'))
        red += 0 if cond else 1
    print(f'\n  ink px {filled}, soft {soft}')
    print(f'{len(rows) - red} ok / {red} red')
    sys.exit(1 if red else 0)


if __name__ == '__main__':
    main()
