#!/usr/bin/env python3
"""r77 judge -- cart drawer restored to the static-site look + raised above the header.

  python3 tools/r77check.py                      # compiled css + static pages
  python3 tools/r77check.py --password 1234      # + live, serving the LOCAL css
  python3 tools/r77check.py --password 1234 --as-served   # + live, as it really is

The live half swaps customstyle.css by route interception rather than appending a
<style>: appended rules win every equal-specificity tie, which would grade the
sheet more favourably than the browser will.
"""
import argparse, re, sys

CSS = 'assets/customstyle.css'
SCSS = 'assets/customstyle.scss'
SITE = 'https://gumi.com.au'
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
# An old round's judge must NOT pin the current build token: it is bumped every
# round, so pinning turns this into a false red the moment r78 lands. What this
# judge owns is "the r77 rules are still there", not which build is current.
MIN_BUILD = '20260907-r77'

fails = []
skips = []
def skip(name, why):
    print('  SKIP ' + name + '   (' + why + ')')
    skips.append(name)

def check(name, got, want, op='=='):
    ok = (got == want) if op == '==' else (got > want if op == '>' else want in str(got))
    print(('  ok   ' if ok else '  FAIL ') + name + ('' if ok else '   got=%s want=%s' % (repr(got), repr(want))))
    if not ok: fails.append(name)

def block(css, sel):
    """Body of the first top-level rule whose selector is exactly `sel`."""
    for m in re.finditer(r'(?m)^([^@{}]+?)\{([^{}]*)\}', css):
        if ' '.join(m.group(1).split()) == sel:
            return ' '.join(m.group(2).split())
    return None


def css_checks():
    print('\n== compiled css ==')
    css = open(CSS, encoding='utf-8').read()
    scss = open(SCSS, encoding='utf-8').read()
    got = re.search(r'\$build:\s*"([^"]+)"', scss).group(1)
    check('$build at or past r77', got >= MIN_BUILD, True)

    d = block(css, '#cart-drawer .theme-drawer__dialog')
    check('dialog rule found (anchor)', d is not None, True)
    if d:
        check('  dialog z above $z-modal', 'z-index: calc(1000 + var(--drawer-stack-order, 0));' in d, True)
        check('  dialog box stripped', all(x in d for x in
              ['inset: 0;', 'width: auto;', 'height: auto;', 'padding: 0;', 'border: 0;']), True)
        check('  dialog ground transparent', 'background: transparent;' in d, True)
        check('  dialog colour inherited', 'color: inherit;' in d, True)

    # Duration deliberately not asserted here: r79 moved it off --animation-speed
    # onto $t-drawer. What r77 owns is "the phase classes drive our keyframes".
    for phase, extra in (('opening', ''), ('closing', ' reverse forwards')):
        for part, kf in (('overlay', 'gb-cart-scrim'), ('panel', 'gb-cart-slide')):
            b = block(css, '#cart-drawer .theme-drawer__dialog--%s .gb-cart__%s' % (phase, part))
            check('%s %s animated' % (phase, part),
                  b is not None and b.startswith('animation: %s ' % kf) and b.rstrip(';').endswith(extra.strip() or 'cubic-bezier(0.77, 0, 0.175, 1)'),
                  True)
    for kf in ('gb-cart-scrim', 'gb-cart-slide'):
        check('@keyframes %s' % kf, ('@keyframes %s' % kf) in css, True)

    s = block(css, '.gb-cart-item__stepper input.gb-cart-item__count')
    check('count input rule found (anchor)', s is not None, True)
    if s:
        check('  count back to the span box', all(x in s for x in
              ['width: 30px;', 'height: 20px;', 'padding: 0;', 'border: 0;']), True)
    check('spinner suppressed', '.gb-cart-item__stepper input.gb-cart-item__count::-webkit-inner-spin-button' in css, True)

    i = block(css, 'select.gb-cart-item__interval:not(.gb-select__native)')
    check('interval rule found (anchor)', i is not None, True)
    if i:
        check('  interval drawn on the native', 'appearance: none;' in i and 'border: 0;' in i, True)
        check('  interval chevron is the blue vee', '%230374a5' in i, True)

    bd = block(css, '#cart-drawer .theme-drawer__dialog::backdrop')
    check('native ::backdrop suppressed', bd, 'background: transparent;')

    # permanent, from r76: @extend rewrites class names INSIDE :has() too
    check('no nested :has()', re.search(r':has\([^)]*:has\(', css) is None, True)
    check('one $build in css', len(set(re.findall(r'\?v=([0-9a-zA-Z-]+)', css))) <= 1, True)


def static_checks():
    print('\n== static pages: every new rule must be a no-op ==')
    import glob
    htmls = {f: open(f, encoding='utf-8').read() for f in glob.glob('*.html')}
    check('no #cart-drawer in static html', sum('id="cart-drawer"' in h for h in htmls.values()), 0)
    check('no theme-drawer__dialog in static html', sum('theme-drawer__dialog' in h for h in htmls.values()), 0)
    check('static count is a <span>', sum(h.count('<span class="gb-cart-item__count">') for h in htmls.values()) > 0, True)
    check('static count is never an <input>', sum(h.count('input class="gb-cart-item__count"') for h in htmls.values()), 0)
    check('static panel always carries __body',
          all(h.count('gb-cart__body') == h.count('class="gb-cart__panel"') for h in htmls.values() if 'gb-cart__panel' in h), True)

    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME)
        pg = b.new_context(viewport={'width': 1440, 'height': 900}).new_page()
        pg.goto('file:///home/ly/project/Gumi-Brand/index.html', wait_until='networkidle')
        pg.evaluate("() => { const c=document.getElementById('gb-cart'); c.classList.add('is-open'); c.removeAttribute('aria-hidden'); }")
        pg.wait_for_timeout(800)
        r = pg.evaluate("""() => {
          const box=(s)=>{const e=document.querySelector(s); if(!e) return null;
            const b=e.getBoundingClientRect(); return [Math.round(b.width),Math.round(b.height)];};
          const iv=document.querySelector('.gb-cart-item__interval');
          return {panel:box('.gb-cart__panel'), stepper:box('.gb-cart-item__stepper'),
                  count:box('.gb-cart-item__count'),
                  intervalNative: iv ? iv.classList.contains('gb-select__native') : null,
                  emptyHidden: getComputedStyle(document.querySelector('.gb-cart__empty')).display,
                  drawn: !!document.querySelector('.gb-select--inline .gb-select__button')};
        }""")
        b.close()
    check('static panel 391 wide', r['panel'], [391, 900])
    check('static stepper still 102x40', r['stepper'], [102, 40])
    check('static count still 30x20', r['count'], [30, 20])
    check('static interval is selectBox-owned', r['intervalNative'], True)
    check('static inline widget still drawn', r['drawn'], True)
    check('static empty state still hidden', r['emptyHidden'], 'none')


def drawer_state(pg):
    return pg.evaluate("""() => ({ dlg: document.querySelector('#cart-drawer dialog').open,
      drawer: document.querySelector('#cart-drawer').hasAttribute('open') })""")


SKIP_WHY = 'needs a line item; --fill would trip the Cloudflare /cart challenge'

LIVE = """
() => {
  const dlg = document.querySelector('#cart-drawer dialog');
  const box = (s) => { const e=document.querySelector(s); if(!e) return null;
    const b=e.getBoundingClientRect(); return [Math.round(b.x),Math.round(b.y),Math.round(b.width),Math.round(b.height)]; };
  const cs = (s,p) => { const e=document.querySelector(s); return e ? getComputedStyle(e)[p] : null; };
  const hdr = document.querySelector('.gb-header');
  const hr = hdr && hdr.getBoundingClientRect();
  const over = hr && document.elementFromPoint(Math.round(hr.width*0.2), Math.round(hr.y + hr.height/2));
  return {
    modal: dlg ? dlg.matches(':modal') : null,
    dialogRect: box('#cart-drawer dialog'),
    dialogZ: cs('#cart-drawer dialog','zIndex'),
    dialogBg: cs('#cart-drawer dialog','backgroundColor'),
    dialogBorder: cs('#cart-drawer dialog','borderLeftWidth'),
    dialogColor: cs('#cart-drawer dialog','color'),
    viewport: [innerWidth, innerHeight],
    panel: box('.gb-cart__panel'),
    stepper: box('.gb-cart-item__stepper'),
    count: box('.gb-cart-item__count'),
    countBorder: cs('.gb-cart-item__count','borderTopWidth'),
    intervalAppearance: cs('.gb-cart-item__interval','appearance'),
    intervalColor: cs('.gb-cart-item__interval','color'),
    intervalBorder: cs('.gb-cart-item__interval','borderTopWidth'),
    overHeader: over ? (over.className||'').toString() : null,
    emptyDisplay: cs('.gb-cart__empty','display'),
    hasBody: !!document.querySelector('.gb-cart__body'),
    cartClass: (document.querySelector('.gb-cart') || {}).className || '',
    emptyCards: document.querySelectorAll('.gb-cart__cards .gb-nav-card').length,
    emptyArt: (() => { const c = document.querySelector('.gb-cart'); if (!c) return null;
      const a = c.querySelector('.gb-nav-card__art'); if (!a) return null;
      const b = a.getBoundingClientRect();
      return [Math.round(b.x), Math.round(b.y), Math.round(b.width), Math.round(b.height)]; })(),
  };
}
"""

def live_checks(password, as_served, want_fill=False):
    """One context, one page, three viewports.

    Every extra navigation is another roll of the Cloudflare dice: this
    storefront sits behind a managed challenge that answers the 2nd-3rd page
    load with "Just a moment...", and any /cart/* path with __cf_chl_rt_tk,
    after which the whole session is stuck. So: one password POST, one goto,
    and the breakpoints are crossed by resizing -- which also exercises
    Horizon's real #onModalBreakpointChange path.
    """
    from playwright.sync_api import sync_playwright
    body_css = None if as_served else open(CSS, encoding='utf-8').read()

    # Superfood Greens Gummies. Pinned rather than discovered: /products.json
    # rate-limits after a handful of runs and then answers HTML.
    VARIANT = 51114971562231

    with sync_playwright() as b_pw:
        b = b_pw.chromium.launch(executable_path=CHROME)
        ctx = b.new_context()
        r = ctx.request.post(SITE + '/password', form={
            'form_type': 'storefront_password', 'utf8': '✓', 'password': password})
        # 429/503 is the Cloudflare challenge, not a bad password. Calling it
        # "rejected" sends the reader off to hunt for a password; the cure is
        # to back off.
        if r.status in (429, 503):
            raise SystemExit('blocked by Cloudflare (HTTP %d) -- back off and rerun' % r.status)
        if not any(c['name'] == '_shopify_essential' for c in ctx.cookies()):
            raise SystemExit('storefront password rejected (HTTP %d)' % r.status)

        pg = ctx.new_page()
        pg.set_viewport_size({'width': 1440, 'height': 900})
        if body_css is not None:
            # Swap, do not append: appended rules win every equal-specificity
            # tie, which grades the sheet more favourably than the browser will.
            pg.route('**/customstyle.css*', lambda rt: rt.fulfill(
                status=200, content_type='text/css', body=body_css))
        pg.goto(SITE + '/', wait_until='networkidle')

        def opened():
            # A bare wait_for_selector timeout says nothing about WHY; the usual
            # cause is landing on the interstitial, so name that instead.
            if not pg.evaluate("!!document.querySelector('#cart-drawer')"):
                raise SystemExit('no #cart-drawer -- url=%s title=%r' % (pg.url, pg.title()))
            pg.evaluate("document.querySelector('#cart-drawer').open()")
            pg.wait_for_timeout(800)

        # ⚠ Opt-in only: /cart/<variant>:<qty> trips the Cloudflare challenge and
        # poisons the session. The line-item checks are announced as SKIPPED
        # instead of quietly dropped.
        filled = False
        if want_fill:
            pg.goto('%s/cart/%d:2' % (SITE, VARIANT), wait_until='domcontentloaded')
            pg.goto(SITE + '/', wait_until='networkidle')
            opened()
            filled = pg.evaluate("document.querySelectorAll('.gb-cart-item').length") > 0
            pg.evaluate("document.querySelector('#cart-drawer').close()")
            pg.wait_for_timeout(400)

        print('\n== live 1440 ==')
        opened()
        r = pg.evaluate(LIVE)
        check('desktop drawer is non-modal (Horizon)', r['modal'], False)
        check('dialog fills the viewport', r['dialogRect'], [0, 0] + r['viewport'])
        check('dialog above .gb-header (100)', int(r['dialogZ']) > 100, True)
        check('dialog ground transparent', r['dialogBg'], 'rgba(0, 0, 0, 0)')
        check('dialog left border gone', r['dialogBorder'], '0px')
        check('dialog colour is $c-ink', r['dialogColor'], 'rgb(1, 19, 7)')
        check('scrim covers the header', 'gb-cart__overlay' in (r['overHeader'] or ''), True)
        check('panel 391 wide, full height', r['panel'][2:], [391, 900])

        # A fresh session starts with an empty cart, which is the live-only
        # shape our state switch used to hide entirely.
        check('empty drawer omits __body (live shape)', r['hasBody'], False)
        # ⚠ This is the guard that used to live in the stylesheet. The vendor
        # marks the empty drawer with `is-empty`; drop that class and our own
        # `.gb-cart:not(.is-empty) .gb-cart__empty{display:none}` blanks the
        # panel. Keying a CSS rescue on a proxy (no __body) risked showing the
        # empty copy on a filled cart, so the check lives here instead.
        check('live empty drawer carries is-empty', 'is-empty' in r['cartClass'], True)
        check('empty message visible', r['emptyDisplay'], 'flex')
        check('empty state shows both nav cards', r['emptyCards'], 2)
        check('empty card art matches the static build', r['emptyArt'], [1106, 250, 229, 276])
        check('native ::backdrop transparent',
              pg.evaluate("() => getComputedStyle("
                          "document.querySelector('#cart-drawer dialog'), '::backdrop').backgroundColor"),
              'rgba(0, 0, 0, 0)')

        if filled:
            check('stepper 102x40 like the board', r['stepper'][2:], [102, 40])
            check('count 30x20 like the board', r['count'][2:], [30, 20])
            check('count has no input border', r['countBorder'], '0px')
            check('interval drawn on the native', r['intervalAppearance'], 'none')
            check('interval is $c-blue', r['intervalColor'], 'rgb(3, 116, 165)')
            check('interval has no select border', r['intervalBorder'], '0px')
        else:
            for n in ('stepper 102x40', 'count 30x20', 'count border',
                      'interval appearance', 'interval colour', 'interval border'):
                skip(n, SKIP_WHY)

        anim = pg.evaluate("""() => {
          const d = document.querySelector('#cart-drawer dialog');
          d.classList.add('theme-drawer__dialog--opening');
          const v = [getComputedStyle(document.querySelector('.gb-cart__panel')).animationName,
                     getComputedStyle(document.querySelector('.gb-cart__overlay')).animationName];
          d.classList.remove('theme-drawer__dialog--opening');
          return v; }""")
        check('opening phase drives panel + scrim', anim, ['gb-cart-slide', 'gb-cart-scrim'])

        # Horizon's own #onBackdropClick goes inert once the dialog fills the
        # viewport (nothing is "outside" any more), so this exercises the
        # vendor's on:click on .gb-cart__overlay instead.
        pg.mouse.click(120, 500)
        pg.wait_for_timeout(900)
        check('scrim click closes (desktop)', drawer_state(pg), {'dlg': False, 'drawer': False})

        opened()
        pg.evaluate("document.querySelector('#cart-drawer').close()")
        pg.wait_for_timeout(900)
        check('close() still completes', drawer_state(pg), {'dlg': False, 'drawer': False})

        print('\n== live 390 (same page, resized) ==')
        pg.set_viewport_size({'width': 390, 'height': 844})
        pg.wait_for_timeout(400)
        opened()
        r = pg.evaluate(LIVE)
        check('narrow drawer is modal (top layer)', r['modal'], True)
        check('narrow panel is full width', r['panel'][2], 390)
        if filled:
            check('narrow stepper 102x40', r['stepper'][2:], [102, 40])
        else:
            skip('narrow stepper 102x40', SKIP_WHY)
        # No scrim to click here: the panel is full-bleed, same as the boards.
        pg.click('.gb-cart__close')
        pg.wait_for_timeout(900)
        check('close button closes (narrow, modal)', drawer_state(pg), {'dlg': False, 'drawer': False})

        print('\n== live 900 (modal, scrim exposed) ==')
        pg.set_viewport_size({'width': 900, 'height': 800})
        pg.wait_for_timeout(400)
        opened()
        g = pg.evaluate("() => { const b = document.querySelector('.gb-cart__panel').getBoundingClientRect();"
                        " return [Math.round(b.x), Math.round(b.width)]; }")
        check('scrim exposed at 900', g[0] > 0, True)
        check('modal at 900', pg.evaluate("document.querySelector('#cart-drawer dialog').matches(':modal')"), True)
        pg.mouse.click(60, 400)
        pg.wait_for_timeout(900)
        check('scrim click closes (modal)', drawer_state(pg), {'dlg': False, 'drawer': False})
        b.close()


a = argparse.ArgumentParser()
a.add_argument('--password')
a.add_argument('--as-served', action='store_true')
a.add_argument('--fill', action='store_true',
               help='add a line item via /cart/<variant>:<qty> -- ⚠ trips Cloudflare')
args = a.parse_args()
css_checks()
static_checks()
if args.password:
    live_checks(args.password, args.as_served, args.fill)
if fails:
    print('\n%d FAIL: %s' % (len(fails), ', '.join(fails)))
if skips:
    print('\n%d SKIPPED (NOT verified): %s' % (len(skips), ', '.join(skips)))
print('\nall assertions ok' if not fails else '')
sys.exit(1 if fails else 0)
