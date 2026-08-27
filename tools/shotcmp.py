#!/usr/bin/env python3
"""Put a slice of the rendered page next to the same slice of the design export.

    python3 tools/shotcmp.py index.html 228-5932 <y0> <y1> [out.png] [--width 390]
    python3 tools/shotcmp.py index.html 228-5932 --sel .gb-reviews --pad 80

The board export and the build are both 390 wide, so a slice can be laid side by
side 1:1 with no scaling -- which is the point: a structural assertion passing is
not the same as the thing being drawn in the right place (round 27 shipped a
mobile bear at the wrong end of the panel with every assertion green).

Two things have to be handled or the build side comes out blank:
  * .wowo only plays on scroll, and a full_page screenshot does not scroll, so
    the page is walked top to bottom first (see kill-animations-blanks-reveal-blocks).
  * the entrance takes 0.7s and the class is dropped at 1500ms, so shooting early
    catches every revealed block mid-fade.

--sel takes the slice from the element's own box instead of raw coordinates, and
prints the y it used so the board side can be lined up by hand.
"""
import os, sys, subprocess
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = os.path.expanduser("~/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome")
SHOTS = os.path.join(ROOT, "figma/screenshots")
OUT = os.path.join(ROOT, "tools/shots")


def find_board(key):
    import glob
    hits = [p for p in glob.glob(os.path.join(SHOTS, "*.png")) if key.lower() in os.path.basename(p).lower()]
    if not hits:
        sys.exit(f"no board screenshot matching {key!r}")
    return sorted(hits)[0]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    page = args[0]
    board = find_board(args[1])

    width = 390
    sel = None
    pad = 40
    board_y = None
    for i, a in enumerate(sys.argv):
        if a == "--width":
            width = int(sys.argv[i + 1])
        elif a == "--sel":
            sel = sys.argv[i + 1]
        elif a == "--pad":
            pad = int(sys.argv[i + 1])
        elif a == "--board-y":
            board_y = float(sys.argv[i + 1])

    os.makedirs(OUT, exist_ok=True)
    live = os.path.join(OUT, "cmp-live.png")

    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME, args=["--no-sandbox"])
        pg = b.new_page(viewport={"width": width, "height": 900}, device_scale_factor=1)
        pg.goto(f"file://{os.path.join(ROOT, page)}")
        pg.wait_for_timeout(600)
        # walk the page so every .wowo / [data-line-reveal] fires, then let the
        # last one finish its 0.7s tween and drop the class at 1500ms
        h = pg.evaluate("() => document.documentElement.scrollHeight")
        y = 0
        while y < h:
            pg.evaluate(f"window.scrollTo(0, {y})")
            pg.wait_for_timeout(120)
            y += 700
        pg.evaluate("window.scrollTo(0, 0)")
        pg.wait_for_timeout(1800)

        if sel:
            r = pg.evaluate("""(s) => { const e = document.querySelector(s);
                if (!e) return null;
                const b = e.getBoundingClientRect();
                return [b.x + scrollX, b.y + scrollY, b.width, b.height]; }""", sel)
            if not r:
                sys.exit(f"selector not found: {sel}")
            y0, y1 = max(0, r[1] - pad), r[1] + r[3] + pad
            print(f"# {sel}: y {r[1]:.1f} .. {r[1]+r[3]:.1f}  (slice {y0:.0f}..{y1:.0f})")
        else:
            y0, y1 = float(args[2]), float(args[3])

        pg.screenshot(path=live, full_page=True)
        b.close()

    y0, y1 = int(y0), int(y1)
    by0 = int(board_y) if board_y is not None else y0
    by1 = by0 + (y1 - y0)
    out = os.path.join(OUT, args[4] if len(args) > 4 else "cmp.png")

    from PIL import Image
    a = Image.open(live).convert("RGB").crop((0, y0, width, y1))
    bd = Image.open(board).convert("RGB")
    by1 = min(by1, bd.height)
    b_img = bd.crop((0, by0, min(width, bd.width), by1))
    h = max(a.height, b_img.height)
    gap = 12
    canvas = Image.new("RGB", (a.width + b_img.width + gap, h), (255, 0, 255))
    canvas.paste(b_img, (0, 0))          # board on the left
    canvas.paste(a, (b_img.width + gap, 0))  # build on the right
    canvas.save(out)
    print(f"# board(blue,left)={os.path.basename(board)} y {by0}..{by1}")
    print(f"# build(red,right)={page} y {y0}..{y1}")
    print(out)


main()
