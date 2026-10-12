#!/usr/bin/env python3
"""Round 119, static side.

  python3 tools/r119check.py

1  $build.
2  .gb-cart__gift-media clips to 4px.
3  enquiryPrefill still selects from ?type= after the selector change, and the
   button the select box draws opens on that option.
4  Guard: the old #enquiry id is what the static page has, so this side can
   never prove the live fix by itself -- assert the NEW selector is what the
   code now runs, and that it matches both name shapes.
"""
import pathlib, sys
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
ok = red = 0


def grade(cond, label, detail=''):
    global ok, red
    if cond:
        ok += 1; print(f'  ok   {label}   {detail}')
    else:
        red += 1; print(f'  RED  {label}   {detail}')


css = (ROOT / 'assets/customstyle.css').read_text(encoding='utf-8')
js = (ROOT / 'assets/main.js').read_text(encoding='utf-8')

print('--- 1. $build ---')
# >=, never ==: a pinned build turns this red in every later round and reads as a
# regression. Same trap HANDOFF logged for r116/r117 -- r119 shipped with it anyway.
import re as _re
_b = _re.search(r'--build: "(\d{8})-r(\d+)"', css)
grade(bool(_b) and (_b.group(1), int(_b.group(2))) >= ('20260908', 119),
      '$build >= 20260908-r119  (got %s)' % (_b.group(0) if _b else 'none'))

print('--- 4. prefill selector shape ---')
grade('form.querySelector(\n        \'select[name="enquiry"], select[name="contact[enquiry]"]\')' in js
      or 'select[name="enquiry"], select[name="contact[enquiry]"]' in js,
      'new selector present')
grade('form.querySelector("#enquiry")' not in js, 'old #enquiry lookup gone')

PROBE_GIFT = """() => {
  const e = document.querySelector('.gb-cart__gift-media');
  if (!e) return 'ABSENT';
  const cs = getComputedStyle(e);
  return {r: cs.borderTopLeftRadius, o: cs.overflowX + '/' + cs.overflowY};
}"""

PROBE_SEL = """() => {
  const s = document.querySelector('#enquiry');
  // ⚠ the enquiry box's own button: a bare .gb-select__button hits the phone
  // field's country code, which is the first select box on the page.
  const wrap = s && s.closest('.gb-select');
  const btn = wrap && wrap.querySelector('.gb-select__button');
  return {idx: s ? s.selectedIndex : -1,
          val: s ? s.options[s.selectedIndex].value : null,
          btn: btn ? btn.textContent.trim() : '(no button)'};
}"""

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=CHROME)
    pg = b.new_context(viewport={'width': 1440, 'height': 900}).new_page()

    print('--- 2. .gb-cart__gift-media ---')
    for name in ('get-in-touch.html', 'faq.html'):
        pg.goto((ROOT / name).as_uri(), wait_until='load', timeout=60000)
        pg.wait_for_timeout(500)
        d = pg.evaluate(PROBE_GIFT)
        if d == 'ABSENT':
            grade(False, f'{name}: gift media present', 'ABSENT'); continue
        grade(d['r'] == '4px', f'{name}: border-radius', d['r'])
        grade(d['o'] == 'hidden/hidden', f'{name}: overflow', d['o'])

    print('--- 3. ?type= still preselects (static) ---')
    for q, want_idx, want_val in (('?type=press', 2, 'press'),
                                  ('?type=careers', 3, 'careers'),
                                  ('?type=partners', 1, 'partners'),
                                  ('', 0, 'contact'),
                                  ('?type=nonsense', 0, 'contact')):
        pg.goto((ROOT / 'get-in-touch.html').as_uri() + q, wait_until='load', timeout=60000)
        pg.wait_for_timeout(600)
        d = pg.evaluate(PROBE_SEL)
        grade(d['idx'] == want_idx, f"{q or '(no query)':<16} select index", f"got={d['idx']} val={d['val']} want={want_idx}")
        if q == '?type=press':
            grade('Press' in d['btn'], '?type=press  button shows the preselected option', d['btn'])
    b.close()

print(f'\n{ok} ok / {red} red')
sys.exit(1 if red else 0)
