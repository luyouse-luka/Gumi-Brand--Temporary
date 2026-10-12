#!/usr/bin/env python3
"""r107 judge -- two client asks.

  python3 tools/r107check.py

1. .gb-form__check no longer shifts colour on hover. The <a> inside still does,
   and that assertion is the liveness guard: without it "label did not change"
   is trivially true in any environment where hover never fires at all.
   ⚠ (hover: hover) is always false in bare headless chromium -- this runs
   through Playwright, where it is true.
2. .gb-page-hero--center padding-top is the board's 64 on desktop again (r106
   had it at 80), 32 on mobile, and the tablet ramp lands on both ends.
   Bottom padding must be untouched -- that is the regression half.
"""
import pathlib, sys
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
GREY = 'rgb(101, 101, 101)'          # #656565, the label's own colour
INK = 'rgb(1, 19, 7)'                # $c-ink, what r106 hovered to
GREEN = 'rgb(0, 86, 53)'             # $c-green #005635, the <a> hover

CENTER_PAGES = ['faq.html', 'get-in-touch.html', 'privacy-policy.html',
                'referral.html', 'shipping.html', 'how-gumi-works.html',
                'our-story.html']
TAG_PAGES = ['index.html', 'pdp.html', 'how-gumi-works.html', 'our-story.html',
             'reviews.html']
# width -> expected padding-top on .gb-page-hero--center
WIDTHS = [(390, '32px'), (768, '32px'), (1281, '64px'), (1440, '64px')]

fails = []


def check(name, got, want):
    ok = got == want
    print(('  ok   ' if ok else '  FAIL ') + name + ('' if ok else '   got=%r want=%r' % (got, want)))
    if not ok:
        fails.append(name)


with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=CHROME)

    # --- 1. hover on the consent label ---------------------------------------
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto((ROOT / 'get-in-touch.html').as_uri())
    page.wait_for_timeout(400)

    check('hover media query is live here',
          page.evaluate("matchMedia('(hover: hover)').matches"), True)

    label = page.locator('.gb-form__check').first
    link = page.locator('.gb-form__check a').first
    colour = lambda loc: loc.evaluate("e => getComputedStyle(e).color")

    check('label rest colour', colour(label), GREY)

    page.mouse.move(0, 0)
    page.wait_for_timeout(150)
    label.hover(position={'x': 4, 'y': 4})      # on the label, off the <a>
    page.wait_for_timeout(400)
    got = colour(label)
    check('label does NOT shift on hover', got, GREY)
    if got == INK:
        print('       ^ that is the r106 value -- the @include hover survived')

    # liveness guard: hover demonstrably works in this environment
    link.hover()
    page.wait_for_timeout(400)
    check('<a> still greens on hover (guard)', colour(link), GREEN)

    # the drawn box keeps its own transition -- only the label's colour one went
    box_tr = page.evaluate(
        "() => getComputedStyle(document.querySelector('.gb-form__check'), '::before').transitionProperty")
    check('::before still transitions', 'background-color' in box_tr and 'border-color' in box_tr, True)
    check('label carries no colour transition',
          page.evaluate("() => getComputedStyle(document.querySelector('.gb-form__check')).transitionProperty"),
          'all')     # 'all' with 0s duration == the UA default, i.e. none of ours
    page.close()

    # --- 2. .gb-page-hero--center padding -------------------------------------
    for w, want_top in WIDTHS:
        page = browser.new_page(viewport={'width': w, 'height': 900})
        for f in CENTER_PAGES:
            page.goto((ROOT / f).as_uri())
            page.wait_for_timeout(120)
            pt, pb = page.evaluate("""() => {
                const e = document.querySelector('.gb-page-hero--center');
                const s = getComputedStyle(e);
                return [s.paddingTop, s.paddingBottom];
            }""")
            check('%-22s @%-5d padding-top' % (f, w), pt, want_top)
            # bottom is regression-only: it must still carry the wave reserve,
            # i.e. be strictly larger than the 70/64 base it is built from.
            check('%-22s @%-5d bottom kept wave' % (f, w),
                  float(pb[:-2]) > 64, True)
        page.close()

    # --- 3. .gb-product__tag hugs its text, static build must not regress -----
    # Here the tag IS a flex item, so display:inline-flex is blockified back to
    # flex and align-self already sized it -- the assertion is that nothing moved
    # and the plate is still narrower than its column. The live half (where the
    # tag sits inside div.shopify-block and is NOT a flex item) is r107live.py.
    for w in (1440, 390):
        page = browser.new_page(viewport={'width': w, 'height': 900})
        for f in TAG_PAGES:
            page.goto((ROOT / f).as_uri())
            page.wait_for_timeout(120)
            got = page.evaluate("""() => {
                const t = document.querySelector('.gb-product__tag');
                if (!t) return null;
                const r = t.getBoundingClientRect();
                const pr = t.parentElement.getBoundingClientRect();
                const s = getComputedStyle(t);
                // width the text actually needs, measured off a clone
                const c = t.cloneNode(true);
                c.style.cssText = 'position:absolute;visibility:hidden;width:max-content';
                t.parentElement.appendChild(c);
                const ink = c.getBoundingClientRect().width;
                c.remove();
                return {w: Math.round(r.width * 10) / 10, parent: Math.round(pr.width * 10) / 10,
                        ink: Math.round(ink * 10) / 10, display: s.display, width: s.width};
            }""")
            check('%-20s @%-5d tag hugs text' % (f, w),
                  got and abs(got['w'] - got['ink']) < 1.5, True)
            check('%-20s @%-5d tag < column' % (f, w),
                  got and got['w'] < got['parent'] - 1, True)
        page.close()

    browser.close()

print('\n%d ok / %d red' % (len(CENTER_PAGES) * len(WIDTHS) * 2 + len(TAG_PAGES) * 4 + 6 - len(fails), len(fails)))
if fails:
    print('RED:'); [print('  -', f) for f in fails]
    sys.exit(1)
