"""button.is-loading swaps a button's label for a spinner without moving anything.

gb-account-data.liquid adds .is-loading to the button that triggered an API call.
For every button class it lands on: the box keeps its size, the label and child
icons disappear, a ring in the button's own text colour spins in their place.
A div with the same class (.gb-cart-item uses it) must get no ring.

    python3 tools/acctloading.py            # expect all ok
    python3 tools/acctloading.py --strip    # rule removed first: must go red
    python3 tools/acctloading.py --shot out.png
"""
import sys, pathlib, threading, functools, http.server
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
CLASSES = ["gb-acct-btn", "gb-acct-btn--ghost", "gb-acct-link", "gb-acct-link--sm",
           "gb-acct-modal__save", "gb-acct-discount__apply", "gb-acct-intro__edit",
           "gb-acct-chip__remove"]

def _chrome():
    import glob
    c = sorted(glob.glob(str(pathlib.Path.home() / ".cache/ms-playwright/chromium-*/chrome-linux/chrome")))
    return c[-1] if c else None

PROBE = r"""
([classes, strip]) => {
  if (strip) for (const s of document.styleSheets) {
    let r; try { r = s.cssRules; } catch (e) { continue; }
    for (let i = r.length - 1; i >= 0; i--) if (/is-loading/.test(r[i].cssText)) s.deleteRule(i);
  }
  const box = document.createElement('div');
  box.id = 'probe-loading';
  box.style.cssText = 'position:fixed;inset:0;z-index:99999;background:#fff;display:grid;grid-template-columns:repeat(2,max-content);gap:16px 40px;padding:24px;align-content:start';
  document.body.append(box);
  const out = [];
  for (const c of classes) {
    const src = document.querySelector('button.' + c);
    if (!src) { out.push({c, missing: true}); continue; }
    const a = src.cloneNode(true), b = src.cloneNode(true);
    a.removeAttribute('hidden'); b.removeAttribute('hidden');
    box.append(a, b);
    b.classList.add('is-loading');
    const ra = a.getBoundingClientRect(), rb = b.getBoundingClientRect();
    const cs = getComputedStyle(b), ps = getComputedStyle(b, '::after');
    const kid = b.firstElementChild;
    out.push({c,
      sameBox: Math.abs(ra.width - rb.width) < 0.5 && Math.abs(ra.height - rb.height) < 0.5,
      textHidden: cs.webkitTextFillColor === 'rgba(0, 0, 0, 0)',
      kidsHidden: !kid || getComputedStyle(kid).visibility === 'hidden',
      ring: ps.content !== 'none' && parseFloat(ps.width) > 0,
      ringColour: ps.borderTopColor === cs.color,
      spinning: /gb-acct-spin\b/.test(ps.animationName) && ps.animationIterationCount.startsWith('infinite'),
      inert: cs.pointerEvents === 'none'});
  }
  const d = document.createElement('div');
  d.className = 'is-loading'; d.textContent = 'row';
  box.append(d);
  out.push({c: 'div.is-loading (negative)', divNoRing: getComputedStyle(d, '::after').content === 'none'});
  return out;
}
"""

def main():
    strip = "--strip" in sys.argv
    shot = sys.argv[sys.argv.index("--shot") + 1] if "--shot" in sys.argv else None
    ok = red = 0
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=_chrome())
        pg = b.new_page(viewport={"width": 1440, "height": 900})
        # http, not file://: file:// sheets hide cssRules and --strip would silently no-op
        class Quiet(http.server.SimpleHTTPRequestHandler):
            def log_message(self, *a): pass
        srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(ROOT)))
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        pg.goto("http://127.0.0.1:%d/account.html" % srv.server_port)
        pg.wait_for_timeout(500)
        res = pg.evaluate(PROBE, [CLASSES, strip])
        if shot:
            pg.wait_for_timeout(300)
            pg.screenshot(path=shot)
        b.close()
        srv.shutdown()
    for r in res:
        if r.get("missing"):
            print("red  %s: no such button on account.html (anchor gone)" % r["c"]); red += 1; continue
        for k, v in r.items():
            if k == "c": continue
            print("%s %s: %s" % ("ok  " if v else "red ", r["c"], k))
            ok += bool(v); red += not v
    print("\n%d ok / %d red" % (ok, red))
    sys.exit(1 if red else 0)

if __name__ == "__main__":
    main()
