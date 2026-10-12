#!/usr/bin/env python3
"""Where every live wave sits, and what it is -- the input to the Gumi Wave migration.

  python3 tools/wavemap.py --password 1234

For each page, walks the shopify-section list in order and reports, for every
wave found, the boundary it occupies (section above -> section below) and the
modifiers it actually carries. Read off the live DOM rather than the liquid,
because several sections hard-code a modifier the template's setting cannot show.
"""
import argparse, json, sys
from playwright.sync_api import sync_playwright

CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
LIVE = 'https://gumi.com.au'
PAGES = {
    'index': '/', 'product': '/products/superfood-greens-gummies',
    'page.science': '/pages/science', 'page.reviews': '/pages/reviews',
    'page.how-gumi-works': '/pages/how-gumi-works', 'page.our-story': '/pages/our-story',
    'page.faq': '/pages/faq', 'page.get-in-touch': '/pages/get-in-touch',
    'page.referral': '/pages/referral', 'page.privacy-policy': '/pages/privacy-policy',
    'page.shipping': '/pages/shipping',
}
PROBE = """() => {
  const rows = [];
  const secs = [...document.querySelectorAll('.shopify-section, #shopify-section-footer-group > *')];
  const nameOf = (el) => {
    const gb = [...el.querySelectorAll('[class*=gb-]')]
      .map(e => [...e.classList].find(c => /^gb-[a-z-]+$/.test(c)))
      .filter(Boolean);
    return gb[0] || el.id || el.tagName.toLowerCase();
  };
  secs.forEach((sec, i) => {
    for (const w of sec.querySelectorAll('.gb-scallop')) {
      const mods = [...w.classList].filter(c => c.startsWith('gb-scallop--')).map(c => c.slice(12));
      const r = w.getBoundingClientRect();
      rows.push({
        idx: i,
        host: nameOf(sec),
        sectionId: (sec.id || '').replace('shopify-section-', ''),
        next: secs[i + 1] ? nameOf(secs[i + 1]) : null,
        mods, h: Math.round(r.height * 10) / 10,
        top: Math.round(w.getBoundingClientRect().top + window.scrollY),
      });
    }
  });
  return rows;
}"""

ap = argparse.ArgumentParser(); ap.add_argument('--password', required=True)
ap.add_argument('--json', help='write the map here')
a = ap.parse_args()

out = {}
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
        pg.wait_for_timeout(700)
        rows = pg.evaluate(PROBE)
        if not rows:
            sys.exit(f'ABORT {name}: no waves at all -- the page did not render')
        out[name] = rows
        print(f'\n=== {name} ===')
        for r in rows:
            size = 'lg' if 'lg' in r['mods'] else 'sm'
            pos  = ('edge-top' if 'edge-top' in r['mods'] else
                    'edge' if 'edge' in r['mods'] else 'flow')
            pair = [m for m in r['mods'] if '-to-' in m or m.startswith('to-')]
            extra = [m for m in r['mods'] if m in ('down', 'bleed')]
            print(f'  [{r["idx"]:2}] {r["host"]:20} -> {str(r["next"]):20} '
                  f'{pos:9} {size} {",".join(pair) or "?":16} {",".join(extra):11} h={r["h"]}')
    b.close()
if a.json:
    open(a.json, 'w').write(json.dumps(out, indent=1))
    print(f'\nwritten {a.json}')
