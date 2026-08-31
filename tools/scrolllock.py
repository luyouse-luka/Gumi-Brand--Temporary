#!/usr/bin/env python3
"""Scroll-lock judge: opening any overlay must not move the page sideways.

    python3 tools/scrolllock.py

Locking the page with `overflow:hidden` removes the desktop scrollbar, which
widens the viewport by its width. Every element that reads that width moves.
The build measures --scrollbar-w before locking and pads it back -- this judge
checks the padding lands exactly once.

⚠ MUST run with the real scrollbar. Playwright launches headless chromium with
--hide-scrollbars, which makes innerWidth - clientWidth == 0: the freed width is
zero, nothing can shift, and every assertion here passes no matter how broken
the CSS is. The launch below drops that flag and the run aborts if the gap is
still 0, so the judge cannot report green from a viewport that has no scrollbar
to lose. (memory: headless-chromium-probe-limits, negative-assert-needs-liveness-guard)

Sampled: every VISIBLE element. Three exclusions, each for a reason:
  - the overlay being opened, and any other overlay sitting idle in the DOM: a
    fixed element's containing block is the viewport, and the viewport really did
    get wider, so growing by the scrollbar width is correct. They are invisible
    while closed, so checkVisibility() drops them without naming them.
  - marquee tracks: .gb-logo-scroll is animating, so it moves between the two
    samples on its own. Animations are paused (not killed -- killing would snap
    reveal blocks back to frame 0, see memory kill-animations-blanks-reveal-blocks)
    so the pause holds them at whatever frame they are on.
"""
import os
import sys

from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXE = os.path.expanduser("~/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome")

PAUSE = "*,*::before,*::after{animation-play-state:paused!important}"

RECTS = """(sel) => {
  const skip = sel ? document.querySelector(sel) : null;
  const out = {};
  const els = document.querySelectorAll('body, body *');
  for (let i = 0; i < els.length; i++) {
    const el = els[i];
    if (skip && (el === skip || skip.contains(el))) continue;
    if (el.tagName === 'SCRIPT' || el.tagName === 'STYLE') continue;
    // only what the viewer can actually see can read as a jump
    if (el.checkVisibility && !el.checkVisibility({checkOpacity: true,
                                                   checkVisibilityCSS: true})) continue;
    const r = el.getBoundingClientRect();
    if (r.width < 0.5) continue;
    const cs = getComputedStyle(el);
    const key = i + '|' + el.tagName + '.' + (el.className || '').toString().split(' ')[0]
                + '[' + cs.position + ']';
    out[key] = [Math.round(r.x * 100) / 100, Math.round(r.width * 100) / 100];
  }
  return out;
}"""

VIEW = """() => ({
  gap: window.innerWidth - document.documentElement.clientWidth,
  sbVar: getComputedStyle(document.documentElement).getPropertyValue('--scrollbar-w').trim(),
  dePad: getComputedStyle(document.documentElement).paddingRight,
  bodyPad: getComputedStyle(document.body).paddingRight,
})"""

# page, width, what to click, the overlay that legitimately resizes
CASES = [
    ("index",          1440, '[data-modal="nutritional-label"]', ".gb-nl-modal"),
    ("index",          1440, '[data-modal="reel-video"]',        ".gb-rv-modal"),
    ("pdp",            1440, '[data-modal="nutritional-label"]', ".gb-nl-modal"),
    ("reviews",        1440, '[data-modal="nutritional-label"]', ".gb-nl-modal"),
    ("how-gumi-works", 1440, '[data-modal="reel-video"]',        ".gb-rv-modal"),
    ("our-story",      1024, '[data-modal="nutritional-label"]', ".gb-nl-modal"),
    # the mobile drawer takes the same lock; 700 is inside `narrow` and still has
    # a real desktop scrollbar, which a phone's overlay scrollbar never does
    ("index",           700, ".gb-header__toggle",               ".gb-header__panel"),
    ("faq",             700, ".gb-header__toggle",               ".gb-header__panel"),
]

fails, checks = [], 0

with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path=EXE, ignore_default_args=["--hide-scrollbars"])
    for page, width, trigger, overlay in CASES:
        pg = br.new_page(viewport={"width": width, "height": 900})
        pg.goto(f"file://{ROOT}/{page}.html")
        pg.wait_for_timeout(700)
        pg.add_style_tag(content=PAUSE)

        v0 = pg.evaluate(VIEW)
        if v0["gap"] <= 0:
            print(f"ABORT {page}@{width}: no real scrollbar (innerWidth - clientWidth = "
                  f"{v0['gap']}). Every assertion would pass vacuously.")
            sys.exit(2)

        if not pg.query_selector(trigger):
            fails.append(f"{page}@{width} {trigger}: trigger not found")
            pg.close()
            continue

        before = pg.evaluate(RECTS, overlay)
        pg.eval_on_selector(trigger, "el => el.click()")
        pg.wait_for_timeout(700)
        v1 = pg.evaluate(VIEW)
        after = pg.evaluate(RECTS, overlay)

        tag = f"{page}@{width} {trigger}"
        checks += 1
        if v1["gap"] != 0:
            fails.append(f"{tag}: page not actually locked (gap still {v1['gap']})")
        checks += 1
        if v1["sbVar"] != f"{v0['gap']}px":
            fails.append(f"{tag}: --scrollbar-w is {v1['sbVar']!r}, measured gap was {v0['gap']}px")
        # the compensation belongs to the scrolling element alone
        checks += 1
        if v1["bodyPad"] not in ("0px", ""):
            fails.append(f"{tag}: body padding-right is {v1['bodyPad']} — width spent twice")

        moved = []
        for k, (x0, w0) in before.items():
            if k not in after:
                continue
            x1, w1 = after[k]
            if abs(x1 - x0) > 0.05 or abs(w1 - w0) > 0.05:
                moved.append((k, x0, x1, w0, w1))
        checks += 1
        if moved:
            fails.append(f"{tag}: {len(moved)} elements shifted, e.g. " +
                         "; ".join(f"{k.split('|')[1]} x {a}→{b} w {c}→{d}"
                                   for k, a, b, c, d in moved[:3]))
        print(f"{tag:<52} scrollbar {v0['gap']}px, "
              f"{len(before)} elements sampled, {len(moved)} shifted")
        pg.close()
    br.close()

print(f"\nscrolllock: {checks} assertions over {len(CASES)} cases, {len(fails)} failed")
for f in fails:
    print("  ✗ " + f)
sys.exit(1 if fails else 0)
