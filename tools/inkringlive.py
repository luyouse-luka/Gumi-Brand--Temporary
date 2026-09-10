#!/usr/bin/env python3
"""Live read-back: the promo title's halo layer and the cart drawer's focus ring.

  python3 tools/inkringlive.py --password 1234

Covers the two r135 fixes; kept as a regression judge, so it is named after the
modules rather than the round (a round-numbered judge gets clobbered by a parallel
session, and its build assertion goes stale the moment the next round ships).

⚠ Never navigates to /cart. That path carries a Cloudflare managed challenge on
this store and touching it poisons the whole browsing session, homepage included
(memory shopify-cart-paths-trip-cloudflare-challenge). The drawer's own dialog is
not opened either -- Horizon may fetch cart sections when it opens. Instead a
fixture <dialog> carrying the real .gb-cart__close class is injected into the
homepage and opened with no gesture, which is the exact shape of the /cart landing:
same live main.js, same live stylesheet, same :focus-visible heuristic.

⚠ One context, one navigation, both checks.
"""
import re
import sys

from playwright.sync_api import sync_playwright

CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
LIVE = 'https://gumi.com.au'
PW = (sys.argv[sys.argv.index('--password') + 1]
      if '--password' in sys.argv else None)

FIXTURE = """
() => {
  const d = document.createElement('dialog');
  d.id = 'r135-probe';
  d.innerHTML = '<button class="gb-cart__close" type="button">x</button>'
              + '<button class="gb-cart__other" type="button">o</button>';
  document.body.appendChild(d);
  d.showModal();
  const b = d.querySelector('.gb-cart__close');
  const cs = getComputedStyle(b);
  return {
    active: document.activeElement === b,
    focusVisible: b.matches(':focus-visible'),
    marked: b.classList.contains('is-refocused'),
    outlineStyle: cs.outlineStyle,
    outlineWidth: cs.outlineWidth,
  };
}
"""

TITLE = """
() => {
  const t = document.querySelector('.gb-promo-panel__title');
  if (!t) { return {present: false}; }
  const halo = t.querySelector('.gb-ink-halo');
  return {
    present: true,
    text: t.textContent.trim().slice(0, 60),
    haloPresent: !!halo,
    haloZ: halo ? getComputedStyle(halo).zIndex : null,
    haloShadow: halo ? getComputedStyle(halo).textShadow.slice(0, 30) : null,
    haloPadTop: halo ? getComputedStyle(halo).paddingTop : null,
    selfShadow: getComputedStyle(t).textShadow,
    selfPadTop: getComputedStyle(t).paddingTop,
  };
}
"""

ok = red = aborted = 0


def check(name, passed, detail):
    global ok, red
    if passed:
        ok += 1
        print(f'  ok    {name}  [{detail}]')
    else:
        red += 1
        print(f'  RED   {name}  [{detail}]')


def abort(name, why):
    global aborted
    aborted += 1
    print(f'  ABORT {name}  [{why}]')


with sync_playwright() as p:
    br = p.chromium.launch(executable_path=CHROME)
    ctx = br.new_context(viewport={'width': 390, 'height': 844})
    if PW:
        # The password field lives in a collapsed panel that fill() cannot reach;
        # post the form directly -- request and browser share the cookie jar.
        ctx.request.post(LIVE + '/password', form={
            'form_type': 'storefront_password', 'utf8': '✓', 'password': PW})
    pg = ctx.new_page()
    resp = pg.goto(LIVE + '/', wait_until='domcontentloaded')
    status = resp.status if resp else 0
    if status in (429, 503):
        abort('reachable', f'{status} -- rate limited / challenged, back off')
        sys.exit(3)

    # Liveness: if the page is the password wall or the theme is not ours, every
    # assertion below would be vacuously true.
    gb = pg.evaluate("() => document.querySelectorAll('[class*=\"gb-\"]').length")
    if gb == 0:
        abort('liveness: the theme rendered', 'zero gb- classes (password wall?)')
        sys.exit(3)
    check('liveness: the theme rendered', gb > 0, f'{gb} gb- elements')

    build = pg.evaluate(
        "() => getComputedStyle(document.documentElement).getPropertyValue('--build').trim()")
    # ⚠ Compare with >=, never ==: pinning the round makes this judge go red on the
    # next push for no reason (it did, one round after it was written).
    m = re.search(r'r(\d+)', build or '')
    check('a build at or past r135 is serving', bool(m) and int(m.group(1)) >= 135,
          build or '(empty)')

    pg.wait_for_timeout(1200)

    # --- 1. cart close ring ------------------------------------------------
    r = pg.evaluate(FIXTURE)
    if not r['active']:
        abort('cart: dialog took initial focus', 'the fixture never focused')
    else:
        check('cart: close button holds the initial focus', r['active'],
              f"focusVisible={r['focusVisible']}")
        check('cart: main.js marked it', r['marked'], f"marked={r['marked']}")
        check('cart: no ring on a gesture-less open', r['outlineStyle'] == 'none',
              f"outline={r['outlineStyle']} {r['outlineWidth']}")

    # --- 2. promo title halo ----------------------------------------------
    t = pg.evaluate(TITLE)
    if not t['present']:
        # Not a pass and not a failure: the modal is behind a theme setting.
        abort('promo title present',
              'no .gb-promo-panel__title -- gb_promo_modal_enabled is off in the admin')
    else:
        check('promo: halo copy injected live', t['haloPresent'],
              f"z={t['haloZ']} shadow={(t['haloShadow'] or '')[:20]}")
        check('promo: the title paints no shadow of its own',
              t['selfShadow'] == 'none', t['selfShadow'][:24])
        check('promo: halo sits underneath', t['haloZ'] == '-1', f"z={t['haloZ']}")
        check('promo: halo carries the same top nudge',
              t['haloPadTop'] == t['selfPadTop'],
              f"halo={t['haloPadTop']} self={t['selfPadTop']}")

    br.close()

print(f'\n{ok} ok / {red} red / {aborted} aborted')
sys.exit(0 if red == 0 and aborted == 0 else 1)
