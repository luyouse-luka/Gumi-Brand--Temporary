#!/usr/bin/env python3
"""Every footer social link carries a title attribute matching its aria-label.

  python3 tools/socialtitle.py [--live <theme-dir>] [--password 1234]

aria-label already covers screen readers; title is what gives sighted users the
hover tooltip. The two must agree -- a title that differs from the aria-label
is read as a second, conflicting name by some AT.
"""
import argparse, pathlib, re, sys

NAMES = {'Facebook', 'Instagram', 'TikTok'}
LINK = re.compile(r'<a[^>]*class="gb-footer__social-link"[^>]*>')
ATTR = re.compile(r'(\w[\w-]*)="([^"]*)"')

ap = argparse.ArgumentParser()
ap.add_argument('--live', help='pulled theme directory, checks gb-footer.liquid too')
ap.add_argument('--password', help='storefront password, checks the rendered page')
a = ap.parse_args()
ok = red = 0


def check(label, html, want):
    global ok, red
    links = LINK.findall(html)
    if len(links) != want:
        print(f'  RED {label:<28} {len(links)} social links, expected {want}')
        red += 1
        return
    for tag in links:
        at = dict(ATTR.findall(tag))
        al, ti = at.get('aria-label'), at.get('title')
        if al in NAMES and ti == al:
            ok += 1
        else:
            print(f'  RED {label:<28} aria-label={al!r} title={ti!r}')
            red += 1
    print(f'  ok  {label:<28} {want} links, title == aria-label')


ROOT = pathlib.Path(__file__).resolve().parent.parent
for p in sorted(ROOT.glob('*.html')):
    if p.name == 'font-check.html':
        continue
    check(p.name, p.read_text(encoding='utf-8'), 3)

if a.live:
    f = pathlib.Path(a.live) / 'sections' / 'gb-footer.liquid'
    check('gb-footer.liquid', f.read_text(encoding='utf-8'), 3)

if a.password:
    from playwright.sync_api import sync_playwright
    CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
    LIVE = 'https://gumi.com.au'
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME)
        ctx = b.new_context(viewport={'width': 1440, 'height': 900})
        ctx.request.post(LIVE + '/password', form={
            'form_type': 'storefront_password', 'utf8': '✓', 'password': a.password})
        if not any(c['name'] == '_shopify_essential' for c in ctx.cookies()):
            sys.exit('storefront password rejected')
        pg = ctx.new_page()
        pg.goto(LIVE + '/', wait_until='domcontentloaded', timeout=90000)
        pg.wait_for_timeout(600)
        rows = pg.evaluate("""() => [...document.querySelectorAll('.gb-footer__social-link')]
            .map(a => ({label: a.getAttribute('aria-label'), title: a.getAttribute('title')}))""")
        if not rows:
            sys.exit('ABORT: no social links on the live page -- did it render?')
        for r in rows:
            good = r['label'] in NAMES and r['title'] == r['label']
            print(f'  {"ok " if good else "RED"} live index.html            '
                  f'aria-label={r["label"]!r} title={r["title"]!r}')
            ok, red = (ok + 1, red) if good else (ok, red + 1)
        b.close()

print(f'\n──────── {ok} ok / {red} red ────────')
sys.exit(0 if red == 0 else 1)
