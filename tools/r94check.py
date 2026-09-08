#!/usr/bin/env python3
"""r94 assertions: .gb-product top paddings swapped, .gb-vs card floor.

  python3 tools/r94check.py                           # static site (file://)
  python3 tools/r94check.py --as-served --password X  # live storefront
  python3 tools/r94check.py --strip                   # liveness self-check

Two things this round:
  1. Client reversal of r89: the base .gb-product goes back to the board's ramp
     (96 desktop / 52 mobile / fluid between) and .gb-product--page drops to 32
     on desktop. The tablet tier had to follow --page down to 32 or 1280 -> 1281
     steps 64px. --page's mobile 20 is the board's and was not named, so it
     stayed; --lg never moved.
  2. .gb-vs__table's trailing track is minmax(25px, 1fr). It used to be a bare
     1fr, so the card's overhang under the last row was whatever min-height
     minus content happened to be -- 0 across all of 768-1024 (where `stack`
     zeroes min-height) and 0 again by 1281 as the copy wrapped taller.

⚠ The base .gb-product has NO live counterpart: sections/gb-product.liquid emits
only `--lg` or `--page`, so tier 1's base half is graded on the static build.

⚠ --strip restores the old values as INLINE style, not by deleting CSSOM rules:
under file:// every sheet's cssRules throws on access (the r93 self-check was
silently a no-op because of it). Each strip returns how many elements it
touched, and a zero count is itself a RED.
"""
import argparse

from playwright.sync_api import sync_playwright

CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
ROOT = 'file:///home/ly/project/Gumi-Brand'
LIVE = 'https://gumi.com.au'

WIDTHS = [390, 575, 767, 768, 900, 1024, 1200, 1280, 1281, 1440]

# The board leaves 25px of lime card below the last row on both boards
# (324:53792 mobile, and the 448-high desktop card over 423 of rows).
FLOOR = 25.0
# 1440 has room to spare inside the 448 board height, and keeping that is the
# point of the 1fr half of minmax -- assert it did not get clipped to the floor.
BOARD_CARD_H = 448.0


class Report:
    def __init__(self):
        self.ok = self.red = 0

    def check(self, tag, got, want):
        good = got == want
        self.ok, self.red = self.ok + good, self.red + (not good)
        print(f"  {'ok  ' if good else 'RED '} {tag}" + ('' if good else f"   got={got!r} want={want!r}"))

    def near(self, tag, got, want, tol):
        good = got is not None and abs(got - want) <= tol
        self.ok, self.red = self.ok + good, self.red + (not good)
        print(f"  {'ok  ' if good else 'RED '} {tag}" + ('' if good else f"   got={got!r} want={want}±{tol}"))

    def atleast(self, tag, got, floor, tol=0.6):
        good = got is not None and got >= floor - tol
        self.ok, self.red = self.ok + good, self.red + (not good)
        print(f"  {'ok  ' if good else 'RED '} {tag}" + ('' if good else f"   got={got!r} want>={floor}"))


JS_PAD = """(sel) => {
  const el = document.querySelector(sel);
  return el ? parseFloat(getComputedStyle(el).paddingTop) : null;
}"""

JS_VS = """() => {
  const col = document.querySelector('.gb-vs__col--gumi');
  if (!col) return null;
  const rows = [...col.querySelectorAll('.gb-vs__row')];
  if (!rows.length) return null;
  const cr = col.getBoundingClientRect();
  const bf = getComputedStyle(col, '::before');
  const cardBottom = cr.top + parseFloat(bf.top) + parseFloat(bf.height);
  return {
    gap: +(cardBottom - rows[rows.length - 1].getBoundingClientRect().bottom).toFixed(2),
    cardH: +parseFloat(bf.height).toFixed(2),
  };
}"""

# Old values, re-applied inline so the fix assertions must go red.
JS_STRIP_PROD = """() => {
  let n = 0;
  for (const el of document.querySelectorAll('.gb-product')) {
    const page = el.classList.contains('gb-product--page');
    const lg = el.classList.contains('gb-product--lg');
    const w = window.innerWidth;
    let v;
    if (page) v = w <= 767 ? 20 : w >= 1281 ? 96 : 20 + (96 - 20) * (w - 768) / (1280 - 768);
    else if (lg) continue;
    else v = 32;
    el.style.paddingTop = v + 'px';
    n++;
  }
  return n;
}"""

JS_STRIP_VS = """() => {
  const t = document.querySelector('.gb-vs__table');
  if (!t) return 0;
  t.style.gridTemplateRows = 'repeat(19, auto) 1fr';
  return 1;
}"""


def source_checks(rep):
    import io, pathlib, re
    root = pathlib.Path(__file__).resolve().parent.parent
    scss = io.open(root / 'assets/customstyle.scss', encoding='utf-8').read()
    css = io.open(root / 'assets/customstyle.css', encoding='utf-8').read()
    print('== source ==')
    rep.check('s1 $build at or past r94',
              re.search(r'\$build:\s*"([^"]+)"', scss).group(1) >= '20260908-r94', True)
    # Dual write: the shipped css must carry the same trailing track as the source.
    rep.check('s2 scss floors the trailing track',
              'repeat(19, auto) minmax(25px, 1fr)' in scss, True)
    rep.check('s3 css floors the trailing track',
              'repeat(19, auto) minmax(25px, 1fr)' in css, True)
    rep.check('s4 no bare `repeat(19, auto) 1fr` left', 'repeat(19, auto) 1fr' in css, False)


def run(rep, base, strip):
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=CHROME)
        ctx = br.new_context(viewport={'width': 1440, 'height': 900})
        yield ctx, br


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--as-served', action='store_true')
    ap.add_argument('--password')
    ap.add_argument('--strip', action='store_true')
    a = ap.parse_args()

    rep = Report()
    if not a.as_served:
        source_checks(rep)

    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=CHROME)
        ctx = br.new_context(viewport={'width': 1440, 'height': 900})
        if a.as_served:
            if a.password:
                ctx.request.post(LIVE + '/password', form={
                    'form_type': 'storefront_password', 'utf8': '✓', 'password': a.password})
                if not any(c['name'] == '_shopify_essential' for c in ctx.cookies()):
                    raise SystemExit('storefront password rejected (no _shopify_essential)')
            pdp = LIVE + '/products/superfood-greens-gummies'
            plain = None            # no live route emits a bare .gb-product
        else:
            pdp = ROOT + '/pdp.html'
            plain = ROOT + '/how-gumi-works.html'

        pg = ctx.new_page()
        touched = {'prod': 0, 'vs': 0}

        # -- tier 1: --page ramps 20 -> 32, and never reads 96 ------------------
        print('\n== .gb-product--page top padding ==')
        pg.goto(pdp, wait_until='domcontentloaded')
        page_vals = {}
        for w in WIDTHS:
            pg.set_viewport_size({'width': w, 'height': 900})
            pg.wait_for_timeout(120)
            if a.strip:
                touched['prod'] += pg.evaluate(JS_STRIP_PROD)
            page_vals[w] = pg.evaluate(JS_PAD, '.gb-product--page')
        for w in (390, 575, 767, 768):
            rep.near(f'1 --page {w} board 20', page_vals[w], 20.0, 0.5)
        for w in (1281, 1440):
            rep.near(f'1 --page {w} client 32', page_vals[w], 32.0, 0.5)
        # The ramp must be monotone and land on 32, or the tier steps at 1281.
        mid = [page_vals[w] for w in (768, 900, 1024, 1200, 1280)]
        rep.check('1b --page ramp monotone', mid == sorted(mid), True)
        rep.near('1b --page ramp lands on 32 at 1280', page_vals[1280], 32.0, 0.6)
        rep.near('1b --page no step across 1281',
                 abs(page_vals[1281] - page_vals[1280]), 0.0, 0.6)

        # -- tier 1: the base class, static only -------------------------------
        if plain:
            print('\n== .gb-product base top padding (static only) ==')
            pg.goto(plain, wait_until='domcontentloaded')
            base_vals = {}
            for w in WIDTHS:
                pg.set_viewport_size({'width': w, 'height': 900})
                pg.wait_for_timeout(120)
                if a.strip:
                    touched['prod'] += pg.evaluate(JS_STRIP_PROD)
                base_vals[w] = pg.evaluate(JS_PAD, '.gb-product')
            for w in (390, 575, 767, 768):
                rep.near(f'2 base {w} board 52', base_vals[w], 52.0, 0.5)
            for w in (1281, 1440):
                rep.near(f'2 base {w} board 96', base_vals[w], 96.0, 0.5)
            mid = [base_vals[w] for w in (768, 900, 1024, 1200, 1280)]
            rep.check('2b base ramp monotone', mid == sorted(mid), True)
            rep.near('2b base no step across 1281',
                     abs(base_vals[1281] - base_vals[1280]), 0.0, 0.6)
            # The reversal's whole point: base must sit ABOVE --page everywhere.
            for w in WIDTHS:
                rep.check(f'2c base > --page at {w}', base_vals[w] > page_vals[w], True)

        # -- tier 2: the lime card never meets the last row --------------------
        print('\n== .gb-vs card overhang under the last row ==')
        pg.goto(pdp, wait_until='domcontentloaded')
        for w in WIDTHS:
            pg.set_viewport_size({'width': w, 'height': 900})
            pg.wait_for_timeout(150)
            if a.strip:
                touched['vs'] += pg.evaluate(JS_STRIP_VS)
                pg.wait_for_timeout(60)
            r = pg.evaluate(JS_VS)
            if r is None:
                rep.check(f'3 {w} vs table present', False, True)
                continue
            rep.atleast(f'3 {w} card clears the last row by {FLOOR}', r['gap'], FLOOR)
            if w == 1440:
                # 1fr still wins where the board height leaves room; clipping to
                # the floor here would mean minmax swallowed the 448 card.
                rep.near('3b 1440 keeps the board card height', r['cardH'], BOARD_CARD_H, 1.0)

        if a.strip:
            print('\n== strip liveness ==')
            rep.check('strip touched .gb-product', touched['prod'] > 0, True)
            rep.check('strip touched .gb-vs__table', touched['vs'] > 0, True)

        br.close()

    print(f"\n{rep.ok} ok / {rep.red} red")
    raise SystemExit(1 if rep.red and not a.strip else 0)


if __name__ == '__main__':
    main()
