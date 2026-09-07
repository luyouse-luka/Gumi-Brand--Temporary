#!/usr/bin/env python3
"""Why does class X compute differently on live? Dump the real class attribute,
the ancestry and the winning declarations on both sides.

    python3 tools/gapwhy.py --password 1234 --page reviews --sel .gb-page-hero__lead
"""
import argparse, pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
SITE = 'https://gumi.com.au'
PAGES = {'index': '/', 'pdp': '/products/superfood-greens-gummies',
         'science': '/pages/science', 'reviews': '/pages/reviews',
         'how-gumi-works': '/pages/how-gumi-works', 'our-story': '/pages/our-story',
         'faq': '/pages/faq', 'get-in-touch': '/pages/get-in-touch',
         'referral': '/pages/referral', 'privacy-policy': '/pages/privacy-policy',
         'shipping': '/pages/shipping'}

DUMP = """(args) => {
  const [sel, props] = args;
  const out = [];
  document.querySelectorAll(sel).forEach((el, i) => {
    if (i > 2) return;
    const chain = [];
    for (let n = el; n && n.tagName !== 'HTML'; n = n.parentElement) {
      chain.push(n.tagName.toLowerCase() + (n.getAttribute('class') ? '.' + n.getAttribute('class').trim().split(/\\s+/).join('.') : ''));
    }
    const cs = getComputedStyle(el);
    const vals = {};
    props.forEach(p => vals[p] = cs.getPropertyValue(p));
    // which stylesheet rules actually match
    const hits = [];
    for (const sheet of document.styleSheets) {
      let rules; try { rules = sheet.cssRules; } catch (e) { continue; }
      const walk = (rs, media) => {
        for (const r of rs) {
          if (r.cssRules && !r.selectorText) { walk(r.cssRules, (media?media+' ':'') + (r.conditionText||'')); continue; }
          if (!r.selectorText) continue;
          let m = false; try { m = el.matches(r.selectorText); } catch (e) {}
          if (!m) continue;
          const decl = [];
          for (const p of props) { const v = r.style.getPropertyValue(p); if (v) decl.push(p + ':' + v); }
          if (decl.length) hits.push({ href: (sheet.href||'inline').split('/').pop().split('?')[0],
                                       media: media, sel: r.selectorText, decl: decl.join('; ') });
        }
      };
      walk(rules, '');
    }
    out.push({ tag: el.tagName.toLowerCase(), cls: el.getAttribute('class'),
               chain: chain.slice(0, 5), vals, hits, inline: el.getAttribute('style') });
  });
  return out;
}"""

ap = argparse.ArgumentParser()
ap.add_argument('--password'); ap.add_argument('--page', default='index')
ap.add_argument('--sel', required=True, help='comma-separated'); ap.add_argument('--width', type=int, default=1440)
ap.add_argument('--props', default='font-size,line-height,font-weight,color,letter-spacing')
a = ap.parse_args()
props = a.props.split(',')

def show(tag, rows):
    print('\n#### %s' % tag)
    for r in rows:
        print('  <%s class="%s">%s' % (r['tag'], r['cls'], '  style="%s"' % r['inline'] if r['inline'] else ''))
        print('    chain: ' + ' < '.join(r['chain'][1:]))
        print('    computed: ' + '  '.join('%s=%s' % (k, v) for k, v in r['vals'].items()))
        for h in r['hits']:
            print('      [%s%s] %s { %s }' % (h['href'], ' @' + h['media'] if h['media'] else '',
                                              h['sel'][:70], h['decl']))

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=CHROME)
    ctx = b.new_context(viewport={'width': a.width, 'height': 1000})
    pg = ctx.new_page()
    pg.goto((ROOT / (a.page + '.html')).as_uri(), wait_until='networkidle')
    pg.wait_for_timeout(500)
    for sel in a.sel.split(','):
        show('static %s.html @%d  %s' % (a.page, a.width, sel), pg.evaluate(DUMP, [sel, props]))
    pg.close()
    if a.password:
        c2 = b.new_context(viewport={'width': a.width, 'height': 1000})
        r = c2.request.post(SITE + '/password', form={'form_type': 'storefront_password',
                                                      'utf8': '✓', 'password': a.password})
        if r.status in (429, 503): raise SystemExit('Cloudflare HTTP %d -- back off' % r.status)
        pg = c2.new_page(); pg.goto(SITE + PAGES[a.page], wait_until='networkidle')
        pg.wait_for_timeout(500)
        for sel in a.sel.split(','):
            show('live %s @%d  %s' % (PAGES[a.page], a.width, sel), pg.evaluate(DUMP, [sel, props]))
    b.close()
