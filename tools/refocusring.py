#!/usr/bin/env python3
"""A control that only has focus because a close handed it back must not look focused.

  python3 tools/refocusring.py
  python3 tools/refocusring.py --live --password 1234
  python3 tools/refocusring.py --strip     # inverted: drop the class, must go RED

Client r121: "Escape 关闭弹窗后，触发的按钮上出现 focus-visible 样式" -- Escape and
close buttons return focus with .focus(), which KEEPS whatever :focus-visible state
came before it, so the trigger paints its focus treatment though the user never
tabbed to it. main.js marks that one return with .is-refocused and CSS drops the
treatment; the mark clears on the next real key or blur.

⚠ The ring can only be reached with a REAL keyboard event -- el.focus() from script
does not set :focus-visible (memory script-focus-does-not-trigger-focus-visible).
Every case here therefore focuses a neighbour and Tabs onto the target for real.

⚠ Reading `outline` alone is not enough: .gb-reel's focus treatment is a scale on a
CHILD and .gb-sub__select's is a border-colour, both of which outrank the generic
.is-refocused rule. Each case declares what to sample.
"""
import argparse
import pathlib
import sys

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
LIVE = 'https://gumi.com.au'

# page, live path, trigger selector, name, what to sample, does Tab alone open it
# ⚠ The reel card was a case here until r123: it opened the shared lightbox, and its
# focus treatment (a scale on a child) needed its own opt-out. r123 made reels play in
# place, so the card no longer returns focus from any dialog -- the case and the
# .gb-reel opt-out both went. Do not re-add it without a dialog behind it.
# ⚠ The header toggle opens on focus (r115), so pressing Enter after Tab would SHUT
# it again and the Escape below would no-op -- the judge then reads a still-tabbed
# control and blames the fix. Anything that opens on focus must skip the Enter.
CASES = [
    ('index.html',  '/',                    '.gb-header__toggle',      'header menu',  'outline', True),
    ('reviews.html', '/pages/reviews',      '[data-modal="nutritional-label"]', 'nutrition label', 'outline', False),
    ('get-in-touch.html', '/pages/get-in-touch',
                                            '.gb-select__button', 'custom select', 'border', False),
]

fails, oks = [], []


def check(name, ok, detail=''):
    print(('  ok   ' if ok else '  FAIL ') + name + ('' if ok else '   ' + detail))
    (oks if ok else fails).append(name)


# Focus a neighbour by script, then Tab for real so :focus-visible engages.
LAND = r"""(sel) => {
  const t = document.querySelector(sel);
  if (!t) return false;
  const all = [...document.querySelectorAll(
    'a[href],button,input,select,textarea,[tabindex]:not([tabindex="-1"])')]
    .filter(e => e.getClientRects().length);
  const i = all.indexOf(t);
  if (i < 0) return false;
  if (i === 0) { if (document.activeElement) document.activeElement.blur(); return true; }
  all[i - 1].focus();
  return true;
}"""

READ = r"""([sel, kind]) => {
  const t = document.querySelector(sel);
  if (!t) return null;
  const cs = getComputedStyle(t);
  const out = {active: document.activeElement === t, outline: cs.outlineWidth + ' ' + cs.outlineStyle,
               marked: t.classList.contains('is-refocused')};
  if (kind === 'childscale') {
    const kid = t.querySelector('.gb-reel__media');
    out.extra = kid ? getComputedStyle(kid).transform : null;
  } else if (kind === 'border') {
    out.extra = cs.borderColor;
  }
  return out;
}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--live', action='store_true')
    ap.add_argument('--password', default='1234')
    ap.add_argument('--strip', action='store_true')
    args = ap.parse_args()

    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME, args=['--no-sandbox'])
        ctx = b.new_context(viewport={'width': 1440, 'height': 900})
        if args.live:
            ctx.request.post(LIVE + '/password',
                             form={'form_type': 'storefront_password', 'utf8': '✓',
                                   'password': args.password})
        pg = ctx.new_page()

        for name, live_path, sel, label, kind, opens_on_focus in CASES:
            url = (LIVE + live_path) if args.live else (ROOT / name).as_uri()
            try:
                pg.goto(url, wait_until='networkidle' if args.live else 'load', timeout=60000)
            except Exception as e:
                check('%s loads' % label, False, str(e)[:70]); continue
            pg.evaluate("() => document.querySelectorAll('.gb-promo-modal,.gb-promo-modal__overlay')"
                        ".forEach(e => e.remove())")
            if args.strip:   # inverted: neuter the mark, the treatment must come back
                pg.add_style_tag(content=
                    '.is-refocused:focus-visible{outline:2px solid #005635!important}')

            rest = pg.evaluate(READ, [sel, kind])   # untouched baseline
            if not pg.evaluate(LAND, sel):
                check('%s  trigger reachable' % label, False, 'selector not found / first in tab order')
                continue
            pg.keyboard.press('Tab')          # real key -> :focus-visible engages
            before = pg.evaluate(READ, [sel, kind])
            if not before or not before['active']:
                check('%s  Tab lands on trigger' % label, False, repr(before))
                continue
            check('%s  Tab lands on trigger' % label, True)

            # baseline: a genuinely tabbed-to control DOES look different from rest
            shown = (before['outline'] != rest['outline']) or (before.get('extra') != rest.get('extra'))
            check('%s  tabbed-to differs from rest' % label, shown,
                  'rest=%r tabbed=%r' % (rest, before))

            if not opens_on_focus:
                pg.keyboard.press('Enter')    # open
                pg.wait_for_timeout(450)
            pg.keyboard.press('Escape')       # close -> focus handed back
            pg.wait_for_timeout(650)

            after = pg.evaluate(READ, [sel, kind])
            check('%s  focus really came back' % label, after and after['active'], repr(after))
            check('%s  marked .is-refocused' % label, after and after['marked'], repr(after))
            quiet = after and after['outline'] == rest['outline'] and after.get('extra') == rest.get('extra')
            check('%s  looks unfocused after Escape' % label, quiet,
                  'rest=%r after=%r' % (rest, after))

            # the mark must clear, or a genuine Tab back would never ring again
            pg.keyboard.press('Tab')
            pg.wait_for_timeout(80)
            cleared = pg.evaluate("(sel) => !document.querySelector(sel).classList.contains('is-refocused')", sel)
            check('%s  mark clears on the next key' % label, cleared)

        b.close()

    print('\n%d ok / %d red' % (len(oks), len(fails)))
    print('RED: ' + ', '.join(fails) if fails else 'ALL GREEN')
    if args.strip:
        print('\n--strip run: red above is the expected result.')
        return 0
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
