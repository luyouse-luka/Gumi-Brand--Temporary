#!/usr/bin/env python3
"""Survey: which elements on /collections/all still run Horizon's font.

  python3 tools/collfont.py --password 1234
"""
import argparse, pathlib, sys
from playwright.sync_api import sync_playwright

CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
LIVE = 'https://gumi.com.au'

PROBE = """() => {
  const out = [];
  const seen = new Set();
  const walk = e => {
    for (const c of e.children) walk(c);
    // leaf-ish: has own text
    const own = [...e.childNodes].filter(n => n.nodeType === 3 && n.textContent.trim()).
                map(n => n.textContent.trim()).join(' ');
    if (!own) return;
    const r = e.getBoundingClientRect();
    if (!r.width || !r.height) return;
    const cs = getComputedStyle(e);
    if (cs.visibility === 'hidden') return;
    const path = (() => {
      let p = [], n = e;
      while (n && n !== document.body && p.length < 4) {
        p.unshift(n.tagName.toLowerCase() + (n.className && typeof n.className === 'string'
          ? '.' + n.className.trim().split(/\\s+/).slice(0,3).join('.') : ''));
        n = n.parentElement;
      }
      return p.join(' > ');
    })();
    const key = path + '|' + cs.fontFamily + '|' + cs.fontSize;
    if (seen.has(key)) return;
    seen.add(key);
    out.push({path, text: own.slice(0, 40), ff: cs.fontFamily,
              fs: cs.fontSize, fw: cs.fontWeight, lh: cs.lineHeight, color: cs.color});
  };
  walk(document.querySelector('#MainContent') || document.body);
  return out;
}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--password', required=True)
    ap.add_argument('--width', type=int, default=1440)
    ap.add_argument('--url', default='/collections/all')
    a = ap.parse_args()

    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME)
        ctx = b.new_context(viewport={'width': a.width, 'height': 900})
        ctx.request.post(LIVE + '/password', form={
            'form_type': 'storefront_password', 'utf8': '✓', 'password': a.password})
        if not any(c['name'] == '_shopify_essential' for c in ctx.cookies()):
            sys.exit('storefront password rejected')
        page = ctx.new_page()
        page.goto(LIVE + a.url, wait_until='load')
        page.wait_for_timeout(2500)
        rows = page.evaluate(PROBE)
        b.close()

    print(f'{len(rows)} text elements @ {a.width} on {a.url}\n')
    for r in rows:
        brand = 'PP Palma' in r['ff']
        print(f"{'PALMA ' if brand else '**HORIZ'}  {r['fs']:>6}/{r['fw']:<3} {r['lh']:>7}  "
              f"{r['ff'][:34]:<34}  {r['color']:<18}  {r['path']}")
        print(f"          text: {r['text']!r}")


main()
