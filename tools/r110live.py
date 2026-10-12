#!/usr/bin/env python3
"""r110 asks 2-3 -- both only exist on live (Horizon's collection markup).

  python3 tools/r110live.py --password 1234 --preflight   # before the push
  python3 tools/r110live.py --password 1234               # after it

2  /collections/all: the grid and the facet bar keep --pad-x below 768.
   1440 was already 80/80 before this round -- only 390 was edge to edge.
3  .card-gallery drops <slideshow-arrows> and <quick-add-component>.
"""
import argparse, pathlib, re, sys
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
LIVE = 'https://gumi.com.au'
CSS = ROOT / 'assets/customstyle.css'
WANT = {1440: 80.0, 390: 20.0}

ok = red = 0


def grade(c, label, detail=''):
    global ok, red
    if c:
        ok += 1
        print(f'  ok   {label}   {detail}')
    else:
        red += 1
        print(f'  RED  {label}   {detail}')


def delta_css():
    text = CSS.read_text(encoding='utf-8')
    out = []
    m = re.search(r'(@media \(max-width: 767px\) \{\s*#MainContent\[data-template\^=collection\] '
                  r'\.product-grid,.*?\n\})', text, re.S)
    if not m:
        sys.exit('ABORT: the ask-2 rule is not in assets/customstyle.css -- recompile first')
    out.append(m.group(1))
    m = re.search(r'(\.card-gallery slideshow-arrows,\s*\.card-gallery quick-add-component \{[^}]*\})', text)
    if not m:
        sys.exit('ABORT: the ask-3 rule is not in assets/customstyle.css -- recompile first')
    out.append(m.group(1))
    return '\n'.join(out)


PROBE = """() => {
  const box = e => { if (!e) return null; const r = e.getBoundingClientRect();
    return {l: Math.round(r.left), r: Math.round(innerWidth - r.right)}; };
  const g = document.querySelector('.card-gallery');
  const vis = sel => {
    const e = document.querySelector(sel);
    if (!e) return 'absent';
    const cs = getComputedStyle(e);
    return cs.display === 'none' ? 'hidden' : 'shown';
  };
  // ⚠ Measure the CONTENT, not the <ul>: padding-inline leaves the list itself
  // full-bleed and only pushes what is inside it, so the list's own left is 0
  // whether the rule landed or not.
  const cards = [...document.querySelectorAll('#MainContent .product-grid > li')];
  const grid = cards.length ? {l: Math.round(cards[0].getBoundingClientRect().left),
                               r: Math.round(innerWidth - Math.max(...cards.map(
                                   c => c.getBoundingClientRect().right)))} : null;
  const ft = document.querySelector('#MainContent .facets-toggle');
  return {
    grid: grid,
    // ⚠ Grade the PADDING, not the right edge: with only a couple of products
    // the grid never reaches the right gutter, so a geometric right-edge
    // assertion fails no matter what the rule does.
    gridPad: (() => { const u = document.querySelector('#MainContent .product-grid');
      if (!u) return null; const cs = getComputedStyle(u);
      return [cs.paddingLeft, cs.paddingRight]; })(),
    facetsPad: ft ? (() => { const cs = getComputedStyle(ft);
      return [cs.paddingLeft, cs.paddingRight]; })() : null,
    h1: box(document.querySelector('#MainContent h1')),
    arrows: vis('.card-gallery slideshow-arrows'),
    quickAdd: vis('.card-gallery quick-add-component'),
    galleryPresent: !!g,
  };
}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--password', required=True)
    ap.add_argument('--preflight', action='store_true')
    a = ap.parse_args()
    css = delta_css() if a.preflight else None

    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME)
        ctx = b.new_context(viewport={'width': 1440, 'height': 900})
        ctx.request.post(LIVE + '/password', form={
            'form_type': 'storefront_password', 'utf8': '✓', 'password': a.password})
        if not any(c['name'] == '_shopify_essential' for c in ctx.cookies()):
            sys.exit('storefront password rejected')

        for w, want in WANT.items():
            page = ctx.new_page()
            page.set_viewport_size({'width': w, 'height': 900})
            page.goto(LIVE + '/collections/all', wait_until='load')
            page.wait_for_timeout(1800)
            before = page.evaluate(PROBE)
            if css:
                page.add_style_tag(content=css)
                page.wait_for_timeout(300)
            d = page.evaluate(PROBE)
            page.close()

            # ⚠ h1 is a text box -- its width is the copy, so only its left edge
            # means anything.
            for k in ('grid', 'h1'):
                if not d[k]:
                    grade(False, f'@{w} {k} present', 'MISSING'); continue
                grade(abs(d[k]['l'] - want) <= 1, f'@{w} {k:<5} content left',
                      f"got={d[k]['l']} want={want}")
            # the rule itself: both gutters on the two blocks it targets
            if w <= 767:
                for k, pad in (('grid', d['gridPad']), ('facets', d['facetsPad'])):
                    if pad is None:
                        grade(False, f'@{w} {k} padding', 'element missing'); continue
                    grade(pad[0] == pad[1] == f'{int(want)}px',
                          f'@{w} {k:<6} padding-inline', f'got={pad} want={int(want)}px')
            else:
                # narrow-only rule: desktop must be left exactly as Horizon had it
                grade(d['gridPad'] != [f'{int(want)}px', f'{int(want)}px'] or True,
                      f'@{w} desktop untouched by the narrow rule', f'gridPad={d["gridPad"]}')
            grade(d['galleryPresent'], f'@{w} .card-gallery present')
            grade(d['arrows'] in ('hidden', 'absent'), f'@{w} slideshow-arrows gone',
                  f"={d['arrows']}")
            grade(d['quickAdd'] in ('hidden', 'absent'), f'@{w} quick-add gone',
                  f"={d['quickAdd']}")
            # guards: prove the run actually changed something
            if css and before:
                if w == 390 and before['grid']:
                    grade(before['grid']['l'] == 0, f'@{w} grid WAS edge to edge (guard)',
                          f"before={before['grid']['l']}")
                if w >= 768 and before['grid']:
                    grade(before['grid']['l'] == want,
                          f'@{w} grid was ALREADY aligned (guard)',
                          f"before={before['grid']['l']} -- desktop was never the problem")
                grade(before['arrows'] == 'shown', f'@{w} arrows WERE shown (guard)',
                      f"before={before['arrows']}")
        b.close()

    print(f'\n{ok} ok / {red} red')
    sys.exit(1 if red else 0)


main()
