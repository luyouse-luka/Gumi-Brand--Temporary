#!/usr/bin/env python3
"""r96 assertions: 7 client items.

  python3 tools/r96check.py            # static site (file://)
  python3 tools/r96check.py --strip    # liveness self-check (must go red)

  0 .gb-crev-card gains a reveal animation the pager replays on un-hide
  1 .gb-faq__list --acc-gap back to 24 (reverses r64 item 3)
  2 .gb-header__panel carries NO border while shut -- it used to box the 0fr row
    2px tall and paint $c-cream there, i.e. a hairline under the bar everywhere
  3 every .gb-page-hero__lead is #4d4d4d; --lg / --text-page no longer override
  4 .gb-science--tight .gb-science-card gap 16 -> 22 (tight board only)
  5 .gb-page-hero__title takes a 30px right inset on phones, ramped to 0 by 1281,
    cancelled on --center (a one-sided inset shifts centred text off centre)
  6 the expert rail's first/last card sit flush to the track edges

⚠ --strip restores the old values as INLINE style / re-inits Swiper without the
new option, never by deleting CSSOM rules: under file:// cssRules throws
([[file-url-stylesheet-cssrules-blocked]]). Every strip returns a touched count
and a zero count is itself a RED.
"""
import argparse
from playwright.sync_api import sync_playwright

CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
ROOT = 'file:///home/ly/project/Gumi-Brand'

SAND = 'rgb(245, 241, 233)'
GREY = 'rgb(77, 77, 77)'          # #4d4d4d
HERO_PAGES = ['faq', 'get-in-touch', 'how-gumi-works', 'our-story',
              'privacy-policy', 'referral', 'reviews', 'science', 'shipping']
CENTRE_PAGES = {'faq', 'get-in-touch', 'how-gumi-works', 'our-story',
                'privacy-policy', 'referral', 'shipping'}


class Report:
    def __init__(self): self.ok = self.red = 0

    def _log(self, good, tag, extra=''):
        self.ok, self.red = self.ok + good, self.red + (not good)
        print(f"  {'ok  ' if good else 'RED '} {tag}{'' if good else extra}")

    def eq(self, tag, got, want):
        self._log(got == want, tag, f'   got={got!r} want={want!r}')

    def near(self, tag, got, want, tol=0.6):
        self._log(got is not None and abs(got - want) <= tol, tag,
                  f'   got={got!r} want={want}±{tol}')

    def true(self, tag, cond, extra=''):
        self._log(bool(cond), tag, f'   {extra}')


# --- strips: put the pre-r96 value back as inline style ------------------------
STRIP_PANEL = """() => {
  const p = document.querySelector('.gb-header__panel'); if (!p) return 0;
  p.style.setProperty('border-top-width', '1px', 'important');
  p.style.setProperty('border-bottom-width', '1px', 'important');
  p.style.setProperty('border-color', 'transparent', 'important');
  return 1;
}"""
STRIP_LEAD = """() => {
  const n = document.querySelectorAll('.gb-page-hero__lead--lg, .gb-page-hero__lead--text-page');
  n.forEach(e => e.style.setProperty('color', '#1a1a1a', 'important'));
  return n.length;
}"""
STRIP_TITLE = """() => {
  const n = document.querySelectorAll('.gb-page-hero__title');
  n.forEach(e => e.style.setProperty('padding-right', '0', 'important'));
  return n.length;
}"""
STRIP_GAP = """() => {
  const n = document.querySelectorAll('.gb-science--tight .gb-science-card');
  n.forEach(e => e.style.setProperty('gap', '16px', 'important'));
  return n.length;
}"""
STRIP_ACC = """() => {
  const n = document.querySelectorAll('.gb-faq__list');
  n.forEach(e => e.style.setProperty('--acc-gap', '16px'));
  return n.length;
}"""
STRIP_ANIM = """() => {
  const n = document.querySelectorAll('.gb-crev-card');
  n.forEach(e => e.style.setProperty('animation', 'none', 'important'));
  return n.length;
}"""
STRIP_RAIL = """() => {
  const t = document.querySelector('.gb-expert__cards');
  if (!t || !t.swiper) return 0;
  const gap = parseFloat(getComputedStyle(t).columnGap) || 0;
  const centred = matchMedia('(max-width: 767px)').matches;
  t.swiper.destroy(true, true);
  const sw = new Swiper(t, {slidesPerView:'auto', spaceBetween:gap, speed:0, rewind:true,
    centeredSlides:centred, initialSlide:1, a11y:false, keyboard:false});
  // main.js's click handler still closes over the instance we just destroyed,
  // so without this the button is dead and the rail never leaves initialSlide.
  t.closest('[data-slider]').querySelector('[data-slider-next]')
   .addEventListener('click', function () { sw.slideNext(); });
  return 1;
}"""

PANEL = """() => {
  const p = document.querySelector('.gb-header__panel'), cs = getComputedStyle(p);
  return {h:+p.getBoundingClientRect().height.toFixed(2), bt:cs.borderTopWidth,
          bb:cs.borderBottomWidth, btc:cs.borderTopColor};
}"""
HERO = """() => {
  const h = document.querySelector('.gb-page-hero');
  const t = h.querySelector('.gb-page-hero__title');
  const l = h.querySelector('.gb-page-hero__lead');
  return {lead: l ? getComputedStyle(l).color : null,
          pr: parseFloat(getComputedStyle(t).paddingRight)};
}"""
RAIL = """() => {
  const t = document.querySelector('.gb-expert__cards');
  const r = t.getBoundingClientRect();
  const spans = [...t.querySelectorAll('.swiper-slide')]
    .map(s => s.getBoundingClientRect())
    .map(b => [Math.max(b.left, r.left), Math.min(b.right, r.right)])
    .filter(([a, b]) => b > a).sort((a, b) => a[0] - b[0]);
  if (!spans.length) return null;
  return {L:+(spans[0][0]-r.left).toFixed(1), R:+(r.right-spans[spans.length-1][1]).toFixed(1)};
}"""


def run(strip):
    rep = Report()

    def do_strip(pg, js, tag, want_positive=True):
        """Apply a strip, then wait out the transition it fights.

        ⚠ padding-bottom and border-width are both transitioned here, so reading
        straight after the write returns the START value and every assertion
        passes on stale numbers -- [[headless-transition-reads-start-value]].
        """
        n = pg.evaluate(js)
        if want_positive:
            rep.true(tag, n > 0, f'touched {n}')
        pg.wait_for_timeout(450)
        return n

    with sync_playwright() as pw:
        br = pw.chromium.launch(executable_path=CHROME)

        # -- 0. review cards animate in when the pager un-hides them ------------
        print('0  crev card reveal')
        pg = br.new_page(viewport={'width': 1440, 'height': 900})
        pg.goto(f'{ROOT}/reviews.html'); pg.wait_for_timeout(900)
        if strip: do_strip(pg, STRIP_ANIM, '0 strip touched cards')
        # The pager hides everything past the 5th; un-hiding must restart the
        # animation, so getAnimations() is non-empty right after the click.
        got = pg.evaluate("""() => {
          const cards = [...document.querySelectorAll('.gb-crev-card')];
          const hid = cards.filter(c => c.hidden).length;
          document.querySelector('[data-crev-more]').click();
          const fresh = cards.filter(c => !c.hidden).slice(-1)[0];
          const an = fresh.getAnimations();
          return {hidBefore: hid, name: an.length ? an[0].animationName : null,
                  playing: an.length ? an[0].playState : null,
                  op: getComputedStyle(fresh).opacity};
        }""")
        rep.true('0a pager had cards to reveal', got['hidBefore'] > 0, str(got))
        rep.eq('0b revealed card runs gm-crev-in', got['name'], 'gm-crev-in')
        rep.eq('0c and it is running, not finished', got['playing'], 'running')
        rep.true('0d opacity has not landed yet', float(got['op']) < 1, str(got['op']))
        # ⚠ and it must actually land -- an entrance that leaves opacity pinned
        # is worse than none ([[reveal-gate-must-track-module-liveness]]).
        pg.wait_for_timeout(600)
        rep.eq('0e opacity lands on 1', pg.evaluate(
            "() => getComputedStyle([...document.querySelectorAll('.gb-crev-card')]"
            ".filter(c=>!c.hidden).slice(-1)[0]).opacity"), '1')
        pg.close()

        # -- 0b. crevPager stands down where the live section's own pager runs --
        print('0b crevPager yields to the live inline pager')
        pg = br.new_page(viewport={'width': 1440, 'height': 900})
        pg.goto(f'{ROOT}/reviews.html'); pg.wait_for_timeout(900)
        # A CLONE, so the handler main.js already bound on the real button cannot
        # answer the click and make a dead guard look alive.
        d = pg.evaluate("""() => {
          const real = document.querySelector('[data-crev-list]');
          const before = [...real.querySelectorAll('.gb-crev-card')].filter(c => c.hidden).length;
          const sec = real.closest('.gb-app-section').cloneNode(true);
          document.body.appendChild(sec);
          const list = sec.querySelector('[data-crev-list]');
          const cards = [...list.querySelectorAll('.gb-crev-card')];
          cards.forEach(c => { c.hidden = false; });

          // (a) without the live marker the pager must still page the clone
          window.gumi.crevPager.wire(list);
          const paged = cards.filter(c => c.hidden).length;

          // (b) with it, wire() must do nothing at all
          cards.forEach(c => { c.hidden = false; c.setAttribute('data-review-id', '1'); });
          window.gumi.crevPager.wire(list);
          const guarded = cards.filter(c => c.hidden).length;
          sec.remove();
          return {before: before, paged: paged, guarded: guarded, n: cards.length};
        }""")
        rep.true('0f pager was actually paging before', d['before'] > 0, str(d))
        rep.true('0g wire() still pages OUR markup', d['paged'] > 0, str(d))
        rep.eq('0h guard makes wire() a no-op on live markup', d['guarded'], 0)
        pg.close()

        # -- 1. faq rows back to 24 --------------------------------------------
        print('1  faq --acc-gap 24')
        for w in (390, 767, 768, 1440):
            pg = br.new_page(viewport={'width': w, 'height': 900})
            pg.goto(f'{ROOT}/faq.html'); pg.wait_for_timeout(400)
            if strip: do_strip(pg, STRIP_ACC, f'1 strip {w} touched lists')
            # Two rows are 0 by design: the [open] one (the panel takes over)
            # and the list's last child (r64 zeroes --acc-gap there). Grade the rest.
            v = pg.evaluate("""() => {
              const rows = [...document.querySelectorAll('.gb-faq__list .gb-faq__item')]
                .filter(i => !i.open && i !== i.parentElement.lastElementChild)
                .map(i => parseFloat(
                  getComputedStyle(i.querySelector('.gb-faq__row')).paddingBottom));
              return {n: rows.length, min: Math.min(...rows), max: Math.max(...rows)};
            }""")
            rep.true(f'1 {w:>4} found shut faq rows to grade', v['n'] >= 4, str(v))
            rep.near(f'1 {w:>4} .gb-faq__row padding-bottom min', v['min'], 24)
            rep.near(f'1 {w:>4} .gb-faq__row padding-bottom max', v['max'], 24)
            pg.close()

        # .gb-faq-image__list keeps its own 16/24 ramp -- only .gb-faq__list moved.
        for w, want in ((390, 24), (1440, 16)):
            pg = br.new_page(viewport={'width': w, 'height': 900})
            pg.goto(f'{ROOT}/science.html'); pg.wait_for_timeout(400)
            v = pg.evaluate("""() => {
              const rows = [...document.querySelectorAll('.gb-faq-image__list .gb-faq__item')]
                .filter(i => !i.open && i !== i.parentElement.lastElementChild)
                .map(i => parseFloat(
                  getComputedStyle(i.querySelector('.gb-faq__row')).paddingBottom));
              return {n: rows.length, min: Math.min(...rows)};
            }""")
            rep.true(f'1 {w:>4} found shut faq-image rows', v['n'] >= 1, str(v))
            rep.near(f'1 {w:>4} .gb-faq-image__list untouched', v['min'], want)
            pg.close()

        # -- 2. header panel carries no border while shut -----------------------
        print('2  header panel border')
        for w in (1440, 900):
            pg = br.new_page(viewport={'width': w, 'height': 800})
            pg.goto(f'{ROOT}/reviews.html'); pg.wait_for_timeout(400)
            if strip: do_strip(pg, STRIP_PANEL, f'2 strip {w} touched panel')
            d = pg.evaluate(PANEL)
            rep.near(f'2 {w:>4} shut height is 0, not a 2px cream bar', d['h'], 0)
            rep.eq(f'2 {w:>4} shut border-top', d['bt'], '0px')
            rep.eq(f'2 {w:>4} shut border-bottom', d['bb'], '0px')
            pg.evaluate("document.querySelector('.gb-header').classList.add('is-open')")
            pg.wait_for_timeout(700)   # transition start value trap
            d = pg.evaluate(PANEL)
            rep.eq(f'2 {w:>4} open border-top', d['bt'], '1px')
            rep.eq(f'2 {w:>4} open border colour', d['btc'], SAND)
            pg.close()
        pg = br.new_page(viewport={'width': 390, 'height': 800})
        pg.goto(f'{ROOT}/reviews.html'); pg.wait_for_timeout(400)
        pg.evaluate("document.querySelector('.gb-header').classList.add('is-open')")
        pg.wait_for_timeout(900)
        d = pg.evaluate(PANEL)
        rep.eq('2  390 drawer open keeps border-top off', d['bt'], '0px')
        rep.eq('2  390 drawer open keeps border-bottom off', d['bb'], '0px')
        pg.close()

        # -- 3 & 5. lead colour + title inset ----------------------------------
        print('3  lead colour  /  5  title inset')
        for w, want_pr in ((390, 30), (767, 30), (768, 30), (1281, 0), (1440, 0)):
            pg = br.new_page(viewport={'width': w, 'height': 900})
            for p in HERO_PAGES:
                pg.goto(f'{ROOT}/{p}.html'); pg.wait_for_timeout(260)
                if strip:
                    do_strip(pg, STRIP_LEAD, f'3 strip {p} {w} leads', want_positive=False)
                    pg.evaluate(STRIP_TITLE)
                d = pg.evaluate(HERO)
                if d['lead'] is not None:
                    rep.eq(f'3 {w:>4} {p:<15} lead #4d4d4d', d['lead'], GREY)
                rep.near(f'5 {w:>4} {p:<15} title padding-right',
                         d['pr'], 0 if p in CENTRE_PAGES else want_pr)
            pg.close()
        # No step across the 1280/1281 seam on the two pages that carry the inset
        pg = br.new_page(viewport={'width': 1280, 'height': 900})
        for p in ('science', 'reviews'):
            pg.goto(f'{ROOT}/{p}.html'); pg.wait_for_timeout(260)
            if strip: pg.evaluate(STRIP_TITLE)
            rep.near(f'5 1280 {p} inset has ramped out (no 1281 step)',
                     pg.evaluate(HERO)['pr'], 0, 0.3)
        pg.close()

        # -- 4. tight science cards ------------------------------------------
        print('4  tight science card gap')
        for w in (390, 767, 1440):
            pg = br.new_page(viewport={'width': w, 'height': 900})
            pg.goto(f'{ROOT}/science.html'); pg.wait_for_timeout(400)
            if strip: do_strip(pg, STRIP_GAP, f'4 strip {w} touched cards')
            d = pg.evaluate("""() => {
              const g = s => parseFloat(getComputedStyle(
                document.querySelector(s + ' .gb-science-card')).rowGap);
              return {tight: g('.gb-science--tight'),
                      base: g('.gb-science:not(.gb-science--tight)')};
            }""")
            rep.near(f'4 {w:>4} tight card gap 22', d['tight'], 22)
            rep.near(f'4 {w:>4} plain card untouched at 16', d['base'], 16)
            pg.close()

        # -- 6. expert rail edges ---------------------------------------------
        print('6  expert rail edges')
        for w in (390, 575, 767):
            pg = br.new_page(viewport={'width': w, 'height': 900})
            pg.goto(f'{ROOT}/reviews.html'); pg.wait_for_timeout(1000)
            if strip: do_strip(pg, STRIP_RAIL, f'6 strip {w} rebuilt rail')
            worst_l = worst_r = 0.0
            for i in range(5):     # a full rewind cycle and then some
                d = pg.evaluate(RAIL)
                if d: worst_l, worst_r = max(worst_l, d['L']), max(worst_r, d['R'])
                pg.evaluate("document.querySelector('.gb-expert__nav [data-slider-next]').click()")
                pg.wait_for_timeout(650)
            d = pg.evaluate(RAIL)
            if d: worst_l, worst_r = max(worst_l, d['L']), max(worst_r, d['R'])
            rep.near(f'6 {w:>4} no gap at the left edge, any position', worst_l, 0, 1.0)
            rep.near(f'6 {w:>4} no gap at the right edge, any position', worst_r, 0, 1.0)
            pg.close()

        # -- 6b. the four loop reels must not have picked the option up --------
        print('6b loop reels untouched')
        for pgname in ('index', 'pdp', 'our-story', 'how-gumi-works'):
            pg = br.new_page(viewport={'width': 390, 'height': 900})
            pg.goto(f'{ROOT}/{pgname}.html'); pg.wait_for_timeout(1100)
            d = pg.evaluate("""() => {
              const t = document.querySelector('[data-slider-track]');
              if (!t || !t.swiper) return null;
              return [t.swiper.params.loop, t.swiper.params.centeredSlidesBounds];
            }""")
            # An endless rail has no first or last slide, so the option would only
            # have side effects there -- main.js gates it on `!loop`.
            rep.eq(f'6b {pgname:<15} loop rail keeps bounds off', d, [True, False])
            pg.close()

        br.close()
    print(f'\n{rep.ok} ok / {rep.red} red')
    return rep.red


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--strip', action='store_true')
    a = ap.parse_args()
    raise SystemExit(1 if (run(a.strip) and not a.strip) else 0)
