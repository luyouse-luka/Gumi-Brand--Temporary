"""All three close paths on /cart, plus what is-open does after each."""
import argparse, json
from playwright.sync_api import sync_playwright
ap = argparse.ArgumentParser(); ap.add_argument('--password', required=True); a = ap.parse_args()
LIVE = 'https://gumi.com.au'
SNAP = """() => {
  const td = document.querySelector('#cart-drawer');
  const dlg = td && td.querySelector('dialog');
  const cart = document.querySelector('.gb-cart');
  const p = document.querySelector('.gb-cart__panel');
  const b = p && p.getBoundingClientRect();
  return {tdOpen: td && td.hasAttribute('open'), dlgOpen: dlg && dlg.open,
          cartIsOpen: cart && cart.classList.contains('is-open'),
          panelX: b ? Math.round(b.x) : null,
          visible: b ? (b.width > 0 && b.x < innerWidth - 2) : null};
}"""
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path='/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome')
    ctx = b.new_context(viewport={'width': 1440, 'height': 900})
    ctx.request.post(LIVE + '/password', form={
        'form_type': 'storefront_password', 'utf8': '✓', 'password': a.password})
    pg = ctx.new_page()
    r = pg.goto(LIVE + '/cart', wait_until='domcontentloaded', timeout=90000)
    pg.wait_for_timeout(3000)
    if r.status != 200 or 'moment' in pg.title():
        print('!! challenged'); raise SystemExit(2)
    print('on load        ', json.dumps(pg.evaluate(SNAP)))

    print('\n-- overlay attributes --')
    print(json.dumps(pg.evaluate("""() => {
        const o = document.querySelector('.gb-cart__overlay');
        const c = document.querySelector('.gb-cart__close');
        const attrs = e => e ? [...e.attributes].map(x => x.name + (x.value ? '=' + x.value : '')) : null;
        return {overlay: attrs(o), close: attrs(c)};
    }"""), indent=1))

    print('\n-- A. click the overlay (empty space) --')
    pg.evaluate("() => document.querySelector('.gb-cart__overlay').click()")
    pg.wait_for_timeout(1300)
    print('   ', json.dumps(pg.evaluate(SNAP)))

    print('\n-- reload, B. click close --')
    pg.reload(wait_until='domcontentloaded', timeout=90000); pg.wait_for_timeout(2800)
    print('   on load', json.dumps(pg.evaluate(SNAP)))
    pg.evaluate("() => document.querySelector('.gb-cart__close').click()")
    pg.wait_for_timeout(1300)
    print('   after  ', json.dumps(pg.evaluate(SNAP)))

    print('\n-- reload, C. real mouse click on empty space --')
    pg.reload(wait_until='domcontentloaded', timeout=90000); pg.wait_for_timeout(2800)
    st = pg.evaluate(SNAP)
    print('   on load', json.dumps(st))
    if st['visible']:
        pg.mouse.click(200, 450)
        pg.wait_for_timeout(1300)
        print('   after  ', json.dumps(pg.evaluate(SNAP)))
    else:
        print('   (drawer not open this load, nothing to click)')
    ctx.close(); b.close()
