#!/usr/bin/env python3
"""Can an in-flow Gumi Wave reproduce the board's --bleed boundary?

  python3 tools/r105bleed.py

The index nutrition -> product boundary is the one the r104 migration could not
restore: the board hangs the wave off the TOP of gb-product (--edge-top) with
--bleed, so the arcs are white and the gaps between them are see-through, and
what shows through is the lime block plus the pack art overrunning it.

An in-flow wave sits BELOW nutrition, so a transparent top shows the page ground
instead. The proposal under test: pull the wave back over nutrition with a
negative margin-top equal to its own height.

Method -- on the static build, so the reference and the candidate are the same
page at the same width:
  reference  the board's own wave, as shipped
  candidate  that wave removed, and a sibling wave inserted after nutrition with
             the in-flow geometry live has, plus the negative margin
Then compare rendered pixels down the boundary. Identical columns mean the
candidate is a faithful stand-in; the pack art showing through is the point, so
the sample runs across a band wide enough to include it.
"""
import sys
from playwright.sync_api import sync_playwright

CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
PAGE = 'file:///home/ly/project/Gumi-Brand/index.html'
WIDTHS = (390, 768, 1440)

# Geometry of the boundary, plus a pixel strip, read the same way in both modes.
MEASURE = """() => {
  const nut = document.querySelector('.gb-nutrition');
  const prod = document.querySelector('.gb-product');
  const w = document.querySelector('.gb-scallop--bleed, .gb-wave-probe');
  if (!nut || !prod || !w) return null;
  const nr = nut.getBoundingClientRect(), pr = prod.getBoundingClientRect(),
        wr = w.getBoundingClientRect();
  const sy = window.scrollY;
  return {
    waveTop: +(wr.top + sy).toFixed(1), waveH: +wr.height.toFixed(1),
    nutBottom: +(nr.bottom + sy).toFixed(1), prodTop: +(pr.top + sy).toFixed(1),
    // what the boundary costs the page: nutrition's end to product's start
    seam: +(pr.top - nr.bottom).toFixed(1),
    pageH: +document.documentElement.scrollHeight.toFixed(1),
  };
}"""

# Replace the board's wave with the live shape: a sibling block after nutrition,
# in flow, transparent on top, pulled back over nutrition by its own height.
REBUILD = """() => {
  const board = document.querySelector('.gb-scallop--bleed');
  const nut = document.querySelector('.gb-nutrition');
  if (!board || !nut) return false;
  const h = getComputedStyle(board).height;
  board.remove();
  const sec = document.createElement('div');
  sec.className = 'gb-wave-section';
  const d = document.createElement('div');
  d.className = 'gb-scallop gb-wave gb-wave--lg gb-wave-probe';
  // the two things --bleed does, as the section would set them inline
  d.style.setProperty('--wave-bg', 'transparent');
  d.style.setProperty('--wave-under', 'transparent');
  d.style.setProperty('--wave-fg', '#ffffff');
  // The proposal: lap back over the block above instead of taking its own room.
  // +1px because .gb-scallop is drawn one pixel taller than --wave-h (the
  // fractional-dpr hairline guard) and pays it back with margin-bottom:-1px.
  sec.style.marginTop = `calc(-1 * ${h} + 1px)`;
  sec.style.position = 'relative';
  sec.appendChild(d);
  nut.parentNode.insertBefore(sec, nut.nextSibling);
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
            pg.goto(PAGE, wait_until='domcontentloaded')
            pg.wait_for_timeout(400)
            ref = pg.evaluate(MEASURE)
            ref_shot = pg.screenshot(full_page=True, clip={
                'x': 0, 'y': max(0, ref['nutBottom'] - ref['waveH'] - 40),
                'width': w, 'height': ref['waveH'] + 80})

            pg.goto(PAGE, wait_until='domcontentloaded')
            pg.wait_for_timeout(400)
            built = pg.evaluate(REBUILD)
            grade(built, f'{w}: rebuilt the boundary in the live shape')
            pg.wait_for_timeout(200)
            cand = pg.evaluate(MEASURE)
            cand_shot = pg.screenshot(full_page=True, clip={
                'x': 0, 'y': max(0, cand['nutBottom'] - cand['waveH'] - 40),
                'width': w, 'height': cand['waveH'] + 80})

            print(f'\n--- {w} ---')
            print(f"  board  wave h={ref['waveH']:<7} top={ref['waveTop']:<9} "
                  f"nut.bottom={ref['nutBottom']:<9} prod.top={ref['prodTop']:<9} seam={ref['seam']}")
            print(f"  live+  wave h={cand['waveH']:<7} top={cand['waveTop']:<9} "
                  f"nut.bottom={cand['nutBottom']:<9} prod.top={cand['prodTop']:<9} seam={cand['seam']}")
            grade(abs(ref['waveH'] - cand['waveH']) < 0.5, f'{w}: same wave height',
                  f"{ref['waveH']} vs {cand['waveH']}")
            grade(abs(ref['seam'] - cand['seam']) < 0.5, f'{w}: same seam cost',
                  f"{ref['seam']} vs {cand['seam']}")
            grade(abs(ref['pageH'] - cand['pageH']) < 1.5, f'{w}: page height unchanged',
                  f"{ref['pageH']} vs {cand['pageH']}")
            same = ref_shot == cand_shot
            grade(same, f'{w}: the boundary renders pixel-identical',
                  'screenshots differ' if not same else '')
            print(f"  pixels {'identical' if same else 'DIFFER'}  "
                  f"({len(ref_shot)} vs {len(cand_shot)} bytes)")
        br.close()
    print(f'\n{ok} ok / {red} red')
    return 1 if red else 0


if __name__ == '__main__':
    sys.exit(main())
