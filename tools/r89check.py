#!/usr/bin/env python3
"""r89 judge -- product padding-top tiers plus the promo card's rebuilt scallop.

  python3 tools/r89check.py --password 1234              # live runs OUR css
  python3 tools/r89check.py --password 1234 --as-served  # live as it is now
  python3 tools/r89check.py --skip-live

--as-served must go RED before a push.

⚠ The base .gb-product has NO live counterpart: sections/gb-product.liquid only
ever emits `gb-product gb-product--lg` or `gb-product gb-product--page`, so the
flat 32 is graded on the static build (how-gumi-works / reviews / our-story).
"""
import argparse, io, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
SITE = 'https://gumi.com.au'
BUILD = '20260907-r89'
GREEN = 'rgb(0, 86, 53)'
CLEAR = 'rgba(0, 0, 0, 0)'

fails = []


def check(name, got, want):
    ok = got == want
    print(('  ok   ' if ok else '  FAIL ') + name + ('' if ok else '   got=%r want=%r' % (got, want)))
    if not ok:
        fails.append(name)


print('== compiled css ==')
css = io.open(ROOT / 'assets/customstyle.css', encoding='utf-8').read()
scss = io.open(ROOT / 'assets/customstyle.scss', encoding='utf-8').read()
check('1 $build at or past r89', re.search(r'\$build:\s*"([^"]+)"', scss).group(1) >= BUILD, True)
# The base class must be a flat 32 -- no tier may reintroduce 52 or 96 on top.
# Parsed rather than substring-matched: a bare `in css` would pass on any other
# block that happens to open with 32.
def _shorthand_top(block):
    for decl in ' '.join(block.split()).split(';'):
        name, _, value = decl.partition(':')
        if name.strip() == 'padding':
            return value.split()[0]
    return None


_base_tops = [t for _, b in re.findall(r'(?m)^(\s*)\.gb-product \{([^}]*)\}', css)
              for t in [_shorthand_top(b)] if t]
check('2 base has exactly three tiers', len(_base_tops), 3)
check('2b every base tier opens at 32', set(_base_tops), {'32px'})
check('3 --lg restates the ramp', re.search(
    r'\.gb-product--lg \{\s*padding-top: 96px;', css) is not None, True)
check('4 --lg narrow 52', re.search(
    r'\.gb-product--lg \{\s*padding-top: 52px;', css) is not None, True)
check('5 --page restates 96', re.search(
    r'\.gb-product--page \{\s*padding-top: 96px;', css) is not None, True)
# The green must have left the card except below 768.
check('6 card keeps green only under 768', re.search(
    r'@media \(max-width: 767px\) \{\s*\.gb-promo-card--green \{\s*background: #005635;', css) is not None, True)
check('7 green moved to the copy half',
      '.gb-promo-card--green .gb-promo-card__body {\n  background: #005635;' in css, True)
check('8 scallop is masked, not an element',
      css.count('.gb-promo-card--green .gb-promo-card__body::before') == 2, True)
# >= not ==: r90 gives the white card the same mask, and this assertion is about
# the prefix being emitted at all, not about how many cards use it.
check('9 webkit prefix shipped', css.count('-webkit-mask: url("data:image/svg+xml,%3Csvg width=\'126\'') >= 1, True)

PROBE = """() => {
  const cs=(s,p)=>{const e=document.querySelector(s); return e?getComputedStyle(e)[p]:null;};
  const bef=(s,p)=>{const e=document.querySelector(s); return e?getComputedStyle(e,'::before')[p]:null;};
  const L=s=>{const e=document.querySelector(s); if(!e)return null; return Math.round(e.getBoundingClientRect().left);};
  return {
    base: cs('.gb-product:not(.gb-product--lg):not(.gb-product--page)','paddingTop'),
    lg: cs('.gb-product--lg','paddingTop'),
    page: cs('.gb-product--page','paddingTop'),
    cardBg: cs('.gb-promo-card--green','backgroundColor'),
    bodyBg: cs('.gb-promo-card--green .gb-promo-card__body','backgroundColor'),
    befDisp: bef('.gb-promo-card--green .gb-promo-card__body','display'),
    befLeft: bef('.gb-promo-card--green .gb-promo-card__body','left'),
    hasMask: (bef('.gb-promo-card--green .gb-promo-card__body','maskImage')||'none') !== 'none',
    bodyL: L('.gb-promo-card--green .gb-promo-card__body'),
    lipL: L('.gb-promo-card--green .gb-promo-card__lip--v'),
    build: getComputedStyle(document.documentElement).getPropertyValue('--build').trim(),
  };
}"""


def grade(tag, d, width):
    if width == 1440:
        if d['lg']: check(tag + ' --lg 96', d['lg'], '96px')
        if d['page']: check(tag + ' --page 96', d['page'], '96px')
        if d['base']: check(tag + ' base 32', d['base'], '32px')
        if d['bodyBg']:
            check(tag + ' card transparent', d['cardBg'], CLEAR)
            check(tag + ' body green', d['bodyBg'], GREEN)
            check(tag + ' scallop painted', d['befDisp'] == 'block' and d['hasMask'], True)
            check(tag + ' scallop offset', d['befLeft'], '-31px')
            # Static build still ships the real SVG: the two must sit on top of
            # each other, or the rebuild is in the wrong place.
            if d['lipL'] is not None and d['bodyL'] is not None:
                check(tag + ' scallop lines up with the svg', d['bodyL'] - 31, d['lipL'])
    else:
        if d['lg']: check(tag + ' --lg narrow 52', d['lg'], '52px')
        if d['page']: check(tag + ' --page narrow 20', d['page'], '20px')
        if d['base']: check(tag + ' base narrow 32', d['base'], '32px')
        if d['bodyBg']:
            check(tag + ' card keeps green', d['cardBg'], GREEN)
            check(tag + ' scallop hidden', d['befDisp'], 'none')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--password')
    ap.add_argument('--as-served', action='store_true')
    ap.add_argument('--skip-live', action='store_true')
    a = ap.parse_args()
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        br = pw.chromium.launch(executable_path=CHROME, args=['--no-sandbox'])
        for width in (1440, 390):
            print('== static %d ==' % width)
            pg = br.new_context(viewport={'width': width, 'height': 900}).new_page()
            for name in ('how-gumi-works', 'index', 'pdp'):
                pg.goto('file://%s/%s.html' % (ROOT, name), wait_until='load')
                pg.wait_for_timeout(700)
                grade('%s %d' % (name, width), pg.evaluate(PROBE), width)
            if a.skip_live:
                continue
            print('== live %d %s ==' % (width, 'as-served' if a.as_served else 'our css'))
            ctx = br.new_context(viewport={'width': width, 'height': 900})
            r = ctx.request.post(SITE + '/password', form={
                'form_type': 'storefront_password', 'utf8': '✓', 'password': a.password})
            if r.status in (429, 503):
                br.close()
                raise SystemExit('Cloudflare (HTTP %d) -- back off, do not retry' % r.status)
            if not a.as_served:
                ctx.route(re.compile(r'customstyle\.css'), lambda route: route.fulfill(
                    status=200, content_type='text/css', body=css))
            for name, path in (('pdp', '/products/superfood-greens-gummies'), ('home', '/')):
                pg = ctx.new_page()
                pg.goto(SITE + path, wait_until='networkidle')
                pg.wait_for_timeout(700)
                d = pg.evaluate(PROBE)
                pg.close()
                grade('live %s %d' % (name, width), d, width)
                if a.as_served and width == 1440 and name == 'pdp':
                    check('live build', d['build'].strip('"') >= BUILD, True)
            ctx.close()
        br.close()
    print()
    print(('%d FAIL' % len(fails)) if fails else 'all green')
    sys.exit(1 if fails else 0)


main()
