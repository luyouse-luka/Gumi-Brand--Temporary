#!/usr/bin/env python3
"""Dump the laid-out geometry of a page at one width, as a tree, for board diffing.

    python3 tools/mobgeo.py [page] [width]

Entrance effects are forced to their end state first: .wowo, [data-line-reveal]
and .gb-float-art all ship a transform, and getBoundingClientRect reports the
transformed box, so an un-neutralised page measures wherever the animation
happens to be. Layout boxes are unaffected by transform, so neutralising them
is safe here (it is NOT safe for screenshots -- see kill-animations-blanks-reveal-blocks).
"""
import os, sys, json
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = os.path.expanduser("~/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome")
PAGE = sys.argv[1] if len(sys.argv) > 1 else "index.html"
WIDTH = int(sys.argv[2]) if len(sys.argv) > 2 else 390

SETTLE = """
.wowo, .gb-float-art, [data-line-reveal], .gb-line-mask__inner, .gb-ink-halo {
  opacity: 1 !important; transform: none !important; animation: none !important;
}
"""

DUMP = """() => {
  const out = [];
  const sy = window.scrollY, sx = window.scrollX;
  const walk = (el, dep) => {
    const cls = (el.className || '').toString().trim();
    const gb  = cls.split(/\\s+/).filter(c => c.startsWith('gb-'));
    const cs  = getComputedStyle(el);
    const shown = cs.display !== 'none' && cs.visibility !== 'hidden';
    if (gb.length && shown) {
      const b = el.getBoundingClientRect();
      // own text only: direct text nodes, so a wrapper does not echo its children
      let own = '';
      for (const n of el.childNodes) if (n.nodeType === 3) own += n.nodeValue;
      own = own.replace(/\\s+/g, ' ').trim();
      const st = { fs: cs.fontSize, lh: cs.lineHeight, ls: cs.letterSpacing,
                   fw: cs.fontWeight, gap: cs.gap, mt: cs.marginTop, mb: cs.marginBottom,
                   ml: cs.marginLeft, pt: cs.paddingTop, pb: cs.paddingBottom,
                   pl: cs.paddingLeft, pr: cs.paddingRight, disp: cs.display };
      out.push({ dep, tag: el.tagName.toLowerCase(), cls: gb.join(' '),
                 x: b.x + sx, y: b.y + sy, w: b.width, h: b.height, txt: own.slice(0, 60), st });
      dep += 1;
    }
    for (const c of el.children) walk(c, dep);
  };
  walk(document.body, 0);
  return out;
}"""

with sync_playwright() as p:
    br = p.chromium.launch(executable_path=CHROME)
    pg = br.new_page(viewport={"width": WIDTH, "height": 844})
    pg.goto("file://" + os.path.join(ROOT, PAGE))
    pg.add_style_tag(content=SETTLE)
    pg.wait_for_timeout(1200)
    pg.evaluate("document.fonts.ready")
    pg.wait_for_timeout(400)
    rows = pg.evaluate(DUMP)
    br.close()

for r in rows:
    st = r["st"]
    extra = f" | fs={st['fs']} lh={st['lh']} ls={st['ls']} fw={st['fw']}" if r["txt"] else ""
    if st["gap"] not in ("normal", "0px"):
        extra += f" | gap={st['gap']}"
    for k, lab in (("mt", "mt"), ("mb", "mb"), ("ml", "ml")):
        if st[k] not in ("0px",):
            extra += f" | {lab}={st[k]}"
    pads = (st["pt"], st["pr"], st["pb"], st["pl"])
    if any(v != "0px" for v in pads):
        extra += f" | pad={pads}"
    txt = f" :: {r['txt']!r}" if r["txt"] else ""
    print(f"{'  '*r['dep']}{r['tag']:6s} {r['cls'][:44]:46s} "
          f"x={r['x']:7.2f} y={r['y']:9.2f} w={r['w']:7.2f} h={r['h']:7.2f}{extra}{txt}")
