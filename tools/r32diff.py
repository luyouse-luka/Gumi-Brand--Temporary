#!/usr/bin/env python3
"""Overlay the 390 promo modal on its own board export and report per-line drift.

    python3 tools/r32diff.py

r32check.py asserts Figma numbers; this one asserts what actually gets painted.
Round 27 shipped a mobile bear that was on the wrong side of the panel with
every structural assertion green, so the two are not interchangeable.

Boards: 285-18988 (email) / 285-19179 (code), both 390x840 exports whose top
96px is a fake Chrome bar — cropped off here, leaving the 390x744 panel.

Three traps this script exists to avoid:
  * screenshotting straight after .click() leaves the pointer parked on the
    button, and in the code state the Copy button inherits that exact spot —
    the whole pill renders in its lime hover state (141 avg diff on that band).
  * the modal moves focus into the revealed state, so a keyboard/scripted
    submit paints a :focus-visible ring the board has no idea about. Mouse
    submit + blur is what a real user sees.
  * a colour mask is only as good as its tolerance. Measuring #666 text with
    tol 30 against #4d4d4d clipped the antialiased edges asymmetrically and
    invented a 3px width difference that is not there; the bands below name
    the colour they actually measure and keep tol loose enough to include the
    full ink but tight enough to exclude the background.

Every band is checked on both axes: a y drift is how the round-32 title
half-leading bug showed up (ink 1px high, box geometry perfect).
"""
import os, sys
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = os.path.expanduser("~/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome")
SHOTS = os.path.join(ROOT, "figma", "screenshots")
OUT = os.path.join(ROOT, "tools", "shots")

OPEN = """() => { const m = document.getElementById('promo-modal');
  m.classList.add('is-open'); m.setAttribute('aria-hidden', 'false'); }"""

GREEN, GRAY, MUTED, WHITE = (0, 86, 53), (77, 77, 77), (102, 102, 102), (255, 255, 255)
# label, colour, window x0 x1 y0 y1, tol on the colour mask, allowed |d| on the edges
# ±1 is the floor: Figma and Skia disagree by up to a pixel on where an
# antialiased stem ends, and every element in this panel sits inside that.
BANDS = [
    ("logo     ", GREEN, 130, 265,  10,  55, 60, 1),
    ("title  l1", GREEN,  20, 370, 126, 166, 60, 1),
    ("title  l2", GREEN,  20, 370, 168, 210, 60, 1),
    ("lead   l1", GRAY,   20, 370, 242, 263, 60, 1),
    ("lead   l2", GRAY,   20, 370, 264, 288, 60, 1),
    ("email ph ", GRAY,   44, 200, 326, 362, 60, 1),
    ("btn pill ", GREEN,  30, 360, 370, 426, 60, 1),
    ("btn label", WHITE, 100, 300, 385, 412, 60, 1),
]
# the "No thanks" line and its underline exist only in the email state. The
# underline is a character-level override in the board (styleOverrideTable),
# not on the node's own style — reading style.textDecoration says NONE.
EMAIL_ONLY = [
    ("dismiss  ", MUTED,  20, 370, 440, 456, 45, 1),
    ("underline",  MUTED, 20, 370, 456, 462, 90, 1),
]
MAX_MEAN_DIFF = 4.0   # whole-panel mean; antialiasing alone lands near 2.5

def shoot(pg, state):
    pg.evaluate(OPEN)
    pg.wait_for_timeout(600)
    if state == "code":
        pg.fill(".gb-promo-panel__input", "a@b.co")
        pg.click(".gb-promo-panel__submit")
        pg.mouse.move(5, 5)                        # off every hover box
        pg.evaluate("() => document.activeElement.blur()")   # no focus ring
        pg.wait_for_timeout(700)                   # let the transition unwind
    p = os.path.join(OUT, "r32diff-%s.png" % state)
    pg.locator(".gb-promo-panel").screenshot(path=p)
    return Image.open(p).convert("RGB")

def ink(a, rgb, x0, x1, y0, y1, tol):
    m = np.abs(a[y0:y1, x0:x1] - np.array(rgb)).max(axis=2) <= tol
    ys, xs = np.where(m)
    if not len(xs):
        return None
    return (xs.min() + x0, xs.max() + x0, ys.min() + y0, ys.max() + y0)

fails = []
os.makedirs(OUT, exist_ok=True)
with sync_playwright() as p:
    br = p.chromium.launch(executable_path=CHROME)
    for state, board_png in (("email", "285-18988_pop-up_390x840.png"),
                             ("code",  "285-19179_pop-up_390x840.png")):
        pg = br.new_page(viewport={"width": 390, "height": 744}, device_scale_factor=1)
        pg.goto("file://" + os.path.join(ROOT, "index.html"))
        pg.wait_for_timeout(2200)
        impl = shoot(pg, state)
        pg.close()

        board = Image.open(os.path.join(SHOTS, board_png)).convert("RGB").crop((0, 96, 390, 840))
        if impl.size != board.size:
            fails.append("%s: panel is %s, board is %s" % (state, impl.size, board.size))
            impl = impl.resize(board.size)
        a, b = np.asarray(board).astype(int), np.asarray(impl).astype(int)
        d = np.abs(a - b).max(axis=2)
        mean = d.mean()
        print("%-5s  mean diff %.2f   >32: %.2f%%" % (state, mean, 100 * (d > 32).mean()))
        if mean > MAX_MEAN_DIFF:
            fails.append("%s: mean diff %.2f over %.1f" % (state, mean, MAX_MEAN_DIFF))

        for label, rgb, x0, x1, y0, y1, tol, lim in BANDS + (EMAIL_ONLY if state == "email" else []):
            ib = ink(a, rgb, x0, x1, y0, y1, tol)
            ii = ink(b, rgb, x0, x1, y0, y1, tol)
            if ib is None or ii is None:
                fails.append("%s %s: no ink (board %s, impl %s)" % (state, label, ib, ii))
                continue
            dd = [ii[i] - ib[i] for i in range(4)]
            line = ("  %s  board x[%3d,%3d] y[%3d,%3d]  impl x[%3d,%3d] y[%3d,%3d]"
                    "  dx%+d/%+d dy%+d/%+d" % ((label,) + ib + ii + tuple(dd)))
            if max(abs(v) for v in dd) > lim:
                fails.append("%s %s: dx%+d/%+d dy%+d/%+d over +-%d" % ((state, label) + tuple(dd) + (lim,)))
                print(line + "   FAIL")
            else:
                print(line)
    br.close()

if fails:
    print("\nFAIL (%d)" % len(fails))
    for f in fails: print("  " + f)
    sys.exit(1)
print("\nr32diff OK — both states overlay their board within +-1px on every band")
