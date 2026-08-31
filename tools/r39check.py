#!/usr/bin/env python3
"""Round-39 assertions — the eight items in 修改任务文档.txt.

    python3 tools/r39check.py

Geometry and computed style on index.html (stats / logo strip / nutrition cards
/ footer) and our-story.html (the four-card testimonial row), at every tier the
round touches: 390 narrow, 768 + 1024 + 1280 tablet, 1440 desktop.

Three items reverse an earlier decision, so each carries a matching "desktop
untouched" assertion — the client asked for mobile and tablet only.
"""
import asyncio, os, sys
from playwright.async_api import async_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXE = "/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome"
SETTLE = """.wowo,.gb-float-art,[data-line-reveal],.gb-line-mask__inner,.gb-ink-halo{
opacity:1!important;transform:none!important;animation:none!important;}"""

PROBE = r"""() => {
  const q  = s => document.querySelector(s);
  const qa = s => [...document.querySelectorAll(s)];
  const cs = (s, p) => { const e = q(s); return e ? getComputedStyle(e)[p] : 'NO-ELEMENT'; };
  const R  = e => { const r = e.getBoundingClientRect();
    return {x:+r.x.toFixed(2), y:+r.y.toFixed(2), w:+r.width.toFixed(2), h:+r.height.toFixed(2)}; };
  const rect = s => { const e = q(s); return e ? R(e) : null; };
  const rects = s => qa(s).map(R);
  const o = {};

  // --- 1 stats arrows -----------------------------------------------------
  o.arrowDisplay = cs('.gb-stats__arrow--1', 'display');
  o.arrowStroke  = cs('.gb-stats__arrow--1 path', 'strokeWidth');
  o.bearSlot     = rect('.gb-stats__bear');
  o.arrowRects   = rects('.gb-stats__arrow');
  o.gridH        = rect('.gb-stats__grid') ? rect('.gb-stats__grid').h : null;

  // --- 6 stats bear / fibre ----------------------------------------------
  o.bearMargin   = [cs('.gb-stats__bear','marginTop'), cs('.gb-stats__bear','marginBottom')];
  { const e = q('.gb-stats__bear-img');
    o.bearImgLeftPct = e ? +(parseFloat(getComputedStyle(e).left)
                             / e.offsetParent.clientWidth * 100).toFixed(2) : null; }
  o.fibreMarginTop = cs('.gb-stat--fibre', 'marginTop');

  // --- 5 logo strip -------------------------------------------------------
  o.logoImgBox   = [cs('.gb-logo-scroll__img','width'), cs('.gb-logo-scroll__img','height'),
                    cs('.gb-logo-scroll__img','objectFit')];
  { // widest ink must stay inside its slot, and no two logos may overlap
    const items = qa('.gb-logo-scroll__item'), imgs = qa('.gb-logo-scroll__img');
    o.logoOverflow = imgs.length && items.length
      ? +Math.max(...imgs.map((im, i) => im.getBoundingClientRect().width
                                       - items[i].getBoundingClientRect().width)).toFixed(2)
      : null;
    let worst = -1e9;
    for (let i = 1; i < imgs.length; i++) {
      const a = imgs[i-1].getBoundingClientRect(), b = imgs[i].getBoundingClientRect();
      worst = Math.max(worst, a.right - b.left);       // > 0 means they overlap
    }
    o.logoWorstOverlap = imgs.length > 1 ? +worst.toFixed(2) : null;
  }

  // --- 2 nutrition cards --------------------------------------------------
  { const box = q('.gb-nutrition__cards');
    if (box) {
      const b = box.getBoundingClientRect(), pad = getComputedStyle(box);
      const inner = {left: b.left + parseFloat(pad.paddingLeft),
                     right: b.right - parseFloat(pad.paddingRight)};
      o.nutriInnerW = +(inner.right - inner.left).toFixed(2);
      o.nutriInnerCentre = +((inner.left + inner.right) / 2).toFixed(2);
      o.nutriCards = rects('.gb-nutrition__cards > *');
      o.nutriGap = getComputedStyle(box).columnGap;
    }
  }

  // --- 3 testimonials -----------------------------------------------------
  { const box = q('.gb-testimonials');
    if (box) {
      const b = box.getBoundingClientRect(), st = getComputedStyle(box);
      o.testiInnerW = +(b.width - parseFloat(st.paddingLeft) - parseFloat(st.paddingRight)).toFixed(2);
      o.testiCentre = +(b.left + b.width / 2).toFixed(2);
      o.testiGap = st.columnGap;
      o.testiCards = rects('.gb-testimonial');
    }
  }

  // --- 4 footer link groups ----------------------------------------------
  o.linkGroupsJustify = cs('.gb-footer__link-groups', 'justifyContent');
  o.linkGroupsRect    = rect('.gb-footer__link-groups');
  { const e = q('.gb-footer__inner');
    if (e) { const r = R(e), st = getComputedStyle(e);
      o.footerInnerContentRight = +(r.x + r.w - parseFloat(st.paddingRight)).toFixed(2);
      o.footerInnerContentLeft  = +(r.x + parseFloat(st.paddingLeft)).toFixed(2); } }

  // --- 7 footer CTA / footer / deco bear ---------------------------------
  o.ctaPad       = [cs('.gb-footer-cta','paddingTop'), cs('.gb-footer-cta','paddingBottom')];
  o.ctaTitleMB   = cs('.gb-footer-cta__title', 'marginBottom');
  o.footerPad    = [cs('.gb-footer','paddingTop'), cs('.gb-footer','paddingBottom')];
  o.decoBTop     = cs('.gb-deco-bear--b', 'top');
  o.decoBRight   = cs('.gb-deco-bear--b', 'right');
  { const e = q('.gb-deco-bear--b');
    o.decoBRightPct = e ? +(parseFloat(getComputedStyle(e).right)
                            / e.offsetParent.clientWidth * 100).toFixed(2) : null; }

  // --- 8 footer internals -------------------------------------------------
  o.middleGap      = cs('.gb-footer__middle', 'rowGap');
  o.newsletterMT   = cs('.gb-footer__newsletter', 'marginTop');
  o.linkGroupGap   = cs('.gb-footer__link-group', 'rowGap');
  o.socialMT       = cs('.gb-footer__social', 'marginTop');
  o.bottomMT       = cs('.gb-footer__bottom', 'marginTop');
  o.innerGap       = cs('.gb-footer__inner', 'rowGap');
  { // the rendered gaps between the board's five stacked Containers
    const brand = rect('.gb-footer__brand'), news = rect('.gb-footer__newsletter'),
          links = rect('.gb-footer__link-groups'), social = rect('.gb-footer__social'),
          bottom = rect('.gb-footer__bottom');
    const gap = (a, b) => (a && b) ? +(b.y - (a.y + a.h)).toFixed(2) : null;
    o.stackGaps = [gap(brand, news), gap(news, links), gap(links, social), gap(social, bottom)];
  }

  // --- 9 conditional <br>: hidden, the two words must not run together ------
  { const hosts = new Set();
    document.querySelectorAll('.gb-br-narrow, .gb-br-wide').forEach(br => {
      const h = br.closest('p,h1,h2,h3,h4,li,th,td,span,div');
      if (h) hosts.add(h.innerText.replace(/\s+/g, ' ').trim()); });
    o.brHosts = [...hosts]; }

  o.overflowX = document.documentElement.scrollWidth - document.documentElement.clientWidth;
  return o;
}"""

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


async def main():
    # 1200 joined the plan in r51: it is the new top of the two-up tier (the
    # 3→2 step moved down from 1280). 1280 stays — other sections still read it.
    plan = {"index.html": (390, 768, 1024, 1200, 1280, 1440),
            "our-story.html": (390, 768, 1024, 1440)}
    data = {}
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path=EXE)
        for page, widths in plan.items():
            for w in widths:
                pg = await b.new_page(viewport={"width": w, "height": 1000})
                await pg.goto("file://" + os.path.join(ROOT, page))
                await pg.add_style_tag(content=SETTLE)
                await pg.evaluate("async()=>{for(let y=0;y<document.body.scrollHeight;y+=700){"
                                  "window.scrollTo(0,y);await new Promise(r=>requestAnimationFrame(r));}"
                                  "window.scrollTo(0,0);}")
                await pg.wait_for_timeout(700)
                data[(page, w)] = await pg.evaluate(PROBE)
                await pg.close()
        await b.close()

    I = lambda w: data[("index.html", w)]
    O = lambda w: data[("our-story.html", w)]

    # ===== 1. arrows show from 1024 down (was: hidden 768-1024) =============
    for w in (390, 768, 1024):
        eq(f"{w} .gb-stats__arrow visible", I(w)["arrowDisplay"], "block")
        eq(f"{w} arrow stroke is the mobile 2.2998 (243:28620 OUTSIDE 1.1499)",
           I(w)["arrowStroke"], "2.2998px")
    eq("1440 arrows still visible", I(1440)["arrowDisplay"], "block")
    # the mobile geometry is anchored on the bear slot, so the slot has to be
    # the same 208 x 257.42 box across the whole stack tier for it to transfer
    for w in (390, 768, 1024):
        s = I(w)["bearSlot"]
        eq(f"{w} bear slot width 208 (332:16221)", s["w"], 208, tol=0.5)
        eq(f"{w} bear slot height 257.42", s["h"], 257.42, tol=0.5)
        # every arrow must sit within a bear-slot-sized halo of the slot, i.e.
        # it hangs off the bear rather than drifting into the next grid row
        for i, a in enumerate(I(w)["arrowRects"], 1):
            dx = (a["x"] + a["w"] / 2) - (s["x"] + s["w"] / 2)
            dy = (a["y"] + a["h"] / 2) - (s["y"] + s["h"] / 2)
            ok_if(f"{w} arrow--{i} stays on the bear", abs(dx) < 160 and abs(dy) < 210,
                  f"centre offset ({dx:.0f}, {dy:.0f}) from the slot centre")

    # ===== 6. bear slot margins / mirror offset / fibre =====================
    for w in (390, 768, 1024):
        eq(f"{w} bear slot margins (client-set 78/48)", I(w)["bearMargin"], ["78px", "48px"])
    eq("390 .gb-stats__bear-img left (client-set -39.2%)", I(390)["bearImgLeftPct"], -39.2, tol=0.15)
    eq("1440 .gb-stats__bear-img left untouched", I(1440)["bearImgLeftPct"], -46.2, tol=0.15)
    eq("390 .gb-stat--fibre margin-top (client-set)", I(390)["fibreMarginTop"], "24px")
    eq("1440 .gb-stat--fibre margin-top untouched", I(1440)["fibreMarginTop"], "0px")
    # board Benefits 243:28608 is 845.34 tall; 78+48 is 2 tighter than 65+63
    eq("390 .gb-stats__grid height vs board 845.34", I(390)["gridH"], 843.4, tol=2)

    # ===== 5. logo strip: one slot-sized box, nothing overlapping ===========
    eq("390 .gb-logo-scroll__img box", I(390)["logoImgBox"], ["106px", "44px", "contain"])
    eq("1440 .gb-logo-scroll__img untouched (per-logo ink height, width follows)",
       [I(1440)["logoImgBox"][1], I(1440)["logoImgBox"][2]], ["34px", "fill"])   # first img is --abc, design ink 166x34
    ok_if("390 no logo overruns its slot", I(390)["logoOverflow"] <= 0.5,
          f"widest overruns by {I(390)['logoOverflow']}px")
    ok_if("390 no two logos overlap", I(390)["logoWorstOverlap"] < 0,
          f"closest pair overlaps by {I(390)['logoWorstOverlap']}px")

    # ===== 2. nutrition cards: lone last card centred on the two-up tier ====
    # r51 moved the 3→2 step from 1280 down to 1200 (client-set), so 1280 is a
    # three-up row now and 1200 is the top of the two-up tier. Three-up geometry
    # is judged in r52check §1.
    for w in (768, 1024, 1200):
        d = I(w)
        cards, gap = d["nutriCards"], float(d["nutriGap"][:-2])
        eq(f"{w} nutrition is two-up", len(cards), 3)
        want = (d["nutriInnerW"] - gap) / 2
        for i, c in enumerate(cards, 1):
            eq(f"{w} nutrition card {i} width == (row - gap) / 2", c["w"], want, tol=0.6)
        eq(f"{w} lone third card is centred", cards[2]["x"] + cards[2]["w"] / 2,
           d["nutriInnerCentre"], tol=0.6)
        eq(f"{w} first two cards share a row", cards[0]["y"], cards[1]["y"], tol=0.5)
        ok_if(f"{w} third card is on its own row", cards[2]["y"] > cards[0]["y"] + 10)
    # desktop stays three across, mobile one
    d = I(1440)
    eq("1440 nutrition three across", len({c["y"] for c in d["nutriCards"]}), 1)
    eq("1440 third card NOT centred (it is the third column)",
       d["nutriCards"][2]["x"] + d["nutriCards"][2]["w"] / 2 > d["nutriInnerCentre"] + 100, True)
    eq("390 nutrition one per row", len({c["y"] for c in I(390)["nutriCards"]}), 3)

    # ===== 3. testimonials 3 -> 2 -> 1 ======================================
    # index ships three, our-story four
    d = I(1440)
    eq("1440 index three testimonials on one row", len({c["y"] for c in d["testiCards"]}), 1)
    for i, c in enumerate(d["testiCards"], 1):
        eq(f"1440 index testimonial {i} width (board 411)", c["w"], 411, tol=0.5)
    o = O(1440)
    eq("1440 our-story four testimonials on TWO rows (board row is 3 x 411)",
       len({round(c["y"]) for c in o["testiCards"]}), 2)
    rows = {}
    for c in o["testiCards"]:
        rows.setdefault(round(c["y"]), []).append(c)
    first, second = [rows[k] for k in sorted(rows)]
    eq("1440 first row holds three", len(first), 3)
    eq("1440 second row holds one", len(second), 1)
    eq("1440 the lone fourth card is centred",
       second[0]["x"] + second[0]["w"] / 2, o["testiCentre"], tol=1.0)
    for w in (768, 1024):
        o = O(w)
        eq(f"{w} our-story testimonials two-up", len({round(c["y"]) for c in o["testiCards"]}), 2)
        # 411 is the board's card width and stays a max-width, so the two-up
        # row uses the narrower of the two and centres what is left over
        want = min(411.0, (o["testiInnerW"] - float(o["testiGap"][:-2])) / 2)
        for i, c in enumerate(o["testiCards"], 1):
            eq(f"{w} testimonial {i} width == min(411, (row - gap) / 2)", c["w"], want, tol=0.8)
        d2 = I(w)
        eq(f"{w} index (three cards) is 2 + 1", len({round(c["y"]) for c in d2["testiCards"]}), 2)
    eq("390 testimonials one per row", len({round(c["y"]) for c in O(390)["testiCards"]}), 4)

    # ===== 4. footer link groups: flex-start below 1281 =====================
    # r42 reversed this round's reversal, which had itself removed the r20-era
    # flex-start override. Desktop still hangs off the right; everything below
    # 1281 hugs the left. Assertions flipped rather than deleted, so the history
    # stays visible here.
    for w in (768, 1024, 1280):
        eq(f"{w} .gb-footer__link-groups justify", I(w)["linkGroupsJustify"], "flex-start")
    eq("1440 .gb-footer__link-groups justify", I(1440)["linkGroupsJustify"], "flex-end")
    # and it really does sit against the left edge of the inner container.
    # 1024 is deliberately not in this list: .gb-footer__middle has not wrapped
    # there yet, so the block is the second item of a row and its box does not
    # start at the content edge. r42check covers that tier box-relative.
    for w in (768,):
        lg = I(w)["linkGroupsRect"]
        eq(f"{w} link groups flush with the left content edge",
           lg["x"], I(w)["footerInnerContentLeft"], tol=2.5)
    lg = I(1440)["linkGroupsRect"]
    eq("1440 link groups still flush with the right content edge",
       lg["x"] + lg["w"], I(1440)["footerInnerContentRight"], tol=2.5)

    # ===== 7. CTA / footer padding, deco bear ==============================
    # board I236:12187;236:11720 is 64/64; 52 = 64 - the 12 the scallop overshoots
    eq("390 .gb-footer-cta padding", I(390)["ctaPad"], ["52px", "78px"])
    eq("1440 .gb-footer-cta padding untouched", I(1440)["ctaPad"], ["96px", "96px"])
    ok_if("767/768 CTA padding continuous",
          abs(float(I(768)["ctaPad"][0][:-2]) - 52) < 0.6
          and abs(float(I(768)["ctaPad"][1][:-2]) - 78) < 0.6,
          f"768 reads {I(768)['ctaPad']}")
    eq("390 .gb-footer-cta__title margin-bottom (236:11722 itemSpacing 32)",
       I(390)["ctaTitleMB"], "32px")
    eq("1440 .gb-footer-cta__title margin-bottom untouched", I(1440)["ctaTitleMB"], "23px")
    eq("390 .gb-footer padding", I(390)["footerPad"], ["52px", "24px"])
    eq("1440 .gb-footer padding untouched (187:3984 64/48)", I(1440)["footerPad"], ["64px", "48px"])
    # r53: same reason as the 1440 assertion below -- top is a percentage now.
    eq("390 .gb-deco-bear--b top (client-set 457)",
       float(I(390)["decoBTop"][:-2]), 457.0, tol=0.6)
    eq("390 .gb-deco-bear--b right as a % (28/390)", I(390)["decoBRightPct"], 7.18, tol=0.15)
    # r53: client-set, top became a percentage of .gb-footer-cta-wrap. The bear
    # must still land where it did on the board, but a resolved percentage never
    # reads back as the string "408px" -- compare the number, not the text.
    eq("1440 .gb-deco-bear--b lands at the board's 408",
       float(I(1440)["decoBTop"][:-2]), 408.0, tol=0.6)

    # ===== 8. footer internals: every stacked gap reads the board's 48 ======
    eq("390 .gb-footer__middle gap (187:3984 itemSpacing 48)", I(390)["middleGap"], "48px")
    eq("390 .gb-footer__newsletter margin-top", I(390)["newsletterMT"], "16px")
    eq("390 .gb-footer__link-group gap (187:4014 itemSpacing 12)", I(390)["linkGroupGap"], "12px")
    eq("390 .gb-footer__social margin-top", I(390)["socialMT"], "16px")
    eq("390 .gb-footer__bottom margin-top", I(390)["bottomMT"], "16px")
    for i, g in enumerate(I(390)["stackGaps"], 1):
        eq(f"390 footer stacked gap {i} == board 48", g, 48, tol=0.5)
    # the same four gaps must still read 48 where inner's own gap carries them
    for w in (1280, 1440):
        for i, g in enumerate(I(w)["stackGaps"][2:], 3):   # 1-2 are inside the wrapping row
            eq(f"{w} footer stacked gap {i} == 48", g, 48, tol=0.5)
    eq("1440 .gb-footer__link-group gap untouched", I(1440)["linkGroupGap"], "16px")
    eq("1440 .gb-footer__social margin-top untouched", I(1440)["socialMT"], "0px")

    # ===== 9. conditional <br> must leave a space behind when it is hidden ===
    # r37 added 18 hard breaks as `word<br class="gb-br-narrow">word`; above 767
    # the br is display:none and the two words render joined ("than avitamin").
    # A space before the br collapses at the end of a wrapped line on narrow and
    # separates the words everywhere else.
    # Checked on the SOURCE, not on innerText: "avitamin" and "Greenbenefits"
    # are ordinary lowercase runs that no rendered-text heuristic can separate
    # from a real word, whereas the markup says exactly what is on each side.
    import glob as _glob, re as _re
    JOIN = _re.compile(r'(\w)(<br class="gb-br-(?:narrow|wide)">)(\w)')
    joined = []
    for f in sorted(_glob.glob(os.path.join(ROOT, "*.html"))):
        src = open(f, encoding="utf-8").read()
        for m in JOIN.finditer(src):
            joined.append(f"{os.path.basename(f)}: …{src[max(0,m.start()-28):m.end()+12]}…")
    ok_if("no conditional <br> sits between two word characters",
          not joined, f"{len(joined)} left, e.g. {joined[0] if joined else ''}")
    # the breaks themselves must still render on narrow
    ok_if("390 conditional breaks still present", len(I(390)["brHosts"]) > 0)

    # ===== guards ===========================================================
    for (page, w), d in data.items():
        eq(f"{page}@{w} no horizontal overflow", d["overflowX"], 0)

    total = len(FAILS)
    if total:
        print(f"r39 FAIL — {total} assertion(s)")
        for f in FAILS:
            print("  ✗", f)
        sys.exit(1)
    print("r39 OK — all assertions pass across 390 / 768 / 1024 / 1200 / 1280 / 1440")

asyncio.run(main())
