#!/usr/bin/env python3
"""Compare the build's section stack against the mobile board's, page by page.

    python3 tools/pagefit.py             # every page
    python3 tools/pagefit.py science.html

Prints each side's top-level blocks in document order with their heights, so a
section that is too tall or too short shows up as a number rather than as a
"looks off" on a screenshot. It does NOT try to pair them up automatically --
the build's section split does not match the boards' frame split one-to-one
(the boards wrap waves in their own Spacer frames, the build hangs them off the
section) -- so the pairing is left to the eye, with running totals to anchor it.

The 96px "Chrome browser" frame most boards carry is dropped: it is mockup
staging, not part of the page (see figma-modal-mockup-includes-fake-staging).
"""
import json, os, sys
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = os.path.expanduser("~/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome")

# page -> (node file stem, id of the frame that holds the page content)
PAGES = {
    "index.html":          ("228-5932_homepage-mobile", "237:13125"),
    "pdp.html":            ("324-53792_pdp-mobile", None),
    "science.html":        ("324-58044_science-moble", "324:58047"),
    "reviews.html":        ("324-64961_reviews", "324:64962"),
    "how-gumi-works.html": ("324-70523_how-gumi-works", "326:89662"),
    "our-story.html":      ("324-73673_our-story", "324:73675"),
    "faq.html":            ("324-76169_faq", "326:93671"),
    "get-in-touch.html":   ("326-80318_get-in-touch", None),
    "referral.html":       ("326-81540_referral", "326:90991"),
    "shipping.html":       ("326-83129_shipping", "326:83131"),
    "privacy-policy.html": ("326-83399_privacy-policy", "326:83401"),
}


def board_blocks(stem, origin):
    d = json.load(open(os.path.join(ROOT, "figma/nodes", stem + ".json")))
    root = list(d["nodes"].values())[0]["document"]

    def find(n, t):
        if n["id"] == t:
            return n
        for c in n.get("children") or []:
            r = find(c, t)
            if r:
                return r

    node = find(root, origin) if origin else root
    out = []
    for c in node.get("children") or []:
        if c.get("visible") is False:
            continue
        nm = c.get("name", "")
        if "chrome browser" in nm.lower():
            continue
        bb = c.get("absoluteBoundingBox") or {}
        out.append((nm, bb.get("height", 0)))
    return out


def build_blocks(page):
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME, args=["--no-sandbox"])
        pg = b.new_page(viewport={"width": 390, "height": 900})
        pg.goto(f"file://{os.path.join(ROOT, page)}")
        pg.wait_for_timeout(1200)
        out = pg.evaluate("""() => {
          const hosts = [document.querySelector('header'), ...document.querySelectorAll('body > section, main > section, body > footer')];
          return hosts.filter(Boolean).map(e => {
            const r = e.getBoundingClientRect();
            const cls = (e.className || '').toString().split(' ').filter(c => c.startsWith('gb-')).slice(0,2).join(' ');
            return [cls || e.tagName.toLowerCase(), +r.height.toFixed(1)];
          }); }""")
        b.close()
    return out


def run(page):
    stem, origin = PAGES[page]
    bd = board_blocks(stem, origin)
    bl = build_blocks(page)
    print(f"\n=== {page}  ({stem}) ===")
    print(f"{'BOARD':<40}{'h':>9}  |  {'BUILD':<34}{'h':>9}")
    n = max(len(bd), len(bl))
    tb = tl = 0.0
    for i in range(n):
        ln = rn = ""
        if i < len(bd):
            tb += bd[i][1]
            ln = f"{bd[i][0][:36]:<40}{bd[i][1]:>9.1f}"
        else:
            ln = " " * 49
        if i < len(bl):
            tl += bl[i][1]
            rn = f"{bl[i][0][:32]:<34}{bl[i][1]:>9.1f}"
        print(f"{ln}  |  {rn}")
    print(f"{'TOTAL':<40}{tb:>9.1f}  |  {'TOTAL':<34}{tl:>9.1f}   Δ={tl-tb:+.1f}")


pages = sys.argv[1:] or list(PAGES)
for p in pages:
    if p not in PAGES:
        print(f"skip {p}")
        continue
    try:
        run(p)
    except Exception as e:
        print(f"\n=== {p} === FAILED: {e}")
