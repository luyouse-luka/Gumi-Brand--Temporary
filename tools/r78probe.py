#!/usr/bin/env python3
"""Measure the focus ring on .gb-reel and in the footer, plus the header CTA box.

  python3 tools/r78probe.py [page.html] [--css <file>]

Rings are reached with real Tab presses: el.focus() does not set :focus-visible.
"""
import sys, json
from playwright.sync_api import sync_playwright
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'

page_file = sys.argv[1] if len(sys.argv) > 1 else 'index.html'

INFO = """(sel) => {
  const e = document.querySelector(sel); if (!e) return null;
  const c = getComputedStyle(e), b = e.getBoundingClientRect();
  // Nearest ancestor that would clip an outline drawn outside the border box.
  let clip = null;
  for (let p = e.parentElement; p; p = p.parentElement) {
    const pc = getComputedStyle(p);
    if (pc.overflow !== 'visible' || pc.overflowX !== 'visible' || pc.overflowY !== 'visible') {
      const pb = p.getBoundingClientRect();
      clip = { who: p.tagName.toLowerCase() + '.' + (p.className||'').toString().slice(0,40),
               overflow: pc.overflow, rect: [Math.round(pb.x),Math.round(pb.y),Math.round(pb.width),Math.round(pb.height)] };
      break;
    }
  }
  return {
    rect: [Math.round(b.x), Math.round(b.y), Math.round(b.width), Math.round(b.height)],
    focusVisible: e.matches(':focus-visible'),
    outline: c.outlineWidth + ' ' + c.outlineStyle + ' ' + c.outlineColor,
    outlineOffset: c.outlineOffset,
    color: c.color, bg: c.backgroundColor,
    padding: c.padding, height: c.height,
    clippedBy: clip,
  };
}"""

def tab_to(pg, sel, limit=90):
    pg.evaluate("document.body.focus()")
    pg.keyboard.press('Tab')
    for i in range(limit):
        if pg.evaluate("(s) => { const a=document.activeElement; return !!(a && a.matches && a.matches(s)); }", sel):
            return i + 1
        pg.keyboard.press('Tab')
    return None

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME)
    pg = b.new_context(viewport={'width': 1440, 'height': 900}).new_page()
    pg.goto('file:///home/ly/project/Gumi-Brand/' + page_file, wait_until='networkidle')
    pg.wait_for_timeout(1200)
    out = {}
    for name, sel in [('reel', '.gb-reel'), ('reelsBtn', '.gb-reels__btn'),
                      ('footerLogo', '.gb-footer__logo'), ('footerLink', '.gb-footer__link'),
                      ('footerSocial', '.gb-footer__social-link'),
                      ('footerSubmit', '.gb-footer__submit'), ('footerInput', '.gb-footer__input'),
                      ('headerCta', '.gb-header__cta')]:
        n = tab_to(pg, sel)
        out[name] = {'tabs': n, **(pg.evaluate(INFO, sel) or {})}
    # footer ground for contrast
    out['footerBg'] = pg.evaluate("() => getComputedStyle(document.querySelector('.gb-footer')).backgroundColor")
    print(json.dumps(out, indent=1))
    b.close()
