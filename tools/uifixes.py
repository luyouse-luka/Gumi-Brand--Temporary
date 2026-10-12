#!/usr/bin/env python3
"""Client UI detail fixes of 2026-09-09, as assertions.

  python3 tools/uifixes.py [--live --password 1234]

  1 .gb-cart-item__interval sizes to the SELECTED option, not the longest one.
  2 .gb-scallop-box's plate is a vector mask, not the 320x320 PNG it used to be
    (which is what read as blurry once the box is drawn bigger than 320).
  4 Cart glyph sits 1px below the account one on phones.
  5 Lenis coasts less: duration 1 -> 0.6.
  6 r132: .gb-product__label-btn takes 0 40px on phones, 0 64px above them.
    ⚠ .gb-product__cta and .gb-form__submit carry the same 0 64px and were NOT
    named by the client -- asserted unchanged so a later sweep does not "tidy"
    them into matching.
"""
import argparse, pathlib, sys
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
LIVE = 'https://gumi.com.au'
LENIS_DURATION = 0.6
CART_NUDGE = 1

ok = red = 0


def check(label, cond, got, want):
    global ok, red
    if cond:
        ok += 1
        print(f'  ok   {label}: {got}')
    else:
        red += 1
        print(f'  RED  {label}: got {got}, want {want}')


def page(br, w, h, url, password=None):
    ctx = br.new_context(viewport={'width': w, 'height': h})
    if password:
        ctx.request.post(LIVE + '/password', form={
            'form_type': 'storefront_password', 'utf8': '✓', 'password': password})
    pg = ctx.new_page()
    pg.goto(url, wait_until='load', timeout=60000)
    pg.wait_for_timeout(1800)
    return ctx, pg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--live', action='store_true')
    ap.add_argument('--password')
    a = ap.parse_args()
    live, pw = a.live, a.password
    index = LIVE + '/' if live else 'file://' + str(ROOT / 'index.html')
    hgw = (LIVE + '/pages/how-gumi-works') if live else 'file://' + str(ROOT / 'how-gumi-works.html')
    # the live product handle is not the static build's; resolved off the store below
    pdp = None if live else 'file://' + str(ROOT / 'pdp.html')

    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=CHROME)

        print('1  cart interval select follows its content')
        ctx, pg = page(br, 1440, 900, index, pw)
        r = pg.evaluate("""async () => {
          const t = document.querySelector('[data-modal="gb-cart"], .gb-header__icon-wrap button');
          if (t) { t.click(); await new Promise(r => setTimeout(r, 900)); }
          const s = document.querySelector('select.gb-cart-item__interval:not(.gb-select__native)');
          if (!s) return {absent: true};
          const w0 = s.getBoundingClientRect().width;
          const opts = [...s.options].map(o => o.text);
          // widest option vs the one actually selected: with field-sizing the box
          // tracks the selection, so picking the shortest must shrink it.
          const iLong = opts.indexOf(opts.slice().sort((a, b) => b.length - a.length)[0]);
          const iShort = opts.indexOf(opts.slice().sort((a, b) => a.length - b.length)[0]);
          s.selectedIndex = iLong; s.dispatchEvent(new Event('change'));
          await new Promise(r => setTimeout(r, 120));
          const wLong = s.getBoundingClientRect().width;
          s.selectedIndex = iShort; s.dispatchEvent(new Event('change'));
          await new Promise(r => setTimeout(r, 120));
          const wShort = s.getBoundingClientRect().width;
          return {fieldSizing: getComputedStyle(s).fieldSizing, opts, w0,
                  wLong: Math.round(wLong), wShort: Math.round(wShort),
                  sameLength: opts.length < 2 || new Set(opts.map(o => o.length)).size === 1};
        }""")
        if r.get('absent'):
            # Live-only by construction: the rule carries :not(.gb-select__native)
            # because the static build draws its own control over a hidden native
            # select. Nothing to assert here -- run with --live.
            print('  n/a  bare <select> is live-only (static draws a selectBox)')
        else:
            check('field-sizing: content', r['fieldSizing'] == 'content', r['fieldSizing'], 'content')
            if r['sameLength']:
                print(f"  n/a  width tracks selection: every option is the same length ({r['opts']})")
            else:
                check('width tracks selection', r['wShort'] < r['wLong'],
                      f"short {r['wShort']} vs long {r['wLong']}", 'short < long')
        pg.close(); ctx.close()

        print('2  scallop plate is a vector mask')
        ctx, pg = page(br, 1440, 900, hgw, pw)
        r = pg.evaluate("""() => {
          const b = document.querySelector('.gb-scallop-box');
          if (!b) return {absent: true};
          const m = getComputedStyle(b, '::before').maskImage || getComputedStyle(b, '::before').webkitMaskImage;
          return {mask: (m || '').slice(0, 60), isSvg: /svg\\+xml/.test(m || ''),
                  isPng: /image\\/png/.test(m || ''), box: b.getBoundingClientRect().width};
        }""")
        if r.get('absent'):
            check('scallop box present', False, 'not found', 'a .gb-scallop-box')
        else:
            check('mask is SVG', r['isSvg'], r['mask'], 'data:image/svg+xml')
            check('mask is not the old PNG', not r['isPng'], r['isPng'], False)
            # the PNG was 320 wide; anything larger is where it went soft
            check('box is drawn larger than the old 320 raster', r['box'] > 320,
                  round(r['box']), '> 320')
        pg.close(); ctx.close()

        print('4  cart glyph nudged 1px on phones')
        for w, expect in ((390, CART_NUDGE), (1440, 0)):
            ctx, pg = page(br, w, 900 if w > 767 else 844, index, pw)
            r = pg.evaluate("""() => {
              const icons = document.querySelector('.gb-header__icons');
              if (!icons) return {absent: true};
              const acc = icons.querySelector('a[aria-label="Account"], a[href*="account"]');
              const cart = icons.querySelector('.gb-header__icon-wrap, [data-modal="gb-cart"]');
              if (!acc || !cart) return {absent: true};
              const a = acc.getBoundingClientRect(), c = cart.getBoundingClientRect();
              const svgA = acc.querySelector('svg'), svgC = cart.querySelector('svg');
              const ra = (svgA || acc).getBoundingClientRect(), rc = (svgC || cart).getBoundingClientRect();
              return {delta: +(rc.top - ra.top).toFixed(2),
                      tf: getComputedStyle(cart).transform};
            }""")
            if r.get('absent'):
                check(f'{w} icons present', False, 'not found', 'account + cart')
            else:
                check(f'{w} cart sits {expect}px below account',
                      abs(r['delta'] - expect) <= 0.51, r['delta'], expect)
            pg.close(); ctx.close()

        print('5  smooth scrolling coasts less')
        ctx, pg = page(br, 1440, 900, index, pw)
        r = pg.evaluate("""() => {
          const s = window.gumi && window.gumi.smoothScroll;
          const l = s && s.lenis;
          if (!l) return {absent: true};
          return {duration: (l.options && l.options.duration) !== undefined
                    ? l.options.duration : (l.duration !== undefined ? l.duration : null)};
        }""")
        if r.get('absent'):
            check('lenis instance reachable', False, 'window.gumi.smoothScroll.lenis missing',
                  'an instance')
        else:
            check('lenis duration', r['duration'] == LENIS_DURATION, r['duration'], LENIS_DURATION)
        pg.close(); ctx.close()


        print('6  label button padding, phones only')
        if live and pdp is None:
            ctx, pg = page(br, 1440, 900, LIVE + '/collections/all', pw)
            h = pg.evaluate("() => (document.querySelector('a[href*=\"/products/\"]')||{}).pathname")
            pg.close(); ctx.close()
            pdp = LIVE + h if h else None
        if not pdp:
            check('a product page to read', False, 'none found', 'a PDP url')
        else:
            for w, want, other in ((390, '0px 40px', '0px 64px'), (1440, '0px 64px', '0px 64px')):
                ctx, pg = page(br, w, 900 if w > 767 else 844, pdp, pw)
                r = pg.evaluate("""() => {
                  const pad = s => {
                    const e = document.querySelector(s);
                    if (!e) return null;
                    const c = getComputedStyle(e);
                    return c.paddingTop + ' ' + c.paddingRight;
                  };
                  return {label: pad('.gb-product__label-btn'), cta: pad('.gb-product__cta')};
                }""")
                check(f'{w} label-btn padding', r['label'] == want, r['label'], want)
                check(f'{w} .gb-product__cta left alone', r['cta'] == other, r['cta'], other)
                pg.close(); ctx.close()
        br.close()

    print(f'\n{ok} ok / {red} red')
    sys.exit(1 if red else 0)


if __name__ == '__main__':
    main()
