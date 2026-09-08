#!/usr/bin/env python3
"""Every scallop on the site: static vs live, class set + measured geometry.

  python3 tools/scallopmap.py                    # static only
  python3 tools/scallopmap.py --password 1234    # both, side by side

Written for docs/SCALLOP.md. The wave is drawn from three independent axes
(size / direction / colour pair) plus a positioning modifier, and every one of
them is spelled as a class -- so the class set IS the spec, and the rendered
height and the two painted colours are how you check the class set is right.
"""
import argparse
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

PROBE = """() => {
  const norm = c => [...c].filter(x => x.startsWith('gb-scallop')).sort().join(' ');
  return [...document.querySelectorAll('.gb-scallop:not(.gb-scallop-box)')].map(e => {
    const cs = getComputedStyle(e);
    // The host is the section that OWNS the wave (it is the section's own last
    // child), not the one it visually divides into.
    let host = e.parentElement;
    while (host && !/^(SECTION|FOOTER)$/.test(host.tagName)) host = host.parentElement;
    const hc = host ? [...host.classList].filter(c => c.startsWith('gb-'))[0] : '?';
    return {host: hc, cls: norm(e.classList),
            h: +e.getBoundingClientRect().height.toFixed(1),
            bg: cs.getPropertyValue('--wave-bg').trim(),
            fg: cs.getPropertyValue('--wave-fg').trim(),
            pos: cs.position, bottom: cs.bottom};
  });
}"""


def collect(pg, url):
    pg.goto(url, wait_until='domcontentloaded')
    pg.wait_for_timeout(700)
    return pg.evaluate(PROBE)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--password')
    a = ap.parse_args()
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=CHROME)
        ctx = br.new_context(viewport={'width': 1440, 'height': 900})
        if a.password:
            ctx.request.post(LIVE + '/password', form={
                'form_type': 'storefront_password', 'utf8': '✓', 'password': a.password})
        pg = ctx.new_page()
        drift = 0
        for name, path in PAGES.items():
            st = collect(pg, f'file:///home/ly/project/Gumi-Brand/{name}.html')
            print(f'\n== {name} ==')
            if not a.password:
                for d in st:
                    print(f"  {d['host']:<20} {d['cls']:<66} h={d['h']:<6} {d['bg']} -> {d['fg']}")
                continue
            lv = collect(pg, LIVE + path)
            lv_by = {}
            for d in lv: lv_by.setdefault(d['host'], []).append(d)
            for d in st:
                cand = lv_by.get(d['host'], [])
                m = cand.pop(0) if cand else None
                same = m and m['cls'] == d['cls'] and abs(m['h'] - d['h']) < 1.5
                if not same: drift += 1
                print(f"  {'   ' if same else '≠≠≠'} {d['host']:<20} {d['cls']}")
                if not same:
                    print(f"        static  h={d['h']:<7} {d['bg']} -> {d['fg']}")
                    print(f"        live    " + (f"h={m['h']:<7} {m['bg']} -> {m['fg']}\n"
                          f"                {m['cls']}" if m else '(no wave on this section)'))
        if a.password:
            print(f'\n{drift} scallop(s) differ between the static build and live')
        br.close()


if __name__ == '__main__':
    main()
