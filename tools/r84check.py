#!/usr/bin/env python3
"""r84 judge -- four cascade losses to Horizon's own CSS, repaired at 0-2-0
(footer newsletter input, contact/referral fields, referral disclaimer margin)
plus the three PDP sections Horizon's .section grid was narrowing.

  python3 tools/r84check.py --password 1234              # live runs OUR css
  python3 tools/r84check.py --password 1234 --as-served  # live as it is now
  python3 tools/r84check.py --skip-live

--as-served must go RED before a push; if it passes, the probe is not reaching
the declarations it claims to grade. CSS is swapped with page.route, never
add_style_tag -- an appended sheet wins every equal-specificity tie and would
grade a specificity fix as passing whatever its selector said.
"""
import argparse, io, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
SITE = 'https://gumi.com.au'
BUILD = '20260907-r84'
INK10 = 'rgba(1, 19, 7, 0.1)'
GRAY300 = 'rgb(204, 204, 204)'
WHITE = 'rgb(255, 255, 255)'

fails, skips = [], []


def check(name, got, want):
    ok = got == want
    print(('  ok   ' if ok else '  FAIL ') + name +
          ('' if ok else '   got=%r want=%r' % (got, want)))
    if not ok:
        fails.append(name)


def skip(name, why):
    print('  SKIP ' + name + '   -- ' + why)
    skips.append(name)


def block(css, sel):
    for m in re.finditer(r'(?m)^([^@{}]+?)\{([^{}]*)\}', css):
        if ' '.join(m.group(1).split()) == sel:
            return ' '.join(m.group(2).split())
    return None


print('== compiled css ==')
css = io.open(ROOT / 'assets/customstyle.css', encoding='utf-8').read()
scss = io.open(ROOT / 'assets/customstyle.scss', encoding='utf-8').read()
check('$build at or past r84',
      re.search(r'\$build:\s*"([^"]+)"', scss).group(1) >= BUILD, True)

check('footer input repair', block(css, '.gb-footer__input.gb-footer__input'),
      'background-color: #ffffff; border-color: rgba(1, 19, 7, 0.1);')
check('field repair', block(css, '.gb-field__control.gb-field__control, .gb-field__input.gb-field__input'),
      'background-color: #ffffff; border-color: #cccccc;')
check('section grid escape', block(css, '.section > .gb-promo, .section > .gb-vs, .section > .gb-app-section'),
      'grid-column: 1/-1;')

# ⚠ Source order is load-bearing for the two input repairs: the states they must
# NOT beat are 0-2-0 as well, so the repair has to come FIRST in the file.
for repair, state in (('.gb-footer__input.gb-footer__input', '.gb-footer__input:focus-visible'),
                      ('.gb-field__input.gb-field__input', '.gb-field__input--select:hover')):
    i, j = css.find(repair), css.find(state)
    check('%s still follows the repair' % state, i != -1 and j != -1 and i < j, True)

# The disclaimer repair lives inside two media blocks, so block() cannot see it.
check('disclaimer repair in narrow',
      re.search(r'@media \(max-width: 767px\)[^@]*?\.gb-form__disclaimer\.gb-form__disclaimer \{\s*margin: 16px 0 -2px;', css) is not None, True)
check('disclaimer repair in tablet',
      css.count('.gb-form__disclaimer.gb-form__disclaimer') == 2, True)


PROBE = """() => {
  const q = (s) => document.querySelector(s);
  const cs = (s) => { const e = q(s); return e ? getComputedStyle(e) : null; };
  const out = {};
  const fi = cs('.gb-footer__input');
  out.footer = fi && [fi.borderTopColor, fi.backgroundColor];
  const gi = cs('.gb-field__input');
  out.field = gi && [gi.borderTopColor, gi.backgroundColor];
  const dc = cs('.gb-form__disclaimer');
  out.disclaimer = dc && dc.marginBottom;
  out.sections = {};
  for (const k of ['gb-promo', 'gb-vs', 'gb-app-section']) {
    const el = q('.' + k);
    if (!el) { out.sections[k] = null; continue; }
    // full bleed means: as wide as the wrapper Horizon put it in
    const host = el.parentElement;
    out.sections[k] = [Math.round(el.getBoundingClientRect().width),
                       Math.round(host.getBoundingClientRect().width)];
  }
  return out;
}"""


def run(pw, tag, urls, css_text, password, width):
    b = pw.chromium.launch(executable_path=CHROME)
    ctx = b.new_context(viewport={'width': width, 'height': 1000})
    if password:
        r = ctx.request.post(SITE + '/password', form={
            'form_type': 'storefront_password', 'utf8': '✓', 'password': password})
        if r.status in (429, 503):
            b.close()
            raise SystemExit('Cloudflare (HTTP %d) -- back off, do not retry' % r.status)
    if css_text is not None:
        ctx.route(re.compile(r'customstyle\.css'), lambda route: route.fulfill(
            status=200, content_type='text/css', body=css_text))
    res = {}
    for name, url in urls:
        pg = ctx.new_page()
        pg.goto(url, wait_until='networkidle', timeout=45000)
        pg.wait_for_timeout(500)
        res[name] = pg.evaluate(PROBE)
        pg.close()
    b.close()
    return res


def grade(tag, res, live, width=1440):
    print('\n== %s ==' % tag)
    for page in res:
        d = res[page]
        if d['footer']:
            check('%s footer input border' % page, d['footer'][0], INK10)
            check('%s footer input ground' % page, d['footer'][1], WHITE)
        else:
            check('%s footer input found (anchor)' % page, False, True)
        if d['field']:
            check('%s field border' % page, d['field'][0], GRAY300)
        if d['disclaimer'] is not None:
            # The negative bottom is a mobile-board value; the tablet ramp takes it
            # back to 0 by 1280, so desktop expects 0 and only <=767 expects -2.
            check('%s disclaimer margin-bottom' % page, d['disclaimer'],
                  '-2px' if width <= 767 else '0px')
        for k, v in d['sections'].items():
            if v is None: continue
            check('%s .%s fills its wrapper' % (page, k), v[0], v[1])


def main():
    from playwright.sync_api import sync_playwright
    ap = argparse.ArgumentParser()
    ap.add_argument('--password')
    ap.add_argument('--as-served', action='store_true')
    ap.add_argument('--skip-live', action='store_true')
    ap.add_argument('--skip-static', action='store_true')
    a = ap.parse_args()
    ours = io.open(ROOT / 'assets/customstyle.css', encoding='utf-8').read()

    with sync_playwright() as pw:
        if not a.skip_static:
            # No-op check: none of the four rules may change the static site.
            # .section does not exist there and the repairs restate the same values.
            for w in (1440, 390):
                res = run(pw, 'static', [(n, (ROOT / (n + '.html')).as_uri())
                                         for n in ('index', 'get-in-touch', 'referral', 'pdp')],
                          None, None, w)
                grade('static @%d' % w, res, False, w)

        if a.skip_live or not a.password:
            skip('live half', 'no --password' if not a.password else '--skip-live')
        else:
            urls = [('index', SITE + '/'), ('get-in-touch', SITE + '/pages/get-in-touch'),
                    ('referral', SITE + '/pages/referral'),
                    ('pdp', SITE + '/products/superfood-greens-gummies')]
            for w in (1440, 390):
                res = run(pw, 'live', urls, None if a.as_served else ours, a.password, w)
                grade('live @%d%s' % (w, '  (as served)' if a.as_served else '  (our css)'),
                      res, True, w)

    print()
    if skips:
        print('%d SKIPPED: %s' % (len(skips), ', '.join(skips)))
    if fails:
        print('%d FAIL: %s' % (len(fails), ', '.join(fails[:12])))
    else:
        print('all assertions ok')
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
