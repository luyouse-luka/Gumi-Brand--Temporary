#!/usr/bin/env python3
"""r83 judge -- science title capped at 660 and centred; card text loses its top margin.

  python3 tools/r83check.py                      # compiled css + static pages
  python3 tools/r83check.py --password 1234      # + live, serving the LOCAL css
  python3 tools/r83check.py --password 1234 --as-served   # + live, as it really is

⚠ The narrow `margin: 0` is load-bearing, not tidy-up. .gb-science__head switches
to align-items:flex-start on phones (board 228:8166, both TEXT nodes LEFT), and an
auto margin OUTRANKS align-items -- without the reset the title centres there.
"""
import argparse, pathlib, re, sys

CSS, SCSS = 'assets/customstyle.css', 'assets/customstyle.scss'
SITE = 'https://gumi.com.au'
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
MIN_BUILD = '20260907-r83'

fails = []
skips = []
def check(name, got, want):
    ok = got == want
    print(('  ok   ' if ok else '  FAIL ') + name + ('' if ok else '   got=%s want=%s' % (repr(got), repr(want))))
    if not ok: fails.append(name)

def block(css, sel):
    for m in re.finditer(r'(?m)^([^@{}]+?)\{([^{}]*)\}', css):
        if ' '.join(m.group(1).split()) == sel:
            return ' '.join(m.group(2).split())
    return None

GEO = """() => {
  const h = document.querySelector('.gb-science__title');
  if (!h) return null;
  const head = h.closest('.gb-science__head');
  const hb = h.getBoundingClientRect(), pb = head.getBoundingClientRect();
  const t = document.querySelector('.gb-science-card__text');
  return {
    align: getComputedStyle(head).alignItems,
    ml: getComputedStyle(h).marginLeft,
    maxW: getComputedStyle(h).maxWidth,
    gapL: Math.round(hb.left - pb.left),
    gapR: Math.round(pb.right - hb.right),
    textMt: t ? getComputedStyle(t).marginTop : null,
  };
}"""


def css_checks():
    print('\n== compiled css ==')
    css = open(CSS, encoding='utf-8').read()
    scss = open(SCSS, encoding='utf-8').read()
    check('$build at or past r83',
          re.search(r'\$build:\s*"([^"]+)"', scss).group(1) >= MIN_BUILD, True)

    t = block(css, '.gb-science__title')
    check('title rule found (anchor)', t is not None, True)
    if t:
        check('  max-width is 660', 'max-width: 660px;' in t, True)
        check('  centred with auto margins', 'margin: 0 auto;' in t, True)
        check('  1072 is gone', '1072px' not in t, True)

    # The narrow reset must exist, or phones lose the board's left alignment.
    m = re.search(r'@media \(max-width: 767px\) \{\s*\.gb-science__title \{([^}]*)\}', css)
    check('narrow override found (anchor)', m is not None, True)
    if m:
        check('  narrow drops the auto margin', 'margin: 0;' in m.group(1), True)

    c = block(css, '.gb-science-card__text')
    check('card text rule found (anchor)', c is not None, True)
    if c:
        check('  no top margin declared', 'margin-top' not in c, True)
        # It relies on the reset, so that has to still be there.
        check('  base p margin reset still present (anchor)',
              block(css, 'h1, h2, h3, h4, h5, h6, p, figure, blockquote, dl, dd') == 'margin: 0;', True)


def render_checks(pg, tag):
    for w, want in ((1440, 'centre'), (1024, 'centre'), (767, 'left'), (390, 'left')):
        pg.set_viewport_size({'width': w, 'height': 900})
        pg.wait_for_timeout(350)
        r = pg.evaluate(GEO)
        if r is None:
            print('  ..   %s %s: no .gb-science__title on this page' % (tag, w)); continue
        # ⚠ Assert the mechanism, not a per-page verdict. A title that fills its
        # head has gapL == gapR == 0 whatever the alignment is, so there is
        # nothing for `margin: 0 auto` to distribute and no way to tell centred
        # from left by geometry. That is the case on the Science page at every
        # width -- announcing the skip rather than hard-coding an expectation.
        if want == 'centre':
            if r['gapL'] + r['gapR'] < 2:
                skips.append('%s %s centring' % (tag, w))
                print('  SKIP %s %s centring   (title fills its head, nothing to distribute)' % (tag, w))
            else:
                check('%s %s title centred' % (tag, w), abs(r['gapL'] - r['gapR']) < 2, True)
        else:
            check('%s %s title flush left' % (tag, w), r['gapL'] < 2, True)
        check('  %s %s max-width 660' % (tag, w), r['maxW'], '660px')
        if want == 'left':
            # The reason this can fail: auto margin outranks align-items.
            check('  %s %s auto margin dropped' % (tag, w), r['ml'], '0px')
            check('  %s %s head is flex-start (anchor)' % (tag, w), r['align'], 'flex-start')
        if r['textMt'] is not None:
            check('  %s %s card text has no top margin' % (tag, w), r['textMt'], '0px')


def static_checks():
    from playwright.sync_api import sync_playwright
    print('\n== static pages ==')
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME)
        pg = b.new_page(viewport={'width': 1440, 'height': 900})
        for f in ('index.html', 'science.html'):
            pg.goto(pathlib.Path(f).resolve().as_uri())
            pg.wait_for_timeout(500)
            render_checks(pg, f.split('.')[0])
        b.close()


def live_checks(password, as_served):
    from playwright.sync_api import sync_playwright
    print('\n== live /pages/science ==')
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
        # Both hosts: /pages/science fills its head at every width (nothing to
        # centre), so the homepage is the only place the 660 cap actually bites.
        for path, tag in (('/', 'live-home'), ('/pages/science', 'live-science')):
            pg.goto(SITE + path, wait_until='networkidle')
            if not pg.evaluate("() => !!document.querySelector('.gb-science__title')"):
                raise SystemExit('no .gb-science__title at %s -- title=%r' % (pg.url, pg.title()))
            render_checks(pg, tag)
        b.close()


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--password'); ap.add_argument('--as-served', action='store_true')
    ap.add_argument('--skip-static', action='store_true')
    a = ap.parse_args()
    css_checks()
    if not a.skip_static: static_checks()
    if a.password: live_checks(a.password, a.as_served)
    if skips: print('\n%d SKIPPED: %s' % (len(skips), ', '.join(skips)))
    print('\n' + ('%d FAIL: ' % len(fails) + ', '.join(fails) if fails else 'all assertions ok'))
    sys.exit(1 if fails else 0)
