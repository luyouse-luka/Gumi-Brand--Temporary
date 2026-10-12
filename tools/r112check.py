#!/usr/bin/env python3
"""r112, graded on the static build.

  python3 tools/r112check.py

1  .gb-promo-panel__logo sizes an <img> the same way it sizes the <svg>.
2  An invisible hCaptcha container costs the flex forms no gap.
3  A viewport too short for the mobile panel scrolls it instead of clipping.

⚠ 1 and 2 inject the element the live theme produces (settings.logo turns the
  logo into an <img>; Shopify appends the h-captcha div on first focus). The
  static build has neither, so these grade the RULE, not the page -- the live
  DOM is graded by tools/r112live.py.
"""
import pathlib, sys
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
ok = red = 0

# 124x32 is what snippets/gb-logo.liquid stamps on the real <img>.
LOGO_SVG = ('data:image/svg+xml;utf8,'
            "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 124 32' "
            "width='124' height='32'><rect width='124' height='32'/></svg>")

OPEN = """() => { const m = document.getElementById('promo-modal');
  if (!m) return false;
  m.classList.add('is-open'); m.setAttribute('aria-hidden', 'false'); return true; }"""

# What Shopify's captcha-bootstrap actually appends, measured on live:
# a 0-height div holding an iframe and the response textarea.
INJECT_CAPTCHA = """(sel) => {
  const f = document.querySelector(sel);
  if (!f) return null;
  const before = +f.getBoundingClientRect().height.toFixed(2);
  const d = document.createElement('div');
  d.className = 'h-captcha';
  d.setAttribute('data-sitekey', 'x');
  d.setAttribute('data-size', 'invisible');
  d.innerHTML = '<iframe style="display:none"></iframe>'
              + '<textarea name="h-captcha-response" style="display:none"></textarea>';
  f.appendChild(d);
  const after = +f.getBoundingClientRect().height.toFixed(2);
  const cs = getComputedStyle(d);
  return {before, after, gap: getComputedStyle(f).rowGap,
          pos: cs.position, disp: cs.display,
          rendered: cs.display !== 'none' && cs.visibility !== 'hidden'};
}"""

PANEL = """() => {
  const q = s => document.querySelector(s);
  const panel = q('.gb-promo-panel'), content = q('.gb-promo-panel__content');
  const art = q('.gb-promo-panel__art');
  const btn = q('[data-promo-panel="email"] .gb-promo-panel__submit');
  const scrollable = e => +(e.scrollHeight - e.clientHeight).toFixed(1);
  // overflow:hidden is programmatically scrollable but NOT by the user, so the
  // computed value has to be graded alongside the numbers.
  const user = e => ['auto', 'scroll', 'overlay'].includes(getComputedStyle(e).overflowY);
  const bottomOf = e => +e.getBoundingClientRect().bottom.toFixed(1);
  const out = {vh: innerHeight,
    panelOvY: getComputedStyle(panel).overflowY,
    panelOvX: getComputedStyle(panel).overflowX,
    panelScroll: scrollable(panel), panelUser: user(panel),
    panelH: +panel.getBoundingClientRect().height.toFixed(1),
    contentScroll: scrollable(content), contentUser: user(content),
    artBottomAt0: bottomOf(art), btnBottomAt0: bottomOf(btn)};
  const sc = user(panel) ? panel : (user(content) ? content : null);
  if (sc) { sc.scrollTop = 99999;
            out.artBottomAtEnd = bottomOf(art);
            out.btnBottomAtEnd = bottomOf(btn);
            sc.scrollTop = 0; }
  return out;
}"""


def grade(cond, label, detail=''):
    global ok, red
    if cond:
        ok += 1
    else:
        red += 1
        print(f'  RED  {label}   {detail}')


def main():
    global ok, red
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME)
        ctx = b.new_context(viewport={'width': 1440, 'height': 900})
        pg = ctx.new_page()

        print('--- 1. promo logo, <svg> and <img> alike ---')
        pg.goto((ROOT / 'index.html').as_uri())
        pg.wait_for_timeout(300)
        pg.evaluate(OPEN)
        m = pg.evaluate("""(src) => {
          const sp = document.querySelector('.gb-promo-panel__logo');
          const r = e => { const b = e.getBoundingClientRect();
                           return [+b.width.toFixed(1), +b.height.toFixed(1)]; };
          const svg = r(sp.firstElementChild);
          const img = document.createElement('img');
          img.src = src; img.width = 124; img.height = 32;
          sp.innerHTML = ''; sp.appendChild(img);
          return new Promise(res => { img.onload = img.onerror = () => setTimeout(
            () => res({svg, img: r(img), h: getComputedStyle(img).height,
                       w: getComputedStyle(img).width,
                       row: +document.querySelector('.gb-promo-panel__head')
                              .getBoundingClientRect().height.toFixed(1)}), 60); });
        }""", LOGO_SVG)
        grade(m['svg'] == [93, 24], 'the inline <svg> still measures 93x24', str(m['svg']))
        grade(m['img'] == [93, 24], 'an <img> measures 93x24 too, not 124x32', str(m['img']))
        grade(m['row'] == 64, 'the head row stays 64', str(m['row']))
        print(f"  svg {m['svg']}  img {m['img']}  head {m['row']}")

        print('--- 2. invisible hCaptcha costs no gap ---')
        for page, sel, want_gap in (('get-in-touch.html', '.gb-form', '32px'),
                                    ('index.html', '.gb-promo-panel__form', '12px')):
            pg.goto((ROOT / page).as_uri())
            pg.wait_for_timeout(300)
            pg.evaluate(OPEN)
            m = pg.evaluate(INJECT_CAPTCHA, sel)
            grade(m is not None, f'{page} {sel} exists')
            if not m:
                continue
            grade(m['gap'] == want_gap, f'{page}: the form still spaces by gap', m['gap'])
            grade(m['after'] == m['before'],
                  f'{page}: the form is no taller for it',
                  f"{m['before']} -> {m['after']} (+{round(m['after'] - m['before'], 2)})")
            grade(m['pos'] == 'absolute', f'{page}: the container is out of flow', m['pos'])
            grade(m['rendered'], f'{page}: and still rendered, so a challenge can open',
                  f"display {m['disp']}")
            print(f"  {page:<20} {m['before']} -> {m['after']}   {m['pos']}")

        print('--- 3. short viewports scroll the panel ---')
        for w, h in ((390, 844), (390, 640), (390, 500), (390, 400), (390, 320),
                     (1440, 900), (1440, 460)):
            pg.set_viewport_size({'width': w, 'height': h})
            pg.goto((ROOT / 'index.html').as_uri())
            pg.wait_for_timeout(300)
            pg.evaluate(OPEN)
            pg.wait_for_timeout(120)
            m = pg.evaluate(PANEL)
            mobile = w <= 767
            # 460 content + 252 art: the mobile card's own height, board-measured.
            need = max(0, 712 - h) if mobile else 0
            if mobile:
                grade(m['panelUser'], f'{w}x{h}: the panel is user-scrollable',
                      f"overflow-y {m['panelOvY']}")
                grade(m['panelOvX'] == 'hidden', f'{w}x{h}: and still clips sideways',
                      m['panelOvX'])
                grade(abs(m['panelScroll'] - need) <= 1.5,
                      f'{w}x{h}: it scrolls exactly the overhang',
                      f"{m['panelScroll']} vs {need}")
                grade(m['contentScroll'] == 0,
                      f'{w}x{h}: the content column is not a second scroller',
                      f"scrollable by {m['contentScroll']}")
                if need:
                    grade(m.get('artBottomAtEnd', 1e9) <= h + 1,
                          f'{w}x{h}: scrolling to the end reveals the bears',
                          f"art bottom {m.get('artBottomAtEnd')} vs {h}")
                    grade(m.get('btnBottomAtEnd', 1e9) <= h + 1,
                          f'{w}x{h}: and the submit button is reachable',
                          f"button bottom {m.get('btnBottomAtEnd')} vs {h}")
                else:
                    grade(m['artBottomAt0'] <= h + 1,
                          f'{w}x{h}: nothing to scroll, the card fits',
                          f"art bottom {m['artBottomAt0']}")
            else:
                # Desktop is a row -- the content column stays the scroller.
                grade(m['panelScroll'] == 0, f'{w}x{h}: the desktop panel has no overhang',
                      str(m['panelScroll']))
                grade(m['contentUser'], f'{w}x{h}: its content column still scrolls itself')
                # 768-1280 scales the card by --pp-k, so a short viewport does not
                # always cap it -- only assert an overhang where it did.
                if m['panelH'] >= h - 48 - 0.5:
                    grade(m['contentScroll'] > 0,
                          f'{w}x{h}: and has something to scroll', str(m['contentScroll']))
                grade(m.get('btnBottomAtEnd', 1e9) <= h + 1,
                      f'{w}x{h}: the submit button is reachable',
                      f"button bottom {m.get('btnBottomAtEnd')} vs {h}")
            print(f"  {w}x{h:<5} panel {m['panelOvY']:<7} scroll {m['panelScroll']:<7} "
                  f"content {m['contentScroll']:<7} art@end {m.get('artBottomAtEnd', '-')}")
        b.close()
    print(f'\n{ok} ok / {red} red')
    return 1 if red else 0


sys.exit(main())
