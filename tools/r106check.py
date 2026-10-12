#!/usr/bin/env python3
"""r106: the nine asks that can be judged on the static build.

  python3 tools/r106check.py
  python3 tools/r106check.py --reverse <n>    # undo ask n in the page, expect red

Ask 9 (/collections/all) is live-only -- its hook is theme.liquid's data-template
and there is no static counterpart; tools/r106live.py covers it after the push.

--reverse is the self-check: each number puts the pre-r106 value back through the
CSSOM and the assertions for that ask must turn red. A judge that stays green
under reversal is reading something the change never touched.
"""
import argparse, sys
from playwright.sync_api import sync_playwright

CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
BASE = 'file:///home/ly/project/Gumi-Brand/'

# Each reversal is written as CSS appended at the end of the cascade, at a
# specificity that beats the rule it undoes.
REVERSE = {
    1: '@media(min-width:1281px){.gb-page-hero--center.gb-page-hero--center{padding-top:64px}}'
       '@media(min-width:768px) and (max-width:1280px){.gb-page-hero--center.gb-page-hero--center'
       '{padding-top:clamp(32px,32px + 32*(100vw - 768px)/513,64px)}}',
    3: '.gb-form__check a.gb-form__check-a,.gb-form__check a{color:#011307}',
    4: '.gb-field__phone input::placeholder{color:rgb(117,117,117)}',
    6: '.gb-select.gb-select.gb-select.gb-select .gb-select__option'
       '[aria-selected="true"]::after{content:none}',
    7: '@media(max-width:767px){.gb-nav-card__art.gb-nav-card__art{width:100%}}',
    8: '.gb-cart-item__media.gb-cart-item__media{border-radius:0;overflow:visible}'
       '.gb-cart-item__media img{object-fit:cover}',
    10: ':where(section,div,footer):has(+ * > .gb-scallop--edge-top){--sc-res:0px}'
        ':where(section,div,footer):has(+ * > .gb-scallop--edge-top.gb-scallop--lg){--sc-res:0px}',
}

ok = red = 0


def grade(c, label, detail=''):
    global ok, red
    if c:
        ok += 1
    else:
        red += 1
        print(f'  RED  {label}   {detail}')


def near(a, b, tol=0.6):
    return abs(a - b) <= tol


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--reverse', type=int, choices=sorted(REVERSE) + [2])
    a = ap.parse_args()
    css = REVERSE.get(a.reverse)

    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=CHROME)
        ctx = br.new_context(viewport={'width': 1440, 'height': 900})
        pg = ctx.new_page()

        def go(page, w=1440):
            pg.set_viewport_size({'width': w, 'height': 900})
            pg.goto(BASE + page + '.html', wait_until='domcontentloaded')
            pg.wait_for_timeout(500)
            if css:
                pg.add_style_tag(content=css)
                pg.wait_for_timeout(120)

        # --- liveness: the page and the stylesheet are actually there ---------
        go('faq')
        grade(pg.evaluate("() => getComputedStyle(document.documentElement)"
                          ".getPropertyValue('--build').trim()") == '"20260908-r106"',
              'liveness: the page is running the r106 stylesheet',
              pg.evaluate("() => getComputedStyle(document.documentElement).getPropertyValue('--build')"))

        # --- 1. --center padding-top: 80 desktop, 32 mobile ------------------
        print('--- 1. .gb-page-hero--center padding-top ---')
        for w, want in ((1440, 80.0), (1281, 80.0), (768, 32.0), (390, 32.0)):
            go('faq', w)
            got = pg.evaluate("() => parseFloat(getComputedStyle("
                              "document.querySelector('.gb-page-hero--center')).paddingTop)")
            grade(near(got, want), f'{w}: padding-top {want}', f'got {got}')
            print(f'  {w:>5}  padding-top {got}')
        go('index')
        grade(pg.evaluate("() => document.querySelector('.gb-page-hero--center')") is None,
              'index has no --center hero (the change is scoped to the text pages)')

        # --- 3. consent link colour ------------------------------------------
        print('--- 3. .gb-form__check a ---')
        go('get-in-touch')
        got = pg.evaluate("() => getComputedStyle(document.querySelector('.gb-form__check a')).color")
        grade(got == 'rgb(101, 101, 101)', 'link is #656565', f'got {got}')
        lab = pg.evaluate("() => getComputedStyle(document.querySelector('.gb-form__check')).color")
        grade(lab == got, 'link matches the label it sits in', f'label {lab} vs link {got}')
        print(f'  link {got}   label {lab}')

        # --- 4. phone placeholder --------------------------------------------
        print('--- 4. .gb-field__phone placeholder ---')
        pair = pg.evaluate("""() => {
          const ph = s => getComputedStyle(document.querySelector(s), '::placeholder').color;
          return [ph('.gb-field__phone input'),
                  ph('.gb-field__input:not(.gb-field__input--area)')];
        }""")
        grade(pair[0] == pair[1], 'phone placeholder matches the other inputs',
              f'phone {pair[0]} vs other {pair[1]}')
        grade(pair[0] == 'rgb(102, 102, 102)', 'and both are $c-gray-600', f'got {pair[0]}')
        print(f'  phone {pair[0]}   other {pair[1]}')

        # --- 6. the check on the chosen row ----------------------------------
        print('--- 6. enquiry dropdown check ---')
        rows = pg.evaluate("""() => {
          const s = [...document.querySelectorAll('.gb-select')]
            .find(el => (el.querySelector('select') || {}).name === 'enquiry');
          const btn = s.querySelector('.gb-select__button');
          btn.click();
          const out = [...s.querySelectorAll('.gb-select__option')].map(o => {
            const af = getComputedStyle(o, '::after');
            const r = o.getBoundingClientRect();
            return {t: o.textContent.trim(), sel: o.getAttribute('aria-selected'),
                    content: af.content, w: af.width, h: af.height,
                    right: +(r.right - o.getBoundingClientRect().right).toFixed(1)};
          });
          btn.click();
          return out;
        }""")
        selected = [r for r in rows if r['sel'] == 'true']
        others = [r for r in rows if r['sel'] != 'true']
        grade(len(selected) == 1, 'exactly one row is selected', f'{len(selected)}')
        grade(bool(selected) and selected[0]['content'] not in ('none', 'normal'),
              'the selected row draws a check',
              selected[0]['content'] if selected else 'no selected row')
        grade(bool(selected) and selected[0]['w'] == '20px' and selected[0]['h'] == '20px',
              'the check is the board\'s 20x20 box',
              f"{selected[0]['w']} x {selected[0]['h']}" if selected else '')
        grade(all(r['content'] in ('none', 'normal') for r in others),
              'no other row draws one',
              str([r['content'] for r in others]))
        for r in rows:
            print(f"  {r['t']:<24} selected={r['sel']:<5} check={r['content']} {r['w']}x{r['h']}")
        bare = pg.evaluate("""() => {
          const s = document.querySelector('.gb-select--bare');
          if (!s) return 'absent';
          const o = s.querySelector('.gb-select__option');
          return o ? getComputedStyle(o, '::after').content : 'no option';
        }""")
        grade(bare in ('none', 'normal', 'absent'),
              'the phone country code (--bare) does not get one', f'got {bare}')

        # --- 7. nav card art back to the board's 135.2% ----------------------
        print('--- 7. .gb-nav-card__art on mobile ---')
        go('index', 390)
        art = pg.evaluate("""() => {
          document.querySelector('.gb-header__toggle').click();
          return new Promise(r => setTimeout(() => {
            const c = document.querySelector('.gb-nav-card');
            const a = c.querySelector('.gb-nav-card__art');
            const cr = c.getBoundingClientRect(), ar = a.getBoundingClientRect();
            r({card: +cr.width.toFixed(2), art: +ar.width.toFixed(2),
               dx: +(ar.left - cr.left).toFixed(2), dy: +(ar.top - cr.top).toFixed(2),
               clipped: getComputedStyle(c).overflow});
          }, 600));
        }""")
        # 283:14915 draws it 228.43 x 275.77 at (37, 34) inside a 169 card.
        grade(near(art['art'], art['card'] * 1.352, 0.5),
              "art is the board's 135.2% of the card", f"{art['art']} vs {art['card'] * 1.352:.2f}")
        grade(near(art['art'], 228.43, 1.0), 'which is the board\'s 228.43', f"got {art['art']}")
        grade(near(art['dx'], 37.0, 1.0) and near(art['dy'], 34.0, 1.0),
              "offset is the board's (37, 34)", f"({art['dx']}, {art['dy']})")
        grade(art['clipped'] == 'hidden', 'the card clips it, as 283:14915 does',
              art['clipped'])
        print(f"  card {art['card']}  art {art['art']} @ ({art['dx']}, {art['dy']})  overflow {art['clipped']}")

        # --- 8. cart line media ----------------------------------------------
        print('--- 8. .gb-cart-item__media ---')
        go('index')
        # The board ships a bare grey placeholder here, so the box has no child to
        # read object-fit off -- one is planted, or the fit assertion is vacuous
        # and stays green through any reversal.
        media = pg.evaluate("""() => {
          const m = document.querySelector('.gb-cart-item__media');
          const cs = getComputedStyle(m);
          let img = m.querySelector('img, video, picture'), planted = false;
          if (!img) { img = document.createElement('img'); m.appendChild(img); planted = true; }
          const fit = getComputedStyle(img).objectFit;
          if (planted) img.remove();
          return {radius: cs.borderRadius, overflow: cs.overflow, fit: fit};
        }""")
        grade(media['radius'] == '4px', 'radius 4px', media['radius'])
        grade(media['overflow'] == 'hidden', 'clips, so the radius reaches the image',
              media['overflow'])
        grade(media['fit'] == 'contain', 'object-fit contain', media['fit'])
        print(f"  radius {media['radius']}  overflow {media['overflow']}  fit {media['fit']}")

        # --- 10. the reservation the section above cannot see -----------------
        print('--- 10. --sc-res for an --edge-top wave ---')
        for w in (1440, 1024, 768, 390):
            go('index', w)
            m = pg.evaluate("""() => {
              const px = s => parseFloat(getComputedStyle(document.querySelector(s)).paddingBottom);
              const wv = s => { const e = document.querySelector(s);
                                return e ? +e.getBoundingClientRect().height.toFixed(2) : null; };
              const nut = document.querySelector('.gb-nutrition');
              const prod = document.querySelector('.gb-product');
              return {nutPadB: px('.gb-nutrition'), statPadB: px('.gb-stats'),
                      lgWave: wv('.gb-scallop--edge-top.gb-scallop--lg'),
                      smWave: wv('.gb-scallop--edge-top:not(.gb-scallop--lg)'),
                      seam: +(prod.getBoundingClientRect().top
                              - nut.getBoundingClientRect().bottom).toFixed(2),
                      bandBottom: +(document.querySelector('.gb-nutrition__band')
                                    .getBoundingClientRect().bottom
                                    - nut.getBoundingClientRect().bottom).toFixed(2)};
            }""")
            # nutrition: the wave's height, less the 9px the 390 board laps it over
            # the pack band (ramped to 0 by 1281).
            lap = 9.0 if w <= 767 else (0.0 if w >= 1281 else 9.0 * (1281 - w) / 513)
            want_nut = m['lgWave'] - 1 - lap          # -1: the hairline seam guard
            grade(near(m['nutPadB'], want_nut, 1.2),
                  f'{w}: .gb-nutrition reserves the wave below it',
                  f"padB {m['nutPadB']} vs wave {m['lgWave']} - lap {lap:.1f}")
            grade(m['nutPadB'] > 0, f'{w}: and it is not zero', str(m['nutPadB']))
            # stats: its own 120/88 ramp on top of the small wave
            own = 120.0 if w >= 1281 else (88.0 if w <= 767 else 88 + 32 * (w - 768) / 513)
            grade(near(m['statPadB'], own + m['smWave'] - 1, 1.5),
                  f'{w}: .gb-stats reserves the small wave',
                  f"padB {m['statPadB']} vs {own:.1f} + {m['smWave']} - 1")
            print(f"  {w:>5}  nutrition padB {m['nutPadB']:<8} (wave {m['lgWave']})   "
                  f"stats padB {m['statPadB']:<8} (wave {m['smWave']})")

        # --- 2. the message box opts out of Lenis ----------------------------
        print('--- 2. the message box scrolls itself ---')
        go('get-in-touch')
        pg.wait_for_timeout(400)
        if a.reverse == 2:
            pg.evaluate("() => document.querySelector('.gb-field__input--area')"
                        ".removeAttribute('data-lenis-prevent')")
        marked = pg.evaluate("""() => {
          const t = document.querySelector('.gb-field__input--area');
          return {prevent: t.hasAttribute('data-lenis-prevent'),
                  lenis: document.documentElement.classList.contains('lenis')};
        }""")
        grade(marked['lenis'], 'Lenis is running (otherwise the test proves nothing)')
        grade(marked['prevent'], 'the textarea carries data-lenis-prevent')
        # ⚠ mouse.move takes VIEWPORT coordinates. The form sits ~700px down, so
        # without this the pointer lands below the fold and the wheel goes to the
        # page no matter what the textarea says -- green and red both read alike.
        ta = pg.query_selector('.gb-field__input--area')
        ta.scroll_into_view_if_needed()
        pg.wait_for_timeout(700)
        pg.evaluate("""() => { const t = document.querySelector('.gb-field__input--area');
                               t.value = ('A long line of message copy. ').repeat(60); }""")
        box = ta.bounding_box()
        grade(box['y'] >= 0 and box['y'] + box['height'] <= 900,
              'the box is inside the viewport (or the wheel test is meaningless)',
              f"y {box['y']:.0f} h {box['height']:.0f}")
        pg.mouse.move(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2)
        before = pg.evaluate("() => [document.querySelector('.gb-field__input--area').scrollTop,"
                             " window.scrollY]")
        pg.mouse.wheel(0, 300)
        pg.wait_for_timeout(800)
        after = pg.evaluate("() => [document.querySelector('.gb-field__input--area').scrollTop,"
                            " window.scrollY]")
        grade(after[0] > before[0], 'the wheel scrolls the box', f'{before[0]} -> {after[0]}')
        grade(after[1] == before[1], 'and not the page behind it', f'{before[1]} -> {after[1]}')
        print(f'  textarea {before[0]} -> {after[0]}   window {before[1]} -> {after[1]}')

        br.close()
    print(f'\n{ok} ok / {red} red' + (f'   [reversed ask {a.reverse}]' if css else ''))
    return 1 if red else 0


if __name__ == '__main__':
    sys.exit(main())
