#!/usr/bin/env python3
"""r105: the two CSS mechanisms this round adds, checked on the static build.

  python3 tools/r105check.py

1  .gb-wave--lap  the bleed boundary. A wave carrying it must take no room of its
   own (its section collapses) and must land exactly where the board's
   --edge-top --bleed wave sits, so the block above shows through the arcs.

2  --cta-wave-h   the footer-CTA compensation. Live lifted that wave out of
   .gb-footer-cta-wrap, which is what both decorative bears are positioned
   against. With the compensation the wrapper keeps the board's own box, so both
   bears stay put and the CTA copy does not move.

Live's DOM shape is built here rather than waited for: the static build has no
.shopify-section wrappers, and these rules key on them.
"""
import sys
from playwright.sync_api import sync_playwright

CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
PAGE = 'file:///home/ly/project/Gumi-Brand/index.html'
WIDTHS = (390, 575, 768, 1024, 1440)

BLEED_MEASURE = """() => {
  const nut = document.querySelector('.gb-nutrition');
  const prod = document.querySelector('.gb-product');
  const w = document.querySelector('.gb-scallop--bleed, .gb-wave--lap');
  if (!nut || !prod || !w) return null;
  const sy = window.scrollY, r = e => e.getBoundingClientRect();
  const sec = w.closest('.gb-wave-section');
  return {
    waveTop: +(r(w).top + sy).toFixed(1), waveH: +r(w).height.toFixed(1),
    secH: sec ? +r(sec).height.toFixed(1) : null,
    secTop: sec ? +(r(sec).top + sy).toFixed(1) : null,
    seam: +(r(prod).top - r(nut).bottom).toFixed(1),
    pageH: +document.documentElement.scrollHeight.toFixed(1),
  };
}"""

# Replace the board's bleed wave with the live shape, using the real class.
BLEED_REBUILD = """() => {
  const board = document.querySelector('.gb-scallop--bleed');
  const nut = document.querySelector('.gb-nutrition');
  if (!board || !nut) return false;
  board.remove();
  const sec = document.createElement('div');
  sec.className = 'gb-wave-section';
  const d = document.createElement('div');
  d.className = 'gb-scallop gb-wave gb-wave--lg gb-wave--lap';
  d.style.setProperty('--wave-bg', 'transparent');
  d.style.setProperty('--wave-under', 'transparent');
  d.style.setProperty('--wave-fg', '#ffffff');
  sec.appendChild(d);
  nut.parentNode.insertBefore(sec, nut.nextSibling);
  return true;
}"""

CTA_MEASURE = """() => {
  const wrap = document.querySelector('.gb-footer-cta-wrap');
  const cta = document.querySelector('.gb-footer-cta');
  const a = document.querySelector('.gb-deco-bear--a');
  const b = document.querySelector('.gb-deco-bear--b');
  if (!wrap || !cta || !a || !b) return null;
  const r = e => e.getBoundingClientRect();
  return {
    wrapH: +r(wrap).height.toFixed(1),
    // distances from the CTA copy: what the eye actually reads
    aFromCta: +(r(a).top - r(cta).top).toFixed(1),
    bFromCta: +(r(b).top - r(cta).top).toFixed(1),
    pageH: +document.documentElement.scrollHeight.toFixed(1),
  };
}"""

# Live's shape: the wave becomes its own .gb-wave-section, and the wrapper gets
# the .gb-footer-cta-section host Shopify gives it.
CTA_REBUILD = """() => {
  const wrap = document.querySelector('.gb-footer-cta-wrap');
  const wave = wrap && wrap.querySelector(':scope > .gb-scallop');
  if (!wave) return false;
  const host = document.createElement('section');
  host.className = 'shopify-section gb-footer-cta-section';
  wrap.parentNode.insertBefore(host, wrap);
  const sec = document.createElement('section');
  sec.className = 'shopify-section gb-wave-section';
  wave.classList.add('gb-wave', 'gb-wave--sm');
  sec.appendChild(wave);
  host.parentNode.insertBefore(sec, host);
  host.appendChild(wrap);
  return true;
}"""

ok = red = 0


def grade(c, label, detail=''):
    global ok, red
    if c:
        ok += 1
    else:
        red += 1
        print(f'  RED  {label}   {detail}')


def main():
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=CHROME)
        pg = br.new_context(viewport={'width': 1440, 'height': 900}).new_page()

        print('--- 1. .gb-wave--lap reproduces the board bleed boundary ---')
        for w in WIDTHS:
            pg.set_viewport_size({'width': w, 'height': 900})
            pg.goto(PAGE, wait_until='domcontentloaded')
            pg.wait_for_timeout(400)
            ref = pg.evaluate(BLEED_MEASURE)
            ref_shot = pg.screenshot(full_page=True, clip={
                'x': 0, 'y': max(0, ref['waveTop'] - 30), 'width': w, 'height': ref['waveH'] + 60})

            pg.goto(PAGE, wait_until='domcontentloaded')
            pg.wait_for_timeout(400)
            grade(pg.evaluate(BLEED_REBUILD), f'{w}: rebuilt the boundary in the live shape')
            pg.wait_for_timeout(150)
            cand = pg.evaluate(BLEED_MEASURE)
            cand_shot = pg.screenshot(full_page=True, clip={
                'x': 0, 'y': max(0, cand['waveTop'] - 30), 'width': w, 'height': cand['waveH'] + 60})

            grade(abs(cand['secTop'] - cand['waveTop']) < 0.5,
                  f'{w}: the section is pulled up onto the block above',
                  f"section top {cand['secTop']} vs wave top {cand['waveTop']}")
            grade(abs(ref['waveTop'] - cand['waveTop']) < 0.5, f'{w}: wave lands where the board puts it',
                  f"{ref['waveTop']} vs {cand['waveTop']}")
            grade(abs(ref['seam'] - cand['seam']) < 0.5, f'{w}: same seam',
                  f"{ref['seam']} vs {cand['seam']}")
            grade(abs(ref['pageH'] - cand['pageH']) < 1.5, f'{w}: page height unchanged',
                  f"{ref['pageH']} vs {cand['pageH']}")
            same = ref_shot == cand_shot
            grade(same, f'{w}: the boundary renders pixel-identical', 'screenshots differ')
            print(f"  {w:>5}  wave {cand['waveH']:<7} section {cand['secH']:<5} "
                  f"seam {cand['seam']:<5} pixels {'identical' if same else 'DIFFER'}")

        print('\n--- 2. --cta-wave-h keeps the wrapper box, so the bears stay put ---')
        for w in WIDTHS:
            pg.set_viewport_size({'width': w, 'height': 900})
            pg.goto(PAGE, wait_until='domcontentloaded')
            pg.wait_for_timeout(400)
            ref = pg.evaluate(CTA_MEASURE)

            pg.goto(PAGE, wait_until='domcontentloaded')
            pg.wait_for_timeout(400)
            grade(pg.evaluate(CTA_REBUILD), f'{w}: rebuilt the CTA in the live shape')
            pg.wait_for_timeout(150)
            cand = pg.evaluate(CTA_MEASURE)

            grade(abs(ref['wrapH'] - cand['wrapH']) < 0.5, f'{w}: wrapper keeps the board height',
                  f"{ref['wrapH']} vs {cand['wrapH']}")
            grade(abs(ref['aFromCta'] - cand['aFromCta']) < 0.5, f'{w}: bear A stays put',
                  f"{ref['aFromCta']} vs {cand['aFromCta']}  (drift {cand['aFromCta'] - ref['aFromCta']:+.1f})")
            grade(abs(ref['bFromCta'] - cand['bFromCta']) < 0.5, f'{w}: bear B stays put',
                  f"{ref['bFromCta']} vs {cand['bFromCta']}  (drift {cand['bFromCta'] - ref['bFromCta']:+.1f})")
            grade(abs(ref['pageH'] - cand['pageH']) < 1.5, f'{w}: page height unchanged',
                  f"{ref['pageH']} vs {cand['pageH']}")
            print(f"  {w:>5}  wrapH {ref['wrapH']} -> {cand['wrapH']}   "
                  f"bearA {ref['aFromCta']} -> {cand['aFromCta']}   "
                  f"bearB {ref['bFromCta']} -> {cand['bFromCta']}")
        br.close()
    print(f'\n{ok} ok / {red} red')
    return 1 if red else 0


if __name__ == '__main__':
    sys.exit(main())
