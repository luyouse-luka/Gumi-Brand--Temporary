#!/usr/bin/env python3
"""Round-42 assertions — footer link alignment, and the expert rail going endless.

    python3 tools/r42check.py

1. .gb-footer__link-groups goes back to flex-start below 1281. Third time this
   block has been flipped: it started as `@include stack { justify-content:
   flex-start }` (r20-era), r39 deleted that override so the wrapped row hung
   off the right edge all the way down to 1280, and r42 puts it back — this
   time on the tablet value tier, whose upper bound (1280) is the number the
   client actually named. Layout thresholds deliberately do NOT reach 1280
   (see PROJECT-STATUS "断点体系").

   computed justify-content alone is not a judge: it reads flex-start even where
   the row has no free space to distribute. So every width also carries a
   geometry assertion, and the ones with no slack are reported as vacuous rather
   than counted as passes.

2. .gb-expert__cards becomes the swipe rail at 991 instead of 767, and loops
   endlessly. Three things could only break here, so each has its own judge:
     - the rail is the only place clones belong. Above 991 the block is a
       three-column grid and cloning would lay the copies out as extra ROWS,
       so the card count is asserted on both sides of 991 and after a resize
       back up (the copies have to be removed again, not just not added).
     - the loop has to be usable in both directions from the first click, i.e.
       parked one set in rather than at scrollLeft 0.
     - clones must not inherit .wowo. wowo re-queries on scroll, so a copy that
       kept the class is not lost for good: it sits at opacity 0 until the next
       scroll, then fades in by itself, out of step with the originals. The
       judge therefore has to read opacity on a page that has NOT scrolled
       since the clones were made — a tall viewport puts the rail on screen
       without a scroll event, and SETTLE is left out because it would force
       .wowo to 1 and mask the very thing being measured.

3. The dashed .gb-app-slot placeholder is gone from reviews (pdp lost its own
   in r40). Anchored on the section still existing, so an empty document or a
   404 cannot pass it.
"""
import asyncio, os

from playwright.async_api import async_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXE = "/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome"
# Must cover the reveal group too, not just .wowo (memory kill-animations-blanks-reveal-blocks).
SETTLE = (".wowo,.gb-float-art,[data-line-reveal],.gb-line-mask__inner,.gb-ink-halo{"
          "opacity:1!important;transform:none!important;animation:none!important}")

PAGES = ("index.html", "faq.html")
WIDTHS = (1440, 1281, 1280, 1200, 1100, 1024, 992, 900, 768, 767, 390)

# the expert rail lives on reviews.html only
RAIL_WIDTHS = (1440, 1280, 1024, 992, 991, 900, 768, 767, 390)
GRID_TIERS = (1440, 1280, 1024, 992)
RAIL_TIERS = (991, 900, 768, 767, 390)

FAILS = []
VACUOUS = []


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
  const box = document.querySelector('.gb-footer__link-groups');
  if (!box) return null;
  const st = getComputedStyle(box);
  const b = box.getBoundingClientRect();
  const kids = [...box.children].map(e => {
    const r = e.getBoundingClientRect();
    return {x: +r.x.toFixed(2), right: +r.right.toFixed(2), w: +r.width.toFixed(2),
            y: +r.y.toFixed(2)};
  });
  const gap = parseFloat(st.columnGap) || 0;
  const used = kids.reduce((s, k) => s + k.w, 0) + gap * Math.max(0, kids.length - 1);
  // does this block sit on a row of its own? .gb-footer__middle wraps at some
  // point and only then can justify-content show up at all.
  const nl = document.querySelector('.gb-footer__newsletter');
  const ownRow = nl ? Math.abs(nl.getBoundingClientRect().y - b.y) > 2 : null;
  return {
    justify: st.justifyContent,
    display: st.display,
    gridCols: st.gridTemplateColumns,
    gap: +gap.toFixed(2),
    boxX: +b.x.toFixed(2),
    boxW: +b.width.toFixed(2),
    kids,
    rows: new Set(kids.map(k => Math.round(k.y))).size,
    free: +(b.width - used).toFixed(2),
    ownRow,
    marginRight: st.marginRight,
    overflowX: document.documentElement.scrollWidth - document.documentElement.clientWidth,
  };
}"""


RAIL = r"""() => {
  const q = s => document.querySelector(s);
  const track = q('.gb-expert__cards');
  if (!track) return null;
  // 第五十轮：轨道改跑 Swiper，三列网格随之下移到 .swiper-wrapper（卡片真正的
  // 父元素）。断言的意图没变，指向要跟着变；克隆机制整套没了，所以 clones 恒 0。
  const box = track.querySelector('.swiper-wrapper') || track;
  const st = getComputedStyle(box);
  const cards = [...box.children];
  const originals = cards;
  const clones = [];
  const tr = track.getBoundingClientRect();
  const gap = parseFloat(st.columnGap) || 0;
  const pitch = cards.length ? cards[0].getBoundingClientRect().width + gap : 0;
  const nav = q('.gb-expert__nav');
  return {
    display: st.display,
    cols: st.gridTemplateColumns,
    overflowX: getComputedStyle(track).overflowX,
    gap: +gap.toFixed(2),
    cards: cards.length,
    originals: originals.length,
    clones: clones.length,
    // a clone that kept .wowo would be stuck transparent
    cloneOpacity: clones.length ? [...new Set(clones.map(c =>
      getComputedStyle(c).opacity))] : [],
    originalOpacity: originals.length ? [...new Set(originals.map(c =>
      getComputedStyle(c).opacity))] : [],
    cloneKeptWowo: clones.filter(c => c.classList.contains('wowo')).length,
    cloneTabbable: clones.reduce((n, c) =>
      n + [...c.querySelectorAll('a,button,[tabindex]')].filter(e => e.tabIndex >= 0).length, 0),
    trackX: +tr.x.toFixed(2),
    trackW: +tr.width.toFixed(2),
    // content-box coordinate: viewport x would be wherever the loop has parked
    firstCardInner: cards.length
      ? +(cards[0].getBoundingClientRect().x - tr.x + track.scrollLeft).toFixed(2) : null,
    cardW: cards.length ? +cards[0].getBoundingClientRect().width.toFixed(2) : null,
    padLeft: +parseFloat(getComputedStyle(track).paddingLeft).toFixed(2),
    swiperLive: !!track.swiper,
    scrollLeft: +track.scrollLeft.toFixed(2),
    scrollW: track.scrollWidth,
    clientW: track.clientWidth,
    pitch: +pitch.toFixed(2),
    setW: +(pitch * originals.length).toFixed(2),
    navDisplay: nav ? getComputedStyle(nav).display : null,
    // the placeholder this round removed, with its anchor
    appSectionExists: !!q('.gb-app-section__inner'),
    appSlots: document.querySelectorAll('.gb-app-slot').length,
    productAppSlots: document.querySelectorAll('.gb-product__app-slot').length,
    pageOverflowX: document.documentElement.scrollWidth - document.documentElement.clientWidth,
  };
}"""


async def main():
    data = {}
    rail = {}
    resized = {}
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path=EXE)

        # --- the expert rail, reviews.html ---------------------------------
        for w in RAIL_WIDTHS:
            pg = await b.new_page(viewport={"width": w, "height": 1000})
            await pg.goto("file://" + os.path.join(ROOT, "reviews.html"))
            await pg.add_style_tag(content=SETTLE)
            await pg.evaluate("() => document.fonts.ready")
            await pg.wait_for_timeout(300)
            rail[w] = await pg.evaluate(RAIL)
            await pg.close()

        # crossing the threshold has to remove the clones again, not just stop
        # adding them -- a resize-up is the only way that failure shows
        for a, z in ((991, 1440), (900, 1024), (1440, 900)):
            pg = await b.new_page(viewport={"width": a, "height": 1000})
            await pg.goto("file://" + os.path.join(ROOT, "reviews.html"))
            await pg.add_style_tag(content=SETTLE)
            await pg.evaluate("() => document.fonts.ready")
            await pg.wait_for_timeout(300)
            await pg.set_viewport_size({"width": z, "height": 1000})
            await pg.wait_for_timeout(300)
            resized[(a, z)] = await pg.evaluate(RAIL)
            await pg.close()

        # Clone visibility, measured the only way that can tell the two
        # implementations apart: no SETTLE (it would force .wowo to 1) and no
        # scroll after the clones were made (a scroll makes wowo re-query and
        # reveal them anyway). A viewport tall enough to hold the rail gets it
        # on screen with neither.
        pg = await b.new_page(viewport={"width": 390, "height": 7000})
        await pg.goto("file://" + os.path.join(ROOT, "reviews.html"))
        await pg.evaluate("() => document.fonts.ready")
        await pg.wait_for_timeout(1800)      # wowo plays 0.7s, sheds class at 1500ms
        bare = await pg.evaluate(RAIL)
        await pg.close()

        for page in PAGES:
            for w in WIDTHS:
                pg = await b.new_page(viewport={"width": w, "height": 1000})
                await pg.goto("file://" + os.path.join(ROOT, page))
                await pg.add_style_tag(content=SETTLE)
                await pg.evaluate("() => document.fonts.ready")
                await pg.wait_for_timeout(250)
                data[(page, w)] = await pg.evaluate(PROBE)
                await pg.close()
        await b.close()

    for page in PAGES:
        for w in WIDTHS:
            d = data[(page, w)]
            tag = f"{w} {page}"
            ok_if(f"{tag}: found .gb-footer__link-groups", d is not None)
            if d is None:
                continue

            # ---- the declaration ------------------------------------------
            if w >= 1281:
                eq(f"{tag} desktop keeps flex-end", d["justify"], "flex-end")
                eq(f"{tag} desktop keeps the board's -2px overhang",
                   d["marginRight"], "-2px")
            elif w >= 768:
                eq(f"{tag} tablet band is flex-start", d["justify"], "flex-start")
                eq(f"{tag} tablet band keeps its fluid gap ramp", d["gap"],
                   32 - 8 * (w - 768) / 513, tol=0.05)
            else:
                eq(f"{tag} phone tier is still the two-track grid", d["display"], "grid")
                eq(f"{tag} phone tier keeps its 32 gap", d["gap"], 32, tol=0.05)

            # ---- the geometry ---------------------------------------------
            # justify-content only shows when the row has slack to hand out. On
            # the phone the grid's two 1fr tracks always consume it, which is
            # why narrow carries no override.
            if d["display"] == "grid":
                tracks = [float(t[:-2]) for t in d["gridCols"].split() if t.endswith("px")]
                eq(f"{tag} grid runs two tracks", len(tracks), 2)
                eq(f"{tag} the two 1fr tracks fill the box, leaving no free space",
                   sum(tracks) + d["gap"], d["boxW"], tol=1.0)
                eq(f"{tag} the three groups wrap onto two rows", d["rows"], 2)
                continue
            if d["free"] <= 1:
                VACUOUS.append(f"{tag}: no free space ({d['free']}px) — "
                               f"justify-content cannot show, assertion skipped")
                continue
            offset = d["kids"][0]["x"] - d["boxX"]
            slack = d["free"]
            if w >= 1281:
                eq(f"{tag} columns hug the right edge", offset, slack, tol=1.0)
            else:
                eq(f"{tag} columns hug the left edge", offset, 0, tol=1.0)
                ok_if(f"{tag} the ~{round(slack)}px hole moved to the right",
                      d["kids"][-1]["right"] < d["boxX"] + d["boxW"] - 1,
                      f"last column ends at {d['kids'][-1]['right']}, "
                      f"box ends at {round(d['boxX'] + d['boxW'], 2)}")

            # ---- nothing else moved ---------------------------------------
            eq(f"{tag} link columns stay on one row", d["rows"], 1)
            eq(f"{tag} no horizontal overflow", d["overflowX"], 0)

    # ===== 2. the expert rail ==============================================
    ok_if("found .gb-expert__cards on reviews.html", rail[1440] is not None)
    if rail[1440] is not None:
        SET = rail[1440]["originals"]
        eq("the board ships three expert cards", SET, 3)

        for w in GRID_TIERS:
            d, tag = rail[w], f"{w} reviews expert"
            eq(f"{tag} is still the three-column grid", d["display"], "grid")
            eq(f"{tag} runs 3 tracks", len(d["cols"].split()), 3)
            eq(f"{tag} nav is hidden", d["navDisplay"], "none")
            # 第五十轮换成 Swiper 之后，这里要防的是「Swiper 没被销毁」：
            # 它 loop 时会重排 slide，禁用而不销毁的话网格会照着重排后的顺序渲染。
            eq(f"{tag} Swiper is destroyed above the threshold", d["swiperLive"], False)
            eq(f"{tag} still exactly the three cards", d["cards"], SET)

        for w in RAIL_TIERS:
            d, tag = rail[w], f"{w} reviews expert"
            eq(f"{tag} is the swipe rail", d["display"], "flex")
            eq(f"{tag} Swiper is driving it", d["swiperLive"], True)
            eq(f"{tag} nav is shown", d["navDisplay"], "flex")
            eq(f"{tag} still exactly the three cards", d["cards"], SET)
            # 第五十轮：克隆式无限循环没了（Swiper 是重排现有 slide，见
            # PROJECT-STATUS 待决 AG），所以「克隆成整套 / 留够跑道 / 停在一套之内 /
            # 克隆不带 wowo、不进 tab 序」这六条随机制一起作废。
            # 轨道的几何判据搬去 tools/r50check.py 第 9 节，那边比的是
            # 间距 == CSS gap、步距 == 卡宽 + gap、两侧不许留空。
            eq(f"{tag} no clone was left behind", d["clones"], 0)
            # full bleed: the rail spans the viewport
            eq(f"{tag} rail is full-bleed to the viewport edge", d["trackX"], 0, tol=1.0)
            # 容器不再带 padding：Swiper 用 clientWidth（含 padding）量容器，
            # 带 padding 会让它以为地方比实际多，991 处整组左移 24、第三张被切。
            eq(f"{tag} the track carries no padding for Swiper to miscount",
               d["padLeft"], 0, tol=0.01)
            eq(f"{tag} card holds the board's 305", d["cardW"], 305, tol=0.5)
            eq(f"{tag} page has no horizontal overflow", d["pageOverflowX"], 0)

        # the threshold itself
        eq("992 is grid / 991 is rail — the switch is exactly at 991",
           (rail[992]["display"], rail[991]["display"]), ("grid", "flex"))

        # 原本这里验的是「克隆有没有继承 .wowo 而永久透明」。第五十轮克隆机制
        # 整套没了（Swiper 不复制 DOM），只留下入场本身的锚点。
        ok_if("bare page: the expert rail is present", bare is not None)
        if bare is not None:
            eq("bare page: the cards did play their entrance",
               bare["originalOpacity"], ["1"])
            eq("bare page: nothing was cloned", bare["clones"], 0)

        # resizing across the threshold cleans up after itself
        for (a, z), d in resized.items():
            tag = f"resize {a}->{z} reviews expert"
            if z > 991:
                eq(f"{tag} drops back to the grid", d["display"], "grid")
                eq(f"{tag} destroys the Swiper on the way up", d["swiperLive"], False)
                eq(f"{tag} still exactly the three cards", d["cards"], SET)
            else:
                eq(f"{tag} becomes the rail", d["display"], "flex")
                eq(f"{tag} rebuilds the Swiper on the way down", d["swiperLive"], True)

        # ===== 3. the dashed placeholder is gone ===========================
        ok_if("anchor: the review section is still on reviews.html",
              rail[1440]["appSectionExists"])
        eq("the dashed .gb-app-slot is gone from reviews", rail[1440]["appSlots"], 0)
        eq("the unrelated .gb-product__app-slot is untouched",
           rail[1440]["productAppSlots"], 1)

    print("=" * 72)
    for line in VACUOUS:
        print("  vacuous:", line)
    if VACUOUS:
        print("-" * 72)
    if FAILS:
        print(f"FAIL — {len(FAILS)}")
        for f in FAILS:
            print("  ✗", f)
    else:
        print("r42: all assertions pass")
    print("=" * 72)
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
