#!/usr/bin/env python3
"""Line breaks: where does live drop a <br> the static build has?

  python3 tools/brdiff.py --password 1234

The mobile boards break several headings by hand (U+2028); the build answers
with <br class="gb-br-narrow"> (shown below 768 only) or a bare <br> (every
width). Those breaks are copy, so they can only survive to live if the liquid
lets them through -- a plain `text` setting run through `| escape` cannot.

Matches elements by (class, ordinal) within the page. Reports three states:
  BR LOST   both sides have the element, static has <br>, live does not
  BR EXTRA  live has one static does not
  NO NODE   the element is not on the live page at all (a content gap, not a
            line-break one -- decided by hand)
"""
import argparse, pathlib, re, sys
from playwright.sync_api import sync_playwright

CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
ROOT = pathlib.Path('/home/ly/project/Gumi-Brand')
LIVE = 'https://gumi.com.au'
PAGES = {
    'index': '/', 'pdp': '/products/superfood-greens-gummies',
    'science': '/pages/science', 'reviews': '/pages/reviews',
    'how-gumi-works': '/pages/how-gumi-works', 'our-story': '/pages/our-story',
    'faq': '/pages/faq', 'get-in-touch': '/pages/get-in-touch',
    'referral': '/pages/referral', 'privacy-policy': '/pages/privacy-policy',
    'shipping': '/pages/shipping',
}
# Text-bearing elements worth grading. The footer's 12 are one shared snippet.
SEL = ('h1, h2, h3, h4, p, .gb-stat__label, .gb-footer__tagline, '
       '.gb-highlight-card__title, .gb-testimonial__quote')

PROBE = """(sel) => {
  const seen = {};
  const out = [];
  for (const e of document.querySelectorAll(sel)) {
    const cls = [...e.classList].filter(c => c.startsWith('gb-'))[0];
    if (!cls) continue;
    seen[cls] = (seen[cls] || 0) + 1;
    const html = e.innerHTML;
    const brs = [...html.matchAll(/<br[^>]*>/gi)].map(m => m[0]);
    if (!brs.length && !html.includes('\\u2028')) continue;
    out.push({key: cls + '#' + seen[cls], n: brs.length,
              narrow: brs.filter(b => /gb-br-narrow/.test(b)).length,
              u2028: (html.match(/\\u2028/g) || []).length,
              text: e.textContent.replace(/\\s+/g, ' ').trim().slice(0, 70)});
  }
  return out;
}"""
# Same, but returns EVERY element so a lost <br> can be told from a missing node.
KEYS = """(sel) => {
  const seen = {}; const out = {};
  for (const e of document.querySelectorAll(sel)) {
    const cls = [...e.classList].filter(c => c.startsWith('gb-'))[0];
    if (!cls) continue;
    seen[cls] = (seen[cls] || 0) + 1;
    out[cls + '#' + seen[cls]] = {
      n: (e.innerHTML.match(/<br[^>]*>/gi) || []).length,
      text: e.textContent.replace(/\\s+/g, ' ').trim().slice(0, 70)};
  }
  return out;
}"""


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--password', required=True)
    a = ap.parse_args()
    lost = extra = nonode = same = 0
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=CHROME)
        ctx = br.new_context(viewport={'width': 390, 'height': 900})
        ctx.request.post(LIVE + '/password', form={
            'form_type': 'storefront_password', 'utf8': '✓', 'password': a.password})
        if not any(c['name'] == '_shopify_essential' for c in ctx.cookies()):
            sys.exit('storefront password rejected')
        pg = ctx.new_page()
        for name, path in PAGES.items():
            pg.goto(f'file://{ROOT}/{name}.html', wait_until='domcontentloaded')
            pg.wait_for_timeout(500)
            st = pg.evaluate(PROBE, SEL)
            pg.goto(LIVE + path, wait_until='domcontentloaded')
            pg.wait_for_timeout(700)
            lv = pg.evaluate(KEYS, SEL)
            hits = []
            for d in st:
                m = lv.get(d['key'])
                if m is None:
                    hits.append(('NO NODE ', d, None)); nonode += 1
                elif m['n'] < d['n']:
                    hits.append(('BR LOST ', d, m)); lost += 1
                elif m['n'] > d['n']:
                    hits.append(('BR EXTRA', d, m)); extra += 1
                else:
                    same += 1
            if hits:
                print(f'\n== {name} ==')
                for tag, d, m in hits:
                    kind = f"{d['n']} br" + (f" ({d['narrow']} narrow)" if d['narrow'] else '')
                    print(f"  {tag} {d['key']:<32} static {kind:<18} live "
                          f"{'-' if m is None else str(m['n']) + ' br'}")
                    print(f"           static: {d['text']}")
                    if m: print(f"           live  : {m['text']}")
        br.close()
    print(f'\n{lost} lost / {extra} extra / {nonode} node missing / {same} match')
    return lost


if __name__ == '__main__':
    raise SystemExit(1 if main() else 0)
