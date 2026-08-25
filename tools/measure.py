#!/usr/bin/env python3
"""Ad-hoc probe: computed styles + rects for selectors at a given width.

    python3 tools/measure.py index.html 1440 .gb-promo-card__body .gb-promo-card__art
    python3 tools/measure.py index.html 1440 --props padding,flex,width .gb-promo-card__body
"""
import os, sys, json
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = os.path.expanduser("~/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome")

PROBE = """([sels, props]) => {
  const out = [];
  for (const s of sels) {
    document.querySelectorAll(s).forEach((el, i) => {
      const cs = getComputedStyle(el), r = el.getBoundingClientRect();
      const o = { sel: s, i, rect: [+r.x.toFixed(2), +r.y.toFixed(2), +r.width.toFixed(2), +r.height.toFixed(2)] };
      for (const p of props) o[p] = cs.getPropertyValue(p);
      out.push(o);
    });
  }
  return out;
}"""

DEFAULT = ["display", "padding", "margin", "gap", "font-size", "line-height", "letter-spacing"]

def main():
    args = sys.argv[1:]
    props = DEFAULT
    if "--props" in args:
        k = args.index("--props"); props = args[k + 1].split(","); del args[k:k + 2]
    page = args[0]; width = int(args[1]); sels = args[2:]
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=CHROME)
        pg = br.new_page(viewport={"width": width, "height": 1000})
        pg.goto("file://" + os.path.join(ROOT, page))
        pg.evaluate("() => document.fonts.ready")
        pg.wait_for_timeout(250)
        for o in pg.evaluate(PROBE, [sels, props]):
            print(json.dumps(o, ensure_ascii=False))
        br.close()

main()
