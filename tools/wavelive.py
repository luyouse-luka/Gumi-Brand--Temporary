#!/usr/bin/env python3
"""Live check for the CTA wave on the templates that have no design board, plus the star icon.

  python3 tools/wavelive.py --password 1234

wavemap.py walks the 11 designed pages; these nine templates (404, blog,
article, collection, list-collections, page, contact, search) never had a wave
until now, so they need their own probe. Also reads the star <img> back, since
the asset changed under a url Shopify fingerprints for us.

⚠ Never point this at /cart/* -- that path trips a Cloudflare challenge that
kills the whole session (memory: shopify-cart-paths-trip-cloudflare-challenge).
"""
import argparse, sys
from playwright.sync_api import sync_playwright

CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
LIVE = 'https://gumi.com.au'
LIME = 'rgb(181, 237, 97)'
PAGES = {
    '404': '/pages/this-page-does-not-exist-probe',
    'blog': '/blogs/news',
    'collection': '/collections/all',
    'list-collections': '/collections',
    'search': '/search?q=gummies',
}
PROBE = """() => {
  const cta = document.querySelector('.gb-footer-cta, .gb-footer-cta-wrap');
  if (!cta) return {err: 'no footer cta'};
  // the wave section sits immediately above the CTA's shopify-section wrapper
  const host = cta.closest('.shopify-section') || cta;
  let prev = host.previousElementSibling;
  const w = prev && prev.querySelector('.gb-wave');
  if (!w) return {err: 'no gb-wave above the CTA', prevClass: prev ? prev.className : null};
  const cs = getComputedStyle(w);
  const r = w.getBoundingClientRect();
  return {
    h: Math.round(r.height * 10) / 10,
    fg: cs.getPropertyValue('--wave-fg').trim(),
    bg: cs.getPropertyValue('--wave-bg').trim(),
    cls: w.className,
  };
}"""
STAR = """() => {
  const im = document.querySelector('.gb-crev__stars img, .gb-crev-card__stars img');
  if (!im) return {err: 'no star img'};
  return {src: im.getAttribute('src'), w: im.width, h: im.height,
          natural: [im.naturalWidth, im.naturalHeight], complete: im.complete};
}"""

ap = argparse.ArgumentParser()
ap.add_argument('--password', required=True)
a = ap.parse_args()
ok = red = 0

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=CHROME)
    ctx = b.new_context(viewport={'width': 1440, 'height': 900})
    ctx.request.post(LIVE + '/password', form={
        'form_type': 'storefront_password', 'utf8': '✓', 'password': a.password})
    if not any(c['name'] == '_shopify_essential' for c in ctx.cookies()):
        sys.exit('storefront password rejected')
    pg = ctx.new_page()

    for name, path in PAGES.items():
        pg.goto(LIVE + path, wait_until='domcontentloaded', timeout=90000)
        pg.wait_for_timeout(600)
        r = pg.evaluate(PROBE)
        if r.get('err'):
            print(f'  RED {name:<20} {r["err"]}  prev={r.get("prevClass")}'); red += 1
            continue
        # the CTA wave must be small, lime below, and paint nothing above it
        good = 90 < r['h'] < 105 and r['fg'].lower() in ('#b5ed61', LIME) and \
               r['bg'] in ('transparent', 'rgba(0, 0, 0, 0)')
        print(f'  {"ok " if good else "RED"} {name:<20} h={r["h"]:<6} '
              f'above={r["bg"]:<18} below={r["fg"]}')
        ok, red = (ok + 1, red) if good else (ok, red + 1)

    # star icon, on the page that renders the review cards
    pg.goto(LIVE + '/pages/reviews', wait_until='domcontentloaded', timeout=90000)
    pg.wait_for_timeout(900)
    s = pg.evaluate(STAR)
    if s.get('err'):
        print(f'  RED star                {s["err"]}'); red += 1
    else:
        # the new asset is 25x24; the old one was 32x32 / 20x20
        good = s['complete'] and s['natural'] == [25, 24]
        print(f'  {"ok " if good else "RED"} {"star":<20} natural={s["natural"]} '
              f'rendered={s["w"]}x{s["h"]} loaded={s["complete"]}')
        print(f'      src={s["src"]}')
        ok, red = (ok + 1, red) if good else (ok, red + 1)
    b.close()

print(f'\n──────── {ok} ok / {red} red ────────')
sys.exit(0 if red == 0 else 1)
