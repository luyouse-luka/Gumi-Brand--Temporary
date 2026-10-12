#!/usr/bin/env python3
"""A reel plays in the card it lives in -- no lightbox (client r123).

  python3 tools/reelplay.py
  python3 tools/reelplay.py --live --password 1234
  python3 tools/reelplay.py --strip     # inverted: break the hooks, must go RED

r123 replaced the shared #reel-video dialog with an in-card player. The whole
.gb-rv-* block (markup, styles, and modal.playVideo/stopVideo) is gone.

⚠ "The lightbox is gone" is a negative assertion, so group A proves the cards are
actually there first -- on a 404 or a renamed section the absence would be free.

⚠ A file:// preview cannot play a hosted URL: YouTube/Vimeo refuse a null origin.
Those cards get .gb-reel__offline instead of an <iframe>, which is why the judge
accepts either and checks the source to decide which one it should be.
"""
import argparse
import pathlib
import sys

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
LIVE = 'https://gumi.com.au'
PAGES = [('index.html', '/'), ('pdp.html', '/products/superfood-greens-gummies'),
         ('our-story.html', '/pages/our-story'), ('how-gumi-works.html', '/pages/how-gumi-works')]

fails, oks = [], []
backlog = []


def check(name, ok, detail=''):
    print(('  ok   ' if ok else '  FAIL ') + name + ('' if ok else '   ' + detail))
    (oks if ok else fails).append(name)


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

        print('=== A. every reel page still has cards, and no lightbox ===')
        for name, path in PAGES:
            url = (LIVE + path) if args.live else (ROOT / name).as_uri()
            try:
                pg.goto(url, wait_until='networkidle' if args.live else 'load', timeout=60000)
            except Exception as e:
                check('%s loads' % name, False, str(e)[:70]); continue
            pg.evaluate("() => document.querySelectorAll('.gb-promo-modal,.gb-promo-modal__overlay')"
                        ".forEach(e => e.remove())")
            if args.strip:   # plant what r123 removed: the assertion must notice
                pg.evaluate("() => { const d = document.createElement('div');"
                            " d.id = 'reel-video'; d.className = 'gb-rv-modal';"
                            " document.body.appendChild(d); }")
            d = pg.evaluate("""() => ({
              cards: document.querySelectorAll('[data-reel]').length,
              triggers: document.querySelectorAll('[data-reel-play]').length,
              lightbox: document.querySelectorAll('#reel-video, .gb-rv-modal, [data-modal="reel-video"]').length,
              rvClasses: document.querySelectorAll('[class*="gb-rv-"]').length,
              withSrc: [...document.querySelectorAll('[data-reel-play]')].filter(t => t.getAttribute('data-video')).length,
            })""")
            check('%s  cards present' % name, d['cards'] > 0, repr(d))       # liveness
            check('%s  trigger per card' % name, d['cards'] == d['triggers'], repr(d))
            check('%s  no lightbox left' % name, d['lightbox'] == 0 and d['rvClasses'] == 0, repr(d))
            # Content, not code: a reel block with no video filled in renders no
            # data-video and play() early-returns. That is a backlog item for the
            # theme editor, so it is summarised at the end rather than failing the
            # code judge -- but it IS reported, because those cards do nothing.
            if d['withSrc'] < d['triggers']:
                backlog.append((name, d['triggers'] - d['withSrc'], d['triggers']))
                print('  n/a  %s  %d of %d reels have no video filled in'
                      % (name, d['triggers'] - d['withSrc'], d['triggers']))
            else:
                check('%s  every trigger has a source' % name, True)

        print('\n=== B. clicking a card plays it in place ===')
        url = (LIVE + '/') if args.live else (ROOT / 'index.html').as_uri()
        pg.goto(url, wait_until='networkidle' if args.live else 'load', timeout=60000)
        pg.evaluate("() => document.querySelectorAll('.gb-promo-modal,.gb-promo-modal__overlay')"
                    ".forEach(e => e.remove())")
        if args.strip:
            # not the hook attribute -- the listener is already bound and the judge
            # falls back to the class. Removing the SOURCE makes play() early-return.
            pg.evaluate("() => document.querySelectorAll('[data-reel-play]')"
                        ".forEach(t => t.removeAttribute('data-video'))")

        # first card: click its trigger through JS so a Swiper drag cannot swallow it
        r = pg.evaluate("""() => {
          const card = document.querySelector('[data-reel]');
          const t = card && card.querySelector('[data-reel-play], .gb-reel__trigger');
          if (!t) return {clicked: false};
          t.click();
          return {clicked: true, src: t.getAttribute('data-video')};
        }""")
        check('B. a trigger was there to click', r['clicked'] is True, repr(r))
        pg.wait_for_timeout(400)
        st = pg.evaluate("""() => {
          const card = document.querySelector('[data-reel]');
          const node = card.querySelector('[data-reel-node]');
          const t = card.querySelector('.gb-reel__trigger');
          const tr = t ? t.getBoundingClientRect() : null;
          return {playing: card.classList.contains('is-playing'),
                  tag: node ? node.tagName : null,
                  cls: node ? node.className : null,
                  // ⚠ the ATTRIBUTE is not the effect: an author `display` outranks
                  // the UA's [hidden]{display:none}. r124 shipped a trigger that
                  // reported hidden:true and was still painted. Read all three.
                  triggerHidden: t ? t.hidden : null,
                  triggerDisplay: t ? getComputedStyle(t).display : null,
                  triggerBox: tr ? [Math.round(tr.width), Math.round(tr.height)] : null,
                  bodyLocked: document.documentElement.classList.contains('is-modal-open')};
        }""")
        check('B. player built in the card', st['tag'] in ('VIDEO', 'IFRAME', 'DIV'), repr(st))
        check('B. card marked is-playing', st['playing'] is True, repr(st))
        check('B. trigger hidden while playing', st['triggerHidden'] is True, repr(st))
        check('B. and actually removed from layout', st['triggerDisplay'] == 'none', repr(st))
        check('B. and painting nothing', st['triggerBox'] == [0, 0], repr(st))
        # the point of the change: no dialog, so no scroll lock
        check('B. page is NOT locked (no dialog opened)', st['bodyLocked'] is False, repr(st))
        # an mp4 must be a <video>, a hosted URL an <iframe> (or the file:// notice)
        if r.get('src'):
            hosted = ('youtube' in r['src'] or 'youtu.be' in r['src'] or 'vimeo' in r['src'])
            want = ('IFRAME', 'DIV') if hosted else ('VIDEO',)
            check('B. player type matches the source', st['tag'] in want,
                  'src=%r tag=%r' % (r['src'][:40], st['tag']))

        print('\n=== C. only one reel plays at a time ===')
        two = pg.evaluate("""() => {
          const cards = document.querySelectorAll('[data-reel]');
          if (cards.length < 2) return null;
          const t = cards[1].querySelector('[data-reel-play], .gb-reel__trigger');
          if (!t) return null;
          t.click();
          return true;
        }""")
        if two:
            pg.wait_for_timeout(400)
            c = pg.evaluate("""() => ({
              playing: document.querySelectorAll('[data-reel].is-playing').length,
              nodes: document.querySelectorAll('[data-reel-node]').length,
            })""")
            check('C. exactly one card playing', c['playing'] == 1 and c['nodes'] == 1, repr(c))
        else:
            print('  n/a  fewer than two reel cards on this page')

        b.close()

    print('\n%d ok / %d red' % (len(oks), len(fails)))
    print('RED: ' + ', '.join(fails) if fails else 'ALL GREEN')
    if backlog:
        print('\n⚠ theme-editor backlog (content, not code) -- docs/LIVE-BACKLOG.md:')
        for name, missing, total in backlog:
            print('    %-22s %d of %d reel blocks have no video -> those cards do nothing'
                  % (name, missing, total))
    if args.strip:
        print('\n--strip run: red above is the expected result.')
        return 0
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
