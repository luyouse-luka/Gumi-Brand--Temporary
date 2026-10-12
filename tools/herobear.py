#!/usr/bin/env python3
"""Mobile hero: where the bear, the scallop and the next section actually sit.

  python3 tools/herobear.py [--live --password 1234]

.gb-hero reserves the bear's own 496 as margin-bottom on narrow. The scallop is
the section's LAST CHILD (absolute, on its bottom edge), so the question is
whether that reserve opens a gap between the hero's colour and the wave.
"""
import argparse, pathlib, re, sys
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
LIVE = 'https://gumi.com.au'

PROBE = """() => {
  const r = e => { if (!e) return null; const b = e.getBoundingClientRect();
    return {top: Math.round(b.top + scrollY), bottom: Math.round(b.bottom + scrollY),
            h: Math.round(b.height), left: Math.round(b.left), w: Math.round(b.width)}; };
  const hero = document.querySelector('.gb-hero');
  const art = document.querySelector('.gb-hero__art');
  const bear = document.querySelector('.gb-hero__bear');
  // live has no built-in scallop inside .gb-hero any more (r105): the wave is a
  // flow Gumi Wave section AFTER the hero's own section wrapper.
  const sc = (hero && hero.querySelector('.gb-scallop, .gb-wave'))
             || document.querySelector('.gb-wave, .gb-scallop');
  const wrap = hero && hero.closest('.shopify-section, section') || hero;
  const next = wrap && wrap.nextElementSibling;
  const cs = hero ? getComputedStyle(hero) : null;
  return {
    hero: r(hero), art: r(art), bear: r(bear), scallop: r(sc), next: r(next),
    nextTag: next ? (String(next.className).slice(0, 60) || next.tagName) : null,
    wrapBox: r(wrap),
    waveSection: r(sc && sc.closest('.gb-wave-section')),
    afterWave: r(sc && sc.closest('.gb-wave-section') && sc.closest('.gb-wave-section').nextElementSibling),
    afterWaveTag: (() => { const ws = sc && sc.closest('.gb-wave-section');
      const n = ws && ws.nextElementSibling;
      return n ? String(n.id || n.className).slice(0, 50) : null; })(),
    scInsideHero: !!(hero && hero.querySelector('.gb-scallop, .gb-wave')),
    scClass: sc ? String(sc.className).slice(0, 70) : null,
    heroMarginBottom: cs && cs.marginBottom,
    heroPaddingBottom: cs && cs.paddingBottom,
    scRes: cs && cs.getPropertyValue('--sc-res').trim(),
    heroBg: cs && cs.backgroundColor,
    scPos: sc && getComputedStyle(sc).position,
  };
}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--live', action='store_true')
    ap.add_argument('--password')
    ap.add_argument('--preflight', action='store_true')
    a = ap.parse_args()
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME)
        ctx = b.new_context(viewport={'width': 390, 'height': 844})
        if a.live:
            ctx.request.post(LIVE + '/password', form={
                'form_type': 'storefront_password', 'utf8': '✓', 'password': a.password})
        page = ctx.new_page()
        page.goto((LIVE + '/') if a.live else (ROOT / 'index.html').as_uri(), wait_until='load')
        page.wait_for_timeout(2500)
        if a.preflight:
            css = (ROOT / 'assets/customstyle.css').read_text(encoding='utf-8')
            m = re.search(r'(@media \(max-width: 767px\) \{\s*\.shopify-section:has\(\+ '
                          r'\.gb-wave-section\) \.gb-hero \{.*?\n\})', css, re.S)
            if not m:
                sys.exit('ABORT: the ask-5 rules are not in assets/customstyle.css -- recompile first')
            page.add_style_tag(content=m.group(1))
            page.wait_for_timeout(400)
        d = page.evaluate(PROBE)
        print(f'--- {"live" if a.live else "static"} index @390 ---')
        for k, v in d.items():
            print(f'  {k:<18} {v}')
        if d['hero'] and d['scallop'] and d['next']:
            print()
            print(f"  scallop bottom      {d['scallop']['bottom']}")
            print(f"  hero box bottom     {d['hero']['bottom']}   (margin-bottom {d['heroMarginBottom']} not in the box)")
            print(f"  next section top    {d['next']['top']}")
            print(f"  GAP wave -> next    {d['next']['top'] - d['scallop']['bottom']} px")
            if d['bear']:
                print(f"  bear bottom         {d['bear']['bottom']}   overruns wave by "
                      f"{d['bear']['bottom'] - d['scallop']['bottom']} px")
        b.close()


main()
