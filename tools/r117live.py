#!/usr/bin/env python3
"""Round 117 read back off live.

  python3 tools/r117live.py --password 1234            # everything but /cart
  python3 tools/r117live.py --password 1234 --cart     # adds the /cart checks

/cart carries a Cloudflare challenge that can poison the whole session, so its
checks are opt-in and reported as SKIPPED rather than silently dropped.

1  $build reached the CDN.
2  /collections/all and /404 line up with the header above 1440 (the shell, not
   just the gutter -- below 1440 the gutter binds and both already agreed).
3  First-pass reveal: the banner lands before the modules under it.
4  (--cart) the drawer /cart renders already open can be closed again.
"""
import argparse, sys
from playwright.sync_api import sync_playwright

CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
LIVE = 'https://gumi.com.au'
ok = red = skip = 0


def grade(cond, label, detail=''):
    global ok, red
    if cond:
        ok += 1
        print(f'  ok   {label}   {detail}')
    else:
        red += 1
        print(f'  RED  {label}   {detail}')


ap = argparse.ArgumentParser()
ap.add_argument('--password', required=True)
ap.add_argument('--cart', action='store_true', help='also probe /cart (Cloudflare risk)')
a = ap.parse_args()

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=CHROME)
    ctx = b.new_context(viewport={'width': 1440, 'height': 900})
    ctx.request.post(LIVE + '/password', form={
        'form_type': 'storefront_password', 'utf8': '✓', 'password': a.password})
    pg = ctx.new_page()

    def go(path, w=1440, h=900, wait=1800):
        pg.set_viewport_size({'width': w, 'height': h})
        pg.goto(LIVE + path, wait_until='domcontentloaded', timeout=90000)
        pg.wait_for_timeout(wait)

    print('--- 1. $build ---')
    go('/')
    got = pg.evaluate("""() => getComputedStyle(document.documentElement)
        .getPropertyValue('--build').trim()""")
    # NOT pinned to r117: a literal build token turns this red on every later
    # round and reads as a regression. What matters on a re-run is that live is
    # at least this round's build.
    _m = __import__('re').search(r'"(\d{8})-r(\d+)"', got)
    grade(bool(_m) and (int(_m.group(1)), int(_m.group(2))) >= (20260908, 117),
          '--build is r117 or later', got)

    print('--- 2. shells line up with the header ---')
    LEFT = """() => {
        const bar = document.querySelector('.gb-header__bar');
        const cs = getComputedStyle(bar);
        const b = bar.getBoundingClientRect();
        return Math.round(b.left + parseFloat(cs.paddingLeft));
    }"""
    GRID = """(sel) => { const e = document.querySelector(sel);
        return e ? Math.round(e.getBoundingClientRect().left) : null; }"""
    for w in (1440, 1920, 2560):
        go('/', w)
        head = pg.evaluate(LEFT)
        go('/collections/all', w)
        col = pg.evaluate(GRID, '.product-grid')
        grade(col is not None and abs(col - head) <= 1,
              f'{w}: collection grid starts where the header content does',
              f'grid {col} vs header {head}')
        go('/404', w)
        p404 = pg.evaluate(GRID,
            '[data-testid="product-list"] .product-grid, [data-testid="product-list"] ul, .ui-test-product-list .resource-list__carousel')
        if p404 is None:
            print(f'  --   {w}: 404 list not found by selector, checking the section box')
            p404 = pg.evaluate("""() => { const s = document.querySelector('[data-testid="product-list"]');
                if (!s) return null; const inner = s.querySelector('.section-resource-list__header, ul, .resource-list');
                return inner ? Math.round(inner.getBoundingClientRect().left) : null; }""")
        grade(p404 is not None and abs(p404 - head) <= 1,
              f'{w}: 404 product list starts there too', f'list {p404} vs header {head}')

    print('--- 3. first-pass reveal order @390 ---')
    pg.set_viewport_size({'width': 390, 'height': 1600})
    pg.goto(LIVE + '/', wait_until='commit', timeout=90000)
    rows = pg.evaluate("""() => new Promise(res => {
      const t0 = performance.now();
      const els = [...document.querySelectorAll('.wowo')].map(e => ({
        e, inBanner: !!e.closest('.gb-hero, .gb-page-hero'), at: null,
        cls: (e.className||'').toString().replace(/\\s+/g,' ').slice(0,30)}));
      const tick = () => {
        let pending = 0;
        for (const o of els) {
          if (o.at === null) {
            if (parseFloat(getComputedStyle(o.e).opacity) > 0.98)
              o.at = Math.round(performance.now() - t0);
            else pending++;
          }
        }
        if (pending && performance.now() - t0 < 6000) requestAnimationFrame(tick);
        else res(els.map(o => ({inBanner: o.inBanner, at: o.at, cls: o.cls})));
      };
      requestAnimationFrame(tick);
    })""")
    inb = [r['at'] for r in rows if r['inBanner'] and r['at'] is not None]
    out = [r['at'] for r in rows if not r['inBanner'] and r['at'] is not None]
    grade(bool(inb) and bool(out), 'both groups revealed in the first pass',
          f'{len(inb)} in banner, {len(out)} below')
    if inb and out:
        grade(max(inb) <= min(out), 'banner lands before anything under it',
              f'banner last {max(inb)}ms vs below first {min(out)}ms')

    print('--- 4. /cart drawer ---')
    if not a.cart:
        skip += 1
        print('  SKIP  /cart checks not run (pass --cart to include them)')
    else:
        r = pg.goto(LIVE + '/cart', wait_until='domcontentloaded', timeout=90000)
        pg.set_viewport_size({'width': 1440, 'height': 900})
        pg.wait_for_timeout(3000)
        if r.status != 200 or 'moment' in pg.title():
            skip += 1
            print(f'  SKIP  /cart challenged (status {r.status}) -- not a failure')
        else:
            st = pg.evaluate("""() => {
                const td = document.querySelector('#cart-drawer');
                const dlg = td && td.querySelector('dialog');
                return {tdOpen: td && td.hasAttribute('open'), dlgOpen: dlg && dlg.open};
            }""")
            if not st['dlgOpen']:
                skip += 1
                print(f'  SKIP  drawer did not render open this visit ({st}) -- '
                      'the split state is what the fix targets, nothing to grade')
            else:
                grade(st['tdOpen'], 'the component was handed the open state it was missing',
                      str(st))
                pg.evaluate("() => document.querySelector('.gb-cart__close').click()")
                pg.wait_for_timeout(1200)
                after = pg.evaluate("""() => {
                    const d = document.querySelector('#cart-drawer dialog');
                    const p = document.querySelector('.gb-cart__panel');
                    return {dlgOpen: d && d.open,
                            x: p ? Math.round(p.getBoundingClientRect().x) : null};
                }""")
                grade(not after['dlgOpen'], 'and the close button now closes it', str(after))
    b.close()

print(f'\n{ok} ok / {red} red' + (f' / {skip} skipped' if skip else '') + '   [LIVE]')
sys.exit(1 if red else 0)
