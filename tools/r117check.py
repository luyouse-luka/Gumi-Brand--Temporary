#!/usr/bin/env python3
"""Round 117, static side.

  python3 tools/r117check.py

1  $build.
2  Snapchat sits between Instagram and TikTok on every page, matching live.
3  Empty-cart checkout: not-allowed on the BAR (the button keeps
   pointer-events:none, which is what blocks the click -- and what would
   swallow a cursor written on the button itself).
4  --page-width redeclared for /collections/all and /404.
5  cartDrawer only acts on the split state.
6  First-pass reveal order: the banner lands before what sits under it.
"""
import pathlib, re, sys
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
ok = red = 0


def grade(cond, label, detail=''):
    global ok, red
    if cond:
        ok += 1
        print(f'  ok   {label}   {detail}')
    else:
        red += 1
        print(f'  RED  {label}   {detail}')


css = (ROOT / 'assets/customstyle.css').read_text(encoding='utf-8')
js = (ROOT / 'assets/main.js').read_text(encoding='utf-8')

print('--- 1. $build ---')
# NOT pinned to r117: a literal build token turns this red on every later round
# and reads as a regression. What matters on a re-run is that the sheet is at
# least this round's build, not that it is exactly it.
import re as _re
_m = _re.search(r'--build: "(\d{8})-r(\d+)"', css)
grade(bool(_m) and (int(_m.group(1)), int(_m.group(2))) >= (20260908, 117),
      '$build is r117 or later', _m.group(0) if _m else 'no --build')

print('--- 2. Snapchat on every page, in live order ---')
pages = [p for p in sorted(ROOT.glob('*.html')) if p.name != 'font-check.html']
grade(len(pages) == 12, '12 static pages', str(len(pages)))
order_ok = missing = 0
for p in pages:
    t = p.read_text(encoding='utf-8')
    labels = re.findall(r'gb-footer__social-link" href="#" aria-label="(\w+)"', t)
    if labels == ['Facebook', 'Instagram', 'Snapchat', 'TikTok']:
        order_ok += 1
    else:
        missing += 1
        print(f'       {p.name}: {labels}')
grade(order_ok == 12, 'all 12 in order Facebook/Instagram/Snapchat/TikTok',
      f'{order_ok} ok, {missing} off')
grade(all('aria-label="Snapchat" title="Snapchat"' in p.read_text(encoding='utf-8')
          for p in pages), 'each Snapchat link carries title too (r111 rule)')
grade(all('fill="currentColor"' in re.search(
        r'aria-label="Snapchat".*?</a>', p.read_text(encoding='utf-8'), re.S).group(0)
        for p in pages), 'icon inherits colour like its peers (no baked #B5ED61)')

print('--- 3/4. css rules ---')
grade('.gb-cart.is-empty .gb-cart__bar {\n  cursor: not-allowed;' in css,
      'not-allowed is on the bar, not the button')
m = re.search(r'\.gb-cart\.is-empty \.gb-cart__checkout \{(.*?)\}', css, re.S)
grade(bool(m) and 'pointer-events: none' in m.group(1),
      'the button keeps pointer-events:none (that is what blocks the click)')
# 1440, not 1280: Horizon's --page-width includes both margins.
grade(css.count('--page-width: 1440px;') == 2,
      '--page-width redeclared twice, at the shell width incl. margins',
      f"count={css.count('--page-width: 1440px;')}, "
      f"bare-content mistake={css.count('--page-width: 1280px;')}")

print('--- 5. cartDrawer guards ---')
for frag, why in (('!dialog.open || host.hasAttribute("open")', 'acts on the split state only'),
                  ('customElements.whenDefined("theme-drawer")', 'waits for the upgrade'),
                  ('["cartDrawer", cartDrawer]', 'registered in the init list')):
    grade(frag in js, f'cartDrawer: {why}')

print('--- 6. first-pass reveal order (390 x 1600) ---')
WATCH = """() => new Promise(res => {
  const t0 = performance.now();
  const els = [...document.querySelectorAll('.wowo')].map(e => ({
    e, inBanner: !!e.closest('.gb-hero, .gb-page-hero'),
    cls: (e.className||'').toString().replace(/\\s+/g,' ').slice(0, 34), at: null}));
  const tick = () => {
    let pending = 0;
    for (const o of els) {
      if (o.at === null) {
        if (parseFloat(getComputedStyle(o.e).opacity) > 0.98)
          o.at = Math.round(performance.now() - t0);
        else pending++;
      }
    }
    if (pending && performance.now() - t0 < 5000) requestAnimationFrame(tick);
    else res(els.map(o => ({inBanner: o.inBanner, cls: o.cls, at: o.at})));
  };
  requestAnimationFrame(tick);
})"""
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=CHROME)
    pg = b.new_context(viewport={'width': 390, 'height': 1600}).new_page()
    pg.goto((ROOT / 'index.html').as_uri(), wait_until='commit', timeout=60000)
    rows = pg.evaluate(WATCH)
    inb = [r['at'] for r in rows if r['inBanner'] and r['at'] is not None]
    out = [r['at'] for r in rows if not r['inBanner'] and r['at'] is not None]
    grade(len(inb) >= 2, 'banner has revealed elements to grade', f'{len(inb)} in banner')
    grade(len(out) >= 1, 'and something below it is in the first pass too',
          f'{len(out)} below: ' + str([r["cls"][:26] for r in rows
                                       if not r["inBanner"] and r["at"] is not None][:3]))
    if inb and out:
        grade(max(inb) <= min(out),
              'the whole banner lands before anything under it',
              f'banner last {max(inb)}ms vs below first {min(out)}ms')
        grade(min(out) - max(inb) >= 250,
              'and with a clear beat between them (>=250ms)',
              f'gap {min(out) - max(inb)}ms')
    b.close()

print(f'\n{ok} ok / {red} red')
sys.exit(1 if red else 0)
