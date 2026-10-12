#!/usr/bin/env python3
"""Mobile hero: the gap between the USP row and the top of the bear's glow.

  python3 tools/herousp.py [--live --password 1234]

Board 228:5932 puts the USPs' bottom at 1314 and the glow's render bounds at
1332.66 -> 18.7px of air. The bear is a full-bleed PNG with no transparent
margin, so its element rect IS its ink box once rotated; the reading below is
pixels, not geometry, because the rotation makes the visible top edge a corner.
"""
import argparse, pathlib, sys
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
LIVE = 'https://gumi.com.au'
WIDTHS = [390, 400, 500, 600, 767]
TARGET = 18.7          # board value
BG = [(0xe7, 0xf8, 0xd0), (0xff, 0xff, 0xff)]   # hero lime-150, page white
TOL = 14
SCAN = 140             # rows below the USP bottom worth looking at


def is_bg(px):
    return any(all(abs(px[i] - c[i]) <= TOL for i in range(3)) for c in BG)


def measure(pg, w, shot):
    box = pg.evaluate("""() => {
      const u = document.querySelector('.gb-usps');
      const h = document.querySelector('.gb-hero');
      if (!u || !h) return null;
      const ub = u.getBoundingClientRect(), hb = h.getBoundingClientRect();
      return {uspBottom: ub.bottom, heroTop: hb.top, heroLeft: hb.left, heroW: hb.width};
    }""")
    if not box:
        return None
    y0 = box['uspBottom']
    pg.screenshot(path=shot, clip={'x': 0, 'y': y0, 'width': w, 'height': SCAN})
    im = Image.open(shot).convert('RGB')
    for y in range(im.height):
        hits = sum(1 for x in range(im.width) if not is_bg(im.getpixel((x, y))))
        if hits >= 3:
            return {'gap': y, 'row_hits': hits,
                    'sample': im.getpixel((max(0, min(im.width - 1, [x for x in range(im.width)
                                if not is_bg(im.getpixel((x, y)))][0])), y))}
    return {'gap': None}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--live', action='store_true')
    ap.add_argument('--password')
    ap.add_argument('--keep', action='store_true', help='keep the scan crops')
    a = ap.parse_args()
    url = LIVE + '/' if a.live else 'file://' + str(ROOT / 'index.html')
    out = ROOT / 'tools' / '_herousp'
    out.mkdir(exist_ok=True)
    rows, red = [], 0
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=CHROME)
        for w in WIDTHS:
            ctx = br.new_context(viewport={'width': w, 'height': 1000})
            if a.live and a.password:
                ctx.request.post(LIVE + '/password', form={
                    'form_type': 'storefront_password', 'utf8': '✓', 'password': a.password})
            pg = ctx.new_page()
            pg.goto(url, wait_until='load', timeout=60000)
            pg.wait_for_timeout(2200)
            # the hero art drifts; park it so the reading is repeatable
            pg.evaluate("""() => { const a = document.querySelector('.gb-hero__art');
              if (a) { a.style.animation = 'none'; a.style.transform = 'none'; } }""")
            pg.wait_for_timeout(120)
            r = measure(pg, w, str(out / f'{w}.png'))
            gap = r and r['gap']
            ok = gap is not None and gap >= TARGET - 4
            red += 0 if ok else 1
            rows.append((w, gap, ok, r and r.get('sample')))
            pg.close(); ctx.close()
        br.close()
    print(f"{'width':>6} {'gap':>6} {'target':>7}  first non-bg pixel")
    for w, gap, ok, s in rows:
        print(f"{w:>6} {str(gap):>6} {TARGET:>7}  {'ok ' if ok else 'RED'} {s}")
    if not a.keep:
        for f in out.glob('*.png'):
            f.unlink()
        out.rmdir()
    print(f"\n{len(rows) - red} ok / {red} red")
    sys.exit(1 if red else 0)


if __name__ == '__main__':
    main()
