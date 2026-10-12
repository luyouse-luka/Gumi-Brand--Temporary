#!/usr/bin/env python3
"""Round 116 read back off live.

  python3 tools/r116live.py --password 1234

1  $build reached the CDN.
2  The science CTA finally renders: r115 shipped the section setting but could
   not fill it, so .gb-science__cta was 0 live for a whole round.
3  Its gap to the card grid is 48 NET. The declared margin-top is a remainder --
   .gb-science__inner is a flex column whose own gap already sits above the
   button -- so this must be measured, never read off the rule. (r115 note 4.)
4  The highlight-card hairline is gone: with an <img> present the media box has
   no grey left to anti-alias into the rounded corner.

Tab order is graded by tools/menutab.py --live (section I).
"""
import argparse, sys
from playwright.sync_api import sync_playwright

CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
LIVE = 'https://gumi.com.au'
ok = red = 0


def grade(cond, label, detail=''):
    global ok, red
    if cond:
        ok += 1
        print(f'  ok   {label}   {detail}')
    else:
        red += 1
        print(f'  RED  {label}   {detail}')


ap = argparse.ArgumentParser(); ap.add_argument('--password', required=True)
a = ap.parse_args()

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=CHROME)
    ctx = b.new_context(viewport={'width': 1440, 'height': 900})
    ctx.request.post(LIVE + '/password', form={
        'form_type': 'storefront_password', 'utf8': '✓', 'password': a.password})
    pg = ctx.new_page()

    def go(path, w, h=900):
        pg.set_viewport_size({'width': w, 'height': h})
        pg.goto(LIVE + path, wait_until='domcontentloaded', timeout=90000)
        pg.wait_for_timeout(1800)

    print('--- 1. $build ---')
    go('/pages/science', 1440)
    got = pg.evaluate("""() => getComputedStyle(document.documentElement)
        .getPropertyValue('--build').trim()""")
    grade(got == '"20260908-r116"', '--build is r116', got)

    print('--- 2. the science CTA renders ---')
    m = pg.evaluate("""() => {
        const c = [...document.querySelectorAll('.gb-science__cta')];
        return {n: c.length,
                txt: c.map(x => x.textContent.trim()),
                href: c.map(x => x.getAttribute('href')),
                tight: c.map(x => !!x.closest('.gb-science--tight')),
                cream: c.map(x => !!x.closest('.gb-science--cream')),
                btn: c.map(x => x.classList.contains('gb-btn--xl'))};
    }""")
    grade(m['n'] == 1, 'exactly one CTA on the page', f"n={m['n']}")
    grade(m['txt'] == ['Shop Now'], "labelled 'Shop Now'", str(m['txt']))
    grade(m['href'] == ['/collections/all'], 'links to /collections/all', str(m['href']))
    grade(m['tight'] == [True] and m['cream'] == [True],
          'and it sits in the --cream --tight section, not another instance',
          f"tight={m['tight']} cream={m['cream']}")
    grade(m['btn'] == [True], 'styled as gb-btn--xl (same as the ingredients CTA)')

    print('--- 3. net gap card grid -> button is 48 at every tier ---')
    for w, h in ((1440, 900), (1024, 900), (390, 844)):
        go('/pages/science', w, h)
        pg.evaluate("""() => { const c = document.querySelector('.gb-science__cta');
                               if (c) c.scrollIntoView({block: 'center'}); }""")
        pg.wait_for_timeout(900)
        g = pg.evaluate("""() => {
            const cta = document.querySelector('.gb-science__cta');
            if (!cta) return null;
            const cards = cta.closest('.gb-science__inner').querySelector('.gb-science__cards');
            if (!cards) return null;
            const gap = cta.getBoundingClientRect().top - cards.getBoundingClientRect().bottom;
            return {gap: Math.round(gap * 100) / 100,
                    declared: getComputedStyle(cta).marginTop,
                    innerGap: getComputedStyle(cta.closest('.gb-science__inner')).rowGap};
        }""")
        grade(g is not None and abs(g['gap'] - 48) <= 1.5,
              f'{w}: net gap is 48',
              f"measured {g and g['gap']}  (declared margin-top {g and g['declared']}, "
              f"inner row-gap {g and g['innerGap']})")

    print('--- 4. highlight-card hairline source is gone ---')
    go('/', 1440)
    pg.evaluate("""() => document.querySelector('.gb-highlight-card__media')
                      .scrollIntoView({block: 'center'})""")
    pg.wait_for_timeout(1500)
    h = pg.evaluate("""() => [...document.querySelectorAll('.gb-highlight-card__media')]
        .map(m => ({img: !!m.querySelector('img'),
                    bg: getComputedStyle(m).backgroundColor}))""")
    grade(len(h) >= 3, 'the cards are on the page', f'n={len(h)}')
    grade(all(x['img'] for x in h), 'live fills every one with an <img>', str([x['img'] for x in h]))
    grade(all(x['bg'] == 'rgba(0, 0, 0, 0)' for x in h),
          'so the grey placeholder is off and cannot bleed into the corner',
          str([x['bg'] for x in h]))
    b.close()

print(f'\n{ok} ok / {red} red   [LIVE]')
sys.exit(1 if red else 0)
