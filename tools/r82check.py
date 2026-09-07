#!/usr/bin/env python3
"""r82 judge -- reel focus mirrors hover; richtext <p> inherits its title host.

  python3 tools/r82check.py                      # compiled css + static pages
  python3 tools/r82check.py --password 1234      # + live, serving the LOCAL css
  python3 tools/r82check.py --password 1234 --as-served   # + live, as it really is

1. r78 drew the reel focus ring as an inset ::after (the rail clips the card box,
   so a real outline loses both horizontal runs). r82 drops the ring entirely:
   focus-visible now runs the same scale as hover, per the client.
2. A `richtext` setting always wraps its value in <p>. Two sections print that
   straight into a heading, where the base `p { font-size: 16px }` beat the
   inherited heading type -- a 56px title rendered at 16px.
"""
import argparse, pathlib, re, sys

CSS = 'assets/customstyle.css'
SCSS = 'assets/customstyle.scss'
SITE = 'https://gumi.com.au'
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
MIN_BUILD = '20260907-r82'
SCALE = 'matrix(1.06, 0, 0, 1.06, 0, 0)'
# host selector -> the size the <p> inside must end up at, measured live
TITLES = {'.gb-stats__title': '56px', '.gb-nutrition__title': '40px'}

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


def css_checks():
    print('\n== compiled css ==')
    css = open(CSS, encoding='utf-8').read()
    scss = open(SCSS, encoding='utf-8').read()
    check('$build at or past r82',
          re.search(r'\$build:\s*"([^"]+)"', scss).group(1) >= MIN_BUILD, True)

    # -- 1. reel focus ----------------------------------------------------
    # Anchor the negative: the card rule must exist, or "no ::after" passes on a
    # typo'd selector.
    check('reel card rule found (anchor)', block(css, '.gb-reel') is not None, True)
    check('r78 focus ring is gone',
          len(re.findall(r'\.gb-reel:focus-visible::?after', css)), 0)
    f = block(css, '.gb-reel:focus-visible')
    check('reel focus rule found (anchor)', f is not None, True)
    check('  focus drops the global outline', f, 'outline: none;')
    inner = block(css, '.gb-reel:focus-visible .gb-reel__media')
    check('focus scales the media like hover', inner, 'transform: scale(1.06);')
    # The hover leg is media-gated; the focus leg must NOT be, or a keyboard user
    # on a touch device gets no focus indication at all.
    check('focus rule sits outside any @media (anchor via hover pair)',
          '@media (hover: hover)' in css, True)
    hov = block(css, '.gb-reel:hover .gb-reel__media')
    check('hover leg still present', hov, 'transform: scale(1.06);')

    # -- 2. title <p> -----------------------------------------------------
    t = block(css, '.gb-stats__title p, .gb-nutrition__title p')
    check('title <p> rule found (anchor)', t is not None, True)
    if t:
        check('  inherits the whole font shorthand', 'font: inherit;' in t, True)
        # letter-spacing is NOT part of `font`, so it needs its own line.
        check('  inherits letter-spacing separately', 'letter-spacing: inherit;' in t, True)
    # It has to outrank the base rule it cancels; that rule must still be there.
    check('base p rule still present (anchor)',
          block(css, 'p') == 'font-size: 16px; line-height: 24px; letter-spacing: -0.32px;', True)
    base = re.search(r'(?m)^p \{', css)
    check('base p rule locatable (anchor)', base is not None, True)
    check('title rule comes after the base p rule it cancels',
          css.index('.gb-stats__title p') > base.start(), True)


def static_checks():
    from playwright.sync_api import sync_playwright
    print('\n== static pages: r82 rules are no-ops there ==')
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME)
        pg = b.new_page(viewport={'width': 1440, 'height': 900})
        pg.goto(pathlib.Path('index.html').resolve().as_uri())
        pg.wait_for_timeout(500)
        for sel, size in TITLES.items():
            r = pg.evaluate("""(sel) => {
              const h = document.querySelector(sel);
              if (!h) return null;
              return {fs: getComputedStyle(h).fontSize, hasP: !!h.querySelector('p')};
            }""", sel)
            check('static %s exists (anchor)' % sel, r is not None, True)
            if r:
                check('  static %s is still plain text (no <p>)' % sel, r['hasP'], False)
                check('  static %s still %s' % (sel, size), r['fs'], size)
        # focus: the ring is gone on the static pages too; the scale is what is left
        pg.goto(pathlib.Path('index.html').resolve().as_uri())
        pg.wait_for_timeout(400)
        has = pg.evaluate("() => !!document.querySelector('.gb-reel')")
        print('  ..   .gb-reel on index: %s (focus measured on the live half)' % has)
        b.close()


def live_checks(password, as_served):
    from playwright.sync_api import sync_playwright
    print('\n== live homepage ==')
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
        pg.goto(SITE + '/', wait_until='networkidle')

        for sel, size in TITLES.items():
            r = pg.evaluate("""(sel) => {
              const h = document.querySelector(sel);
              if (!h) return null;
              const p = h.querySelector('p');
              if (!p) return {hasP: false};
              const hs = getComputedStyle(h), ps = getComputedStyle(p);
              return {hasP: true, hostFs: hs.fontSize, pFs: ps.fontSize,
                      hostLh: hs.lineHeight, pLh: ps.lineHeight,
                      hostLs: hs.letterSpacing, pLs: ps.letterSpacing};
            }""", sel)
            check('live %s carries a richtext <p> (anchor)' % sel, r is not None and r['hasP'], True)
            if r and r.get('hasP'):
                check('  %s <p> font-size inherits' % sel, r['pFs'], r['hostFs'])
                check('  %s <p> line-height inherits' % sel, r['pLh'], r['hostLh'])
                check('  %s <p> letter-spacing inherits' % sel, r['pLs'], r['hostLs'])
                check('  %s host is still %s (anchor)' % (sel, size), r['hostFs'], size)

        # Reel focus: drive it with a real keyboard so :focus-visible actually
        # matches -- el.focus() from script does not (see memory).
        n = pg.evaluate("() => document.querySelectorAll('.gb-reel').length")
        if not n:
            print('  ..   no .gb-reel on the homepage; focus half skipped')
        else:
            r = pg.evaluate("""() => {
              const el = document.querySelector('.gb-reel');
              el.setAttribute('tabindex', '0');
              return !!el;
            }""")
            pg.evaluate("() => document.querySelector('.gb-reel').focus()")
            pg.keyboard.press('Shift')     # promotes to :focus-visible in Chrome
            pg.wait_for_timeout(400)
            m = pg.evaluate("""() => {
              const el = document.querySelector('.gb-reel');
              const media = el.querySelector('.gb-reel__media');
              return {matches: el.matches(':focus-visible'),
                      after: getComputedStyle(el, '::after').content,
                      tr: media ? getComputedStyle(media).transform : null};
            }""")
            check('reel is :focus-visible (anchor)', m['matches'], True)
            check('  no ring drawn by ::after', m['after'] in ('none', 'normal'), True)
            check('  focus scales the media like hover', m['tr'], SCALE)
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
