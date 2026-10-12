#!/usr/bin/env python3
"""Does the per-line entrance ever get cut short by the font landing late?

  python3 tools/linereveal.py [--live --password 1234] [--delay 800]

Before r132 lineReveal split at 500ms whether or not the brand font had arrived,
revealed straight away, then re-split on document.fonts.ready so the wrap points
were measured against the real metrics. groupLines() sends a host that is ALREADY
revealing to .is-settled -- the end state -- so a font that landed mid-run stopped
the entrance dead and the whole block appeared at once. Cold loads only: with the
font cached, fonts.ready beats the timer.

Reproduced without touching the network: document.fonts.ready is shadowed so it
resolves `--delay` ms after the real one.

RED = a host picked up .is-settled before its own lines were due to finish.
"""
import argparse
import sys

from playwright.sync_api import sync_playwright

CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
LIVE = 'https://gumi.com.au'

INIT = r'''(d => {
  const real = document.fonts.ready;
  Object.defineProperty(document.fonts, 'ready', {
    configurable: true,
    get: () => real.then(v => new Promise(r => setTimeout(() => r(v), d)))
  });
})(%DELAY%);
window.__lr = [];
window.__lrDue = 0;
addEventListener('DOMContentLoaded', () => {
  const t0 = performance.now();
  const cls = new WeakMap();
  const due = new WeakMap();
  new MutationObserver(ms => {
    for (const m of ms) {
      const el = m.target;
      if (!el.hasAttribute || !el.hasAttribute('data-line-reveal')) continue;
      const c = el.className;
      if (cls.get(el) === c) continue;
      cls.set(el, c);
      if (c.indexOf('is-revealed') >= 0 && el.getAnimations) {
        /* One frame later, not here: a MutationObserver callback runs before the
           style recalc that creates the CSS animations, so getAnimations() is
           empty at this point and every schedule would read as zero -- the judge
           would pass vacuously. */
        requestAnimationFrame(() => {
          let end = 0;
          for (const a of el.getAnimations({subtree: true})) {
            if (!a.effect) continue;
            const e = (a.startTime || 0) + (a.effect.getComputedTiming().endTime || 0);
            if (e > end) end = e;
          }
          if (end) { due.set(el, end); window.__lrDue++; }
        });
      }
      const owed = due.get(el) || 0;
      window.__lr.push({t: Math.round(performance.now() - t0), cls: c,
                        id: el.getAttribute('data-lr-id'),
                        early: (c.indexOf('is-settled') >= 0 && owed)
                               ? Math.round(owed - document.timeline.currentTime) : 0});
    }
  }).observe(document.documentElement, {subtree: true, attributes: true,
                                        attributeFilter: ['class']});
});'''

FINAL = """() => [...document.querySelectorAll('[data-line-reveal]')].map(e => {
  const r = e.getBoundingClientRect();
  return {id: e.getAttribute('data-lr-id'), op: getComputedStyle(e).opacity,
          onScreen: r.bottom > 0 && r.top < innerHeight,
          masks: e.querySelectorAll('.gb-line-mask').length};
})"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--live', action='store_true')
    ap.add_argument('--password')
    ap.add_argument('--delay', type=int, default=800)
    a = ap.parse_args()
    url = (LIVE + '/') if a.live else 'file:///home/ly/project/Gumi-Brand/index.html'

    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=CHROME)
        ctx = br.new_context(viewport={'width': 390, 'height': 844})
        if a.live and a.password:
            ctx.request.post(LIVE + '/password', form={
                'form_type': 'storefront_password', 'utf8': '✓', 'password': a.password})
        ctx.add_init_script(INIT.replace('%DELAY%', str(a.delay)))
        pg = ctx.new_page()
        pg.goto(url, wait_until='load', timeout=90000)
        pg.evaluate("""() => document.querySelectorAll('[data-line-reveal]')
            .forEach((e, i) => e.setAttribute('data-lr-id', 'lr' + i))""")
        pg.wait_for_timeout(6000)
        log = pg.evaluate('() => window.__lr') or []
        scheduled_n = pg.evaluate('() => window.__lrDue') or 0
        final = pg.evaluate(FINAL)
        br.close()

    cut = [r for r in log if r['early'] > 30]
    revealed = [r for r in log if 'is-revealed' in (r['cls'] or '')]

    hidden = [f for f in final if f['onScreen'] and float(f['op']) < 0.99]

    rows = [
        ('the entrance is never cut short by the re-split', not cut,
         ', '.join(f"{c['id']} settled {c['early']}ms early @{c['t']}ms"
                   for c in cut[:4]) or '0 cut', '0'),
        ('something actually revealed (probe is live)', len(revealed) > 0,
         f'{len(revealed)} reveals seen', '> 0'),
        ('a reveal schedule was captured (this judge can see "early" at all)',
         scheduled_n > 0, f'{scheduled_n} hosts timed', '> 0'),
        ('every host on screen ends visible', not hidden,
         f'{len(hidden)} still transparent', '0'),
        ('every host ended up split', all(f['masks'] > 0 for f in final),
         f"{sum(1 for f in final if not f['masks'])} unsplit of {len(final)}", '0'),
    ]
    red = 0
    for label, cond, got, want in rows:
        print(('  ok   ' if cond else '  RED  ') + f'{label}: {got}'
              + ('' if cond else f'  (want {want})'))
        red += 0 if cond else 1
    print(f'\n  fonts.ready held back {a.delay}ms; {len(log)} class changes logged')
    print(f'{len(rows) - red} ok / {red} red')
    sys.exit(1 if red else 0)


if __name__ == '__main__':
    main()
