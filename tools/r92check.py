#!/usr/bin/env python3
"""r92 judge -- gb-vs brand-row artwork stays out of the rows; 404 on theme type.

  python3 tools/r92check.py --password 1234                  # live runs OUR css
  python3 tools/r92check.py --password 1234 --as-served      # live as it is now
  python3 tools/r92check.py --password 1234 --inject-hook    # pre-push: fake .gb-404
  python3 tools/r92check.py --skip-live

The 404 half grades a hook class that lives in sections/main-404.liquid, which
page.route cannot reach -- it stays red until that liquid is pushed. --inject-hook
adds the class from JS so the CSS half can be proved before the push.
"""
import argparse, io, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
SITE = 'https://gumi.com.au'
BUILD = '20260907-r92'
BRAND = '"PP Palma"'
GREEN = 'rgb(0, 86, 53)'
INK = 'rgb(1, 19, 7)'
GRAY7 = 'rgb(77, 77, 77)'

fails, skips = [], []


def check(name, got, want, tol=None):
    ok = abs(got - want) <= tol if tol is not None and isinstance(got, (int, float)) else got == want
    print(('  ok   ' if ok else '  FAIL ') + name + ('' if ok else '   got=%r want=%r' % (got, want)))
    if not ok:
        fails.append(name)


def skip(name, why):
    print('  SKIP ' + name + '   -- ' + why)
    skips.append(name)


VS_PROBE = r"""() => {
  const R=e=>{const r=e.getBoundingClientRect();return{x:+r.x.toFixed(1),y:+r.y.toFixed(1),r:+r.right.toFixed(1),b:+r.bottom.toFixed(1),w:+r.width.toFixed(1),h:+r.height.toFixed(1)};};
  if(!document.querySelector('.gb-vs__table')) return null;
  const o={docW:document.documentElement.scrollWidth, vw:window.innerWidth};
  o.brandG=R(document.querySelector('.gb-vs__col--gumi .gb-vs__brand'));
  o.brandO=R(document.querySelector('.gb-vs__col--others .gb-vs__brand'));
  for(const k of ['logo','bear','pile']){const e=document.querySelector('.gb-vs__'+k); o[k]=e?R(e):null;}
  const texts=[...document.querySelectorAll('.gb-vs__label,.gb-vs__value,.gb-vs__mark')].map(R);
  const overlaps=a=>texts.filter(t=>!(a.r<=t.x||a.x>=t.r||a.b<=t.y||a.y>=t.b)).length;
  o.hit={logo:overlaps(o.logo), bear:overlaps(o.bear), pile:o.pile?overlaps(o.pile):0};
  o.spill={logo:+(o.logo.b-o.brandG.b).toFixed(1), bear:+(o.bear.b-o.brandG.b).toFixed(1),
           pile:o.pile?+(o.pile.b-o.brandO.b).toFixed(1):null};
  // the bear's right edge sits ~3px past the lime card's, at every width
  const cs=getComputedStyle(document.querySelector('.gb-vs__col--gumi'),'::before');
  const gr=R(document.querySelector('.gb-vs__col--gumi'));
  o.cardR=+(gr.x+parseFloat(cs.left)+parseFloat(cs.width)).toFixed(1);
  // ⚠ the bear's rect is the ROTATED bbox, which reaches ~0.079*w further right
  // than the box CSS positions. Work back to the untransformed right edge.
  const be=document.querySelector('.gb-vs__bear');
  o.bearRight=+(o.brandG.x+o.brandG.w-parseFloat(getComputedStyle(be).right)).toFixed(1);
  return o;
}"""

P404_PROBE = r"""() => {
  const g=s=>{const e=document.querySelector(s); if(!e)return null; const c=getComputedStyle(e);
    return {ff:c.fontFamily.split(',')[0], fs:c.fontSize, fw:c.fontWeight, lh:c.lineHeight,
            ls:c.letterSpacing, col:c.color, bg:c.backgroundColor, br:c.borderRadius, h:c.height,
            pad:c.padding, tt:c.textTransform};};
  const o={};
  o.h1=g('.gb-404 .text-block h1');
  o.p=g('.gb-404 .text-block p');
  o.btn=g('.gb-404 .button');
  o.head=g('.ui-test-product-list .section-resource-list__header .text-block p');
  o.card=g('.ui-test-product-list .resource-list__item .product-title');
  const pl=document.querySelector('[data-testid="product-list"]');
  o.plPad=pl?getComputedStyle(pl).paddingBlockEnd:null;
  const names=[...document.querySelectorAll('.ui-test-product-list .resource-list__item *')]
    .filter(e=>e.children.length===0 && e.textContent.trim());
  const bear=document.querySelector('.gb-deco-bear--a');
  const last=names.length?Math.max(...names.map(e=>e.getBoundingClientRect().bottom)):null;
  o.bearGap=(last!==null&&bear)?+(bear.getBoundingClientRect().top-last).toFixed(1):null;
  o.docW=document.documentElement.scrollWidth; o.vw=window.innerWidth;
  return o;
}"""

INJECT = "()=>document.querySelectorAll('.shopify-section.section-wrapper').forEach(e=>e.classList.add('gb-404'))"


def run(urls, css_text, password, width, pw, probe, inject=False):
    b = pw.chromium.launch(executable_path=CHROME)
    ctx = b.new_context(viewport={'width': width, 'height': 1200})
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
        pg.goto(url, wait_until='load' if url.startswith('file') else 'networkidle', timeout=60000)
        if inject:
            pg.evaluate(INJECT)
        pg.wait_for_timeout(500)
        res[name] = pg.evaluate(probe)
        pg.close()
    b.close()
    return res


def grade_vs(tag, res, width):
    print('\n== %s ==' % tag)
    for page, d in res.items():
        if not d:
            continue
        p = lambda s: '%s %s' % (page, s)
        check(p('0 no horizontal overflow'), d['docW'], d['vw'])
        # THE round's point: nothing in the brand row may reach the table rows
        for k in ('logo', 'bear', 'pile'):
            check(p('1 %s hits no row text' % k), d['hit'][k], 0)
            if d['spill'][k] is not None:
                check(p('1 %s stays inside its brand row' % k), d['spill'][k] < 0, True)
        # one scale for the whole brand row, every width
        check(p('2 bear : pile'), d['bear']['w'] / d['pile']['w'], 1.795, tol=0.02)
        check(p('2 logo : bear'), d['logo']['w'] / d['bear']['w'], 0.849, tol=0.015)
        # bear's right edge rides the lime card's, not the column's
        check(p('3 bear right edge vs card'), d['bearRight'] - d['cardR'], 3.0, tol=1.5)


def grade_404(tag, res, width):
    print('\n== %s ==' % tag)
    d = res['404']
    p = lambda s: '404 %s' % s
    check(p('0 no horizontal overflow'), d['docW'], d['vw'])
    if d['h1']:
        check(p('4 heading is the brand face'), d['h1']['ff'], BRAND)
        check(p('4 heading size'), d['h1']['fs'], '30px' if width <= 767 else '56px')
        check(p('4 heading weight'), d['h1']['fw'], '800')
        check(p('4 heading colour'), d['h1']['col'], GREEN)
    else:
        check(p('4 heading found'), False, True)
    if d['p']:
        check(p('5 copy colour'), d['p']['col'], GRAY7)
    if d['btn']:
        check(p('6 button face'), d['btn']['ff'], BRAND)
        check(p('6 button height'), d['btn']['h'], '52px')
        check(p('6 button radius'), d['btn']['br'], '999px')
        check(p('6 button fill'), d['btn']['bg'], GREEN)
        check(p('6 button case'), d['btn']['tt'], 'capitalize')
    else:
        check(p('6 button found'), False, True)
    if d['head']:
        check(p('7 list heading face'), d['head']['ff'], BRAND)
        check(p('7 list heading size'), d['head']['fs'], '24px' if width <= 767 else '32px')
        check(p('7 list heading colour'), d['head']['col'], INK)
    # ⚠ the product CARDS must NOT pick up the heading's type
    if d['card']:
        check(p('8 product card keeps its own size'), d['card']['fs'], '16px')
        check(p('8 product card keeps its own weight'), d['card']['fw'], '400')
    check(p('9 product list bottom padding'), d['plPad'], '64px' if width <= 767 else '120px')
    # the whole reason for that padding: the CTA's deco bear must clear the names
    check(p('9 deco bear clears the product names'), d['bearGap'] is not None and d['bearGap'] > 0, True)


def main():
    from playwright.sync_api import sync_playwright
    ap = argparse.ArgumentParser()
    ap.add_argument('--password')
    ap.add_argument('--as-served', action='store_true')
    ap.add_argument('--inject-hook', action='store_true')
    ap.add_argument('--skip-live', action='store_true')
    ap.add_argument('--skip-static', action='store_true')
    a = ap.parse_args()

    print('== source ==')
    scss = io.open(ROOT / 'assets/customstyle.scss', encoding='utf-8').read()
    css = io.open(ROOT / 'assets/customstyle.css', encoding='utf-8').read()
    flat = css.replace(' ', '')
    check('$build at or past r92', re.search(r'\$build:\s*"([^"]+)"', scss).group(1) >= BUILD, True)
    check('brand artwork is capped', flat.count('max-width:174.168px') >= 1
          and flat.count('max-width:105.993px') >= 1 and flat.count('max-width:68.5px') >= 1, True)
    check('bear is anchored right', 'right:calc(-5.426%-3px)' in flat, True)
    check('404 hook is styled', '.gb-404' in css, True)
    check('product list bottom is overridden', 'data-testid=' in css.replace('"', ''), True)

    with sync_playwright() as pw:
        if not a.skip_static:
            urls = [('pdp', (ROOT / 'pdp.html').as_uri())]
            for w in (1440, 1280, 1100, 1025, 1024, 992, 900, 800, 768, 767, 575, 480, 390, 360):
                grade_vs('static @%d' % w, run(urls, None, None, w, pw, VS_PROBE), w)
        if a.skip_live or not a.password:
            skip('live half', 'no --password' if not a.password else '--skip-live')
        else:
            ours = None if a.as_served else css
            for w in (1440, 1024, 768, 390):
                grade_vs('live vs @%d%s' % (w, '  (as served)' if a.as_served else ''),
                         run([('pdp', SITE + '/products/superfood-greens-gummies')],
                             ours, a.password, w, pw, VS_PROBE), w)
            for w in (1440, 390):
                grade_404('live 404 @%d%s%s' % (w, '  (as served)' if a.as_served else '',
                                                '  (hook injected)' if a.inject_hook else ''),
                          run([('404', SITE + '/404')], ours, a.password, w, pw, P404_PROBE,
                              inject=a.inject_hook), w)

    print()
    if skips:
        print('%d SKIPPED: %s' % (len(skips), ', '.join(skips)))
    if fails:
        print('%d FAIL: %s' % (len(fails), ', '.join(sorted(set(fails))[:16])))
    else:
        print('all assertions ok')
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
