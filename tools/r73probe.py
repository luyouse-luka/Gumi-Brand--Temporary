#!/usr/bin/env python3
"""Probe live for r73: header sticky chain, PDP gallery pin, gb-sub select.

  python3 tools/r73probe.py --password 1234 [--url ...]

Reads the real ancestor chain because the static site has no Shopify section
wrappers -- source alone cannot say where the pin dies.
"""
import argparse
from playwright.sync_api import sync_playwright

CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'

CHAIN = """
(sel) => {
  const el = document.querySelector(sel);
  if (!el) return {missing: sel};
  const out = [];
  let n = el;
  while (n && n.tagName !== 'HTML') {
    const cs = getComputedStyle(n);
    out.push({
      tag: n.tagName.toLowerCase(),
      id: n.id || '',
      cls: (typeof n.className === 'string' ? n.className : '').slice(0, 48),
      position: cs.position,
      top: cs.top,
      zIndex: cs.zIndex,
      overflow: cs.overflow + '/' + cs.overflowX + '/' + cs.overflowY,
      display: cs.display,
      height: Math.round(n.getBoundingClientRect().height),
    });
    n = n.parentElement;
  }
  return {chain: out};
}
"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--password', help='storefront password')
    ap.add_argument('--url', default='https://gumi.com.au/')
    ap.add_argument('--width', type=int, default=1440)
    ap.add_argument('--height', type=int, default=900)
    a = ap.parse_args()

    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=CHROME)
        ctx = br.new_context(viewport={'width': a.width, 'height': a.height})
        if a.password:
            ctx.request.post('https://gumi.com.au/password', form={
                'form_type': 'storefront_password', 'utf8': '✓',
                'password': a.password})
            if not any(c['name'] == '_shopify_essential' for c in ctx.cookies()):
                raise SystemExit('storefront password rejected')

        page = ctx.new_page()
        page.goto(a.url, wait_until='load')
        page.wait_for_timeout(2500)

        print('URL  %s  @%dx%d' % (a.url, a.width, a.height))

        for sel in ('.gb-header', '.gb-product__media'):
            r = page.evaluate(CHAIN, sel)
            print('\n--- ancestor chain of %s ---' % sel)
            if r.get('missing'):
                print('  MISSING on this page')
                continue
            for lv in r['chain']:
                print('  %-6s %-26s pos=%-8s top=%-6s of=%-20s h=%-5d z=%s'
                      % (lv['tag'], (('#' + lv['id']) if lv['id'] else '.' + lv['cls'])[:26],
                         lv['position'], lv['top'], lv['overflow'], lv['height'], lv['zIndex']))

        # Does the pin actually hold? Scroll and read the viewport-relative top.
        print('\n--- pin behaviour (scroll 0 -> 900) ---')
        for sel in ('.gb-header', '.gb-product__media'):
            before = page.evaluate(
                "(s)=>{const e=document.querySelector(s);return e?Math.round(e.getBoundingClientRect().top):null}", sel)
            page.evaluate('window.scrollTo(0, 900)')
            page.wait_for_timeout(400)
            after = page.evaluate(
                "(s)=>{const e=document.querySelector(s);return e?Math.round(e.getBoundingClientRect().top):null}", sel)
            page.evaluate('window.scrollTo(0, 0)')
            page.wait_for_timeout(200)
            verdict = 'n/a' if after is None else ('PINNED' if after > -50 else 'SCROLLED AWAY')
            print('  %-22s top %s -> %s   %s' % (sel, before, after, verdict))

        # gb-sub select: enhanced by selectBox, or still the native control?
        print('\n--- gb-sub__select ---')
        s = page.evaluate("""() => {
          const n = document.querySelector('.gb-sub__select');
          if (!n) return {missing: true};
          return {
            attrs: [...n.attributes].map(a => a.name).join(' '),
            wrapped: !!n.closest('.gb-select'),
            button: !!document.querySelector('.gb-sub__every .gb-select__button'),
            display: getComputedStyle(n).display,
          };
        }""")
        print('  %s' % s)

        br.close()

main()
