#!/usr/bin/env python3
"""Round-36 assertions — the eight items in 修改任务文档.txt.

Computed-style / geometry checks at 390 and 1440, both index.html states.
Anything sourced from a board carries its node id in the message.
"""
import asyncio, json, sys
from playwright.async_api import async_playwright

EXE = "/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome"
URL = "file:///home/ly/project/Gumi-Brand/index.html"
SETTLE = """.wowo,.gb-float-art,[data-line-reveal],.gb-line-mask__inner,.gb-ink-halo{
opacity:1!important;transform:none!important;animation:none!important;}"""

PROBE = r"""() => {
  const q = s => document.querySelector(s);
  const cs = (s, p) => { const e = q(s); return e ? getComputedStyle(e)[p] : 'NO-ELEMENT'; };
  const rect = s => { const e = q(s); if (!e) return null; const r = e.getBoundingClientRect();
    return {x:+r.x.toFixed(2), y:+r.y.toFixed(2), w:+r.width.toFixed(2), h:+r.height.toFixed(2)}; };
  const parentTag = s => { const e = q(s); return e ? e.parentElement.className : 'NO-ELEMENT'; };
  const o = {};
  // 1 hero
  o.heroTitlePad   = cs('.gb-hero__title', 'paddingLeft');
  { const e = q('.gb-hero__bear');
    o.heroBearLeftPct = e ? +(parseFloat(getComputedStyle(e).left) / e.offsetParent.clientWidth * 100).toFixed(2) : null;
    o.heroBearWPct    = e ? +(e.offsetWidth / e.offsetParent.clientWidth * 100).toFixed(2) : null; }   // offsetWidth: the bear is rotated, so the client rect is the aabb
  o.heroBearW      = rect('.gb-hero__bear');
  o.heroSlotW      = rect('.gb-hero__art') || rect('.gb-hero__bear');
  // 2 logo scroll
  o.logoItem       = [cs('.gb-logo-scroll__item','width'), cs('.gb-logo-scroll__item','height')];
  o.logoViewportPad= cs('.gb-logo-scroll__viewport','paddingTop');
  // 3 stats
  o.noteMarginTop  = cs('.gb-stats__note','marginTop');
  o.arrowDisplay   = cs('.gb-stats__arrow--1','display');
  o.bearImgXform   = cs('.gb-stats__bear-img','transform');
  o.bearMargin     = [cs('.gb-stats__bear','marginTop'), cs('.gb-stats__bear','marginBottom')];
  o.gridH          = rect('.gb-stats__grid').h;
  o.bearArtOverflow= cs('.gb-stats__bear-art','overflow');
  // 4 / 8 structure
  o.waveCreamParent = parentTag('.gb-scallop--cream-to-sand');
  o.waveLimeParent  = parentTag('.gb-scallop--lime-to-white');
  o.decoParent      = parentTag('.gb-stats__deco-bear');
  o.statsZ          = cs('.gb-stats','zIndex');
  o.decoXform       = cs('.gb-stats__deco-bear','transform');
  const sci = rect('.gb-science'), deco = rect('.gb-stats__deco-bear');
  o.decoCentreAboveSeam = deco ? +(sci.y - (deco.y + deco.h/2)).toFixed(2) : null;
  o.decoCentrePct       = deco ? +(((deco.x + deco.w/2) / window.innerWidth) * 100).toFixed(2) : null;
  const wave = rect('.gb-scallop--cream-to-sand');
  o.waveBottomVsSeam    = wave ? +((wave.y + wave.h) - sci.y).toFixed(2) : null;
  // 6 science
  o.sciPadTop      = cs('.gb-science','paddingTop');
  o.headAlign      = [cs('.gb-science__head','alignItems'), cs('.gb-science__head','textAlign')];
  o.headGap        = cs('.gb-science__head','rowGap');
  o.innerAlign     = cs('.gb-science__inner','alignItems');
  o.innerGap       = cs('.gb-science__inner','rowGap');
  o.cardsGap       = cs('.gb-science__cards','rowGap');
  o.bodyGap        = cs('.gb-science-card__body','rowGap');
  o.hlRadius       = cs('.gb-highlight-card','borderTopLeftRadius');
  // 7
  o.lipWidth       = rect('.gb-highlight-card__lip').w;
  o.mediaWidth     = rect('.gb-highlight-card__media').w;
  o.mediaRadius    = [cs('.gb-highlight-card__media','borderTopLeftRadius'),
                      cs('.gb-highlight-card__media','borderBottomLeftRadius')];
  o.hlTextMax      = cs('.gb-highlight-card__text','maxWidth');
  { const e = q('.gb-nutrition__bears-img');
    o.bearsImgLeftPx = e ? +parseFloat(getComputedStyle(e).left).toFixed(2) : null; }
  { const e = q('.gb-pack-band');
    o.packLeftPct = e ? +(parseFloat(getComputedStyle(e).left) / e.offsetParent.clientWidth * 100).toFixed(2) : null; }
  // guards
  o.overflowX      = document.documentElement.scrollWidth - document.documentElement.clientWidth;
  o.brNarrow       = getComputedStyle(document.querySelector('.gb-science__title .gb-br-narrow')
                       || document.createElement('br')).display;
  return o;
}"""

FAILS = []
def eq(label, got, want, tol=None):
    ok = (abs(float(got) - float(want)) <= tol) if tol is not None else (got == want)
    if not ok:
        FAILS.append(f"{label}: got {got!r}, want {want!r}" + (f" (±{tol})" if tol else ""))

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=EXE)
        data = {}
        for w in (390, 1440):
            pg = await b.new_page(viewport={"width": w, "height": 1000})
            await pg.goto(URL)
            await pg.add_style_tag(content=SETTLE)
            await pg.evaluate("async()=>{for(let y=0;y<document.body.scrollHeight;y+=700){window.scrollTo(0,y);await new Promise(r=>requestAnimationFrame(r));}window.scrollTo(0,0);}")
            await pg.wait_for_timeout(1200)
            data[w] = await pg.evaluate(PROBE)
            await pg.close()
        await b.close()

    m, d = data[390], data[1440]

    # --- 1 hero (client-set) ---
    eq("390 .gb-hero__title padding-inline", m["heroTitlePad"], "25px")
    eq("1440 .gb-hero__title padding-inline untouched", d["heroTitlePad"], "0px")
    eq("390 .gb-hero__bear left 65%", m["heroBearLeftPct"], 65.0, tol=0.2)
    eq("1440 .gb-hero__bear left untouched 50%", d["heroBearLeftPct"], 50.0, tol=0.2)
    eq("390 .gb-hero__bear width 79.39%", m["heroBearWPct"], 79.39, tol=0.3)

    # --- 2 logo scroll (client-set; no mobile board exists for Social Proof) ---
    eq("390 .gb-logo-scroll__item size", m["logoItem"], ["106px", "44px"])
    eq("1440 .gb-logo-scroll__item size untouched", d["logoItem"], ["193px", "80px"])
    eq("390 .gb-logo-scroll__viewport padding", m["logoViewportPad"], "4px")
    eq("1440 .gb-logo-scroll__viewport padding untouched", d["logoViewportPad"], "8px")

    # --- 3 stats ---
    eq("390 .gb-stats__note margin-top", m["noteMarginTop"], "-16px")
    # 第四十九轮改成 -34（需求方点名）。这条本来是「桌面端别动」的守卫，
    # 值跟着新需求走，守卫本身留着 —— 手机的 -16 不许被顺手带走。
    eq("1440 .gb-stats__note margin-top (r50 client-set -34)", d["noteMarginTop"], "-34px")
    eq("390 arrows visible (243:28620/32/41/53)", m["arrowDisplay"], "block")
    eq("1440 arrows visible", d["arrowDisplay"], "block")
    if "matrix(-1" not in m["bearImgXform"]:
        FAILS.append(f"390 .gb-stats__bear-img must be mirrored (332:16221): {m['bearImgXform']}")
    eq("1440 .gb-stats__bear-img not mirrored", d["bearImgXform"], "none")
    # r39: client re-measured off the screenshot -- 78/48 instead of 65/63, and
    # the margin moved from narrow onto the stack tier so the arrows, which now
    # show from 1024 down, have the same room to hang in there.
    eq("390 bear slot opens the arrow gaps", m["bearMargin"], ["78px", "48px"])
    # board Benefits 243:28608 is 845.34 tall
    eq("390 .gb-stats__grid height vs board 845.34", m["gridH"], 845.34, tol=2)
    eq("390 the clip is on the art, not the slot", m["bearArtOverflow"], "hidden")

    # --- 4 / 8 structure ---
    for k, want, node in (("waveCreamParent", "gb-science", "236:10300 sits before science"),
                          ("waveLimeParent", "gb-product gb-product--lg", "243:22225 opens PDP"),
                          ("decoParent", "gb-science", "243:28564 paints last")):
        eq(f"390 {k} ({node})", m[k], want)
        eq(f"1440 {k} ({node})", d[k], want)
    eq("1440 .gb-stats z-index hack removed", d["statsZ"], "auto")
    # the wave must still land exactly on the section boundary
    eq("390 wave bottom == science top", m["waveBottomVsSeam"], 0, tol=1.5)
    eq("1440 wave bottom == science top", d["waveBottomVsSeam"], 0, tol=1.5)
    # deco bear: board 3244.5 vs 3304.11 (1440) and 3215.0 vs 3224.34 (390)
    eq("1440 deco centre above seam", d["decoCentreAboveSeam"], 59.61, tol=2)
    # r37: the client re-measured this off the design screenshots and moved the
    # bear up to 22.34 above the seam (and pinned its width in px, see the scss).
    eq("390 deco centre above seam", m["decoCentreAboveSeam"], 22.34, tol=2)
    eq("1440 deco centre across (81.28%)", d["decoCentrePct"], 81.28, tol=0.6)
    eq("390 deco centre across (69.36%)", m["decoCentrePct"], 69.36, tol=0.6)
    if "matrix(-" not in m["decoXform"]:
        FAILS.append(f"390 deco bear must be mirrored (243:28564): {m['decoXform']}")
    if d["decoXform"] == "none":
        FAILS.append("1440 deco bear must be rotated 18.52deg (341:47524)")

    # --- 6 science ---
    eq("390 .gb-science padding-top", m["sciPadTop"], "53px")
    eq("1440 .gb-science padding-top untouched", d["sciPadTop"], "96px")
    eq("390 head left-aligned (228:8166 TEXT align LEFT)", m["headAlign"], ["flex-start", "left"])
    eq("1440 head still centred (341:46641)", d["headAlign"], ["center", "center"])
    eq("390 head gap (228:8166 itemSpacing 16)", m["headGap"], "16px")
    eq("390 inner align", m["innerAlign"], "flex-start")
    eq("1440 inner align untouched", d["innerAlign"], "center")
    eq("390 inner gap", m["innerGap"], "46px")
    eq("1440 inner gap untouched", d["innerGap"], "48px")
    eq("390 cards gap", m["cardsGap"], "31px")
    eq("1440 cards gap untouched", d["cardsGap"], "24px")
    eq("390 card body gap", m["bodyGap"], "19px")
    eq("1440 card body gap untouched", d["bodyGap"], "22px")
    eq("390 highlight radius (236:10405 cornerRadius 16)", m["hlRadius"], "16px")
    eq("1440 highlight radius (341:46409 cornerRadius 24)", d["hlRadius"], "24px")

    # --- 7 ---
    eq("390 lip 143.35% of the media (228:8969 444.41/310)",
       m["lipWidth"] / m["mediaWidth"] * 100, 143.35, tol=0.5)
    eq("1440 lip still 158% (324:37001 573/362.67)",
       d["lipWidth"] / d["mediaWidth"] * 100, 158.0, tol=0.5)
    eq("390 media radius (228:8968 [8,8,0,0])", m["mediaRadius"], ["8px", "0px"])
    eq("1440 media radius (285:21045 [16,16,8,8])", d["mediaRadius"], ["16px", "8px"])
    eq("390 highlight text max-width", m["hlTextMax"], "283px")
    eq("1440 highlight text max-width untouched", d["hlTextMax"], "271px")
    # calc(51.5% - fluid(107, 420.97)):  390 -> .515*390 - 107,  1440 -> .515*1440 - 420.97
    eq("390 .gb-nutrition__bears-img left", m["bearsImgLeftPx"], 0.515 * 390 - 107, tol=0.5)
    eq("1440 .gb-nutrition__bears-img left", d["bearsImgLeftPx"], 0.515 * 1440 - 420.97, tol=0.5)
    eq("390 .gb-pack-band left (228:9018 75.75%)", m["packLeftPct"], 76.0, tol=0.3)
    eq("1440 .gb-pack-band left (341:46422 50.00%)", d["packLeftPct"], 50.0, tol=0.3)

    # --- guards ---
    eq("390 no horizontal overflow", m["overflowX"], 0)
    eq("1440 no horizontal overflow", d["overflowX"], 0)
    eq("390 science title mobile break shown (228:8167 has 2x U+2028)", m["brNarrow"], "inline")
    eq("1440 science title mobile break hidden (341:46642 has 1)", d["brNarrow"], "none")

    if FAILS:
        print(f"r36 FAIL — {len(FAILS)} assertion(s)")
        for f in FAILS:
            print("  ✗", f)
        sys.exit(1)
    print("r36 OK — all assertions pass, 390 + 1440")

asyncio.run(main())
