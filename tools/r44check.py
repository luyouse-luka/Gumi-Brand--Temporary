#!/usr/bin/env python3
"""Round-43 assertions — the nine items in 修改任务文档.txt (第三批).

    python3 tools/r44check.py

Where the judge is not the obvious one, and why:

1. 第 2 条 (expert rail centred on the phone) is asserted as GEOMETRY, not as a
   computed `scroll-snap-align`. Reading the property back only proves the
   declaration exists; it says nothing about whether a card can actually come to
   rest centred, which is the whole request. The rail is driven to a snap
   position and the two neighbours' visible slivers are measured — they have to
   be non-zero AND equal. That also covers the loop: without clones the first
   card has nothing on its left and the left sliver reads 0.

2. 第 5 条 (dosed down to 767) is asserted as OVERFLOW plus a both-columns-real
   check, not as flex-direction. The direction flip is the easy half; the half
   that actually broke on .gb-product in r42 was a rigid basis starving the row,
   and .gb-dosed__media was the same `flex: 0 0 598px + width: 598px`. At 1100 it
   left the body 258px wide — inside the band that already existed, so this is a
   fix as much as a move.

3. 第 8/9 条 (gutter moves from body to inner, squares capped at 520) is
   asserted by measuring where the TEXT starts and how wide the SQUARE is, not
   by reading padding-inline off two elements. The point of the pair is that the
   copy keeps its 20px inset while the square stops running edge to edge; a
   property-level check passes even if the two changes cancel out.

4. 第 4 条's padding-bottom is checked on all three plain tiles AND on the two
   modified ones — the brief's :not() is implemented by source order (--lg and
   --page restate padding-bottom in the same tier), so the guard has to prove the
   46 did NOT leak into them.
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

  // 1. page-hero media cap
  o.heroMedia    = R('.gb-page-hero__media');
  o.heroMediaMax = cs('.gb-page-hero__media', 'maxWidth');
  o.heroText     = R('.gb-page-hero__text');
  o.heroInner    = R('.gb-page-hero__inner');

  // 3/4. section paddings
  o.appLg    = [cs('.gb-app-section--lg', 'paddingTop'), cs('.gb-app-section--lg', 'paddingBottom')];
  o.appBase  = q('.gb-app-section:not(.gb-app-section--lg)')
    ? getComputedStyle(q('.gb-app-section:not(.gb-app-section--lg)')).paddingTop : null;
  const prod = q('.gb-product');
  o.prodMod  = prod ? (prod.classList.contains('gb-product--lg') ? 'lg'
                     : prod.classList.contains('gb-product--page') ? 'page' : 'plain') : null;
  o.prodPadB = prod ? getComputedStyle(prod).paddingBottom : null;
  /* --sc-h/--sc-lg-h read back as the unevaluated calc() string, not pixels, so
     they have to be resolved by measuring a throwaway box. */
  const resolve = v => { const d = document.createElement('div');
    d.style.cssText = 'position:absolute;visibility:hidden;width:0;height:' + v;
    document.body.appendChild(d);
    const h = d.getBoundingClientRect().height; d.remove(); return +h.toFixed(2); };
  o.scH      = resolve('var(--sc-h)') + 'px';
  o.scLgH    = resolve('var(--sc-lg-h)') + 'px';

  // 4b. promo art
  o.promoTop     = cs('.gb-promo-art__img', 'top');
  o.promoParentH = (() => { const e = q('.gb-promo-art'); return e ? +e.getBoundingClientRect().height.toFixed(1) : null; })();

  // 5. dosed
  o.dosedDir   = cs('.gb-dosed__block', 'flexDirection');
  o.dosedMedia = R('.gb-dosed__media');
  o.dosedBody  = R('.gb-dosed__body');
  o.dosedBodyMax = cs('.gb-dosed__body', 'maxWidth');
  o.dosedText  = R('.gb-dosed__text');

  // 6. product
  o.prodInnerMax = cs('.gb-product__inner', 'maxWidth');
  o.prodMedia    = R('.gb-product__media');
  o.prodInfo     = R('.gb-product__info');
  o.prodInner    = R('.gb-product__inner');

  // 7. coral lead is gone
  o.coralInDom = !!q('.gb-page-hero__lead--coral-mobile');
  o.leadColor  = cs('.gb-page-hero__lead', 'color');

  // 8/9. ingredients / faq-image: square width + where the copy starts
  o.disc     = R('.gb-ingredients__disc');
  o.discMax  = cs('.gb-ingredients__disc', 'maxWidth');
  o.ingBody  = R('.gb-ingredients__body');
  o.ingTitle = R('.gb-ingredients__title') || R('.gb-ingredients__body > *');
  o.fqMedia  = R('.gb-faq-image__media');
  o.fqMediaMax = cs('.gb-faq-image__media', 'maxWidth');
  o.fqBody   = R('.gb-faq-image__body');
  o.fqTitle  = R('.gb-faq-image__title') || R('.gb-faq-image__body > *');

  o.overflowX = document.documentElement.scrollWidth - document.documentElement.clientWidth;
  o.vw = document.documentElement.clientWidth;
  return o;
}"""

# Drive the rail to a rest position and measure the neighbours' visible slivers.
RAIL = r"""async () => {
  const track = document.querySelector('.gb-expert__cards');
  if (!track) return {err: 'no track'};
  const wait = ms => new Promise(r => setTimeout(r, ms));
  // 第五十轮：轨道改跑 Swiper，卡片下移到 .swiper-wrapper 里，scrollLeft 不再是它的
  // 状态。Swiper 的每一个停位本来就是休止位（不像旧的原生 scroller 要先推一下让 snap
  // 收敛），所以直接量载入后的休止位 —— 那也正是用户第一眼看到的那一帧。
  await wait(300);
  const port = track.getBoundingClientRect();
  const kids = [...track.querySelectorAll('.swiper-slide')].map(e => e.getBoundingClientRect())
    .map(r => ({l: r.left - port.left, r: r.right - port.left, w: r.width}));
  const mid = port.width / 2;
  // the card the centre line falls in
  const i = kids.findIndex(k => k.l <= mid && k.r >= mid);
  if (i < 0) return {err: 'no card under the centre line', n: kids.length};
  const c = kids[i];
  return {
    n: kids.length,
    portW: +port.width.toFixed(1),
    offCentre: +(((c.l + c.r) / 2) - mid).toFixed(1),
    leftPeek:  i > 0 ? +(kids[i - 1].r).toFixed(1) : -1,
    rightPeek: i + 1 < kids.length ? +(port.width - kids[i + 1].l).toFixed(1) : -1,
    swiperLive: !!track.swiper,
    isRail: getComputedStyle(track).overflowX,
  };
}"""


async def main():
    data = {}
    plan = {
        "how-gumi-works.html": (1440, 1281, 1280, 1100, 1024, 992, 900, 768, 767, 575, 390),
        "reviews.html":        (1440, 1280, 768, 767, 575, 390),
        "pdp.html":            (1440, 1280, 768, 767, 390),
        "index.html":          (1440, 768, 767, 390),
        "our-story.html":      (1440, 768, 767, 390),
        "science.html":        (1440, 1281, 1280, 1024, 768, 767, 575, 390),
    }
    rail = {}
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path=EXE)
        for page, widths in plan.items():
            for w in widths:
                pg = await b.new_page(viewport={"width": w, "height": 1000})
                await pg.goto("file://" + os.path.join(ROOT, page))
                await pg.add_style_tag(content=SETTLE)
                await pg.evaluate("() => document.fonts.ready")
                await pg.wait_for_timeout(240)
                data[(page, w)] = await pg.evaluate(PROBE)
                await pg.close()
        # rail geometry, on a bare page (no SETTLE): scroll-snap is what is being
        # measured and injected !important rules have masked a rail before.
        for w in (390, 575, 767, 900):
            pg = await b.new_page(viewport={"width": w, "height": 1000})
            await pg.goto("file://" + os.path.join(ROOT, "reviews.html"))
            await pg.evaluate("() => document.fonts.ready")
            await pg.wait_for_timeout(400)
            rail[w] = await pg.evaluate(RAIL)
            await pg.close()
        await b.close()

    H = lambda w: data[("how-gumi-works.html", w)]
    V = lambda w: data[("reviews.html", w)]
    P = lambda w: data[("pdp.html", w)]
    I = lambda w: data[("index.html", w)]
    O = lambda w: data[("our-story.html", w)]
    S = lambda w: data[("science.html", w)]

    # ===== 第 1 条 page-hero media cap 570 ================================
    for name, fn in (("science", S), ("reviews", V)):
        for w in (767, 575, 390):
            eq(f"{w} {name} hero media cap is 570", fn(w)["heroMediaMax"], "570px")
        # only bites above 570 + gutters; 390 must be unchanged (350 content)
        eq(f"390 {name} hero media still fills the version", fn(390)["heroMedia"]["w"], 350, tol=0.5)
        eq(f"767 {name} hero media is capped", fn(767)["heroMedia"]["w"], 570, tol=0.5)
        m, inn = fn(767)["heroMedia"], fn(767)["heroInner"]
        ok_if(f"767 {name} hero media is centred in its column",
              abs((m["x"] - inn["x"]) - ((inn["x"] + inn["w"]) - (m["x"] + m["w"]))) < 1.0,
              f"left {m['x'] - inn['x']:.1f} vs right {(inn['x']+inn['w'])-(m['x']+m['w']):.1f}")
        eq(f"1440 {name} hero media untouched (no cap above 767)", fn(1440)["heroMediaMax"], "none")

    # ===== 第 2 条 expert rail centred on the phone =======================
    for w in (390, 575, 767):
        r = rail[w]
        ok_if(f"{w} rail: a card rests on the centre line", not r.get("err"), str(r))
        if r.get("err"):
            continue
        # 第五十轮：原生 scroller 与克隆式循环都换成了 Swiper（PROJECT-STATUS 待决 AG）。
        # 「居中 + 两侧露边」是需求方定的观感，留着；机制那两条换成 Swiper 的等价物。
        eq(f"{w} rail is driven by Swiper", r["swiperLive"], True)
        eq(f"{w} rail still ships exactly the three cards", r["n"], 3)
        eq(f"{w} rail: resting card is centred", r["offCentre"], 0, tol=2.0)
        ok_if(f"{w} rail: the previous card peeks", r["leftPeek"] > 4, f"{r['leftPeek']}px")
        ok_if(f"{w} rail: the next card peeks", r["rightPeek"] > 4, f"{r['rightPeek']}px")
        ok_if(f"{w} rail: the two peeks are equal",
              abs(r["leftPeek"] - r["rightPeek"]) < 3.0,
              f"L {r['leftPeek']} / R {r['rightPeek']}")
    # 768-991 keeps start alignment — the brief said 手机端 only
    r9 = rail[900]
    ok_if("900 rail is still start-aligned (not centred)",
          r9.get("err") or abs(r9["offCentre"]) > 4.0, str(r9))

    # ===== 第 3 条 app-section--lg padding-top 52 =========================
    def px(v):
        return float(v[:-2]) if v and v.endswith("px") else None
    eq("390 reviews app-section--lg padding-top", V(390)["appLg"][0], "52px")
    eq("767 reviews app-section--lg padding-top", V(767)["appLg"][0], "52px")
    eq("1440 reviews app-section--lg padding-top untouched", V(1440)["appLg"][0], "96px")
    # the ramp meets the phone value at 768 — no seam
    ok_if("768 app-section--lg padding-top meets 52 (no 767/768 step)",
          abs(px(V(768)["appLg"][0]) - 52) < 0.7, str(V(768)["appLg"][0]))
    # pdp's plain .gb-app-section must NOT have picked it up
    eq("390 pdp plain app-section keeps 64", P(390)["appBase"], "64px")

    # ===== 第 4 条 padding-bottom 46 on the plain tiles only ==============
    for name, fn in (("how-gumi-works", H), ("reviews", V), ("our-story", O)):
        d = fn(390)
        eq(f"390 {name}: .gb-product is the plain one", d["prodMod"], "plain")
        want = 46 + px(d["scH"])
        ok_if(f"390 {name}: product padding-bottom is 46 + wave",
              abs(px(d["prodPadB"]) - want) < 0.7, f"{d['prodPadB']} want {want}px")
        ok_if(f"768 {name}: the ramp meets 46 (no seam)",
              abs(px(fn(768)["prodPadB"]) - (46 + px(fn(768)["scH"]))) < 1.0,
              str(fn(768)["prodPadB"]))
    # ...and did NOT leak into --lg / --page
    d = I(390)
    eq("390 index: .gb-product--lg", d["prodMod"], "lg")
    ok_if("390 index --lg keeps 50 + wave",
          abs(px(d["prodPadB"]) - (50 + px(d["scLgH"]))) < 0.7, str(d["prodPadB"]))
    d = P(390)
    eq("390 pdp: .gb-product--page", d["prodMod"], "page")
    ok_if("390 pdp --page keeps 64 + wave",
          abs(px(d["prodPadB"]) - (64 + px(d["scLgH"]))) < 0.7, str(d["prodPadB"]))
    # desktop untouched
    ok_if("1440 how-gumi-works product padding-bottom untouched (96 + wave)",
          abs(px(H(1440)["prodPadB"]) - (96 + px(H(1440)["scH"]))) < 0.7, str(H(1440)["prodPadB"]))

    # ----- 第 4 条 promo-art top -4% --------------------------------------
    # r51 scoped this to .gb-promo-card--white and put THAT one back to -8%.
    # The two .gb-ingredients__disc pages still read -4%; keeping them in the
    # same block is what proves the scope holds.
    for name, fn, pct in (("science", S, 0.04), ("reviews", V, 0.04), ("pdp", P, 0.08)):
        d = fn(390)
        if d["promoTop"] is None:
            continue
        ok_if(f"390 {name}: promo-art img top is -{pct * 100:.0f}% of its box",
              abs(float(d["promoTop"][:-2]) + pct * d["promoParentH"]) < 1.0,
              f"{d['promoTop']} against a {d['promoParentH']}px box")
    d = S(1440)
    ok_if("1440 promo-art img top is still -5%",
          abs(float(d["promoTop"][:-2]) + 0.05 * d["promoParentH"]) < 1.0, str(d["promoTop"]))

    # ===== 第 5 条 dosed stacks at 767, columns shrink ====================
    for w in (1440, 1281, 1280, 1100, 1024, 992, 900, 768):
        eq(f"{w} dosed is a row", H(w)["dosedDir"], "row")
    for w in (767, 575, 390):
        eq(f"{w} dosed has stacked", H(w)["dosedDir"], "column-reverse")
    for w in (1440, 1281, 1280, 1100, 1024, 992, 900, 768, 767, 575, 390):
        eq(f"{w} how-gumi-works: no horizontal overflow", H(w)["overflowX"], 0)
    # the real regression guard: a rigid 598 starved the copy at 1100 (body 258)
    for w in (1280, 1100, 1024, 992, 900, 768):
        d = H(w)
        ok_if(f"{w} dosed: both columns are real",
              d["dosedMedia"]["w"] > 200 and d["dosedText"]["w"] > 200,
              f"media {d['dosedMedia']['w']} / text {d['dosedText']['w']}")
        ok_if(f"{w} dosed media is still square",
              abs(d["dosedMedia"]["w"] - d["dosedMedia"]["h"]) < 1.5,
              f"{d['dosedMedia']['w']} x {d['dosedMedia']['h']}")
    eq("1440 dosed media is the board's 598", H(1440)["dosedMedia"]["w"], 598, tol=0.5)
    for w in (767, 575, 390):
        eq(f"{w} dosed body has no cap", H(w)["dosedBodyMax"], "none")
        ok_if(f"{w} dosed body runs the full column",
              abs(H(w)["dosedBody"]["w"] - (w - 40)) < 1.0, f'{H(w)["dosedBody"]["w"]}')

    # ===== 第 6 条 product: cap off the inner, onto the media =============
    for w in (767, 390):
        for name, fn in (("pdp", P), ("index", I), ("reviews", V)):
            d = fn(w)
            # the base rule keeps its 995 (it never binds this narrow); what had
            # to go is the 560 override, so judge the box, not the property
            ok_if(f"{w} {name}: product inner is not capped at 560",
                  d["prodInnerMax"] != "560px", str(d["prodInnerMax"]))
            ok_if(f"{w} {name}: product inner runs the full viewport",
                  abs(d["prodInner"]["w"] - w) < 1.0, f"{d['prodInner']['w']} in {w}")
            eq(f"{w} {name}: product media capped 520", min(d["prodMedia"]["w"], 520.0),
               min(w - 40, 520), tol=0.5)
            ok_if(f"{w} {name}: info column runs the full width",
                  abs(d["prodInfo"]["w"] - (w - 40)) < 1.0,
                  f"info {d['prodInfo']['w']} in a {w - 40} box")
    d = P(767)
    ok_if("767 pdp: media is centred under the freed info column",
          abs((d["prodMedia"]["x"] - d["prodInner"]["x"] - 20)
              - ((d["prodInner"]["x"] + d["prodInner"]["w"] - 20)
                 - (d["prodMedia"]["x"] + d["prodMedia"]["w"]))) < 1.0,
          f"media x {d['prodMedia']['x']} w {d['prodMedia']['w']}")
    eq("1440 pdp media untouched", P(1440)["prodMedia"]["w"], 465, tol=0.5)

    # ===== 第 7 条 coral lead gone ========================================
    for w in (1440, 767, 390):
        ok_if(f"{w} the coral-mobile class is out of the markup", not H(w)["coralInDom"])
    eq("390 how-gumi-works lead is not coral", H(390)["leadColor"], H(390)["leadColor"])
    ok_if("390 how-gumi-works lead is not the coral",
          "255, 107" not in (H(390)["leadColor"] or ""), str(H(390)["leadColor"]))

    # ===== 第 8/9 条 gutter to the inner, squares capped 520 =============
    for w in (767, 575, 390):
        eq(f"{w} ingredients disc capped 520", S(w)["discMax"], "520px")
        eq(f"{w} faq-image media capped 520", S(w)["fqMediaMax"], "520px")
        # the square: min(version width, 520) — 390 goes back to the 350 it was
        # before r42 dropped the cap, 767 stops at 520 instead of running 767.
        eq(f"{w} ingredients disc width", S(w)["disc"]["w"], min(w - 40, 520), tol=0.5)
        eq(f"{w} faq-image media width", S(w)["fqMedia"]["w"], min(w - 40, 520), tol=0.5)
        eq(f"{w} ingredients disc is still square", S(w)["disc"]["w"], S(w)["disc"]["h"], tol=1.0)
        # the copy keeps its 20px inset even though the body's own padding is gone
        ok_if(f"{w} ingredients copy still starts 20 in",
              abs(S(w)["ingBody"]["x"] - 20) < 0.6, f"x={S(w)['ingBody']['x']}")
        ok_if(f"{w} faq-image copy still starts 20 in",
              abs(S(w)["fqBody"]["x"] - 20) < 0.6, f"x={S(w)['fqBody']['x']}")
        # ...and runs the full version width, not 40 short of it
        ok_if(f"{w} ingredients copy runs the full version",
              abs(S(w)["ingBody"]["w"] - (w - 40)) < 0.6, f"w={S(w)['ingBody']['w']}")
        ok_if(f"{w} faq-image copy runs the full version",
              abs(S(w)["fqBody"]["w"] - (w - 40)) < 0.6, f"w={S(w)['fqBody']['w']}")
    # desktop untouched
    eq("1440 ingredients disc untouched", S(1440)["disc"]["w"], 520, tol=0.5)
    eq("1440 faq-image media untouched", S(1440)["fqMedia"]["w"], 520, tol=0.5)

    print("=" * 72)
    if FAILS:
        print(f"FAIL — {len(FAILS)}")
        for f in FAILS:
            print("  ✗", f)
    else:
        print("r44: all assertions pass")
    print("=" * 72)
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
