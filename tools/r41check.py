#!/usr/bin/env python3
"""Round-41 assertions — the three responsive items in 修改任务文档.txt.

    python3 tools/r41check.py

All three are about the 768–1280 band, which has no board, so the judge is
behaviour rather than board values:

  1. .gb-page-hero must not starve either column. Both used to be rigid in
     opposite directions — the media held a hard 570 down to 1025 (text fell to
     243.8 at 1100, a six-line title) and then flipped to a basis of 0 below it
     (media collapsed to 119.8 x 90.3). The pair now shares one basis ratio.
  2. .gb-science__cards, two-up, must centre a lone third card.
  3. compare / ingredients / faq-image hold two columns down to 991, not 1024,
     and drop their stacked width caps — except the two square images, whose
     520 cap stays (without it they blow up to the full version width).

The 1440 and 390 tiers carry "unchanged" assertions throughout: this round is
meant to touch neither board width.
"""
import asyncio, os, sys
from playwright.async_api import async_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXE = "/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome"
# Must cover the reveal group too, not just .wowo: the line masks otherwise
# sit at frame 0 and clip the copy (see memory kill-animations-blanks-reveal-blocks).
SETTLE = (".wowo,.gb-float-art,[data-line-reveal],.gb-line-mask__inner,.gb-ink-halo{"
          "opacity:1!important;transform:none!important;animation:none!important}")

FAILS = []

def eq(label, got, want, tol=None):
    try:
        ok = (abs(float(got) - float(want)) <= tol) if tol is not None else (got == want)
    except (TypeError, ValueError):
        ok = False
    if not ok:
        FAILS.append(f"{label}: got {got!r}, want {want!r}" + (f" (±{tol})" if tol else ""))

def ok_if(label, cond, detail=""):
    if not cond:
        FAILS.append(f"{label}{(': ' + detail) if detail else ''}")


PROBE = r"""() => {
  const q=s=>document.querySelector(s), qa=s=>[...document.querySelectorAll(s)];
  const R=s=>{const e=q(s); if(!e) return null; const r=e.getBoundingClientRect();
    return {x:+r.x.toFixed(2), w:+r.width.toFixed(2), h:+r.height.toFixed(2)};};
  const cs=(s,p)=>{const e=q(s); return e?getComputedStyle(e)[p]:null};
  const o={};

  // --- 1 page hero -------------------------------------------------------
  if (q('.gb-page-hero__inner')) {
    o.phDir   = cs('.gb-page-hero__inner','flexDirection');
    o.phText  = R('.gb-page-hero__text');
    o.phMedia = R('.gb-page-hero__media');
    const t = q('.gb-page-hero__title');
    o.phTitleLines = t ? Math.round(t.getBoundingClientRect().height
                                    / parseFloat(getComputedStyle(t).lineHeight)) : null;
    o.phInnerContent = (() => {                 // the box the two columns share
      const e = q('.gb-page-hero__inner'), st = getComputedStyle(e);
      return +(e.getBoundingClientRect().width
               - parseFloat(st.paddingLeft) - parseFloat(st.paddingRight)).toFixed(2);
    })();
    o.phGap = parseFloat(cs('.gb-page-hero__inner','columnGap'));
  }

  // --- 2 science cards ---------------------------------------------------
  { const boxes = qa('.gb-science__cards');
    o.sciBoxCount = boxes.length;
    o.sciGroups = boxes.map(box => {
      const b = box.getBoundingClientRect();
      const kids = [...box.children].map(e => {
        const r = e.getBoundingClientRect();
        return {x:+r.x.toFixed(2), w:+r.width.toFixed(2)};
      });
      return {boxCentre:+(b.x + b.width/2).toFixed(2), cols:getComputedStyle(box).gridTemplateColumns,
              kids};
    });
  }

  // --- 3 the three two-column sections -----------------------------------
  for (const [key, sel] of [['cmp','.gb-compare__inner'], ['ing','.gb-ingredients__inner'],
                            ['fq','.gb-faq-image__inner']]) {
    if (!q(sel)) continue;
    o[key+'Dir'] = cs(sel,'flexDirection');
  }
  o.cmpHead   = R('.gb-compare__heading');
  o.cmpPanel  = R('.gb-compare__panel');
  o.cmpHeadMax  = cs('.gb-compare__heading','maxWidth');
  o.cmpPanelMax = cs('.gb-compare__panel','maxWidth');
  o.ingDisc   = R('.gb-ingredients__disc');
  o.ingBody   = R('.gb-ingredients__body');
  o.fqMedia   = R('.gb-faq-image__media');
  o.fqBody    = R('.gb-faq-image__body');

  o.overflowX = document.documentElement.scrollWidth - document.documentElement.clientWidth;
  return o;
}"""


async def main():
    plan = {"science.html": (1440, 1280, 1200, 1100, 1024, 992, 991, 900, 768, 390),
            "reviews.html": (1440, 1280, 1024, 992, 991, 390),
            "index.html":   (1440, 1024, 768, 390)}
    data = {}
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path=EXE)
        for page, widths in plan.items():
            for w in widths:
                pg = await b.new_page(viewport={"width": w, "height": 1000})
                await pg.goto("file://" + os.path.join(ROOT, page))
                await pg.add_style_tag(content=SETTLE)
                await pg.evaluate("() => document.fonts.ready")
                await pg.wait_for_timeout(250)
                data[(page, w)] = await pg.evaluate(PROBE)
                await pg.close()
        await b.close()

    S = lambda w: data[("science.html", w)]
    V = lambda w: data[("reviews.html", w)]
    I = lambda w: data[("index.html", w)]

    # ===== 1. page hero: neither column may be starved ======================
    # the board pair, untouched at 1440
    eq("1440 hero text is the board's 566", S(1440)["phText"]["w"], 566, tol=0.5)
    eq("1440 hero media is the board's 570", S(1440)["phMedia"]["w"], 570, tol=0.5)
    eq("1440 hero title is 3 lines", S(1440)["phTitleLines"], 3)

    # through the whole crowded band the two columns must stay in step, and the
    # media must never collapse. 566:570 is the board ratio.
    for w in (1280, 1200, 1100, 1024, 992, 991, 900, 768):
        d = S(w)
        t, m = d["phText"]["w"], d["phMedia"]["w"]
        ok_if(f"{w} hero media has not collapsed", m > 300, f"media {m}px wide")
        ok_if(f"{w} hero text has not been starved", t > 300, f"text {t}px wide")
        ratio = m / t
        eq(f"{w} hero columns keep the board's 570:566 ratio", ratio, 570 / 566, tol=0.02)
        # and together they fill the content box exactly (no slack, no overflow)
        eq(f"{w} hero columns fill the content box", t + m + d["phGap"],
           d["phInnerContent"], tol=1.5)
    # the specific regressions this replaces
    ok_if("1100 hero title no longer runs 6 lines", S(1100)["phTitleLines"] <= 4,
          f"{S(1100)['phTitleLines']} lines")
    ok_if("1024 hero media is no longer 119.8 wide", S(1024)["phMedia"]["w"] > 400,
          f"{S(1024)['phMedia']['w']}px")
    # phone tier untouched: column-reverse, and the basis must NOT act as a height
    eq("390 hero stays column-reverse", S(390)["phDir"], "column-reverse")
    eq("390 hero media is full width", S(390)["phMedia"]["w"], 350, tol=0.5)
    ok_if("390 hero text is content-height, not the 566 basis",
          S(390)["phText"]["h"] < 400, f"{S(390)['phText']['h']}px tall")
    eq("390 reviews hero text is content-height too", V(390)["phText"]["h"] < 400, True)

    # ===== 2. a lone third card is centred ==================================
    # r51 moved the 3→2 step to 1200, so 1280 is three-up on 3 tracks now.
    for page, fn, widths in (("science", S, (1200, 1100, 1024, 992, 900, 768)),
                             ("index", I, (1024, 768))):
        for w in widths:
            d = fn(w)
            ok_if(f"{w} {page}: found the card grids", d["sciBoxCount"] > 0)
            for gi, g in enumerate(d["sciGroups"]):
                eq(f"{w} {page} grid {gi} runs on 4 tracks", len(g["cols"].split()), 4)
                ok_if(f"{w} {page} grid {gi} holds 3 cards", len(g["kids"]) == 3,
                      f"{len(g['kids'])}")
                first, second, third = g["kids"]
                # row 1 unchanged: two cards of equal width side by side
                eq(f"{w} {page} grid {gi} two-up widths match", first["w"], second["w"], tol=0.5)
                # row 2: the lone card centres on the grid, not on the left edge
                c = third["x"] + third["w"] / 2
                eq(f"{w} {page} grid {gi} lone card is centred", c, g["boxCentre"], tol=1.0)
                ok_if(f"{w} {page} grid {gi} lone card actually moved off the left edge",
                      abs(third["x"] - first["x"]) > 1,
                      f"third at {third['x']}, first at {first['x']}")
    # three-up on desktop is untouched
    for g in S(1440)["sciGroups"]:
        eq("1440 science grid is still 3 tracks", len(g["cols"].split()), 3)
        xs = [k["x"] for k in g["kids"]]
        ok_if("1440 science cards are all on one row", len(set(round(x) for x in xs)) == 3, f"{xs}")
    # one column on the phone
    for g in S(390)["sciGroups"]:
        eq("390 science grid is 1 track", len(g["cols"].split()), 1)

    # ===== 3. two columns hold to 767 (was 991 this round) ==================
    # ⚠ The client moved this again in r43: 1024 (r30) -> 991 (this round) ->
    # 767. The assertions are flipped rather than deleted so the history stays
    # visible; r43check.py owns the current thresholds.
    for w in (1440, 1280, 1200, 1100, 1024, 992, 991, 900, 768):
        eq(f"{w} compare is two columns", S(w)["cmpDir"], "row")
        eq(f"{w} ingredients is two columns", S(w)["ingDir"], "row")
        eq(f"{w} faq-image is two columns", S(w)["fqDir"], "row")
    eq("390 compare has stacked", S(390)["cmpDir"], "column")
    eq("390 ingredients has stacked", S(390)["ingDir"], "column")
    eq("390 faq-image has stacked", S(390)["fqDir"], "column")
    eq("992 reviews ingredients is two columns", V(992)["ingDir"], "row")
    eq("991 reviews ingredients is two columns too (r43)", V(991)["ingDir"], "row")

    # both columns must stay real everywhere they are side by side — this is
    # what the r41 change bought and r43 extends down to 768
    for w in (1024, 992, 991, 900, 768):
        d = S(w)
        ok_if(f"{w} compare heading is a real column", d["cmpHead"]["w"] > 250,
              f"{d['cmpHead']['w']}px")
        ok_if(f"{w} compare panel is a real column", d["cmpPanel"]["w"] > 250,
              f"{d['cmpPanel']['w']}px")
        ok_if(f"{w} ingredients square did not starve the body",
              d["ingDisc"]["w"] > 250 and d["ingBody"]["w"] > 250,
              f"disc {d['ingDisc']['w']}, body {d['ingBody']['w']}")
        eq(f"{w} ingredients square stays square", d["ingDisc"]["w"], d["ingDisc"]["h"], tol=1)
        ok_if(f"{w} faq-image square did not starve the body",
              d["fqMedia"]["w"] > 250 and d["fqBody"]["w"] > 250,
              f"media {d['fqMedia']['w']}, body {d['fqBody']['w']}")

    # stacked: every cap is gone now (r43 — the client asked for the squares'
    # too, having asked only for compare's in r41)
    d = S(390)
    eq("390 compare heading has no width cap", d["cmpHeadMax"], "none")
    eq("390 compare panel has no width cap", d["cmpPanelMax"], "none")
    # r43 put the version gutter back on the inner and capped both squares at
    # 520, so full-bleed is over: 390 is 350 again (the pre-r41 figure) and 767
    # stops at 520 instead of running the whole screen.
    eq("390 ingredients square keeps the 20 gutter", d["ingDisc"]["w"], 350, tol=0.5)
    eq("390 faq-image square keeps the 20 gutter", d["fqMedia"]["w"], 350, tol=0.5)
    eq("390 ingredients square stays square", d["ingDisc"]["w"], d["ingDisc"]["h"], tol=1)

    # nothing may scroll sideways at any width tested
    for (page, w), d in data.items():
        eq(f"{page}@{w} no horizontal overflow", d["overflowX"], 0)

    if FAILS:
        print(f"r41 FAILED — {len(FAILS)} assertion(s)\n")
        for f in FAILS: print("  ✗", f)
        return 1
    print("r41 OK — all assertions pass across 1440 / 1280 / 1200 / 1100 / 1024"
          " / 992 / 991 / 900 / 768 / 390")
    return 0


sys.exit(asyncio.run(main()))
