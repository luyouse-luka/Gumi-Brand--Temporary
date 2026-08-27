#!/usr/bin/env python3
"""Do the line-reveal masks change where the text wraps?

Invariant = the SAME page with JavaScript disabled, so every [data-line-reveal]
host is plain unsplit copy wrapping naturally.  The previous probe compared
"opened at W" against "resized to W" -- both already split, i.e. two readings of
one polluted source (see memory probe-must-compare-against-invariant).

Three readings per width:
  natural  JS off, per-line text read back off Range client rects
  settled  JS on, after the resize debounce has rebuilt the masks
  during   JS on, sampled INSIDE the debounce window right after the resize
"""
import asyncio, json, sys
from playwright.async_api import async_playwright

EXE = "/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome"
URL = "file:///home/ly/project/Gumi-Brand/"
WIDTHS = [390, 500, 700, 900, 1200, 1440]

NATURAL = r"""() => {
  const norm = s => s.replace(/\s+/g, ' ').trim();
  const out = {};
  document.querySelectorAll('[data-line-reveal]').forEach((el, idx) => {
    const w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
    const items = []; let n;
    while ((n = w.nextNode())) {
      if (n.parentElement.closest('[aria-hidden="true"]')) continue;
      for (let i = 0; i < n.nodeValue.length; i++) items.push([n, i]);
    }
    // A superscript (.gb-stat__plus / __unit) sits on the same visual line but
    // its rect top is several px higher, so the split point is half a line, not 1px.
    const lh = parseFloat(getComputedStyle(el).lineHeight) || 20;
    const rg = document.createRange();
    const lines = []; let lastTop = null, cur = null;
    for (const [node, i] of items) {
      rg.setStart(node, i); rg.setEnd(node, i + 1);
      const r = rg.getBoundingClientRect();
      if (!r.width && !r.height) continue;
      if (lastTop === null || Math.abs(r.top - lastTop) > lh * 0.5) { cur = []; lines.push(cur); lastTop = r.top; }
      cur.push(node.nodeValue[i]);
    }
    out[idx] = lines.map(l => norm(l.join(''))).filter(Boolean);
  });
  return out;
}"""

# With the masks flattened there is nothing to read line text off, so fall back
# to the same Range walk the invariant uses — that IS the question being asked.
SPLIT = NATURAL.replace(
    "out[idx] = lines.map(l => norm(l.join(''))).filter(Boolean);",
    """const masks = el.querySelectorAll('.gb-line-mask');
    out[idx] = masks.length
      ? [...masks].map(m => { const c = m.cloneNode(true);
          c.querySelectorAll('[aria-hidden="true"]').forEach(x => x.remove());
          return norm(c.textContent); }).filter(Boolean)
      : lines.map(l => norm(l.join(''))).filter(Boolean);""")


async def read(ctx, width, js_on, resize_from=None, settle=0):
    pg = await ctx.new_page()
    await pg.set_viewport_size({"width": resize_from or width, "height": 900})
    await pg.goto(URL + "index.html")
    await pg.wait_for_timeout(1500 if js_on else 300)
    if js_on:
        # scroll the whole page so every host has been revealed -> is-settled branch
        await pg.evaluate("async()=>{for(let y=0;y<document.body.scrollHeight;y+=600){window.scrollTo(0,y);await new Promise(r=>requestAnimationFrame(r));}window.scrollTo(0,0);}")
        await pg.wait_for_timeout(600)
    if resize_from:
        await pg.set_viewport_size({"width": width, "height": 900})
        await pg.wait_for_timeout(settle)
    data = await pg.evaluate(SPLIT if js_on else NATURAL)
    await pg.close()
    return data


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=EXE)
        on = await b.new_context(viewport={"width": 390, "height": 900})
        off = await b.new_context(viewport={"width": 390, "height": 900}, java_script_enabled=False)
        bad_settled = bad_during = total = 0
        for w in WIDTHS:
            nat = await read(off, w, False)
            settled = await read(on, w, True, resize_from=1440 if w != 1440 else 390, settle=900)
            during = await read(on, w, True, resize_from=1440 if w != 1440 else 390, settle=80)
            for k in nat:
                total += 1
                n, s, d = nat[k], settled.get(k, []), during.get(k, [])
                if n != s:
                    bad_settled += 1
                    print(f"[{w}] SETTLED host#{k}\n   natural {n}\n   masks   {s}")
                if n != d:
                    bad_during += 1
                    if n == s:
                        print(f"[{w}] DURING  host#{k}\n   natural {n}\n   masks   {d}")
        print(f"\n{total} host-readings: settled mismatches {bad_settled}, during-resize mismatches {bad_during}")
        await b.close()

asyncio.run(main())
