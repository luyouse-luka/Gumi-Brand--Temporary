#!/usr/bin/env python3
"""A drawer opened behind the component's back must still close from the UI.

  python3 tools/cartsplit.py --password 1234

Client r136: "通过 /cart 进入页面，购物车是展开的，点空白处和关闭按钮都关不掉".

/cart is a redirect to /#open-cart, and gb-cart-scripts' handler for that hash does

    if (typeof drawer.showDialog === 'function') { drawer.showDialog(); }
    else { drawer.querySelector('dialog').showModal(); }    // always exists

so whenever <theme-drawer> has not upgraded yet it takes the second branch, opens
the native dialog behind the component's back, and never retries. <dialog> then
reads open while <theme-drawer> still reads closed, and on:click="#cart-drawer/close"
no-ops on BOTH the close button and the overlay. Escape still works -- that split is
the signature (memory custom-element-open-attr-vs-inner-dialog).

cartDrawer.watchSplit() observes the open attribute instead of sampling it once, so
the component gets its state back no matter when or how the dialog was opened.

⚠ Live only: the static site's cart is our own modal, with no <theme-drawer> and no
<dialog>, so there is nothing here to split. Absent structure ABORTS, never passes.

⚠ Never navigates to /cart -- that path is a Cloudflare risk on this store
(memory shopify-cart-paths-trip-cloudflare-challenge) and, being a redirect stub,
holds no cart UI anyway. The split is reproduced on the homepage, which carries the
very same drawer from layout/theme.liquid.

⚠ This judge is its own reverse test: run it against a build without watchSplit and
cases 1-3 go RED. It was written against live r135 (no fix) and confirmed RED there
before r136 was pushed.
"""
import sys

from playwright.sync_api import sync_playwright

CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
LIVE = 'https://gumi.com.au'
PW = (sys.argv[sys.argv.index('--password') + 1]
      if '--password' in sys.argv else None)

# Exactly what gb-cart-scripts does when the custom element has not upgraded:
# open the native dialog and leave the component none the wiser.
SPLIT = """
() => {
  const h = document.getElementById('cart-drawer');
  const d = h && h.querySelector('dialog');
  if (!h || !d) { return null; }
  if (d.open) { d.close(); }
  d.showModal();
  h.removeAttribute('open');
  return {hostOpen: h.hasAttribute('open'), dlgOpen: d.open};
}
"""

STATE = """
() => {
  const h = document.getElementById('cart-drawer');
  const d = h && h.querySelector('dialog');
  const c = document.querySelector('.gb-cart');
  return {
    hostOpen: h ? h.hasAttribute('open') : null,
    dlgOpen: d ? d.open : null,
    visible: c ? c.getClientRects().length > 0 : null,
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
    ctx = br.new_context(viewport={'width': 1440, 'height': 900})
    if PW:
        ctx.request.post(LIVE + '/password', form={
            'form_type': 'storefront_password', 'utf8': '✓', 'password': PW})
    pg = ctx.new_page()
    resp = pg.goto(LIVE + '/', wait_until='domcontentloaded')
    if resp and resp.status in (429, 503):
        abort('reachable', f'{resp.status} -- rate limited, back off')
        sys.exit(3)
    pg.wait_for_timeout(2500)

    build = pg.evaluate(
        "() => getComputedStyle(document.documentElement).getPropertyValue('--build').trim()")
    print(f'  live build: {build}')

    # ---- liveness: the structure this judge is about must exist ------------
    shape = pg.evaluate("""() => {
      const h = document.getElementById('cart-drawer');
      return {host: !!h, dialog: !!(h && h.querySelector('dialog')),
              close: !!document.querySelector('.gb-cart__close'),
              overlay: !!document.querySelector('.gb-cart__overlay')};
    }""")
    if not all(shape.values()):
        abort('liveness: drawer structure present', str(shape))
        br.close()
        print(f'\n{ok} ok / {red} red / {aborted} aborted')
        sys.exit(3)
    check('liveness: drawer structure present', True, str(shape))

    # ---- 1. the split cannot survive -------------------------------------
    made = pg.evaluate(SPLIT)
    pg.wait_for_timeout(400)
    s = pg.evaluate(STATE)
    check('1. component state repaired after a back-door open',
          s['hostOpen'] is True and s['dlgOpen'] is True,
          f"made={made} -> host={s['hostOpen']} dlg={s['dlgOpen']}")

    # ---- 2. the close button works ---------------------------------------
    try:
        pg.locator('.gb-cart__close').click(timeout=5000)
    except Exception as e:
        print(f'   (close click threw: {str(e)[:80]})')
    pg.wait_for_timeout(1000)
    s = pg.evaluate(STATE)
    check('2. close button shuts it', s['dlgOpen'] is False and s['visible'] is False,
          f"dlg={s['dlgOpen']} visible={s['visible']}")

    # ---- 3. the overlay works --------------------------------------------
    pg.evaluate(SPLIT)
    pg.wait_for_timeout(400)
    try:
        pg.locator('.gb-cart__overlay').click(position={'x': 40, 'y': 40}, timeout=5000)
    except Exception as e:
        print(f'   (overlay click threw: {str(e)[:80]})')
    pg.wait_for_timeout(1000)
    s = pg.evaluate(STATE)
    check('3. overlay shuts it', s['dlgOpen'] is False and s['visible'] is False,
          f"dlg={s['dlgOpen']} visible={s['visible']}")

    # ---- 4. Escape still works (it always did; guards against a fix that
    #         somehow breaks the native path) ------------------------------
    pg.evaluate(SPLIT)
    pg.wait_for_timeout(400)
    pg.keyboard.press('Escape')
    pg.wait_for_timeout(1000)
    s = pg.evaluate(STATE)
    check('4. Escape still shuts it', s['dlgOpen'] is False,
          f"dlg={s['dlgOpen']}")

    br.close()

print(f'\n{ok} ok / {red} red / {aborted} aborted')
sys.exit(0 if red == 0 and aborted == 0 else 1)
