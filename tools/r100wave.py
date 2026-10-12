#!/usr/bin/env python3
"""Geometry check for .gb-wave: does "3 waves" actually draw 3 arcs?

  python3 tools/r100wave.py

Arc count = container width / --wave-w. The pitch is (100vw - scrollbar) / N, so
the count should come out at exactly N at every width, and the height should be
the arc amplitude (pitch * 0.24008) plus the near-zero band.

⚠ Headless reports --scrollbar-w as 0, so the subtraction itself cannot be
verified here -- this checks the arithmetic, not the desktop scrollbar case.
The last block forces a non-zero --scrollbar-w to prove the CSS responds to it.
"""
import pathlib, sys
from playwright.sync_api import sync_playwright

CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
CSS = pathlib.Path('/home/ly/project/Gumi-Brand/assets/customstyle.css')
WIDTHS = [1920, 1440, 1280, 991, 768, 575, 390]

PAGE = """<!doctype html><meta charset=utf-8>
<style>%s</style>
<style>body{margin:0}</style>
<div class="gb-scallop gb-wave gb-scallop--white-to-cream" id="w3" style="--wave-n:3"></div>
<div class="gb-scallop gb-wave gb-scallop--white-to-cream" id="w5" style="--wave-n:5"></div>
<div class="gb-scallop gb-wave gb-scallop--down gb-scallop--white-to-cream" id="d3" style="--wave-n:3"></div>
<div class="gb-scallop gb-scallop--white-to-cream" id="base"></div>
"""
PROBE = """() => {
  const out = {};
  for (const id of ['w3','w5','d3','base']) {
    const e = document.getElementById(id);
    const cs = getComputedStyle(e);
    const pitch = parseFloat(cs.backgroundSize.split(',')[0]);
    out[id] = {w: e.getBoundingClientRect().width, h: e.getBoundingClientRect().height,
               pitch, arcs: e.getBoundingClientRect().width / pitch,
               img: cs.backgroundImage.slice(0, 60)};
  }
  return out;
}"""

ok = red = 0
def grade(c, label, detail=''):
    global ok, red
    if c: ok += 1; print(f'  ok   {label}')
    else: red += 1; print(f'  RED  {label}   {detail}')

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=CHROME)
    pg = b.new_page()
    pg.set_content(PAGE % CSS.read_text(encoding='utf-8'))
    for w in WIDTHS:
        pg.set_viewport_size({'width': w, 'height': 700})
        pg.wait_for_timeout(60)
        g = pg.evaluate(PROBE)
        print(f'\n--- {w}px ---')
        for wid, n in (('w3', 3), ('w5', 5), ('d3', 3)):
            d = g[wid]
            grade(abs(d['arcs'] - n) < 0.02, f'{w:5} {wid} draws {n} arcs',
                  f'got {d["arcs"]:.3f} (pitch {d["pitch"]:.2f})')
            amp = d['pitch'] * 0.24008
            grade(abs(d['h'] - (amp + 1)) < 3.0, f'{w:5} {wid} height ~ amplitude',
                  f'h={d["h"]:.1f} amp={amp:.1f}')
            print(f'       .. pitch {d["pitch"]:7.2f}  h {d["h"]:6.1f}')
        # the built-in waves must keep the design pitch, not the new one
        grade(abs(g['base']['arcs'] - 3) > 0.05 and abs(g['base']['arcs'] - 5) > 0.05
              or w < 500,
              f'{w:5} built-in .gb-scallop keeps its own pitch',
              f'arcs {g["base"]["arcs"]:.3f} pitch {g["base"]["pitch"]:.2f}')
        # direction actually changes the paint
        grade(g['d3']['img'] != g['w3']['img'], f'{w:5} --down paints differently')

    # scrollbar compensation: headless has none, so force one and check response
    print('\n--- --scrollbar-w responds (forced 15px) ---')
    pg.set_viewport_size({'width': 1440, 'height': 700})
    before = pg.evaluate("() => parseFloat(getComputedStyle(document.getElementById('w3')).backgroundSize)")
    pg.evaluate("() => document.documentElement.style.setProperty('--scrollbar-w','15px')")
    pg.wait_for_timeout(50)
    after = pg.evaluate("() => parseFloat(getComputedStyle(document.getElementById('w3')).backgroundSize)")
    grade(abs(before - after - 5) < 0.02, 'pitch drops by exactly 15/3 = 5px',
          f'{before:.3f} -> {after:.3f}')
    b.close()
print(f'\n{ok} ok / {red} red')
sys.exit(1 if red else 0)
