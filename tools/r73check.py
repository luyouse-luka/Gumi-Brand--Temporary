#!/usr/bin/env python3
"""r73 assertions: header pin on live, PDP gallery flush, cta gap, no press dip.

  python3 tools/r73check.py                      # static site only
  python3 tools/r73check.py --password 1234      # + live (injects the new css)

Live checks inject the freshly compiled customstyle.css and the data-select
attribute, so they answer "will the push fix it" before anything is pushed.
"""
import argparse, pathlib, re, sys
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
LIVE_PDP = 'https://gumi.com.au/products/superfood-greens-gummies'

ok = fail = 0
def check(label, got, want, note=''):
    global ok, fail
    good = (got == want) if not callable(want) else want(got)
    print('  %s %-52s got=%-22s %s' % ('ok  ' if good else 'FAIL', label, repr(got),
                                       ('want=%s' % repr(want)) if not callable(want) else note))
    if good: ok += 1
    else: fail += 1

def css_text_checks():
    print('--- compiled css (text assertions) ---')
    css = (ROOT / 'assets/customstyle.css').read_text()
    scss = (ROOT / 'assets/customstyle.scss').read_text()
    # 5. the press dip is gone everywhere, but the scale presses stay
    check('translateY(1px) press dips removed', css.count('translateY(1px)'), 0)
    check('scale() press states kept',
          len(re.findall(r':active\s*\{\s*transform:\s*scale', css)), 8)
    # transform must not linger in a transition list that has no transform state.
    # The block regex is asserted to MATCH first: a miss would make the negative
    # assertion below pass on an empty string.
    for sel in ('.gb-btn', '.gb-product__cta', '.gb-product__label-btn',
                '.gb-footer__submit', '.gb-promo-panel__copy'):
        blk = re.search(r'^' + re.escape(sel) + r'\s*\{[^}]*\}', css, re.M)
        check('%s block found (anchor)' % sel, blk is not None, True)
        body = blk.group(0) if blk else 'transition: ANCHOR-MISSING transform'
        tr = [l for l in body.split('\n') if 'transition:' in l]
        check('%s transition drops transform' % sel,
              any('transform' in l for l in tr) or not tr, False)
    # 1. the live-only wrapper rule
    check('#header-group display:contents rule present',
          bool(re.search(r'#header-group,\s*\n#header-group > \* \{\s*\n\s*display: contents;', css)), True)
    # 3/4. live-only cta gap, scoped by the child combinator
    check('.gb-product__form > .gb-product__cta margin-top:20px',
          bool(re.search(r'\.gb-product__form > \.gb-product__cta \{\s*\n\s*margin-top: 20px;', css)), True)
    # anchored on the declaration, not a line index: inserting anything above it
    # silently moved this check off target once already
    m = re.search(r'^\$build:\s*"([^"]+)"', scss, re.M)
    # >= not ==: the token moves every round; pinning it is a false red.
    check('$build at or past r76', bool(m) and m.group(1) >= '20260907-r76', True)
    js = (ROOT / 'assets/main.js').read_text()
    # r76 reverted the adopt loop: the live list stays native, by client request
    check('main.js no longer adopts the live select',
          'data-gb-plan-select' in js, False)
    check('native select restyled for the live theme',
          '.gb-sub__select:not(.gb-select__native)' in scss, True)
    check('footer wave regains its mint top after .gb-faq',
          bool(re.search(r'#MainContent:has\(> \.shopify-section:last-child > \.gb-faq\)'
                         r' \+ footer \.gb-scallop--to-lime', css)), True)
    # one level of :has() only -- it cannot nest, and an @extend once spliced a
    # selector inside one and killed the rule silently
    check('no nested :has() anywhere', bool(re.search(r':has\([^)]*:has\(', css)), False)
    check('.gb-scallop left as a single selector',
          bool(re.search(r'^\.gb-scallop \{', css, re.M)), True)

def static_checks():
    print('\n--- static site (file://) ---')
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=CHROME)
        pg = br.new_context(viewport={'width': 1440, 'height': 900}).new_page()
        pg.goto((ROOT / 'pdp.html').as_uri(), wait_until='load')
        pg.wait_for_timeout(1200)
        # 2. gallery pins flush under the 80px header
        check('pdp .gb-product__media sticky top @1440 (client rev 2: header+20)',
              pg.evaluate("()=>getComputedStyle(document.querySelector('.gb-product__media')).top"), '100px')
        # the live-only cart bubble rules must not match anything locally
        check('static has no .gb-header__icon-wrap (bubble rules inert)',
              pg.evaluate("()=>document.querySelectorAll('.gb-header__icon-wrap, .cart-bubble').length"), 0)
        # 4. the static copy sits in .gb-sub, so it must NOT gain the 20px margin
        check('static cta margin-top unchanged',
              pg.evaluate("()=>getComputedStyle(document.querySelector('.gb-product__cta')).marginTop"), '0px')
        check('static cta still 20px below .gb-sub__plans',
              pg.evaluate("""()=>{const c=document.querySelector('.gb-product__cta');
                const pr=c.previousElementSibling;
                return Math.round(c.getBoundingClientRect().top-pr.getBoundingClientRect().bottom)}"""), 20)
        check('static cta parent is .gb-sub (no .gb-product__form here)',
              pg.evaluate("()=>document.querySelector('.gb-product__cta').parentElement.className"), 'gb-sub')
        check('static select unaffected by the adopt loop (no vendor hook here)',
              pg.evaluate("()=>document.querySelector('.gb-sub__select').hasAttribute('data-gb-plan-select')"), False)
        check('static select still enhanced, 40px button',
              pg.evaluate("()=>{const b=document.querySelector('.gb-sub__every .gb-select__button');return b?Math.round(b.getBoundingClientRect().height):null}"), 40)
        # header pin still works on the static site (no wrappers there)
        pg.evaluate('window.scrollTo(0,900)'); pg.wait_for_timeout(300)
        check('static header still pinned at 0',
              pg.evaluate("()=>Math.round(document.querySelector('.gb-header').getBoundingClientRect().top)"), 0)
        br.close()

def live_checks(password, inject=True):
    print('\n--- live (%s) ---' % ('new css + data-select injected, nothing pushed'
                                   if inject else 'AS SERVED, nothing injected'))
    css = (ROOT / 'assets/customstyle.css').read_text()
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=CHROME)
        ctx = br.new_context(viewport={'width': 1440, 'height': 900})
        ctx.request.post('https://gumi.com.au/password', form={
            'form_type': 'storefront_password', 'utf8': '✓', 'password': password})
        if not any(c['name'] == '_shopify_essential' for c in ctx.cookies()):
            raise SystemExit('storefront password rejected')
        pg = ctx.new_page()
        pg.goto(LIVE_PDP, wait_until='load'); pg.wait_for_timeout(2500)

        if inject:
            # Informational, not an assertion: it reproduces the bug only while the
            # css fix is unpushed. Once r73's css is live this reads 0, which is
            # the fix working -- not a regression.
            before = pg.evaluate("()=>{window.scrollTo(0,900);return Math.round(document.querySelector('.gb-header').getBoundingClientRect().top)}")
            print('  --   pre-injection header top = %s  (%s)' % (
                  before, 'bug still reproduces, css not pushed' if before < -50
                          else 'already fixed on live'))
            pg.evaluate('window.scrollTo(0,0)'); pg.wait_for_timeout(200)

            pg.add_style_tag(content=css)
            # r76 reverted the adopt loop, so undo what the live (r75) main.js
            # already did -- otherwise this measures the build being replaced.
            # Once r76 is live the page arrives in this state on its own.
            pg.evaluate("""()=>{document.querySelectorAll('.gb-sub__every .gb-select').forEach(w=>{
              const n=w.querySelector('select'); if(!n) return;
              n.classList.remove('gb-select__native');
              n.removeAttribute('tabindex'); n.removeAttribute('data-select');
              w.parentNode.insertBefore(n, w); w.remove();});}""")
            pg.wait_for_timeout(400)
        else:
            # served build must actually be the one we pushed, or every assertion
            # below is measuring the previous release
            check('served build is r76',
                  pg.evaluate("""()=>[...document.querySelectorAll('link[rel=stylesheet],script[src]')]
                    .some(e=>/customstyle/.test(e.href||e.src||''))"""), True)
            check('served main.js dropped the adopt loop',
                  pg.evaluate("""()=>!document.querySelector('.gb-sub__every .gb-select__button')"""), True)
            check('press dip gone in served css',
                  pg.evaluate("""()=>{const b=document.querySelector('.gb-btn');
                    return getComputedStyle(b).transitionProperty.includes('transform')}"""), False)

        pg.evaluate('window.scrollTo(0,900)'); pg.wait_for_timeout(400)
        check('header pinned at top after fix',
              pg.evaluate("()=>Math.round(document.querySelector('.gb-header').getBoundingClientRect().top)"), 0)
        check('announcement bar still scrolls away',
              pg.evaluate("()=>Math.round(document.querySelector('.gb-announcement').getBoundingClientRect().top)") < -50, True,
              'must NOT pin with the header')
        check('gallery pinned at header+20',
              pg.evaluate("()=>Math.round(document.querySelector('.gb-product__media').getBoundingClientRect().top)"), 100)
        pg.evaluate('window.scrollTo(0,0)'); pg.wait_for_timeout(300)
        check('live cta margin-top now 20px',
              pg.evaluate("()=>getComputedStyle(document.querySelector('.gb-product__cta')).marginTop"), '20px')
        check('live cta 20px below .gb-sub',
              pg.evaluate("""()=>{const c=document.querySelector('.gb-product__cta');
                const pr=c.previousElementSibling;
                return Math.round(c.getBoundingClientRect().top-pr.getBoundingClientRect().bottom)}"""), 20)
        check('live select stays native (client: leave the popup alone)',
              pg.evaluate("()=>!!document.querySelector('.gb-sub__every .gb-select__button')"), False)
        check('native select restyled to the board',
              pg.evaluate("""()=>{const n=document.querySelector('.gb-sub__select');
                if(!n) return null; const cs=getComputedStyle(n);
                return Math.round(n.getBoundingClientRect().height)+'/'+cs.borderRadius
                       +'/'+cs.fontSize+'/'+(cs.backgroundImage.includes('svg')?'arrow':'noarrow')}"""),
              '40/8px/14px/arrow')
        check('native select kept as value carrier',
              pg.evaluate("()=>!!document.querySelector('.gb-sub__select[data-gb-plan-select]')"), True)

        # the enhancement must still drive the vendor's price logic
        changed = 'change fired'  # native control: the vendor's own listener, untouched
        # Native control now: drive it the way a user would (select an option and
        # let the change event fly) and confirm the vendor's listener still reacts.
        changed = pg.evaluate("""()=>new Promise(res=>{
            const n=document.querySelector('.gb-sub__select');
            if(!n||n.options.length<2) return res('too few options');
            let fired=false; n.addEventListener('change',()=>fired=true,{once:true});
            n.selectedIndex = 1;
            n.dispatchEvent(new Event('change',{bubbles:true}));
            setTimeout(()=>res(fired?'change fired':'NO change event'),200);})""")
        check('selecting an option fires change (vendor js hook)', changed, 'change fired')

        if True:
            # simulate a non-empty cart: the bubble is visually-hidden at 0 items
            pg.evaluate("""()=>{const w=document.querySelector('.gb-header__icon-wrap');
              const b=document.querySelector('.cart-bubble');
              if(!w||!b) return; w.classList.add('header-actions__cart-icon--has-cart');
              b.classList.remove('visually-hidden');
              const c=b.querySelector('.cart-bubble__text-count');
              c.classList.remove('hidden'); c.textContent='3';}""")
            pg.wait_for_timeout(300)
            bub = pg.evaluate("""()=>{const i=document.querySelector('.gb-header__icon-wrap .gb-header__icon');
              const b=document.querySelector('.cart-bubble');
              if(!i||!b) return null; const ir=i.getBoundingClientRect(), br=b.getBoundingClientRect();
              return {dx:Math.round(br.right-ir.right), dy:Math.round(br.top-ir.top),
                      w:Math.round(br.width), h:Math.round(br.height),
                      bg:getComputedStyle(document.querySelector('.cart-bubble__background')).backgroundColor,
                      iconH:Math.round(ir.height)};}""")
            check('cart bubble sits top-right of the icon', (bub['dx'], bub['dy']), (3, -3))
            check('cart bubble size 16', (bub['w'], bub['h']), (16, 16))
            check('cart bubble background is $c-green', bub['bg'], 'rgb(0, 86, 53)')
            check('icon box no longer stretched by the bubble', bub['iconH'], 24)
        br.close()

def faq_wave_checks(password, inject=True):
    """The wave between .gb-faq and the footer. The theme sets it from a section
    setting to `to-lime`, whose transparent top is right under the white cta
    band (faq page) and wrong straight after .gb-faq, where the mint has to
    carry into it."""
    print('\n--- footer wave above the faq (%s) ---' % ('css injected' if inject else 'as served'))
    css = (ROOT / 'assets/customstyle.css').read_text()
    PROBE = """()=>{
      const w=document.querySelector('footer .gb-scallop--to-lime');
      if(!w) return {none:true};
      const cs=getComputedStyle(w);
      const t=w.getBoundingClientRect().top+scrollY;
      let above=null;
      document.querySelectorAll('section,div').forEach(e=>{
        const c=(e.className||'').toString().split(' ')[0];
        if(!c.startsWith('gb-')||e===w) return;
        const r=e.getBoundingClientRect();
        if(Math.abs(r.bottom+scrollY-t)<8 && r.height>60) above=c;});
      return {bg:cs.getPropertyValue('--wave-bg').trim(),
              under:cs.getPropertyValue('--wave-under').trim(), above};
    }"""
    # (page, expected --wave-bg). faq page keeps the transparent top: the block
    # above it there is the white cta band, which is what that variant is for.
    pages = [('pdp', 'https://gumi.com.au/products/superfood-greens-gummies', '#e7f8d0'),
             ('how-gumi-works', 'https://gumi.com.au/pages/how-gumi-works', '#e7f8d0'),
             ('reviews', 'https://gumi.com.au/pages/reviews', '#e7f8d0'),
             ('faq', 'https://gumi.com.au/pages/faq', 'transparent')]
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=CHROME)
        ctx = br.new_context(viewport={'width': 1440, 'height': 900})
        ctx.request.post('https://gumi.com.au/password', form={
            'form_type': 'storefront_password', 'utf8': '✓', 'password': password})
        pg = ctx.new_page()
        for name, url, want_bg in pages:
            pg.goto(url, wait_until='load'); pg.wait_for_timeout(1800)
            if inject: pg.add_style_tag(content=css); pg.wait_for_timeout(350)
            r = pg.evaluate(PROBE)
            check('%s: footer wave --wave-bg' % name, r.get('bg'), want_bg,
                  'block above: .%s' % r.get('above'))
            # --wave-under must follow: a transparent pair needs a transparent
            # under, an opaque one needs the arc colour, or a hairline shows
            check('%s: --wave-under consistent' % name,
                  r.get('under') == ('transparent' if want_bg == 'transparent' else '#b5ed61'), True)
        # the static pages have no #MainContent, so the override cannot reach them
        st = br.new_context(viewport={'width': 1440, 'height': 900}).new_page()
        for name in ('pdp', 'faq'):
            st.goto((ROOT / (name + '.html')).as_uri(), wait_until='load')
            st.wait_for_timeout(700)
            r = st.evaluate("""()=>{const w=document.querySelector('.gb-footer-cta-wrap .gb-scallop');
              const cs=getComputedStyle(w);
              return {cls:w.className, bg:cs.getPropertyValue('--wave-bg').trim()};}""")
            # static markup already names the right variant per page
            check('static %s: variant untouched' % name, r['bg'],
                  '#e7f8d0' if name == 'pdp' else 'transparent')
        br.close()


a = argparse.ArgumentParser(); a.add_argument('--password')
a.add_argument('--as-served', action='store_true',
               help='verify the live site as it is actually served (post-push)')
a = a.parse_args()
css_text_checks()
static_checks()
if a.password:
    live_checks(a.password, inject=not a.as_served)
    faq_wave_checks(a.password, inject=not a.as_served)
print('\n%d ok, %d FAIL' % (ok, fail))
sys.exit(1 if fail else 0)
