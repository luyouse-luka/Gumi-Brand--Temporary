#!/usr/bin/env python3
"""No media box paints a placeholder ground -- r120, client asked for all of them gone.

  python3 tools/placeholderbg.py                      # static build
  python3 tools/placeholderbg.py --live --password 1234
  python3 tools/placeholderbg.py --strip              # inverted: must go RED

Named after the module, not a round: crevcheck.py was overwritten once because it
carried a round number.

⚠ This is a NEGATIVE assertion ("no grey anywhere"), so it is worthless without a
liveness guard: a typo'd class, a renamed hook or a 404 page all make "no grey"
trivially true. Group B therefore fails if any target class was never found at all.

The greys removed in r120 were $c-gray-200 (#d9d9d9) on 13 boxes, #d5d4d4 on
.gb-crev-card__image, and .gb-scallop-box's --box-bg default. $c-gray-200 itself
stays in the palette -- $color-border still points at it.
"""
import argparse
import pathlib
import sys

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
TRANSPARENT = 'rgba(0, 0, 0, 0)'
GREYS = ('rgb(217, 217, 217)', 'rgb(213, 212, 212)')   # #d9d9d9, #d5d4d4

# class -> pages that carry it (static build)
# ⚠ .gb-rv-panel__video was here until r123: the reel lightbox it belonged to was
# removed when reels became in-place players. The liveness guard caught its absence
# on the first run after -- that is the guard working, not a regression.
TARGETS = {
    'gb-acc-body__media':      ['how-gumi-works.html', 'index.html', 'pdp.html', 'our-story.html', 'reviews.html'],
    'gb-cart-item__media':     ['index.html', 'pdp.html', 'faq.html'],
    'gb-cart__gift-media':     ['index.html', 'pdp.html', 'faq.html'],
    'gb-page-hero__media':     ['reviews.html', 'science.html'],
    'gb-highlight-card__media': ['index.html'],
    'gb-product__thumb':       ['index.html', 'pdp.html', 'reviews.html'],
    'gb-product__image':       ['index.html', 'pdp.html', 'our-story.html'],
    'gb-reel__media':          ['index.html', 'pdp.html', 'our-story.html'],
    'gb-promo-card__media':    ['pdp.html'],
    'gb-crev-card__image':     ['pdp.html', 'reviews.html'],
    'gb-faq-image__media':     ['science.html'],
    'gb-expert-card__media':   ['reviews.html'],
    'gb-story-card__media':    ['our-story.html'],
}

# Not reachable on live: the other team's gb-cart-drawer.liquid renders no
# .gb-cart__gift* at all (HANDOFF r119, "not a bug" #3), and a line item needs a
# non-empty cart. Both DO exist in the static build, where group B still guards them.
LIVE_NA = {'gb-cart-item__media', 'gb-cart__gift-media'}

LIVE_URL = {
    'index.html':          '/',
    'pdp.html':            '/products/superfood-greens-gummies',
    'reviews.html':        '/pages/reviews',
    'science.html':        '/pages/science',
    'our-story.html':      '/pages/our-story',
    'how-gumi-works.html': '/pages/how-gumi-works',
    'faq.html':            '/pages/faqs',
}

PROBE = r"""(cls) => {
  const els = [...document.querySelectorAll('.' + cls)];
  return els.map(e => getComputedStyle(e).backgroundColor);
}"""

# .gb-scallop-box paints through --box-bg on its ::before, so read the pseudo.
SCALLOP = r"""() => {
  const out = {plain: [], disc: []};
  for (const e of document.querySelectorAll('.gb-scallop-box')) {
    const bg = getComputedStyle(e, '::before').backgroundColor;
    (e.classList.contains('gb-ingredients__disc') ? out.disc : out.plain).push(bg);
  }
  return out;
}"""

fails = []
oks = []
found = {k: 0 for k in TARGETS}


def check(name, ok, detail=''):
    print(('  ok   ' if ok else '  FAIL ') + name + ('' if ok else '   ' + detail))
    (oks if ok else fails).append(name)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--live', action='store_true')
    ap.add_argument('--password', default='1234')
    ap.add_argument('--strip', action='store_true', help='inverted run: expect RED')
    args = ap.parse_args()

    pages = sorted({p for ps in TARGETS.values() for p in ps} | {'science.html', 'reviews.html'})
    if args.live:
        pages = [p for p in pages if p in LIVE_URL]

    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME, args=['--no-sandbox'])
        ctx = b.new_context(viewport={'width': 1440, 'height': 900})
        if args.live:
            ctx.request.post('https://gumi.com.au/password',
                             form={'form_type': 'storefront_password', 'utf8': '✓',
                                   'password': args.password})
        pg = ctx.new_page()

        print('=== A. no media box paints a placeholder ground ===')
        for name in pages:
            url = ('https://gumi.com.au' + LIVE_URL[name]) if args.live else (ROOT / name).as_uri()
            try:
                pg.goto(url, wait_until='load' if not args.live else 'networkidle', timeout=60000)
            except Exception as e:
                check('%s loads' % name, False, str(e)[:80]);  continue
            if args.strip:   # inverted run: repaint the greys, judge must go red
                pg.add_style_tag(content='.gb-acc-body__media,.gb-rv-panel__video,'
                                         '.gb-cart-item__media,.gb-cart__gift-media,'
                                         '.gb-page-hero__media,.gb-highlight-card__media,'
                                         '.gb-product__thumb,.gb-product__image,.gb-reel__media,'
                                         '.gb-promo-card__media,.gb-crev-card__image,'
                                         '.gb-faq-image__media,.gb-expert-card__media,'
                                         '.gb-story-card__media{background:#d9d9d9!important}')
            for cls, hosts in TARGETS.items():
                if name not in hosts:
                    continue
                bgs = pg.evaluate(PROBE, cls)
                found[cls] += len(bgs)
                if not bgs:
                    continue   # counted by group B, not a failure here
                bad = [c for c in bgs if c != TRANSPARENT]
                check('%s  .%s  x%d' % (name, cls, len(bgs)), not bad,
                      'painted: %s' % sorted(set(bad))[:3])

        print('\n=== B. liveness -- every target class was actually found ===')
        for cls, n in sorted(found.items()):
            if args.live and cls in LIVE_NA:
                print('  n/a  .%s -- not rendered on live (see LIVE_NA)' % cls)
                continue
            check('.%s located (%d)' % (cls, n), n > 0, 'class never matched -- wrong file or renamed hook')

        print('\n=== C. --box-bg: default transparent, .gb-ingredients__disc keeps its sand ===')
        for name in (['science.html'] if not args.live else ['science.html']):
            url = ('https://gumi.com.au' + LIVE_URL[name]) if args.live else (ROOT / name).as_uri()
            pg.goto(url, wait_until='load' if not args.live else 'networkidle', timeout=60000)
            sc = pg.evaluate(SCALLOP)
            check('%s scallop-box found' % name, bool(sc['plain']) or bool(sc['disc']),
                  'no .gb-scallop-box on the page')
            check('%s plain scallop ::before transparent' % name,
                  all(c == TRANSPARENT for c in sc['plain']), repr(sc['plain'][:3]))
            check('%s .gb-ingredients__disc keeps a ground' % name,
                  all(c not in GREYS and c != TRANSPARENT for c in sc['disc']), repr(sc['disc'][:3]))

        b.close()

    print('\n%d ok / %d red' % (len(oks), len(fails)))
    print('RED: ' + ', '.join(fails) if fails else 'ALL GREEN')
    if args.strip:
        print('\n--strip run: red above is the expected result.')
        return 0
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
