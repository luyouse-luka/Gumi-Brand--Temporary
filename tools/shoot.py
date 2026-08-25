#!/usr/bin/env python3
"""Full-page screenshots + the two regressions that keep coming back.

    python3 tools/shoot.py science.html 1440 390
    python3 tools/shoot.py --all            # every page at every width

Checks, per width:
  * horizontal overflow — documentElement.scrollWidth vs clientWidth, plus the
    widest offending element so the report points at something.
  * stuck .wowo — the entrance class leaves opacity:0 until main.js adds
    .animated, so a script error hides content permanently. The page is scrolled
    in 400px steps first; a single jump to the bottom never puts the middle of
    the page in the viewport and reports false positives (11th round).

Shots land in tools/shots/ and are not part of the handoff.
"""
import os, sys, glob
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "tools", "shots")
CHROME = os.path.expanduser("~/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome")
# 断点改制后（2026-08-21）：手机 ≤575 / 平板 576–1280 / PC ≥1281。
# 每档取两端 + 中间一个，边界两侧各取一格，专抓「差一像素就塌」。
# 断点边界两侧各取一档（r29 起含 767/768 与 991/992）
WIDTHS = [360, 390, 575, 576, 767, 768, 991, 992, 1024, 1200, 1280, 1281, 1440, 1920]

PROBE = """() => {
  const de = document.documentElement;
  const over = [];
  if (de.scrollWidth > de.clientWidth + 1) {
    for (const el of document.querySelectorAll('body *')) {
      const r = el.getBoundingClientRect();
      if (r.right > de.clientWidth + 1 || r.left < -1) {
        over.push({ sel: el.tagName.toLowerCase() + '.' + (el.className || '').toString().split(' ')[0],
                    left: Math.round(r.left), right: Math.round(r.right) });
      }
    }
  }
  const stuck = [];
  for (const el of document.querySelectorAll('.wowo')) {
    // Elements the breakpoint hides never enter the viewport, so their opacity
    // legitimately stays 0 — counting them reports a stuck class that is not one.
    if (el.offsetParent === null && getComputedStyle(el).position !== 'fixed') continue;
    if (parseFloat(getComputedStyle(el).opacity) < 0.5) {
      stuck.push(el.className.toString().slice(0, 60));
    }
  }
  return { scrollWidth: de.scrollWidth, clientWidth: de.clientWidth,
           over: over.slice(0, 6), stuck, height: de.scrollHeight };
}"""


def run(pages, widths):
    os.makedirs(OUT, exist_ok=True)
    bad = 0
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=CHROME)
        for page_file in pages:
            for w in widths:
                pg = br.new_page(viewport={"width": w, "height": 900},
                                 device_scale_factor=1)
                pg.goto("file://" + os.path.join(ROOT, page_file))
                pg.wait_for_timeout(400)
                h = pg.evaluate("document.documentElement.scrollHeight")
                y = 0
                while y < h:
                    pg.evaluate(f"window.scrollTo(0, {y})")
                    pg.wait_for_timeout(60)
                    y += 400
                # wowo plays 0.7s then drops its classes at 1500ms; shooting
                # before that catches half-played words and reads as "ghosting".
                pg.wait_for_timeout(1700)
                pg.evaluate("window.scrollTo(0, 0)")
                pg.wait_for_timeout(600)
                r = pg.evaluate(PROBE)
                stem = os.path.splitext(os.path.basename(page_file))[0]
                pg.screenshot(path=os.path.join(OUT, f"{stem}-{w}.png"), full_page=True)
                flag = ""
                if r["scrollWidth"] > r["clientWidth"] + 1:
                    flag += f"  OVERFLOW {r['scrollWidth']}>{r['clientWidth']} {r['over']}"
                    bad += 1
                if r["stuck"]:
                    flag += f"  STUCK-WOWO {len(r['stuck'])} {r['stuck'][:3]}"
                    bad += 1
                print(f"{stem:22} {w:5}  h={r['height']:6}{flag or '  ok'}")
                pg.close()
        br.close()
    return bad


if __name__ == "__main__":
    args = sys.argv[1:]
    if args[:1] == ["--all"]:
        pages = [os.path.basename(f) for f in sorted(glob.glob(os.path.join(ROOT, "*.html")))
                 if not f.endswith("font-check.html")]
        widths = WIDTHS
    else:
        pages = [a for a in args if a.endswith(".html")]
        widths = [int(a) for a in args if a.isdigit()] or WIDTHS
    sys.exit(1 if run(pages, widths) else 0)
