#!/usr/bin/env python3
"""r121 second item: the centred page-hero title is capped at 990.

  python3 tools/r121check.py
  python3 tools/r121check.py --live --password 1234

The ring half of r121 has its own judge: tools/refocusring.py.

⚠ $build is asserted with >=, never ==. A pinned build turns this file red in every
later round and reads as a regression -- r116/r117/r119 all shipped with that bug.
"""
import argparse
import pathlib
import re
import sys

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
LIVE = 'https://gumi.com.au'
# ⚠ Seven, not the five the scss comment lists: our-story and how-gumi-works use the
# variant too. Grepped, not copied from the comment.
# ⚠ /pages/faq, not /pages/faqs -- the latter is a 404 and the liveness guard caught it.
PAGES = [('faq.html', '/pages/faq'), ('get-in-touch.html', '/pages/get-in-touch'),
         ('privacy-policy.html', '/pages/privacy-policy'), ('referral.html', '/pages/referral'),
         ('shipping.html', '/pages/shipping'), ('our-story.html', '/pages/our-story'),
         ('how-gumi-works.html', '/pages/how-gumi-works')]

fails, oks = [], []


def check(name, ok, detail=''):
    print(('  ok   ' if ok else '  FAIL ') + name + ('' if ok else '   ' + detail))
    (oks if ok else fails).append(name)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--live', action='store_true')
    ap.add_argument('--password', default='1234')
    args = ap.parse_args()

    css = (ROOT / 'assets/customstyle.css').read_text(encoding='utf-8')
    b = re.search(r'--build: "(\d{8})-r(\d+)"', css)
    check('$build >= 20260909-r121  (got %s)' % (b.group(0) if b else 'none'),
          bool(b) and (b.group(1), int(b.group(2))) >= ('20260909', 121))

    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=CHROME, args=['--no-sandbox'])
        ctx = br.new_context(viewport={'width': 1440, 'height': 900})
        if args.live:
            ctx.request.post(LIVE + '/password',
                             form={'form_type': 'storefront_password', 'utf8': '✓',
                                   'password': args.password})
        pg = ctx.new_page()
        for name, path in PAGES:
            url = (LIVE + path) if args.live else (ROOT / name).as_uri()
            try:
                pg.goto(url, wait_until='networkidle' if args.live else 'load', timeout=60000)
            except Exception as e:
                check('%s loads' % name, False, str(e)[:70]); continue
            d = pg.evaluate("""() => {
              const t = document.querySelector('.gb-page-hero--center .gb-page-hero__title');
              if (!t) return null;
              const cs = getComputedStyle(t);
              return {max: cs.maxWidth, w: Math.round(t.getBoundingClientRect().width)};
            }""")
            # liveness first: a missing node would make any assertion trivially true
            if not d:
                check('%s  centred hero title present' % name, False, 'selector not found')
                continue
            check('%s  max-width 990px' % name, d['max'] == '990px', repr(d))
            check('%s  rendered width <= 990' % name, d['w'] <= 990, repr(d))
        br.close()

    print('\n%d ok / %d red' % (len(oks), len(fails)))
    print('RED: ' + ', '.join(fails) if fails else 'ALL GREEN')
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
