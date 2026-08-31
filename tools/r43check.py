#!/usr/bin/env python3
"""Round-42 assertions — the four items added to 修改任务文档.txt (5/6/7/8).

    python3 tools/r43check.py

1. Stack point moved 991/1024 -> 767 on .gb-compare__inner, .gb-ingredients__inner,
   .gb-faq-image__inner and .gb-product__inner, and the width caps below 767 are
   gone. Two columns therefore have to survive the whole tablet tier, which is
   what actually bit: .gb-product__media was a rigid `width: 465 + flex-shrink: 0`
   and the row overflowed by 163px at 768. Both product columns are shrinkable
   basis now, so the overflow assertions below are the real judge, not the
   flex-direction ones.

2. 3 -> 2 -> 1 card grids: the 2 -> 1 step moved from 767 down to 575, so two-up
   now spans 576-1280. The single-column tier MUST reset `grid-column: span 2`
   or the implicit grid rebuilds a second column and the cards stay two-up —
   that is asserted by counting distinct card x positions, not by reading
   grid-template-columns.

3. Six client-set mobile values (第 6 条).

4. countUp: the figures must still read exactly what the markup ships once the
   animation lands. Asserted by driving the observer and sampling mid-flight as
   well as at rest — a module that never ran would pass an end-state-only check.
"""
import asyncio
import os

from playwright.async_api import async_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXE = "/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome"
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
  const q = s => document.querySelector(s);
  const cs = (s, p) => { const e = q(s); return e ? getComputedStyle(e)[p] : null; };
  const R = s => { const e = q(s); if (!e) return null; const r = e.getBoundingClientRect();
    return {x:+r.x.toFixed(1), w:+r.width.toFixed(1), h:+r.height.toFixed(1)}; };
  const o = {};

  for (const [k, sel] of [['cmp','.gb-compare__inner'], ['ing','.gb-ingredients__inner'],
                          ['fq','.gb-faq-image__inner'], ['prod','.gb-product__inner']]) {
    if (q(sel)) o[k + 'Dir'] = cs(sel, 'flexDirection');
  }
  o.disc     = R('.gb-ingredients__disc');
  o.discMax  = cs('.gb-ingredients__disc', 'maxWidth');
  o.fqMedia  = R('.gb-faq-image__media');
  o.fqMediaMax = cs('.gb-faq-image__media', 'maxWidth');
  o.ingBodyMax = cs('.gb-ingredients__body', 'maxWidth');
  o.fqBodyMax  = cs('.gb-faq-image__body', 'maxWidth');
  o.prodMedia  = R('.gb-product__media');
  o.prodInfo   = R('.gb-product__info');

  // card grids: count DISTINCT x positions, which is what "two-up" means
  o.grids = [...document.querySelectorAll('.gb-science__cards, .gb-nutrition__cards')]
    .map(g => {
      const kids = [...g.children].map(e => e.getBoundingClientRect());
      return {sel: g.className.split(' ')[0],
              cols: new Set(kids.map(r => Math.round(r.x))).size,
              rows: new Set(kids.map(r => Math.round(r.y))).size,
              n: kids.length};
    });

  // 第 6 条
  o.creamPadTop  = cs('.gb-science--cream', 'paddingTop');
  o.valueFs      = cs('.gb-science-card__value', 'fontSize');
  o.valueLh      = cs('.gb-science-card__value', 'lineHeight');
  o.tightGap     = cs('.gb-science--tight .gb-science__inner', 'rowGap');
  o.cmpGap       = cs('.gb-compare__inner', 'rowGap');
  o.promoTop     = cs('.gb-promo-art__img', 'top');
  o.promoParentH = (() => { const e = q('.gb-promo-art'); return e ? +e.getBoundingClientRect().height.toFixed(1) : null; })();
  o.faqImagePad  = [cs('.gb-faq-image', 'paddingTop'), cs('.gb-faq-image', 'paddingBottom')];

  // rail: one card per gesture
  // 第五十轮：轨道改跑 Swiper，「一次手势只走一张」由 longSwipes: false 承担，
  // scroll-snap-stop 随原生 scroller 一起没了。读 Swiper 的实际参数。
  o.oneStep = (function () { const t = document.querySelector('.gb-expert__cards');
                             return t && t.swiper ? t.swiper.params.longSwipes : null; })();
  o.hasStep  = !!q('[data-slider-step]');

  o.overflowX = document.documentElement.scrollWidth - document.documentElement.clientWidth;
  return o;
}"""

COUNT = r"""() => {
  const els = [...document.querySelectorAll('[data-count-up]')];
  return {n: els.length, texts: els.map(e => e.textContent.trim())};
}"""


async def main():
    data = {}
    plan = {"science.html": (1440, 1281, 1280, 1024, 992, 900, 768, 767, 576, 575, 390),
            "pdp.html":     (1440, 1280, 1024, 900, 768, 767, 390),
            "index.html":   (1440, 768, 576, 575, 390),
            "reviews.html": (1440, 768, 767, 390)}
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path=EXE)
        for page, widths in plan.items():
            for w in widths:
                pg = await b.new_page(viewport={"width": w, "height": 1000})
                await pg.goto("file://" + os.path.join(ROOT, page))
                await pg.add_style_tag(content=SETTLE)
                await pg.evaluate("() => document.fonts.ready")
                await pg.wait_for_timeout(220)
                data[(page, w)] = await pg.evaluate(PROBE)
                await pg.close()

        # countUp runs bare: SETTLE does not touch it, but the figures have to be
        # scrolled into view for the observer to fire.
        pg = await b.new_page(viewport={"width": 1440, "height": 900})
        await pg.goto("file://" + os.path.join(ROOT, "science.html"))
        await pg.evaluate("() => document.fonts.ready")
        before = await pg.evaluate(COUNT)
        await pg.evaluate("() => document.querySelector('.gb-science-card__value').scrollIntoView()")
        await pg.wait_for_timeout(180)          # mid-flight
        during = await pg.evaluate(COUNT)
        await pg.wait_for_timeout(2000)         # COUNT_MS is 1400
        after = await pg.evaluate(COUNT)
        await pg.close()
        await b.close()

    S = lambda w: data[("science.html", w)]
    P = lambda w: data[("pdp.html", w)]
    I = lambda w: data[("index.html", w)]
    V = lambda w: data[("reviews.html", w)]

    # ===== 1. stack point at 767 ==========================================
    for w in (1440, 1280, 1024, 992, 900, 768):
        eq(f"{w} compare is two columns", S(w)["cmpDir"], "row")
        eq(f"{w} ingredients is two columns", S(w)["ingDir"], "row")
        eq(f"{w} faq-image is two columns", S(w)["fqDir"], "row")
    for w in (767, 576, 575, 390):
        eq(f"{w} compare has stacked", S(w)["cmpDir"], "column")
        eq(f"{w} ingredients has stacked", S(w)["ingDir"], "column")
        eq(f"{w} faq-image has stacked", S(w)["fqDir"], "column")
    for w in (1440, 1280, 1024, 900, 768):
        eq(f"{w} pdp product is two columns", P(w)["prodDir"], "row")
    for w in (767, 390):
        eq(f"{w} pdp product has stacked", P(w)["prodDir"], "column")

    # the regression this actually guards: a rigid 465 overflowed 768 by 163
    for page, fn, widths in (("science", S, (1440, 1280, 1024, 992, 900, 768, 767, 576, 575, 390)),
                             ("pdp", P, (1440, 1280, 1024, 900, 768, 767, 390)),
                             ("reviews", V, (1440, 768, 767, 390)),
                             ("index", I, (1440, 768, 576, 575, 390))):
        for w in widths:
            eq(f"{w} {page}: no horizontal overflow", fn(w)["overflowX"], 0)
    for w in (1024, 900, 768):
        d = P(w)
        ok_if(f"{w} pdp both product columns are real",
              d["prodMedia"]["w"] > 250 and d["prodInfo"]["w"] > 250,
              f"media {d['prodMedia']['w']} / info {d['prodInfo']['w']}")
    # desktop untouched
    eq("1440 pdp media is the board's 465", P(1440)["prodMedia"]["w"], 465, tol=0.5)
    eq("1440 pdp info is the board's 465", P(1440)["prodInfo"]["w"], 465, tol=0.5)

    # caps below 767: r43 put 520 back on the two squares (they ran edge to edge
    # at 767 without it) and left both BODY caps off, which is still r42's ask.
    for w in (767, 575, 390):
        eq(f"{w} ingredients disc capped 520 (r42 had none)", S(w)["discMax"], "520px")
        eq(f"{w} faq-image media capped 520 (r42 had none)", S(w)["fqMediaMax"], "520px")
        eq(f"{w} ingredients body has no cap", S(w)["ingBodyMax"], "none")
        eq(f"{w} faq-image body has no cap", S(w)["fqBodyMax"], "none")
        # square stays square whatever width it lands on
        d = S(w)
        eq(f"{w} disc is still square", d["disc"]["w"], d["disc"]["h"], tol=1.0)

    # ===== 2. card grids: 2 -> 1 at 575 ===================================
    # Rows, not distinct x: a lone third card is CENTRED on the two-up tiers, so
    # it shares neither column's x and a column count reads 3 for a two-up grid.
    # 3 cards: one row when three-up, two when two-up, three when single file.
    # r51: the 3→2 step moved from 1280 down to 1200 (client-set), so 1280 now
    # runs three-up on one row. 1201/1200 is judged as a seam in r52check §1.
    for w, want_rows in ((1440, 1), (1281, 1), (1280, 1), (1024, 2), (768, 2), (576, 2),
                         (575, 3), (390, 3)):
        for g in S(w)["grids"]:
            eq(f"{w} {g['sel']} ({g['n']} cards) runs {want_rows} row(s)", g["rows"], want_rows)
    for w, want_rows in ((1440, 1), (768, 2), (576, 2), (575, 3), (390, 3)):
        for g in I(w)["grids"]:
            eq(f"{w} index {g['sel']} ({g['n']} cards) runs {want_rows} row(s)",
               g["rows"], want_rows)
    # the span reset: at 575 every card sits at the same x (one true column).
    # Without resetting `grid-column: span 2` the implicit grid rebuilds a
    # second column and they alternate between two x values instead.
    for g in S(575)["grids"]:
        eq(f"575 {g['sel']} is a single column (spans reset)", g["cols"], 1)

    # ===== 3. the six client-set mobile values ============================
    eq("390 .gb-science--cream padding-top (client-set 64)", S(390)["creamPadTop"], "64px")
    # 第四十九轮把这条撤回板值 56/44；第五十三轮需求方再次反转，手机端回到
    # 36/40/-0.36（324:58044 的规格），两组卡一起。详见 CHANGELOG 第五十三轮。
    eq("390 .gb-science-card__value font-size (r53 client-set 36)", S(390)["valueFs"], "36px")
    eq("390 .gb-science-card__value line-height (r53)", S(390)["valueLh"], "40px")
    eq("390 .gb-science--tight .gb-science__inner gap", S(390)["tightGap"], "48px")
    eq("390 .gb-compare__inner gap", S(390)["cmpGap"], "46px")
    # top is a percentage of the parent box, so assert the resolved pixels
    # r43: -5% -> -4% (third move; -8 in r40). r51 scoped it to the promo card
    # and put that one back to -8%; the probe reads pdp, i.e. the white card.
    # .gb-ingredients__disc still reads -4% — asserted in r52check §6.
    ok_if("390 .gb-promo-art__img top is -8% of its box (scoped to the promo card)",
          abs(float(P(390)["promoTop"][:-2]) + 0.08 * P(390)["promoParentH"]) < 1.0,
          f"{P(390)['promoTop']} against a {P(390)['promoParentH']}px box")
    eq("390 .gb-faq-image padding", S(390)["faqImagePad"], ["64px", "80px"])
    # desktop untouched
    eq("1440 .gb-science-card__value untouched", S(1440)["valueFs"], "56px")
    eq("1440 .gb-faq-image padding untouched", S(1440)["faqImagePad"], ["96px", "120px"])

    # ===== 4. rail: one card per gesture ==================================
    eq("390 expert rail steps one card per gesture", V(390)["oneStep"], False)
    eq("767 expert rail steps one card per gesture", V(767)["oneStep"], False)
    ok_if("reviews carries data-slider-step", V(390)["hasStep"])

    # ===== 5. countUp =====================================================
    ok_if("countUp: science.html carries its 6 hooks", before["n"] == 6, f"{before['n']} found")
    # mid-flight the figure must be BELOW its final value — this is what proves
    # the module ran at all; an end-state check alone passes when it never did.
    moved = sum(1 for a, b in zip(during["texts"], after["texts"]) if a != b)
    ok_if("countUp: figures were mid-count 180ms in", moved > 0,
          f"during={during['texts'][:3]} after={after['texts'][:3]}")
    eq("countUp: every figure lands on its authored value", after["texts"], before["texts"])

    print("=" * 72)
    if FAILS:
        print(f"FAIL — {len(FAILS)}")
        for f in FAILS:
            print("  ✗", f)
    else:
        print("r43: all assertions pass")
    print("=" * 72)
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
