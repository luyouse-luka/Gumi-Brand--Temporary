#!/usr/bin/env python3
"""What the :has() clearance does to LIVE, without pushing anything.

  python3 tools/r102live.py --password 1234

Serves the local customstyle.css in place of the theme's via page.route, then
compares every module's padding-bottom against the same page unrouted. Anything
that moves is a module whose reserve the DOM does not justify -- either a stale
hard-coded one (good riddance) or an --edge-top boundary the selector cannot see
(must be migrated in the same round).
"""
import argparse, pathlib, sys
from playwright.sync_api import sync_playwright

CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
CSS = pathlib.Path('/home/ly/project/Gumi-Brand/assets/customstyle.css')
LIVE = 'https://gumi.com.au'
PAGES = {'index': '/', 'product': '/products/superfood-greens-gummies',
         'science': '/pages/science', 'reviews': '/pages/reviews',
         'how-gumi-works': '/pages/how-gumi-works', 'our-story': '/pages/our-story',
         'faq': '/pages/faq', 'get-in-touch': '/pages/get-in-touch',
         'referral': '/pages/referral', 'privacy-policy': '/pages/privacy-policy',
         'shipping': '/pages/shipping'}
PROBE = """() => {
  const out = {};
  document.querySelectorAll('section, .gb-footer-cta-wrap, .gb-footer-wrap').forEach((el, i) => {
    const cls = [...el.classList].filter(c => c.startsWith('gb-')).join('.');
    if (!cls) return;
    const w = el.querySelector(':scope > .gb-scallop');
    out[`${i}|${cls}`] = [getComputedStyle(el).paddingBottom,
      w ? [...w.classList].filter(c => c.startsWith('gb-scallop--')).join(' ') : '-'];
  });
  return out;
}"""

ap = argparse.ArgumentParser(); ap.add_argument('--password', required=True); a = ap.parse_args()
css = CSS.read_text(encoding='utf-8')
ok = red = 0
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=CHROME)
    ctx = b.new_context(viewport={'width': 1440, 'height': 900})
    ctx.request.post(LIVE + '/password', form={
        'form_type': 'storefront_password', 'utf8': '✓', 'password': a.password})
    if not any(c['name'] == '_shopify_essential' for c in ctx.cookies()):
        sys.exit('storefront password rejected')
    plain, routed = {}, {}
    pg = ctx.new_page()
    for name, path in PAGES.items():
        pg.goto(LIVE + path, wait_until='domcontentloaded', timeout=90000)
        pg.wait_for_timeout(600)
        plain[name] = pg.evaluate(PROBE)
        if not plain[name]: sys.exit(f'ABORT {name}: nothing rendered')
    pg.close()
    pg = ctx.new_page()
    pg.route('**/customstyle.css*', lambda r: r.fulfill(status=200,
             content_type='text/css', body=css))
    for name, path in PAGES.items():
        pg.goto(LIVE + path, wait_until='domcontentloaded', timeout=90000)
        pg.wait_for_timeout(600)
        routed[name] = pg.evaluate(PROBE)
    b.close()

print('modules whose padding-bottom moves under the new CSS:\n')
for name in PAGES:
    o, n = plain[name], routed[name]
    moved = [(k, o[k], n.get(k)) for k in o if n.get(k) and o[k][0] != n[k][0]]
    if not moved:
        ok += 1; print(f'  ok   {name:16} nothing moves'); continue
    for k, ov, nv in moved:
        red += 1
        print(f'  MOVE {name:16} {k.split("|")[1]:34} {ov[0]:>11} -> {nv[0]:<11} wave={ov[1] or "-"}')
print(f'\n{ok} pages unchanged / {red} modules move')
