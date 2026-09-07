#!/usr/bin/env python3
"""Every scallop, static vs live: size, the two colours it blends, and the
colour actually painted underneath it.

    python3 tools/wavecheck.py --password 1234
    python3 tools/wavecheck.py --password 1440 --width 390

On live the wave is a section setting (`gb-scallop--{{ s.trailing_scallop }}`),
on the static site it is written into the markup -- so this is the only place
the two vocabularies meet, and a wrong pick shows up as --wave-fg disagreeing
with the ground below it.

Waves are matched by ORDER within the page, not by class: the class is exactly
what may be wrong, and a page whose section list differs will show up as a count
mismatch rather than as a string of bogus colour diffs.
"""
import argparse, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
SITE = 'https://gumi.com.au'
PAGES = {'index': '/', 'pdp': '/products/superfood-greens-gummies',
         'science': '/pages/science', 'reviews': '/pages/reviews',
         'how-gumi-works': '/pages/how-gumi-works', 'our-story': '/pages/our-story',
         'faq': '/pages/faq', 'get-in-touch': '/pages/get-in-touch',
         'referral': '/pages/referral', 'privacy-policy': '/pages/privacy-policy',
         'shipping': '/pages/shipping'}

PROBE = """() => {
  const hex = (c) => {
    const m = /rgba?\\((\\d+), (\\d+), (\\d+)(?:, ([\\d.]+))?\\)/.exec(c || '');
    if (!m) return c;
    if (m[4] !== undefined && parseFloat(m[4]) === 0) return 'transparent';
    return '#' + [1,2,3].map(i => (+m[i]).toString(16).padStart(2,'0')).join('');
  };
  // What is painted at a point: walk up until something is not transparent.
  const groundAt = (x, y) => {
    let el = document.elementFromPoint(x, y);
    while (el) {
      const bg = getComputedStyle(el).backgroundColor;
      if (bg && !/rgba\\(0, 0, 0, 0\\)/.test(bg)) return hex(bg);
      el = el.parentElement;
    }
    return null;
  };
  const out = [];
  for (const sc of document.querySelectorAll('.gb-scallop')) {
    const cs = getComputedStyle(sc);
    const r = sc.getBoundingClientRect();
    const mods = (sc.getAttribute('class') || '').split(/\\s+/)
      .filter(c => c.startsWith('gb-scallop--'))
      .map(c => c.slice('gb-scallop--'.length));
    sc.scrollIntoView({ block: 'center' });
    const b = sc.getBoundingClientRect();
    const x = Math.round(window.innerWidth / 2);
    out.push({
      mods: mods.join(' '),
      h: Math.round(r.height),
      fg: hex(cs.getPropertyValue('--wave-fg').trim()) || cs.getPropertyValue('--wave-fg').trim(),
      bg: hex(cs.getPropertyValue('--wave-bg').trim()) || cs.getPropertyValue('--wave-bg').trim(),
      under: b.height ? groundAt(x, Math.round(b.bottom) + 8) : null,
      over: b.height ? groundAt(x, Math.round(b.top) - 8) : null,
    });
  }
  return out;
}"""


def collect(ctx, url):
    pg = ctx.new_page()
    pg.goto(url, wait_until='networkidle', timeout=45000)
    pg.wait_for_timeout(600)
    pg.evaluate("() => document.querySelectorAll('.wowo').forEach(e => e.classList.remove('wowo'))")
    r = pg.evaluate(PROBE)
    pg.close()
    return r


def main():
    from playwright.sync_api import sync_playwright
    ap = argparse.ArgumentParser()
    ap.add_argument('--password'); ap.add_argument('--width', type=int, default=1440)
    ap.add_argument('--page', action='append')
    a = ap.parse_args()
    pages = a.page or list(PAGES)
    bad = 0

    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME)
        cs = b.new_context(viewport={'width': a.width, 'height': 1000})
        cl = None
        if a.password:
            cl = b.new_context(viewport={'width': a.width, 'height': 1000})
            r = cl.request.post(SITE + '/password', form={
                'form_type': 'storefront_password', 'utf8': '✓', 'password': a.password})
            if r.status in (429, 503):
                raise SystemExit('Cloudflare (HTTP %d) -- back off' % r.status)

        for name in pages:
            st = collect(cs, (ROOT / (name + '.html')).as_uri())
            lv = collect(cl, SITE + PAGES[name]) if cl else []
            print('\n== %s @%d   static %d waves / live %d ==' % (name, a.width, len(st), len(lv)))
            if cl and len(st) != len(lv):
                print('   ⚠ count differs -- section list is not the same, rows below are NOT aligned')
                bad += 1
            for i in range(max(len(st), len(lv))):
                s = st[i] if i < len(st) else None
                l = lv[i] if i < len(lv) else None
                f = lambda d, k: ('-' if not d else str(d[k]))
                flag = ''
                if s and l:
                    if s['mods'] != l['mods'] or s['h'] != l['h']: flag = '  <-- DIFF'
                if l and l['under'] and l['fg'] not in ('transparent', None) and l['under'] != l['fg']:
                    flag += '  [live fg != ground below]'
                if flag: bad += 1
                print('  %2d  static %-26s h=%-4s fg=%-11s under=%-9s | live %-26s h=%-4s fg=%-11s under=%-9s%s'
                      % (i, f(s, 'mods'), f(s, 'h'), f(s, 'fg'), f(s, 'under'),
                         f(l, 'mods'), f(l, 'h'), f(l, 'fg'), f(l, 'under'), flag))
        b.close()
    print('\n%d rows flagged' % bad)


if __name__ == '__main__':
    main()
