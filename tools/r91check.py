#!/usr/bin/env python3
"""r91 judge -- gb-promo restored to the static build, gb-vs table alignment.

  python3 tools/r91check.py --password 1234              # live runs OUR css
  python3 tools/r91check.py --password 1234 --as-served  # live as it is now
  python3 tools/r91check.py --skip-live

--as-served must go RED before a push. CSS is swapped with page.route, so the
white card's MOBILE ARC stays red either way: that half lives in
sections/gb-promo.liquid, which routing cannot reach.
"""
import argparse, io, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
SITE = 'https://gumi.com.au'
BUILD = '20260907-r91'

fails, skips = [], []


def check(name, got, want, tol=None):
    ok = abs(got - want) <= tol if tol is not None and isinstance(got, (int, float)) else got == want
    print(('  ok   ' if ok else '  FAIL ') + name + ('' if ok else '   got=%r want=%r' % (got, want)))
    if not ok:
        fails.append(name)


def skip(name, why):
    print('  SKIP ' + name + '   -- ' + why)
    skips.append(name)


PROBE = r"""() => {
  const R = e => { const r = e.getBoundingClientRect(); return {x:+r.x.toFixed(2), w:+r.width.toFixed(2), h:+r.height.toFixed(2)}; };
  const o = {docW: document.documentElement.scrollWidth, vw: window.innerWidth};

  // ---- gb-vs ------------------------------------------------------------
  const gumi = document.querySelector('.gb-vs__col--gumi');
  if (gumi) {
    const oth = document.querySelector('.gb-vs__col--others');
    const cb = getComputedStyle(gumi, '::before');
    const gr = R(gumi);
    o.vs = {
      colW: gr.w,
      cardX: +(gr.x + parseFloat(cb.left)).toFixed(2),
      cardR: +(gr.x + parseFloat(cb.left) + parseFloat(cb.width)).toFixed(2),
      colR:  +(gr.x + gr.w).toFixed(2),
      labels: {},
      logoX: null
    };
    for (const [k, col] of [['gumi', gumi], ['others', oth]]) {
      const ls = [...col.querySelectorAll('.gb-vs__label')].filter(e => getComputedStyle(e).display !== 'none');
      o.vs.labels[k] = {n: ls.length,
                        w: [...new Set(ls.map(e => +R(e).w.toFixed(1)))],
                        maxRight: ls.length ? Math.max(...ls.map(e => R(e).x + R(e).w)) : null};
      const vs = [...col.querySelectorAll('.gb-vs__value')];
      o.vs.labels[k].valueX = [...new Set(vs.map(e => +R(e).x.toFixed(1)))];
    }
    for (const k of ['logo', 'bear', 'pile']) {
      const e = document.querySelector('.gb-vs__' + k);
      o.vs[k] = e ? R(e) : null;
    }
  }

  // ---- gb-promo ---------------------------------------------------------
  const green = document.querySelector('.gb-promo-card--green');
  const white = document.querySelector('.gb-promo-card--white');
  if (green) {
    const pe = (e, p) => { const c = getComputedStyle(e, p);
      return {content: c.content, bg: c.backgroundColor, w: c.width, h: c.height,
              bottom: c.bottom, left: c.left, mask: (c.maskImage || c.webkitMaskImage || '').slice(0, 46)}; };
    const media = green.querySelector('.gb-promo-card__media');
    const img = green.querySelector('.gb-promo-card__media img');
    const arc = green.querySelector('.gb-promo-card__arc');
    const main = green.querySelector('.gb-promo-card__main');
    const stack = green.querySelector('.gb-promo-card__stack');
    o.promo = {
      imgFit: img ? getComputedStyle(img).objectFit : null,
      greenArc: arc ? getComputedStyle(arc).display : 'absent',
      greenMainGap: main ? getComputedStyle(main).rowGap : null,
      greenStackGap: stack ? getComputedStyle(stack).rowGap : null,
      halves: [...green.children].map(e => +R(e).w.toFixed(1)),
      lipGreen: media ? pe(media, '::after') : null,
      lipWhite: white ? pe(white.querySelector('.gb-promo-card__art'), '::after') : null,
      arcMob: white ? !!white.querySelector('.gb-arc-text--mob') : null
    };
    // the static build ships the svg; where it does, the pseudo must land on it
    const svg = green.querySelector('.gb-promo-card__lip--h');
    o.promo.lipSvg = svg ? R(svg) : null;
  }
  return o;
}"""


def run(urls, css_text, password, width, pw):
    b = pw.chromium.launch(executable_path=CHROME)
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
    res = {}
    for name, url in urls:
        pg = ctx.new_page()
        pg.goto(url, wait_until='load' if url.startswith('file') else 'networkidle', timeout=60000)
        pg.wait_for_timeout(500)
        res[name] = pg.evaluate(PROBE)
        pg.close()
    b.close()
    return res


# board ratios: bear's rendered (rotated) bbox against the pile, and the logo
# against that bbox. Desktop 201.5/112 and 173/201.5; phone 122.7/68.5, 103/122.7.
RATIO = {'wide': (1.799, 0.8586), 'narrow': (1.791, 0.8395)}


def grade(tag, res, width, live):
    print('\n== %s ==' % tag)
    for page, d in res.items():
        p = lambda s: '%s %s' % (page, s)
        check(p('0 no horizontal overflow'), d['docW'], d['vw'])

        v = d.get('vs')
        if v:
            for k, lab in v['labels'].items():
                if not lab['n']:
                    continue
                # one width for every row, so every value starts at the same x
                check(p('1 %s label column is one width' % k), len(lab['w']), 1)
                check(p('1 %s values share an x' % k), len(lab['valueX']), 1)
            # the lime card must clear the label column it now hangs off
            mr = v['labels']['gumi']['maxRight']
            check(p('2 lime card clears the labels'), mr <= v['cardX'] + 0.5, True)
            # right edge is the board's, wherever the left edge lands
            check(p('2 lime card right edge'), v['cardR'] - v['colR'], v['colW'] * 0.05426 if width > 767 else 0.0, tol=1.0)
            # the logo rides inside the card
            check(p('3 logo starts inside the card'), v['logo']['x'] >= v['cardX'] - 0.5, True)
            # one scale for the whole brand row
            r1, r2 = RATIO['narrow' if width <= 767 else 'wide']
            check(p('4 bear : pile'), v['bear']['w'] / v['pile']['w'], r1, tol=0.02)
            check(p('4 logo : bear'), v['logo']['w'] / v['bear']['w'], r2, tol=0.02)

        m = d.get('promo')
        if m:
            if m['imgFit'] is not None:
                check(p('5 promo media image is contained'), m['imgFit'], 'contain')
            check(p('6 green card draws no arc'), m['greenArc'] in ('none', 'absent'), True)
            check(p('6 green card halves are even'), abs(m['halves'][0] - m['halves'][1]) <= 1
                  if width > 767 else True, True)
            # static ships title/lead straight into the stack -- __main is the theme's
            if m['greenMainGap'] is not None:
                check(p('7 green __main takes the stack rhythm'), m['greenMainGap'], m['greenStackGap'])
            for k, want_bg in [('lipGreen', 'rgb(0, 86, 53)'), ('lipWhite', 'rgb(255, 255, 255)')]:
                lip = m[k]
                if width <= 767:
                    check(p('8 %s painted' % k), lip['content'], '""')
                    check(p('8 %s colour' % k), lip['bg'], want_bg)
                    check(p('8 %s masked' % k), lip['mask'].startswith('url("data:image/svg+xml'), True)
                    check(p('8 %s bottom' % k), lip['bottom'], '-48px')
                else:
                    check(p('8 %s absent above 767' % k), lip['content'], 'none')
            if width <= 767 and m['lipSvg']:
                # static only: the rebuild has to land exactly on the shipped svg
                check(p('8 pseudo matches the shipped svg'),
                      round(float(m['lipGreen']['w'][:-2]), 1), round(m['lipSvg']['w'], 1), tol=0.5)
            if m['arcMob'] is not None:
                check(p('9 white card ships a mobile arc'), m['arcMob'], True)


def main():
    from playwright.sync_api import sync_playwright
    ap = argparse.ArgumentParser()
    ap.add_argument('--password')
    ap.add_argument('--as-served', action='store_true')
    ap.add_argument('--skip-live', action='store_true')
    ap.add_argument('--skip-static', action='store_true')
    a = ap.parse_args()

    print('== source ==')
    scss = io.open(ROOT / 'assets/customstyle.scss', encoding='utf-8').read()
    css = io.open(ROOT / 'assets/customstyle.css', encoding='utf-8').read()
    check('$build at or past r91', re.search(r'\$build:\s*"([^"]+)"', scss).group(1) >= BUILD, True)
    check('label floor reaches the css', '--vs-label-w:max(' in css.replace(' ', ''), True)
    check('card left is derived', '--vs-card-x:calc(var(--vs-label-w)' in css.replace(' ', ''), True)
    check('pile keeps a column-relative width', css.count('.gb-vs__pile') >= 1
          and 'left:80.627%' not in css.replace(' ', ''), True)

    with sync_playwright() as pw:
        if not a.skip_static:
            urls = [('pdp', (ROOT / 'pdp.html').as_uri())]
            for w in (1440, 1280, 1100, 1025, 1024, 900, 768, 767, 575, 390, 360):
                grade('static @%d' % w, run(urls, None, None, w, pw), w, False)
        if a.skip_live or not a.password:
            skip('live half', 'no --password' if not a.password else '--skip-live')
        else:
            urls = [('pdp', SITE + '/products/superfood-greens-gummies')]
            ours = css
            for w in (1440, 1100, 1024, 768, 390):
                res = run(urls, None if a.as_served else ours, a.password, w, pw)
                grade('live @%d%s' % (w, '  (as served)' if a.as_served else '  (our css)'), res, w, True)

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
