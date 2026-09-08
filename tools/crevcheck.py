#!/usr/bin/env python3
"""Real Customer Reviews judge -- reviews.html and pdp.html.

  python3 tools/crevcheck.py
  python3 tools/crevcheck.py --strip     # inverted run: must go RED

Named after the module rather than a round: two parallel sessions collided on
r89check.py twice in one day. Re-run this whenever gb-crev is touched.

Static site only. ⚠ Not because live has nothing to probe -- it did not until
2026-09-08, when the other team rebuilt sections/gb-app-section.liquid as a real
review list on our whole gb-crev class set. Live geometry is graded by
tools/crevlive.py, and it has to be: the first live-only defect (stars blown up
to 1500px by Horizon's `img { width: 100% }`) is invisible from here, because the
static build's star file carries its own dimensions and the live one does not.
Run BOTH whenever gb-crev is touched.

Every expected number is the Figma board: 324:64032 at 1440, 324:64978 at 390.

r90 additions: the points are five <img>, the attachment holds a bear
placeholder, the score is stroked, and More/Less pages the list.
"""
import io, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
PAGES = ['reviews.html', 'pdp.html']
LIME = 'rgb(181, 237, 97)'

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
  // r90: the board strokes the figure. Count the halo copies and their colour.
  out.scoreShadow = sc ? [(sc.textShadow.match(/rgb\(181, 237, 97\)/g) || []).length,
                          sc.textShadow.indexOf('none') === 0] : null;

  const su = cs('.gb-crev__summary');
  out.summary = su && [su.flexDirection, su.columnGap, su.rowGap];

  // r90: five 32px <img>, touching, adding up to the board's 160x32.
  const st = q('.gb-crev__stars');
  const stImgs = st ? [...st.querySelectorAll('img')] : [];
  out.stars = st && [box(st), stImgs.length,
                     stImgs.every(i => /star\.svg/.test(i.getAttribute('src'))),
                     stImgs.every(i => box(i).join('x') === '32x32')];

  const ct = cs('.gb-crev__count');
  out.count = ct && [ct.fontSize, ct.lineHeight, ct.letterSpacing, ct.color];

  const cards = all('.gb-crev-card');
  out.nCards = cards.length;
  // r90 duplicates the board's five for the pager, so the BOARD assertions look
  // only at the first five. Anything past that is a copy by design.
  const board = cards.slice(0, 5);
  if (board.length) {
    const c0 = getComputedStyle(board[0]);
    out.card = [c0.rowGap, c0.paddingBottom, c0.borderBottomWidth, c0.borderBottomColor];
    out.withImage = board.map(c => !!c.querySelector('.gb-crev-card__image'));
    out.ratings = board.map(c => {
      const r = c.querySelector('.gb-crev-card__rating');
      const pts = [...r.querySelectorAll('img')];
      return [r.dataset.rating, box(r).join('x'), pts.length,
              pts.length === 5 ? getComputedStyle(pts[4]).opacity : null];
    });
    // r90: the attachment is no longer an empty grey box.
    const im = board[0].querySelector('.gb-crev-card__image');
    const imImg = im && im.querySelector('img');
    out.attach = im && [box(im).join('x'), getComputedStyle(im).backgroundColor,
                        !!imImg && /review-bear/.test(imImg.getAttribute('src')),
                        imImg ? getComputedStyle(imImg).objectFit : null,
                        imImg ? imImg.naturalWidth > 0 : null];
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

# r97: crevPager was removed -- the live section owns paging now, and the static
# build no longer has any. Every card renders and the button is inert; this
# samples that, so re-adding a second pager here would show up as a RED.
PAGER = r"""() => {
  const btn = document.querySelector('[data-crev-more]');
  const cards = [...document.querySelectorAll('.gb-crev-card')];
  const shot = () => [
    cards.filter(c => !c.hidden && getComputedStyle(c).display !== 'none').length,
    btn.textContent.trim(),
    btn.getAttribute('aria-expanded'),
    btn.hidden
  ];
  const out = [shot()];
  for (let i = 0; i < 3; i++) { btn.click(); out.push(shot()); }
  return out;
}"""


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


def run(width, strip=False, pager=False):
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
            # The attachment is loading="lazy": off-screen it never decodes and
            # naturalWidth reads 0, which looks exactly like a broken path.
            pg.evaluate("() => { const l = document.querySelector('.gb-crev__list');"
                        "if (l) l.scrollIntoView({block: 'start'}); }")
            pg.wait_for_timeout(700)
            res[name] = pg.evaluate(PAGER if pager else PROBE)
            pg.close()
        b.close()
    return res


def grade(tag, res, desktop):
    print('\n== %s ==' % tag)
    for page, d in res.items():
        p = lambda s: '%s %s' % (page, s)
        # A floor, not an equality: r90 pages a duplicated set in behind these.
        check(p('board 5 cards present'), d['nCards'] >= 5, True)
        # 736 / 1056 are the board's 272 / 112 side padding expressed as a cap.
        check(p('head cap 736'), d['head'][0], '736px')
        check(p('list cap 1056'), d['list'][0], '1056px')
        check(p('list gap 32'), d['list'][2], '32px')
        check(p('card 20 / 32 / hairline'), d['card'],
              ['20px', '32px', '1px', 'rgba(1, 19, 7, 0.05)'])
        check(p('image on 1 and 3 only'), d['withImage'],
              [True, False, True, False, False])
        # 4.5 dims the whole fifth point to 30%; only review 1 is a full five.
        check(p('ratings'), d['ratings'],
              [['5', '100x20', 5, '1'], ['4.5', '100x20', 5, '0.3'],
               ['4.5', '100x20', 5, '0.3'], ['4.5', '100x20', 5, '0.3'],
               ['4.5', '100x20', 5, '0.3']])
        # r90: 64 box, grey still behind, bear actually decodes, contained.
        check(p('attachment'), d['attach'],
              ['64x64', 'rgb(213, 212, 212)', True, 'contain', True])
        check(p('avatar 48 ring'), d['avatar'][:2], ['48x48', '50%'])
        # Chromium quantises lengths to 1/64px, so assert the band, not 39.27.
        try:
            disc = float(d['avatar'][2][:-2])
        except (TypeError, ValueError):
            disc = None
        check(p('avatar disc ~39.27'), disc is not None and 39.2 < disc < 39.3, True)
        check(p('stars 160x32, five images'), d['stars'], [[160, 32], 5, True, True])
        check(p('score colour'), d['score'][3], 'rgb(0, 86, 53)')
        check(p('score weight 800'), d['score'][2], '800')
        # ink-outline(0.25em, lime, 72 steps) = 24 + 48 + 72 ring copies.
        check(p('score stroke 144 lime copies'), d['scoreShadow'], [144, False])
        check(p('count colour'), d['count'][3], 'rgb(77, 77, 77)')
        # Rule 13: a pressable thing transitions. 0s here means the rule was lost.
        check(p('vote transitions'), d['vote'][1] != '0s', True)

        if desktop:
            check(p('score 66.18/52'), d['score'][:2], ['66.18px', '52px'])
            check(p('count 16/24/-0.32'), d['count'][:3], ['16px', '24px', '-0.32px'])
            check(p('summary row gap 12'), d['summary'], ['row', '12px', '12px'])
            check(p('button 52 / 64 / 28 / .48'), d['btn'], [52, '64px', '28px', '0.48px'])
        else:
            check(p('score 56/44'), d['score'][:2], ['56px', '44px'])
            check(p('count 14/20/-0.28'), d['count'][:3], ['14px', '20px', '-0.28px'])
            check(p('summary column gap 16'), d['summary'], ['column', '16px', '16px'])
            check(p('button 44 / 40 / 24 / -.32'), d['btn'], [44, '40px', '24px', '-0.32px'])


def grade_pager(res):
    """r97 reversal: there is no pager on the static build any more.

    The client chose the live section's own inline pager as the single
    implementation, so crevPager is gone from main.js. What is graded here is
    that NOTHING moves: every card is visible and stays visible through three
    clicks. A RED means a second pager crept back in.
    """
    print('\n== no pager on the static build (1440) ==')
    for page, steps in res.items():
        # All ten, not the old resting five: with no pager the [hidden] attrs
        # the markup used to ship would have made half the list unreachable, so
        # r97 stripped them from reviews.html / pdp.html too.
        check('%s all ten cards render (r97 reversal)' % page, [s[0] for s in steps], [10] * 4)
        check('%s label never flips (r97 reversal)' % page, [s[1] for s in steps],
              ['See More Reviews'] * 4)
        check('%s button stays visible' % page, [s[3] for s in steps], [False] * 4)


STRIP = '--strip' in sys.argv

print('== source ==')
css = io.open(ROOT / 'assets/customstyle.css', encoding='utf-8').read()
js = io.open(ROOT / 'assets/main.js', encoding='utf-8').read()
# Rule 13: hover must sit behind (hover: hover) or it sticks after a tap.
check('vote hover is gated',
      re.search(r'@media \(hover: hover\) \{\s*\.gb-crev-card__vote:hover', css) is not None, True)
# r90 moved the dim point off a path fill onto the <img>; the 30% must survive.
check('dim point is 30%',
      re.search(r'\.gb-crev-card__star--dim \{\s*opacity: 0\.3', css) is not None, True)
# [hidden] loses to an author display; both restatements have to be there or the
# pager "hides" rows that stay on screen.
check('card [hidden] restated', '.gb-crev-card[hidden]' in css, True)
check('button [hidden] restated', '.gb-crev__more[hidden]' in css, True)
check('more button is the shared gb-btn', all(
    'gb-btn gb-btn--lg gb-crev__more' in io.open(ROOT / p, encoding='utf-8').read()
    for p in PAGES), True)
# r97 reversal: the live section's inline script is the only pager now. Two of
# them on the same hooks double every click (8 rows revealed, label written twice).
check('pager module is gone (r97 reversal)', 'crevPager' in js, False)
check('our reveal animation went with it', 'gm-crev-in' in css, False)

grade('desktop 1440', run(1440, STRIP), True)
grade('mobile 390', run(390, STRIP), False)
if not STRIP:
    grade_pager(run(1440, pager=True))

if STRIP:
    # Inverted run: without our rules the numbers must NOT match. Green here
    # would mean the judge is reading something else.
    print('\n--strip: %d FAIL (expected: many)' % len(fails))
    sys.exit(0 if fails else 1)
print('\n%d FAIL' % len(fails) if fails else '\nall green')
sys.exit(1 if fails else 0)
