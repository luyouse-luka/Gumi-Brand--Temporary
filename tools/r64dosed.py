"""Measure .gb-dosed__inner descendants live vs static. Live is password-gated."""
import sys, json
from playwright.sync_api import sync_playwright

CHROME = "/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome"
LIVE = "https://gumi.com.au/pages/how-gumi-works"
STATIC = "file:///home/ly/project/Gumi-Brand/how-gumi-works.html"
WIDTHS = [1440, 1280, 1024, 768, 390]

PROBE = """() => {
  const out = {};
  const inner = document.querySelector('.gb-dosed__inner');
  if (!inner) return {err: 'no .gb-dosed__inner'};
  const cs = getComputedStyle(inner);
  out.inner = {w: inner.getBoundingClientRect().width,
               align: cs.alignItems, gap: cs.rowGap, pad: cs.paddingLeft};
  out.kids = [...inner.children].map(k => {
    const r = k.getBoundingClientRect();
    return {cls: k.className, w: +r.width.toFixed(1), h: +r.height.toFixed(1)};
  });
  out.blocks = [...document.querySelectorAll('.gb-dosed__block')].map(b => {
    const r = b.getBoundingClientRect();
    const m = b.querySelector('.gb-dosed__media');
    return {w: +r.width.toFixed(1), h: +r.height.toFixed(1),
            dir: getComputedStyle(b).flexDirection,
            mediaW: m ? +m.getBoundingClientRect().width.toFixed(1) : null};
  });
  return out;
}"""

def gate_cookie():
    """storefront password rides in _shopify_essential; grab it with curl since the
    theme's password field lives inside a modal Playwright cannot see."""
    import subprocess, tempfile, os
    jar = tempfile.mktemp()
    subprocess.run(["curl", "-s", "-c", jar, "-b", jar, "-o", os.devnull,
                    "https://gumi.com.au/password"], check=True)
    subprocess.run(["curl", "-s", "-c", jar, "-b", jar, "-X", "POST", "-d",
                    "form_type=storefront_password&utf8=%E2%9C%93&password=1234",
                    "-o", os.devnull, "https://gumi.com.au/password"], check=True)
    out = []
    for line in open(jar):
        line = line.lstrip("#").replace("HttpOnly_", "")
        f = line.rstrip("\n").split("\t")
        if len(f) == 7 and f[5] == "_shopify_essential":
            out.append({"name": f[5], "value": f[6], "domain": "gumi.com.au", "path": "/"})
    os.unlink(jar)
    if not out:
        sys.exit("no _shopify_essential cookie - password flow changed")
    return out


def run(pw, url, gate):
    b = pw.chromium.launch(executable_path=CHROME)
    ctx = b.new_context(viewport={"width": 1440, "height": 900})
    if gate:
        ctx.add_cookies(gate_cookie())
    p = ctx.new_page()
    res = {}
    for w in WIDTHS:
        p.set_viewport_size({"width": w, "height": 900})
        p.goto(url, wait_until="load")
        p.wait_for_timeout(700)
        res[w] = p.evaluate(PROBE)
    b.close()
    return res

with sync_playwright() as pw:
    live = run(pw, LIVE, True)
    static = run(pw, STATIC, False)

print("width | side   | inner w  align   | children (class -> w)")
for w in WIDTHS:
    for name, d in (("live", live[w]), ("static", static[w])):
        if "err" in d:
            print("%5d | %-6s | %s" % (w, name, d["err"])); continue
        kids = "; ".join("%s -> %s" % (k["cls"][:34], k["w"]) for k in d["kids"])
        print("%5d | %-6s | %7.1f %-8s | %s" % (w, name, d["inner"]["w"], d["inner"]["align"], kids))
    for name, d in (("live", live[w]), ("static", static[w])):
        if "err" in d: continue
        print("      | %-6s |   blocks: %s" % (name, [ (b["w"], b["mediaW"]) for b in d["blocks"] ]))
    print()

print("\n=== 判据 ===")
red = 0
for w in WIDTHS:
    lb = [b["w"] for b in live[w].get("blocks", [])]
    sb = [b["w"] for b in static[w].get("blocks", [])]
    ok = lb == sb
    red += 0 if ok else 1
    print("%5d  block widths live=%s static=%s  %s" % (w, lb, sb, "ok" if ok else "RED"))
print("red:", red)
