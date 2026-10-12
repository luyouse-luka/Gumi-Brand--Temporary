#!/usr/bin/env python3
"""Why the banner title lands after the copy below it (mobile).

  python3 tools/revealrace.py                      # static build
  python3 tools/revealrace.py --live --password 1234

Samples every frame from document-start: when does the hero title actually reach
opacity 1, and when does the first .wowo block below it? The title runs
lineReveal ([data-line-reveal] + html.js gate, r72); the block runs wowo.
"""
import argparse, pathlib, sys
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
LIVE = 'https://gumi.com.au'

PAGES = [('faq.html', '/pages/faq'), ('index.html', '/'),
         ('our-story.html', '/pages/our-story'),
         ('get-in-touch.html', '/pages/get-in-touch')]

# ⚠ Do NOT grade the host's own opacity: .is-split flips it to 1 while every
# line is still parked at translateY(100%) inside its mask. What the eye calls
# "the title appeared" is the LAST line's slide finishing.
INIT = """
window.__r = {frames: []};
(function tick() {
  const t = Math.round(performance.now());
  const title = document.querySelector('.gb-page-hero__title, .gb-hero__title');
  const wowo = document.querySelector('.wowo');
  const shown = e => {
    if (!e) return null;
    const r = e.getBoundingClientRect();
    if (getComputedStyle(e).opacity < 0.99) return false;
    const inners = e.querySelectorAll('.gb-line-mask__inner');
    if (!inners.length) return true;
    // every line home == the whole title is legible
    return [...inners].every(i => {
      const m = new DOMMatrixReadOnly(getComputedStyle(i).transform);
      return Math.abs(m.m42) < 0.5;
    });
  };
  if (title || wowo) {
    window.__r.frames.push({
      t: t,
      titleShown: shown(title),
      lines: title ? title.querySelectorAll('.gb-line-mask').length : null,
      titleSplit: title ? title.classList.contains('is-split') : null,
      wowoShown: wowo ? (getComputedStyle(wowo).opacity >= 0.99) : null,
      wowoAnim: wowo ? wowo.classList.contains('animated') : null,
    });
  }
  if (t < 7000) requestAnimationFrame(tick);
})();
"""


def first_at(frames, key, pred):
    for f in frames:
        if f.get(key) is not None and pred(f[key]):
            return f['t']
    return None


def run(page, url, label):
    page.goto(url, wait_until='load')
    page.wait_for_timeout(6200)
    fr = page.evaluate('window.__r.frames')
    if not fr:
        print(f'  {label:<22} no sample'); return
    t_title = next((f['t'] for f in fr if f['titleShown']), None)
    t_wowo = next((f['t'] for f in fr if f['wowoShown']), None)
    t_split = next((f['t'] for f in fr if f['titleSplit']), None)
    lines = next((f['lines'] for f in fr if f['lines']), 0)
    gap = (t_title - t_wowo) if (t_title is not None and t_wowo is not None) else None
    flag = '  <-- LAGS' if (gap or 0) > 0 else ''
    print(f'  {label:<22} lines={lines}  is-split@{t_split}  title_legible={t_title}  '
          f'wowo_visible={t_wowo}  ->  gap {gap:+} ms{flag}' if gap is not None
          else f'  {label:<22} lines={lines} title={t_title} wowo={t_wowo}')
    return gap


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--live', action='store_true')
    ap.add_argument('--password')
    ap.add_argument('--width', type=int, default=390)
    a = ap.parse_args()

    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME)
        ctx = b.new_context(viewport={'width': a.width, 'height': 844},
                            is_mobile=True, has_touch=True)
        ctx.add_init_script(INIT)
        if a.live:
            if not a.password:
                sys.exit('--live needs --password')
            ctx.request.post(LIVE + '/password', form={
                'form_type': 'storefront_password', 'utf8': '✓', 'password': a.password})
        page = ctx.new_page()
        print(f'--- {"live" if a.live else "static"} @{a.width} ---')
        for f, path in PAGES:
            url = (LIVE + path) if a.live else (ROOT / f).as_uri()
            run(page, url, f)
        b.close()


main()
