#!/usr/bin/env python3
"""Round 119, live side -- the two asks that only exist on live.

  python3 tools/r119live.py --password 1234 --preflight   # before the push
  python3 tools/r119live.py --password 1234               # after it

1  /collections/all: nothing visible is left on Horizon's Inter.
   Guard: without the delta, the same sweep must find some -- otherwise the
   assertion is green because the sweep is blind, not because the fix landed.
3  ?type=press preselects on the live contact form, whose select id is
   section-suffixed. Guard: the shipped main.js must FAIL the same check.
"""
import argparse, pathlib, re, sys
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
LIVE = 'https://gumi.com.au'
ok = red = 0


def grade(cond, label, detail=''):
    global ok, red
    if cond:
        ok += 1; print(f'  ok   {label}   {detail}')
    else:
        red += 1; print(f'  RED  {label}   {detail}')


def delta_css():
    """The font-var block as it compiled -- what the push will actually ship."""
    css = (ROOT / 'assets/customstyle.css').read_text(encoding='utf-8')
    m = re.search(r'(#MainContent\[data-template\^=collection\] \{.*?\n\})', css, re.S)
    if not m:
        sys.exit('ABORT: the collection block is not in assets/customstyle.css -- recompile')
    block = m.group(1)
    if '--font-h6--family' not in block:
        sys.exit('ABORT: the r119 font vars are not in the compiled block -- recompile')
    return block


# Every visible text element still off the brand face.
STRAY = """() => {
  const stray = [];
  const walk = e => { for (const c of e.children) walk(c);
    if (![...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) return;
    const r = e.getBoundingClientRect(); if (!r.width || !r.height) return;
    const cs = getComputedStyle(e); if (cs.visibility === 'hidden') return;
    if (!/PP Palma/.test(cs.fontFamily)) stray.push({
      ff: cs.fontFamily.split(',')[0],
      cls: (typeof e.className === 'string' ? e.className : '').trim().replace(/\\s+/g, '.').slice(0, 46),
      txt: e.textContent.trim().slice(0, 22)}); };
  walk(document.querySelector('#MainContent') || document.body);
  return stray;
}"""

# The h1/grid work r106-r117 did must not move.
KEEP = """() => {
  const g = s => { const e = document.querySelector(s); if (!e) return null;
    const cs = getComputedStyle(e); const r = e.getBoundingClientRect();
    return {ff: cs.fontFamily.split(',')[0], fs: cs.fontSize, fw: cs.fontWeight,
            l: Math.round(r.left)}; };
  return {h1: g('#MainContent h1'), title: g('.product-card__content a.contents p')};
}"""

PREFILL = """() => {
  const s = document.querySelector('select[name="contact[enquiry]"], select[name="enquiry"]');
  if (!s) return 'NO SELECT';
  const wrap = s.closest('.gb-select');
  const btn = wrap && wrap.querySelector('.gb-select__button');
  return {id: s.id, name: s.name, idx: s.selectedIndex,
          val: s.options[s.selectedIndex] && s.options[s.selectedIndex].value,
          btn: btn ? btn.textContent.trim() : '(no button)',
          oldIdWouldMatch: !!document.querySelector('#enquiry')};
}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--password', required=True)
    ap.add_argument('--preflight', action='store_true',
                    help='inject the not-yet-pushed css/js instead of reading what is live')
    a = ap.parse_args()
    css = delta_css() if a.preflight else None
    js = (ROOT / 'assets/main.js').read_text(encoding='utf-8') if a.preflight else None

    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME)
        ctx = b.new_context(viewport={'width': 1440, 'height': 900})
        ctx.request.post(LIVE + '/password', form={
            'form_type': 'storefront_password', 'utf8': '✓', 'password': a.password})
        if not any(c['name'] == '_shopify_essential' for c in ctx.cookies()):
            sys.exit('storefront password rejected')

        print('=== 1. /collections/all: no element left on Inter ===')
        for w in (1440, 390):
            pg = ctx.new_page(); pg.set_viewport_size({'width': w, 'height': 900})
            pg.goto(LIVE + '/collections/all', wait_until='load'); pg.wait_for_timeout(2200)
            before = pg.evaluate(STRAY)
            keep_before = pg.evaluate(KEEP)
            if css:
                # guard first: a sweep that finds nothing BEFORE the delta proves nothing
                grade(len(before) > 0, f'@{w} sweep sees the problem without the delta (guard)',
                      f'{len(before)} stray')
                pg.add_style_tag(content=css); pg.wait_for_timeout(400)
            after = pg.evaluate(STRAY)
            keep = pg.evaluate(KEEP)
            grade(len(after) == 0, f'@{w} nothing left on a non-brand face',
                  '0 stray' if not after else f'{len(after)}: ' + '; '.join(
                      f"{s['ff']}|{s['cls']}|{s['txt']}" for s in after))
            for k in ('h1', 'title'):
                if not keep[k]:
                    grade(False, f'@{w} {k} present', 'MISSING'); continue
                grade(keep[k] == keep_before[k], f'@{w} {k} untouched by this round',
                      f"{keep[k]['ff']} {keep[k]['fs']}/{keep[k]['fw']} left={keep[k]['l']}")
            pg.close()

        print('=== 3. ?type=press on the live contact form ===')
        # baseline: whatever main.js is live right now
        pg = ctx.new_page()
        pg.goto(LIVE + '/pages/get-in-touch?type=press', wait_until='load')
        pg.wait_for_timeout(2200)
        shipped = pg.evaluate(PREFILL)
        pg.close()
        if a.preflight:
            grade(shipped != 'NO SELECT' and shipped['val'] != 'press',
                  'shipped main.js does NOT preselect (guard)',
                  f"idx={shipped.get('idx')} val={shipped.get('val')}")
            grade(shipped != 'NO SELECT' and shipped['oldIdWouldMatch'] is False,
                  'the old #enquiry id does not exist on live (root cause)',
                  f"live id={shipped.get('id')}")
            pg = ctx.new_page()
            pg.route('**/assets/main.js*', lambda r: r.fulfill(
                status=200, content_type='text/javascript; charset=utf-8', body=js))
            pg.goto(LIVE + '/pages/get-in-touch?type=press', wait_until='load')
            pg.wait_for_timeout(2200)
            d = pg.evaluate(PREFILL); pg.close()
        else:
            d = shipped
        if d == 'NO SELECT':
            grade(False, 'enquiry select found on live', 'NO SELECT')
        else:
            grade(d['val'] == 'press', 'select lands on press', f"idx={d['idx']} val={d['val']} id={d['id']}")
            grade('Press' in d['btn'], 'the box button shows it', d['btn'])
        b.close()

    print(f'\n{ok} ok / {red} red')
    sys.exit(1 if red else 0)


main()
