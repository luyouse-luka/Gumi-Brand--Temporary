#!/usr/bin/env python3
"""r90 judge -- five client-named fixes.

  python3 tools/r90check.py --password 1234              # live runs OUR css
  python3 tools/r90check.py --password 1234 --as-served  # live as it is now
  python3 tools/r90check.py --skip-live

--as-served must go RED before a push.

⚠ Two of the five are LIQUID and routing cannot reach them, so they stay red
until sections/gb-header.liquid and blocks/gb-title.liquid are pushed:
  - the h1 assertion
  - the two-list menu assertions
⚠ The menu also depends on the ADMIN: the mobile link list has to carry the full
six-entry phone menu. Until it does, the phone list is short and that is a data
gap, not a CSS one -- see docs/LIVE-BACKLOG.md.
"""
import argparse, io, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
SITE = 'https://gumi.com.au'
PDP = SITE + '/products/superfood-greens-gummies'
BUILD = '20260907-r90'

fails = []


def check(name, got, want):
    ok = got == want
    print(('  ok   ' if ok else '  FAIL ') + name + ('' if ok else '   got=%r want=%r' % (got, want)))
    if not ok:
        fails.append(name)


print('== compiled css / liquid ==')
css = io.open(ROOT / 'assets/customstyle.css', encoding='utf-8').read()
scss = io.open(ROOT / 'assets/customstyle.scss', encoding='utf-8').read()
hdr = io.open(ROOT / 'liquid/sections/gb-header.liquid', encoding='utf-8').read()
ttl = io.open(ROOT / 'liquid/blocks/gb-title.liquid', encoding='utf-8').read()
check('1 $build at or past r90', re.search(r'\$build:\s*"([^"]+)"', scss).group(1) >= BUILD, True)
check('2 header emits two lists', hdr.count('class="gb-header__links gb-header__links--') == 2, True)
# Class ATTRIBUTES only -- the comment above the markup names the old class on
# purpose, and a bare substring test would match that and never go green.
check('3 per-item mobile class no longer used',
      re.search(r'class="[^"]*gb-header__links-item--mobile', hdr) is not None, False)
check('4 title block is an h1', ttl.count('<h1 class="gb-product__title"') == 1, True)
check('5 desktop list hides under 768', re.search(
    r'@media \(max-width: 767px\) \{\s*\.gb-header__links--desktop \{\s*display: none;', css) is not None, True)
check('6 mobile list hidden by default', re.search(
    r'\.gb-header__links--mobile \{\s*display: none;', css) is not None, True)
check('7 form rebuilds the 24 rhythm', re.search(
    r'\.gb-product__form \{\s*display: flex;\s*flex-direction: column;\s*gap: 24px;', css) is not None, True)
check('8 head group walks back to 16', css.count('margin-top: -8px') >= 1, True)
check('9 empty block is dropped', ':not(:has(*))' in css, True)
check('10 white card gets the mask', css.count('.gb-promo-card--white .gb-promo-card__body::before') == 2, True)
check('11 vs table is a grid', re.search(
    r'\.gb-vs__table \{\s*display: grid;', css) is not None, True)
check('12 columns share the parent rows', re.search(
    r'\.gb-vs__col \{[^}]*grid-template-rows: subgrid;', css) is not None, True)
check('13 last track absorbs the slack', 'repeat(19, auto) 1fr' in css, True)

PROBE = """() => {
  const R=e=>{if(!e)return null;const b=e.getBoundingClientRect();return {t:Math.round(b.top+scrollY),b:Math.round(b.bottom+scrollY)};};
  const q=s=>document.querySelector(s);
  const bef=(s,p)=>{const e=q(s); return e?getComputedStyle(e,'::before')[p]:null;};
  const seq=['.gb-product__rating','.gb-product__title','.gb-product__tag','.gb-product__lead','.gb-product__features'];
  const gaps=[]; let prev=null;
  for(const s of seq){const r=R(q(s)); if(r&&prev)gaps.push(r.t-prev.b); if(r)prev=r;}
  const cta=R(q('.gb-product__cta')), gn=R(q('.gb-product__guarantee-note'));
  const rows=c=>[...document.querySelectorAll('.gb-vs__col--'+c+' .gb-vs__row')].map(r=>Math.round(r.getBoundingClientRect().top+scrollY));
  const g=rows('gumi'), o=rows('others');
  const col=q('.gb-vs__col--gumi');
  return {
    headGaps: gaps, ctaToNote: (cta&&gn)?gn.t-cta.b:null,
    h1: document.querySelectorAll('h1').length,
    titleTag: q('.gb-product__title') ? q('.gb-product__title').tagName : null,
    whiteBefore: bef('.gb-promo-card--white .gb-promo-card__body','display'),
    whiteRight: bef('.gb-promo-card--white .gb-promo-card__body','right'),
    vsDrift: (g.length&&o.length)?Math.max(...g.map((v,i)=>Math.abs((o[i]===undefined?v:o[i])-v))):null,
    vsCardH: col?Math.round(parseFloat(getComputedStyle(col,'::before').height)):null,
    vsColH: col?Math.round(col.getBoundingClientRect().height):null,
    build: getComputedStyle(document.documentElement).getPropertyValue('--build').trim(),
  };
}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--password')
    ap.add_argument('--as-served', action='store_true')
    ap.add_argument('--skip-live', action='store_true')
    a = ap.parse_args()
    if a.skip_live:
        print()
        print(('%d FAIL' % len(fails)) if fails else 'all green')
        sys.exit(1 if fails else 0)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        br = pw.chromium.launch(executable_path=CHROME, args=['--no-sandbox'])
        for width in (1440, 1100, 390):
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
            pg = ctx.new_page()
            pg.goto(PDP, wait_until='networkidle')
            pg.wait_for_timeout(800)
            d = pg.evaluate(PROBE)
            ctx.close()
            tag = 'live %d' % width
            # 3: the head group runs at 16 everywhere it is laid out as a column
            check(tag + ' head gaps are 16', d['headGaps'], [16, 16, 16, 16])
            check(tag + ' cta->note is 24', d['ctaToNote'], 24)
            # 5: rows must line up one-to-one above the stack breakpoint
            if width >= 768:
                check(tag + ' vs rows aligned', d['vsDrift'], 0)
                check(tag + ' lime card fills the column', d['vsCardH'], d['vsColH'])
                check(tag + ' white scallop painted', d['whiteBefore'], 'block')
                check(tag + ' white scallop offset', d['whiteRight'], '-26px')
            else:
                check(tag + ' white scallop hidden', d['whiteBefore'], 'none')
            # 2 + 4: liquid -- red until pushed
            if a.as_served and width == 1440:
                check(tag + ' pdp has exactly one h1', d['h1'], 1)
                check(tag + ' product title is the h1', d['titleTag'], 'H1')
                check(tag + ' build', d['build'].strip('"') >= BUILD, True)
        br.close()
    print()
    print(('%d FAIL' % len(fails)) if fails else 'all green')
    sys.exit(1 if fails else 0)


main()
