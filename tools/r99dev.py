#!/usr/bin/env python3
"""Grade snippets/gb-lines.liquid on live (or any base URL).

  python3 tools/r99dev.py [--base https://gumi.com.au] [--password 1234]

`shopify theme dev` cannot serve this store -- 33 Horizon 4.1.5 base files fail the
CLI 3.92.1 schema check and the dev server answers 500 for every page. So this runs
against live instead.

Two questions, because the dev theme reads the LIVE settings and nobody has
retyped the copy yet:
  A  migration is safe -- the leftover richtext/inline_richtext values still
     render as text, not as visible <p> or &lt;p&gt; markup
  B  the snippet is wired in -- every element that should now be able to carry a
     break renders, and no page shows a stray marker (// or ^^) as body copy
"""
import argparse, sys
from playwright.sync_api import sync_playwright

CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
PAGES = {
    'index': '/', 'pdp': '/products/superfood-greens-gummies',
    'science': '/pages/science', 'reviews': '/pages/reviews',
    'how-gumi-works': '/pages/how-gumi-works', 'our-story': '/pages/our-story',
    'faq': '/pages/faq',
}
HOSTS = {
    'gb-footer__tagline':      list(PAGES),
    'gb-page-hero__title':     ['science', 'reviews', 'how-gumi-works', 'our-story', 'faq'],
    'gb-hero__lead':           ['index'],
    'gb-usp__label':           ['index'],
    'gb-reviews__title':       ['index', 'pdp', 'how-gumi-works', 'our-story'],
    'gb-science__title':       ['index'],
    'gb-nutrition__title':     ['index'],
    'gb-highlight-card__text': ['index'],
    'gb-stats__title':         ['index'],
    'gb-stat__label':          ['index'],
    'gb-promo-card__title':    ['pdp'],
    'gb-dosed__title':         ['how-gumi-works'],
    'gb-expert__title':        ['reviews'],
}
PROBE = """(classes) => {
  const out = {};
  for (const c of classes) {
    out[c] = [...document.querySelectorAll('.' + c)].map(e => ({
      html: e.innerHTML.trim().slice(0, 240),
      text: e.textContent.replace(/\\s+/g, ' ').trim().slice(0, 120),
      br:   e.querySelectorAll('br').length,
      narrow: e.querySelectorAll('br.gb-br-narrow').length,
      wide:   e.querySelectorAll('br.gb-br-wide').length,
    }));
  }
  return out;
}"""

ok = red = 0
def grade(cond, label, detail=''):
    global ok, red
    if cond: ok += 1; print(f'  ok   {label}')
    else:    red += 1; print(f'  RED  {label}   {detail}')

ap = argparse.ArgumentParser()
ap.add_argument('--base', default='https://gumi.com.au')
ap.add_argument('--password', default='1234')
a = ap.parse_args()

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=CHROME)
    ctx = b.new_context(viewport={'width': 1440, 'height': 900})
    # The storefront password form is hidden behind a disclosure, so posting the
    # form directly is the only reliable way in from a headless context.
    ctx.request.post(a.base + '/password', form={
        'form_type': 'storefront_password', 'utf8': '✓', 'password': a.password})
    if not any(c['name'] == '_shopify_essential' for c in ctx.cookies()):
        sys.exit('storefront password rejected')
    pg = ctx.new_page()
    for name, path in PAGES.items():
        url = a.base + path
        pg.goto(url, wait_until='domcontentloaded', timeout=90000)
        pg.wait_for_timeout(800)
        anchors = pg.evaluate("() => document.querySelectorAll('[class*=gb-]').length")
        if anchors < 20:
            sys.exit(f'ABORT {name}: only {anchors} gb- elements on the page. '
                     f'It did not render (500? password wall?), so nothing below '
                     f'would mean anything. url={pg.url}')
        got = pg.evaluate(PROBE, list(HOSTS))
        body = pg.evaluate("() => document.body.innerText")
        print(f'\n--- {name} ---')
        for cls, pages in HOSTS.items():
            if name not in pages: continue
            nodes = got.get(cls) or []
            grade(bool(nodes), f'{name:15} {cls} renders', '(no node)')
            for i, n in enumerate(nodes):
                grade('<p>' not in n['html'] and '&lt;p&gt;' not in n['html'],
                      f'{name:15} {cls}#{i} no leftover <p>', n['html'][:90])
                grade('<p' not in n['text'] and '</p' not in n['text'],
                      f'{name:15} {cls}#{i} no <p> in text', n['text'][:90])
                if n['br']:
                    print(f'       .. {cls}#{i} br={n["br"]} narrow={n["narrow"]} wide={n["wide"]}')
        for mark in ('//', '^^'):
            hits = [l for l in body.split('\n') if mark in l and 'http' not in l]
            grade(not hits, f'{name:15} no stray "{mark}" in copy', str(hits[:2]))
    b.close()
print(f'\n{ok} ok / {red} red')
sys.exit(1 if red else 0)
