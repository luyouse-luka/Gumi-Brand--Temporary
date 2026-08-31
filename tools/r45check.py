#!/usr/bin/env python3
"""Round-44 assertions — 修改任务文档.txt 第 10/11/12 条（第 13 条未做，见 PROJECT-STATUS 待决 S）。

    python3 tools/r45check.py

判据取法与理由：

1. 第 10 条（dosed 标题多出一行）是**行盒数**判据，不是「有没有 &nbsp;」。
   病因是行尾的 U+00A0 不像普通空格那样在行末悬挂：1440 处 "One pouch. Once a day."
   墨迹 475.4 + nbsp 11.1 = 486.5 比 mask 的 486 宽 0.5px，nbsp 自己折到第二行，
   于是 h2 占 3 个行盒而只显示 2 行文字，halo 在那空行上画出一团色块。
   所以判据 = **h2 高度 / 行高 == 真实文字行数**，并附一条全站不变量：
   凡是 display:none 的 <br>，其前后两个词必须同行 —— 这证明 &nbsp; 兼着的
   「此处不许断行」职责确实用不上，换成普通空格没有引入新的断点。
   ⚠ 只断言「HTML 里没有 &nbsp;」是没用的：那既不解释病因，也抓不住复发。

2. 第 12 条（story 与卡片网格同款）用**行数**判断，不是不同 x 位置的个数 ——
   三张卡跨两轨时落单那张是居中的，与前两张谁的 x 都不同，列数会被数成 3。
   这条坑第四十二轮踩过，见 HANDOFF「历轮踩到的坑」13。

3. 第 11 条的 gap 同时断言 1440 的定值与 768 处斜坡下端，后者防的是 767/768 跳档。
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


TITLE = r"""() => {
  const out = [];
  document.querySelectorAll('.gb-dosed__title').forEach((h, i) => {
    const cs = getComputedStyle(h);
    const lh = parseFloat(cs.lineHeight);
    const r = h.getBoundingClientRect();
    // 真实文字行数 = 内容层里不同 offsetTop 的个数（halo 是副本，排除）
    const words = [...h.querySelectorAll('.gb-line-word')];
    const tops = new Set(words.map(w => Math.round(w.getBoundingClientRect().top)));
    out.push({i, h: +r.height.toFixed(1), lh,
              boxes: Math.round(r.height / lh), lines: tops.size,
              text: words.map(w => w.textContent).join(' ')});
  });
  return out;
}"""

PROBE = r"""() => {
  const q = s => document.querySelector(s);
  const cs = (s, p) => { const e = q(s); return e ? getComputedStyle(e)[p] : null; };
  const o = {};
  o.dosedGap = cs('.gb-dosed__inner', 'rowGap');
  const g = q('.gb-story__inner');
  if (g) {
    const k = [...g.children].map(e => e.getBoundingClientRect());
    o.story = {rows: new Set(k.map(r => Math.round(r.y))).size,
               cols: new Set(k.map(r => Math.round(r.x))).size,
               n: k.length,
               xs: k.map(r => +r.x.toFixed(1)),
               ws: k.map(r => +r.width.toFixed(1))};
  }
  o.nbsp = document.body.innerHTML.indexOf(' ') > -1;
  o.overflowX = document.documentElement.scrollWidth - document.documentElement.clientWidth;
  return o;
}"""


async def main():
    data, titles = {}, {}
    plan = {"how-gumi-works.html": (1440, 1281, 1280, 1024, 900, 768, 767, 575, 390),
            # 1200 joined in r51: with the 3→2 step moved down from 1280, that is
            # where the lone third card starts being centred.
            "our-story.html":      (1440, 1281, 1280, 1200, 1024, 768, 767, 700, 576, 575, 390)}
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path=EXE)
        for page, widths in plan.items():
            for w in widths:
                pg = await b.new_page(viewport={"width": w, "height": 1000})
                await pg.goto("file://" + os.path.join(ROOT, page))
                await pg.add_style_tag(content=SETTLE)
                await pg.evaluate("() => document.fonts.ready")
                await pg.evaluate("""() => document.querySelectorAll('[data-line-reveal]')
                                       .forEach(e => e.scrollIntoView())""")
                await pg.wait_for_timeout(700)
                data[(page, w)] = await pg.evaluate(PROBE)
                if page == "how-gumi-works.html":
                    titles[w] = await pg.evaluate(TITLE)
                await pg.close()
        await b.close()

    H = lambda w: data[("how-gumi-works.html", w)]
    O = lambda w: data[("our-story.html", w)]

    # ===== 第 10 条：标题的行盒数 == 文字行数 =============================
    for w in (1440, 1281, 1280, 1024, 900, 768, 767, 575, 390):
        ts = titles[w]
        ok_if(f"{w} how-gumi-works 有两个 dosed 标题", len(ts) == 2, str(len(ts)))
        for t in ts:
            ok_if(f"{w} dosed 标题 #{t['i']} 没有多出空行盒",
                  t["boxes"] == t["lines"],
                  f"{t['boxes']} 个行盒 / {t['lines']} 行文字 (h={t['h']}, lh={t['lh']})")
    # 这一条就是需求方看到的那个症状：1440 处第二个标题曾是 3 个行盒、2 行文字
    t = [x for x in titles[1440] if x["i"] == 1][0]
    eq("1440 “One pouch…” 是两行", t["lines"], 2)
    eq("1440 “One pouch…” 高度 = 2 × 48", t["h"], 96, tol=0.5)
    # 全站不再有 U+00A0（19 处全部换成普通空格）
    for w in (1440, 390):
        ok_if(f"{w} how-gumi-works 正文里没有 U+00A0", not H(w)["nbsp"])
        ok_if(f"{w} our-story 正文里没有 U+00A0", not O(w)["nbsp"])

    # ===== 第 11 条：dosed__inner gap 80 =================================
    eq("1440 .gb-dosed__inner gap（需求方定 80，板是 96）", H(1440)["dosedGap"], "80px")
    eq("1281 .gb-dosed__inner gap", H(1281)["dosedGap"], "80px")
    eq("390 .gb-dosed__inner gap 不变", H(390)["dosedGap"], "48px")
    eq("767 .gb-dosed__inner gap 不变", H(767)["dosedGap"], "48px")
    # 斜坡下端要接住手机值，否则 767/768 跳档
    ok_if("768 .gb-dosed__inner gap 接住 48（无缝）",
          abs(float(H(768)["dosedGap"][:-2]) - 48) < 0.7, str(H(768)["dosedGap"]))
    # 上端要接住 80
    ok_if("1280 .gb-dosed__inner gap 接住 80（无缝）",
          abs(float(H(1280)["dosedGap"][:-2]) - 80) < 0.7, str(H(1280)["dosedGap"]))

    # ===== 第 12 条：story 3 -> 2 -> 1 ===================================
    # 用行数判断：3 张卡 —— 三列 1 行 / 两列 2 行 / 单列 3 行
    # r51 moved the 3→2 step from 1280 to 1200 (client-set); 1280 is three-up now.
    for w, rows in ((1440, 1), (1281, 1), (1280, 1), (1024, 2), (768, 2), (767, 2),
                    (700, 2), (576, 2), (575, 3), (390, 3)):
        d = O(w)["story"]
        eq(f"{w} story 三张卡排 {rows} 行", d["rows"], rows)
        eq(f"{w} story 仍是 3 张卡", d["n"], 3)
    # 落单那张在两列档必须居中：它的 x 应落在前两张的 x 之间
    # 1280 dropped off this list with the threshold move — three-up has no lone card.
    for w in (1200, 1024, 768, 576):
        xs = O(w)["story"]["xs"]
        ok_if(f"{w} story 落单的第三张居中",
              xs[0] < xs[2] < xs[1], f"xs={xs}")
    # 单列档 span 必须重置，否则隐式网格把第二列造回来
    eq("575 story 是真正的单列", O(575)["story"]["cols"], 1)
    eq("390 story 是真正的单列", O(390)["story"]["cols"], 1)
    # 桌面不变：三张等宽
    ws = O(1440)["story"]["ws"]
    ok_if("1440 story 三张等宽", max(ws) - min(ws) < 0.6, f"ws={ws}")

    for page, fn, widths in (("how-gumi-works", H, (1440, 1281, 1280, 1024, 900, 768, 767, 575, 390)),
                             ("our-story", O, (1440, 1281, 1280, 1024, 768, 767, 700, 576, 575, 390))):
        for w in widths:
            eq(f"{w} {page}: 无横向溢出", fn(w)["overflowX"], 0)

    print("=" * 72)
    if FAILS:
        print(f"FAIL — {len(FAILS)}")
        for f in FAILS:
            print("  ✗", f)
    else:
        print("r45: all assertions pass")
    print("=" * 72)
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
