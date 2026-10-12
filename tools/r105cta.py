#!/usr/bin/env python3
"""What moving the footer-CTA wave out of its wrapper costs.

  python3 tools/r105cta.py

The board draws that wave INSIDE .gb-footer-cta-wrap, as the first thing in the
flow. Turning it into a Gumi Wave section moves it OUT, above the wrapper -- and
both decorative bears are positioned against that wrapper:

  .gb-deco-bear--a  top: -100px       (overhangs the wrapper upward)
  .gb-deco-bear--b  top: 71.087%      (percentage of the wrapper's own height)

So the wrapper's top edge moves down by the wave's height and its height shrinks
by the same amount, and both bears follow. This measures how far.

Three modes on the same page at the same width:
  board    as shipped
  moved    wave lifted out, sitting above the wrapper in the flow
  lapped   same, plus the r104 .gb-wave--lap margin so the wrapper keeps its box
"""
import sys
from playwright.sync_api import sync_playwright

CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
PAGE = 'file:///home/ly/project/Gumi-Brand/index.html'
WIDTHS = (390, 768, 1440)

MEASURE = """() => {
  const wrap = document.querySelector('.gb-footer-cta-wrap');
  const a = document.querySelector('.gb-deco-bear--a');
  const b = document.querySelector('.gb-deco-bear--b');
  const w = document.querySelector('.gb-footer-cta-wrap .gb-scallop, .gb-cta-wave-probe .gb-scallop');
  const sy = window.scrollY, r = e => e.getBoundingClientRect();
  if (!wrap || !a || !b || !w) return null;
  return {
    wrapTop: +(r(wrap).top + sy).toFixed(1), wrapH: +r(wrap).height.toFixed(1),
    bearA: +(r(a).top + sy).toFixed(1), bearB: +(r(b).top + sy).toFixed(1),
    waveTop: +(r(w).top + sy).toFixed(1), waveH: +r(w).height.toFixed(1),
    pageH: +document.documentElement.scrollHeight.toFixed(1),
  };
}"""

# Lift the wave out into a sibling block above the wrapper -- the shape it would
# have as its own Gumi Wave section.
LIFT = """(lap) => {
  const wrap = document.querySelector('.gb-footer-cta-wrap');
  const wave = wrap && wrap.querySelector(':scope > .gb-scallop');
  if (!wave) return false;
  const sec = document.createElement('div');
  sec.className = 'gb-wave-section gb-cta-wave-probe';
  wave.classList.add('gb-wave', 'gb-wave--sm');
  if (lap) wave.style.marginTop = 'calc(-1 * var(--wave-h))';
  sec.appendChild(wave);
  wrap.parentNode.insertBefore(sec, wrap);
  return true;
}"""


def main():
    ok = red = 0

    def grade(c, label, detail=''):
        nonlocal ok, red
        if c:
            ok += 1
        else:
            red += 1
            print(f'  RED  {label}   {detail}')

    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=CHROME)
        pg = br.new_context(viewport={'width': 1440, 'height': 900}).new_page()
        for w in WIDTHS:
            pg.set_viewport_size({'width': w, 'height': 900})
            modes = {}
            for name, lap in (('board', None), ('moved', False), ('lapped', True)):
                pg.goto(PAGE, wait_until='domcontentloaded')
                pg.wait_for_timeout(400)
                if lap is not None:
                    grade(pg.evaluate(LIFT, lap), f'{w}/{name}: lifted the wave out')
                    pg.wait_for_timeout(150)
                modes[name] = pg.evaluate(MEASURE)

            print(f'\n--- {w} ---')
            bd = modes['board']
            for name in ('board', 'moved', 'lapped'):
                m = modes[name]
                print(f"  {name:<7} wrap.top={m['wrapTop']:<9} wrap.h={m['wrapH']:<8} "
                      f"bearA={m['bearA']:<9} bearB={m['bearB']:<9} "
                      f"wave.top={m['waveTop']:<9} pageH={m['pageH']}")
            mv, lp = modes['moved'], modes['lapped']
            print(f"  drift  moved:  bearA {mv['bearA'] - bd['bearA']:+.1f}  "
                  f"bearB {mv['bearB'] - bd['bearB']:+.1f}  pageH {mv['pageH'] - bd['pageH']:+.1f}")
            print(f"         lapped: bearA {lp['bearA'] - bd['bearA']:+.1f}  "
                  f"bearB {lp['bearB'] - bd['bearB']:+.1f}  pageH {lp['pageH'] - bd['pageH']:+.1f}")
            # The wave itself must land where the board puts it, in both modes.
            grade(abs(mv['waveTop'] - bd['waveTop']) < 0.5, f'{w}/moved: wave in the same place',
                  f"{mv['waveTop']} vs {bd['waveTop']}")
            grade(abs(mv['bearA'] - bd['bearA']) < 0.5, f'{w}/moved: bear A did not move',
                  f"{mv['bearA'] - bd['bearA']:+.1f}px")
            grade(abs(mv['bearB'] - bd['bearB']) < 0.5, f'{w}/moved: bear B did not move',
                  f"{mv['bearB'] - bd['bearB']:+.1f}px")
            grade(abs(mv['pageH'] - bd['pageH']) < 1.5, f'{w}/moved: page height unchanged',
                  f"{mv['pageH'] - bd['pageH']:+.1f}px")
        br.close()
    print(f'\n{ok} ok / {red} red')
    return 1 if red else 0


if __name__ == '__main__':
    sys.exit(main())
