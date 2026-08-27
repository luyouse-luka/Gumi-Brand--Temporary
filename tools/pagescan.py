#!/usr/bin/env python3
"""Slice a page and its board side by side, one anchor pair at a time.

    python3 tools/pagescan.py science.html --list
    python3 tools/pagescan.py science.html --pairs ".gb-page-hero=96,.gb-compare=2478"

Numbers alone miss things: round 35 shipped four arrows whose element boxes
matched the board to within 2px while the artwork inside them was 25-35% short,
and every assertion was green. So every page gets looked at, not just measured.

Anchors are explicit and per block. Pairing build sections to board frames in
document order does NOT work: board children are not stored in y order and the
boards carry Spacer frames (the scallop bands) the build folds into the section
above. --list prints both sides sorted so the pairs can be read off by hand.

Board y is measured from the board root, so it already includes the 96px
"Chrome browser" mockup bar the boards carry above the page -- do not add it.

The page is walked top to bottom before shooting: .wowo only plays on scroll and
full_page does not scroll, so an un-walked page shoots its reveal blocks blank
(see kill-animations-blanks-reveal-blocks).
"""
import json, math, os, sys
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = os.path.expanduser("~/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome")
OUT = os.path.join(ROOT, "tools/shots")
NODES = os.path.join(ROOT, "figma/nodes")
SHOTS = os.path.join(ROOT, "figma/screenshots")

# page -> (node-file stem, screenshot stem, content-frame id or None)
PAGES = {
    "index.html":          ("228-5932_homepage-mobile", "228-5932", "237:13125"),
    "pdp.html":            ("324-53792_pdp-mobile", "324-53792", None),
    "science.html":        ("324-58044_science-moble", "324-58044", "324:58047"),
    "reviews.html":        ("324-64961_reviews", "324-64961", "324:64962"),
    "how-gumi-works.html": ("324-70523_how-gumi-works", "324-70523", "326:89662"),
    "our-story.html":      ("324-73673_our-story", "324-73673", "324:73675"),
    "faq.html":            ("324-76169_faq", "324-76169", "326:93671"),
    "get-in-touch.html":   ("326-80318_get-in-touch", "326-80318", None),
    "referral.html":       ("326-81540_referral", "326-81540", "326:90991"),
    "shipping.html":       ("326-83129_shipping", "326-83129", "326:83131"),
    "privacy-policy.html": ("326-83399_privacy-policy", "326-83399", "326:83401"),
}


def board_png(stem):
    import glob
    hits = [p for p in glob.glob(os.path.join(SHOTS, "*.png")) if os.path.basename(p).startswith(stem)]
    if not hits:
        sys.exit(f"no board screenshot for {stem}")
    return sorted(hits)[0]


def board_blocks(stem, origin, depth=1):
    d = json.load(open(os.path.join(NODES, stem + ".json")))
    root = list(d["nodes"].values())[0]["document"]
    ry = root["absoluteBoundingBox"]["y"]

    def find(n, t):
        if n["id"].split(";")[-1] == t:
            return n
        for c in n.get("children") or []:
            r = find(c, t)
            if r:
                return r

    node = find(root, origin) if origin else root
    out = []

    def walk(n, lvl):
        for c in n.get("children") or []:
            if c.get("visible") is False:
                continue
            if "chrome browser" in c.get("name", "").lower():
                continue
            bb = c.get("absoluteBoundingBox") or {}
            if not bb:
                continue
            out.append((c["name"], c["id"], round(bb["y"] - ry), round(bb["height"]), lvl))
            if lvl < depth:
                walk(c, lvl + 1)

    walk(node, 1)
    out.sort(key=lambda r: (r[2], r[4]))
    return out


def shoot(page, width, sels):
    live = os.path.join(OUT, f"scan-{page.replace('.html','')}.png")
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME, args=["--no-sandbox"])
        pg = b.new_page(viewport={"width": width, "height": 900}, device_scale_factor=1)
        pg.goto(f"file://{os.path.join(ROOT, page)}")
        pg.wait_for_timeout(500)
        h = pg.evaluate("() => document.documentElement.scrollHeight")
        y = 0
        while y < h:
            pg.evaluate(f"window.scrollTo(0,{y})")
            pg.wait_for_timeout(90)
            y += 700
        pg.evaluate("window.scrollTo(0,0)")
        pg.wait_for_timeout(1800)
        tops = pg.evaluate("""() => {
          const out = [];
          const push = e => { if (!e) return; const r = e.getBoundingClientRect();
            out.push([ (e.className||'').toString().split(' ').filter(c=>c.startsWith('gb-'))[0] || e.tagName.toLowerCase(),
                       Math.round(r.y + scrollY), Math.round(r.height) ]); };
          push(document.querySelector('header'));
          document.querySelectorAll('body > section, main > section, body > footer, main > div').forEach(push);
          return out; }""")
        boxes = {}
        for s in sels:
            r = pg.evaluate("""(s) => { const e = document.querySelector(s);
                if (!e) return null; const b = e.getBoundingClientRect();
                return [Math.round(b.y + scrollY), Math.round(b.height)]; }""", s)
            boxes[s] = r
        pg.screenshot(path=live, full_page=True)
        b.close()
    return live, tops, boxes


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    page = args[0]
    if page not in PAGES:
        sys.exit(f"unknown page {page}")
    stem, shot_stem, origin = PAGES[page]

    do_list = "--list" in sys.argv
    pairs, sh, width, depth, tag = [], 900, 390, 1, ""
    for i, a in enumerate(sys.argv):
        if a == "--pairs":
            for part in sys.argv[i + 1].split(","):
                sel, _, by = part.rpartition("=")
                pairs.append((sel.strip(), float(by)))
        elif a == "--h":
            sh = int(sys.argv[i + 1])
        elif a == "--width":
            width = int(sys.argv[i + 1])
        elif a == "--depth":
            depth = int(sys.argv[i + 1])
        elif a == "--tag":
            tag = sys.argv[i + 1]

    os.makedirs(OUT, exist_ok=True)
    blocks = board_blocks(stem, origin, depth)

    if do_list and not pairs:
        live, tops, _ = shoot(page, width, [])
        lv = Image.open(live)
        bd = Image.open(board_png(shot_stem))
        print(f"=== {page}   build {lv.width}x{lv.height}   board {bd.width}x{bd.height}")
        print("--- build sections (y, h) ---")
        for c, y, h in tops:
            print(f"    {c:<26} y={y:<6} h={h}")
        print("--- board blocks (y, h) ---")
        for nm, nid, y, h, lvl in blocks:
            print(f"    {'  '*(lvl-1)}{nm[:34]:<36} y={y:<6} h={h:<6} {nid}")
        return

    live, tops, boxes = shoot(page, width, [s for s, _ in pairs])
    lv = Image.open(live).convert("RGB")
    bd = Image.open(board_png(shot_stem)).convert("RGB")
    print(f"=== {page}   build {lv.width}x{lv.height}   board {bd.width}x{bd.height}")
    for sel, by in pairs:
        r = boxes.get(sel)
        if not r:
            print(f"    !! selector not found: {sel}")
            continue
        ly, lh = r
        n = max(1, math.ceil(lh / sh))
        base = sel.strip(".#").replace(" ", "_").replace(">", "-").replace(":", "-")
        for k in range(n):
            y0 = ly + k * sh
            y1 = min(lv.height, y0 + sh)
            b0 = by + k * sh
            b1 = min(bd.height, b0 + (y1 - y0))
            if y1 <= y0 or b1 <= b0:
                break
            a = lv.crop((0, y0, lv.width, y1))
            c = bd.crop((0, b0, min(width, bd.width), b1))
            H = max(a.height, c.height)
            canvas = Image.new("RGB", (a.width + c.width + 12, H), (255, 0, 255))
            canvas.paste(c, (0, 0))
            canvas.paste(a, (c.width + 12, 0))
            name = f"scan{tag}-{page.replace('.html','')}-{base}{'' if n == 1 else f'-{k}'}.png"
            canvas.save(os.path.join(OUT, name))
            print(f"    {name:<56} board y {b0}..{b1}   build y {y0}..{y1}")


main()
