#!/usr/bin/env python3
"""The cart drawer must not open with its close button looking selected.

  python3 tools/cartfocus.py
  python3 tools/cartfocus.py --strip     # inverted: baseline main.js, must go RED

Client r135: "landing on /cart opens the drawer and .gb-cart__close carries the
focus-visible treatment". The drawer is Horizon's <dialog>, so the
[role=dialog][tabindex=-1] rule that keeps OUR modals from ringing their close
button never reaches it -- showModal() hands initial focus to the first focusable
child. On a direct landing there is no user gesture behind that focus, and Chrome
rings it anyway. cartDrawer.guardInitialFocus marks the button the way
returnFocus marks a handed-back focus; CSS drops the ring.

⚠ Live-only shape: our own cart modal gives initial focus to the dialog CONTAINER,
so the static site cannot reproduce it at all. The fixture below is a real
<dialog> opened with no gesture, which is what the theme does.

⚠ This reads getComputedStyle().outline, not the class -- "the mark is set" is not
"the ring is gone" (memory: assert the effect, not the attribute).

⚠ Two guards abort rather than pass: (pointer: coarse) would make r107's rule
drop the ring on its own and every case would be green for the wrong reason, and
the fixture has to actually reach :focus-visible or there is nothing to suppress.
"""
import argparse
import pathlib
import sys

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
BASELINE = pathlib.Path(
    '/home/ly/project/Gumi-Brand-shopify/baseline-20260909-r134/assets/main.js')

# Two buttons so a Tab has somewhere to go and can come back -- case 3 needs the
# button to be reachable by a real keypress.
FIXTURE = """
<!doctype html><html class="js"><head><meta charset="utf-8"></head><body>
  <theme-drawer id="cart-drawer">
    <dialog id="dlg">
      <button class="gb-cart__close" type="button" aria-label="Close cart">x</button>
      <button class="gb-cart__other" type="button">other</button>
    </dialog>
  </theme-drawer>
</body></html>
"""

READ = """
() => {
  const b = document.querySelector('.gb-cart__close');
  const cs = getComputedStyle(b);
  return {
    active: document.activeElement === b,
    focusVisible: b.matches(':focus-visible'),
    marked: b.classList.contains('is-refocused'),
    outlineStyle: cs.outlineStyle,
    outlineWidth: cs.outlineWidth,
  };
}
"""

ok = red = aborted = 0


def report(name, passed, detail):
    global ok, red
    if passed:
        ok += 1
        print(f'  ok    {name}  [{detail}]')
    else:
        red += 1
        print(f'  RED   {name}  [{detail}]')


def abort(name, why):
    global aborted
    aborted += 1
    print(f'  ABORT {name}  [{why}]')


def build(pg, main_js, open_before_script):
    """open_before_script: does the drawer open before main.js parses?"""
    pg.set_content(FIXTURE)
    pg.add_style_tag(path=str(ROOT / 'assets' / 'customstyle.css'))
    if open_before_script:
        pg.evaluate("() => document.getElementById('dlg').showModal()")
        pg.add_script_tag(path=str(main_js))
    else:
        pg.add_script_tag(path=str(main_js))
        pg.evaluate("() => document.getElementById('dlg').showModal()")
    pg.wait_for_timeout(120)
    return pg.evaluate(READ)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--strip', action='store_true',
                    help='load the baseline main.js; every suppression case must go RED')
    args = ap.parse_args()
    main_js = BASELINE if args.strip else ROOT / 'assets' / 'main.js'
    if not main_js.exists():
        print(f'main.js not found: {main_js}')
        return 2
    print(f'main.js: {main_js}')

    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=CHROME)
        pg = br.new_page()

        # ---- guards -------------------------------------------------------
        media = pg.evaluate("""() => ({
          coarse: matchMedia('(pointer: coarse)').matches,
          hover: matchMedia('(hover: hover)').matches,
        })""")
        if media['coarse']:
            abort('guard: pointer is fine',
                  'coarse -- r107 drops the ring by itself, cases prove nothing')
            br.close()
            print(f'\n{ok} ok / {red} red / {aborted} aborted')
            return 3

        # Sass emits expanded css, so strip ALL whitespace before matching --
        # a rule split over three lines is the normal shape here.
        css = ''.join((ROOT / 'assets' / 'customstyle.css').read_text().split())
        report('guard: the suppressing rule is in the build',
               '.is-refocused:focus-visible{outline:none' in css,
               'compiled css')

        # The bug itself must be reachable, or "no ring" means nothing.
        pg.set_content(FIXTURE)
        pg.add_style_tag(path=str(ROOT / 'assets' / 'customstyle.css'))
        pg.evaluate("() => document.getElementById('dlg').showModal()")
        pg.wait_for_timeout(80)
        bare = pg.evaluate(READ)
        if not bare['focusVisible']:
            abort('guard: showModal reaches :focus-visible',
                  'engine does not ring the initial focus -- nothing to suppress')
            br.close()
            print(f'\n{ok} ok / {red} red / {aborted} aborted')
            return 3
        report('guard: unpatched fixture really rings',
               bare['outlineStyle'] == 'solid' and bare['outlineWidth'] == '2px',
               f"{bare['outlineStyle']} {bare['outlineWidth']}")

        # ---- 1. drawer already open when main.js parses (the /cart landing) --
        r = build(pg, main_js, open_before_script=True)
        report('1. opened before main.js: no ring',
               r['active'] and r['outlineStyle'] == 'none',
               f"active={r['active']} marked={r['marked']} outline={r['outlineStyle']}")

        # ---- 2. main.js first, drawer opens after --------------------------
        r = build(pg, main_js, open_before_script=False)
        report('2. opened after main.js: no ring',
               r['active'] and r['outlineStyle'] == 'none',
               f"active={r['active']} marked={r['marked']} outline={r['outlineStyle']}")

        # ---- 3. a real Tab onto it MUST still ring ------------------------
        # Not a suppression case: this is the accessibility floor. It has to stay
        # green with the baseline too, so --strip does not count it as a failure.
        build(pg, main_js, open_before_script=False)
        # ⚠ Tab twice leaves the dialog in this fixture (close -> other -> body),
        # it does not wrap. Go forward once and come back.
        pg.keyboard.press('Tab')          # real keydown -> disarms, clears the mark
        pg.keyboard.press('Shift+Tab')    # back onto the close button, user's own
        pg.wait_for_timeout(80)
        r = pg.evaluate(READ)
        report('3. a genuine Tab still rings (a11y floor)',
               r['active'] and r['outlineStyle'] == 'solid' and not r['marked'],
               f"active={r['active']} marked={r['marked']} outline={r['outlineStyle']}")

        br.close()

    print(f'\n{ok} ok / {red} red / {aborted} aborted')
    if args.strip:
        # cases 1 and 2 must fail without the fix; case 3 and the guards stay green
        print('--strip: expect RED on cases 1 and 2')
        return 0 if red >= 2 else 1
    return 0 if red == 0 and aborted == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
