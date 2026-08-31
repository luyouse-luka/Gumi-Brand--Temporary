#!/usr/bin/env python3
"""Round-40 assertions — the five items in 修改任务文档.txt.

    python3 tools/r40check.py

Item 1 (the mobile drawer) is an interaction, so it is driven for real: the
toggle is clicked, the slide is waited out, and the panel is closed again with
its own button. Everything else is computed style / geometry on index.html and
pdp.html at 390 (narrow), 768 + 1024 (tablet) and 1440 (desktop).

Every mobile change carries a matching "desktop untouched" assertion — the
client asked for phone values, and three of these selectors are shared with the
desktop boards.

Two negative assertions here ("the icons are covered", "the app slot is gone")
are guarded: each first proves its anchor exists, so a 404 or an empty document
fails loudly instead of passing by absence.
"""
import asyncio, os, re, sys
from playwright.async_api import async_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXE = "/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome"

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


# --- 1 + 2: the drawer, driven for real ------------------------------------
DRAWER = r"""() => {
  const q = s => document.querySelector(s);
  const cs = (s,p) => { const e=q(s); return e ? getComputedStyle(e)[p] : 'NO-ELEMENT'; };
  const R = s => { const e=q(s); if(!e) return null; const r=e.getBoundingClientRect();
    return {x:+r.x.toFixed(2), y:+r.y.toFixed(2), w:+r.width.toFixed(2), h:+r.height.toFixed(2)}; };
  const icons = q('.gb-header__icons');
  const ib = icons ? icons.getBoundingClientRect() : null;
  return {
    panelPos:   cs('.gb-header__panel','position'),
    panelZ:     cs('.gb-header__panel','zIndex'),
    panelDur:   cs('.gb-header__panel','transitionDuration'),
    panelEase:  cs('.gb-header__panel','transitionTimingFunction'),
    panelRect:  R('.gb-header__panel'),
    barDisplay: cs('.gb-header__panel-bar','display'),
    barRect:    R('.gb-header__panel-bar'),
    closeRect:  R('.gb-header__panel-close'),
    logoRect:   R('.gb-header__panel-logo'),
    cardsRect:  R('.gb-header__cards'),
    innerPadTop: cs('.gb-header__panel-inner','paddingTop'),
    innerGap:    cs('.gb-header__panel-inner','rowGap'),
    // anchor first: if the icons are missing, "covered" would pass by absence
    iconsExist: !!icons,
    iconsHitTest: ib ? (() => {
      const hit = document.elementFromPoint(ib.x + ib.width/2, ib.y + ib.height/2);
      return hit ? (hit.closest('.gb-header__panel') ? 'PANEL' : 'BAR') : 'NOTHING';
    })() : null,
    htmlOverflow: getComputedStyle(document.documentElement).overflow,
    bodyOverflow: getComputedStyle(document.body).overflow,
    scrollbarVar: getComputedStyle(document.documentElement).getPropertyValue('--scrollbar-w').trim(),
    isOpen: document.getElementById('site-header').classList.contains('is-open'),
    transform: cs('.gb-header__panel','transform'),
  };
}"""

# --- 3: hero float (no settle stylesheet here, the animation IS the subject)
FLOAT = r"""() => {
  const e = document.querySelector('.gb-hero__art');
  if (!e) return null;
  const c = getComputedStyle(e);
  return {name:c.animationName, dur:c.animationDuration, delay:c.animationDelay,
          iter:c.animationIterationCount, comp:c.animationComposition,
          bearTransform:getComputedStyle(document.querySelector('.gb-hero__bear')).transform};
}"""

# --- 4 + 5: values ----------------------------------------------------------
VALUES = r"""() => {
  const q = s => document.querySelector(s);
  const cs = (s,p) => { const e=q(s); return e ? getComputedStyle(e)[p] : 'NO-ELEMENT'; };
  const R = s => { const e=q(s); if(!e) return null; const r=e.getBoundingClientRect();
    return {x:+r.x.toFixed(2), y:+r.y.toFixed(2), w:+r.width.toFixed(2), h:+r.height.toFixed(2)}; };
  const o = {};
  // 5 — PDP
  o.productPadTop  = cs('.gb-product--page','paddingTop');
  o.imageRadius    = cs('.gb-product__image','borderTopLeftRadius');
  o.lipLeft        = cs('.gb-promo-card__lip--h','left');
  o.lipBottom      = cs('.gb-promo-card__lip--h','bottom');
  o.lipRect        = R('.gb-promo-card__lip--h');
  o.lipDisplay     = cs('.gb-promo-card__lip--h','display');
  o.lipMaxWidth    = cs('.gb-promo-card__lip--h','maxWidth');
  // SVGElement has no offsetParent at all (it is an HTMLElement property), and
  // a display:none box reports a zero rect — so measure against the parent,
  // which is the lip's containing block, and treat zero width as "not painted".
  { const e = q('.gb-promo-card__lip--h');
    const b = e && e.getBoundingClientRect();
    const p = e && e.parentElement;
    o.lipWidthPct = (b && b.width) ? +(b.width / p.clientWidth * 100).toFixed(2) : null;
    o.lipRatio = (b && b.height) ? +(b.width / b.height).toFixed(3) : null; }
  { const e = q('.gb-promo-art__img');
    const p = e && e.offsetParent;
    o.artTopPct = p ? +(parseFloat(getComputedStyle(e).top) / p.clientHeight * 100).toFixed(2) : null; }
  o.listMarginRight = cs('.gb-promo-card__list','marginRight');
  // `margin: 0 auto` resolves to real pixels, so centring is left == right
  o.listMarginLeft  = parseFloat(cs('.gb-promo-card__list','marginLeft'));
  o.listMarginRightPx = parseFloat(cs('.gb-promo-card__list','marginRight'));
  o.listSvg        = [cs('.gb-promo-card__list-item svg','width'),
                      cs('.gb-promo-card__list-item svg','height')];
  o.disclaimerMT   = cs('.gb-reviews__disclaimer','marginTop');
  o.vsPadTop       = cs('.gb-vs','paddingTop');
  o.vsRowPadTop    = cs('.gb-vs__row + .gb-vs__row','paddingTop');
  o.vsValuePadRight= cs('.gb-vs__value','paddingRight');
  o.vsOthersTop    = cs('.gb-vs__others','top');
  o.faqPadTop      = cs('.gb-faq','paddingTop');
  o.faqPadBottom   = cs('.gb-faq','paddingBottom');
  // anchor first: the section must still be here for "slot removed" to mean anything
  o.appSectionExists = !!q('.gb-app-section__inner');
  o.appSlotCount     = document.querySelectorAll('.gb-app-slot').length;
  return o;
}"""

NL = r"""() => {
  const q = s => document.querySelector(s);
  const cs = (s,p) => { const e=q(s); return e ? getComputedStyle(e)[p] : 'NO-ELEMENT'; };
  const tb = q('.gb-nl-table'); if (!tb) return null;
  const tr = tb.querySelector('tbody tr');
  const L = tb.getBoundingClientRect().x;
  // ink, not the cell box: the board's numbers are positioned by their glyphs
  const ink = [...tr.children].slice(1).map(c => {
    const r = document.createRange(); r.selectNodeContents(c);
    const b = r.getBoundingClientRect();
    return {t: c.textContent.trim(), x: +(b.x - L).toFixed(2)};
  });
  return {
    paneGap: cs('.gb-nl-pane--info','rowGap'),
    fs: cs('.gb-nl-table','fontSize'),
    lh: cs('.gb-nl-table','lineHeight'),
    family: cs('.gb-nl-table','fontFamily').split(',')[0].replace(/"/g,''),
    weight: cs('.gb-nl-table','fontWeight'),
    ls: cs('.gb-nl-table','letterSpacing'),
    thPadTop: cs('.gb-nl-table th','paddingTop'),
    capPadTop: cs('.gb-nl-table caption','paddingTop'),
    capBorderTop: cs('.gb-nl-table caption','borderTopWidth'),
    subPad: cs('.gb-nl-table .gb-nl-table__sub','paddingLeft'),
    notesFs: cs('.gb-nl-notes','fontSize'),
    tableW: +tb.getBoundingClientRect().width.toFixed(2),
    ink,
  };
}"""


async def open_nl(pg):
    await pg.click(".gb-product__label-btn")
    await pg.wait_for_timeout(600)
    tabs = await pg.query_selector_all(".gb-nl-tab")
    await tabs[1].click()               # Ingredient List
    await pg.wait_for_timeout(400)


async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path=EXE)

        # ---- 1 + 2: drawer at 390, dropdown at 1440 ------------------------
        drawer = {}
        for w in (390, 1440):
            pg = await b.new_page(viewport={"width": w, "height": 844})
            await pg.goto("file://" + os.path.join(ROOT, "index.html"))
            await pg.evaluate("() => document.fonts.ready")
            await pg.wait_for_timeout(300)
            drawer[(w, "shut")] = await pg.evaluate(DRAWER)
            await pg.click(".gb-header__toggle")
            await pg.wait_for_timeout(1000)          # $t-drawer is 0.7s
            drawer[(w, "open")] = await pg.evaluate(DRAWER)
            if w == 390:                             # close with the panel's own button
                await pg.click(".gb-header__panel-close")
                await pg.wait_for_timeout(1000)
                drawer[(w, "reshut")] = await pg.evaluate(DRAWER)
            await pg.close()

        # ---- 3: hero float, real animation ---------------------------------
        pg = await b.new_page(viewport={"width": 1440, "height": 900})
        await pg.goto("file://" + os.path.join(ROOT, "index.html"))
        await pg.evaluate("() => document.fonts.ready")
        await pg.wait_for_timeout(300)
        float_cs = await pg.evaluate(FLOAT)
        drift = []
        for t in (900, 2150, 3400, 4650):
            await pg.evaluate("t => document.querySelector('.gb-hero__art').getAnimations()"
                              ".forEach(a => { a.pause(); a.currentTime = t; })", t)
            await pg.wait_for_timeout(50)
            drift.append(await pg.evaluate(
                "() => +document.querySelector('.gb-hero__art').getBoundingClientRect().y.toFixed(2)"))
        await pg.close()

        # reduced motion must drop the drift entirely
        pg = await b.new_page(viewport={"width": 1440, "height": 900},
                              reduced_motion="reduce")
        await pg.goto("file://" + os.path.join(ROOT, "index.html"))
        await pg.wait_for_timeout(300)
        float_rm = await pg.evaluate(FLOAT)
        await pg.close()

        # ---- 4 + 5: pdp values ---------------------------------------------
        vals, nl = {}, {}
        for w in (390, 768, 1024, 1440):
            pg = await b.new_page(viewport={"width": w, "height": 1000})
            await pg.goto("file://" + os.path.join(ROOT, "pdp.html"))
            await pg.evaluate("() => document.fonts.ready")
            await pg.wait_for_timeout(400)
            vals[w] = await pg.evaluate(VALUES)
            await open_nl(pg)
            nl[w] = await pg.evaluate(NL)
            await pg.close()
        await b.close()

    D = lambda w, s: drawer[(w, s)]
    V = lambda w: vals[w]
    N = lambda w: nl[w]

    # ===== 1. mobile drawer =================================================
    o = D(390, "open")
    eq("390 drawer is fixed to the viewport", o["panelPos"], "fixed")
    eq("390 drawer paints over the bar", o["panelZ"], "900")
    eq("390 drawer slide duration (funkyfood's 0.7s)", o["panelDur"], "0.7s")
    eq("390 drawer easing (funkyfood's curve)", o["panelEase"], "cubic-bezier(0.77, 0, 0.175, 1)")
    r = o["panelRect"]
    eq("390 drawer starts at the viewport top", r["y"], 0, tol=0.5)
    eq("390 drawer is full width", r["w"], 390, tol=0.5)
    eq("390 drawer is full height", r["h"], 844, tol=1)
    eq("390 drawer is slid in", o["transform"], "matrix(1, 0, 0, 1, 0, 0)")
    # the account / cart icons must actually be behind it — anchor guarded
    ok_if("390 the header icons exist to be covered", o["iconsExist"])
    eq("390 the icons are covered by the drawer", o["iconsHitTest"], "PANEL")
    # the panel's own close row, against board 283:14915
    eq("390 panel bar shows", o["barDisplay"], "grid")
    eq("390 close icon x (board 20)", o["closeRect"]["x"], 20, tol=0.6)
    eq("390 close icon 24x24", [o["closeRect"]["w"], o["closeRect"]["h"]], [24.0, 24.0])
    eq("390 logo 93x24 (board 92.88)", [o["logoRect"]["w"], o["logoRect"]["h"]], [93.0, 24.0])
    logo_c = o["logoRect"]["x"] + o["logoRect"]["w"] / 2
    eq("390 logo optically centred (board 195.5)", logo_c, 195, tol=1.5)
    # the client's 9 + 15 land the nav cards on the board's own 72
    eq("390 nav cards start at the board's 72", o["cardsRect"]["y"], 72, tol=1)
    eq("390 nav cards 350x169 (board)", [o["cardsRect"]["w"], o["cardsRect"]["h"]], [350.0, 169.0])
    # page locked, and the freed scrollbar width padded back in
    eq("390 html locked", o["htmlOverflow"], "hidden")
    eq("390 body locked", o["bodyOverflow"], "hidden")
    ok_if("390 --scrollbar-w was measured", re.match(r"^-?\d", o["scrollbarVar"] or ""),
          f"got {o['scrollbarVar']!r}")
    # closing with the panel's own button really closes and unlocks
    c = D(390, "reshut")
    ok_if("390 the panel's close button closes it", not c["isOpen"])
    eq("390 drawer slid back out", c["transform"], "matrix(1, 0, 0, 1, -390, 0)")
    eq("390 page unlocked again", c["htmlOverflow"], "visible")
    # shut state
    s = D(390, "shut")
    eq("390 drawer starts off-screen", s["transform"], "matrix(1, 0, 0, 1, -390, 0)")
    eq("390 page not locked before opening", s["htmlOverflow"], "visible")

    # desktop is still the dropdown, untouched
    for st in ("shut", "open"):
        d = D(1440, st)
        eq(f"1440 panel is still the absolute dropdown ({st})", d["panelPos"], "absolute")
        eq(f"1440 panel bar hidden ({st})", d["barDisplay"], "none")
    eq("1440 dropdown keeps its 0.35s grid animation",
       D(1440, "open")["panelDur"], "0.35s")
    ok_if("1440 the icons are NOT covered", D(1440, "open")["iconsHitTest"] == "BAR",
          f"hit {D(1440,'open')['iconsHitTest']}")
    eq("1440 page never locked", D(1440, "open")["htmlOverflow"], "visible")

    # ===== 2. panel inner ===================================================
    eq("390 .gb-header__panel-inner padding-top (client-set)", D(390, "open")["innerPadTop"], "9px")
    eq("390 .gb-header__panel-inner gap (client-set)", D(390, "open")["innerGap"], "15px")
    eq("1440 .gb-header__panel-inner padding-top untouched",
       D(1440, "open")["innerPadTop"], "32px")

    # ===== 3. hero bear drifts again =======================================
    eq("hero art runs fade + float", float_cs["name"], "gm-art-fade-in, gm-art-float")
    eq("hero float is a 5s loop", float_cs["dur"], "0.7s, 5s")
    eq("hero float starts as the fade lands", float_cs["delay"], "0.2s, 0.9s")
    eq("hero float never stops", float_cs["iter"], "1, infinite")
    eq("hero float is composited onto the fade", float_cs["comp"], "replace, add")
    travel = round(max(drift) - min(drift), 2)
    eq("hero drift travels the keyframe's 15px", travel, 15, tol=0.6)
    # the bear's own 7.92deg tilt must survive — the float is on the wrapper
    ok_if("hero bear keeps its own tilt", float_cs["bearTransform"].startswith("matrix(0.990"),
          float_cs["bearTransform"])
    eq("reduced motion drops the drift", float_rm["name"], "gm-fade-in")

    # ===== 4. nutrition pane + ingredient table ============================
    eq("390 .gb-nl-pane--info gap (client-set)", N(390)["paneGap"], "24px")
    eq("1440 .gb-nl-pane--info gap untouched", N(1440)["paneGap"], "20px")
    eq("390 table font-size (board 9.5368)", N(390)["fs"], "9.54px")
    eq("390 table line-height is PP Palma's auto leading, not 100%",
       N(390)["lh"], "12.02px")
    eq("390 table family", N(390)["family"], "PP Palma")
    eq("390 table weight (FizzyLight)", N(390)["weight"], "300")
    eq("390 table tracking 0", N(390)["ls"], "normal")
    eq("390 row padding (7.64 x 0.7415)", N(390)["thPadTop"], "5.19px")
    eq("390 caption padding", N(390)["capPadTop"], "5.93px")
    eq("390 caption top rule (board 3.0)", N(390)["capBorderTop"], "3px")
    eq("390 sub-row indent", N(390)["subPad"], "8.16px")
    eq("390 notes font-size", N(390)["notesFs"], "9.71px")
    # the two number columns, measured off board 336:31186 / 336:31188
    eq("390 table is the board's 350", N(390)["tableW"], 350, tol=0.5)
    eq("390 '15 g' starts at the board's 278.95", N(390)["ink"][0]["x"], 278.95, tol=1)
    eq("390 '5%' starts at the board's 331.28", N(390)["ink"][1]["x"], 331.28, tol=1)
    # desktop untouched
    eq("1440 table font-size untouched", N(1440)["fs"], "12.9px")
    eq("1440 table line-height untouched", N(1440)["lh"], "16.2px")
    eq("1440 row padding untouched", N(1440)["thPadTop"], "7px")
    eq("1440 sub-row indent untouched", N(1440)["subPad"], "11px")
    ok_if("1440 number columns untouched",
          abs(N(1440)["ink"][0]["x"] - 611) < 1 and abs(N(1440)["ink"][1]["x"] - 683) < 1,
          f"{N(1440)['ink']}")
    # 768 must not jump: the ramp has to leave both tiers continuous
    for w in (768, 1024):
        f = float(N(w)["fs"].rstrip("px"))
        ok_if(f"{w} table font-size ramps between 9.54 and 12.9", 9.5 <= f <= 12.9, f"{f}px")

    # ===== 5. PDP values ====================================================
    v = V(390)
    eq("390 .gb-product--page padding-top (client-set)", v["productPadTop"], "20px")
    eq("390 .gb-product__image radius (client-set 16)", v["imageRadius"], "16px")
    # r51: client moved this to 50.5% (and the card's cap from 343 to 575).
    eq("390 lip--h left (client-set)", v["lipLeft"], "176.75px")    # 50.5% of 350
    eq("390 lip--h bottom (client-set)", v["lipBottom"], "-48px")
    eq("390 lip--h width is 143% of the card", v["lipWidthPct"], 143, tol=0.5)
    eq("390 lip--h keeps the svg's own 492:81 ratio", v["lipRatio"], 492 / 81, tol=0.02)
    eq("390 lip--h is not clamped by the reset's svg max-width", v["lipMaxWidth"], "none")
    # r43 reversed this: the client set -8 in this round and -5 in the next.
    # r43 moved this again: -8 (r40) -> -5 (r42) -> -4. Flipped rather than
    # deleted so the value stays under a judge and the history stays readable.
    # r51 (fourth pass) scoped it: the promo card's own artwork is back to -8%,
    # while .gb-ingredients__disc on science/reviews keeps -4%. This probe reads
    # pdp's, i.e. the white card's.
    eq("390 promo art top (client-set -8%; -4 in r43, -5 in r42, -8 in r40)",
       v["artTopPct"], -8, tol=0.2)
    # r56 briefly centred this; r57 withdrew that on the client's final answer
    # (centred on pc, NOT centred on phones), so the r40/r51 value is back and
    # this is now the settled one. Decision I is closed on it -- see r56check AQ.
    eq("390 promo list margin-right (client-set, final)", v["listMarginRight"], "15px")
    eq("390 promo list icons 20px", v["listSvg"], ["20px", "20px"])
    eq("390 reviews disclaimer margin-top (client-set)", v["disclaimerMT"], "2px")
    eq("390 .gb-vs padding-top (client-set 52)", v["vsPadTop"], "52px")
    eq("390 .gb-vs__row rule gap (client-set 11)", v["vsRowPadTop"], "11px")
    eq("390 .gb-vs__value padding-right (client-set 15)", v["vsValuePadRight"], "15px")
    eq("390 .gb-vs__others top (client-set 46.25)", v["vsOthersTop"], "46.25px")
    eq("390 .gb-faq padding (client-set 52 / 80)",
       [v["faqPadTop"], v["faqPadBottom"]], ["52px", "80px"])
    # app slot removed — anchor guarded so an empty document cannot pass this
    ok_if("the review section is still on the page", v["appSectionExists"])
    eq("the dashed app-slot placeholder is gone from pdp", v["appSlotCount"], 0)

    # desktop untouched
    d = V(1440)
    eq("1440 .gb-product--page padding-top untouched", d["productPadTop"], "96px")
    eq("1440 .gb-product__image radius untouched", d["imageRadius"], "24px")
    eq("1440 promo list icons untouched", d["listSvg"], ["24px", "24px"])
    ok_if("1440 promo list still centred", abs(d["listMarginLeft"] - d["listMarginRightPx"]) < 0.6,
          f"left {d['listMarginLeft']} vs right {d['listMarginRightPx']}")
    eq("1440 disclaimer margin-top untouched", d["disclaimerMT"], "0px")
    eq("1440 .gb-vs padding-top untouched", d["vsPadTop"], "120px")
    eq("1440 .gb-vs__row rule gap untouched", d["vsRowPadTop"], "13px")
    eq("1440 .gb-vs__value padding-right untouched", d["vsValuePadRight"], "1px")
    eq("1440 .gb-vs__others top untouched", d["vsOthersTop"], "62px")
    eq("1440 .gb-faq padding untouched",
       [d["faqPadTop"], d["faqPadBottom"]], ["96px", "120px"])
    eq("1440 lip--h is not painted", V(1440)["lipRect"]["w"], 0)
    eq("1440 lip--h display", V(1440)["lipDisplay"], "none")

    # no page may scroll sideways at any tier
    for w in (390, 768, 1024, 1440):
        pass  # covered by tools/rwd.py across all 12 pages

    if FAILS:
        print(f"r40 FAILED — {len(FAILS)} assertion(s)\n")
        for f in FAILS: print("  ✗", f)
        return 1
    print("r40 OK — all assertions pass across 390 / 768 / 1024 / 1440,"
          " drawer driven open and closed for real")
    return 0


sys.exit(asyncio.run(main()))
