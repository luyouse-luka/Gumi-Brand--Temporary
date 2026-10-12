#!/usr/bin/env python3
"""Quantify the hairline: scan the rounded corner arc of __media.

The straight edges hide it (the photo's own border pixels are near the card
green), but the corner arc is where overflow:hidden anti-aliases the box --
and the only thing under the photo there is the media's own #d9d9d9.

  python3 tools/hlcardarc.py --password 1234 [--nobg]

--nobg re-tests with the grey background removed, to prove it is the cause.
"""
import argparse, io, math
from PIL import Image
from playwright.sync_api import sync_playwright

CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
LIVE = 'https://gumi.com.au'
GREEN = (0, 86, 53)

a = argparse.ArgumentParser()
a.add_argument('--password', required=True)
a.add_argument('--nobg', action='store_true')
args = a.parse_args()


def lum(p):
    return 0.2126 * p[0] + 0.7152 * p[1] + 0.0722 * p[2]


with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=CHROME)
    ctx = b.new_context(viewport={'width': 1440, 'height': 900}, device_scale_factor=2)
    ctx.request.post(LIVE + '/password', form={
        'form_type': 'storefront_password', 'utf8': '✓', 'password': args.password})
    pg = ctx.new_page()
    pg.goto(LIVE + '/', wait_until='domcontentloaded', timeout=90000)
    pg.wait_for_timeout(2000)
    if args.nobg:
        pg.add_style_tag(content='.gb-highlight-card__media{background:none!important}')
    pg.evaluate("""() => document.querySelector('.gb-highlight-card__media')
                      .scrollIntoView({block:'center'})""")
    pg.wait_for_function("""() => {
        const m = document.querySelector('.gb-highlight-card__media');
        const img = m.querySelector('img');
        return getComputedStyle(m).opacity === '1'
            && getComputedStyle(m.closest('.gb-highlight-card')).opacity === '1'
            && img && img.complete && img.naturalWidth > 0;
    }""", timeout=20000)
    pg.wait_for_timeout(600)

    r = pg.evaluate("""() => { const b = document.querySelector(
        '.gb-highlight-card__media').getBoundingClientRect();
        return {x: b.x, y: b.y, w: b.width, h: b.height}; }""")
    im = Image.open(io.BytesIO(pg.screenshot())).convert('RGB')
    dpr = 2
    R = 16          # top-left radius in css px
    cx, cy = r['x'] + R, r['y'] + R      # arc centre

    print(f"{'--nobg' if args.nobg else 'as-is'}  media {r}")
    print('  top-left arc: sample along the radius at each angle, report the')
    print('  brightest pixel found within +-2.5px of the arc')
    worst = None
    for deg in range(5, 90, 5):
        th = math.radians(deg)
        best = None
        for t in [x * 0.25 for x in range(-10, 11)]:      # -2.5 .. +2.5 px
            rad = R + t
            px = cx - rad * math.cos(th)
            py = cy - rad * math.sin(th)
            p = im.getpixel((int(round(px * dpr)), int(round(py * dpr))))
            if best is None or lum(p) > lum(best[0]):
                best = (p, t)
        flag = ''
        # a pixel much brighter than the card green, and desaturated toward grey
        if lum(best[0]) > lum(GREEN) + 30 and abs(best[0][0] - best[0][2]) < 60:
            flag = '  <-- grey-ish hairline'
            worst = best if worst is None or lum(best[0]) > lum(worst[0]) else worst
        print(f'    {deg:2d}deg  {best[0]}  at r{best[1]:+.2f}  lum={lum(best[0]):.0f}{flag}')
    print('  worst:', worst)
    ctx.close(); b.close()
