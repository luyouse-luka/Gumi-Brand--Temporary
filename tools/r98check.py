#!/usr/bin/env python3
"""r98: the expert rail dead-ends, and the arrows grey out at each end.

  python3 tools/r98check.py           # static site
  python3 tools/r98check.py --strip   # liveness self-check: must go RED

`data-slider-rewind` is gone from the rail, which is what switches slider.sync()
on -- it early-returns for any rail that loops or rewinds. The disabled styling
(.gb-reels__btn[disabled]) has existed since r70 and had never once fired,
because every rail on the site was one or the other.

⚠ 767 is the case that broke the first attempt: three 305px cards in a 768 track
still move, but activeIndex never leaves 1, so `slideChange` never fires and the
arrows stayed live at both ends. sync() is now also bound to `transitionEnd`.

⚠ Read the arrows AFTER a settle. opacity is transitioned, so a read taken while
it is still running returns the START value ([[headless-transition-reads-start-value]]).
"""
import argparse
from playwright.sync_api import sync_playwright

CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
ROOT = 'file:///home/ly/project/Gumi-Brand'
DIM = 0.35

STATE = """() => {
  const t = document.querySelector('.gb-expert__cards');
  const root = t.closest('[data-slider]');
  const one = s => { const e = root.querySelector(s);
    const cs = getComputedStyle(e);
    return {off: e.disabled, op: +parseFloat(cs.opacity).toFixed(3), cur: cs.cursor}; };
  const r = t.getBoundingClientRect();
  const spans = [...t.querySelectorAll('.swiper-slide')].map(s => s.getBoundingClientRect())
    .map(b => [Math.max(b.left, r.left), Math.min(b.right, r.right)])
    .filter(([a, b]) => b > a).sort((a, b) => a[0] - b[0]);
  return {prev: one('[data-slider-prev]'), next: one('[data-slider-next]'),
          rewind: root.hasAttribute('data-slider-rewind'),
          L: spans.length ? +(spans[0][0] - r.left).toFixed(1) : null,
          R: spans.length ? +(r.right - spans[spans.length - 1][1]).toFixed(1) : null};
}"""

# Put rewind back and rebuild, which is exactly the pre-r98 rail.
STRIP = """() => {
  const t = document.querySelector('.gb-expert__cards');
  const root = t.closest('[data-slider]');
  if (!t.swiper) return 0;
  root.setAttribute('data-slider-rewind', '');
  const gap = parseFloat(getComputedStyle(t).columnGap) || 0;
  const centred = matchMedia('(max-width: 767px)').matches;
  t.swiper.destroy(true, true);
  const sw = new Swiper(t, {slidesPerView:'auto', spaceBetween:gap, speed:0, rewind:true,
    centeredSlides:centred, centeredSlidesBounds:centred, initialSlide:1,
    a11y:false, keyboard:false});
  root.querySelectorAll('[data-slider-prev],[data-slider-next]').forEach(b => {
    b.disabled = false;
    b.addEventListener('click', () => b.hasAttribute('data-slider-next')
      ? sw.slideNext() : sw.slidePrev());
  });
  return 1;
}"""


def run(strip):
    ok = red = 0

    def check(tag, got, want, tol=0.02):
        nonlocal ok, red
        good = (abs(got - want) <= tol) if isinstance(want, float) and isinstance(got, float) \
               else got == want
        ok, red = ok + good, red + (not good)
        print(f"  {'ok  ' if good else 'RED '} {tag}" + ('' if good else f"   got={got!r} want={want!r}"))

    with sync_playwright() as pw:
        br = pw.chromium.launch(executable_path=CHROME)

        def click(pg, which):
            pg.evaluate(f"document.querySelector('.gb-expert__nav [data-slider-{which}]').click()")
            pg.wait_for_timeout(700)   # settle: opacity is transitioned

        # -- the three centred tiers: middle -> both live, each end -> one dead --
        for w in (390, 575, 767):
            print(f'{w}  dead-ends at both edges')
            pg = br.new_page(viewport={'width': w, 'height': 900})
            pg.goto(f'{ROOT}/reviews.html'); pg.wait_for_timeout(1100)
            if strip: check(f'{w} strip rebuilt the rail', pg.evaluate(STRIP), 1); pg.wait_for_timeout(500)

            d = pg.evaluate(STATE)
            check(f'{w} rewind attribute is gone', d['rewind'], False)
            check(f'{w} opens in the middle: prev live', d['prev']['off'], False)
            check(f'{w} opens in the middle: next live', d['next']['off'], False)

            click(pg, 'next'); click(pg, 'next'); click(pg, 'next')
            d = pg.evaluate(STATE)
            check(f'{w} at the end: next disabled', d['next']['off'], True)
            check(f'{w} at the end: next dimmed', d['next']['op'], DIM)
            check(f'{w} at the end: next cursor', d['next']['cur'], 'not-allowed')
            check(f'{w} at the end: prev still live', d['prev']['off'], False)
            check(f'{w} at the end: prev at full opacity', d['prev']['op'], 1.0)
            # dead-ending must not reintroduce the gap centeredSlidesBounds fixed
            check(f'{w} at the end: no gap left', d['L'], 0.0, 1.0)
            check(f'{w} at the end: no gap right', d['R'], 0.0, 1.0)

            click(pg, 'prev'); click(pg, 'prev'); click(pg, 'prev')
            d = pg.evaluate(STATE)
            check(f'{w} at the start: prev disabled', d['prev']['off'], True)
            check(f'{w} at the start: prev dimmed', d['prev']['op'], DIM)
            check(f'{w} at the start: next still live', d['next']['off'], False)
            check(f'{w} at the start: no gap left', d['L'], 0.0, 1.0)
            pg.close()

        # -- 991: all three cards already fit, so BOTH arrows are dead ----------
        print('991 whole set fits, so both arrows are dead')
        pg = br.new_page(viewport={'width': 991, 'height': 900})
        pg.goto(f'{ROOT}/reviews.html'); pg.wait_for_timeout(1100)
        if strip: check('991 strip rebuilt the rail', pg.evaluate(STRIP), 1); pg.wait_for_timeout(500)
        d = pg.evaluate(STATE)
        check('991 prev disabled', d['prev']['off'], True)
        check('991 next disabled', d['next']['off'], True)
        pg.close()

        # -- the four loop reels must not have grown disabled arrows -----------
        print('loop reels keep live arrows (sync early-returns for them)')
        for page in ('index', 'pdp', 'our-story', 'how-gumi-works'):
            pg = br.new_page(viewport={'width': 390, 'height': 900})
            pg.goto(f'{ROOT}/{page}.html'); pg.wait_for_timeout(1200)
            d = pg.evaluate("""() => {
              const root = document.querySelector('[data-slider]');
              const b = [...root.querySelectorAll('[data-slider-prev],[data-slider-next]')];
              return {loop: root.hasAttribute('data-slider-loop'),
                      off: b.map(e => e.disabled)};
            }""")
            check(f'{page:<15} is a loop rail', d['loop'], True)
            check(f'{page:<15} arrows stay live', d['off'], [False, False])
            pg.close()

        br.close()
    print(f'\n{ok} ok / {red} red')
    return red


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--strip', action='store_true')
    a = ap.parse_args()
    raise SystemExit(1 if (run(a.strip) and not a.strip) else 0)
