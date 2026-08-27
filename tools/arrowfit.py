#!/usr/bin/env python3
"""Solve the four stats arrows' width/left/top from INK measured on the screenshots.

    python3 tools/arrowfit.py

Why not the node data: the boards' absoluteRenderBounds for these groups are 25-35%
larger than the ink that actually appears in the export (they carry the OUTSIDE
stroke's mitre reach, and the arrowhead is a separate vector), so sizing the
element box to match renderBounds leaves the drawn arrow visibly short. Round 35
did exactly that and the client still reported the arrows as not matching.

So the target is taken from the design export itself: find the lime ink inside a
window around each arrow, on both the board PNG and a screenshot of the build,
and scale the current CSS width by the ratio. left/top are re-centred on the
measured ink centre, expressed against the 208 x 257.42 bear slot.
"""
import json, os, sys
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = os.path.expanduser("~/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome")
BOARD = os.path.join(ROOT, "figma/screenshots/228-5932_homepage-mobile_390x11543.png")

# board ink boxes, converted to screenshot coords:
#   x = abs_x + 26199.48828125     y = abs_y - 710.0
BOARD_INK = {
    "--1": (75.99, 1794.79, 60.08, 64.69),
    "--2": (270.74, 1761.56, 67.76, 71.30),
    "--3": (59.14, 2103.80, 79.73, 80.54),
    "--4": (250.83, 2079.76, 76.34, 78.53),
}


def ink_bbox(arr, x0, y0, x1, y1, seed=None):
    """Lime ink inside a window, restricted to the blob connected to `seed`.

    The bear's glow is lime too and reaches into every arrow's window, so a plain
    bbox over the window measures the glow. Flood-filling from the arrow's own
    centre keeps the arrow and drops anything not touching it.
    """
    h, w, _ = arr.shape
    x0, y0 = max(0, int(x0)), max(0, int(y0))
    x1, y1 = min(w, int(x1)), min(h, int(y1))
    sub = arr[y0:y1, x0:x1]
    r, g, b = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
    m = (g > 140) & (r < g - 30) & (b < g - 50)
    if not m.any():
        return None
    if seed is None:
        ys, xs = np.nonzero(m)
        return (x0 + xs.min(), y0 + ys.min(), xs.max() - xs.min() + 1, ys.max() - ys.min() + 1)

    sxp, syp = int(seed[0]) - x0, int(seed[1]) - y0
    hh, ww = m.shape
    # nearest lit pixel to the seed starts the fill
    ys, xs = np.nonzero(m)
    d = (xs - sxp) ** 2 + (ys - syp) ** 2
    i = int(np.argmin(d))
    start = (int(ys[i]), int(xs[i]))

    seen = np.zeros_like(m)
    stack = [start]
    seen[start] = True
    while stack:
        cy, cx = stack.pop()
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                ny, nx = cy + dy, cx + dx
                if 0 <= ny < hh and 0 <= nx < ww and m[ny, nx] and not seen[ny, nx]:
                    seen[ny, nx] = True
                    stack.append((ny, nx))
    ys, xs = np.nonzero(seen)
    return (x0 + xs.min(), y0 + ys.min(), xs.max() - xs.min() + 1, ys.max() - ys.min() + 1)


def main():
    live = os.path.join(ROOT, "tools/shots/arrowfit-live.png")
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME, args=["--no-sandbox"])
        pg = b.new_page(viewport={"width": 390, "height": 900}, device_scale_factor=1)
        pg.goto(f"file://{os.path.join(ROOT, 'index.html')}")
        pg.wait_for_timeout(500)
        hgt = pg.evaluate("() => document.documentElement.scrollHeight")
        y = 0
        while y < hgt:
            pg.evaluate(f"window.scrollTo(0,{y})"); pg.wait_for_timeout(90); y += 700
        pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(1800)
        info = pg.evaluate("""() => {
          const slot = document.querySelector('.gb-stats__bear').getBoundingClientRect();
          const out = {slot: [slot.x + scrollX, slot.y + scrollY, slot.width, slot.height], arrows: {}};
          for (const a of document.querySelectorAll('.gb-stats__arrow')) {
            const k = [...a.classList].find(c => c.startsWith('gb-stats__arrow--')).slice(-3);
            const r = a.getBoundingClientRect(), cs = getComputedStyle(a);
            out.arrows[k] = {rect: [r.x + scrollX, r.y + scrollY, r.width, r.height],
                             left: cs.left, top: cs.top, width: cs.width};
          }
          return out; }""")
        pg.screenshot(path=live, full_page=True)
        b.close()

    board = np.array(Image.open(BOARD).convert("RGB")).astype(int)
    build = np.array(Image.open(live).convert("RGB")).astype(int)
    sx, sy, sw, sh = info["slot"]
    print(f"# bear slot: x={sx:.2f} y={sy:.2f} w={sw:.2f} h={sh:.2f}\n")

    print(f"{'arrow':<7}{'board ink':>20}{'build ink':>20}{'w ratio':>9}{'h ratio':>9}   new width   new left   new top")
    for k in ("--1", "--2", "--3", "--4"):
        bx, by, bw, bh = BOARD_INK[k]
        bi = ink_bbox(board, bx - 25, by - 25, bx + bw + 25, by + bh + 25,
                      seed=(bx + bw / 2, by + bh / 2))
        r = info["arrows"][k]["rect"]
        li = ink_bbox(build, r[0] - 25, r[1] - 25, r[0] + r[2] + 25, r[1] + r[3] + 25,
                      seed=(r[0] + r[2] / 2, r[1] + r[3] / 2))
        if bi is None or li is None:
            print(f"{k:<7} MISSING board={bi} build={li}")
            continue
        rw, rh = bi[2] / li[2], bi[3] / li[3]
        cur_w = float(info["arrows"][k]["width"].rstrip("px"))
        new_w = cur_w * (rw + rh) / 2
        # Both sides are anchored on the BEAR SLOT, not on raw page coords: the
        # stats block does not start at the same y in the build as on the board
        # (the sections above it differ), so a raw dy would fold that drift into
        # the arrow's own offset. 332:16221 is the board's slot, 207.82 x 254 at
        # (90.64, 1854.00) in screenshot coords -- the build's is 208 x 257.42.
        BOARD_SLOT = (90.64, 1854.00)
        bcx, bcy = bi[0] + bi[2] / 2, bi[1] + bi[3] / 2
        lcx, lcy = li[0] + li[2] / 2, li[1] + li[3] / 2
        dx = (bcx - BOARD_SLOT[0]) - (lcx - sx)
        dy = (bcy - BOARD_SLOT[1]) - (lcy - sy)
        cur_l = float(info["arrows"][k]["left"].rstrip("px"))
        cur_t = float(info["arrows"][k]["top"].rstrip("px"))
        nl = (cur_l + dx) / sw * 100
        nt = (cur_t + dy) / sh * 100
        bs = f"{bi[0]},{bi[1]} {bi[2]}x{bi[3]}"
        ls = f"{li[0]},{li[1]} {li[2]}x{li[3]}"
        print(f"{k:<7}{bs:>20}{ls:>20}{rw:>9.3f}{rh:>9.3f}   {new_w/sw*100:>8.2f}%  {nl:>8.2f}%  {nt:>8.2f}%")


main()
