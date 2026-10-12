#!/usr/bin/env python3
"""Did lifting the CTA wave out of its wrapper move the decorative bears?

  python3 tools/r105bears.py --password 1234

Both bears are absolutely positioned against .gb-footer-cta-wrap:

  .gb-deco-bear--a  top: -100px    (a length, so it tracks the wrapper's top edge)
  .gb-deco-bear--b  top: 71.087%   (a percentage of the wrapper's own height)

The board draws the wave INSIDE that wrapper. Once it becomes its own section the
wrapper starts one wave lower and is one wave shorter, so bear A slides down by
the wave's height and bear B by a fraction of it.

Measured as offsets FROM THE WRAPPER, not page coordinates: live and the static
build have different page heights, and only the offsets are comparable.
"""
import argparse, sys
from playwright.sync_api import sync_playwright

CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
LIVE = 'https://gumi.com.au'
PAGES = {'index': '/', 'pdp': '/products/superfood-greens-gummies'}
WIDTHS = (390, 768, 1440)

PROBE = """() => {
  const wrap = document.querySelector('.gb-footer-cta-wrap');
  const cta = document.querySelector('.gb-footer-cta');
  const a = document.querySelector('.gb-deco-bear--a');
  const b = document.querySelector('.gb-deco-bear--b');
  if (!wrap || !cta || !a || !b) return null;
  const r = e => e.getBoundingClientRect();
  const w = r(wrap);
  return {
    wrapH: +w.height.toFixed(1),
    // where each bear sits relative to the wrapper, and to the CTA copy block
    aFromWrap: +(r(a).top - w.top).toFixed(1),
    bFromWrap: +(r(b).top - w.top).toFixed(1),
    aFromCta: +(r(a).top - r(cta).top).toFixed(1),
    bFromCta: +(r(b).top - r(cta).top).toFixed(1),
    ctaFromWrap: +(r(cta).top - w.top).toFixed(1),
  };
}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--password', required=True)
    a = ap.parse_args()
    ok = red = 0

    def grade(c, label, detail=''):
        nonlocal ok, red
        if c:
            ok += 1
        else:
            red += 1
            print(f'  RED  {label}   {detail}')

    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=CHROME)
        ctx = br.new_context(viewport={'width': 1440, 'height': 900})
        ctx.request.post(LIVE + '/password', form={
            'form_type': 'storefront_password', 'utf8': '✓', 'password': a.password})
        if not any(c['name'] == '_shopify_essential' for c in ctx.cookies()):
            sys.exit('storefront password rejected')
        pg = ctx.new_page()
        for name, path in PAGES.items():
            print(f'\n=== {name} ===')
            for w in WIDTHS:
                pg.set_viewport_size({'width': w, 'height': 900})
                pg.goto(f'file:///home/ly/project/Gumi-Brand/{name}.html',
                        wait_until='domcontentloaded')
                pg.wait_for_timeout(400)
                st = pg.evaluate(PROBE)
                pg.goto(LIVE + path, wait_until='domcontentloaded', timeout=90000)
                pg.wait_for_timeout(700)
                lv = pg.evaluate(PROBE)
                if not st or not lv:
                    grade(False, f'{name}/{w}: found the wrapper and both bears')
                    continue
                print(f"  {w:>5} static  wrapH={st['wrapH']:<8} "
                      f"A={st['aFromWrap']:<9} B={st['bFromWrap']:<9} cta={st['ctaFromWrap']}")
                print(f"  {w:>5} live    wrapH={lv['wrapH']:<8} "
                      f"A={lv['aFromWrap']:<9} B={lv['bFromWrap']:<9} cta={lv['ctaFromWrap']}")
                # The bears must sit the same distance from the CTA copy, which is
                # the thing the board positions them against visually.
                for tag, s, l in (('A', st['aFromCta'], lv['aFromCta']),
                                  ('B', st['bFromCta'], lv['bFromCta'])):
                    grade(abs(s - l) < 1.5, f'{name}/{w}: bear {tag} sits where the board puts it',
                          f'static {s} vs live {l}  (drift {l - s:+.1f})')
                    print(f"        bear {tag} from CTA: static {s:<9} live {l:<9} "
                          f"drift {l - s:+.1f}")
        br.close()
    print(f'\n{ok} ok / {red} red')
    return 1 if red else 0


if __name__ == '__main__':
    sys.exit(main())
