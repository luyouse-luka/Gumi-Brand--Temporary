#!/usr/bin/env python3
"""r85 judge -- the nine client-named fixes.

  python3 tools/r85check.py --password 1234              # live runs OUR css+js
  python3 tools/r85check.py --password 1234 --as-served  # live as it is now
  python3 tools/r85check.py --skip-live

--as-served must go RED before a push; if it passes, the probe is not reaching
what it claims to grade. Assets are swapped with page.route, never
add_style_tag -- an appended sheet wins every equal-specificity tie.

⚠ One assertion cannot be graded by routing: item 7's src="0" lives in
snippets/gb-logo.liquid, which only exists on live. It is printed under
"pending liquid" and stays red until that snippet is pushed.
"""
import argparse, io, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
SITE = 'https://gumi.com.au'
BUILD = '20260907-r85'
GREEN = 'rgb(0, 86, 53)'
SAND = 'rgb(245, 241, 233)'

fails, skips, pending = [], [], []


def check(name, got, want):
    ok = got == want
    print(('  ok   ' if ok else '  FAIL ') + name + ('' if ok else '   got=%r want=%r' % (got, want)))
    if not ok:
        fails.append(name)


def near(name, got, want, tol):
    ok = got is not None and abs(got - want) <= tol
    print(('  ok   ' if ok else '  FAIL ') + name + ('' if ok else '   got=%r want=%r+-%s' % (got, want, tol)))
    if not ok:
        fails.append(name)


def note(name, got, want):
    ok = got == want
    print(('  ok   ' if ok else '  PEND ') + name + ('' if ok else '   got=%r want=%r' % (got, want)))
    if not ok:
        pending.append(name)


def skip(name, why):
    print('  SKIP ' + name + '   -- ' + why)
    skips.append(name)


def block(css, sel):
    for m in re.finditer(r'(?m)^([^@{}]+?)\{([^{}]*)\}', css):
        if ' '.join(m.group(1).split()) == sel:
            return ' '.join(m.group(2).split())
    return None


# --------------------------------------------------------------- offline half
print('== compiled css / js ==')
css = io.open(ROOT / 'assets/customstyle.css', encoding='utf-8').read()
scss = io.open(ROOT / 'assets/customstyle.scss', encoding='utf-8').read()
js = io.open(ROOT / 'assets/main.js', encoding='utf-8').read()

check('$build at or past r85', re.search(r'\$build:\s*"([^"]+)"', scss).group(1) >= BUILD, True)
check('1 thumb focus', block(css, '.gb-product__thumb:focus-visible'),
      'outline: none; border-color: #005635;')
check('2 guarantee icon takes img', block(css, '.gb-product__guarantee svg, .gb-product__guarantee img'),
      'width: 34px; height: 32px; object-fit: contain; color: #faf9f8;')
check('3 plan ring is an overlay', block(css, '.gb-sub__plan::after'),
      'content: ""; position: absolute; inset: 0; border: 1px solid #005635; border-radius: inherit; pointer-events: none;')
check('3 inset shadow gone', 'box-shadow: inset 0 0 0 1px' in css, False)
check('4 divider opacity', 'opacity: 0.2;' in (block(css, '.gb-footer__divider') or ''), True)
check('7 header logo takes img', block(css, '.gb-header__logo svg, .gb-header__logo img'),
      'width: 124px; height: 32px; object-fit: contain;')
check('7 footer logo takes img', block(css, '.gb-footer__logo svg, .gb-footer__logo img'),
      'width: 193px; height: 50px; object-fit: contain;')
check('9 static rail centres', block(css, '[data-slider].is-static > [data-slider-track] > .swiper-wrapper'),
      'justify-content: center; column-gap: inherit;')
# ⚠ the loop gate is what keeps the expert rail out of this; it has no computed
# trace, so the source is the only place it can be asserted.
check('9 fit check is gated on loop', re.search(r'var fits = function \(\) \{\s*if \(!loop\) \{ return false; \}', js) is not None, True)
check('9 resize listener ignores height-only', 'if (window.innerWidth === lastW) { return; }' in js, True)

# --------------------------------------------------------------------- probes
PROBE = """() => {
  const q = s => document.querySelector(s);
  const cs = s => { const e = q(s); return e ? getComputedStyle(e) : null; };
  const box = e => { const r = e.getBoundingClientRect(); return [Math.round(r.width), Math.round(r.height)]; };
  const out = {};

  const g = q('.gb-product__guarantee svg, .gb-product__guarantee img');
  out.guarantee = g ? [g.tagName.toLowerCase()].concat(box(g)) : null;

  const sp = q('.gb-sub__plan--sub');
  if (sp) {
    const a = getComputedStyle(sp, '::after');
    const r = sp.getBoundingClientRect();
    out.plan = [getComputedStyle(sp).boxShadow, a.borderTopWidth, a.borderTopColor,
                Math.round(r.x + scrollX), Math.round(r.y + scrollY + r.height / 2)];
  } else { out.plan = null; }

  const dv = cs('.gb-footer__divider'); out.divider = dv && dv.opacity;
  const pn = cs('.gb-header__panel');
  out.panel = pn && [pn.borderTopWidth, pn.borderTopColor];
  const pi = cs('.gb-header__panel-inner'); out.panelInner = pi && pi.alignItems;

  const mk = e => e ? { tag: e.tagName.toLowerCase(), box: box(e),
                        src: e.getAttribute('src'),
                        nat: e.naturalWidth === undefined ? null : e.naturalWidth } : null;
  out.logoHeader = mk(q('.gb-header__logo svg, .gb-header__logo img'));
  out.logoPanel  = mk(q('.gb-header__panel-logo svg, .gb-header__panel-logo img'));
  out.logoFooter = mk(q('.gb-footer__logo svg, .gb-footer__logo img'));

  // The artwork is display:none until the drawer opens -- open it, measure, shut it.
  const hdr = q('.gb-header'), art = q('.gb-nav-card__art');
  if (hdr && art) {
    const had = hdr.classList.contains('is-open');
    hdr.classList.add('is-open');
    const card = art.closest('.gb-nav-card') || art.parentElement;
    out.art = [Math.round(art.getBoundingClientRect().width),
               Math.round(card.getBoundingClientRect().width)];
    if (!had) { hdr.classList.remove('is-open'); }
  } else { out.art = null; }
  return out;
}"""

# Programmatic .focus() does not arm :focus-visible reliably, so the state is
# forced through CDP instead of tabbing 40 stops down the page.
FOCUS_READ = """() => {
  const t = document.querySelector('.gb-product__thumb:not(.is-active)');
  if (!t) { return null; }
  const c = getComputedStyle(t);
  return [c.outlineStyle, c.borderTopColor];
}"""

REELS = """(keep) => {
  const root = document.querySelector('.gb-reviews__reels');
  if (!root) { return null; }
  const track = root.querySelector('[data-slider-track]');
  const sl = [...track.querySelectorAll('.swiper-slide')];
  for (let i = keep; i < sl.length; i++) { sl[i].remove(); }
  return sl.length;
}"""

REELS_READ = """() => {
  const root = document.querySelector('.gb-reviews__reels');
  const track = root.querySelector('[data-slider-track]');
  const w = track.querySelector('.swiper-wrapper');
  const sl = [...track.querySelectorAll('.swiper-slide')];
  const tr = track.getBoundingClientRect();
  const nav = root.querySelector('.gb-reels__nav');
  return {
    n: sl.length,
    isStatic: root.classList.contains('is-static'),
    swiper: !!track.swiper,
    justify: getComputedStyle(w).justifyContent,
    gap: getComputedStyle(w).columnGap,
    navDisplay: nav ? getComputedStyle(nav).display : null,
    leftPad: Math.round(sl[0].getBoundingClientRect().left - tr.left),
    rightPad: Math.round(tr.right - sl[sl.length - 1].getBoundingClientRect().right)
  };
}"""

EXPERT = """(keep) => {
  const root = document.querySelector('.gb-expert__inner');
  if (!root) { return null; }
  const track = root.querySelector('[data-slider-track]');
  const sl = [...track.querySelectorAll('.swiper-slide')];
  for (let i = keep; i < sl.length; i++) { sl[i].remove(); }
  return true;
}"""


def run(urls, css_text, js_text, password, width, pw):
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
    if js_text is not None:
        ctx.route(re.compile(r'/main\.js'), lambda route: route.fulfill(
            status=200, content_type='text/javascript', body=js_text))

    res = {}
    for name, url in urls:
        pg = ctx.new_page()
        pg.goto(url, wait_until='networkidle', timeout=45000)
        pg.wait_for_timeout(600)
        d = pg.evaluate(PROBE)

        if name == 'pdp':
            cdp = ctx.new_cdp_session(pg)
            cdp.send('DOM.enable'); cdp.send('CSS.enable')
            root = cdp.send('DOM.getDocument')['root']['nodeId']
            nid = cdp.send('DOM.querySelector', {
                'nodeId': root, 'selector': '.gb-product__thumb:not(.is-active)'})['nodeId']
            if nid:
                cdp.send('CSS.forcePseudoState', {'nodeId': nid, 'forcedPseudoClasses': ['focus-visible']})
                # border-color is on a 0.2s transition: read it too early and the
                # probe grades the START value and calls a working rule broken.
                pg.wait_for_timeout(400)
                d['thumbFocus'] = pg.evaluate(FOCUS_READ)
                cdp.send('CSS.forcePseudoState', {'nodeId': nid, 'forcedPseudoClasses': []})
            else:
                d['thumbFocus'] = None
            if d['plan']:
                x, y = d['plan'][3], d['plan'][4]
                from PIL import Image
                im = Image.open(io.BytesIO(pg.screenshot(
                    full_page=True, clip={'x': x, 'y': y, 'width': 3, 'height': 1})))
                d['planPixel'] = im.convert('RGB').getpixel((0, 0))

        if name == 'index':
            # No card count fits 390 -- the phone card is 228 of a 390 track --
            # so the width decides how far the set has to be trimmed to reach the
            # state under test.
            keep = 1 if width <= 767 else 4
            n = pg.evaluate(REELS, keep)
            if n is not None:
                d['reelsBefore'] = n
                # apply() only re-runs on a WIDTH change, which is the point of the
                # guard -- so the probe has to move the viewport, not fake a resize.
                pg.set_viewport_size({'width': width + 1, 'height': 1000})
                pg.wait_for_timeout(400)
                d['reels'] = pg.evaluate(REELS_READ)
                pg.set_viewport_size({'width': width, 'height': 1000})

        if name == 'reviews':
            if pg.evaluate(EXPERT, 1):
                pg.set_viewport_size({'width': width + 1, 'height': 1000})
                pg.wait_for_timeout(400)
                d['expertStatic'] = pg.evaluate(
                    "() => document.querySelector('.gb-expert__inner').classList.contains('is-static')")
                pg.set_viewport_size({'width': width, 'height': 1000})

        res[name] = d
        pg.close()
    b.close()
    return res


def grade(tag, res, width, live):
    print('\n== %s ==' % tag)
    for page, d in res.items():
        p = lambda s: '%s %s' % (page, s)
        if d.get('thumbFocus'):
            check(p('1 thumb focus draws no outline'), d['thumbFocus'][0], 'none')
            check(p('1 thumb focus takes the active border'), d['thumbFocus'][1], GREEN)
        if d['guarantee']:
            check(p('2 guarantee icon 34x32'), d['guarantee'][1:], [34, 32])
        if d['plan']:
            check(p('3 plan carries no inset shadow'), d['plan'][0], 'none')
            check(p('3 plan ring 1px'), d['plan'][1], '1px')
            check(p('3 plan ring green'), d['plan'][2], GREEN)
        if d.get('planPixel'):
            r, g, b = d['planPixel']
            near(p('3 plan left edge paints green (R)'), r, 0, 24)
            near(p('3 plan left edge paints green (G)'), g, 86, 24)
            near(p('3 plan left edge paints green (B)'), b, 53, 24)
        if d['divider'] is not None:
            check(p('4 divider opacity'), d['divider'], '0.2')
        if d['panel']:
            check(p('5 panel border-top'), d['panel'][0], '0px' if width <= 767 else '1px')
            # ⚠ r86 moved the COLOUR onto .gb-header.is-open (shut, the panel is a
            # 0fr row and the line read as a second hairline under the bar), so
            # only the reserved width belongs to this judge now. The colour is
            # r86check's -- see its "5 panel top paints when open".
            if width > 767:
                check(p('5 panel border-top transparent while shut'), d['panel'][1], 'rgba(0, 0, 0, 0)')
        if d['panelInner']:
            check(p('6 panel-inner align'), d['panelInner'],
                  'stretch' if width <= 767 else 'flex-start')
        if d['logoHeader']:
            check(p('7 header logo box'), d['logoHeader']['box'],
                  [93, 24] if width <= 767 else [124, 32])
        if d['logoFooter']:
            check(p('7 footer logo box'), d['logoFooter']['box'],
                  [167, 43] if width <= 767 else [193, 50])
        if width <= 767 and d['logoPanel']:
            check(p('7 drawer logo box'), d['logoPanel']['box'], [93, 24])
        if live:
            for k in ('logoHeader', 'logoPanel', 'logoFooter'):
                m = d[k]
                if m and m['tag'] == 'img':
                    note(p('7 %s src resolves (liquid)' % k), m['src'] != '0' and (m['nat'] or 0) > 0, True)
        if d['art']:
            check(p('8 nav card art width'), d['art'][0],
                  d['art'][1] if width <= 767 else round(d['art'][1] * 1.352))
        if 'reels' in d:
            r = d['reels']
            check(p('9 four reels go static'), [r['isStatic'], r['swiper']], [True, False])
            check(p('9 static rail centres'), r['justify'], 'center')
            check(p('9 static rail keeps its gap'), r['gap'], '24px' if width > 767 else '16px')
            check(p('9 static rail drops the nav'), r['navDisplay'], 'none')
            near(p('9 static rail is symmetric'), r['leftPad'] - r['rightPad'], 0, 2)
            check(p('9 rail was NOT static at full count'), d['reelsBefore'] > r['n'], True)
        if 'expertStatic' in d:
            check(p('9 rewind rail never goes static'), d['expertStatic'], False)


def main():
    from playwright.sync_api import sync_playwright
    ap = argparse.ArgumentParser()
    ap.add_argument('--password')
    ap.add_argument('--as-served', action='store_true')
    ap.add_argument('--skip-live', action='store_true')
    ap.add_argument('--skip-static', action='store_true')
    a = ap.parse_args()
    ours_css = io.open(ROOT / 'assets/customstyle.css', encoding='utf-8').read()
    ours_js = io.open(ROOT / 'assets/main.js', encoding='utf-8').read()

    with sync_playwright() as pw:
        if not a.skip_static:
            urls = [(n, (ROOT / (n + '.html')).as_uri()) for n in ('index', 'pdp', 'reviews')]
            for w in (1440, 390):
                grade('static @%d' % w, run(urls, None, None, None, w, pw), w, False)

        if a.skip_live or not a.password:
            skip('live half', 'no --password' if not a.password else '--skip-live')
        else:
            urls = [('index', SITE + '/'), ('pdp', SITE + '/products/superfood-greens-gummies'),
                    ('reviews', SITE + '/pages/reviews')]
            for w in (1440, 390):
                res = run(urls, None if a.as_served else ours_css,
                          None if a.as_served else ours_js, a.password, w, pw)
                grade('live @%d%s' % (w, '  (as served)' if a.as_served else '  (our css+js)'), res, w, True)

    print()
    if skips:
        print('%d SKIPPED: %s' % (len(skips), ', '.join(skips)))
    if pending:
        print('%d PENDING LIQUID (snippets/gb-logo.liquid not pushed): %d assertions' % (len(pending), len(pending)))
    if fails:
        print('%d FAIL: %s' % (len(fails), ', '.join(fails[:14])))
    else:
        print('all assertions ok')
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
