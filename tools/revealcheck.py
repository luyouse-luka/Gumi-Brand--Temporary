#!/usr/bin/env python3
"""Every entrance effect must end at opacity 1 with its transform back at rest.

    python3 tools/revealcheck.py

Scrolls each page top to bottom, waits out the longest entrance (1.4s line
slide + the 1.05s halo delay + 0.35s), then checks [data-line-reveal] hosts,
their line masks, .gb-ink-halo, .wowo and .gb-float-art. .wowo sets opacity:0
unconditionally, so anything that stops the script leaves content permanently
invisible -- this is the guard for that.

⚠ display:none elements never reach the observer and keep opacity:0 forever,
  which is correct. Judging them fires on healthy markup
  (.gb-ingredients__desktop-only at 390 did exactly that), so offsetParent
  filters them out.
"""
import os, glob, sys
from playwright.sync_api import sync_playwright
ROOT="/home/ly/project/Gumi-Brand"
CHROME=os.path.expanduser("~/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome")
CHECK = r"""() => {
  const bad = [];
  // display:none never enters the observer, so it keeps its .wowo opacity:0.
  // Judging a hidden element is the classic恒真 negative assertion.
  const shown = (e) => e.offsetParent !== null || getComputedStyle(e).position === 'fixed';
  const push = (e, why) => bad.push(why + ' | ' + e.tagName.toLowerCase() + '.' +
      (typeof e.className === 'string' ? e.className.trim().split(/\s+/).slice(0,2).join('.') : '?'));
  for (const e of document.querySelectorAll('[data-line-reveal]'))
    if (shown(e) && +getComputedStyle(e).opacity < 0.99) push(e, 'line-reveal host opacity ' + getComputedStyle(e).opacity);
  for (const e of document.querySelectorAll('.gb-line-mask__inner')) {
    if (!shown(e)) continue;
    const cs = getComputedStyle(e);
    if (+cs.opacity < 0.99) push(e, 'mask inner opacity ' + cs.opacity);
    if (cs.transform !== 'none' && cs.transform !== 'matrix(1, 0, 0, 1, 0, 0)') push(e, 'mask inner transform ' + cs.transform);
  }
  for (const e of document.querySelectorAll('.gb-ink-halo'))
    if (e.parentElement.offsetParent !== null && +getComputedStyle(e).opacity < 0.99) push(e, 'ink-halo opacity ' + getComputedStyle(e).opacity);
  for (const e of document.querySelectorAll('.wowo'))
    if (shown(e) && +getComputedStyle(e).opacity < 0.99) push(e, 'wowo opacity ' + getComputedStyle(e).opacity);
  for (const e of document.querySelectorAll('.gb-float-art'))
    if (shown(e) && +getComputedStyle(e).opacity < 0.99) push(e, 'float-art opacity ' + getComputedStyle(e).opacity);
  return bad;
}"""
pages=[os.path.basename(p) for p in sorted(glob.glob(os.path.join(ROOT,'*.html'))) if os.path.basename(p)!='font-check.html']
fails=0
with sync_playwright() as p:
    br=p.chromium.launch(executable_path=CHROME)
    for page in pages:
        for w in (390,1440):
            pg=br.new_page(viewport={"width":w,"height":900}, device_scale_factor=1)
            pg.goto("file://"+os.path.join(ROOT,page)); pg.wait_for_timeout(1500)
            h=pg.evaluate("()=>document.body.scrollHeight")
            y=0
            while y < h:
                pg.evaluate("(y)=>window.scrollTo(0,y)", y); pg.wait_for_timeout(260); y+=700
            pg.wait_for_timeout(2600)
            bad=pg.evaluate(CHECK); pg.close()
            if bad:
                fails+=len(bad); print('%-22s w%-5d %d 条:'%(page,w,len(bad)))
                for b in bad[:6]: print('     ',b)
    br.close()
print('\n入场动效收尾检查：%s'%('FAIL %d'%fails if fails else 'OK 全部 opacity=1、transform 归位'))
sys.exit(1 if fails else 0)
