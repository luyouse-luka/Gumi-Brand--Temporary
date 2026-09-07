#!/usr/bin/env python3
"""r80 judge -- .gb-product__packed-item icons sized like the static build.

  python3 tools/r80check.py                      # compiled css + static pages
  python3 tools/r80check.py --password 1234      # + live, serving the LOCAL css
  python3 tools/r80check.py --password 1234 --as-served   # + live, as it really is

The vendor swapped the placeholder <svg> circle for an <img> (image_picker).
width/height attributes only declare the ratio, so with no CSS width the icon
rendered at its intrinsic size: measured 171x161 against the board's 34x32.
"""
import argparse, pathlib, re, sys

CSS = 'assets/customstyle.css'
SCSS = 'assets/customstyle.scss'
SITE = 'https://gumi.com.au'
PDP = '/products/superfood-greens-gummies'
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
MIN_BUILD = '20260907-r80'
BOARD = [34, 32]        # packed
BOARD_TASTE = [51, 48]  # taste

fails = []
def check(name, got, want):
    ok = got == want
    print(('  ok   ' if ok else '  FAIL ') + name + ('' if ok else '   got=%s want=%s' % (repr(got), repr(want))))
    if not ok: fails.append(name)

def block(css, sel):
    for m in re.finditer(r'(?m)^([^@{}]+?)\{([^{}]*)\}', css):
        if ' '.join(m.group(1).split()) == sel:
            return ' '.join(m.group(2).split())
    return None

MEASURE = """(sel) => {
  const item = document.querySelector(sel);
  if (!item) return null;
  const icon = item.querySelector('img, svg');
  if (!icon) return {tag: null};
  const r = icon.getBoundingClientRect(), cs = getComputedStyle(icon);
  return {
    tag: icon.tagName.toLowerCase(),
    w: Math.round(r.width), h: Math.round(r.height),
    shrink: cs.flexShrink, fit: cs.objectFit,
    rowH: Math.round(item.getBoundingClientRect().height),
    gap: getComputedStyle(item).gap,
  };
}"""

# Not asserted -- the same <img> swap hit .gb-product__guarantee too and it is
# NOT in scope (the ask named packed and taste). Printed so the next round can
# see whether it was handled. NB it sits on 5 pages, not just the PDP.
NEIGHBOURS = """() => ['guarantee'].map(k => {
  const it = document.querySelector('.gb-product__' + k + '-item');
  if (!it) return k + ': not on page';
  const i = it.querySelector('img, svg');
  if (!i) return k + ': no icon';
  const r = i.getBoundingClientRect();
  return k + ': <' + i.tagName.toLowerCase() + '> ' + Math.round(r.width) + 'x' + Math.round(r.height);
})"""


def css_checks():
    print('\n== compiled css ==')
    css = open(CSS, encoding='utf-8').read()
    scss = open(SCSS, encoding='utf-8').read()
    check('$build at or past r80',
          re.search(r'\$build:\s*"([^"]+)"', scss).group(1) >= MIN_BUILD, True)

    b = block(css, '.gb-product__packed-item svg, .gb-product__packed-item img')
    check('icon rule covers svg AND img (anchor)', b is not None, True)
    if b:
        check('  width is the board 34', 'width: 34px;' in b, True)
        check('  height is the board 32', 'height: 32px;' in b, True)
        check('  does not shrink', 'flex-shrink: 0;' in b, True)
        check('  non-34:32 source not stretched', 'object-fit: contain;' in b, True)
        check('  svg still takes its colour', 'color: #faf9f8;' in b, True)
    t = block(css, '.gb-product__taste-item svg, .gb-product__taste-item img')
    check('taste rule covers svg AND img (anchor)', t is not None, True)
    if t:
        check('  taste width is the board 51', 'width: 51px;' in t, True)
        check('  taste height is the board 48', 'height: 48px;' in t, True)
        check('  taste not stretched', 'object-fit: contain;' in t, True)
        # Column flow: the board pins no flex-shrink here and the static svg
        # carries none, so adding one would be a deviation, not a fix.
        check('  taste carries no flex-shrink (matches static)', 'flex-shrink' not in t, True)

    # Specificity: 0-1-1 must outrank the reset's `img { height: auto }` (0-0-1),
    # or the height above is silently dropped on live.
    check('reset height:auto still present (anchor)', block(css, 'img') is not None, True)
    # The board value carries every tier; a stray override would break live only.
    check('no responsive override of the packed icon',
          len(re.findall(r'\.gb-product__packed-item (svg|img)', css)), 2)
    check('no responsive override of the taste icon',
          len(re.findall(r'\.gb-product__taste-item (svg|img)', css)), 2)


def static_checks():
    from playwright.sync_api import sync_playwright
    print('\n== static pdp.html: unchanged ==')
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME)
        pg = b.new_page(viewport={'width': 1440, 'height': 900})
        pg.goto(pathlib.Path('pdp.html').resolve().as_uri())
        pg.wait_for_timeout(400)
        r = pg.evaluate(MEASURE, '.gb-product__packed-item')
        check('static packed icon is still the placeholder svg', r and r['tag'], 'svg')
        check('static packed icon still 34x32', [r['w'], r['h']], BOARD)
        check('static packed icon still does not shrink', r['shrink'], '0')
        check('static packed row still 32 tall', r['rowH'], 32)
        check('static packed gap still 16', r['gap'], '16px')
        t = pg.evaluate(MEASURE, '.gb-product__taste-item')
        check('static taste icon is still the placeholder svg', t and t['tag'], 'svg')
        check('static taste icon still 51x48', [t['w'], t['h']], BOARD_TASTE)
        check('static taste gap still 8', t['gap'], '8px')
        print('   guarantee (NOT in scope): ' + '; '.join(pg.evaluate(NEIGHBOURS)))
        b.close()


def live_checks(password, as_served):
    from playwright.sync_api import sync_playwright
    print('\n== live PDP ==')
    body_css = None if as_served else open(CSS, encoding='utf-8').read()
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME)
        ctx = b.new_context()
        r = ctx.request.post(SITE + '/password', form={
            'form_type': 'storefront_password', 'utf8': '✓', 'password': password})
        if r.status in (429, 503):
            raise SystemExit('blocked by Cloudflare (HTTP %d) -- back off and rerun' % r.status)
        pg = ctx.new_page(); pg.set_viewport_size({'width': 1440, 'height': 900})
        if body_css is not None:
            pg.route('**/customstyle.css*', lambda rt: rt.fulfill(
                status=200, content_type='text/css', body=body_css))
        pg.goto(SITE + PDP, wait_until='networkidle')
        m = pg.evaluate(MEASURE, '.gb-product__packed-item')
        if m is None:
            raise SystemExit('no packed row at %s -- title=%r' % (pg.url, pg.title()))
        # Anchor the whole point of the round: live really does ship an <img>.
        check('live packed icon is an <img> (anchor)', m['tag'], 'img')
        check('live packed icon sized to the board 34x32', [m['w'], m['h']], BOARD)
        check('live packed icon does not shrink', m['shrink'], '0')
        check('live packed icon not stretched', m['fit'], 'contain')
        check('live packed row back to 32 tall', m['rowH'], 32)
        check('live packed gap matches the static build', m['gap'], '16px')

        t = pg.evaluate(MEASURE, '.gb-product__taste-item')
        check('live taste icon is an <img> (anchor)', t and t['tag'], 'img')
        check('live taste icon sized to the board 51x48', [t['w'], t['h']], BOARD_TASTE)
        check('live taste icon not stretched', t['fit'], 'contain')
        check('live taste gap matches the static build', t['gap'], '8px')
        print('   guarantee (NOT in scope this round): ' + '; '.join(pg.evaluate(NEIGHBOURS)))
        b.close()


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--password'); ap.add_argument('--as-served', action='store_true')
    ap.add_argument('--skip-static', action='store_true')
    a = ap.parse_args()
    css_checks()
    if not a.skip_static: static_checks()
    if a.password: live_checks(a.password, a.as_served)
    print('\n' + ('%d FAIL: ' % len(fails) + ', '.join(fails) if fails else 'all assertions ok'))
    sys.exit(1 if fails else 0)
