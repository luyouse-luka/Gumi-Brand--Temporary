#!/usr/bin/env python3
"""r80 probe -- how the icon rows render live now that the vendor swapped the
placeholder <svg> circles for <img> (packed / taste / guarantee blocks).

  python3 tools/r80probe.py --password 1234
"""
import argparse, pathlib
from playwright.sync_api import sync_playwright

CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
SITE = 'https://gumi.com.au'

MEASURE = """() => {
  const out = {};
  for (const key of ['packed', 'taste', 'guarantee']) {
    const item = document.querySelector('.gb-product__' + key + '-item')
              || document.querySelector('.gb-product__' + key + ' li');
    if (!item) { out[key] = null; continue; }
    const icon = item.querySelector('img, svg');
    const r = icon ? icon.getBoundingClientRect() : null;
    const cs = icon ? getComputedStyle(icon) : null;
    out[key] = {
      tag: icon ? icon.tagName.toLowerCase() : null,
      rect: r ? [Math.round(r.width), Math.round(r.height)] : null,
      shrink: cs ? cs.flexShrink : null,
      width: cs ? cs.width : null,
      itemH: Math.round(item.getBoundingClientRect().height),
      gap: getComputedStyle(item).gap,
    };
  }
  return out;
}"""

def report(tag, data):
    print('\n== %s ==' % tag)
    for k, v in data.items():
        if v is None: print('  %-10s not on this page' % k); continue
        print('  %-10s <%s> %sx%s   flex-shrink=%s  css-width=%s  row-h=%s  gap=%s'
              % (k, v['tag'], v['rect'][0] if v['rect'] else '?',
                 v['rect'][1] if v['rect'] else '?', v['shrink'], v['width'], v['itemH'], v['gap']))

ap = argparse.ArgumentParser(); ap.add_argument('--password'); a = ap.parse_args()
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=CHROME)

    pg = b.new_page(viewport={'width': 1440, 'height': 900})
    pg.goto(pathlib.Path('pdp.html').resolve().as_uri())
    pg.wait_for_timeout(500)
    report('static pdp.html (the target)', pg.evaluate(MEASURE))
    pg.close()

    if a.password:
        ctx = b.new_context()
        r = ctx.request.post(SITE + '/password', form={
            'form_type': 'storefront_password', 'utf8': '✓', 'password': a.password})
        if r.status in (429, 503): raise SystemExit('Cloudflare (HTTP %d) -- back off' % r.status)
        pg = ctx.new_page(); pg.set_viewport_size({'width': 1440, 'height': 900})
        pg.goto(SITE + '/', wait_until='domcontentloaded')
        hrefs = pg.evaluate("() => [...new Set([...document.querySelectorAll('a[href]')]"
                            ".map(a => a.getAttribute('href')))].slice(0, 40)")
        href = next((h for h in hrefs if '/products/' in h), None)
        if not href:
            print('\n   no /products/ link on the homepage; hrefs seen:')
            for h in hrefs: print('     ' + h)
            # The cart judge pins this product; try its handle before giving up.
            href = '/products/superfood-greens-gummies'
            print('   falling back to ' + href)
        pg.goto(SITE + href.split('?')[0], wait_until='networkidle')
        if 'gb-product__packed' not in pg.content():
            raise SystemExit('no packed row at %s -- title=%r' % (pg.url, pg.title()))
        print('\n   live PDP: ' + pg.url)
        report('live PDP (as served)', pg.evaluate(MEASURE))
    b.close()
