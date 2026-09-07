#!/usr/bin/env python3
"""r93 assertions: compare avatar/icon alignment, expert card heights, hero fade.

  python3 tools/r93check.py                          # static site (file://)
  python3 tools/r93check.py --as-served --password X # live storefront
  python3 tools/r93check.py --strip                  # liveness self-check

Three things this round:
  1. .gb-compare__avatars tracks now ramp with .gb-compare__avatar across the
     768-1280 tier. Before, the track stayed at the desktop 96px while the image
     ramped from 66, so the icons below sat up to 56.7px off the avatars.
  2. .gb-expert-card gets height: auto in the rail tier. .swiper-slide sets
     height: 100%, a non-auto cross size, which stops align-self: stretch.
  3. sections/gb-page-hero.liquid carries `wowo fadeIn delay-in-1` (the static
     pages have had it all along; the live section never did).

The static pages ship one quote length for all three expert cards, so the
uneven-height case only exists live. --strip aside, the static run injects the
live copy mix (193/82/82 chars) before measuring.
"""
import argparse

from playwright.sync_api import sync_playwright

CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
LIVE = 'https://gumi.com.au'

# Both boards place the icons a few px off the avatars by hand (1440: -2.5/+2.0,
# 390: -3.28/+1.78). That offset is the design's, so the assertion is that the
# tier between them interpolates inside it -- not that the centres coincide.
D2_RANGE = (-3.40, -2.40)
D3_RANGE = (1.70, 2.10)

WIDTHS = [390, 575, 767, 768, 900, 1024, 1200, 1280, 1281, 1440]

SHORT_QUOTE = '"Gumi is the easiest way I have found to keep my daily vitamins on track."'

JS_COMPARE = """() => {
  const av = [...document.querySelectorAll('.gb-compare__avatar')];
  const row = document.querySelector('.gb-compare__row');
  if (av.length < 2 || !row) return null;
  const mk = [...row.querySelectorAll('.gb-compare__mark')];
  const wrap = document.querySelector('.gb-compare__avatars');
  const mid = el => { const r = el.getBoundingClientRect(); return r.left + r.width / 2; };
  const tracks = getComputedStyle(wrap).gridTemplateColumns.split(' ').map(parseFloat);
  return {
    d2: +(mid(mk[0]) - mid(av[0])).toFixed(2),
    d3: +(mid(mk[1]) - mid(av[1])).toFixed(2),
    track2: tracks[1], track3: tracks[2],
    avW: +av[0].getBoundingClientRect().width.toFixed(2),
  };
}"""

JS_EXPERT = """() => {
  const cards = [...document.querySelectorAll('.gb-expert-card')];
  if (!cards.length) return null;
  return {
    h: cards.map(c => +c.getBoundingClientRect().height.toFixed(1)),
    quoteLen: cards.map(c => {
      const q = c.querySelector('.gb-expert-card__quote');
      return q ? q.textContent.trim().length : 0;
    }),
    trackH: +document.querySelector('.gb-expert__cards').getBoundingClientRect().height.toFixed(1),
  };
}"""

JS_INJECT = """(short) => {
  const q = [...document.querySelectorAll('.gb-expert-card__quote')];
  q.slice(1).forEach(el => { el.textContent = short; });
  return q.length;
}"""

JS_HERO = """() => {
  const m = document.querySelector('.gb-page-hero__media');
  if (!m) return null;
  return { cls: m.className.split(/\\s+/).filter(Boolean) };
}"""

# Undo each fix so a passing run proves the rules are what holds the assertions
# up (CLAUDE.md rule 6). Written as inline style, not a CSSOM edit: under
# file:// every sheet's cssRules throws on access, so a rule-walking strip is
# silently a no-op and every assertion stays green. Each strip returns how many
# elements it touched and a zero count is itself a RED.
JS_STRIP_COMPARE = """(w) => {
  if (w < 768 || w > 1280) return -1;          // tier the fix applies to
  const el = document.querySelector('.gb-compare__avatars');
  if (!el) return 0;
  el.style.gridTemplateColumns = '1fr 96px 96px';   // the pre-r93 desktop value
  return 1;
}"""

JS_STRIP_EXPERT = """(w) => {
  if (w > 991) return -1;                      // tier the fix applies to
  const cards = [...document.querySelectorAll('.gb-expert-card')];
  cards.forEach(c => { c.style.height = '100%'; });  // .swiper-slide's own value
  return cards.length;
}"""


class Report:
    def __init__(self):
        self.ok = 0
        self.red = []

    def check(self, cond, label):
        if cond:
            self.ok += 1
        else:
            self.red.append(label)
        return cond

    def done(self):
        print(f"\n{self.ok} ok / {len(self.red)} red")
        for r in self.red:
            print(f"  RED  {r}")
        return 1 if self.red else 0


def run(pg, rep, url_science, url_reviews, inject, strip, tag):
    for w in WIDTHS:
        pg.set_viewport_size({'width': w, 'height': 900})
        pg.goto(url_science, wait_until='load')
        pg.wait_for_timeout(350)
        if strip:
            n = pg.evaluate(JS_STRIP_COMPARE, w)
            rep.check(n != 0, f"[{tag}] strip compare @{w}: touched nothing")
            pg.wait_for_timeout(120)
        d = pg.evaluate(JS_COMPARE)
        if d is None:
            rep.check(False, f"[{tag}] {w}: science has no .gb-compare")
            continue
        rep.check(D2_RANGE[0] <= d['d2'] <= D2_RANGE[1],
                  f"[{tag}] compare col2 @{w}: d2={d['d2']} outside {D2_RANGE}")
        rep.check(D3_RANGE[0] <= d['d3'] <= D3_RANGE[1],
                  f"[{tag}] compare col3 @{w}: d3={d['d3']} outside {D3_RANGE}")
        # The track has to equal the image it holds, or the <picture> grid item
        # is wider than the <img> and the image parks at its left edge.
        rep.check(abs(d['track2'] - d['avW']) <= 0.6,
                  f"[{tag}] compare track2 @{w}: {d['track2']} vs avatar {d['avW']}")
        rep.check(abs(d['track3'] - d['avW']) <= 0.6,
                  f"[{tag}] compare track3 @{w}: {d['track3']} vs avatar {d['avW']}")

    for w in WIDTHS:
        pg.set_viewport_size({'width': w, 'height': 900})
        pg.goto(url_reviews, wait_until='load')
        pg.wait_for_timeout(350)
        if inject:
            pg.evaluate(JS_INJECT, SHORT_QUOTE)
        if strip:
            n = pg.evaluate(JS_STRIP_EXPERT, w)
            rep.check(n != 0, f"[{tag}] strip expert @{w}: touched nothing")
        pg.wait_for_timeout(200)
        d = pg.evaluate(JS_EXPERT)
        if d is None:
            rep.check(False, f"[{tag}] {w}: reviews has no .gb-expert-card")
            continue
        spread = max(d['h']) - min(d['h'])
        rep.check(spread <= 0.5,
                  f"[{tag}] expert heights @{w}: {d['h']} spread {spread:.1f}")
        # Levelling must not add height: the rail is already as tall as its
        # tallest card, so the track height is the invariant here.
        rep.check(abs(d['trackH'] - max(d['h'])) <= 0.6,
                  f"[{tag}] expert track @{w}: {d['trackH']} vs tallest {max(d['h'])}")
        # A run where every quote is the same length proves nothing.
        rep.check(len(set(d['quoteLen'])) > 1,
                  f"[{tag}] expert copy @{w}: all quotes same length {d['quoteLen']}, "
                  f"the uneven case was never exercised")

    for url, name in ((url_science, 'science'), (url_reviews, 'reviews')):
        pg.set_viewport_size({'width': 1440, 'height': 900})
        pg.goto(url, wait_until='load')
        pg.wait_for_timeout(300)
        d = pg.evaluate(JS_HERO)
        if d is None:
            rep.check(False, f"[{tag}] {name}: no .gb-page-hero__media")
            continue
        for cls in ('wowo', 'fadeIn', 'delay-in-1'):
            rep.check(cls in d['cls'],
                      f"[{tag}] {name} hero media missing .{cls} (has {d['cls']})")


def source_checks(rep):
    scss = open('assets/customstyle.scss', encoding='utf-8').read()
    css = open('assets/customstyle.css', encoding='utf-8').read()
    liq = open('liquid/sections/gb-page-hero.liquid', encoding='utf-8').read()
    rep.check(scss.count('grid-template-columns: 1fr fluid(66px, 96px) fluid(66px, 96px)') == 1,
              'scss: avatars tablet track missing')
    rep.check(css.count('grid-template-columns: 1fr clamp(66px') == 1,
              'css: avatars tablet track missing (dual write)')
    rep.check('height: auto;' in scss.split('.gb-expert-card {')[1].split('}')[0]
              or 'height: auto' in scss.split('.gb-expert-card {')[1][:1200],
              'scss: .gb-expert-card height: auto missing')
    rep.check(css.count('height: auto') >= 1, 'css: height: auto missing (dual write)')
    rep.check('gb-page-hero__media wowo fadeIn delay-in-1' in liq,
              'liquid: hero media missing wowo classes')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--as-served', action='store_true', help='run against the live storefront')
    ap.add_argument('--password', help='storefront password (live only)')
    ap.add_argument('--strip', action='store_true', help='remove the fixes; every fix assertion should go red')
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
            science, reviews, inject, tag = (
                LIVE + '/pages/science', LIVE + '/pages/reviews', False, 'live')
        else:
            base = 'file:///home/ly/project/Gumi-Brand/'
            science, reviews, inject, tag = (
                base + 'science.html', base + 'reviews.html', True, 'static')
        pg = ctx.new_page()
        run(pg, rep, science, reviews, inject, a.strip, tag)
        br.close()

    raise SystemExit(rep.done())


if __name__ == '__main__':
    main()
