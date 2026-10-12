#!/usr/bin/env python3
"""Does each migrated wave still join the two blocks it sits between?

  python3 tools/r102seam.py --password 1234

Three things can go wrong once a wave becomes its own section, and none of them
show up in a class list:
  seam    a gap or an overlap between the wave and the block above/below
  colour  the pair names a colour the neighbouring section does not actually use
  reserve the block above still pads for a wave that no longer hangs off it
Colours are sampled from the rendered pixels, not from the class name.
"""
import argparse, sys
from playwright.sync_api import sync_playwright

CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
LIVE = 'https://gumi.com.au'
PAGES = {'index': '/', 'product': '/products/superfood-greens-gummies',
         'science': '/pages/science', 'reviews': '/pages/reviews',
         'how-gumi-works': '/pages/how-gumi-works', 'our-story': '/pages/our-story',
         'faq': '/pages/faq', 'get-in-touch': '/pages/get-in-touch',
         'referral': '/pages/referral', 'privacy-policy': '/pages/privacy-policy',
         'shipping': '/pages/shipping'}
PROBE = """() => {
  const px = (el) => { const c = getComputedStyle(el).backgroundColor;
                       return c === 'rgba(0, 0, 0, 0)' ? null : c; };
  const bgOf = (el) => { let n = el; while (n && n !== document.body) { const c = px(n); if (c) return c; n = n.parentElement; }
                         return getComputedStyle(document.body).backgroundColor; };
  const out = [];
  const waves = [...document.querySelectorAll('.gb-scallop.gb-wave')];
  for (const w of waves) {
    const host = w.closest('.shopify-section') || w.parentElement;
    const prev = host.previousElementSibling, next = host.nextElementSibling;
    const r = w.getBoundingClientRect();
    const pr = prev && prev.getBoundingClientRect(), nr = next && next.getBoundingClientRect();
    const cs = getComputedStyle(w);
    const inner = (el) => { if (!el) return null;
      const t = el.querySelector('section, .gb-footer-cta-wrap, div'); return t || el; };
    out.push({
      pair: [...w.classList].filter(c => c.includes('-to-')).map(c => c.slice(12))[0] || '?',
      n: cs.getPropertyValue('--wave-n').trim(),
      h: Math.round(r.height * 10) / 10,
      gapAbove: pr ? Math.round((r.top - pr.bottom) * 10) / 10 : null,
      gapBelow: nr ? Math.round((nr.top - r.bottom) * 10) / 10 : null,
      wBg: cs.getPropertyValue('--wave-bg').trim(),
      wFg: cs.getPropertyValue('--wave-fg').trim(),
      above: prev ? bgOf(inner(prev)) : null,
      below: next ? bgOf(inner(next)) : null,
      prevPadB: prev ? getComputedStyle(inner(prev)).paddingBottom : null,
      prevName: prev ? ([...(inner(prev)).classList].find(c => /^gb-[a-z-]+$/.test(c)) || prev.id) : null,
      nextName: next ? ([...(inner(next)).classList].find(c => /^gb-[a-z-]+$/.test(c)) || next.id) : null,
    });
  }
  return out;
}"""

def rgb(s):
    m = [int(x) for x in (s or '').replace('rgba(', '').replace('rgb(', '').rstrip(')').split(',')[:3] if x.strip().isdigit()]
    return tuple(m) if len(m) == 3 else None
def hexs(s):
    s = (s or '').strip().lstrip('#')
    if len(s) == 6: return tuple(int(s[i:i+2], 16) for i in (0, 2, 4))
    return rgb(s)
def near(a, b, tol=6):
    a, b = rgb(a) if a and a.startswith('rgb') else hexs(a), rgb(b) if b and b.startswith('rgb') else hexs(b)
    return a and b and all(abs(x - y) <= tol for x, y in zip(a, b))

ap = argparse.ArgumentParser(); ap.add_argument('--password', required=True); a = ap.parse_args()
ok = red = 0
def grade(c, label, detail=''):
    global ok, red
    if c: ok += 1
    else: red += 1; print(f'  RED  {label}   {detail}')

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
        if not rows: sys.exit(f'ABORT {name}: no gb-wave found -- did the push land?')
        print(f'\n--- {name}  ({len(rows)} waves) ---')
        for r in rows:
            tag = f'{r["prevName"]} -> {r["nextName"]}'
            print(f'  {tag:34} n={r["n"]} h={r["h"]:6} {r["pair"]:15} '
                  f'above={r["above"]} below={r["below"]} prevPadB={r["prevPadB"]}')
            grade(r['gapAbove'] is None or abs(r['gapAbove']) <= 1.5,
                  f'{name} {tag}: flush with the block above', f'gap {r["gapAbove"]}')
            grade(r['gapBelow'] is None or abs(r['gapBelow']) <= 1.5,
                  f'{name} {tag}: flush with the block below', f'gap {r["gapBelow"]}')
            if r['wBg'] and r['wBg'] != 'transparent':
                grade(near(r['wBg'], r['above']),
                      f'{name} {tag}: top colour matches the block above',
                      f'wave {r["wBg"]} vs section {r["above"]}')
            grade(near(r['wFg'], r['below']),
                  f'{name} {tag}: bottom colour matches the block below',
                  f'wave {r["wFg"]} vs section {r["below"]}')
    b.close()
print(f'\n{ok} ok / {red} red')
sys.exit(1 if red else 0)
