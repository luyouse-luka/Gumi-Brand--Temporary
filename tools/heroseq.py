#!/usr/bin/env python3
"""The hero plays as one run: title lines, then each CTA item a beat behind.

  python3 tools/heroseq.py
  python3 tools/heroseq.py --live --password 1234
  python3 tools/heroseq.py --strip     # inverted: neuter the beat, must go RED

Client r122. Two animation systems have to share one clock here: the title and lead
are lineReveal (150ms per LINE), the button and the USP list are wowo (delay-in-N,
0.1s per level, authored in the theme's gb-hero.liquid which we do not edit). The fix
runs them off one counter -- --line-base, set by lineReveal.sequence() -- and lets a
0-3-0 rule outrank the delay-in-N class.

⚠ Do not assert against a fixed ms value: the title and lead re-split on resize, so
the number of beats before the button is width-dependent. Assert the ORDER and that
each step is strictly later than the last.

⚠ .animated is stripped 1500ms after the reveal, taking the computed delay with it.
Everything here reads --line-base, which is an inline style and stays put.
"""
import argparse
import pathlib
import sys

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
LIVE = 'https://gumi.com.au'
BEAT = 150

fails, oks = [], []


def check(name, ok, detail=''):
    print(('  ok   ' if ok else '  FAIL ') + name + ('' if ok else '   ' + detail))
    (oks if ok else fails).append(name)


PROBE = r"""() => {
  const text = document.querySelector('.gb-hero__text');
  if (!text) return null;
  const base = el => el ? parseFloat(getComputedStyle(el).getPropertyValue('--line-base')) : null;
  const title = text.querySelector('.gb-hero__title');
  const lead  = text.querySelector('.gb-hero__lead');
  const btn   = text.querySelector('.gb-hero__btn');
  const usps  = text.querySelector('.gb-usps');
  const lines = el => el ? el.querySelectorAll('.gb-line-mask').length : 0;
  return {
    sequenced: text.hasAttribute('data-line-sequence'),
    steps: [...text.querySelectorAll('[data-seq-step]')].map(e => e.className.split(' ')[0]),
    titleBase: base(title), titleLines: lines(title),
    leadBase: base(lead),   leadLines: lines(lead),
    btnBase: base(btn),     uspBase: base(usps),
    // ⚠ wowo strips .wowo/.animated once the reveal is done, and the rule under
    // test only applies while they are on. Put them back for the read (live pages
    // load slowly enough that they are always gone by now), then restore.
    btnRule: (() => {
      if (!btn) return null;
      const had = [btn.classList.contains('wowo'), btn.classList.contains('animated')];
      btn.classList.add('wowo', 'animated');
      const v = getComputedStyle(btn).animationDelay;
      if (!had[0]) btn.classList.remove('wowo');
      if (!had[1]) btn.classList.remove('animated');
      return v;
    })(),
  };
}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--live', action='store_true')
    ap.add_argument('--password', default='1234')
    ap.add_argument('--strip', action='store_true')
    args = ap.parse_args()

    url = (LIVE + '/') if args.live else (ROOT / 'index.html').as_uri()
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME, args=['--no-sandbox'])
        ctx = b.new_context(viewport={'width': 1440, 'height': 900})
        if args.live:
            ctx.request.post(LIVE + '/password',
                             form={'form_type': 'storefront_password', 'utf8': '✓',
                                   'password': args.password})
        pg = ctx.new_page()
        pg.goto(url, wait_until='networkidle' if args.live else 'load', timeout=60000)
        if args.strip:
            pg.evaluate("""() => {
                const t = document.querySelector('.gb-hero__text');
                if (t) { t.removeAttribute('data-line-sequence');
                  t.querySelectorAll('[data-seq-step]').forEach(e => {
                    e.removeAttribute('data-seq-step'); e.style.removeProperty('--line-base'); }); }
            }""")
        else:
            try:
                pg.wait_for_function(
                    "() => { const b = document.querySelector('.gb-hero__btn');"
                    " return b && getComputedStyle(b).getPropertyValue('--line-base').trim() !== ''; }",
                    timeout=15000)
            except Exception:
                pass
        d = pg.evaluate(PROBE)

        # The last step must still be animating when Terra's flat 1500ms strip would
        # have fired -- otherwise it snaps to its end state mid-fade (r122 fixed play()).
        late = None
        if not args.strip:
            pg2 = ctx.new_page()
            pg2.goto(url, wait_until='networkidle' if args.live else 'load', timeout=60000)
            pg2.wait_for_timeout(1550)
            late = pg2.evaluate("""() => {
              const u = document.querySelector('.gb-usps');
              if (!u) return null;
              return {held: u.classList.contains('animated'),
                      delayMs: parseFloat(getComputedStyle(u).animationDelay) * 1000};
            }""")
        b.close()

    if not d:
        check('hero present', False, '.gb-hero__text not found'); 
    else:
        check('hero present', True)
        check('.gb-hero__text is a sequence', d['sequenced'] is True, repr(d))
        check('both CTA items are steps', sorted(d['steps']) == ['gb-btn', 'gb-usps'], repr(d['steps']))
        check('title starts the run (base 0)', d['titleBase'] == 0, repr(d))
        check('title actually split into lines', (d['titleLines'] or 0) > 0, repr(d))
        check('lead follows the title', d['leadBase'] == d['titleLines'], repr(d))
        expect_btn = (d['titleLines'] or 0) + (d['leadLines'] or 0)
        check('button follows the lead', d['btnBase'] == expect_btn,
              'btnBase=%r expected %r' % (d['btnBase'], expect_btn))
        check('USPs follow the button', d['uspBase'] == expect_btn + 1, repr(d))
        # the whole point: strictly increasing, no two items share a beat
        order = [d['titleBase'], d['leadBase'], d['btnBase'], d['uspBase']]
        check('strictly increasing across the run', all(
            order[i] is not None and order[i + 1] is not None and order[i + 1] > order[i]
            for i in range(len(order) - 1)), repr(order))
        # and the authored delay-in-2 (0.2s) must have lost
        check('sequence beat outranks delay-in-N',
              d['btnRule'] == '%gs' % (expect_btn * BEAT / 1000.0),
              'computed=%r expected %gs' % (d['btnRule'], expect_btn * BEAT / 1000.0))

        if late is not None:
            # only meaningful when the last step actually runs past 1500-700=800ms
            if late['delayMs'] + 700 > 1500:
                check('last step survives Terra\'s 1500ms strip', late['held'] is True, repr(late))
            else:
                print('  n/a  last step ends before 1500ms (delay %gms) -- strip cannot cut it'
                      % late['delayMs'])

    print('\n%d ok / %d red' % (len(oks), len(fails)))
    print('RED: ' + ', '.join(fails) if fails else 'ALL GREEN')
    if args.strip:
        print('\n--strip run: red above is the expected result.')
        return 0
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
