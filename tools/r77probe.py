#!/usr/bin/env python3
"""Probe the live cart drawer: geometry, stacking, and what Horizon's dialog does to it.

  python3 tools/r77probe.py --password 1234 [--width 1440] [--shot name.png]
"""
import argparse, json
from playwright.sync_api import sync_playwright

CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
SITE = 'https://gumi.com.au'

DUMP = """
() => {
  const g = (s) => document.querySelector(s);
  const info = (el) => {
    if (!el) return null;
    const c = getComputedStyle(el);
    const r = el.getBoundingClientRect();
    return {
      tag: el.tagName.toLowerCase(), cls: el.className && el.className.toString().slice(0,80),
      rect: [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)],
      display: c.display, position: c.position, zIndex: c.zIndex,
      top: c.top, right: c.right, width: c.width, height: c.height,
      bg: c.backgroundColor, border: c.borderLeftWidth + ' ' + c.borderLeftColor,
      padding: c.padding, opacity: c.opacity, visibility: c.visibility,
      transform: c.transform, overflow: c.overflow, animation: c.animationName,
      font: c.fontFamily.split(',')[0] + ' ' + c.fontSize + '/' + c.lineHeight,
      color: c.color,
    };
  };
  const dlg = g('#cart-drawer dialog');
  return {
    modalOpen: dlg ? (dlg.matches(':modal')) : null,
    dialogOpen: dlg ? dlg.hasAttribute('open') : null,
    squeeze: !!document.querySelector('.page-wrapper--drawer-open'),
    pageWrapperMarginRight: (() => { const p = g('.page-wrapper'); return p ? getComputedStyle(p).marginRight : null; })(),
    bodyOverflow: getComputedStyle(document.body).overflow,
    htmlOverflow: getComputedStyle(document.documentElement).overflow,
    scrollbarComp: window.innerWidth - document.documentElement.clientWidth,
    nodes: {
      themeDrawer: info(g('#cart-drawer')),
      dialog: info(dlg),
      cartDrawerComponent: info(g('cart-drawer-component')),
      cartItemsComponent: info(g('cart-items-component')),
      gbCart: info(g('.gb-cart')),
      overlay: info(g('.gb-cart__overlay')),
      panel: info(g('.gb-cart__panel')),
      head: info(g('.gb-cart__head')),
      title: info(g('.gb-cart__title')),
      ship: info(g('.gb-cart__ship')),
      body: info(g('.gb-cart__body')),
      lines: info(g('.gb-cart__lines')),
      item: info(g('.gb-cart-item')),
      itemMedia: info(g('.gb-cart-item__media')),
      itemName: info(g('.gb-cart-item__name')),
      stepper: info(g('.gb-cart-item__stepper')),
      count: info(g('.gb-cart-item__count')),
      interval: info(g('.gb-cart-item__interval')),
      totals: info(g('.gb-cart__totals')),
      bar: info(g('.gb-cart__bar')),
      checkout: info(g('.gb-cart__checkout')),
      header: info(g('.gb-header')),
      headerSection: info(g('#header-group')),
    },
    // who paints on top at the panel's centre
    hitAtPanel: (() => {
      const p = g('.gb-cart__panel'); if (!p) return null;
      const r = p.getBoundingClientRect();
      const el = document.elementFromPoint(r.x + r.width/2, r.y + 24);
      return el ? el.tagName.toLowerCase() + '.' + (el.className||'').toString().slice(0,60) : null;
    })(),
    hitTopRight: (() => {
      const el = document.elementFromPoint(window.innerWidth - 60, 30);
      return el ? el.tagName.toLowerCase() + '.' + (el.className||'').toString().slice(0,60) : null;
    })(),
  };
}
"""

a = argparse.ArgumentParser()
a.add_argument('--password', required=True)
a.add_argument('--width', type=int, default=1440)
a.add_argument('--height', type=int, default=900)
a.add_argument('--shot')
a.add_argument('--css')          # local css file to inject instead of live
args = a.parse_args()

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME)
    ctx = b.new_context(viewport={'width': args.width, 'height': args.height})
    ctx.request.post(SITE + '/password', form={
        'form_type': 'storefront_password', 'utf8': '✓', 'password': args.password})
    if not any(c['name'] == '_shopify_essential' for c in ctx.cookies()):
        raise SystemExit('storefront password rejected')
    pg = ctx.new_page()
    if args.css:
        #真替换,不是叠加:叠加会让同权重规则凭顺序取胜,测出来比线上乐观
        body = open(args.css, encoding='utf-8').read()
        pg.route('**/customstyle.css*', lambda r: r.fulfill(
            status=200, content_type='text/css', body=body))
    pg.goto(SITE + '/', wait_until='networkidle')

    # find a variant to add
    vid = pg.evaluate("""async () => {
        const r = await fetch('/products.json?limit=5');
        const j = await r.json();
        for (const p of j.products) for (const v of p.variants) if (v.available) return v.id;
        return null;
    }""")
    print('variant:', vid)
    if vid:
        print('add:', pg.evaluate("""async (id) => {
            const r = await fetch('/cart/add.js', {method:'POST',
              headers:{'Content-Type':'application/json'},
              body: JSON.stringify({items:[{id:id, quantity:2}]})});
            return r.status;
        }""", vid))
    pg.goto(SITE + '/', wait_until='networkidle')

    pg.evaluate("document.querySelector('#cart-drawer').open()")
    pg.wait_for_timeout(700)
    print(json.dumps(pg.evaluate(DUMP), indent=1, ensure_ascii=False))
    if args.shot:
        pg.screenshot(path=args.shot)
    b.close()
