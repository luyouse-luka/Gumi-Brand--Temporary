#!/usr/bin/env python3
"""r89 judge -- the Real Customer Reviews block on reviews.html and pdp.html.

  python3 tools/r89check.py

Static site only: gb-app-section has no liquid on live, so there is nothing to
probe there yet. Every expected number is the Figma board -- 324:64032 at 1440,
324:64978 at 390. Two widths, because the two boards disagree on the score
figure, the summary axis and the button.
"""
import io, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
PAGES = ['reviews.html', 'pdp.html']

fails = []


def check(name, got, want):
    ok = got == want
    print(('  ok   ' if ok else '  FAIL ') + name + ('' if ok else '   got=%r want=%r' % (got, want)))
    if not ok:
        fails.append(name)


PROBE = r"""() => {
  const q = s => document.querySelector(s);
  const all = s => [...document.querySelectorAll(s)];
  const cs = s => { const e = q(s); return e ? getComputedStyle(e) : null; };
  const box = e => { const r = e.getBoundingClientRect();
                     return [Math.round(r.width * 100) / 100, Math.round(r.height * 100) / 100]; };
  const out = {};

  const head = q('.gb-crev__head'), list = q('.gb-crev__list');
  out.head = head && [getComputedStyle(head).maxWidth, box(head)[0]];
  out.list = list && [getComputedStyle(list).maxWidth, box(list)[0], getComputedStyle(list).rowGap];

  const sc = cs('.gb-crev__score');
  out.score = sc && [sc.fontSize, sc.lineHeight, sc.fontWeight, sc.color];

  const su = cs('.gb-crev__summary');
  out.summary = su && [su.flexDirection, su.columnGap, su.rowGap];

  const st = q('.gb-crev__stars');
  out.stars = st && box(st);

  const ct = cs('.gb-crev__count');
  out.count = ct && [ct.fontSize, ct.lineHeight, ct.letterSpacing, ct.color];

  const cards = all('.gb-crev-card');
  out.nCards = cards.length;
  if (cards.length) {
    const c0 = getComputedStyle(cards[0]);
    out.card = [c0.rowGap, c0.paddingBottom, c0.borderBottomWidth, c0.borderBottomColor];
    // The board hangs an image on reviews 1 and 3 only (191:5468 hidden elsewhere).
    out.withImage = cards.map(c => !!c.querySelector('.gb-crev-card__image'));
    out.ratings = cards.map(c => {
      const r = c.querySelector('.gb-crev-card__rating');
      const last = r.querySelector('path:last-of-type');
      return [r.dataset.rating, box(r).join('x'), getComputedStyle(last).fillOpacity];
    });
  }

  const av = q('.gb-crev-card__avatar');
  out.avatar = av && [box(av).join('x'), getComputedStyle(av).borderRadius,
                      getComputedStyle(av, '::before').width];

  const btn = q('.gb-crev__more');
  out.btn = btn && [box(btn)[1], getComputedStyle(btn).paddingLeft,
                    getComputedStyle(btn).lineHeight, getComputedStyle(btn).letterSpacing];

  const vote = cs('.gb-crev-card__vote');
  out.vote = vote && [vote.color, vote.transitionDuration, vote.transitionProperty];
  return out;
}"""


def grade(tag, res, desktop):
    print('\n== %s ==' % tag)
    for page, d in res.items():
        p = lambda s: '%s %s' % (page, s)
        check(p('5 cards'), d['nCards'], 5)
        # 736 / 1056 are the board's 272 / 112 side padding expressed as a cap.
        check(p('head cap 736'), d['head'][0], '736px')
        check(p('list cap 1056'), d['list'][0], '1056px')
        check(p('list gap 32'), d['list'][2], '32px')
        check(p('card 20 / 32 / hairline'), d['card'],
              ['20px', '32px', '1px', 'rgba(1, 19, 7, 0.05)'])
        check(p('image on 1 and 3 only'), d['withImage'],
              [True, False, True, False, False])
        # 4.5 dims the fifth point to 30%; only review 1 is a full five.
        check(p('ratings'), d['ratings'],
              [['5', '100x20', '1'], ['4.5', '100x20', '0.3'], ['4.5', '100x20', '0.3'],
               ['4.5', '100x20', '0.3'], ['4.5', '100x20', '0.3']])
        # Chromium quantises lengths to 1/64px, so assert the band, not 39.27 itself.
        check(p('avatar 48 ring'), d['avatar'][:2], ['48x48', '50%'])
        # Stays a FAIL rather than a crash when the disc rule is absent ('auto').
        try:
            disc = float(d['avatar'][2][:-2])
        except (TypeError, ValueError):
            disc = None
        check(p('avatar disc ~39.27'), disc is not None and 39.2 < disc < 39.3, True)
        check(p('stars 160x32'), d['stars'], [160, 32])
        check(p('score colour'), d['score'][3], 'rgb(0, 86, 53)')
        check(p('score weight 800'), d['score'][2], '800')
        check(p('count colour'), d['count'][3], 'rgb(77, 77, 77)')
        # Rule 13: a pressable thing transitions. 0s here means the rule was lost.
        check(p('vote transitions'), d['vote'][1] != '0s', True)

        if desktop:
            check(p('score 66.18/52'), d['score'][:2], ['66.18px', '52px'])
            check(p('count 16/24/-0.32'), d['count'][:3], ['16px', '24px', '-0.32px'])
            check(p('summary row gap 12'), d['summary'], ['row', '12px', '12px'])
            check(p('button 52 / 64 / 28 / .48'), d['btn'],
                  [52, '64px', '28px', '0.48px'])
        else:
            check(p('score 56/44'), d['score'][:2], ['56px', '44px'])
            check(p('count 14/20/-0.28'), d['count'][:3], ['14px', '20px', '-0.28px'])
            check(p('summary column gap 16'), d['summary'], ['column', '16px', '16px'])
            check(p('button 44 / 40 / 24 / -.32'), d['btn'],
                  [44, '40px', '24px', '-0.32px'])


def strip_crev(css):
    """Drops every .gb-crev rule so --strip can prove the judge reads OUR rules
    and not something the page had already. Brace matching, because the block
    also lives inside @media."""
    out, i, n = [], 0, len(css)
    while i < n:
        j = css.find('{', i)
        if j < 0:
            out.append(css[i:]); break
        sel = css[i:j]
        if '.gb-crev' in sel and '@media' not in sel:
            depth, k = 1, j + 1
            while k < n and depth:
                if css[k] == '{': depth += 1
                elif css[k] == '}': depth -= 1
                k += 1
            i = k
        else:
            out.append(css[i:j + 1]); i = j + 1
    return ''.join(out)


def run(width, strip=False):
    from playwright.sync_api import sync_playwright
    res = {}
    body = strip_crev(css) if strip else None
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME)
        ctx = b.new_context(viewport={'width': width, 'height': 900})
        if body is not None:
            ctx.route(re.compile(r'customstyle\.css'), lambda route: route.fulfill(
                status=200, content_type='text/css', body=body))
        for name in PAGES:
            pg = ctx.new_page()
            pg.goto((ROOT / name).as_uri(), wait_until='load', timeout=30000)
            pg.wait_for_timeout(400)
            res[name] = pg.evaluate(PROBE)
            pg.close()
        b.close()
    return res


print('== source ==')
css = io.open(ROOT / 'assets/customstyle.css', encoding='utf-8').read()
# Rule 13: hover must sit behind (hover: hover) or it sticks after a tap.
check('vote hover is gated', '@media (hover: hover)' in css and
      re.search(r'@media \(hover: hover\) \{\s*\.gb-crev-card__vote:hover', css) is not None, True)
check('more button is the shared gb-btn', all(
    'gb-btn gb-btn--lg gb-crev__more' in io.open(ROOT / p, encoding='utf-8').read()
    for p in PAGES), True)

STRIP = '--strip' in sys.argv
grade('desktop 1440', run(1440, STRIP), True)
grade('mobile 390', run(390, STRIP), False)

if STRIP:
    # Inverted run: without our rules the numbers must NOT match. Green here
    # would mean the judge is reading something else.
    print('\n--strip: %d FAIL (expected: many)' % len(fails))
    sys.exit(0 if fails else 1)
print('\n%d FAIL' % len(fails) if fails else '\nall green')
sys.exit(1 if fails else 0)
