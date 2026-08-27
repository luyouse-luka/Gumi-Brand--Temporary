#!/usr/bin/env python3
"""Catch copy clipped by a stale line mask during the resize debounce.

    python3 tools/masktrap.py [page]

.gb-line-mask is overflow:hidden and is rebuilt only 200ms after the last
resize event. While a visitor drags the window narrower, every mask still holds
the wrap points of the old width -- if the copy inside now needs more lines than
the mask was built for, the extra lines are clipped and the text is simply gone
until the drag stops. Measures scrollHeight against clientHeight per mask.
"""
import os, sys
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = os.path.expanduser("~/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome")
PAGE = sys.argv[1] if len(sys.argv) > 1 else "index.html"

SCROLL = """async () => {
  const step = window.innerHeight * 0.8;
  for (let y = 0; y < document.body.scrollHeight; y += step) {
    window.scrollTo(0, y);
    await new Promise(r => setTimeout(r, 60));
  }
  window.scrollTo(0, 0);
}"""

CLIPPED = """() => {
  const out = [];
  for (const m of document.querySelectorAll('.gb-line-mask')) {
    if (m.scrollHeight > m.clientHeight + 1) {
      const host = m.closest('[data-line-reveal]');
      out.push({ host: (host?.className || '').toString().split(' ').filter(c => c.startsWith('gb-'))[0] || '?',
                 clip: +(m.scrollHeight - m.clientHeight).toFixed(1),
                 text: (m.textContent || '').replace(/\\s+/g, ' ').trim().slice(0, 44) });
    }
  }
  return out;
}"""

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME)
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto("file://" + os.path.join(ROOT, PAGE))
    pg.wait_for_timeout(1500)
    pg.evaluate("document.fonts.ready")
    pg.wait_for_timeout(400)
    pg.evaluate(SCROLL)
    pg.wait_for_timeout(1000)

    for w in (1200, 900, 700, 500, 390):
        pg.set_viewport_size({"width": w, "height": 844})
        pg.wait_for_timeout(80)                 # inside the 200ms debounce
        mid = pg.evaluate(CLIPPED)
        pg.wait_for_timeout(600)                # after the rebuild
        after = pg.evaluate(CLIPPED)
        print(f"--- {w}px   during drag: {len(mid)} clipped   after rebuild: {len(after)} clipped")
        for r in mid[:4]:
            print(f"      mid   {r['host']:26s} -{r['clip']:.0f}px  {r['text']!r}")
        for r in after[:4]:
            print(f"      AFTER {r['host']:26s} -{r['clip']:.0f}px  {r['text']!r}")
    b.close()
