#!/usr/bin/env python3
"""Round 116, static side.

  python3 tools/r116check.py

1  $build reached the compiled sheet.
2  The hairline rule is in the artifact AND is a selector the browser accepts.
   :has() is silently dropped when malformed -- the rule stays visible in the
   stylesheet and simply never applies, so grep alone proves nothing. matches()
   throws on an invalid selector, which is the only loud test.
3  The static site keeps the board's grey placeholder: it ships no <img> here,
   so :has(img) must NOT match and the background must stay #d9d9d9.
4  Inject an <img> and the same element must drop to transparent -- that is the
   live condition, reproduced locally.

Round 116 tab order is graded by tools/menutab.py (section I).
"""
import pathlib, sys
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
ok = red = 0


def grade(cond, label, detail=''):
    global ok, red
    if cond:
        ok += 1
        print(f'  ok   {label}   {detail}')
    else:
        red += 1
        print(f'  RED  {label}   {detail}')


css = (ROOT / 'assets/customstyle.css').read_text(encoding='utf-8')
print('--- 1/2. artifact ---')
# NOT pinned to r116: a literal build token turns this red on every later round
# and reads as a regression. What matters on a re-run is that the sheet is at
# least this round's build, not that it is exactly it.
import re as _re
_m = _re.search(r'--build: "(\d{8})-r(\d+)"', css)
grade(bool(_m) and (int(_m.group(1)), int(_m.group(2))) >= (20260908, 116),
      '$build is r116 or later', _m.group(0) if _m else 'no --build')
grade(css.count('.gb-highlight-card__media:has(img)') == 1,
      'hairline rule present exactly once',
      f'count={css.count(".gb-highlight-card__media:has(img)")}')

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=CHROME)
    pg = b.new_context(viewport={'width': 1440, 'height': 900}).new_page()
    pg.goto((ROOT / 'index.html').as_uri(), wait_until='domcontentloaded', timeout=60000)
    pg.wait_for_timeout(1200)

    valid = pg.evaluate("""() => {
        try { document.body.matches('.gb-highlight-card__media:has(img)'); return 'ok'; }
        catch (err) { return String(err); }
    }""")
    grade(valid == 'ok', 'the browser accepts :has(img) (not silently dropped)', valid)

    print('--- 3. static keeps the grey placeholder ---')
    st = pg.evaluate("""() => {
        const m = [...document.querySelectorAll('.gb-highlight-card__media')];
        return {n: m.length,
                withImg: m.filter(x => x.querySelector('img')).length,
                bgs: [...new Set(m.map(x => getComputedStyle(x).backgroundColor))]};
    }""")
    grade(st['n'] >= 3, 'index has the highlight cards', f"n={st['n']}")
    grade(st['withImg'] == 0, 'and none of them ships an <img>', f"withImg={st['withImg']}")
    grade(st['bgs'] == ['rgb(217, 217, 217)'],
          'so every one keeps the board grey #d9d9d9', str(st['bgs']))

    print('--- 4. live condition, reproduced ---')
    after = pg.evaluate("""() => {
        const m = document.querySelector('.gb-highlight-card__media');
        const before = getComputedStyle(m).backgroundColor;
        const img = document.createElement('img');
        img.src = 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7';
        m.appendChild(img);
        const now = getComputedStyle(m).backgroundColor;
        img.remove();
        return {before, now, restored: getComputedStyle(m).backgroundColor};
    }""")
    grade(after['before'] == 'rgb(217, 217, 217)', 'grey before the <img>', after['before'])
    grade(after['now'] == 'rgba(0, 0, 0, 0)',
          'transparent once an <img> is inside -- the hairline source is gone',
          after['now'])
    grade(after['restored'] == 'rgb(217, 217, 217)',
          'and grey again when it is removed (rule is live, not cached)',
          after['restored'])
    b.close()

print(f'\n{ok} ok / {red} red')
sys.exit(1 if red else 0)
