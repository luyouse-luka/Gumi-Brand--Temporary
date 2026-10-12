#!/usr/bin/env python3
"""padding-bottom snapshot for every module that reserves room for a wave.

  python3 tools/r102pad.py --save before.json
  python3 tools/r102pad.py --cmp  before.json

Switching the 22 hard-coded reserves to :has()-driven ones must not move a single
pixel while the built-in waves are still in place. Compares computed values on the
static build across every breakpoint tier.
"""
import argparse, json, pathlib, sys
from playwright.sync_api import sync_playwright

CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
ROOT = pathlib.Path('/home/ly/project/Gumi-Brand')
PAGES = ['index', 'pdp', 'science', 'reviews', 'how-gumi-works', 'our-story',
         'faq', 'get-in-touch', 'referral', 'privacy-policy', 'shipping']
WIDTHS = [1440, 1280, 991, 768, 575, 390]
PROBE = """() => {
  const out = {};
  document.querySelectorAll('section, .gb-footer-cta-wrap, .gb-footer-wrap').forEach((el, i) => {
    const cls = [...el.classList].filter(c => c.startsWith('gb-')).join('.');
    if (!cls) return;
    const cs = getComputedStyle(el);
    out[`${i}|${cls}`] = [cs.paddingBottom, cs.paddingTop, cs.marginBottom,
                          Math.round(el.getBoundingClientRect().height * 10) / 10];
  });
  return out;
}"""

ap = argparse.ArgumentParser()
ap.add_argument('--save'); ap.add_argument('--cmp')
a = ap.parse_args()
if not (a.save or a.cmp): sys.exit('need --save or --cmp')

snap = {}
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=CHROME)
    pg = b.new_page()
    for name in PAGES:
        pg.goto((ROOT / f'{name}.html').as_uri(), wait_until='domcontentloaded')
        for w in WIDTHS:
            pg.set_viewport_size({'width': w, 'height': 900})
            pg.wait_for_timeout(80)
            snap[f'{name}@{w}'] = pg.evaluate(PROBE)
    b.close()

if a.save:
    json.dump(snap, open(a.save, 'w'), indent=0)
    n = sum(len(v) for v in snap.values())
    print(f'saved {a.save}: {len(snap)} page/width combos, {n} elements')
    sys.exit(0)

old = json.load(open(a.cmp))
ok = red = 0
for key in sorted(set(old) | set(snap)):
    o, n = old.get(key, {}), snap.get(key, {})
    for el in sorted(set(o) | set(n)):
        if o.get(el) == n.get(el): ok += 1
        else:
            red += 1
            print(f'  DIFF {key:26} {el:44}\n       was {o.get(el)}\n       now {n.get(el)}')
print(f'\n{ok} identical / {red} changed')
sys.exit(1 if red else 0)
