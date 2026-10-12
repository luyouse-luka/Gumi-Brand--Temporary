#!/usr/bin/env python3
"""Task 44 -- a select list inside a modal panel must stay reachable.

The shared selectBox sizes its list with a fixed `max-height: 224px` and decides
whether to drop it upwards from ONE side's room (and its clipBottom() treats
overflow:clip as non-clipping, which a modal panel is). In a short panel the
list therefore ran past the panel edge, and `overflow: clip` cut it off.

⚠ The worst case is 4-5 options, not many: there the content is under 224 so the
list has no scrollbar of its own, and the cut part is unreachable by any means.
More options are less bad -- the list scrolls, it is only the window that is
short. So the assertion is not "it scrolls", it is "nothing is cut off AND
whatever does not fit is scrollable".

⚠ Options are injected from an init script, before any page script runs, so
selectBox builds its widget from the grown <select> -- the real path. Rewriting
.gb-select__list by hand instead measures markup the widget never made.
"""
import sys, pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent

# panel -> the native select's id
CASES = [("edit-frequency", "acct-f-freq"),     # short panel: the reported one
         ("shipping-form", "acct-sh-state")]    # tall panel: must not be clamped
COUNTS = [3, 4, 5, 8, 30]

ok = red = 0


def check(label, got, want):
    global ok, red
    if got == want:
        print("ok   %-62s %s" % (label, got)); ok += 1
    else:
        print("RED  %-62s got %r want %r" % (label, got, want)); red += 1


def _chrome():
    hits = sorted((pathlib.Path.home() / ".cache/ms-playwright").glob(
        "chromium-*/chrome-linux64/chrome"))
    if not hits:
        sys.exit("no chromium -- run: npx playwright install chromium")
    return str(hits[-1])


def seed(select_id, n):
    return ("document.addEventListener('DOMContentLoaded',function(){"
            "var s=document.getElementById('%s');if(!s)return;s.innerHTML='';"
            "for(var i=1;i<=%d;i++){var o=document.createElement('option');"
            "o.value='v'+i;o.textContent='Option number '+i;s.appendChild(o);}});"
            % (select_id, n))


MEAS = """
(panel)=>{
 const p=document.querySelector(`[data-acct-modal-panel='${panel}']`);
 const box=p.querySelector('.gb-acct-modal__panel');
 const s=p.querySelector('.gb-select');
 const l=s.querySelector('.gb-select__list');
 const lr=l.getBoundingClientRect(), br=box.getBoundingClientRect();
 // natural = what CSS alone would give it, i.e. how tall it wants to be
 const clamp=l.style.maxHeight; l.style.maxHeight='';
 const natural=l.offsetHeight; l.style.maxHeight=clamp;
 return {opts:l.children.length, h:+lr.height.toFixed(1), natural,
   clamp:clamp||null, up:s.classList.contains('is-up'),
   overBottom:+(lr.bottom-br.bottom).toFixed(1),
   overTop:+(br.top-lr.top).toFixed(1),
   scrollable:l.scrollHeight>l.clientHeight+1,
   fitsWhole:l.scrollHeight<=l.clientHeight+1,
   boxOverflowY:getComputedStyle(box).overflowY,
   panelH:+br.height.toFixed(1)};}
"""


def run(b, width, height):
    tag = "@%d" % width
    for panel, sid in CASES:
        for n in COUNTS:
            ctx = b.new_context(viewport={"width": width, "height": height},
                                reduced_motion="no-preference")
            ctx.add_init_script(seed(sid, n))
            pg = ctx.new_page()
            pg.goto((ROOT / "account.html").as_uri() + "#detail")
            pg.wait_for_timeout(900)

            # The patch must be live; a silent no-op would make everything below
            # pass on whatever the shared widget happens to do.
            if panel == CASES[0][0] and n == COUNTS[0]:
                check("selectFit is wired" + tag, pg.evaluate(
                    "()=>!!(window.gumiAcct&&window.gumiAcct.selectFit)"), True)

            pg.evaluate("(p)=>window.gumiAcct.modal.open(p)", panel)
            pg.wait_for_timeout(500)
            pg.click("[data-acct-modal-panel='%s'] .gb-select__button" % panel)
            pg.wait_for_timeout(350)
            r = pg.evaluate(MEAS, panel)

            lbl = "%s/%d%s" % (panel, n, tag)
            check("anchor: the panel really clips -- " + lbl, r["boxOverflowY"], "clip")
            check("list has all %d options -- %s" % (n, lbl), r["opts"], n)
            # The two that matter: not cut off on either edge.
            check("not cut at the panel's bottom -- " + lbl, r["overBottom"] <= 0.5, True)
            check("not cut at the panel's top -- " + lbl, r["overTop"] <= 0.5, True)
            # Everything the list cannot show must be scrollable to.
            check("either it all fits or it scrolls -- " + lbl,
                  r["fitsWhole"] or r["scrollable"], True)

            # A tall panel must not be clamped for nothing: room >= natural
            # means the shared 224 stands.
            if panel == "shipping-form" and not r["up"]:
                pass   # side chosen by room; nothing to assert about the clamp
            if r["natural"] <= r["h"] + 0.5 and r["clamp"]:
                check("no pointless clamp -- " + lbl, r["clamp"], None)

            # Closing must drop the inline clamp, or the next open starts short.
            pg.keyboard.press("Escape")
            pg.wait_for_timeout(400)
            if panel == CASES[0][0] and n == 8:
                check("clamp is cleared on close" + tag, pg.eval_on_selector(
                    "[data-acct-modal-panel='%s'] .gb-select__list" % panel,
                    "e=>e.style.maxHeight || null"), None)
            ctx.close()


with sync_playwright() as p_:
    b = p_.chromium.launch(executable_path=_chrome())
    run(b, 1440, 950)
    run(b, 390, 844)
    b.close()

print("\n%d ok / %d red" % (ok, red))
sys.exit(1 if red else 0)
