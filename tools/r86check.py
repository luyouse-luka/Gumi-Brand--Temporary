#!/usr/bin/env python3
"""r86 judge -- the five client-named fixes.

  python3 tools/r86check.py --password 1234              # live runs OUR css
  python3 tools/r86check.py --password 1234 --as-served  # live as it is now
  python3 tools/r86check.py --skip-live

--as-served must go RED before a push. CSS is swapped with page.route, never
add_style_tag.

⚠ `(hover: hover)` is false in a bare headless chromium; the hover half of item
4 is skipped rather than silently passing if the context does not report it.

⚠ Item 5 was REVERSED in r96 -- the shut panel now carries a zero-width border
rather than a transparent 1px one. Three assertions here were rewritten to the
new mechanism; a RED on them means r96 came undone, not that r86 regressed.
"""
import argparse, io, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
SITE = 'https://gumi.com.au'
BUILD = '20260907-r86'
SAND = 'rgb(245, 241, 233)'

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
check('$build at or past r86', re.search(r'\$build:\s*"([^"]+)"', scss).group(1) >= BUILD, True)
check('1 features order', block(css, '.gb-product__info > .gb-product__features, .gb-product__info > .shopify-block:has(> .gb-product__features)'), 'order: -1;')
check('1 head order', block(css, '.gb-product__info > .gb-product__head'), 'order: -2;')
# ⚠ the whole point of item 2: body must NOT be a scroll container while locked.
check('2 body lock is clip, not hidden',
      re.search(r'body\.is-menu-open \{\s*overflow-x: clip;\s*overflow-y: visible;', css) is not None, True)
check('2 no body overflow:hidden left in the menu lock',
      re.search(r'body\.is-menu-open \{\s*overflow: hidden', css) is None, True)
check('2b modal lock body is clip',
      block(css, 'body.is-modal-open'), 'overflow-x: clip; overflow-y: visible;')
check('2b modal lock html still hidden',
      block(css, 'html.is-modal-open'), 'overflow: hidden;')
# ⚠ the compensation stays on html ALONE -- padding both spends the scrollbar
# width twice and pulls a centred layout left by half of it.
check('2b modal padding stays on html only',
      block(css, 'body.is-modal-open') and 'padding-right' not in block(css, 'body.is-modal-open'), True)
check('2c cart drawer body is clip',
      block(css, 'html:has(#cart-drawer .theme-drawer__dialog[open]) body'),
      'overflow-x: clip; overflow-y: visible;')
check('4 underline mixin gone', '@mixin link-underline' in scss, False)
check('4 no sliding underline compiled', 'transform-origin: right center' in css, False)
# r96 reversal: the edge is zero-WIDTH while shut, not a transparent 1px. A
# transparent border still boxed the 0fr row 2px tall and painted $c-cream there.
check('5 panel top has no border while shut (r96 reversal)',
      'border-top: 0 solid #f5f1e9;' in css, True)

PROBE = """() => {
  const q = s => document.querySelector(s);
  const out = {};
  const head = q('.gb-product__head'), feat = q('.gb-product__features');
  if (head && feat) {
    const h = head.getBoundingClientRect(), f = feat.getBoundingClientRect();
    // whatever follows the pair -- the form on live, the picker on the static site
    const after = q('.gb-product__form') || q('.gb-sub');
    // The order lives on whatever is the direct child of .gb-product__info --
    // on live that is the div.shopify-block wrapper, not the <ul> itself.
    const info = q('.gb-product__info');
    let item = feat;
    while (item.parentElement && item.parentElement !== info) { item = item.parentElement; }
    out.order = {
      css: getComputedStyle(item).order,
      featCss: getComputedStyle(feat).order,
      headCss: getComputedStyle(head).order,
      inHead: head.contains(feat),
      belowHead: Math.round(f.top - h.top),
      headBottom: Math.round(h.bottom), featTop: Math.round(f.top),
      featBottom: Math.round(f.bottom),
      afterTop: after ? Math.round(after.getBoundingClientRect().top) : null
    };
  } else { out.order = null; }

  const it = q('.gb-logo-scroll__item'), im = q('.gb-logo-scroll__img');
  const box = e => { const r = e.getBoundingClientRect(); return [Math.round(r.width), Math.round(r.height)]; };
  out.marquee = it ? { item: box(it), img: im ? box(im) : null } : null;

  const pn = q('.gb-header__panel');
  out.panelShut = pn ? [getComputedStyle(pn).borderTopWidth, getComputedStyle(pn).borderTopColor] : null;

  out.pseudo = {};
  for (const s of ['.gb-header__link', '.gb-header__sublink', '.gb-footer__link',
                   '.gb-footer__legal-links a']) {
    const e = q(s);
    out.pseudo[s] = e ? getComputedStyle(e, '::after').content : null;
  }
  out.hoverMedia = matchMedia('(hover: hover)').matches;
  return out;
}"""

# Item 2 needs the page scrolled and the drawer actually open, so it runs on its
# own rather than inside PROBE.
LOCK_OPEN = """() => {
  window.scrollTo(0, 900);
  window.gumi.header.set(true);
}"""
LOCK_READ = """() => {
  const h = document.getElementById('site-header');
  return {top: Math.round(h.getBoundingClientRect().top),
          scrollY: Math.round(window.scrollY),
          html: getComputedStyle(document.documentElement).overflow,
          body: getComputedStyle(document.body).overflow};
}"""


def run(urls, css_text, password, width, pw):
    b = pw.chromium.launch(executable_path=CHROME)
    ctx = b.new_context(viewport={'width': width, 'height': 780})
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
        # border-top-color rides the panel's own 0.35s transition -- read it in
        # the same frame the class lands and the probe grades the START value.
        pg.evaluate("()=>{const h=document.querySelector('.gb-header');if(h)h.classList.add('is-open');}")
        pg.wait_for_timeout(500)
        d['panelOpen'] = pg.evaluate(
            "()=>{const p=document.querySelector('.gb-header__panel');if(!p)return null;"
            "const c=getComputedStyle(p);return [c.borderTopWidth,c.borderTopColor];}")
        pg.evaluate("()=>{const h=document.querySelector('.gb-header');if(h)h.classList.remove('is-open');}")
        pg.wait_for_timeout(450)

        if name == 'index' and width <= 767:
            pg.wait_for_timeout(200)
            before = pg.evaluate(LOCK_READ)
            pg.evaluate(LOCK_OPEN)
            pg.wait_for_timeout(500)
            locked = pg.evaluate(LOCK_READ)
            # The lock must still hold: a wheel gesture may not move the page.
            # ⚠ headless wheel is not a real touch gesture -- this catches a
            # regression in the lock, it does not prove phone behaviour.
            pg.mouse.wheel(0, 600)
            pg.wait_for_timeout(400)
            after = pg.evaluate(LOCK_READ)
            d['lock'] = {'before': before, 'locked': locked, 'wheeled': after}

        # The modal lock is not scoped to a tier, so it is graded at both widths.
        if name == 'index':
            # Start from a clean state and take the path modal.open() takes:
            # ⚠ it pauses Lenis. Without that the wheel drives Lenis's own
            # scrollTo, which moves an overflow:hidden html -- measured identical
            # on the r85 baseline, so it is not this round's doing and not
            # reachable in production, but it makes the assertion below a lie.
            pg.evaluate("()=>{if(window.gumi&&window.gumi.header)window.gumi.header.set(false);}")
            pg.wait_for_timeout(900)
            pg.evaluate("()=>window.scrollTo(0,900)")
            pg.wait_for_timeout(300)
            pg.evaluate("()=>{window.gumi.smoothScroll.pause();"
                        "document.documentElement.classList.add('is-modal-open');"
                        "document.body.classList.add('is-modal-open');}")
            pg.wait_for_timeout(300)
            ml = pg.evaluate(LOCK_READ)
            pg.mouse.wheel(0, 600)
            pg.wait_for_timeout(400)
            ml2 = pg.evaluate(LOCK_READ)
            pg.evaluate("()=>{document.documentElement.classList.remove('is-modal-open');"
                        "document.body.classList.remove('is-modal-open');"
                        "window.gumi.smoothScroll.resume();}")
            d['modalLock'] = {'locked': ml, 'wheeled': ml2}

            # Horizon's cart drawer, live only. The `open` attribute is all the
            # selector needs -- set it directly rather than opening the real
            # drawer, which would hit /cart/* and trip Cloudflare for the session.
            d['cartLock'] = pg.evaluate('''() => {
              const dlg = document.querySelector('#cart-drawer .theme-drawer__dialog');
              if (!dlg) { return null; }
              const had = dlg.hasAttribute('open');
              dlg.setAttribute('open', '');
              const h = document.getElementById('site-header');
              const out = {top: Math.round(h.getBoundingClientRect().top),
                           body: getComputedStyle(document.body).overflow,
                           html: getComputedStyle(document.documentElement).overflow};
              if (!had) { dlg.removeAttribute('open'); }
              return out;
            }''')

        # Item 4 says hover becomes a COLOUR change; assert the colour still moves
        # now that the underline is gone. CDP rather than a real pointer, and a
        # settle wait because these carry trans(color).
        if d['hoverMedia']:
            cdp = ctx.new_cdp_session(pg)
            cdp.send('DOM.enable'); cdp.send('CSS.enable')
            root = cdp.send('DOM.getDocument')['root']['nodeId']
            d['hover'] = {}
            for sel in ('.gb-header__link', '.gb-header__sublink', '.gb-footer__link',
                        '.gb-footer__legal-links a'):
                nid = cdp.send('DOM.querySelector', {'nodeId': root, 'selector': sel})['nodeId']
                if not nid:
                    continue
                rest = pg.eval_on_selector(sel, 'e => getComputedStyle(e).color')
                cdp.send('CSS.forcePseudoState', {'nodeId': nid, 'forcedPseudoClasses': ['hover']})
                pg.wait_for_timeout(350)
                hov = pg.eval_on_selector(sel, 'e => getComputedStyle(e).color')
                cdp.send('CSS.forcePseudoState', {'nodeId': nid, 'forcedPseudoClasses': []})
                pg.wait_for_timeout(250)
                d['hover'][sel] = [rest, hov]
        res[name] = d
        pg.close()
    b.close()
    return res


def grade(tag, res, width):
    print('\n== %s ==' % tag)
    for page, d in res.items():
        p = lambda s: '%s %s' % (page, s)
        o = d['order']
        if o:
            if o['inHead']:
                # static site: the <ul> is a child of the head, so the order rules
                # cannot reach it and nothing may move.
                check(p('1 static keeps features inside the head'), o['featCss'], '0')
                check(p('1 features sit inside the head box'),
                      o['headBottom'] >= o['featBottom'], True)
            else:
                check(p('1 features take order -1'), o['css'], '-1')
                check(p('1 head takes order -2'), o['headCss'], '-2')
                check(p('1 features follow the head'), o['featTop'] >= o['headBottom'], True)
                if o['afterTop'] is not None:
                    check(p('1 features precede the form'), o['featBottom'] <= o['afterTop'], True)
        if d['marquee']:
            check(p('3 marquee slot'), d['marquee']['item'],
                  [88, 36] if width <= 767 else [193, 80])
            if d['marquee']['img'] and width <= 767:
                check(p('3 marquee logo fits the slot'),
                      d['marquee']['img'][0] <= 88 and d['marquee']['img'][1] <= 36, True)
        if d['panelShut']:
            if width <= 767:
                check(p('5 phone drawer keeps both edges off'), d['panelShut'][0], '0px')
                check(p('5 phone drawer stays off when open'), d['panelOpen'][0], '0px')
            else:
                # r96 reversal, see the source assertion above: colour is now
                # always sand and the WIDTH is what the open state switches.
                check(p('5 panel top zero width while shut (r96 reversal)'), d['panelShut'][0], '0px')
                check(p('5 panel top colour always sand (r96 reversal)'), d['panelShut'][1], SAND)
                check(p('5 panel top paints when open'), d['panelOpen'][1], SAND)
        for sel, content in d['pseudo'].items():
            if content is not None:
                check(p('4 %s has no underline pseudo' % sel), content, 'none')
        for sel, pair in (d.get('hover') or {}).items():
            check(p('4 %s hover changes colour' % sel), pair[0] != pair[1], True)
        if not d['hoverMedia']:
            skip(p('4 hover colour'), '(hover: hover) is false in this context')
        if d.get('modalLock'):
            M = d['modalLock']
            check(p('2b header holds its place under the modal lock'), M['locked']['top'], 0)
            check(p('2b modal lock leaves body scroll-free'), M['locked']['body'], 'clip visible')
            check(p('2b the modal lock still blocks the wheel'),
                  M['wheeled']['scrollY'], M['locked']['scrollY'])
        if d.get('cartLock'):
            C = d['cartLock']
            check(p('2c header holds its place under the cart drawer'), C['top'], 0)
            check(p('2c cart lock leaves body scroll-free'), C['body'], 'clip visible')
            check(p('2c cart lock holds html'), C['html'], 'hidden')
        if 'lock' in d:
            L = d['lock']
            check(p('2 header holds its place while the menu is open'), L['locked']['top'], 0)
            check(p('2 body is not a scroll container while locked'),
                  L['locked']['body'], 'clip visible')
            check(p('2 html is locked'), L['locked']['html'], 'hidden')
            check(p('2 the lock still blocks the wheel'),
                  L['wheeled']['scrollY'], L['locked']['scrollY'])


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
            urls = [(n, (ROOT / (n + '.html')).as_uri()) for n in ('index', 'pdp')]
            for w in (1440, 390):
                grade('static @%d' % w, run(urls, None, None, w, pw), w)
        if a.skip_live or not a.password:
            skip('live half', 'no --password' if not a.password else '--skip-live')
        else:
            urls = [('index', SITE + '/'), ('pdp', SITE + '/products/superfood-greens-gummies')]
            for w in (1440, 390):
                res = run(urls, None if a.as_served else ours, a.password, w, pw)
                grade('live @%d%s' % (w, '  (as served)' if a.as_served else '  (our css)'), res, w)

    print()
    if skips:
        print('%d SKIPPED: %s' % (len(skips), ', '.join(skips)))
    if fails:
        print('%d FAIL: %s' % (len(fails), ', '.join(fails[:14])))
    else:
        print('all assertions ok')
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
