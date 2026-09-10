#!/usr/bin/env python3
"""The phone field's country list and the placeholder that has to follow it.

  python3 tools/phonecode.py
  python3 tools/phonecode.py --live --password 1234
  python3 tools/phonecode.py --strip     # inverted: drop data-dial, must go RED

Client r137: "表单这个下拉只有 AU，需要多增加几个" -> AU / NZ / US / GB / CA / SG,
ISO letters kept as the board draws them, and the placeholder's dial code follows
whatever is picked.

⚠ Drives the CUSTOM widget, not the native <select>: selectBox replaces the native
control with a button + listbox, so setting native.value in script would prove
nothing about what a user can actually do.

⚠ The tick matters here. --bare was excluded from the selected-tick rule while it
had a single always-selected option; with six there is no other way to see which
one is current, so its absence is a real defect now and is asserted below.

⚠ US and CA share +1. Correct, not a slip -- the judge expects it.

⚠ Live carries an auto-opening promo modal (data-promo-delay 4000) whose overlay
swallows clicks partway through the run. That is the site behaving normally, not a
defect: the judge suppresses it before navigating and closes it if it slips through.
"""
import argparse
import pathlib
import sys

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
LIVE = 'https://gumi.com.au'

# iso, dial, example tail, digits after the dial code.
# ⚠ The digit counts are the point of this table. r137 first shipped one shared
# tail (the board's AU "400 000 000") behind every dial code, which was wrong for
# four of the six: US/CA/GB a digit short, SG a digit over, and NZ has no 400
# range. Real prefixes with zeroed tails; US/CA use 555, the North American range
# reserved for fiction, so no placeholder points at a live line.
WANT = [('AU', '+61', '400 000 000', 9),
        ('NZ', '+64', '21 000 0000', 9),
        ('US', '+1', '201 555 0000', 10),
        ('GB', '+44', '7400 000000', 10),
        ('CA', '+1', '204 555 0000', 10),
        ('SG', '+65', '8000 0000', 8)]

PAGES = [('get-in-touch.html', '/pages/get-in-touch'),
         ('referral.html', '/pages/referral')]

STRIP = """
() => {
  document.querySelectorAll('[data-phone-code] option').forEach(o => {
    o.removeAttribute('data-dial'); o.removeAttribute('data-example');
  });
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--live', action='store_true')
    ap.add_argument('--password')
    ap.add_argument('--strip', action='store_true',
                    help='remove data-dial in the page; the follow cases must go RED')
    args = ap.parse_args()

    global aborted
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=CHROME)
        ctx = br.new_context(viewport={'width': 1440, 'height': 900})
        if args.live and args.password:
            ctx.request.post(LIVE + '/password', form={
                'form_type': 'storefront_password', 'utf8': '✓', 'password': args.password})
        pg = ctx.new_page()
        # Suppress the first-order promo modal: its overlay is modal and swallows
        # the option clicks below. ⚠ Setting our own sessionStorage flag is NOT
        # enough live -- what opens it there reads data-promo-delay, not
        # gb-promo-seen, so the element itself is removed instead. Judge-side only;
        # nothing about the page under test changes.
        pg.add_init_script("""
          try { sessionStorage.setItem('gb-promo-seen', '1'); } catch (e) {}
          document.addEventListener('DOMContentLoaded', function () {
            var m = document.getElementById('promo-modal');
            if (m) { m.remove(); }
          });
        """)

        for local, path in PAGES:
            url = LIVE + path if args.live else (ROOT / local).as_uri()
            label = path if args.live else local
            resp = pg.goto(url, wait_until='domcontentloaded')
            if args.live and resp and resp.status in (429, 503):
                print(f'  ABORT {label}  [{resp.status} rate limited]')
                aborted += 1
                continue
            pg.wait_for_timeout(900)
            print(f'--- {label} ---')

            if args.strip:
                pg.evaluate(STRIP)
                # rebind so the stripped DOM is what the module reads
                pg.evaluate("() => window.gumi && window.gumi.phoneCode.init()")

            shape = pg.evaluate("""() => {
              const s = document.querySelector('[data-phone-code]');
              if (!s) return null;
              return {
                opts: [...s.options].map(o => [o.value, o.textContent.trim(),
                        o.getAttribute('data-dial'), o.getAttribute('data-example')]),
                widget: !!document.querySelector('.gb-select--bare .gb-select__button'),
              };
            }""")
            if not shape:
                print(f'  ABORT {label}  [no [data-phone-code] on the page]')
                aborted += 1
                continue
            if not shape['widget']:
                print(f'  ABORT {label}  [selectBox built no widget]')
                aborted += 1
                continue

            if not args.strip:
                got = [(v, t) for v, t, _, _ in shape['opts']]
                report(f'{label}: six countries, ISO letters, board order',
                       got == [(c, c) for c, _, _, _ in WANT], str(got))
                pairs = [(v, d, e) for v, _, d, e in shape['opts']]
                report(f'{label}: dial code + per-country example attached',
                       pairs == [(c, d, e) for c, d, e, _ in WANT], str(pairs))

            # open the custom list and click each row
            for idx, (iso, dial, example, ndigits) in enumerate(WANT):
                # belt and braces: it can be injected after DOMContentLoaded
                pg.evaluate("""() => {
                  const m = document.getElementById('promo-modal');
                  if (m) { m.remove(); }
                  document.documentElement.classList.remove('is-modal-open');
                  document.body.classList.remove('is-modal-open');
                }""")
                pg.locator('.gb-select--bare .gb-select__button').click()
                pg.wait_for_timeout(220)
                rows = pg.locator('.gb-select--bare .gb-select__option')
                if rows.count() != len(WANT):
                    report(f'{label}: list shows all six', False, f'{rows.count()} rows')
                    break
                rows.nth(idx).click()
                pg.wait_for_timeout(260)
                st = pg.evaluate("""() => {
                  const f = document.querySelector('.gb-field__phone');
                  const b = document.querySelector('.gb-select--bare .gb-select__button');
                  const i = f.querySelector('input[type="tel"]');
                  const sel = document.querySelector('.gb-select--bare .gb-select__option[aria-selected="true"]');
                  const tick = sel ? getComputedStyle(sel, '::after').backgroundImage : null;
                  const list = document.querySelector('.gb-select--bare .gb-select__list');
                  return {
                    button: b.textContent.trim(),
                    placeholder: i.getAttribute('placeholder'),
                    selectedRow: sel ? sel.textContent.trim() : null,
                    tickPainted: !!(tick && tick !== 'none'),
                    listOverflows: list ? list.scrollWidth > list.clientWidth + 1 : null,
                    listScrolls: list ? list.scrollHeight > list.clientHeight + 1 : null,
                    listBox: list ? [Math.round(list.clientHeight), list.scrollHeight] : null,
                  };
                }""")
                want_ph = f'{dial} {example}'
                report(f'{label}: pick {iso} -> button + placeholder follow',
                       st['button'] == iso and st['placeholder'] == want_ph,
                       f"button={st['button']} placeholder={st['placeholder']}")
                # The question this table exists to answer: is the number the
                # right LENGTH for the country, not just the right prefix.
                tail = (st['placeholder'] or '')
                tail = tail[len(dial):] if tail.startswith(dial) else tail
                got_digits = sum(c.isdigit() for c in tail)
                report(f'{label}: {iso} number is {ndigits} digits',
                       got_digits == ndigits,
                       f'{got_digits} digits in "{tail.strip()}"')
                if idx == 1 and not args.strip:
                    report(f'{label}: the current row is ticked',
                           st['tickPainted'] and st['selectedRow'] == iso,
                           f"row={st['selectedRow']} tick={st['tickPainted']}")
                    report(f'{label}: the list does not overflow itself',
                           st['listOverflows'] is False, f"overflow={st['listOverflows']}")
                    # ⚠ The horizontal check above missed this on the first pass:
                    # all six rows must be visible without scrolling, or the last
                    # one sits half-cut at the scroll edge and reads as broken.
                    report(f'{label}: all six rows fit without scrolling',
                           st['listScrolls'] is False,
                           f"client/scroll={st['listBox']}")

        br.close()

    print(f'\n{ok} ok / {red} red / {aborted} aborted')
    if args.strip:
        print('--strip: expect RED on the follow cases')
        return 0 if red > 0 else 1
    return 0 if red == 0 and aborted == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
