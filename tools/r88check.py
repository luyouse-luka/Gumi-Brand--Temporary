#!/usr/bin/env python3
"""r88 judge -- collection page bottom padding.

  python3 tools/r88check.py --password 1234              # live runs OUR css
  python3 tools/r88check.py --password 1234 --as-served  # live as it is now
  python3 tools/r88check.py --skip-live

--as-served must go RED before a push.

The rule has NO static counterpart: .gb-page-wrapper and .product-grid-container
are both live-only, so every geometry assertion here needs the live site.
"""
import argparse, io, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
SITE = 'https://gumi.com.au'
COLL = SITE + '/collections/all'
BUILD = '20260907-r88'

fails, skips = [], []


def check(name, got, want, tol=None):
    ok = abs(got - want) <= tol if (tol is not None and isinstance(got, (int, float))) else got == want
    print(('  ok   ' if ok else '  FAIL ') + name + ('' if ok else '   got=%r want=%r' % (got, want)))
    if not ok:
        fails.append(name)


print('== compiled css ==')
css = io.open(ROOT / 'assets/customstyle.css', encoding='utf-8').read()
scss = io.open(ROOT / 'assets/customstyle.scss', encoding='utf-8').read()
check('1 $build at or past r88', re.search(r'\$build:\s*"([^"]+)"', scss).group(1) >= BUILD, True)
check('2 desktop base 120',
      re.search(r'\.gb-page-wrapper \.product-grid-container \{\s*padding-block-end: 120px;', css) is not None, True)
check('3 narrow 64',
      re.search(r'@media \(max-width: 767px\) \{\s*\.gb-page-wrapper \.product-grid-container \{\s*'
                r'padding-block-end: 64px;', css) is not None, True)
check('4 tablet ramps 64->120',
      re.search(r'@media \(min-width: 768px\) and \(max-width: 1280px\) \{\s*'
                r'\.gb-page-wrapper \.product-grid-container \{\s*padding-block-end: clamp\(64px,', css) is not None, True)
# The three bands must not overlap -- see CLAUDE.md rule 18.
check('5 no unscoped duplicate', css.count('.gb-page-wrapper .product-grid-container') == 3, True)

PROBE = """() => {
  const R = e => { if (!e) return null; const b = e.getBoundingClientRect();
                   return {top: Math.round(b.top + scrollY), bottom: Math.round(b.bottom + scrollY)}; };
  const rl = document.querySelector('.product-grid-container');
  const grid = document.querySelector('.product-grid');
  const sec = document.querySelector('.gb-footer-cta-section');
  const bear = document.querySelector('.gb-deco-bear--a');
  return {
    pb: rl ? getComputedStyle(rl).paddingBottom : null,
    grid: R(grid), sec: R(sec), bear: R(bear),
    build: getComputedStyle(document.documentElement).getPropertyValue('--build').trim(),
  };
}"""


def run(css_text, password, width, pw):
    b = pw.chromium.launch(executable_path=CHROME, args=['--no-sandbox'])
    ctx = b.new_context(viewport={'width': width, 'height': 900})
    if password:
        r = ctx.request.post(SITE + '/password', form={
            'form_type': 'storefront_password', 'utf8': '✓', 'password': password})
        if r.status in (429, 503):
            b.close()
            raise SystemExit('Cloudflare (HTTP %d) -- back off, do not retry' % r.status)
    if css_text is not None:
        ctx.route(re.compile(r'customstyle\.css'), lambda route: route.fulfill(
            status=200, content_type='text/css', body=css_text))
    pg = ctx.new_page()
    pg.goto(COLL, wait_until='networkidle')
    pg.wait_for_timeout(700)
    out = pg.evaluate(PROBE)
    b.close()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--password')
    ap.add_argument('--as-served', action='store_true')
    ap.add_argument('--skip-live', action='store_true')
    a = ap.parse_args()
    if not a.skip_live:
        from playwright.sync_api import sync_playwright
        body = None if a.as_served else css
        with sync_playwright() as pw:
            for width, want_pb in ((1440, 120), (390, 64), (1024, 91.95)):
                print('== live %d %s ==' % (width, 'as-served' if a.as_served else 'our css'))
                d = run(body, a.password, width, pw)
                if d['pb'] is None:
                    print('  FAIL no .product-grid-container -- storefront password?')
                    fails.append('probe %d' % width)
                    continue
                check('%d padding-bottom' % width, float(d['pb'][:-2]), want_pb, tol=0.6)
                if d['grid'] and d['sec']:
                    check('%d grid->scallop gap' % width,
                          d['sec']['top'] - d['grid']['bottom'], want_pb, tol=1)
                # The CTA bear overhangs upward; at 32 it sat on the product names.
                if d['grid'] and d['bear']:
                    check('%d bear clears the grid' % width, d['bear']['top'] >= d['grid']['bottom'], True)
                if a.as_served:
                    check('%d build' % width, d['build'].strip('"'), BUILD)
    print()
    print('%d FAIL' % len(fails) if fails else 'all green')
    if fails:
        print('failed: ' + ', '.join(fails))
    sys.exit(1 if fails else 0)


main()
