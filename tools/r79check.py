#!/usr/bin/env python3
"""r79 judge -- BH (exit runs the board's 0.7s) + BI (desktop locks the page).

  python3 tools/r79check.py                      # compiled css + js + static pages
  python3 tools/r79check.py --password 1234      # + live, serving the LOCAL css
  python3 tools/r79check.py --password 1234 --as-served   # + live, as it really is

BH: Horizon times display:none off the dialog's OWN animation, so the panel's
exit was cut at --animation-speed (0.125s). The duration is overridden on the
dialog element -- not on the variable, which the whole subtree inherits.

BI: >=990 Horizon opens the cart with dialog.show(), which does not lock. The
lock is keyed on dialog[open] because theme-drawer[open] and html[scroll-lock]
are both dropped BEFORE the exit animation, which would return the scrollbar
mid-slide and step the right-pinned panel sideways.
"""
import argparse, re, sys

CSS = 'assets/customstyle.css'
SCSS = 'assets/customstyle.scss'
JS = 'assets/main.js'
SITE = 'https://gumi.com.au'
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
MIN_BUILD = '20260907-r79'
LOCK_SEL = 'html:has(#cart-drawer .theme-drawer__dialog[open])'

fails = []
skips = []
def skip(name, why):
    print('  SKIP ' + name + '   (' + why + ')')
    skips.append(name)

def check(name, got, want, op='=='):
    ok = (got == want) if op == '==' else (want in str(got))
    print(('  ok   ' if ok else '  FAIL ') + name + ('' if ok else '   got=%s want=%s' % (repr(got), repr(want))))
    if not ok: fails.append(name)

def block(css, sel):
    """Body of the first top-level rule whose selector list is exactly `sel`."""
    for m in re.finditer(r'(?m)^([^@{}]+?)\{([^{}]*)\}', css):
        if ' '.join(m.group(1).split()) == sel:
            return ' '.join(m.group(2).split())
    return None


def css_checks():
    print('\n== compiled css ==')
    css = open(CSS, encoding='utf-8').read()
    scss = open(SCSS, encoding='utf-8').read()
    check('$build at or past r79', re.search(r'\$build:\s*"([^"]+)"', scss).group(1) >= MIN_BUILD, True)

    # -- BH ------------------------------------------------------------------
    d = block(css, '#cart-drawer .theme-drawer__dialog--opening, #cart-drawer .theme-drawer__dialog--closing')
    check('dialog duration rule found (anchor)', d is not None, True)
    check('  dialog animation runs $t-drawer', d, 'animation-duration: 0.7s;')

    # Anchor first: a "no longer references X" assertion over a selector that
    # does not exist would pass on a typo. r77check owns the keyframe contract.
    seen = 0
    for phase, extra in (('opening', ''), ('closing', ' reverse forwards')):
        for part, kf in (('overlay', 'gb-cart-scrim'), ('panel', 'gb-cart-slide')):
            b = block(css, '#cart-drawer .theme-drawer__dialog--%s .gb-cart__%s' % (phase, part))
            check('%s %s rule found (anchor)' % (phase, part), b is not None, True)
            if b is None: continue
            seen += 1
            check('  %s %s runs 0.7s' % (phase, part),
                  b.startswith('animation: %s 0.7s cubic-bezier(0.77, 0, 0.175, 1)' % kf), True)
            check('  %s %s off --animation-speed' % (phase, part), '--animation-speed' not in b, True)
    check('all four phase rules present', seen, 4)
    check('no --animation-speed left in the cart block',
          css.count('--animation-speed') == 0, True)

    # -- BI ------------------------------------------------------------------
    lock = block(css, LOCK_SEL + ', ' + LOCK_SEL + ' body')
    check('lock rule found (anchor)', lock is not None, True)
    check('  lock hides overflow', lock, 'overflow: hidden;')
    pad = block(css, LOCK_SEL)
    check('pad rule found (anchor)', pad is not None, True)
    check('  freed width padded back', pad, 'padding-right: var(--scrollbar-w, 0px);')
    # Padded once: html is the scroller and its padding already narrows body, so
    # padding body too spends the width twice and pulls the layout left by half.
    check('  padding not also on body', 'body' not in (LOCK_SEL if pad is None else pad), True)

    # :has() cannot nest -- a nested one silently drops the whole rule.
    for m in re.finditer(r':has\(([^()]*(\([^()]*\))?[^()]*)\)', css):
        if ':has(' in m.group(1): fails.append('nested :has()')
    check('no nested :has()', 'nested :has()' not in fails, True)


def js_checks():
    print('\n== main.js ==')
    js = open(JS, encoding='utf-8').read()
    check('scrollbarProbe module defined', 'var scrollbarProbe = {' in js, True)
    # Runs first: the locks that read --scrollbar-w can land any time after init.
    check('  registered first in the init list',
          re.search(r'var modules = \[\["([a-zA-Z]+)"', js).group(1), 'scrollbarProbe')
    check('  exported on window.gumi', 'scrollbarProbe: scrollbarProbe }' in js, True)
    m = re.search(r'var scrollbarProbe = \{.*?\n  \};', js, re.S)
    body = m.group(0) if m else ''
    # Both guards matter: Horizon locks via html[scroll-lock], our own modal and
    # menu locks via computed overflow. Reading through either returns 0.
    check('  skips while Horizon holds the lock', "hasAttribute(\"scroll-lock\")" in body, True)
    check('  skips while our own lock holds', 'overflowY === "hidden"' in body, True)
    check('  writes --scrollbar-w', '--scrollbar-w' in body, True)
    check('  measures innerWidth - clientWidth',
          'window.innerWidth - de.clientWidth' in body, True)


def static_checks():
    """Every r79 rule must be a no-op on the static pages."""
    from playwright.sync_api import sync_playwright
    import pathlib
    print('\n== static pages: r79 rules must be no-ops ==')
    pages = ['index.html', 'pdp.html']
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME)
        pg = b.new_page(viewport={'width': 1440, 'height': 900})
        for f in pages:
            pg.goto(pathlib.Path(f).resolve().as_uri())
            pg.wait_for_timeout(400)
            # Anchor the negative: the drawer must actually BE here, or
            # "no #cart-drawer" would pass on a page that failed to load.
            check('%s has the static drawer (anchor)' % f,
                  pg.evaluate("!!document.querySelector('#gb-cart .gb-cart__panel')"), True)
            check('  no #cart-drawer, lock cannot match',
                  pg.evaluate("document.querySelectorAll('#cart-drawer').length"), 0)
            check('  --scrollbar-w written by scrollbarProbe',
                  pg.evaluate("getComputedStyle(document.documentElement)"
                              ".getPropertyValue('--scrollbar-w').trim() !== ''"), True)
        # Static exit is unchanged: modal.open/close still drive it at 0.7s.
        pg.goto(pathlib.Path('index.html').resolve().as_uri())
        pg.wait_for_timeout(400)
        pg.evaluate("window.gumi.modal.open(document.getElementById('gb-cart'))")
        pg.wait_for_timeout(900)
        check('static panel opens to transform none',
              pg.evaluate("getComputedStyle(document.querySelector('#gb-cart .gb-cart__panel')).transform"),
              'none')
        check('static panel transition still 0.7s',
              pg.evaluate("getComputedStyle(document.querySelector('#gb-cart .gb-cart__panel')).transitionDuration"),
              '0.7s')
        b.close()


LIVE_OPEN = """() => {
  const de = document.documentElement;
  const dlg = document.querySelector('#cart-drawer dialog');
  return {
    overflow: getComputedStyle(de).overflow,
    padRight: getComputedStyle(de).paddingRight,
    scrollbarW: getComputedStyle(de).getPropertyValue('--scrollbar-w').trim(),
    dlgOpen: dlg.hasAttribute('open'),
    anchorX: document.querySelector('.gb-header').getBoundingClientRect().width,
  };
}"""

# Samples the close: when does dialog[open] go, and does the lock outlive it?
LIVE_CLOSE = """() => new Promise(res => {
  const de = document.documentElement;
  const drawer = document.querySelector('#cart-drawer');
  const dlg = drawer.querySelector('dialog');
  const t0 = performance.now();
  let openGone = null, lockGone = null;
  drawer.close();
  const tick = () => {
    const t = performance.now() - t0;
    if (openGone === null && !dlg.hasAttribute('open')) openGone = t;
    if (lockGone === null && getComputedStyle(de).overflow !== 'hidden') lockGone = t;
    if ((openGone !== null && lockGone !== null) || t > 2500) return res({openGone, lockGone});
    requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
})"""


PHASE_DUR = """() => new Promise(res => {
  const drawer = document.querySelector('#cart-drawer');
  drawer.open();
  requestAnimationFrame(() => requestAnimationFrame(() => {
    const dlg = drawer.querySelector('dialog');
    res({
      phase: dlg.classList.contains('theme-drawer__dialog--opening'),
      dialog: getComputedStyle(dlg).animationDuration,
      panel: getComputedStyle(drawer.querySelector('.gb-cart__panel')).animationDuration,
    });
  }));
})"""


def live_checks(password, as_served):
    """One context, one page. Never touches /cart/* -- see r77check's note."""
    from playwright.sync_api import sync_playwright
    body_css = None if as_served else open(CSS, encoding='utf-8').read()
    body_js = None if as_served else open(JS, encoding='utf-8').read()
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME)
        ctx = b.new_context()
        r = ctx.request.post(SITE + '/password', form={
            'form_type': 'storefront_password', 'utf8': '✓', 'password': password})
        if r.status in (429, 503):
            raise SystemExit('blocked by Cloudflare (HTTP %d) -- back off and rerun' % r.status)
        if not any(c['name'] == '_shopify_essential' for c in ctx.cookies()):
            raise SystemExit('storefront password rejected (HTTP %d)' % r.status)

        pg = ctx.new_page()
        pg.set_viewport_size({'width': 1440, 'height': 900})
        if body_css is not None:
            pg.route('**/customstyle.css*', lambda rt: rt.fulfill(
                status=200, content_type='text/css', body=body_css))
            # main.js carries scrollbarProbe; without it --scrollbar-w is absent
            # and the padding check would compare 0px against 0px.
            pg.route('**/main.js*', lambda rt: rt.fulfill(
                status=200, content_type='text/javascript', body=body_js))
        pg.goto(SITE + '/', wait_until='networkidle')
        if not pg.evaluate("!!document.querySelector('#cart-drawer')"):
            raise SystemExit('no #cart-drawer -- url=%s title=%r' % (pg.url, pg.title()))

        print('\n== live 1440 (BI: desktop lock) ==')
        before = pg.evaluate(LIVE_OPEN)
        check('page scrolls before opening (anchor)', before['overflow'] != 'hidden', True)
        # Proves our main.js is the one running -- the live file has no probe,
        # and without it both sides of the padding check read 0px and agree
        # while compensating nothing.
        check('scrollbarProbe is live (anchor)',
              pg.evaluate("!!(window.gumi && window.gumi.scrollbarProbe)"), True)
        check('probe wrote --scrollbar-w', before['scrollbarW'] != '', True)
        bar = int(re.sub(r'[^0-9]', '', before['scrollbarW']) or 0)

        pg.evaluate("document.querySelector('#cart-drawer').open()")
        pg.wait_for_timeout(1000)
        after = pg.evaluate(LIVE_OPEN)
        check('drawer is open (anchor)', after['dlgOpen'], True)
        check('desktop page is locked', after['overflow'], 'hidden')
        check('freed width padded back', after['padRight'], '%dpx' % bar)
        check('layout does not shift sideways', after['anchorX'], before['anchorX'])

        # ⚠ Headless chromium has no on-screen scrollbar, so the real width is
        # always 0 here and the two assertions above compensate nothing. Force a
        # value to prove the CSS actually responds; the true width needs a real
        # browser. See memory headless-chromium-probe-limits / rule 14.
        if bar == 0:
            skip('real scrollbar width compensated', 'headless has no scrollbar -- verify on a real browser')
            synth = pg.evaluate("""() => {
              const de = document.documentElement;
              de.style.setProperty('--scrollbar-w', '15px');
              const got = getComputedStyle(de).paddingRight;
              de.style.setProperty('--scrollbar-w', '0px');
              return got;
            }""")
            check('  lock consumes --scrollbar-w (synthetic 15px)', synth, '15px')
        else:
            check('real scrollbar width compensated', after['padRight'], '%dpx' % bar)

        print('\n== live 1440 (BH: exit runs 0.7s) ==')
        # Sampled during the phase, not after: Horizon removes --opening on
        # animationend, and a computed read off an element with no animation
        # is '0s' -- a green-looking measurement of nothing.
        pg.evaluate("document.querySelector('#cart-drawer').close()")
        pg.wait_for_timeout(900)
        dur = pg.evaluate(PHASE_DUR)
        check('dialog animation duration mid-phase', dur['dialog'], '0.7s')
        check('panel animation duration mid-phase', dur['panel'], '0.7s')
        check('  sampled while --opening was on (anchor)', dur['phase'], True)

        pg.evaluate("document.querySelector('#cart-drawer').open()")
        pg.wait_for_timeout(900)
        t = pg.evaluate(LIVE_CLOSE)
        og, lg = t['openGone'], t['lockGone']
        check('exit ran the full 0.7s (not cut at 0.125)', og is not None and 600 < og < 1100, True)
        # The lock must not be handed back mid-slide: the viewport would widen
        # under .gb-cart and step the right-pinned panel sideways.
        check('lock held until the panel was gone',
              lg is not None and og is not None and lg >= og - 50, True)
        print('       openGone=%.0fms lockGone=%.0fms' % (og or -1, lg or -1))

        pg.wait_for_timeout(300)
        back = pg.evaluate(LIVE_OPEN)
        check('page scrolls again after close', back['overflow'] != 'hidden', True)
        check('padding released', back['padRight'], '0px')
        b.close()


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--password')
    ap.add_argument('--as-served', action='store_true')
    ap.add_argument('--skip-static', action='store_true')
    a = ap.parse_args()
    css_checks()
    js_checks()
    if not a.skip_static: static_checks()
    if a.password: live_checks(a.password, a.as_served)
    if skips: print('\n%d SKIPPED: %s' % (len(skips), ', '.join(skips)))
    print('\n' + ('%d FAIL: ' % len(fails) + ', '.join(fails) if fails else 'all assertions ok'))
    sys.exit(1 if fails else 0)
