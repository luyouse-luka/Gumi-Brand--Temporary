#!/usr/bin/env python3
"""r107 asks 3-4 on live -- the halves whose hooks only exist there.

  python3 tools/r107live.py --password 1234 --preflight   # before the push
  python3 tools/r107live.py --password 1234               # after it
  python3 tools/r107live.py --password 1234 --diagnose    # print, do not grade

  3  .gb-product__tag — live wraps it in div.shopify-block, so it is NOT a flex
     item and align-self never reaches it: the green plate runs the full column.
     Invisible from the static build, where the tag is a flex item itself.
  4  /404's product-list — Horizon leaves it on its own 40/40/16 gutters while
     every gb-* module runs --pad-x (80/20/20). /404 exists only on live.

--preflight injects THIS ROUND'S rules, lifted verbatim out of the compiled
assets/customstyle.css, into the live page. Both are additive at the end of the
file, so an appended copy lands where the pushed file would. A rehearsal, not a
substitute: rerun without the flag afterwards.
"""
import argparse, pathlib, re, sys
from playwright.sync_api import sync_playwright

CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
LIVE = 'https://gumi.com.au'
CSS = pathlib.Path('assets/customstyle.css')

# --pad-x per width, straight off the site's own :root -- the "same as the site"
# the client asked for. 768 sits at the ramp's bottom end.
WANT_GUTTER = {1440: 80.0, 768: 20.0, 390: 20.0}

ok = red = 0


def grade(c, label, detail=''):
    global ok, red
    if c:
        ok += 1
        print(f'  ok   {label}   {detail}')
    else:
        red += 1
        print(f'  RED  {label}   {detail}')


def near(a, b, tol=0.8):
    return a is not None and b is not None and abs(a - b) <= tol


def delta_css():
    """This round's two rules, cut out of the shipped file by their selectors."""
    text = CSS.read_text(encoding='utf-8')
    out = []
    m = re.search(r'(\.gb-product__tag \{[^}]*\})', text)
    if not m or 'inline-flex' not in m.group(1):
        sys.exit('ABORT: .gb-product__tag is not in assets/customstyle.css -- recompile first')
    out.append(m.group(1))
    m = re.search(r'(\.gb-page-wrapper \[data-testid=product-list\] \{[^}]*\})', text)
    if not m or '--page-margin' not in m.group(1):
        sys.exit('ABORT: the product-list rule is not in assets/customstyle.css -- recompile first')
    out.append(m.group(1))
    return '\n'.join(out)


TAG = """() => {
  const t = document.querySelector('.gb-product__tag');
  if (!t) return null;
  const r = t.getBoundingClientRect();
  const host = t.closest('.shopify-block') || t.parentElement;
  const hr = host.getBoundingClientRect();
  const c = t.cloneNode(true);
  c.style.cssText = 'position:absolute;visibility:hidden;width:max-content';
  host.appendChild(c);
  const ink = c.getBoundingClientRect().width;
  c.remove();
  return {w: Math.round(r.width * 10) / 10, host: Math.round(hr.width * 10) / 10,
          ink: Math.round(ink * 10) / 10, inBlock: !!t.closest('.shopify-block'),
          display: getComputedStyle(t).display};
}"""

GUT = """() => {
  const q = s => document.querySelector(s);
  const left = e => e ? Math.round(e.getBoundingClientRect().left * 10) / 10 : null;
  const pl = q('[data-testid="product-list"]');
  if (!pl) return null;
  const hdr = pl.querySelector('.section-resource-list__header');
  const card = pl.querySelector('li, .product-card, .card-gallery');
  // ⚠ Measure the INNER wrapper, not the section: product-list is full-bleed
  // and --page-margin is spent on a wrapper inside it, so the section's own
  // right edge is 0 at every width whether the rule lands or not.
  const hr = hdr && hdr.getBoundingClientRect();
  return {header: left(hdr), card: left(card),
          right: hr ? Math.round((window.innerWidth - hr.right) * 10) / 10 : null,
          pm: getComputedStyle(pl).getPropertyValue('--page-margin').trim(),
          m404: left(q('.gb-404'))};
}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--password', required=True)
    ap.add_argument('--preflight', action='store_true')
    ap.add_argument('--diagnose', action='store_true')
    a = ap.parse_args()
    css = delta_css() if a.preflight else None

    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME)
        ctx = b.new_context(viewport={'width': 1440, 'height': 900})
        ctx.request.post(LIVE + '/password', form={
            'form_type': 'storefront_password', 'utf8': '✓', 'password': a.password})
        if not any(c['name'] == '_shopify_essential' for c in ctx.cookies()):
            sys.exit('storefront password rejected')

        # find a real product page for ask 3
        page = ctx.new_page()
        page.goto(LIVE + '/collections/all', wait_until='load')
        page.wait_for_timeout(700)
        href = page.evaluate("""() => {
            const a = document.querySelector('a[href*="/products/"]');
            return a ? a.getAttribute('href') : null; }""")
        page.close()
        if not href:
            sys.exit('ABORT: no product link found on /collections/all')
        pdp = LIVE + href.split('?')[0]
        print(f'PDP: {pdp}\n')

        # --- ask 3 -----------------------------------------------------------
        for w in (1440, 390):
            page = ctx.new_page()
            page.set_viewport_size({'width': w, 'height': 900})
            page.goto(pdp, wait_until='load')
            page.wait_for_timeout(900)
            before = page.evaluate(TAG)
            if css:
                page.add_style_tag(content=css)
                page.wait_for_timeout(250)
            d = page.evaluate(TAG)
            page.close()
            if d is None:
                grade(False, f'tag @{w}', 'no .gb-product__tag on the PDP')
                continue
            if a.diagnose:
                print(f'  @{w} before={before} after={d}')
                continue
            grade(d['inBlock'], f'tag @{w} sits in .shopify-block',
                  '(the reason align-self cannot reach it)')
            grade(near(d['w'], d['ink'], 2.0), f'tag @{w} hugs its text',
                  f"w={d['w']} ink={d['ink']} host={d['host']}")
            grade(d['w'] < d['host'] - 1, f'tag @{w} narrower than its block',
                  f"w={d['w']} host={d['host']}")
            if css and before:
                grade(before['w'] > before['host'] - 1, f'tag @{w} WAS full width (guard)',
                      f"before={before['w']} host={before['host']}")

        # --- asks 1-2 on live: same rules, but the DOM is liquid's, not ours ---
        # r107check grades these on the static build; here the point is only
        # that the shipped file reached the pages that use them.
        HERO = {'/pages/faq': None, '/pages/get-in-touch': None,
                '/pages/privacy-policy': None, '/pages/referral': None,
                '/pages/shipping': None, '/pages/how-gumi-works': None,
                '/pages/our-story': None}
        for w, want_top in ((1440, '64px'), (390, '32px')):
            page = ctx.new_page()
            page.set_viewport_size({'width': w, 'height': 900})
            for path in HERO:
                page.goto(LIVE + path, wait_until='load')
                page.wait_for_timeout(500)
                got = page.evaluate("""() => {
                    const e = document.querySelector('.gb-page-hero--center');
                    return e ? getComputedStyle(e).paddingTop : null; }""")
                grade(got == want_top, f'{path} @{w} hero padding-top', f'got={got} want={want_top}')
            page.close()

        # the consent label's hover, on the page that has the form
        page = ctx.new_page()
        page.set_viewport_size({'width': 1440, 'height': 900})
        page.goto(LIVE + '/pages/get-in-touch', wait_until='load')
        page.wait_for_timeout(700)
        lab = page.locator('.gb-form__check').first
        if lab.count():
            rest = lab.evaluate('e => getComputedStyle(e).color')
            page.mouse.move(0, 0); page.wait_for_timeout(120)
            lab.hover(position={'x': 4, 'y': 4}); page.wait_for_timeout(350)
            hov = lab.evaluate('e => getComputedStyle(e).color')
            grade(hov == rest, 'consent label does not shift on hover', f'rest={rest} hover={hov}')
            grade(rest == 'rgb(101, 101, 101)', 'consent label rest colour', f'got={rest}')
        else:
            grade(False, 'consent label present on live', 'no .gb-form__check found')
        page.close()

        # --- ask 4 -----------------------------------------------------------
        for w, want in WANT_GUTTER.items():
            page = ctx.new_page()
            page.set_viewport_size({'width': w, 'height': 900})
            page.goto(LIVE + '/404-this-page-does-not-exist', wait_until='load')
            page.wait_for_timeout(900)
            before = page.evaluate(GUT)
            if css:
                page.add_style_tag(content=css)
                page.wait_for_timeout(250)
            d = page.evaluate(GUT)
            page.close()
            if d is None:
                grade(False, f'404 @{w}', 'no product-list on /404')
                continue
            if a.diagnose:
                print(f'  @{w} before={before} after={d}')
                continue
            grade(near(d['header'], want), f'404 @{w} list header gutter',
                  f"got={d['header']} want={want}")
            grade(near(d['card'], want), f'404 @{w} card gutter',
                  f"got={d['card']} want={want}")
            grade(near(d['right'], want, 2.0), f'404 @{w} right gutter',
                  f"got={d['right']} want={want}")
            if css and before:
                grade(not near(before['header'], want),
                      f'404 @{w} WAS off the site gutter (guard)',
                      f"before={before['header']}")
        b.close()

    if not a.diagnose:
        print(f'\n{ok} ok / {red} red')
        sys.exit(1 if red else 0)


main()
