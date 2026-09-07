#!/usr/bin/env python3
"""Screenshot the static-site cart drawer as the restoration target."""
import sys
from playwright.sync_api import sync_playwright
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
w = int(sys.argv[1]) if len(sys.argv) > 1 else 1440
out = sys.argv[2] if len(sys.argv) > 2 else 'tools/r73shots/cart-static-desktop.png'
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME)
    pg = b.new_context(viewport={'width': w, 'height': 900}).new_page()
    pg.goto('file:///home/ly/project/Gumi-Brand/index.html', wait_until='networkidle')
    pg.evaluate("""() => {
      const c = document.getElementById('gb-cart');
      c.classList.add('is-open'); c.removeAttribute('aria-hidden');
    }""")
    pg.wait_for_timeout(900)
    print(pg.evaluate("""() => {
      const q=(s)=>{const e=document.querySelector(s); if(!e) return null;
        const r=e.getBoundingClientRect(), c=getComputedStyle(e);
        return [s, [Math.round(r.x),Math.round(r.y),Math.round(r.width),Math.round(r.height)], c.backgroundColor, c.color, c.fontSize+'/'+c.lineHeight];};
      return [q('.gb-cart__panel'),q('.gb-cart__head'),q('.gb-cart__ship'),q('.gb-cart-item__stepper'),
              q('.gb-cart-item__count'),q('.gb-cart-item__qty'),q('.gb-cart__bar'),q('.gb-select--inline'),
              q('.gb-cart-item__plan'),q('.gb-cart__continue'),q('.gb-cart-item__media')];
    }"""))
    pg.screenshot(path=out)
    b.close()
