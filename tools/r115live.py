#!/usr/bin/env python3
"""r115 read back off live.

  python3 tools/r115live.py --password 1234

1  $build reached the CDN.
2  .gb-rich-table th:first-child is 124 on /pages/shipping.
3  br.gb-br-wide is drawn on 390 now -- the reviews h1 gains its mobile break.
4  gb-science still renders after the CTA edit, and stays CTA-less until the
   setting is filled (that is the expected state, not a failure).
"""
import argparse, sys
from playwright.sync_api import sync_playwright

CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
LIVE = 'https://gumi.com.au'
ok = red = 0


def grade(cond, label, detail=''):
    global ok, red
    if cond:
        ok += 1
        print(f'  ok   {label}   {detail}')
    else:
        red += 1
        print(f'  RED  {label}   {detail}')


a = argparse.ArgumentParser(); a.add_argument('--password', required=True)
args = a.parse_args()

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=CHROME)
    ctx = b.new_context(viewport={'width': 1440, 'height': 900})
    ctx.request.post(LIVE + '/password', form={
        'form_type': 'storefront_password', 'utf8': '✓', 'password': args.password})
    pg = ctx.new_page()

    def go(path, w, h=900):
        pg.set_viewport_size({'width': w, 'height': h})
        pg.goto(LIVE + path, wait_until='domcontentloaded', timeout=90000)
        pg.wait_for_timeout(1600)

    print('--- 1. $build ---')
    go('/pages/shipping', 1440)
    grade(pg.evaluate("""() => getComputedStyle(document.documentElement)
            .getPropertyValue('--build').trim()""") == '"20260908-r115"',
         '--build is r115',
         pg.evaluate("""() => getComputedStyle(document.documentElement)
            .getPropertyValue('--build').trim()"""))

    print('--- 2. rich-table label column ---')
    for w in (1440, 390):
        go('/pages/shipping', w)
        m = pg.evaluate("""() => {
            const t = [...document.querySelectorAll('.gb-rich-table')];
            const plain = t.find(x => !x.classList.contains('gb-rich-table--even'));
            const even  = t.find(x =>  x.classList.contains('gb-rich-table--even'));
            const w1 = e => e ? Math.round(e.querySelector('th').getBoundingClientRect().width * 10) / 10 : null;
            return {n: t.length, plain: w1(plain), even: w1(even)};
        }""")
        grade(m['n'] >= 1, f'@{w:<5} the table is on the page at all', f"n={m['n']}")
        grade(m['plain'] == 124, f'@{w:<5} th:first-child is 124', f"got {m['plain']}")
        grade(m['even'] not in (None, 124), f'@{w:<5} --even still opts out', f"got {m['even']}")

    # Line COUNT is the wrong claim here: live's hero carries --lg (a registered
    # static/live difference), so "Aussies are obsessed." wraps on its own at 350
    # either way. What the break has to prove is that "Here's why." owns the last
    # line instead of being split across two -- read the words, not the height.
    print('--- 3. gb-br-wide now draws on the phone ---')
    for w, want in ((1440, 3), (390, 3)):
        go('/pages/reviews', w)
        m = pg.evaluate("""() => {
            const h = document.querySelector('.gb-page-hero__title, h1');
            const cs = h && getComputedStyle(h);
            const wide = [...document.querySelectorAll('br.gb-br-wide')];
            return {lines: h ? Math.round(h.getBoundingClientRect().height / parseFloat(cs.lineHeight)) : null,
                    h: h ? Math.round(h.getBoundingClientRect().height) : null,
                    lh: cs && cs.lineHeight,
                    nWide: wide.length,
                    drawn: wide.filter(b => getComputedStyle(b).display !== 'none').length,
                    caret: (document.body.innerText.match(/\\^\\^/g) || []).length,
                    lastLine: (() => {
                      // leaves only: the mask/halo wrappers repeat the same words
                      // at a coarser granularity and would double the join
                      const ws = [...h.querySelectorAll('*')].filter(
                        s => s.children.length === 0 && s.offsetParent !== null
                             && s.textContent.trim());
                      const rows = {};
                      for (const s of ws) { const t = Math.round(s.getBoundingClientRect().top);
                        (rows[t] = rows[t] || []).push(s.textContent.trim()); }
                      const tops = Object.keys(rows).map(Number).sort((a, b) => a - b);
                      // the halo repeats every word, so dedupe before joining
                      return tops.length ? [...new Set(rows[tops[tops.length - 1]])].join(' ') : null;
                    })()};
        }""")
        grade(m['nWide'] >= 1, f'@{w:<5} the h1 still carries a gb-br-wide', f"n={m['nWide']}")
        grade(m['drawn'] == m['nWide'], f'@{w:<5} and it is drawn (display != none)',
              f"{m['drawn']}/{m['nWide']}")
        grade(m['lines'] == want, f'@{w:<5} h1 is {want} lines',
              f"got {m['lines']}  ({m['h']}px / {m['lh']})")
        grade(m['caret'] == 0, f'@{w:<5} no literal ^^ printed', f"{m['caret']} found")
        grade(m['lastLine'] == "Here's why.",
              f'@{w:<5} the break owns the last line', f"last line {m['lastLine']!r}")

    print('--- 4. gb-science survives the CTA edit ---')
    for w in (1440, 390):
        go('/pages/science', w)
        m = pg.evaluate("""() => ({
            sections: document.querySelectorAll('.gb-science').length,
            tight: document.querySelectorAll('.gb-science--tight').length,
            cards: document.querySelectorAll('.gb-science-card').length,
            cta: document.querySelectorAll('.gb-science__cta').length,
            liquidError: /Liquid error|Liquid syntax error/i.test(document.body.innerText)})""")
        grade(not m['liquidError'], f'@{w:<5} no Liquid error on the page')
        grade(m['sections'] == 2 and m['tight'] == 1,
              f'@{w:<5} both gb-science sections still render',
              f"{m['sections']} sections / {m['tight']} tight")
        grade(m['cards'] >= 6, f'@{w:<5} the cards are all there', f"n={m['cards']}")
        grade(m['cta'] == 0, f'@{w:<5} CTA stays hidden while cta_label is empty',
              f"n={m['cta']} (expected 0)")
    b.close()

print(f'\n{ok} ok / {red} red   [LIVE]')
sys.exit(1 if red else 0)
