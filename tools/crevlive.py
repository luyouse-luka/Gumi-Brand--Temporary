#!/usr/bin/env python3
"""gb-crev on the storefront -- what the static judge structurally cannot see.

  python3 tools/crevlive.py --password 1234
  python3 tools/crevlive.py --password 1234 --strip   # inverted: must go RED

Named after the module, not a round (same reason as crevcheck.py).

⚠ Why this file exists at all: crevcheck.py's header used to say "gb-app-section
has no liquid on live, so there is nothing to probe there yet". That stopped
being true on 2026-09-08, when the other team rebuilt the section for real and
reused our whole gb-crev class set. The very first live-only defect showed up
the same day and the static build could never have caught it:

Horizon ships `img { width: 100%; height: auto }`. We size .gb-crev__stars img
and .gb-crev-card__rating img with `flex: none` only -- no width -- so on the
storefront the theme's rule wins. The live star.svg carries a viewBox and no
width/height, so its intrinsic size falls back to 150, the 100% resolves against
the flex box, and each star measured 1500x1500 (10533px of section). The static
build's own star file has real dimensions, which is exactly why it looked fine.

So: any px this file asserts is a size the STATIC build gets for free from the
file itself, and the live build only gets because we wrote it down.
"""
import argparse

from playwright.sync_api import sync_playwright

CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
LIVE = 'https://gumi.com.au'
PDP = '/products/superfood-greens-gummies'

# Board sizes, flat across every breakpoint (measured on the static build at
# 390 / 575 / 767 / 768 / 900 / 1024 / 1200 / 1280 / 1281 / 1440 -- all identical).
STAR_LG = 32.0
STAR_SM = 20.0
WIDTHS = [390, 768, 1440]

PROBE = """() => {
  const box = s => { const e = document.querySelector(s); if (!e) return null;
    const r = e.getBoundingClientRect(); return [+r.width.toFixed(1), +r.height.toFixed(1)]; };
  const sec = document.querySelector('.gb-app-section');
  return {
    starsImg: box('.gb-crev__stars img'),
    stars:    box('.gb-crev__stars'),
    ratingImg:box('.gb-crev-card__rating img'),
    rating:   box('.gb-crev-card__rating'),
    head:     getComputedStyle(document.querySelector('.gb-crev__head') || document.body).maxWidth,
    list:     getComputedStyle(document.querySelector('.gb-crev__list') || document.body).maxWidth,
    nCards:   document.querySelectorAll('.gb-crev-card').length,
    secH:     sec ? Math.round(sec.getBoundingClientRect().height) : null,
  };
}"""

# Put the theme's rule back on the images, inline. Deleting CSSOM rules is not an
# option here for the same reason as r93: it fails silently.
STRIP = """() => {
  let n = 0;
  for (const i of document.querySelectorAll('.gb-crev__stars img, .gb-crev-card__rating img')) {
    i.style.width = '100%'; i.style.height = 'auto'; n++;
  }
  return n;
}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--password', required=True)
    ap.add_argument('--strip', action='store_true')
    a = ap.parse_args()

    ok = red = 0

    def check(tag, got, want, tol=0.6):
        nonlocal ok, red
        if isinstance(want, (int, float)) and isinstance(got, (int, float)):
            good = abs(got - want) <= tol
        else:
            good = got == want
        ok, red = ok + good, red + (not good)
        print(f"  {'ok  ' if good else 'RED '} {tag}" + ('' if good else f"   got={got!r} want={want!r}"))

    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=CHROME)
        ctx = br.new_context(viewport={'width': 1440, 'height': 900})
        ctx.request.post(LIVE + '/password', form={
            'form_type': 'storefront_password', 'utf8': '✓', 'password': a.password})
        if not any(c['name'] == '_shopify_essential' for c in ctx.cookies()):
            raise SystemExit('storefront password rejected (no _shopify_essential)')
        pg = ctx.new_page()
        touched = 0
        for w in WIDTHS:
            pg.set_viewport_size({'width': w, 'height': 900})
            pg.goto(LIVE + PDP, wait_until='domcontentloaded')
            pg.wait_for_timeout(900)
            if a.strip:
                touched += pg.evaluate(STRIP)
                pg.wait_for_timeout(150)
            d = pg.evaluate(PROBE)
            print(f'\n== live {w} ==')
            if d['starsImg'] is None:
                check(f'{w} section present', False, True)
                continue
            check(f'{w} summary star is {STAR_LG:.0f}', d['starsImg'][0], STAR_LG)
            check(f'{w} summary star square', d['starsImg'][1], STAR_LG)
            check(f'{w} five stars = {STAR_LG * 5:.0f} wide', d['stars'][0], STAR_LG * 5)
            check(f'{w} card star is {STAR_SM:.0f}', d['ratingImg'][0], STAR_SM)
            check(f'{w} card star square', d['ratingImg'][1], STAR_SM)
            check(f'{w} five card stars = {STAR_SM * 5:.0f} wide', d['rating'][0], STAR_SM * 5)
            check(f'{w} head cap 736', d['head'], '736px')
            check(f'{w} list cap 1056', d['list'], '1056px')
            # A blown-up star inflates the whole block; this is the symptom the
            # merchant actually sees, so assert it directly rather than by proxy.
            check(f'{w} section under 4000px tall', d['secH'] < 4000, True)

        # .is-voted only exists live (the inline script adds it). Read it after
        # the transition settles -- getComputedStyle mid-transition returns the
        # start value and this assertion would be permanently red.
        pg.set_viewport_size({'width': 1440, 'height': 900})
        pg.goto(LIVE + PDP, wait_until='domcontentloaded')
        pg.wait_for_timeout(800)
        print('\n== voted state ==')
        base = pg.evaluate("getComputedStyle(document.querySelector('.gb-crev-card__vote')).color")
        pg.evaluate("document.querySelector('.gb-crev-card__vote').classList.add('is-voted')")
        pg.wait_for_timeout(450)
        voted = pg.evaluate("getComputedStyle(document.querySelector('.gb-crev-card__vote')).color")
        stroke = pg.evaluate("getComputedStyle(document.querySelector('.gb-crev-card__vote svg')).strokeWidth")
        check('resting is gray-600', base, 'rgb(102, 102, 102)')
        check('voted is green', voted, 'rgb(0, 86, 53)')
        check('voted thickens the icon', stroke, '2px')

        if a.strip:
            print('\n== strip liveness ==')
            check('strip touched images', touched > 0, True)
        br.close()

    print(f'\n{ok} ok / {red} red')
    raise SystemExit(1 if red and not a.strip else 0)


if __name__ == '__main__':
    main()
