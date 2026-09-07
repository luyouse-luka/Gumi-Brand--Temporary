"""R67 part 2: the reel rail keeps the board's framing above 1440.

Board (1440): three whole cards with a clipped one at each end, card 304x540,
gap 24. Above 1440 the card tracks the viewport at the same 304:540 ratio.
"""
import sys
from playwright.sync_api import sync_playwright

CHROME = "/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome"
WIDTHS = [1280, 1440, 1600, 1920, 2560]
RATIO = 304.0 / 540.0

PROBE = """() => {
  const rail = document.querySelector('.gb-reels');
  const cards = [...document.querySelectorAll('.gb-reel')];
  if (!rail || !cards.length) return {missing: true};
  const r0 = cards[0].getBoundingClientRect();
  const vw = document.documentElement.clientWidth;
  // how many cards fit across the viewport, gap included
  const gap = parseFloat(getComputedStyle(rail).columnGap) || 0;
  // count cards whose box intersects the viewport at all, and those fully inside
  let touching = 0, whole = 0;
  for (const c of cards) {
    const r = c.getBoundingClientRect();
    if (r.right > 0 && r.left < vw) touching++;
    if (r.left >= -0.5 && r.right <= vw + 0.5) whole++;
  }
  return {missing: false, vw, gap,
          w: +r0.width.toFixed(1), h: +r0.height.toFixed(1),
          ratio: +(r0.width / r0.height).toFixed(4),
          slots: +(vw / (r0.width + gap)).toFixed(2),
          touching, whole};
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
    p = b.new_context(viewport={"width": 1440, "height": 1000}).new_page()
    print("  width |    card w x h |  ratio | gap |  slots | whole/touching")
    for w in WIDTHS:
        p.set_viewport_size({"width": w, "height": 1000})
        p.goto("file:///home/ly/project/Gumi-Brand/index.html", wait_until="load")
        p.wait_for_timeout(900)
        d = p.evaluate(PROBE)
        if d["missing"]:
            chk(False, "%d no reel rail" % w); continue
        print("  %5d | %6.1f x %5.1f | %6.4f | %3.0f | %6.2f | %d/%d"
              % (w, d["w"], d["h"], d["ratio"], d["gap"], d["slots"], d["whole"], d["touching"]))

        # 1. the board's ratio holds at every width
        chk(abs(d["ratio"] - RATIO) < 0.005,
            "%d ratio %.4f != board %.4f" % (w, d["ratio"], RATIO))
        # 2. at and below 1440 the card is exactly the board's 304x540
        if w <= 1440:
            chk(abs(d["w"] - 304) < 0.6, "%d card w=%s want 304" % (w, d["w"]))
            chk(abs(d["h"] - 540) < 0.6, "%d card h=%s want 540" % (w, d["h"]))
        # 3. above 1440 it tracks the viewport
        else:
            want = w * 304.0 / 1440.0
            chk(abs(d["w"] - want) < 1.5,
                "%d card w=%s want %.1f (viewport-tracked)" % (w, d["w"], want))
        # 4. the framing itself: three whole cards, and a clipped one each side
        chk(d["whole"] >= 3, "%d only %d whole cards on screen" % (w, d["whole"]))
        chk(d["touching"] >= d["whole"] + 1,
            "%d nothing clipped at the edges (whole=%d touching=%d)"
            % (w, d["whole"], d["touching"]))
        # The framing target is a 1440-and-up requirement; below that the card
        # is the board's fixed 304 and the rail simply fits fewer of them.
        if w >= 1440:
            chk(4.2 <= d["slots"] <= 4.7,
                "%d slots=%.2f outside the board's framing" % (w, d["slots"]))
    b.close()

print("\n%d ok / %d red" % (ok, red))
sys.exit(1 if red else 0)
