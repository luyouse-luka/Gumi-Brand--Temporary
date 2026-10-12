#!/usr/bin/env python3
"""r112 on live, where all three hooks only exist.

  python3 tools/r112live.py --password 1234 --preflight   # before the push
  python3 tools/r112live.py --password 1234               # after it

1  settings.logo is uploaded, so gb-logo.liquid renders an <img> in the promo
   head. The static build only ever shows the inline <svg>.
2  Shopify's captcha-bootstrap appends <div class="h-captcha" data-size=
   "invisible"> to the contact and customer forms on first focus. Nothing to see
   locally, and it is NOT :empty -- it holds an iframe and a textarea.
3  Short viewports on the live panel.

--preflight is a rehearsal, not a substitute. The shipped rule DROPS
max-height/overflow-y from the mobile content column; an appended copy cannot
delete a declaration, so the flag injects explicit resets instead. Rerun without
it after the push.
"""
import argparse, json, pathlib, re, sys
from playwright.sync_api import sync_playwright

CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
LIVE = 'https://gumi.com.au'
CSS = pathlib.Path(__file__).resolve().parent.parent / 'assets/customstyle.css'
ok = red = 0

OPEN = """() => { const m = document.getElementById('promo-modal');
  if (!m) return false;
  m.classList.add('is-open'); m.setAttribute('aria-hidden', 'false'); return true; }"""


def grade(cond, label, detail=''):
    global ok, red
    if cond:
        ok += 1
    else:
        red += 1
        print(f'  RED  {label}   {detail}')


def delta_css():
    """The r112 rules, cut out of the shipped file by their own selectors."""
    text = CSS.read_text(encoding='utf-8')
    want = ['.gb-promo-panel__logo svg,.gb-promo-panel__logo img{display:block;height:100%;width:auto}',
            '.h-captcha[data-size=invisible]{position:absolute}',
            '.gb-promo-panel{overflow:hidden auto}']
    for w in want:
        if w not in text:
            sys.exit(f'ABORT: not in assets/customstyle.css, recompile first:\n  {w}')
    return (want[0] + want[1]
            + '@media (max-width:767px){' + want[2]
            # the shipped rule removes these two; an appended copy has to
            # overwrite them by hand
            + '.gb-promo-panel__content{max-height:none;overflow-y:visible}}')


LOGO = """() => {
  const sp = document.querySelector('.gb-promo-panel__logo');
  if (!sp) return null;
  const kid = sp.firstElementChild;
  const r = e => { const b = e.getBoundingClientRect();
                   return [+b.width.toFixed(1), +b.height.toFixed(1)]; };
  return {tag: kid.tagName, box: r(kid), span: r(sp),
          nat: kid.tagName === 'IMG' ? [kid.naturalWidth, kid.naturalHeight] : null,
          head: +document.querySelector('.gb-promo-panel__head')
                  .getBoundingClientRect().height.toFixed(1),
          overflows: r(kid)[1] > r(sp)[1] + 0.5};
}"""

FORM = """(sel) => {
  const f = document.querySelector(sel);
  if (!f) return null;
  const cap = f.querySelector(':scope > .h-captcha');
  const cs = cap && getComputedStyle(cap);
  return {h: +f.getBoundingClientRect().height.toFixed(2),
          gap: getComputedStyle(f).rowGap,
          bound: f.dataset.hcaptchaBound === 'true',
          hasCap: !!cap, capKids: cap ? cap.children.length : null,
          capEmpty: cap ? (cap.children.length === 0 && !cap.textContent.trim()) : null,
          capPos: cs && cs.position, capDisp: cs && cs.display,
          capRendered: cs ? (cs.display !== 'none' && cs.visibility !== 'hidden') : null};
}"""

PANEL = """() => {
  const q = s => document.querySelector(s);
  const panel = q('.gb-promo-panel'), content = q('.gb-promo-panel__content');
  const art = q('.gb-promo-panel__art');
  const btn = q('[data-promo-panel="email"] .gb-promo-panel__submit');
  const s = e => +(e.scrollHeight - e.clientHeight).toFixed(1);
  const user = e => ['auto', 'scroll', 'overlay'].includes(getComputedStyle(e).overflowY);
  const bot = e => +e.getBoundingClientRect().bottom.toFixed(1);
  const out = {vh: innerHeight, panelOvY: getComputedStyle(panel).overflowY,
    panelOvX: getComputedStyle(panel).overflowX,
    panelScroll: s(panel), panelUser: user(panel),
    panelH: +panel.getBoundingClientRect().height.toFixed(1),
    contentScroll: s(content), contentUser: user(content),
    artBottomAt0: bot(art)};
  const sc = user(panel) ? panel : (user(content) ? content : null);
  if (sc) { sc.scrollTop = 99999; out.artEnd = bot(art); out.btnEnd = bot(btn); sc.scrollTop = 0; }
  return out;
}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--password', required=True)
    ap.add_argument('--preflight', action='store_true')
    a = ap.parse_args()
    css = delta_css() if a.preflight else None

    with sync_playwright() as pw:
        br = pw.chromium.launch(executable_path=CHROME)
        ctx = br.new_context(viewport={'width': 1440, 'height': 900})
        ctx.request.post(LIVE + '/password', form={
            'form_type': 'storefront_password', 'utf8': '✓', 'password': a.password})
        if not any(c['name'] == '_shopify_essential' for c in ctx.cookies()):
            sys.exit('storefront password rejected')
        pg = ctx.new_page()

        def go(path, w, h, open_modal=False):
            pg.set_viewport_size({'width': w, 'height': h})
            pg.goto(LIVE + path, wait_until='domcontentloaded', timeout=90000)
            pg.wait_for_timeout(1200)
            if css:
                pg.add_style_tag(content=css)
                pg.wait_for_timeout(150)
            if open_modal:
                grade(pg.evaluate(OPEN), f'{path}: #promo-modal is on the page')
                pg.wait_for_timeout(250)

        print('--- 1. the promo head logo is an <img> on live ---')
        for w, h in ((1440, 900), (390, 844)):
            go('/', w, h, True)
            m = pg.evaluate(LOGO)
            grade(m is not None, f'{w}: found .gb-promo-panel__logo')
            if not m:
                continue
            grade(m['tag'] == 'IMG', f'{w}: live really does render an <img>', m['tag'])
            grade(m['box'] == [93, 24], f'{w}: sized to 93x24 by the 24-tall row', str(m['box']))
            grade(not m['overflows'], f'{w}: it no longer overflows the row',
                  f"img {m['box']} in span {m['span']}")
            grade(m['head'] == 64, f'{w}: the head row is still 64', str(m['head']))
            print(f"  {w:>5}  {m['tag']} {m['box']} natural {m['nat']} head {m['head']}")

        print('--- 2. the invisible hCaptcha earns no gap ---')
        # focusin is what captcha-bootstrap listens for; the widget is not in the
        # DOM before that, which is why r109 could not measure it.
        cases = [('/pages/get-in-touch', '.gb-form', '.gb-form input[type=text]', '32px', False),
                 ('/', '.gb-promo-panel__form', '.gb-promo-panel__input', '12px', True)]
        for path, sel, focus, want_gap, modal in cases:
            go(path, 1440, 900, modal)
            before = pg.evaluate(FORM, sel)
            grade(before is not None, f'{path}: found {sel}')
            if not before:
                continue
            grade(not before['hasCap'], f'{path}: no captcha before focus')
            pg.focus(focus)
            pg.evaluate("(s)=>{const e=document.querySelector(s);"
                        "e.dispatchEvent(new Event('focusin',{bubbles:true}));"
                        "e.dispatchEvent(new Event('change',{bubbles:true}));}", focus)
            pg.wait_for_timeout(4500)
            after = pg.evaluate(FORM, sel)
            grade(after['bound'] and after['hasCap'],
                  f'{path}: hCaptcha did bind (else this proves nothing)',
                  json.dumps(after))
            if not after['hasCap']:
                continue
            grade(after['capEmpty'] is False,
                  f'{path}: and it is NOT :empty, so r109 could never have matched',
                  f"{after['capKids']} children")
            grade(after['gap'] == want_gap, f'{path}: the form still spaces by gap', after['gap'])
            grade(after['h'] == before['h'], f'{path}: the form is no taller for it',
                  f"{before['h']} -> {after['h']} (+{round(after['h'] - before['h'], 2)})")
            grade(after['capPos'] == 'absolute', f'{path}: the container is out of flow',
                  after['capPos'])
            grade(after['capRendered'],
                  f'{path}: and still rendered, so a challenge can open', after['capDisp'])
            print(f"  {path:<24} {before['h']} -> {after['h']}  {after['capPos']} "
                  f"kids {after['capKids']}")

        print('--- 3. short viewports scroll the panel ---')
        for w, h in ((390, 844), (390, 640), (390, 500), (390, 400), (390, 320),
                     (768, 500), (1440, 900), (1440, 460)):
            go('/', w, h, True)
            m = pg.evaluate(PANEL)
            mobile = w <= 767
            need = max(0, 712 - h) if mobile else 0
            if mobile:
                grade(m['panelUser'], f'{w}x{h}: the panel is user-scrollable', m['panelOvY'])
                grade(m['panelOvX'] == 'hidden', f'{w}x{h}: and still clips sideways', m['panelOvX'])
                grade(abs(m['panelScroll'] - need) <= 1.5,
                      f'{w}x{h}: it scrolls exactly the overhang',
                      f"{m['panelScroll']} vs {need}")
                grade(m['contentScroll'] == 0,
                      f'{w}x{h}: no second, nested scroller', str(m['contentScroll']))
                if need:
                    grade(m.get('artEnd', 1e9) <= h + 1, f'{w}x{h}: the bears come into view',
                          f"art bottom {m.get('artEnd')} vs {h}")
                    grade(m.get('btnEnd', 1e9) <= h + 1, f'{w}x{h}: the button is reachable',
                          f"button bottom {m.get('btnEnd')} vs {h}")
            else:
                grade(m['panelScroll'] == 0, f'{w}x{h}: the desktop panel has no overhang',
                      str(m['panelScroll']))
                grade(m['contentUser'], f'{w}x{h}: its content column is still the scroller')
                # 768-1280 scales the whole card by --pp-k, so a short viewport
                # does not necessarily cap it -- only assert an overhang where
                # the panel actually ran into max-height.
                capped = m['panelH'] >= h - 48 - 0.5
                if capped:
                    grade(m['contentScroll'] > 0, f'{w}x{h}: with something to scroll',
                          str(m['contentScroll']))
                grade(min(m.get('btnEnd', 1e9), m['artBottomAt0']) <= h + 1,
                      f'{w}x{h}: the button is reachable', f"button bottom {m.get('btnEnd')} vs {h}")
            print(f"  {w}x{h:<5} panel {m['panelOvY']:<7} scroll {m['panelScroll']:<7} "
                  f"content {m['contentScroll']:<7} art@end {m.get('artEnd', '-')}")
        br.close()
    tag = '   [PREFLIGHT: rules injected, not pushed]' if a.preflight else ''
    print(f'\n{ok} ok / {red} red{tag}')
    return 1 if red else 0


sys.exit(main())
