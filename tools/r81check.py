#!/usr/bin/env python3
"""r81 judge -- product gallery boxes fit with `contain`, everything else keeps `cover`.

  python3 tools/r81check.py                      # compiled css + static pages
  python3 tools/r81check.py --password 1234      # + live, serving the LOCAL css
  python3 tools/r81check.py --password 1234 --as-served   # + live, as it really is

r64 set `cover` across all nine placeholder boxes on the client's instruction.
r81 overturns that for the two that carry product photography: a product shot
must not be cropped. The grey ground shows as letterboxing where the source is
off-ratio -- that is the intended trade, not a bug.
"""
import argparse, pathlib, re, sys

CSS = 'assets/customstyle.css'
SCSS = 'assets/customstyle.scss'
SITE = 'https://gumi.com.au'
PDP = '/products/superfood-greens-gummies'
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
MIN_BUILD = '20260907-r81'
CONTAIN = ['.gb-product__image', '.gb-product__thumb']

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

FIT = """(sel) => {
  const box = document.querySelector(sel);
  if (!box) return null;
  const el = box.querySelector('img, video');
  if (!el) return {tag: null};
  const cs = getComputedStyle(el);
  return {tag: el.tagName.toLowerCase(), fit: cs.objectFit,
          w: cs.width, h: cs.height, display: cs.display};
}"""


def css_checks():
    print('\n== compiled css ==')
    css = open(CSS, encoding='utf-8').read()
    scss = open(SCSS, encoding='utf-8').read()
    check('$build at or past r81',
          re.search(r'\$build:\s*"([^"]+)"', scss).group(1) >= MIN_BUILD, True)

    for sel in CONTAIN:
        full = ', '.join('%s %s' % (sel, t) for t in ('img', 'video', 'picture'))
        b = block(css, full)
        check('%s rule found (anchor)' % sel, b is not None, True)
        if b:
            check('  %s fits with contain' % sel, 'object-fit: contain;' in b, True)
            # A second object-fit would work by source order but inflates every
            # "count the covers" judge (r64check does exactly that).
            check('  %s declares object-fit once' % sel, b.count('object-fit'), 1)
            check('  %s still fills the box' % sel,
                  'width: 100%;' in b and 'height: 100%;' in b, True)

    # The mixin default must stay cover: eleven other placeholder boxes read it,
    # and flipping the default would silently change all of them.
    m = re.search(r'@mixin cover-img\(\$fit:\s*(\w+)\)', scss)
    check('mixin default still cover (anchor)', m and m.group(1), 'cover')
    check('only two callers pass contain',
          len(re.findall(r'@include cover-img\(contain\)', scss)), 2)
    # 13 include sites total; 11 of them must still emit cover.
    check('cover still emitted 13x in the product',
          len(re.findall(r'object-fit: cover', css)), 13)
    # ⚠ Count on the STRIPPED source: a comment mentioning the mixin would be
    # counted as a call site. r63check was bitten by exactly this.
    stripped = re.sub(r'//[^\n]*', '', scss)
    check('mixin called 13x (comments stripped)',
          len(re.findall(r'@include cover-img', stripped)), 13)


def static_checks():
    from playwright.sync_api import sync_playwright
    print('\n== static pages ==')
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME)
        pg = b.new_page(viewport={'width': 1440, 'height': 900})
        pg.goto(pathlib.Path('pdp.html').resolve().as_uri())
        pg.wait_for_timeout(400)
        for sel in CONTAIN:
            r = pg.evaluate(FIT, sel)
            # The box must exist; its CONTENTS must not. The static build ships
            # these as empty grey placeholders ("no product photos exist yet" --
            # see the scss note), so the rule has nothing to act on here and the
            # real measurement lives in the live half. Asserting media here was
            # the anchor pointing the wrong way.
            check('static %s box exists (anchor)' % sel, r is not None, True)
            check('  static %s is still an empty placeholder' % sel,
                  r is not None and r['tag'] is None, True)
        # Negative side: an untouched placeholder must still be cover, or the
        # change leaked into the mixin.
        other = pg.evaluate(FIT, '.gb-promo-card__media')
        if other and other['tag']:
            check('untouched placeholder still cover', other['fit'], 'cover')
        else:
            print('  ..   .gb-promo-card__media not on this page; cover side covered by r64check')
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
        for sel in CONTAIN:
            m = pg.evaluate(FIT, sel)
            check('live %s has media (anchor)' % sel, m is not None and m['tag'] is not None, True)
            if m and m['tag']:
                check('  live %s fits with contain' % sel, m['fit'], 'contain')
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
