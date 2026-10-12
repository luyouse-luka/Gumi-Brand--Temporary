#!/usr/bin/env python3
"""r106 on live: the two asks whose hook only exists there.

  python3 tools/r106live.py --password 1234 --preflight   # before the push
  python3 tools/r106live.py --password 1234               # after it

  9   /collections/all — Horizon's Inter/black H1 and its 16/40 gutters.
  10  index nutrition -> product — the room the block above has to leave for a
      wave it cannot see (live models it as a Gumi Wave section carrying --lap;
      the static build as the next section's --edge-top child, which r106check
      covers).

--preflight injects THIS ROUND'S OWN RULES, lifted verbatim out of the compiled
assets/customstyle.css, into the live page. Both blocks are purely additive at
the end of the file, so an appended copy lands exactly where the pushed file
would. It is a rehearsal, not a substitute: rerun without the flag afterwards.
"""
import argparse, pathlib, re, sys
from playwright.sync_api import sync_playwright

CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
LIVE = 'https://gumi.com.au'
CSS = pathlib.Path('assets/customstyle.css')

ok = red = 0


def grade(c, label, detail=''):
    global ok, red
    if c:
        ok += 1
    else:
        red += 1
        print(f'  RED  {label}   {detail}')


def near(a, b, tol=0.8):
    return a is not None and b is not None and abs(a - b) <= tol


def delta_css():
    """The r106 rules, cut out of the shipped file by their own selectors."""
    text = CSS.read_text(encoding='utf-8')
    out = []
    # ask 10: four flat rules, contiguous
    m = re.search(r'(:where\(section, div, footer\):has\(\+ \* > \.gb-scallop--edge-top\).*?'
                  r':where\(section, div, footer\):has\(\+ \* > \.gb-wave--lg\.gb-wave--lap\) \{[^}]*\})',
                  text, re.S)
    if not m:
        sys.exit('ABORT: the ask-10 rules are not in assets/customstyle.css -- recompile first')
    out.append(m.group(1))
    # ask 9: the block plus its two media queries, up to .gb-404
    m = re.search(r'(#MainContent\[data-template\^=collection\] \{.*?)\n\n\.gb-404 ', text, re.S)
    if not m:
        sys.exit('ABORT: the ask-9 rules are not in assets/customstyle.css -- recompile first')
    out.append(m.group(1))
    return '\n'.join(out)


COLL = """() => {
  const h1 = document.querySelector('h1');
  const main = document.querySelector('#MainContent');
  const content = document.querySelector('.section--page-width .custom-section-content')
                || document.querySelector('.custom-section-content');
  // .product-grid exactly: .product-grid-container is the full-bleed section
  // around it and never moves, so it would read green either way.
  const grid = document.querySelector('.product-grid');
  const facets = document.querySelector('.facets-block-wrapper');
  const cs = h1 && getComputedStyle(h1);
  const r = e => e ? +e.getBoundingClientRect().width.toFixed(1) : null;
  const l = e => e ? +e.getBoundingClientRect().left.toFixed(1) : null;
  return {
    template: main && main.getAttribute('data-template'),
    pageMargin: main ? getComputedStyle(main).getPropertyValue('--page-margin').trim() : null,
    padX: getComputedStyle(document.documentElement).getPropertyValue('--pad-x').trim(),
    h1: cs && {font: cs.fontFamily.split(',')[0].replace(/"/g, ''), size: cs.fontSize,
               weight: cs.fontWeight, lh: cs.lineHeight, ls: cs.letterSpacing,
               color: cs.color, left: l(h1)},
    contentW: r(content), contentLeft: l(content),
    gridW: r(grid), gridLeft: l(grid), facetsLeft: l(facets),
    // a product card's own type must NOT have moved -- the .text-block selector
    // is scoped to h1 precisely so the card names keep Horizon's own size.
    cardType: (() => { const c = document.querySelector('.product-grid .text-block');
                       if (!c) return null;
                       const s = getComputedStyle(c);
                       return {size: s.fontSize, font: s.fontFamily.split(',')[0].replace(/"/g, '')}; })(),
  };
}"""

NUT = """() => {
  const n = document.querySelector('.gb-nutrition');
  const p = document.querySelector('.gb-product');
  const band = document.querySelector('.gb-nutrition__band');
  const wave = document.querySelector('.gb-wave--lap');
  if (!n || !p || !wave) return null;
  const cs = getComputedStyle(n), r = e => e.getBoundingClientRect();
  return {padB: +parseFloat(cs.paddingBottom).toFixed(2),
          scRes: cs.getPropertyValue('--sc-res').trim() || '(unset)',
          waveH: +r(wave).height.toFixed(2),
          seam: +(r(p).top - r(n).bottom).toFixed(2),
          bandOver: +(r(band).bottom - r(n).bottom).toFixed(2),
          nutBottom: +(r(n).bottom + window.scrollY).toFixed(2),
          waveTop: +(r(wave).top + window.scrollY).toFixed(2)};
}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--password', required=True)
    ap.add_argument('--preflight', action='store_true')
    a = ap.parse_args()
    css = delta_css() if a.preflight else None

    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=CHROME)
        ctx = br.new_context(viewport={'width': 1440, 'height': 900})
        ctx.request.post(LIVE + '/password', form={
            'form_type': 'storefront_password', 'utf8': '✓', 'password': a.password})
        if not any(c['name'] == '_shopify_essential' for c in ctx.cookies()):
            sys.exit('storefront password rejected')
        pg = ctx.new_page()

        def go(path, w):
            pg.set_viewport_size({'width': w, 'height': 900})
            pg.goto(LIVE + path, wait_until='domcontentloaded', timeout=90000)
            pg.wait_for_timeout(1100)
            if css:
                pg.add_style_tag(content=css)
                pg.wait_for_timeout(200)

        print('--- 9. /collections/all ---')
        for w in (1440, 768, 390):
            go('/collections/all', w)
            m = pg.evaluate(COLL)
            grade(m['template'] and m['template'].startswith('collection'),
                  f'{w}: the data-template hook is there', str(m['template']))
            want_pad = 80.0 if w >= 1281 else (20.0 if w <= 767 else None)
            grade(m['h1']['font'] == 'PP Palma', f'{w}: H1 is the brand face', m['h1']['font'])
            grade(m['h1']['color'] == 'rgb(0, 86, 53)', f'{w}: and the brand green', m['h1']['color'])
            want_size = 56.0 if w >= 1281 else (30.0 if w <= 767 else None)
            if want_size:
                grade(near(float(m['h1']['size'][:-2]), want_size, 0.5),
                      f'{w}: H1 {want_size}px like every other page', m['h1']['size'])
            if want_pad:
                grade(near(m['contentLeft'], want_pad), f'{w}: content starts at --pad-x',
                      f"left {m['contentLeft']} vs {want_pad}")
                # ⚠ Only above 767. The grid and the filter bar run full-bleed on
                # phones because collection.json's main section carries
                # full_width_on_mobile:true -- measured left 0 both before and
                # after this change, so asserting --pad-x there would fail on a
                # theme-editor setting nobody asked to touch.
                if w >= 768:
                    for tag, got in (('product grid', m['gridLeft']),
                                     ('filter bar', m['facetsLeft'])):
                        grade(got is None or near(got, want_pad),
                              f'{w}: and so does the {tag}', f'left {got} vs {want_pad}')
                else:
                    grade(m['gridLeft'] == 0 and m['facetsLeft'] == 0,
                          f'{w}: the grid stays full-bleed (full_width_on_mobile, unchanged)',
                          f"grid {m['gridLeft']} facets {m['facetsLeft']}")
            print(f"  {w:>5}  h1 {m['h1']['font']} {m['h1']['size']}/{m['h1']['weight']} "
                  f"{m['h1']['color']}  content {m['contentW']}@{m['contentLeft']}  "
                  f"grid {m['gridW']}@{m['gridLeft']}  facets@{m['facetsLeft']}")

        print('--- 10. index nutrition -> product ---')
        for w in (1440, 1024, 768, 390):
            go('/', w)
            m = pg.evaluate(NUT)
            if not m:
                grade(False, f'{w}: found nutrition, product and the --lap wave')
                continue
            lap = 9.0 if w <= 767 else (0.0 if w >= 1281 else 9.0 * (1281 - w) / 513)
            grade(m['padB'] > 0, f'{w}: .gb-nutrition reserves something at all', str(m['padB']))
            grade(near(m['padB'], m['waveH'] - 1 - lap, 1.2),
                  f'{w}: and it is the wave below it, less the board lap',
                  f"padB {m['padB']} vs wave {m['waveH']} - 1 - {lap:.1f}")
            grade(near(m['waveTop'], m['nutBottom'] - m['waveH'] + 1, 1.5),
                  f'{w}: the wave still laps back over the block above',
                  f"wave top {m['waveTop']} vs nutrition bottom {m['nutBottom']}")
            print(f"  {w:>5}  padB {m['padB']:<9} wave {m['waveH']:<9} "
                  f"seam {m['seam']:<7} band over {m['bandOver']}")
        br.close()
    tag = '   [PREFLIGHT: rules injected, not pushed]' if a.preflight else ''
    print(f'\n{ok} ok / {red} red{tag}')
    return 1 if red else 0


if __name__ == '__main__':
    sys.exit(main())
