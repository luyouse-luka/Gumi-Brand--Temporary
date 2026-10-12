#!/usr/bin/env python3
"""Every wave as a BOUNDARY, static vs live -- the input to the r104 restoration.

  python3 tools/r104map.py                    # static only
  python3 tools/r104map.py --password 1234    # both, aligned on the boundary

scallopmap.py keys on the HOST section, which stopped working once the waves
became their own sections on live: a static `--edge-top` wave belongs to the
section BELOW it, a live one belongs to neither. The boundary (name above ->
name below) is the only key both sides share, so it is the key here.

Reports, per boundary: rendered height, the two painted colours, and the
padding-bottom of the block above -- the three things the restoration touches.
"""
import argparse, sys
from playwright.sync_api import sync_playwright

CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
LIVE = 'https://gumi.com.au'
PAGES = {
    'index': '/', 'pdp': '/products/superfood-greens-gummies',
    'science': '/pages/science', 'reviews': '/pages/reviews',
    'how-gumi-works': '/pages/how-gumi-works', 'our-story': '/pages/our-story',
    'faq': '/pages/faq', 'get-in-touch': '/pages/get-in-touch',
    'referral': '/pages/referral', 'privacy-policy': '/pages/privacy-policy',
    'shipping': '/pages/shipping',
}

# One probe for both sides. A live wave is its own .shopify-section; a static one
# hangs off its host. Either way the boundary is read off the rendered box: the
# nearest top-level block whose bottom is above the wave, and the one below it.
PROBE = """() => {
  const px = (el) => { const c = getComputedStyle(el).backgroundColor;
                       return c === 'rgba(0, 0, 0, 0)' ? null : c; };
  const bgOf = (el) => { let n = el; while (n && n !== document.body) {
                           const c = px(n); if (c) return c; n = n.parentElement; }
                         return getComputedStyle(document.body).backgroundColor; };
  // Live wraps some modules in a `gb-<name>-section` div the static build has no
  // counterpart for, so the suffix is dropped -- both sides key on `gb-<name>`.
  const nameOf = (el) => {
    if (!el) return null;
    const self = [...el.classList].find(c => /^gb-[a-z-]+$/.test(c));
    const inner = el.querySelector('[class]');
    const c = self || (inner && [...inner.classList].find(c => /^gb-[a-z-]+$/.test(c)));
    let n = (c || el.id || el.tagName.toLowerCase()).replace(/-section$/, '');
    // The board keeps the CTA wave inside .gb-footer-cta-wrap; live has it as a
    // sibling of .gb-footer-cta-section. Same boundary, two spellings.
    return n === 'gb-footer-cta-wrap' ? 'gb-footer-cta' : n;
  };
  // The blocks a wave can sit between: top-level children of main/body plus the
  // wrappers Shopify introduces. A wave's own section is excluded.
  // The board puts the CTA wrapper and the footer AFTER </main>, as bare body
  // children; live has them as .shopify-section. Both spellings are candidates.
  const blocks = [...document.querySelectorAll(
      'main > *, body > .shopify-section, body > section, body > footer, '
      + '#shopify-section-footer-group > *')]
    .filter(el => !el.querySelector('.gb-wave') || el.querySelectorAll('*').length > 3);

  return [...document.querySelectorAll('.gb-scallop:not(.gb-scallop-box)')].map(w => {
    const cs = getComputedStyle(w), r = w.getBoundingClientRect();
    const mid = r.top + r.height / 2;
    let above = null, below = null;
    for (const b of blocks) {
      const br = b.getBoundingClientRect();
      if (br.height < 2) continue;
      // An --edge wave is absolutely positioned at its host's bottom, so the
      // host's bottom IS the wave's bottom -- keying `above` off bottom<=mid
      // skips the host and lands one section too early. Key off the top edge:
      // above = the lowest block that starts at or before the wave.
      // A block the wave OPENS is its `below`, never its `above`, even though it
      // starts at the same y -- that is the board's in-flow CTA wave.
      const opens = b.contains(w) && Math.abs(br.top - r.top) < 2;
      if (!opens && br.top <= r.top + 2
          && (!above || br.bottom > above.getBoundingClientRect().bottom)) above = b;
      if (br.top + 2 >= mid && (!below || br.top < below.getBoundingClientRect().top)) below = b;
      // In-flow wave that opens a block (the board's CTA wave): the block starts
      // where the wave starts, so the top-edge test above never reaches it.
      if (opens && !below) below = b;
    }
    const host = w.closest('section, footer, .shopify-section');
    return {
      cls: [...w.classList].filter(c => c.startsWith('gb-scallop--') || c === 'gb-wave')
                           .map(c => c.replace('gb-scallop--', '')).sort().join(' '),
      h: +r.height.toFixed(1),
      n: cs.getPropertyValue('--wave-n').trim() || '-',
      bg: cs.getPropertyValue('--wave-bg').trim(),
      fg: cs.getPropertyValue('--wave-fg').trim(),
      above: nameOf(above), below: nameOf(below),
      aboveBg: above ? bgOf(above) : null, belowBg: below ? bgOf(below) : null,
      abovePadB: above ? getComputedStyle(above.querySelector('section') || above).paddingBottom : null,
      top: +r.top.toFixed(1),
    };
  }).sort((a, b) => a.top - b.top);
}"""


def norm(c):
    """rgb()/hex -> (r,g,b), so the two sides compare on values not notation."""
    c = (c or '').strip()
    if c.startswith('rgb'):
        n = [int(x) for x in c.replace('rgba(', '').replace('rgb(', '').rstrip(')').split(',')[:3]
             if x.strip().lstrip('-').isdigit()]
        return tuple(n) if len(n) == 3 else None
    c = c.lstrip('#')
    if len(c) == 6:
        return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))
    return None


def near(a, b, tol=6):
    # A transparent top is a real value (the board's --to-lime), not a missing
    # one, and it parses to no RGB -- so match those two before parsing.
    ta, tb = (a or '').strip() in ('', 'transparent'), (b or '').strip() in ('', 'transparent')
    if ta or tb:
        return ta and tb
    a, b = norm(a), norm(b)
    return bool(a and b and all(abs(x - y) <= tol for x, y in zip(a, b)))


def show(r):
    tag = f"{r['above'] or '(top)'} -> {r['below'] or '(end)'}"
    return (f"{tag:<38} h={r['h']:<6} n={r['n']:<2} "
            f"{r['bg'] or 'transparent'} -> {r['fg']}   padB={r['abovePadB']}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--password')
    ap.add_argument('--all', action='store_true',
                    help='include the two in-flow footer waves (r102 left them un-migrated on purpose)')
    a = ap.parse_args()

    def keep(rows):
        return rows if a.all else [r for r in rows if r['below']]
    drift = 0
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=CHROME)
        ctx = br.new_context(viewport={'width': 1440, 'height': 900})
        if a.password:
            ctx.request.post(LIVE + '/password', form={
                'form_type': 'storefront_password', 'utf8': '✓', 'password': a.password})
            if not any(c['name'] == '_shopify_essential' for c in ctx.cookies()):
                sys.exit('storefront password rejected')
        pg = ctx.new_page()
        for name, path in PAGES.items():
            pg.goto(f'file:///home/ly/project/Gumi-Brand/{name}.html', wait_until='domcontentloaded')
            pg.wait_for_timeout(600)
            st = keep(pg.evaluate(PROBE))
            print(f'\n=== {name} ===')
            if not a.password:
                for r in st:
                    print('  ' + show(r))
                continue
            pg.goto(LIVE + path, wait_until='domcontentloaded', timeout=90000)
            pg.wait_for_timeout(800)
            lv = keep(pg.evaluate(PROBE))
            # Align on the boundary; a static wave with no live counterpart is a
            # missing wave, and a live one with no static counterpart is extra.
            used = set()
            for s in st:
                key = (s['above'], s['below'])
                m = next((i for i, l in enumerate(lv)
                          if i not in used and (l['above'], l['below']) == key), None)
                if m is None:
                    drift += 1
                    print(f"  MISSING on live   {show(s)}")
                    continue
                used.add(m)
                l = lv[m]
                same = abs(l['h'] - s['h']) < 1.5 and near(l['bg'], s['bg']) and near(l['fg'], s['fg'])
                if same:
                    print(f"  ok   {show(s)}")
                else:
                    drift += 1
                    print(f"  ≠    static  {show(s)}")
                    print(f"       live    {show(l)}")
            for i, l in enumerate(lv):
                if i not in used:
                    drift += 1
                    print(f"  EXTRA on live     {show(l)}")
        br.close()
    if a.password:
        print(f'\n{drift} boundary/boundaries differ between the static build and live')
    return 1 if drift else 0


if __name__ == '__main__':
    sys.exit(main())
