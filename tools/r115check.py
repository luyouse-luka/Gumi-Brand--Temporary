#!/usr/bin/env python3
"""r115 asks 1-3, graded on the static build.

  python3 tools/r115check.py

1  .gb-science__cta sits 48px clear of .gb-science__cards at every tier.
2  .gb-br-wide is drawn at every width now, so gb-dosed__title breaks 4 up on 390.
3  .gb-rich-table th:first-child is 124, and --even still opts out.
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


# offsetTop, not getBoundingClientRect: .wowo/fadeInUp puts a transform on these
# mid-animation and the rect would carry it. Both share .gb-science as their
# offsetParent (it is position:relative), so the difference is the real gap.
GAP = """() => {
  const sec = document.querySelector('.gb-science--tight');
  if (!sec) return null;
  const cards = sec.querySelector('.gb-science__cards');
  const cta = sec.querySelector('.gb-science__cta');
  if (!cards || !cta) return {cards: !!cards, cta: !!cta};
  return {cards: true, cta: true,
          sameParent: cards.offsetParent === cta.offsetParent,
          gap: Math.round((cta.offsetTop - cards.offsetTop - cards.offsetHeight) * 10) / 10,
          tag: cta.tagName, href: cta.getAttribute('href'),
          txt: cta.textContent.trim(),
          h: Math.round(cta.getBoundingClientRect().height),
          n: document.querySelectorAll('.gb-science__cta').length};
}"""

# Range over this h2 counts double: .gb-ink-halo is a second, offset copy of the
# same words. It is absolutely positioned, so the box height is the real flow and
# lineHeight divides it cleanly.
LINES = """(sel) => {
  // how-gumi-works carries TWO .gb-dosed__title; only the second holds breaks.
  const el = [...document.querySelectorAll(sel)].find(e => e.querySelector('br'));
  if (!el) return null;
  const cs = getComputedStyle(el);
  return {lines: Math.round(el.getBoundingClientRect().height / parseFloat(cs.lineHeight)),
          brWide: document.querySelectorAll('br.gb-br-wide').length,
          wideDrawn: [...document.querySelectorAll('br.gb-br-wide')]
                       .filter(b => getComputedStyle(b).display !== 'none').length,
          narrowDrawn: [...document.querySelectorAll('br.gb-br-narrow')]
                       .filter(b => getComputedStyle(b).display !== 'none').length};
}"""

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=CHROME)
    ctx = b.new_context(viewport={'width': 1440, 'height': 900})
    pg = ctx.new_page()

    print('--- 1. science CTA, 48 clear of the cards ---')
    for w in (1440, 1281, 1280, 1024, 768, 767, 390):
        pg.set_viewport_size({'width': w, 'height': 900})
        pg.goto((ROOT / 'science.html').as_uri())
        pg.wait_for_timeout(200)
        m = pg.evaluate(GAP)
        if not m or not m.get('cta'):
            grade(False, f'@{w:<5} CTA present', str(m))
            continue
        grade(m['sameParent'], f'@{w:<5} gap is measurable (one offsetParent)')
        grade(abs(m['gap'] - 48) < 1.0, f'@{w:<5} cards -> CTA is 48', f"got {m['gap']}")
        if w == 1440:
            grade(m['tag'] == 'A' and m['href'] == 'pdp.html' and m['txt'] == 'Shop Now',
                  'CTA is a Shop Now link', f"{m['tag']} {m['href']} {m['txt']!r}")
            grade(m['n'] == 1, 'and only the tight section has one', f"n={m['n']}")
            grade(m['h'] == 60, 'gb-btn--xl height 60 on desktop', str(m['h']))
        if w == 390:
            grade(m['h'] == 52, 'gb-btn--xl height 52 on 390', str(m['h']))

    print('--- 2. .gb-br-wide is drawn at every width ---')
    # 768 carries no line-count claim: the h2 box is only 285 wide there, so it
    # wraps to 4 on its own -- the class states are the only honest reading.
    for w, want in ((1440, 2), (768, None), (390, 4)):
        pg.set_viewport_size({'width': w, 'height': 900})
        pg.goto((ROOT / 'how-gumi-works.html').as_uri())
        pg.wait_for_timeout(200)
        m = pg.evaluate(LINES, '.gb-dosed__title')
        if not m:
            grade(False, f'@{w} gb-dosed__title present')
            continue
        grade(m['brWide'] and m['wideDrawn'] == m['brWide'],
              f'@{w:<5} every br.gb-br-wide has display != none',
              f"{m['wideDrawn']}/{m['brWide']}")
        if want is not None:
            grade(m['lines'] == want, f'@{w:<5} gb-dosed__title is {want} lines',
                  f"got {m['lines']}")
        else:
            grade(m['narrowDrawn'] == 0, f'@{w:<5} and br.gb-br-narrow is still hidden',
                  f"{m['narrowDrawn']} drawn")

    print('--- 3. rich-table label column ---')
    for w in (1440, 768, 390):
        pg.set_viewport_size({'width': w, 'height': 900})
        pg.goto((ROOT / 'shipping.html').as_uri())
        pg.wait_for_timeout(200)
        m = pg.evaluate("""() => {
            const t = [...document.querySelectorAll('.gb-rich-table')];
            const plain = t.find(x => !x.classList.contains('gb-rich-table--even'));
            const even  = t.find(x =>  x.classList.contains('gb-rich-table--even'));
            const w1 = e => e ? Math.round(e.querySelector('th').getBoundingClientRect().width * 10) / 10 : null;
            return {plain: w1(plain), even: w1(even),
                    tw: plain ? Math.round(plain.getBoundingClientRect().width) : null};
        }""")
        grade(m['plain'] == 124, f'@{w:<5} th:first-child is 124', f"got {m['plain']}  (table {m['tw']})")
        grade(m['even'] not in (None, 124), f'@{w:<5} --even still opts out', f"got {m['even']}")
    b.close()

print(f'\n{ok} ok / {red} red')
sys.exit(1 if red else 0)
