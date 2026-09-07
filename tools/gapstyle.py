#!/usr/bin/env python3
"""Static site vs live theme: per-class computed-style diff.

    python3 tools/gapstyle.py --password 1234              # all pages
    python3 tools/gapstyle.py --password 1234 --page index
    python3 tools/gapstyle.py --password 1234 --width 390

Why computed style and not screenshots: the two sides render DIFFERENT content
(live pulls real product data, static has design copy), so pixels differ
everywhere and drown the signal. What must match is the style the cascade lands
on each class -- a difference there means our CSS did not reach the element on
live, and that is fixable without touching structure.

Two noise sources are separated out rather than filtered away:
  * class present on one side only  -> structural gap (LIVE-GAP.md), reported apart
  * geometry (width/height)         -> content-driven, reported apart with tolerance

Reveal state is normalised on both sides before sampling: .wowo parks at
opacity 0 and a headless page cannot drive the scroll that lifts it.
"""
import argparse, json, pathlib, re, sys, collections
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
SITE = 'https://gumi.com.au'

PAGES = {
    'index':          '/',
    'pdp':            '/products/superfood-greens-gummies',
    'science':        '/pages/science',
    'reviews':        '/pages/reviews',
    'how-gumi-works': '/pages/how-gumi-works',
    'our-story':      '/pages/our-story',
    'faq':            '/pages/faq',
    'get-in-touch':   '/pages/get-in-touch',
    'referral':       '/pages/referral',
    'privacy-policy': '/pages/privacy-policy',
    'shipping':       '/pages/shipping',
}

# Cascade-visible properties. Geometry lives in GEO and is graded separately.
PROPS = [
    'display', 'position', 'flex-direction', 'flex-wrap', 'align-items',
    'justify-content', 'gap', 'grid-template-columns', 'overflow-x', 'overflow-y',
    'font-family', 'font-size', 'font-weight', 'line-height', 'letter-spacing',
    'text-align', 'text-transform', 'text-decoration-line', 'white-space',
    'color', 'background-color', 'background-image', 'opacity', 'visibility',
    'border-top-width', 'border-bottom-width', 'border-left-width', 'border-right-width',
    'border-top-color', 'border-top-style',
    'border-top-left-radius', 'border-bottom-left-radius',
    'padding-top', 'padding-right', 'padding-bottom', 'padding-left',
    'margin-top', 'margin-right', 'margin-bottom', 'margin-left',
    'max-width', 'min-height', 'box-shadow', 'transform', 'z-index',
    'object-fit', 'aspect-ratio', 'flex-shrink', 'flex-grow', 'list-style-type',
]
GEO = ['width', 'height']

PROBE = """(args) => {
  const [props, geo] = args;
  // Reveal modules park content at opacity 0 until scrolled into view; a headless
  // page cannot drive that reliably, and it is not what we are grading.
  document.querySelectorAll('.wowo').forEach(e => e.classList.remove('wowo', 'animated'));
  document.querySelectorAll('[data-line-reveal]').forEach(e => {
    e.removeAttribute('data-line-reveal'); e.classList.add('is-revealed');
  });
  document.documentElement.classList.add('js');

  const TOK = /^gb-[a-z0-9-]+(?:__[a-z0-9-]+)?(?:--[a-z0-9-]+)?$/;
  const buckets = new Map();
  for (const el of document.querySelectorAll('[class]')) {
    const cn = el.getAttribute('class') || '';
    for (const c of cn.split(/\\s+/)) {
      if (!TOK.test(c)) continue;
      if (!buckets.has(c)) buckets.set(c, []);
      buckets.get(c).push(el);
    }
  }
  const out = {};
  for (const [cls, els] of buckets) {
    const el = els[0];
    const cs = getComputedStyle(el);
    const rec = { n: els.length, tag: el.tagName.toLowerCase(), s: {}, g: {} };
    for (const p of props) rec.s[p] = cs.getPropertyValue(p);
    const r = el.getBoundingClientRect();
    rec.g['width'] = Math.round(r.width);
    rec.g['height'] = Math.round(r.height);
    for (const pseudo of ['::before', '::after']) {
      const ps = getComputedStyle(el, pseudo);
      if (ps.content === 'none' || ps.content === 'normal') { rec[pseudo] = null; continue; }
      rec[pseudo] = {};
      for (const p of ['content','position','width','height','background-color',
                       'background-image','top','left','right','bottom',
                       '-webkit-mask-image','mask-image','transform','opacity','z-index']) {
        rec[pseudo][p] = ps.getPropertyValue(p);
      }
    }
    out[cls] = rec;
  }
  return out;
}"""


def sample(page, props):
    return page.evaluate(PROBE, [props, GEO])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--password')
    ap.add_argument('--page', action='append')
    ap.add_argument('--width', type=int, default=1440)
    ap.add_argument('--out', default=None)
    a = ap.parse_args()

    pages = a.page or list(PAGES)
    report = {}

    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME)
        ctx_live = b.new_context(viewport={'width': a.width, 'height': 1000})
        if a.password:
            r = ctx_live.request.post(SITE + '/password', form={
                'form_type': 'storefront_password', 'utf8': '✓', 'password': a.password})
            if r.status in (429, 503):
                raise SystemExit('Cloudflare (HTTP %d) -- back off, do not retry' % r.status)
        ctx_st = b.new_context(viewport={'width': a.width, 'height': 1000})

        for name in pages:
            f = ROOT / (name + '.html')
            if not f.exists():
                print('!! no static page %s' % name); continue
            pg = ctx_st.new_page()
            pg.goto(f.as_uri(), wait_until='networkidle')
            pg.wait_for_timeout(700)
            st = sample(pg, PROPS)
            pg.close()

            lv = None
            if a.password:
                pg = ctx_live.new_page()
                try:
                    pg.goto(SITE + PAGES[name], wait_until='networkidle', timeout=45000)
                except Exception as e:
                    print('!! live %s: %s' % (name, str(e)[:80]))
                if 'gb-' not in pg.content():
                    print('!! live %s served no gb-* markup (title=%r)' % (name, pg.title()))
                else:
                    pg.wait_for_timeout(700)
                    lv = sample(pg, PROPS)
                pg.close()
            report[name] = {'static': st, 'live': lv}
            print('sampled %-16s static=%d live=%s' % (
                name, len(st), len(lv) if lv else '-'))
        b.close()

    outp = a.out or str(ROOT / 'tools' / ('gapstyle-%d.json' % a.width))
    pathlib.Path(outp).write_text(json.dumps(report), encoding='utf-8')
    print('\nwrote ' + outp)


if __name__ == '__main__':
    main()
