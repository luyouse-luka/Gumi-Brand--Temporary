#!/usr/bin/env python3
"""r107 asks 7-8 -- the two states that only exist under a forced pseudo-class.

  python3 tools/r107states.py

7  No focus ring on a drawer's close button / the header icons on a TOUCH screen
   (pointer: coarse). A desktop pointer must still get the ring.
8  No :active scale left anywhere.

⚠ el.focus() does not produce :focus-visible and a scripted click does not
  produce :active, so both states are forced through CDP CSS.forcePseudoState.
⚠ The Safari half is NOT tested here. This machine has chromium only, and the
  reported symptom (Horizon's <dialog> handing focus to .gb-cart__close, Safari
  counting it as keyboard focus) is engine-specific. What this grades is that the
  rule matches on a coarse pointer and does not on a fine one.
"""
import pathlib, re, sys
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'

RING = ['.gb-cart__close', '.gb-header__icon', '.gb-header__panel-close',
        '.gb-nl-panel__close', '.gb-promo-panel__close', '.gb-rv-panel__close']
PRESS = ['.gb-rv-panel__close', '.gb-cart__close', '.gb-cart-item__remove',
         '.gb-cart-item__step', '.gb-header__icon', '.gb-header__panel-close',
         '.gb-reel', '.gb-reels__btn', '.gb-crev-card__vote']
PAGES = ['index.html', 'pdp.html', 'reviews.html']

fails = []


def no_scale(tr):
    if tr in (None, '', 'none'):
        return True
    m = re.match(r'matrix\(([-\d.]+),\s*[-\d.]+,\s*[-\d.]+,\s*([-\d.]+)', tr)
    if not m:
        return False
    return abs(float(m.group(1)) - 1) < 1e-3 and abs(float(m.group(2)) - 1) < 1e-3


def check(name, got, want):
    ok = got == want
    print(('  ok   ' if ok else '  FAIL ') + name + ('' if ok else f'   got={got!r} want={want!r}'))
    if not ok:
        fails.append(name)


def forced(page, sel, pseudo, prop):
    """computed `prop` on the first `sel` with `pseudo` forced on, or None."""
    cdp = page.context.new_cdp_session(page)
    cdp.send('DOM.enable'); cdp.send('CSS.enable')
    doc = cdp.send('DOM.getDocument')
    n = cdp.send('DOM.querySelector', {'nodeId': doc['root']['nodeId'], 'selector': sel})
    if not n['nodeId']:
        cdp.detach(); return None
    cdp.send('CSS.forcePseudoState',
             {'nodeId': n['nodeId'], 'forcedPseudoClasses': [pseudo]})
    val = page.evaluate("""([s, p]) => {
        const e = document.querySelector(s);
        return e ? getComputedStyle(e).getPropertyValue(p) : null; }""", [sel, prop])
    cdp.send('CSS.forcePseudoState', {'nodeId': n['nodeId'], 'forcedPseudoClasses': []})
    cdp.detach()
    return val


with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME)

    # --- 7. the ring, coarse vs fine pointer ---------------------------------
    for label, kw, want in (('touch ', dict(viewport={'width': 390, 'height': 844},
                                            is_mobile=True, has_touch=True), 'none'),
                            ('mouse ', dict(viewport={'width': 1440, 'height': 900}), 'ring')):
        ctx = b.new_context(**kw)
        page = ctx.new_page()
        seen = 0
        for f in PAGES:
            page.goto((ROOT / f).as_uri())
            page.wait_for_timeout(200)
            for sel in RING:
                # ⚠ outline is a shorthand: its computed value starts with the
                # COLOUR ("rgb(1, 19, 7) none 0px"), so testing the first token
                # for "none" reports a ring on every element. Read the style.
                out = forced(page, sel, 'focus-visible', 'outline-style')
                if out is None:
                    continue
                seen += 1
                has_ring = out not in ('none', '')
                check(f'{label}{sel:<26} {"ring" if has_ring else "none"}',
                      'ring' if has_ring else 'none', want)
        check(f'{label}selectors actually found', seen > 0, True)
        ctx.close()

    # --- 8. no press-shrink anywhere -----------------------------------------
    ctx = b.new_context(viewport={'width': 1440, 'height': 900})
    page = ctx.new_page()
    seen = 0
    for f in PAGES:
        page.goto((ROOT / f).as_uri())
        page.wait_for_timeout(200)
        for sel in PRESS:
            tr = forced(page, sel, 'active', 'transform')
            if tr is None:
                continue
            seen += 1
            # ⚠ .gb-reel is also .swiper-slide, whose own transform resolves to
            # the identity matrix -- equal to no scale, but not the string
            # "none". Grade the matrix's scale components, not the text.
            check(f'active {sel:<26} no scale', no_scale(tr), True)
    check('press selectors actually found', seen > 0, True)
    ctx.close()
    b.close()

print(f'\n{len(fails)} red')
if fails:
    print('RED:'); [print('  -', f) for f in fails]
    sys.exit(1)
