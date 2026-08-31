#!/usr/bin/env python3
"""Round-47 assertions — 修改任务文档.txt 第 14–19 条。

    python3 tools/r48check.py

判据取法与理由：

1. 第 15 条前半（cta-band 按钮 padding 加响应式）的判据是**标签占几行**，不是
   padding 等于某个数。病因是 __content 的 38 gutter 把按钮从板上的 350 压到 274，
   64 的内缩于是只剩 146 给一条 146.34 的标签 —— 差 0.34px 就折行。所以断言
   「墨迹宽 <= 可用宽」且行盒数 == 1，并在板上真出现过的最窄几档都验一遍。

2. 第 15 条后半（去掉 --lg）不能断言「class 不存在」—— 那既不解释病因也抓不住复发。
   真判据是**内容底到波浪顶的距离**：两组页头在同一档必须相等（1440 = 70、390 = 64），
   而两页的波浪仍是大瓦片、高度不同。padding 若被误统一成 --sc-h，波浪会顶到内容上，
   这条会立刻报红。

3. 第 19 条（shipping 表格）过去两轮只落在 narrow 档，768 处整张网格消失（auto 布局、
   无边框、无底色）。判据因此跨 390/767/768/1440 四档验同一组不变量，
   并锁死两张表在 350 板宽下的列宽 88/262 与 203/147。

4. 值档交接：每条改动都验 767 与 768 两侧，防的是只写 narrow 没配 tablet 斜坡。
"""
import asyncio
import json
import os

from playwright.async_api import async_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXE = "/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome"
SETTLE = (".wowo,.gb-float-art,[data-line-reveal],.gb-line-mask__inner,.gb-ink-halo{"
          "opacity:1!important;transform:none!important;animation:none!important}")

FAILS = []
CHECKS = [0]


def eq(label, got, want, tol=None):
    CHECKS[0] += 1
    try:
        ok = (abs(float(got) - float(want)) <= tol) if tol is not None else (got == want)
    except (TypeError, ValueError):
        ok = False
    if not ok:
        FAILS.append(f"{label}: got {got!r}, want {want!r}" + (f" (±{tol})" if tol else ""))


def ok_if(label, cond, detail=""):
    CHECKS[0] += 1
    if not cond:
        FAILS.append(f"{label}{(': ' + detail) if detail else ''}")


ACC = r"""() => {
  const e = document.querySelector('.gb-acc-body__text');
  if (!e) return null;                       // anchor guard: no element, no verdict
  const cs = getComputedStyle(e);
  return {fs: parseFloat(cs.fontSize), lh: parseFloat(cs.lineHeight),
          ls: parseFloat(cs.letterSpacing)};
}"""

FAQPLAIN = r"""() => {
  const e = document.querySelector('.gb-faq--plain');
  if (!e) return null;
  const cs = getComputedStyle(e);
  return {pt: parseFloat(cs.paddingTop), pb: parseFloat(cs.paddingBottom)};
}"""

BTN = r"""() => {
  const b = document.querySelector('.gb-cta-band__btn');
  if (!b) return null;
  const r = b.getBoundingClientRect(), cs = getComputedStyle(b);
  const rng = document.createRange(); rng.selectNodeContents(b);
  const t = rng.getBoundingClientRect();
  return {w: +r.width.toFixed(2),
          avail: +(r.width - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight)).toFixed(2),
          inkW: +t.width.toFixed(2),
          lines: Math.round(t.height / parseFloat(cs.lineHeight))};
}"""

HERO = r"""() => {
  const s = document.querySelector('.gb-page-hero');
  if (!s) return null;
  const sr = s.getBoundingClientRect();
  const inner = s.querySelector('.gb-page-hero__inner');
  const sc = s.querySelector('.gb-scallop');
  if (!inner || !sc) return null;
  const ir = inner.getBoundingClientRect(), cr = sc.getBoundingClientRect();
  return {gap: +(cr.top - ir.bottom).toFixed(2),
          waveH: +cr.height.toFixed(2),
          lgWave: sc.className.includes('gb-scallop--lg'),
          slack: +(sr.bottom - cr.bottom).toFixed(2)};
}"""

FORM = r"""() => {
  const s = document.querySelector('.gb-form-section');
  const d = document.querySelector('.gb-form__disclaimer');
  if (!s || !d) return null;
  const scs = getComputedStyle(s), dcs = getComputedStyle(d);
  return {pb: parseFloat(scs.paddingBottom), pt: parseFloat(scs.paddingTop),
          mt: parseFloat(dcs.marginTop), mb: parseFloat(dcs.marginBottom)};
}"""

SECTION = r"""() => {
  const s = document.querySelector('.gb-form-section');
  if (!s) return null;
  return {pb: parseFloat(getComputedStyle(s).paddingBottom)};
}"""

RICH = r"""() => {
  const p = document.querySelector('.gb-rich-text p');
  if (!p) return null;
  return {mb: parseFloat(getComputedStyle(p).marginBottom)};
}"""

TABLE = r"""() => {
  const ts = [...document.querySelectorAll('.gb-rich-table')];
  if (ts.length !== 2) return null;
  return ts.map(t => {
    const cs = getComputedStyle(t);
    const head = [...t.querySelectorAll('thead th')];
    const rows = [...t.querySelectorAll('tbody tr')];
    const cell = t.querySelector('tbody td');
    const ccs = getComputedStyle(cell);
    return {
      w: +t.getBoundingClientRect().width.toFixed(2),
      layout: cs.tableLayout,
      cols: head.map(h => +h.getBoundingClientRect().width.toFixed(2)),
      headBg: getComputedStyle(head[0]).backgroundColor,
      headRowH: +head[0].getBoundingClientRect().height.toFixed(2),
      rowH: +rows[0].getBoundingClientRect().height.toFixed(2),
      pad: ccs.padding,
      border: ccs.borderTopWidth + ' ' + ccs.borderTopStyle,
      zebra: rows.map(r => getComputedStyle(r).backgroundColor),
      scroll: t.closest('.gb-rich-table__wrap').scrollWidth
              - t.closest('.gb-rich-table__wrap').clientWidth,
    };
  });
}"""

GREY = "rgb(243, 243, 243)"
NONE = "rgba(0, 0, 0, 0)"


async def main():
    async with async_playwright() as pw:
        br = await pw.chromium.launch(executable_path=EXE)

        async def probe(page_name, width, js):
            pg = await br.new_page(viewport={"width": width, "height": 900})
            await pg.goto(f"file://{ROOT}/{page_name}.html")
            await pg.add_style_tag(content=SETTLE)
            await pg.wait_for_timeout(250)
            r = await pg.evaluate(js)
            await pg.close()
            return r

        # --- 14a  .gb-acc-body__text: mobile 16/24/-0.32, desktop 18/28/-0.36
        for w, fs, lh, ls in ((390, 16, 24, -0.32), (767, 16, 24, -0.32),
                              (768, 16, 24, -0.32), (1440, 18, 28, -0.36)):
            r = await probe("science", w, ACC)
            ok_if(f"14a anchor @{w}", r is not None, ".gb-acc-body__text not found")
            if r:
                eq(f"14a font-size @{w}", r["fs"], fs, 0.05)
                eq(f"14a line-height @{w}", r["lh"], lh, 0.05)
                eq(f"14a letter-spacing @{w}", r["ls"], ls, 0.02)

        # --- 14b  .gb-faq--plain: mobile 52 / 64, desktop 94 top
        for w, pt, pb in ((390, 52, 64), (767, 52, 64), (768, 52, 64), (1440, 94, 120)):
            r = await probe("faq", w, FAQPLAIN)
            ok_if(f"14b anchor @{w}", r is not None, ".gb-faq--plain not found")
            if r:
                eq(f"14b padding-top @{w}", r["pt"], pt, 0.6)
                eq(f"14b padding-bottom @{w}", r["pb"], pb, 0.6)

        # --- 15a  cta-band button label stays on one line at every drawn width
        for w in (320, 360, 375, 390, 414, 575, 767, 768, 1440):
            r = await probe("faq", w, BTN)
            ok_if(f"15a anchor @{w}", r is not None, ".gb-cta-band__btn not found")
            if r:
                eq(f"15a label lines @{w}", r["lines"], 1)
                ok_if(f"15a label fits @{w}", r["inkW"] <= r["avail"] + 0.5,
                      f"ink {r['inkW']} > avail {r['avail']}")

        # --- 15b  both page-hero groups share one gap; the large wave still clears
        for w, gap in ((390, 64), (1440, 70)):
            for page, lg in (("faq", False), ("how-gumi-works", True), ("our-story", True)):
                r = await probe(page, w, HERO)
                ok_if(f"15b anchor {page}@{w}", r is not None, "hero/inner/scallop missing")
                if r:
                    eq(f"15b gap {page}@{w}", r["gap"], gap, 0.6)
                    eq(f"15b wave tile {page}@{w}", r["lgWave"], lg)
                    # the scallop is deliberately drawn 1px past its own height
                    # (r34's hairline-seam fix), so the section may end 1px short
                    ok_if(f"15b wave inside section {page}@{w}", r["slack"] >= -1.6,
                          f"scallop overruns section by {-r['slack']:.2f}")

        # --- 16 / 17  form section padding-bottom (both pages) + disclaimer
        #     margins (referral only -- get-in-touch has no disclaimer line)
        # r53: client-set margin 16px 0 -2px on phones, ramped to 0 by 1281, so
        # top and bottom no longer share one number.
        for w, pb, m, mb in ((390, 84, 16, -2), (767, 84, 16, -2), (768, 84, 16, -2), (1440, 96, 0, 0)):
            r = await probe("referral", w, FORM)
            ok_if(f"16/17 anchor @{w}", r is not None, "form-section/disclaimer missing")
            if r:
                eq(f"16 form padding-bottom @{w}", r["pb"], pb, 0.6)
                eq(f"17 disclaimer margin-top @{w}", r["mt"], m, 0.6)
                eq(f"17 disclaimer margin-bottom @{w}", r["mb"], mb, 0.6)
            g = await probe("get-in-touch", w, SECTION)
            ok_if(f"16 anchor get-in-touch @{w}", g is not None, ".gb-form-section missing")
            if g:
                eq(f"16 form padding-bottom get-in-touch @{w}", g["pb"], pb, 0.6)

        # --- 18  rich-text block spacing 16 on mobile, 20 on desktop
        for w, mb in ((390, 16), (767, 16), (768, 16), (1440, 20)):
            r = await probe("privacy-policy", w, RICH)
            ok_if(f"18 anchor @{w}", r is not None, ".gb-rich-text p not found")
            if r:
                eq(f"18 margin-bottom @{w}", r["mb"], mb, 0.6)

        # --- 19  shipping tables keep the board's grid at every width
        for w in (390, 767, 768, 1440):
            ts = await probe("shipping", w, TABLE)
            ok_if(f"19 anchor @{w}", ts is not None, "expected exactly 2 .gb-rich-table")
            if not ts:
                continue
            for i, t in enumerate(ts):
                eq(f"19 t{i} table-layout @{w}", t["layout"], "fixed")
                eq(f"19 t{i} header fill @{w}", t["headBg"], GREY)
                ok_if(f"19 t{i} cell border @{w}", t["border"].endswith("solid")
                      and float(t["border"].split()[0][:-2]) > 0, t["border"])
                eq(f"19 t{i} cell padding @{w}", t["pad"], "9.5px 12px")
                eq(f"19 t{i} body row height @{w}", t["rowH"], 44, 0.6)
                eq(f"19 t{i} no h-scroll @{w}", t["scroll"], 0)
                zeb = t["zebra"]
                ok_if(f"19 t{i} zebra @{w}",
                      all(c == (GREY if n % 2 else NONE) for n, c in enumerate(zeb)),
                      str(zeb))
            # fixed column keeps the board value; the fill column takes the rest
            eq(f"19 t0 hug column @{w}", ts[0]["cols"][0], 88, 0.6)
            eq(f"19 t1 fixed column @{w}", ts[1]["cols"][1], 147, 0.6)
            eq(f"19 t0 two-line header @{w}", ts[0]["headRowH"], 68, 0.6)
            eq(f"19 t1 one-line header @{w}", ts[1]["headRowH"], 44, 0.6)

        # At the board's own 350 both splits must land on the board. border-collapse
        # folds the outer edge into the table box, so the pair sums to 349, not 350
        # -- the board's 0.5 CENTER stroke takes no layout space in Figma.
        ts = await probe("shipping", 390, TABLE)
        if ts:
            eq("19 t0 hug col @390 == board 88", ts[0]["cols"][0], 88, 0.6)
            eq("19 t0 fill col @390 == board 262", ts[0]["cols"][1], 262, 1.1)
            eq("19 t1 fill col @390 == board 203", ts[1]["cols"][0], 203, 1.1)
            eq("19 t1 fixed col @390 == board 147", ts[1]["cols"][1], 147, 0.6)
            for i, t in enumerate(ts):
                eq(f"19 t{i} cols sum @390", sum(t["cols"]), t["w"] - 1, 0.6)

        await br.close()

    print(f"r48check: {CHECKS[0]} assertions, {len(FAILS)} failed")
    for f in FAILS:
        print("  ✗ " + f)
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
