#!/usr/bin/env python3
"""r96 on the storefront -- the five items that can be graded live.

  python3 tools/r96live.py --password 1234           # after the push: all green
  python3 tools/r96live.py --password 1234 --strip   # inverted: must go RED

Not graded here, on purpose:
  0  the reveal animation is scoped OFF live cards (`:not([data-review-id])`) --
     the live section grew its own `.is-appearing` reveal and strips that class
     450ms later, which would replay ours. Asserted NEGATIVELY below.
  6  centeredSlidesBounds lives in main.js, which is not being pushed. Asserted
     NEGATIVELY below so a later main.js push shows up as a RED here, not as a
     silent change.
"""
import argparse

from playwright.sync_api import sync_playwright

CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
LIVE = 'https://gumi.com.au'
PDP = '/products/superfood-greens-gummies'
GREY = 'rgb(77, 77, 77)'
SAND = 'rgb(245, 241, 233)'

# live path -> is the hero the centred variant?
HEROES = {
    '/pages/faq': True, '/pages/get-in-touch': True, '/pages/how-gumi-works': True,
    '/pages/our-story': True, '/pages/privacy-policy': True, '/pages/referral': True,
    '/pages/shipping': True, '/pages/reviews': False, '/pages/science': False,
}

HERO = """() => {
  const h = document.querySelector('.gb-page-hero');
  if (!h) return null;
  const t = h.querySelector('.gb-page-hero__title');
  const l = h.querySelector('.gb-page-hero__lead');
  return {centre: h.classList.contains('gb-page-hero--center'),
          lead: l ? getComputedStyle(l).color : null,
          pr: t ? parseFloat(getComputedStyle(t).paddingRight) : null};
}"""

PANEL = """() => {
  const p = document.querySelector('.gb-header__panel');
  if (!p) return null;
  const cs = getComputedStyle(p);
  return {h: +p.getBoundingClientRect().height.toFixed(2),
          bt: cs.borderTopWidth, bb: cs.borderBottomWidth, btc: cs.borderTopColor};
}"""

FAQ = """() => {
  const rows = [...document.querySelectorAll('.gb-faq__list .gb-faq__item')];
  if (!rows.length) return null;
  // ⚠ live wraps every block in a bare div.shopify-block, so "last" is the
  // list's last DIRECT child, not the last item (r64).
  const list = document.querySelector('.gb-faq__list');
  const last = list.lastElementChild;
  const vals = rows.filter(i => !i.open && !last.contains(i))
    .map(i => parseFloat(getComputedStyle(i.querySelector('.gb-faq__row')).paddingBottom));
  return {n: vals.length, min: Math.min(...vals), max: Math.max(...vals)};
}"""

SCIENCE = """() => {
  const tight = document.querySelector('.gb-science--tight');
  if (!tight) return null;
  const cards = tight.querySelector('.gb-science__cards');
  const card = tight.querySelector('.gb-science-card');
  const plain = document.querySelector('.gb-science:not(.gb-science--tight) .gb-science-card');
  return {gap: parseFloat(getComputedStyle(card).rowGap),
          mt: parseFloat(getComputedStyle(cards).marginTop),
          plain: plain ? parseFloat(getComputedStyle(plain).rowGap) : null};
}"""

NEG = """() => {
  const c = document.querySelector('.gb-crev-card');
  const t = document.querySelector('.gb-expert__cards');
  return {crevAnim: c ? getComputedStyle(c).animationName : 'no-card',
          crevHasId: c ? c.hasAttribute('data-review-id') : null,
          bounds: (t && t.swiper) ? t.swiper.params.centeredSlidesBounds : 'no-swiper'};
}"""

# --- strips: put the pre-r96 values back inline ------------------------------
STRIP_HERO = """() => {
  let n = 0;
  for (const e of document.querySelectorAll('.gb-page-hero__lead--lg, .gb-page-hero__lead--text-page')) {
    e.style.setProperty('color', '#1a1a1a', 'important'); n++; }
  for (const e of document.querySelectorAll('.gb-page-hero__title')) {
    e.style.setProperty('padding-right', '0', 'important'); n++; }
  return n;
}"""
STRIP_PANEL = """() => {
  const p = document.querySelector('.gb-header__panel'); if (!p) return 0;
  p.style.setProperty('border-top-width', '1px', 'important');
  p.style.setProperty('border-bottom-width', '1px', 'important');
  p.style.setProperty('border-color', 'transparent', 'important');
  return 1;
}"""
STRIP_FAQ = """() => {
  const n = document.querySelectorAll('.gb-faq__list');
  n.forEach(e => e.style.setProperty('--acc-gap', '16px'));
  return n.length;
}"""
STRIP_SCI = """() => {
  const t = document.querySelector('.gb-science--tight'); if (!t) return 0;
  t.querySelectorAll('.gb-science-card').forEach(
    e => e.style.setProperty('gap', '16px', 'important'));
  t.querySelector('.gb-science__cards').style.setProperty('margin-top', '26px', 'important');
  return 1;
}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--password', required=True)
    ap.add_argument('--strip', action='store_true')
    a = ap.parse_args()
    ok = red = 0

    def check(tag, got, want, tol=0.6):
        nonlocal ok, red
        if isinstance(want, (int, float)) and isinstance(got, (int, float)):
            good = abs(got - want) <= tol
        else:
            good = got == want
        ok, red = ok + good, red + (not good)
        print(f"  {'ok  ' if good else 'RED '} {tag}" + ('' if good else f"   got={got!r} want={want!r}"))

    def strip(pg, js, tag):
        n = pg.evaluate(js)
        print(f'  ..   {tag}: touched {n}')
        # ⚠ padding-bottom and border-width are transitioned; reading straight
        # after the write returns the START value and everything passes on stale
        # numbers -- [[headless-transition-reads-start-value]].
        pg.wait_for_timeout(450)

    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=CHROME)
        ctx = br.new_context(viewport={'width': 1440, 'height': 900})
        ctx.request.post(LIVE + '/password', form={
            'form_type': 'storefront_password', 'utf8': '✓', 'password': a.password})
        if not any(c['name'] == '_shopify_essential' for c in ctx.cookies()):
            raise SystemExit('storefront password rejected (no _shopify_essential)')
        pg = ctx.new_page()

        print('\n== 3 & 5  hero lead colour / title inset ==')
        for w, want_pr in ((390, 30), (768, 30), (1440, 0)):
            pg.set_viewport_size({'width': w, 'height': 900})
            for path, centred in HEROES.items():
                pg.goto(LIVE + path, wait_until='domcontentloaded')
                pg.wait_for_timeout(500)
                if a.strip: strip(pg, STRIP_HERO, f'{path} {w}')
                d = pg.evaluate(HERO)
                name = path.rsplit('/', 1)[-1]
                if d is None:
                    check(f'{w} {name} hero present', False, True); continue
                check(f'{w} {name:<15} centre flag', d['centre'], centred)
                if d['lead'] is not None:
                    check(f'{w} {name:<15} lead #4d4d4d', d['lead'], GREY)
                check(f'{w} {name:<15} title padding-right',
                      d['pr'], 0 if centred else want_pr)

        print('\n== 2  header panel border ==')
        for w in (1440, 900):
            pg.set_viewport_size({'width': w, 'height': 800})
            pg.goto(LIVE + '/pages/reviews', wait_until='domcontentloaded')
            pg.wait_for_timeout(700)
            if a.strip: strip(pg, STRIP_PANEL, f'panel {w}')
            d = pg.evaluate(PANEL)
            if d is None:
                check(f'{w} panel present', False, True); continue
            check(f'{w} shut height is 0, not a 2px cream bar', d['h'], 0)
            check(f'{w} shut border-top', d['bt'], '0px')
            check(f'{w} shut border-bottom', d['bb'], '0px')
            pg.evaluate("document.querySelector('.gb-header').classList.add('is-open')")
            pg.wait_for_timeout(700)
            d = pg.evaluate(PANEL)
            check(f'{w} open border-top 1px', d['bt'], '1px')
            check(f'{w} open border colour sand', d['btc'], SAND)
        pg.set_viewport_size({'width': 390, 'height': 800})
        pg.goto(LIVE + '/pages/reviews', wait_until='domcontentloaded')
        pg.wait_for_timeout(700)
        pg.evaluate("document.querySelector('.gb-header').classList.add('is-open')")
        pg.wait_for_timeout(900)
        d = pg.evaluate(PANEL)
        check('390 drawer keeps border-top off', d['bt'], '0px')
        check('390 drawer keeps border-bottom off', d['bb'], '0px')

        print('\n== 1  faq row padding-bottom 24 ==')
        for w in (390, 1440):
            pg.set_viewport_size({'width': w, 'height': 900})
            pg.goto(LIVE + '/pages/faq', wait_until='domcontentloaded')
            pg.wait_for_timeout(600)
            if a.strip: strip(pg, STRIP_FAQ, f'faq {w}')
            d = pg.evaluate(FAQ)
            if d is None:
                check(f'{w} faq list present', False, True); continue
            check(f'{w} shut rows found', d['n'] >= 4, True)
            check(f'{w} .gb-faq__row padding-bottom min', d['min'], 24)
            check(f'{w} .gb-faq__row padding-bottom max', d['max'], 24)

        print('\n== 4  tight science card gap 22, margin-top gone ==')
        for w in (390, 1440):
            pg.set_viewport_size({'width': w, 'height': 900})
            pg.goto(LIVE + '/pages/science', wait_until='domcontentloaded')
            pg.wait_for_timeout(600)
            if a.strip: strip(pg, STRIP_SCI, f'science {w}')
            d = pg.evaluate(SCIENCE)
            if d is None:
                check(f'{w} tight section present', False, True); continue
            check(f'{w} tight card gap 22', d['gap'], 22)
            check(f'{w} tight cards margin-top removed', d['mt'], 0)
            if d['plain'] is not None:
                check(f'{w} plain card untouched at 16', d['plain'], 16)

        print('\n== 0 & 6  the two that must NOT be live ==')
        pg.set_viewport_size({'width': 390, 'height': 900})
        # ⚠ Two different pages: gb-app-section is rendered from product.json
        # only, the expert rail from page.reviews.json only.
        pg.goto(LIVE + PDP, wait_until='domcontentloaded')
        pg.wait_for_timeout(1200)
        d = pg.evaluate(NEG)
        check('live cards carry data-review-id', d['crevHasId'], True)
        check('0 our reveal stays off live cards', d['crevAnim'], 'none')
        pg.goto(LIVE + '/pages/reviews', wait_until='domcontentloaded')
        pg.wait_for_timeout(1400)
        check('6 main.js not pushed: rail has no bounds', pg.evaluate(NEG)['bounds'], False)

        br.close()
    print(f'\n{ok} ok / {red} red')
    return red


if __name__ == '__main__':
    raise SystemExit(1 if main() else 0)
