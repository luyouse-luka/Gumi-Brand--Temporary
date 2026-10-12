#!/usr/bin/env python3
"""The header menu's keyboard path.

  python3 tools/menutab.py                      # static build
  python3 tools/menutab.py --live --password 1234

The panel and its sublists are shut by geometry, never by display, so before
this round everything inside stayed in the tab order while invisible: 6 dead
stops on desktop, 19 in the phone drawer, plus 4 more on the bar the open drawer
covers. Graded here:

  A  no Tab stop lands on something the user cannot see
  B  focus entering the panel opens the menu
  C  focus entering a shut sublist expands it
  D  focus leaving the header closes the menu again
  E  the open phone drawer inerts the bar it covers, and takes focus with it
  F  Escape closes and hands focus back to the toggle
  G  regression: the toggle still opens and closes on click
  H  r115: Tab landing on the toggle opens the menu, a mouse click does not,
     and Escape's hand-back to the toggle does not reopen it
  I  r116: desktop Tab runs toggle -> whole menu -> rest of the bar -> page,
     and Shift+Tab undoes both seams
"""
import argparse, pathlib, sys
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
LIVE = 'https://gumi.com.au'
ok = red = 0

WHERE = """() => {
  const a = document.activeElement;
  if (!a || a === document.body) return null;
  const b = a.getBoundingClientRect();
  const cx = b.left + b.width / 2, cy = b.top + b.height / 2;
  const hit = document.elementFromPoint(cx, cy);
  return {tag: a.tagName,
          cls: (typeof a.className === 'string' ? a.className : '').slice(0, 30),
          txt: (a.textContent || a.getAttribute('aria-label') || '').trim().slice(0, 20),
          aria: (a.getAttribute('aria-label') || '').trim(),
          inHeader: !!a.closest('#site-header'), inPanel: !!a.closest('.gb-header__panel'),
          inBar: !!a.closest('.gb-header__bar'),
          menuOpen: !!document.querySelector('.gb-header.is-open'),
          onScreen: b.width > 0 && b.height > 0 && b.bottom > 0 && b.top < innerHeight
                    && b.right > 0 && b.left < innerWidth,
          // catches "painted under the drawer" -- geometry alone cannot
          hitSelf: !!(hit && (hit === a || a.contains(hit) || hit.contains(a)))};
}"""


def grade(cond, label, detail=''):
    global ok, red
    if cond:
        ok += 1
    else:
        red += 1
        print(f'  RED  {label}   {detail}')


def prep(pg, url, w, h):
    pg.set_viewport_size({'width': w, 'height': h})
    pg.goto(url, wait_until='domcontentloaded', timeout=90000)
    pg.wait_for_timeout(1400)
    # the promo modal traps focus by design; it is not what this grades
    pg.evaluate("() => { const m = document.getElementById('promo-modal'); if (m) m.remove(); }")
    pg.evaluate("() => { document.activeElement && document.activeElement.blur(); }")


SETTLE = """() => new Promise(res => {
  // $t-drawer is 0.7s and a sublist's 0fr -> 1fr row is 0.3s: measuring mid-move
  // reports drawer links offscreen, or -- since a growing row has nothing to
  // scroll yet -- still sitting under the drawer's fixed CTA.
  // ⚠ "the rect stopped changing" is NOT enough on its own: $ease-in-out starts
  // at zero velocity, so the first frames of the row round to the same integers
  // and a frame-diff settles instantly. Wait for the header to have no running
  // transition at all, then for the geometry to hold.
  const h = document.getElementById('site-header');
  const p = document.querySelector('.gb-header__panel');
  if (!p || !h) return res(0);
  let last = null, still = 0;
  const t0 = performance.now();
  const busy = () => h.getAnimations
    ? h.getAnimations({subtree: true}).some(a => a.playState === 'running') : false;
  const tick = () => {
    if (performance.now() - t0 > 1500) return res(2);   // never hang the walk
    const a = document.activeElement;
    const ar = a ? a.getBoundingClientRect() : null;
    const now = getComputedStyle(p).transform + '|' + p.getBoundingClientRect().top
              + '|' + (ar ? Math.round(ar.top) + ',' + Math.round(ar.bottom) : '-');
    still = (now === last && !busy()) ? still + 1 : 0;
    last = now;
    if (still >= 3) return res(1);
    requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
})"""


def walk(pg, n):
    seen = []
    pg.keyboard.press('Tab')
    for _ in range(n):
        pg.wait_for_timeout(60)
        pg.evaluate(SETTLE)
        m = pg.evaluate(WHERE)
        if not m:
            break
        seen.append(m)
        pg.keyboard.press('Tab')
    return seen


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--live', action='store_true')
    ap.add_argument('--password')
    a = ap.parse_args()
    if a.live and not a.password:
        sys.exit('--live needs --password')
    url = (LIVE + '/') if a.live else (ROOT / 'index.html').as_uri()

    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME)
        ctx = b.new_context(viewport={'width': 1440, 'height': 900})
        if a.live:
            ctx.request.post(LIVE + '/password', form={
                'form_type': 'storefront_password', 'utf8': '✓', 'password': a.password})
        pg = ctx.new_page()

        for w, h, steps in ((1440, 900, 26), (390, 844, 30)):
            print(f'--- A. tab walk @{w}x{h} ---')
            prep(pg, url, w, h)
            stops = walk(pg, steps)
            # Only the header is this judge's business. A page control can read
            # "covered" for reasons of its own (sticky bar, an entrance animation
            # mid-flight) and grading those here would make the result noise.
            blind = [s for s in stops
                     if s['inHeader']
                     and (not s['onScreen'] or not s['hitSelf']
                          or (s['inPanel'] and not s['menuOpen']))]
            for s in blind:
                print(f"    blind stop: {s['tag']} .{s['cls']} {s['txt']!r} "
                      f"onScreen={s['onScreen']} hitSelf={s['hitSelf']} open={s['menuOpen']}")
            grade(not blind, f'{w}: every Tab stop is visible where it lands',
                  f'{len(blind)} blind of {len(stops)}')
            panel_stops = [s for s in stops if s['inPanel']]
            grade(panel_stops, f'{w}: the walk did reach the panel at all',
                  'never entered -- this judge would pass vacuously')
            grade(all(s['menuOpen'] for s in panel_stops),
                  f'{w}: and the menu was open for every one of them',
                  f"{sum(1 for s in panel_stops if not s['menuOpen'])} shut")
            last_panel = max((i for i, s in enumerate(stops) if s['inPanel']), default=-1)
            after = [s for s in stops[last_panel + 1:] if not s['inHeader']]
            grade(after, f'{w}: and Tab carries on into the page afterwards',
                  'the walk ended inside the menu')
            grade(not any(s['menuOpen'] for s in after),
                  f'{w}: which shuts the menu behind it',
                  f"{sum(1 for s in after if s['menuOpen'])} page stops with it still open")
            print(f"  {len(stops)} stops, {len(panel_stops)} of them in the panel")

        print('--- B/C/D. focus opens, expands, and lets go ---')
        for w, h in ((1440, 900), (390, 844)):
            prep(pg, url, w, h)
            grade(not pg.evaluate("!!document.querySelector('.gb-header.is-open')"),
                  f'{w}: menu starts shut')
            picked = pg.evaluate("""() => { const a = [...document.querySelectorAll(
                '.gb-header__panel a.gb-header__link')].find(
                  e => e.getClientRects().length > 0);
                if (a) { a.focus(); return a.textContent.trim().slice(0, 20); }
                return null; }""")
            grade(picked, f'{w}: found a panel link that is laid out at all')
            pg.wait_for_timeout(250)
            grade(pg.evaluate("!!document.querySelector('.gb-header.is-open')"),
                  f'{w}: B. focusing a panel link opens the menu')
            # C -- only the phone list carries collapsibles
            has_sub = pg.evaluate("""() => { const s = [...document.querySelectorAll(
                '.gb-header__sublist a')].find(e => e.getClientRects().length > 0);
                if (!s) return null;
                s.focus();
                const item = s.closest('[data-collapsible]');
                return {open: item.classList.contains('is-open'),
                        aria: item.querySelector('.gb-header__link').getAttribute('aria-expanded')}; }""")
            if has_sub:
                grade(has_sub['open'], f'{w}: C. focusing a sublink expands its group')
                grade(has_sub['aria'] == 'true', f'{w}: and says so in aria-expanded',
                      str(has_sub['aria']))
            # D -- leave the header
            pg.evaluate("""() => { const t = document.querySelector(
                'main a, main button, #MainContent a, #MainContent button');
                if (t) t.focus(); }""")
            pg.wait_for_timeout(250)
            grade(not pg.evaluate("!!document.querySelector('.gb-header.is-open')"),
                  f'{w}: D. focus leaving the header shuts the menu')

        print('--- E. the phone drawer inerts the bar it covers ---')
        prep(pg, url, 390, 844)
        pg.click('.gb-header__toggle')
        pg.wait_for_timeout(700)
        m = pg.evaluate("""() => ({
            open: !!document.querySelector('.gb-header.is-open'),
            inert: document.querySelector('.gb-header__bar').hasAttribute('inert'),
            active: document.activeElement.className,
            inPanel: !!document.activeElement.closest('.gb-header__panel')})""")
        grade(m['open'], 'E. clicking the toggle opens the drawer')
        grade(m['inert'], 'E. and inerts the bar behind it')
        grade(m['inPanel'], 'E. and moves focus into the drawer', m['active'])
        stops = walk(pg, 10)
        grade(not any(s['inBar'] for s in stops),
              'E. Tab no longer visits the covered bar',
              str([s['cls'] for s in stops if s['inBar']]))
        grade(all(s['onScreen'] and s['hitSelf'] for s in stops if s['inHeader']),
              'E. and every header stop from there is visible',
              str([s['cls'] for s in stops if s['inHeader']
                   and not (s['onScreen'] and s['hitSelf'])]))

        print('--- F. Escape ---')
        prep(pg, url, 390, 844)
        pg.click('.gb-header__toggle')
        pg.wait_for_timeout(600)
        pg.keyboard.press('Escape')
        pg.wait_for_timeout(600)
        m = pg.evaluate("""() => ({open: !!document.querySelector('.gb-header.is-open'),
            inert: document.querySelector('.gb-header__bar').hasAttribute('inert'),
            onToggle: document.activeElement.classList.contains('gb-header__toggle')})""")
        grade(not m['open'], 'F. Escape shuts the menu')
        grade(not m['inert'], 'F. and gives the bar back')
        grade(m['onToggle'], 'F. and hands focus back to the toggle')

        print('--- G. the toggle still toggles ---')
        for w, h in ((1440, 900), (390, 844)):
            prep(pg, url, w, h)
            pg.click('.gb-header__toggle')
            pg.wait_for_timeout(500)
            grade(pg.evaluate("!!document.querySelector('.gb-header.is-open')"),
                  f'{w}: G. click opens')
            closer = ('.gb-header__panel-close' if w <= 767 else '.gb-header__toggle')
            pg.click(closer)
            pg.wait_for_timeout(700)
            grade(not pg.evaluate("!!document.querySelector('.gb-header.is-open')"),
                  f'{w}: G. click closes again')
        print('--- H. Tab onto the toggle opens the menu ---')
        for w, h in ((1440, 900), (390, 844)):
            prep(pg, url, w, h)
            grade(not pg.evaluate("!!document.querySelector('.gb-header.is-open')"),
                  f'{w}: H. starts shut')
            # On the phone the open drawer takes focus off the toggle at once, so
            # "did we reach it" cannot be read after the fact -- stop on either.
            hit = None
            for i in range(6):
                pg.keyboard.press('Tab')
                pg.wait_for_timeout(90)
                hit = pg.evaluate("""() => ({
                    open: !!document.querySelector('.gb-header.is-open'),
                    onToggle: !!(document.activeElement && document.activeElement
                        .classList.contains('gb-header__toggle')),
                    inPanel: !!(document.activeElement &&
                        document.activeElement.closest('.gb-header__panel')),
                    active: ((document.activeElement || {}).className || '') + ''})""")
                if hit['open'] or hit['onToggle']:
                    break
            # inPanel counts as reaching it: on the phone the open drawer has
            # already pulled focus off the toggle by the time this reads back.
            grade(hit and (hit['onToggle'] or (hit['open'] and hit['inPanel'])),
                  f'{w}: H. Tab reaches the toggle',
                  f'stopped on {hit and hit["active"]!r} after {i + 1} tabs')
            grade(hit and hit['open'], f'{w}: H. and that alone opens the menu',
                  f'still shut after {i + 1} tabs')
            if w <= 767:
                pg.wait_for_timeout(800)
                grade(pg.evaluate(
                    """() => !!(document.activeElement &&
                        document.activeElement.closest('.gb-header__panel'))"""),
                    f'{w}: H. and hands focus to the drawer it just uncovered')
            # Escape now returns focus to the toggle, which is still :focus-visible
            # from the Tab -- without the guard the focus handler reopens it.
            pg.keyboard.press('Escape')
            pg.wait_for_timeout(900)
            m = pg.evaluate("""() => ({open: !!document.querySelector('.gb-header.is-open'),
                onToggle: !!(document.activeElement && document.activeElement
                    .classList.contains('gb-header__toggle'))})""")
            grade(m['onToggle'], f'{w}: H. Escape hands focus back to the toggle')
            grade(not m['open'], f'{w}: H. and it stays shut (no reopen loop)')

            # A mouse click must still open on the click, not open-then-close.
            prep(pg, url, w, h)
            pg.click('.gb-header__toggle')
            pg.wait_for_timeout(800)
            grade(pg.evaluate("!!document.querySelector('.gb-header.is-open')"),
                  f'{w}: H. pointer click still opens (focus did not eat it)')

        print('--- I. r116: the menu runs before the rest of the bar ---')
        # Desktop only. The phone drawer inerts the bar (graded in E), so there
        # is no second group to interleave and the order there is unchanged.
        prep(pg, url, 1440, 900)
        for _ in range(6):
            pg.keyboard.press('Tab')
            pg.wait_for_timeout(90)
            if pg.evaluate("""() => !!(document.activeElement && document.activeElement
                    .classList.contains('gb-header__toggle'))"""):
                break
        pg.wait_for_timeout(700)
        pg.evaluate(SETTLE)
        seq = []
        for _ in range(18):
            m = pg.evaluate(WHERE)
            if not m or not m['inHeader']:
                break
            seq.append(m)
            pg.keyboard.press('Tab')
            pg.wait_for_timeout(110)
            pg.evaluate(SETTLE)

        names = [f"{'P' if s['inPanel'] else 'B'}:{s['txt']!r}" for s in seq]
        grade(bool(seq) and 'gb-header__toggle' in seq[0]['cls'],
              '1440: I. the walk starts on the toggle', str(names[:3]))
        grade(len(seq) > 1 and seq[1]['inPanel'],
              '1440: I. the stop AFTER the toggle is inside the menu',
              f'got {names[1] if len(seq) > 1 else None}')
        # shape must be exactly toggle, then one solid panel run, then one solid
        # bar run -- interleaving would mean the reroute fired on the wrong seam
        rest = seq[1:]
        panel_run = 0
        while panel_run < len(rest) and rest[panel_run]['inPanel']:
            panel_run += 1
        tail = rest[panel_run:]
        grade(panel_run >= 3, '1440: I. the whole menu is walked before leaving it',
              f'{panel_run} panel stops: {names[1:1 + panel_run]}')
        grade(bool(tail) and all(s['inBar'] and not s['inPanel'] for s in tail),
              '1440: I. and the bar picks up straight after, unbroken',
              str([f"{s['inPanel']}/{s['inBar']}" for s in tail]))
        grade(bool(tail) and 'gb-header__logo' in tail[0]['cls'],
              '1440: I. the bar run restarts at the logo',
              f'got {tail[0]["cls"] if tail else None!r}')
        got = ' | '.join(f"{s['txt']}/{s['aria']}" for s in tail)
        for want, key in (('Shop now', 'txt'), ('Account', 'aria'), ('Cart', 'aria')):
            grade(any(want in s[key] for s in tail),
                  f'1440: I. bar run still reaches {want!r}', got)
        grade(all(s['onScreen'] for s in seq),
              '1440: I. every stop on the new path is visible',
              str([s['txt'] for s in seq if not s['onScreen']]))
        grade(all(s['menuOpen'] for s in seq[1:]),
              '1440: I. the menu stays open for the whole path')

        # Shift+Tab has to undo the same two seams, or the path is one-way.
        # Reopen first: the forward walk above ended past the header, which
        # closes the menu, and every seam early-returns while it is shut.
        pg.click('.gb-header__toggle')
        pg.wait_for_timeout(700)
        pg.evaluate(SETTLE)
        grade(pg.evaluate("!!document.querySelector('.gb-header.is-open')"),
              '1440: I. (setup) menu reopened for the reverse walk')
        pg.evaluate("""() => document.querySelector('.gb-header__logo').focus()""")
        pg.wait_for_timeout(120)
        pg.keyboard.press('Shift+Tab')
        pg.wait_for_timeout(160)
        m = pg.evaluate(WHERE)
        grade(bool(m) and m['inPanel'],
              '1440: I. Shift+Tab off the logo goes back into the menu',
              f'landed on {m and m["txt"]!r}')
        for _ in range(14):
            pg.keyboard.press('Shift+Tab')
            pg.wait_for_timeout(110)
            m = pg.evaluate(WHERE)
            if not m or not m['inPanel']:
                break
        grade(bool(m) and 'gb-header__toggle' in m['cls'],
              '1440: I. and walking back out of the menu lands on the toggle',
              f'landed on {m and m["cls"]!r}')

        b.close()
    print(f'\n{ok} ok / {red} red' + ('   [LIVE]' if a.live else '   [static]'))
    return 1 if red else 0


sys.exit(main())
