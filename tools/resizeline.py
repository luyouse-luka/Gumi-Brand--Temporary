#!/usr/bin/env python3
"""Compare line-reveal wrap points between "opened at width W" and "resized to W".

    python3 tools/resizeline.py [page]

lineReveal measures offsetTop to group words into per-line masks, and re-runs on
a debounced resize. A page that only ever gets probed at a fixed viewport never
exercises that path, so a wrap point that is right on load can still be wrong
after the viewport changes -- which is what a real visitor does.
"""
import os, sys, json
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = os.path.expanduser("~/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome")
PAGE = sys.argv[1] if len(sys.argv) > 1 else "index.html"

READ = """() => {
  const out = [];
  for (const el of document.querySelectorAll('[data-line-reveal]')) {
    const masks = [...el.querySelectorAll('.gb-line-mask')];
    const lines = masks.length
      ? masks.map(m => (m.textContent || '').replace(/\\s+/g, ' ').trim())
      : [(el.textContent || '').replace(/\\s+/g, ' ').trim()];
    const b = el.getBoundingClientRect();
    const brs = el.querySelectorAll('br').length;
    const brShown = [...el.querySelectorAll('br')].filter(x => getComputedStyle(x).display !== 'none').length;
    out.push({ cls: (el.className||'').toString().split(' ').filter(c=>c.startsWith('gb-'))[0] || el.tagName,
               h: +b.height.toFixed(2), masks: masks.length, brs, brShown, lines });
  }
  return out;
}"""

SCROLL = """async () => {
  const step = window.innerHeight * 0.8;
  for (let y = 0; y < document.body.scrollHeight; y += step) {
    window.scrollTo(0, y);
    await new Promise(r => setTimeout(r, 60));
  }
  window.scrollTo(0, 0);
}"""

with sync_playwright() as p:
    br = p.chromium.launch(executable_path=CHROME)

    pg = br.new_page(viewport={"width": 390, "height": 844})
    pg.goto("file://" + os.path.join(ROOT, PAGE))
    pg.wait_for_timeout(1500)
    pg.evaluate("document.fonts.ready")
    pg.wait_for_timeout(600)
    direct = pg.evaluate(READ)
    pg.close()

    pg = br.new_page(viewport={"width": 1440, "height": 900})
    pg.goto("file://" + os.path.join(ROOT, PAGE))
    pg.wait_for_timeout(1500)
    pg.evaluate("document.fonts.ready")
    pg.wait_for_timeout(600)
    # scroll the whole page first: groupLines takes a different branch for a host
    # that already revealed (is-settled), and an unscrolled page never exercises
    # it for anything below the fold
    pg.evaluate(SCROLL)
    pg.wait_for_timeout(1200)
    pg.set_viewport_size({"width": 390, "height": 844})
    pg.wait_for_timeout(1200)          # 200ms debounce + reveal settle
    resized = pg.evaluate(READ)
    pg.close()
    br.close()

bad = 0
for a, b in zip(direct, resized):
    same = a["h"] == b["h"] and a["masks"] == b["masks"] and a["lines"] == b["lines"]
    if same:
        continue
    bad += 1
    print(f"! {a['cls']}   br={a['brs']} shown={a['brShown']}")
    print(f"    opened at 390 : h={a['h']:7.2f} masks={a['masks']}  {a['lines']}")
    print(f"    resized to 390: h={b['h']:7.2f} masks={b['masks']}  {b['lines']}")
print(f"\n{bad} of {len(direct)} [data-line-reveal] hosts differ between opened-at-390 and resized-to-390")
