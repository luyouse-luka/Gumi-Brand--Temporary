#!/usr/bin/env python3
"""r78 judge -- reel focus ring un-clipped, footer ring takes the text colour,
header CTA back to 0 40px.

  python3 tools/r78check.py

Static-site only: all three live in modules that render identically on live, and
the live half needs the storefront, which rate-limits. Rings are reached with
real Tab presses -- el.focus() does not set :focus-visible.
"""
import io, re, sys
from playwright.sync_api import sync_playwright

CSS, SCSS = 'assets/customstyle.css', 'assets/customstyle.scss'
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
BUILD = '20260907-r78'
GREEN, LIME200, LIME100, LIME = '#005635', '#daf6b0', '#f4fce7', '#b5ed61'

fails = []
def check(name, got, want):
    ok = got == want
    print(('  ok   ' if ok else '  FAIL ') + name + ('' if ok else '   got=%s want=%s' % (repr(got), repr(want))))
    if not ok: fails.append(name)

def block(css, sel):
    for m in re.finditer(r'(?m)^([^@{}]+?)\{([^{}]*)\}', css):
        if ' '.join(m.group(1).split()) == sel:
            return ' '.join(m.group(2).split())
    return None

print('== compiled css ==')
css = io.open(CSS, encoding='utf-8').read()
scss = io.open(SCSS, encoding='utf-8').read()
# Not pinned to ==: $build is bumped every round, so an equality here turns
# this judge false-red the moment the next round lands. r77check does the same.
check('$build at or past r78', re.search(r'\$build:\s*"([^"]+)"', scss).group(1) >= BUILD, True)

# ⚠ r82 (client) replaced the inset ::after ring with the hover scale, so the
# ring's geometry is no longer this judge's business -- r82check owns the new
# shape. What survives from r78 is the contract that made the ring necessary:
# the global outline is suppressed AND focus still has a visible answer, because
# the rail clips the card box and a plain outline reads as no focus at all.
check('reel outline suppressed', block(css, '.gb-reel:focus-visible'), 'outline: none;')
check('reel focus still has a visible answer',
      block(css, '.gb-reel:focus-visible .gb-reel__media') is not None
      or block(css, '.gb-reel:focus-visible::after') is not None, True)

check('footer ring takes the text colour', block(css, '.gb-footer :focus-visible'),
      'outline-color: currentColor;')
check('footer submit ring is the light one', block(css, '.gb-footer__submit:focus-visible'),
      'outline-color: %s;' % LIME200)

cta = block(css, '.gb-header__cta')
check('header cta rule found (anchor)', cta is not None, True)
check('  header cta padding', 'padding: 0 40px;' in (cta or ''), True)

# ⚠ negative: the base class must NOT have moved -- .gb-btn--primary is also the
# cart drawer's Shop Now, and the cart is frozen this round. Anchor first, or a
# missed block would make this pass vacuously.
prim = block(css, '.gb-btn--primary')
check('.gb-btn--primary found (anchor)', prim is not None, True)
check('  base class untouched (cart is frozen)', 'padding: 0 42px;' in (prim or ''), True)

print('\n== static render ==')
def tab_to(pg, sel, limit=110):
    pg.evaluate("document.body.focus()")
    for _ in range(limit):
        pg.keyboard.press('Tab')
        if pg.evaluate("(s)=>{const a=document.activeElement;return !!(a&&a.matches&&a.matches(s));}", sel):
            return True
    return False

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME)
    pg = b.new_context(viewport={'width': 1440, 'height': 900}).new_page()
    pg.goto('file:///home/ly/project/Gumi-Brand/index.html', wait_until='networkidle')
    pg.wait_for_timeout(1200)
    # .wowo parks at opacity 0 and only animates on scroll, which a headless page
    # cannot drive reliably; without this the crop comes back washed out.
    pg.evaluate("""() => { document.querySelectorAll('.wowo').forEach(e=>e.classList.remove('wowo','animated'));
                  document.querySelector('.gb-reels').scrollIntoView({block:'center'}); }""")
    pg.wait_for_timeout(500)

    check('tabbed to a reel', tab_to(pg, '.gb-reel'), True)
    idx = pg.evaluate("""()=>{const e=[...document.querySelectorAll('.gb-reel')];
        const v=e.find(x=>{const b=x.getBoundingClientRect();return b.x>0&&b.x+b.width<1440;});
        return v?e.indexOf(v):0;}""")
    for _ in range(idx):
        pg.keyboard.press('Tab')
    # ⚠ r82 (client) dropped the ring for the hover scale, so the four-edge pixel
    # scan that used to live here no longer describes the design. The contract it
    # was guarding -- "a focused reel looks different, and the rail does not clip
    # the difference away" -- is now carried by the transform, which paints on
    # .gb-reel__media INSIDE the card and so cannot be clipped at the card edge.
    # ⚠ .gb-reel__media transitions the transform; reading straight after the
    # Tab returns the START value (identity). See memory
    # headless-transition-reads-start-value.
    pg.wait_for_timeout(400)
    m = pg.evaluate("()=>{const el=document.activeElement;"
                    "const md=el.querySelector('.gb-reel__media');"
                    "return {vis: el.matches(':focus-visible'),"
                    "        tr: md?getComputedStyle(md).transform:null,"
                    "        after: getComputedStyle(el,'::after').content};}")
    check('focused reel is :focus-visible (anchor)', m['vis'], True)
    check('focus scales the media', m['tr'], 'matrix(1.06, 0, 0, 1.06, 0, 0)')
    check('no ::after ring left', m['after'] in ('none', 'normal'), True)

    # every footer ring must match the text beside it (the submit is the exception)
    for sel, want in [('.gb-footer__logo', 'same'), ('.gb-footer__link', 'same'),
                      ('.gb-footer__social-link', 'same'),
                      ('.gb-footer__submit', 'rgb(218, 246, 176)')]:
        check('tabbed to %s' % sel, tab_to(pg, sel), True)
        v = pg.evaluate("""(s)=>{const e=document.querySelector(s);const c=getComputedStyle(e);
            return [c.outlineColor, c.color];}""", sel)
        check('  %s ring' % sel, v[0], v[1] if want == 'same' else want)

    check('footer ground unchanged', pg.evaluate(
        "()=>getComputedStyle(document.querySelector('.gb-footer')).backgroundColor"), 'rgb(0, 65, 40)')

    geo = pg.evaluate("""()=>{const q=(s)=>{const e=document.querySelector(s);if(!e)return null;
        const b=e.getBoundingClientRect();return [Math.round(b.width),getComputedStyle(e).padding];};
        return {cta:q('.gb-header__cta'), cartShop:q('.gb-cart__shop')};}""")
    check('header cta box', geo['cta'], [159, '0px 40px'])
    # The cart's Shop Now carries its OWN padding rule (0 40px) and always has --
    # byte-identical in live-20260907-r77check. It does not inherit the base
    # class's 42, so "unchanged" here means 40, not 42. Anchor first so a renamed
    # button cannot make this pass vacuously.
    check('cart Shop Now found (anchor)', geo['cartShop'] is not None, True)
    check('  cart Shop Now unchanged (frozen)', geo['cartShop'][1], '0px 40px')
    b.close()

if fails:
    print('\n%d FAIL: %s' % (len(fails), ', '.join(fails)))
else:
    print('\nall assertions ok')
sys.exit(1 if fails else 0)
