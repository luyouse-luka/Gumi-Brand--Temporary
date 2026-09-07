"""R66: the play glyph is gone from the reel panel, in BOTH markup shapes.

The static pages wrap the svg in .gb-rv-panel__glyph; the live liquid still
ships it bare (docs/LIQUID-TODO-reels.md item 1). A rule hung on the wrapper
would pass here and miss on the live site, so the second pass strips the
wrapper and asserts again.
"""
import sys
from playwright.sync_api import sync_playwright

CHROME = "/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome"
PAGES = ["index", "our-story", "how-gumi-works", "pdp"]

# reproduce the live markup: unwrap .gb-rv-panel__glyph
UNWRAP = """() => {
  let n = 0;
  for (const g of document.querySelectorAll('.gb-rv-panel__glyph')) {
    const p = g.parentNode;
    while (g.firstChild) p.insertBefore(g.firstChild, g);
    g.remove(); n++;
  }
  return n;
}"""

PROBE = """() => {
  const box = document.querySelector('.gb-rv-panel__video');
  if (!box) return {missing: true};
  const svgs = [...box.querySelectorAll('svg')];
  return {missing: false,
          count: svgs.length,
          displays: svgs.map(s => getComputedStyle(s).display),
          widths: svgs.map(s => +s.getBoundingClientRect().width.toFixed(1)),
          glyphs: box.querySelectorAll('.gb-rv-panel__glyph').length};
}"""

ok = red = 0
def chk(c, label):
    global ok, red
    if c: ok += 1
    else:
        red += 1
        print("  RED  " + label)

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=CHROME)
    p = b.new_context(viewport={"width": 1440, "height": 900}).new_page()
    for page in PAGES:
        for mode in ("wrapped", "bare"):
            p.goto("file:///home/ly/project/Gumi-Brand/%s.html" % page, wait_until="load")
            p.wait_for_timeout(300)
            n = p.evaluate(UNWRAP) if mode == "bare" else 0
            d = p.evaluate(PROBE)
            tag = "%s/%s" % (page, mode)
            if d["missing"]:
                chk(False, "%s no .gb-rv-panel__video" % tag); continue
            # liveness: there has to BE an svg for "it is hidden" to mean anything
            chk(d["count"] >= 1, "%s no svg to hide (assertion would be vacuous)" % tag)
            for i, disp in enumerate(d["displays"]):
                chk(disp == "none", "%s svg%d display=%s" % (tag, i, disp))
            for i, w in enumerate(d["widths"]):
                chk(w == 0, "%s svg%d still occupies %spx" % (tag, i, w))
            if mode == "bare":
                chk(n >= 1, "%s unwrap found no .gb-rv-panel__glyph to strip" % tag)
                chk(d["glyphs"] == 0, "%s wrapper survived the unwrap" % tag)
            else:
                chk(d["glyphs"] >= 1, "%s expected a .gb-rv-panel__glyph wrapper" % tag)
    b.close()

print("\n%d ok / %d red" % (ok, red))
sys.exit(1 if red else 0)
