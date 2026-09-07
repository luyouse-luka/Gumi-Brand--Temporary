"""R67: every line's halo rides its OWN line.

r64 asserted the halo's animation-name/delay against line 0 only, which is why a
whole-string halo passed while the outline visibly landed ahead of line 2. The
assertions here are per line, and one of them reads the transform MID-FLIGHT.
"""
import sys
from playwright.sync_api import sync_playwright

CHROME = "/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome"
BASE = "file:///home/ly/project/Gumi-Brand"
# .gb-usp__value is deliberately NOT here: it carries a halo but no
# data-line-reveal, so it never splits and its halo is a static whole-string copy.
CASES = [("index", ".gb-stat__value", [1440, 390]),
         ("how-gumi-works", ".gb-dosed__title", [1440, 768, 390])]

PROBE = """(sel) => {
  const out = [];
  for (const host of document.querySelectorAll(sel)) {
    const lines = [...host.querySelectorAll(':scope > .gb-line-mask')];
    const halos = [...host.querySelectorAll(':scope > .gb-ink-halo--line')];
    const orig  = host.querySelector(':scope > .gb-ink-halo:not(.gb-ink-halo--line)');
    out.push({
      split: host.classList.contains('is-split'),
      masks: lines.length,
      halos: halos.length,
      origDisplay: orig ? getComputedStyle(orig).display : null,
      maskDelay: lines.map(m => getComputedStyle(m.firstChild).animationDelay),
      haloDelay: halos.map(h => getComputedStyle(h).animationDelay),
      maskName:  lines.map(m => getComputedStyle(m.firstChild).animationName),
      haloName:  halos.map(h => getComputedStyle(h).animationName),
      haloTop:   halos.map(h => h.style.top),
      maskTop:   lines.map(m => m.offsetTop + 'px'),
      haloIdx:   halos.map(h => h.style.getPropertyValue('--line-i').trim())
    });
  }
  return out;
}"""

MIDFLIGHT = """(sel) => {
  const host = document.querySelector(sel);
  host.classList.remove('is-revealed', 'is-settled');
  void host.offsetWidth;
  host.classList.add('is-revealed');
  return true;
}"""
SAMPLE = """(sel) => {
  const host = document.querySelector(sel);
  const ty = el => {
    const m = new DOMMatrixReadOnly(getComputedStyle(el).transform);
    return Math.round(m.m42 * 10) / 10;
  };
  return {
    mask: [...host.querySelectorAll(':scope > .gb-line-mask')].map(m => ty(m.firstChild)),
    halo: [...host.querySelectorAll(':scope > .gb-ink-halo--line')].map(ty)
  };
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
    for page, sel, widths in CASES:
        for w in widths:
            p.set_viewport_size({"width": w, "height": 1000})
            p.goto("%s/%s.html" % (BASE, page), wait_until="load")
            p.wait_for_timeout(700)
            # animation-name only resolves once the host is revealed, and a
            # headless page never scrolls it into view
            p.evaluate("""(sel) => document.querySelectorAll(sel)
                .forEach(h => h.classList.add('is-revealed'))""", sel)
            p.wait_for_timeout(60)
            hosts = p.evaluate(PROBE, sel)
            tag = "%s %s @%d" % (page, sel, w)
            chk(len(hosts) > 0, "%s no host found" % tag)
            for hi, h in enumerate(hosts):
                t = "%s #%d" % (tag, hi)
                chk(h["split"], "%s not split" % t)
                chk(h["masks"] >= 1, "%s no masks (assertion vacuous)" % t)
                chk(h["halos"] == h["masks"],
                    "%s %d halos for %d lines" % (t, h["halos"], h["masks"]))
                chk(h["origDisplay"] == "none",
                    "%s whole-string halo still shown (%s)" % (t, h["origDisplay"]))
                chk(h["haloTop"] == h["maskTop"],
                    "%s halo tops %s != mask tops %s" % (t, h["haloTop"], h["maskTop"]))
                chk(h["haloIdx"] == [str(i) for i in range(h["masks"])],
                    "%s --line-i %s" % (t, h["haloIdx"]))
                chk(h["haloDelay"] == h["maskDelay"],
                    "%s halo delays %s != mask delays %s" % (t, h["haloDelay"], h["maskDelay"]))
                for i, (hn, mn) in enumerate(zip(h["haloName"], h["maskName"])):
                    chk(hn == "gm-halo-up", "%s halo%d anim=%s" % (t, i, hn))
                    chk(mn == "gm-line-up", "%s mask%d anim=%s" % (t, i, mn))

            p.evaluate(MIDFLIGHT, sel)
            p.wait_for_timeout(260)
            s = p.evaluate(SAMPLE, sel)
            chk(len(s["halo"]) == len(s["mask"]) and len(s["mask"]) > 0,
                "%s mid-flight layer count %s/%s" % (tag, len(s["halo"]), len(s["mask"])))
            for i, (hy, my) in enumerate(zip(s["halo"], s["mask"])):
                chk(abs(hy - my) <= 1.0,
                    "%s line%d mid-flight halo ty=%s vs glyphs ty=%s" % (tag, i, hy, my))
            chk(any(abs(v) > 0.5 for v in s["mask"]),
                "%s nothing in flight at 260ms (assertion vacuous)" % tag)

    p.set_viewport_size({"width": 1440, "height": 1000})
    p.goto("%s/how-gumi-works.html" % BASE, wait_until="load")
    p.wait_for_timeout(700)
    before = p.evaluate("() => document.querySelectorAll('.gb-ink-halo--line').length")
    for w in (900, 500, 1200, 1440):
        p.set_viewport_size({"width": w, "height": 1000})
        p.wait_for_timeout(400)
    p.set_viewport_size({"width": 1440, "height": 1000})
    p.wait_for_timeout(600)
    after = p.evaluate("() => document.querySelectorAll('.gb-ink-halo--line').length")
    chk(before > 0, "no per-line halos to begin with (assertion vacuous)")
    chk(after == before, "resize left %d halos, started with %d" % (after, before))
    b.close()

print("\n%d ok / %d red" % (ok, red))
sys.exit(1 if red else 0)
