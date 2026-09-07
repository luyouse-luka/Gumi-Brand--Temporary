#!/usr/bin/env python3
"""r87 judge -- six client-named CSS fixes plus the gb-logo liquid repair.

  python3 tools/r87check.py --password 1234              # live runs OUR css
  python3 tools/r87check.py --password 1234 --as-served  # live as it is now
  python3 tools/r87check.py --skip-live

--as-served must go RED before a push. CSS is swapped with page.route.
The logo assertions grade LIQUID, which routing cannot reach -- they stay red
until snippets/gb-logo.liquid is pushed.
"""
import argparse, io, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
SITE = 'https://gumi.com.au'
BUILD = '20260907-r87'
SAND = 'rgb(245, 241, 233)'
CLEAR = 'rgba(0, 0, 0, 0)'

fails, skips = [], []


def check(name, got, want):
    ok = got == want
    print(('  ok   ' if ok else '  FAIL ') + name + ('' if ok else '   got=%r want=%r' % (got, want)))
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
check('$build at or past r87', re.search(r'\$build:\s*"([^"]+)"', scss).group(1) >= BUILD, True)
check('2 panel bottom starts transparent',
      'border-bottom: 1px solid transparent;' in (block(css, '.gb-header__panel') or ''), True)
check('3 guarantees stack under 370',
      re.search(r'@media \(max-width: 369\.98px\) \{\s*\.gb-product__guarantees \{\s*'
                r'flex-direction: column;', css) is not None, True)
# ⚠ the phone figures must exist ONLY under .gb-science--tight now.
check('5 phone figures are scoped to tight',
      re.search(r'(?m)^\s*\.gb-science-card__value \{[^}]*font-size: 36px', css) is None, True)
check('5 tight still has them', css.count('.gb-science--tight .gb-science-card__value') == 2, True)
check('6 pane gutter', block(css, '.gb-nl-pane'), 'padding: 18px 24px 24px 24px;')

PROBE = """() => {
  const q = s => document.querySelector(s);
  const cs = s => { const e = q(s); return e ? getComputedStyle(e) : null; };
  const out = {};

  const t = q('.gb-reviews__title');
  out.reviewsTitle = t ? [getComputedStyle(t).maxWidth,
                          Math.round(t.getBoundingClientRect().width)] : null;

  const pn = q('.gb-header__panel');
  out.panelShut = pn ? [getComputedStyle(pn).borderTopWidth,
                        getComputedStyle(pn).borderTopColor,
                        getComputedStyle(pn).borderBottomColor] : null;

  const g = q('.gb-product__guarantees');
  if (g) {
    const kids = [...g.children].map(e => e.getBoundingClientRect());
    out.guarantees = {
      dir: getComputedStyle(g).flexDirection,
      n: kids.length,
      stacked: kids.length > 1 && kids.every((r, i) => i === 0 || r.top >= kids[i - 1].bottom - 1)
    };
  } else { out.guarantees = null; }

  const n = cs('.gb-stats__note');
  out.note = n && n.marginTop;

  // science.html carries both variants; index carries only the plain one.
  const plain = q('.gb-science:not(.gb-science--tight) .gb-science-card__value');
  const tight = q('.gb-science--tight .gb-science-card__value');
  const fs = e => e ? [getComputedStyle(e).fontSize, getComputedStyle(e).lineHeight] : null;
  out.valuePlain = fs(plain);
  out.valueTight = fs(tight);

  const p = cs('.gb-nl-pane');
  out.pane = p && [p.paddingTop, p.paddingRight, p.paddingBottom, p.paddingLeft];

  // Liquid half: settings.logo renders an <img> whose src must actually resolve.
  const mk = e => e ? {tag: e.tagName.toLowerCase(), src: e.getAttribute('src'),
                       nat: e.naturalWidth === undefined ? null : e.naturalWidth} : null;
  out.logo = {
    header: mk(q('.gb-header__logo svg, .gb-header__logo img')),
    footer: mk(q('.gb-footer__logo svg, .gb-footer__logo img'))
  };
  return out;
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
        pg.goto(url, wait_until='networkidle', timeout=45000)
        pg.wait_for_timeout(600)
        d = pg.evaluate(PROBE)
        # border-*-color rides the panel's 0.35s transition -- settle before reading.
        pg.evaluate("()=>{const h=document.querySelector('.gb-header');if(h)h.classList.add('is-open');}")
        pg.wait_for_timeout(500)
        d['panelOpen'] = pg.evaluate(
            "()=>{const p=document.querySelector('.gb-header__panel');if(!p)return null;"
            "const c=getComputedStyle(p);return [c.borderTopColor,c.borderBottomColor];}")
        pg.evaluate("()=>{const h=document.querySelector('.gb-header');if(h)h.classList.remove('is-open');}")
        res[name] = d
        pg.close()
    b.close()
    return res


def grade(tag, res, width, live):
    print('\n== %s ==' % tag)
    for page, d in res.items():
        p = lambda s: '%s %s' % (page, s)
        if d['reviewsTitle']:
            check(p('1 reviews title cap'), d['reviewsTitle'][0], '570px')
            check(p('1 reviews title within the cap'), d['reviewsTitle'][1] <= 570, True)
        if d['panelShut']:
            if width <= 767:
                check(p('2 phone drawer keeps both edges off'), d['panelShut'][0], '0px')
            else:
                check(p('2 panel top invisible while shut'), d['panelShut'][1], CLEAR)
                check(p('2 panel bottom invisible while shut'), d['panelShut'][2], CLEAR)
                check(p('2 both edges paint when open'), d['panelOpen'], [SAND, SAND])
        if d['guarantees']:
            if width < 370:
                check(p('3 guarantees stack'), d['guarantees']['dir'], 'column')
                check(p('3 guarantees really are one per row'), d['guarantees']['stacked'], True)
            else:
                check(p('3 guarantees stay in a row'), d['guarantees']['dir'], 'row')
        if d['note'] is not None:
            check(p('4 stats note margin-top'), d['note'], '0px' if width <= 991 else '-34px')
        if d['valuePlain']:
            check(p('5 plain science value keeps the desktop size'),
                  d['valuePlain'], ['56px', '44px'])
        if d['valueTight'] and width <= 767:
            check(p('5 tight science value takes the phone size'),
                  d['valueTight'], ['36px', '40px'])
        if d['pane']:
            check(p('6 pane gutter'), d['pane'],
                  ['20px', '20px', '20px', '20px'] if width <= 767
                  else ['18px', '24px', '24px', '24px'])
        if live:
            for k, m in d['logo'].items():
                if m and m['tag'] == 'img':
                    check(p('7 %s logo src resolves' % k),
                          m['src'] != '0' and (m['nat'] or 0) > 0, True)


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
            urls = [(n, (ROOT / (n + '.html')).as_uri()) for n in ('index', 'science', 'pdp')]
            for w in (1440, 900, 390, 360):
                grade('static @%d' % w, run(urls, None, None, w, pw), w, False)
        if a.skip_live or not a.password:
            skip('live half', 'no --password' if not a.password else '--skip-live')
        else:
            urls = [('index', SITE + '/'), ('science', SITE + '/pages/science'),
                    ('pdp', SITE + '/products/superfood-greens-gummies')]
            for w in (1440, 900, 390, 360):
                res = run(urls, None if a.as_served else ours, a.password, w, pw)
                grade('live @%d%s' % (w, '  (as served)' if a.as_served else '  (our css)'), res, w, True)

    print()
    if skips:
        print('%d SKIPPED: %s' % (len(skips), ', '.join(skips)))
    if fails:
        print('%d FAIL: %s' % (len(fails), ', '.join(sorted(set(fails))[:14])))
    else:
        print('all assertions ok')
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
