#!/usr/bin/env python3
"""Footer links have to visibly change on hover.

  python3 tools/footerhover.py
  python3 tools/footerhover.py --live --password 1234

r86 dropped the sliding underline from all four link users because "each already
changes colour". That held on the cream header; in the footer the change was
$c-lime-100 -> $c-white on $c-green-900, i.e. #f4fce7 -> #ffffff -- an RGB
distance of 26.6, which reads as no hover at all. The threshold below is set at
60 precisely so that pair fails it and the new one (148.5) passes.
"""
import argparse, math, pathlib, re, sys
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
LIVE = 'https://gumi.com.au'
MIN_DIST = 60.0
LIME = (181, 237, 97)          # $c-lime #b5ed61
ok = red = 0


def grade(cond, label, detail=''):
    global ok, red
    if cond:
        ok += 1
    else:
        red += 1
        print(f'  RED  {label}   {detail}')


def rgb(s):
    m = re.findall(r'[\d.]+', s or '')
    return tuple(float(x) for x in m[:3]) if len(m) >= 3 else None


def dist(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b))) if a and b else 0.0


READ = """e => { const s = getComputedStyle(e);
  return {color: s.color, bg: s.backgroundColor, op: s.opacity,
          td: s.textDecorationLine, tp: s.transitionProperty,
          cls: (typeof e.className === 'string' ? e.className : ''),
          txt: (e.textContent || e.getAttribute('aria-label') || '').trim().slice(0, 18)}; }"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--live', action='store_true')
    ap.add_argument('--password')
    a = ap.parse_args()
    if a.live and not a.password:
        sys.exit('--live needs --password')
    url = (LIVE + '/') if a.live else (ROOT / 'index.html').as_uri()

    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME)
        ctx = b.new_context(viewport={'width': 1440, 'height': 900})
        if a.live:
            ctx.request.post(LIVE + '/password', form={
                'form_type': 'storefront_password', 'utf8': '✓', 'password': a.password})
        pg = ctx.new_page()
        pg.goto(url, wait_until='domcontentloaded', timeout=90000)
        pg.wait_for_timeout(1500)
        # the promo modal's overlay swallows every hover on the page
        pg.evaluate("() => { const m = document.getElementById('promo-modal'); if (m) m.remove(); }")
        grade(pg.evaluate("matchMedia('(hover: hover)').matches"),
              'the run is in a hover-capable context (else @include hover is dead)')

        els = pg.query_selector_all('.gb-footer a, .gb-footer button')
        grade(len(els) >= 15, 'found the footer controls', f'{len(els)}')
        for el in els:
            before = el.evaluate(READ)
            el.scroll_into_view_if_needed()
            el.hover(timeout=5000)
            pg.wait_for_timeout(320)
            after = el.evaluate(READ)
            first = before['cls'].split(' ')[0] or before['cls']
            moved = (before['color'] != after['color'] or before['bg'] != after['bg']
                     or before['op'] != after['op'] or before['td'] != after['td'])
            grade(moved, f"{first} '{before['txt']}' reacts to hover at all",
                  f"{before['color']} / {before['bg']} unchanged")
            d = dist(rgb(before['color']), rgb(after['color']))
            if 'gb-footer__link' in before['cls'] or first == 'gb-footer__legal-link' \
                    or (el.evaluate("e => !!e.closest('.gb-footer__legal-links')")
                        and before['cls'] == ''):
                grade(rgb(after['color']) == LIME,
                      f"{first} '{before['txt']}' hovers to the brand lime", after['color'])
                grade(d >= MIN_DIST,
                      f"{first} '{before['txt']}' shift is visible (>= {MIN_DIST})",
                      f'{d:.1f}')
                grade('color' in before['tp'],
                      f"{first} '{before['txt']}' transitions that colour", before['tp'])
                print(f"  {first:<26} {before['txt']:<18} {before['color']} -> "
                      f"{after['color']}   d={d:.1f}")
        b.close()
    print(f'\n{ok} ok / {red} red' + ('   [LIVE]' if a.live else '   [static]'))
    return 1 if red else 0


sys.exit(main())
