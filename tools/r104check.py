#!/usr/bin/env python3
"""r104: the three changes of this round, on the static build.

  python3 tools/r104check.py

1  .gb-wave--sm / --lg render at exactly the height of the built-in small / large
   waves. That equality is the whole point: live already pads the block above by
   the net value, so a wave of the board's height restores the board's gap too.
2  .gb-sub__banner is a block box and its text still sits centred.
3  .gb-dosed__inner keeps an 80px gap at every tier, mobile included.

The wave is injected rather than read off an existing node -- no static page has
a .gb-wave on it, that class only exists on live.
"""
import sys
from playwright.sync_api import sync_playwright

CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
BASE = 'file:///home/ly/project/Gumi-Brand'
TIERS = [390, 575, 767, 768, 1024, 1280, 1440, 1920]

WAVE_PROBE = """() => {
  const mk = (cls) => {
    const d = document.createElement('div');
    d.className = 'gb-scallop gb-wave ' + cls;
    document.body.appendChild(d);
    const h = d.getBoundingClientRect().height;
    const w = getComputedStyle(d).getPropertyValue('--wave-w').trim();
    d.remove();
    return {h: +h.toFixed(2), w};
  };
  // What the built-in waves resolve to on this page, at this width.
  const probe = (cls) => {
    const d = document.createElement('div');
    d.className = 'gb-scallop ' + cls;
    document.body.appendChild(d);
    const h = d.getBoundingClientRect().height;
    const w = getComputedStyle(d).getPropertyValue('--wave-w').trim();
    d.remove();
    return {h: +h.toFixed(2), w};
  };
  return {
    waveSm: mk('gb-wave--sm'), waveLg: mk('gb-wave--lg'),
    waveN5: mk(''),                       // no size class -> the arc-count route
    builtinSm: probe(''), builtinLg: probe('gb-scallop--lg'),
  };
}"""

BANNER_PROBE = """() => {
  const el = document.querySelector('.gb-sub__banner');
  if (!el) return null;
  const cs = getComputedStyle(el), r = el.getBoundingClientRect();
  const range = document.createRange();
  range.selectNodeContents(el);
  const tr = range.getBoundingClientRect();
  return {display: cs.display, textAlign: cs.textAlign,
          w: +r.width.toFixed(1), h: +r.height.toFixed(1),
          // distance from the text ink to each edge -- equal means still centred
          left: +(tr.left - r.left).toFixed(1), right: +(r.right - tr.right).toFixed(1)};
}"""

DOSED_PROBE = """() => {
  const el = document.querySelector('.gb-dosed__inner');
  if (!el) return null;
  const kids = [...el.children].filter(k => k.getBoundingClientRect().height > 1);
  const gaps = [];
  for (let i = 1; i < kids.length; i++)
    gaps.push(+(kids[i].getBoundingClientRect().top - kids[i - 1].getBoundingClientRect().bottom).toFixed(1));
  return {gap: getComputedStyle(el).rowGap, measured: gaps};
}"""

ok = red = 0


def grade(cond, label, detail=''):
    global ok, red
    if cond:
        ok += 1
    else:
        red += 1
        print(f'  RED  {label}   {detail}')


def main():
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=CHROME)
        pg = br.new_context(viewport={'width': 1440, 'height': 900}).new_page()

        print('--- 1. gb-wave--sm / --lg match the built-in waves ---')
        pg.goto(f'{BASE}/index.html', wait_until='domcontentloaded')
        for w in TIERS:
            pg.set_viewport_size({'width': w, 'height': 900})
            pg.wait_for_timeout(120)
            r = pg.evaluate(WAVE_PROBE)
            # Height AND pitch. Height alone passes a wave whose arcs are the
            # wrong width, since height reads --wave-h and never --wave-w.
            for tag, mine, built in (('sm', r['waveSm'], r['builtinSm']),
                                     ('lg', r['waveLg'], r['builtinLg'])):
                grade(abs(mine['h'] - built['h']) < 0.5,
                      f'{w}: gb-wave--{tag} height == built-in', f"{mine['h']} vs {built['h']}")
                grade(mine['w'] == built['w'],
                      f'{w}: gb-wave--{tag} pitch == built-in', f"{mine['w']} vs {built['w']}")
            # The arc-count route must be left alone: same class, no size class.
            grade(abs(r['waveN5']['h'] - r['builtinSm']['h']) > 1,
                  f'{w}: the arc-count route is still its own size',
                  f"{r['waveN5']['h']} vs built-in {r['builtinSm']['h']}")
            print(f"  {w:>5}  sm {r['waveSm']['h']:>7} == {r['builtinSm']['h']:<7} "
                  f"lg {r['waveLg']['h']:>7} == {r['builtinLg']['h']:<7} (count route {r['waveN5']['h']})")

        print('\n--- 2. .gb-sub__banner is a block ---')
        pg.goto(f'{BASE}/pdp.html', wait_until='domcontentloaded')
        for w in (390, 768, 1440):
            pg.set_viewport_size({'width': w, 'height': 900})
            pg.wait_for_timeout(120)
            b = pg.evaluate(BANNER_PROBE)
            if not b:
                grade(False, f'{w}: .gb-sub__banner found')
                continue
            grade(b['display'] == 'block', f'{w}: display is block', b['display'])
            grade(b['textAlign'] == 'center', f'{w}: text-align still centre', b['textAlign'])
            grade(abs(b['left'] - b['right']) < 1.5,
                  f'{w}: text still centred in the box', f"left {b['left']} right {b['right']}")
            print(f"  {w:>5}  {b['display']:<6} box {b['w']}x{b['h']}  ink inset {b['left']} / {b['right']}")

        print('\n--- 3. .gb-dosed__inner gap is 80 at every tier ---')
        pg.goto(f'{BASE}/how-gumi-works.html', wait_until='domcontentloaded')
        for w in TIERS:
            pg.set_viewport_size({'width': w, 'height': 900})
            pg.wait_for_timeout(120)
            d = pg.evaluate(DOSED_PROBE)
            if not d:
                grade(False, f'{w}: .gb-dosed__inner found')
                continue
            grade(d['gap'] == '80px', f'{w}: computed row-gap is 80px', d['gap'])
            grade(all(abs(g - 80) < 0.5 for g in d['measured']),
                  f'{w}: measured gaps are 80', str(d['measured']))
            print(f"  {w:>5}  {d['gap']:<8} measured {d['measured']}")

        br.close()
    print(f'\n{ok} ok / {red} red')
    return 1 if red else 0


if __name__ == '__main__':
    sys.exit(main())
