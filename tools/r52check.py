#!/usr/bin/env python3
"""Round-51 assertions — 修改任务文档.txt 第二组第 1-7 条。

    python3 tools/r52check.py

判据取法与理由：

1. 第 1 条（3 → 2 → 1 的阈值改成 1200 / 575）**按行数判列数，不数 x 的取值个数**。
   三张卡两列时落单那张居中，它与前两张谁的 x 都不同 —— 数 x 会把两列数成三列
   （第四十二轮踩过）。这里按每张卡的 top 聚类分行，再断言每行的张数。
   四个组件一起验：三个网格（science / nutrition / story）和一个 flex
   （testimonials）走的是两套不同装置，只验网格会漏掉 flex 那套。
   两个接缝（1200/1201、575/576）各自成对断言 —— 阈值改动的风险全在接缝上。
   ⚠ 单列档还要断言 span 真的被重置：对着一条轨道，隐式网格会拿 span 2 再造出
   第二列，卡片依旧两列排，而 grid-template-columns 读回来是 "1fr"，全绿。
   行数判据抓得住这一条。

2. 第 2 条（cta 最大宽度）取**盒子的实际宽度**，不读 max-width 属性：
   .gb-product__cta 基础就有 width:100%，属性断言分不清「上限生效了」和
   「容器本来就更窄」（第四十三轮坑 16）。另断言 768 处**不**受限，
   否则一个泼到全站的 max-width 也会全绿。

3. 第 4/5/6 条量的是**相对几何**（探出卡片边缘多少 px、中心落在卡宽的百分之几、
   图相对画框上移几分之几），不是 CSS 声明值：这几条都是百分比或负偏移，
   声明对了而参照系错了照样是坏的。

4. 第 6 条另加一条反向断言：science / reviews 的 .gb-ingredients__disc 复用同一个
   .gb-promo-art，它必须还是 -4%。改动写在 .gb-promo-card--white 作用域里就是为了
   不泼到它身上，不验这条等于没验作用域。

5. 第 7 条断言「右边的空隙比左边多 15」。改前是 margin-left:auto 吃掉全部余量、
   盒子挂到最右（右 15、左 W-w-15），改后 align-items:center 接管、右比左多 15。
   直接断言「左边距 == 0」会恒真地放过 auto —— auto 解析成 0 的场合太多。
"""
import math
import os
import sys

from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXE = os.path.expanduser("~/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome")

# 完整版：只注入 animation:none 会让入场区块停在第 0 帧（memory
# kill-animations-blanks-reveal-blocks），三个属性要一起给。
SETTLE = """.wowo,.gb-float-art,[data-line-reveal],.gb-line-mask__inner,.gb-ink-halo{
  opacity:1!important;transform:none!important;animation:none!important}"""

FAILS = []
CHECKED = [0]


def eq(label, got, want, tol=None):
    CHECKED[0] += 1
    try:
        ok = (abs(float(got) - float(want)) <= tol) if tol is not None else (got == want)
    except (TypeError, ValueError):
        ok = False
    if not ok:
        FAILS.append("%s: got %r, want %r%s" % (label, got, want, " (+/-%s)" % tol if tol else ""))


def ok_if(label, cond, detail=""):
    CHECKED[0] += 1
    if not cond:
        FAILS.append(label + ((": " + detail) if detail else ""))


def page(b, name, w, h=1200):
    pg = b.new_page(viewport={"width": w, "height": h})
    pg.goto("file://" + os.path.join(ROOT, name))
    pg.add_style_tag(content=SETTLE)
    pg.wait_for_timeout(350)
    return pg


# 每张卡的 top 聚类成行，返回每行的张数。align-items 在这些组件里是 start /
# stretch，同一行的卡顶边对齐，5px 容差吸收亚像素。
ROWS = """(sel) => [...document.querySelectorAll(sel)].map(box => {
  const kids = [...box.children].map(e => e.getBoundingClientRect());
  const rows = [];
  for (const r of kids.sort((a, b) => a.top - b.top || a.left - b.left)) {
    const row = rows.find(x => Math.abs(x.top - r.top) < 5);
    if (row) row.n++; else rows.push({top: r.top, n: 1});
  }
  return {rows: rows.map(r => r.n),
          overflow: box.scrollWidth - box.clientWidth,
          pageOverflow: document.documentElement.scrollWidth - document.documentElement.clientWidth};
})"""


def expect_rows(n, cols):
    """n 张卡排成 cols 列时，每行应有几张。"""
    return [min(cols, n - i * cols) for i in range(int(math.ceil(n / float(cols))))]


# 组件 -> (页面, 每处的卡片数)
LADDER = [
    (".gb-science__cards", [("index.html", [3]), ("science.html", [3, 3])]),
    (".gb-nutrition__cards", [("index.html", [3])]),
    (".gb-story__inner", [("our-story.html", [3])]),
    (".gb-testimonials", [("index.html", [3]), ("our-story.html", [4]),
                          ("how-gumi-works.html", [4])]),
]

# 客户定的阈值：≥1201 三列 / 576-1200 两列 / ≤575 一列
WIDTHS = [(1440, 3), (1281, 3), (1201, 3), (1200, 2), (992, 2), (768, 2),
          (767, 2), (576, 2), (575, 1), (390, 1)]


def rect_of(pg, sel, within=None):
    return pg.evaluate("""(a) => {
      const root = a[1] ? document.querySelector(a[1]) : document;
      const e = root && root.querySelector(a[0]);
      if (!e) return null;
      const b = e.getBoundingClientRect();
      return {x: b.x, y: b.y, w: b.width, h: b.height, right: b.right, bottom: b.bottom,
              display: getComputedStyle(e).display};
    }""", [sel, within])


def main():
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=EXE)

        # ===== 1. 3 → 2 → 1，阈值 1200 / 575 =============================
        # 页面 -> 该页要查的 (选择器, 卡片数列表)
        by_page = {}
        for sel, uses in LADDER:
            for name, counts in uses:
                by_page.setdefault(name, []).append((sel, counts))

        for name, sels in sorted(by_page.items()):
            for w, cols in WIDTHS:
                pg = page(b, name, w)
                for sel, counts in sels:
                    got = pg.evaluate(ROWS, sel)
                    ok_if("%s %s@%d 找得到（选择器锚点）" % (name, sel, w),
                          len(got) == len(counts),
                          "found %d, expected %d" % (len(got), len(counts)))
                    for i, (g, n) in enumerate(zip(got, counts)):
                        eq("%s %s[%d]@%d 分行" % (name, sel, i, w),
                           g["rows"], expect_rows(n, cols))
                        ok_if("%s %s[%d]@%d 容器不横向溢出" % (name, sel, i, w),
                              g["overflow"] <= 1, "scrollWidth-clientWidth=%s" % g["overflow"])
                        ok_if("%s@%d 页面不横向溢出" % (name, w),
                              g["pageOverflow"] <= 1, "%s" % g["pageOverflow"])
                pg.close()

        # ===== 2. .gb-product__info padding / .gb-product__cta 上限 ========
        for w, pad in ((1440, 32), (1281, 32), (1200, 0), (992, 0), (768, 0), (767, 0), (390, 0)):
            pg = page(b, "pdp.html", w)
            cs = pg.evaluate("""() => {
              const e = document.querySelector('.gb-product__info'), s = getComputedStyle(e);
              return [s.paddingLeft, s.paddingRight];
            }""")
            eq("%d product__info padding-left" % w, float(cs[0][:-2]), pad, tol=0.1)
            eq("%d product__info padding-right" % w, float(cs[1][:-2]), pad, tol=0.1)
            pg.close()

        for w in (767, 576, 390, 768):
            pg = page(b, "pdp.html", w)
            cta = rect_of(pg, ".gb-product__cta")
            info = rect_of(pg, ".gb-product__info")
            if w == 768:
                # 两栏并排，上限属于 narrow —— 这里按钮必须仍然跟满整列。
                eq("768 cta 宽 == info 内容宽（上限不越界到 tablet）", cta["w"], info["w"], tol=0.6)
            else:
                ok_if("%d cta 宽不超过 520" % w, cta["w"] <= 520.6, "%.1f" % cta["w"])
                eq("%d cta 宽" % w, cta["w"], min(520.0, info["w"]), tol=0.6)
                # 居中：左右两侧留白相等
                eq("%d cta 在信息列里居中" % w,
                   (cta["x"] - info["x"]) - (info["right"] - cta["right"]), 0, tol=0.6)
            pg.close()

        # ===== 3. .gb-promo-card 手机上限 575 =============================
        for w, want in ((767, 575), (576, 536), (390, 350)):
            pg = page(b, "pdp.html", w)
            for cls in ("--green", "--white"):
                r = rect_of(pg, ".gb-promo-card.gb-promo-card%s" % cls)
                eq("%d promo-card%s 宽" % (w, cls), r["w"], want, tol=0.6)
            pg.close()
        pg = page(b, "pdp.html", 767)
        r = rect_of(pg, ".gb-promo-card--green")
        ok_if("767 promo-card 不再停在板上的 343", r["w"] > 343 + 1, "%.1f" % r["w"])
        pg.close()

        # ===== 4. 绿卡 lip--v 探出 95（白卡仍是 63）========================
        for w in (1440, 1024, 768):
            pg = page(b, "pdp.html", w)
            d = pg.evaluate("""() => {
              const out = {};
              for (const k of ['green', 'white']) {
                const c = document.querySelector('.gb-promo-card--' + k);
                const l = c.querySelector('.gb-promo-card__lip--v');
                // The lip is absolutely positioned inside its own HALF of the
                // card (media on the green one, art on the white), not on the
                // card box -- measuring against the card reads ~-436.
                // It is an <svg>, so offsetParent is undefined; walk up instead.
                const host = l.closest('.gb-promo-card__media, .gb-promo-card__art');
                const hb = host.getBoundingClientRect();
                const lb = l.getBoundingClientRect();
                out[k] = {right: lb.right - hb.right, left: hb.left - lb.left,
                          w: lb.width, host: host.className.split(' ')[0],
                          display: getComputedStyle(l).display};
              }
              return out;
            }""")
            eq("%d 绿卡 lip--v 右探出（相对 media 半边）" % w, d["green"]["right"], 95, tol=0.6)
            eq("%d 绿卡 lip--v 挂在 media 半边上" % w, d["green"]["host"], "gb-promo-card__media")
            eq("%d 白卡 lip--v 左探出仍是 63" % w, d["white"]["left"], 63, tol=0.6)
            eq("%d 白卡 lip--v 挂在 art 半边上" % w, d["white"]["host"], "gb-promo-card__art")
            eq("%d lip--v 盒宽仍是 126" % w, d["green"]["w"], 126, tol=0.6)
            pg.close()
        pg = page(b, "pdp.html", 767)
        eq("767 lip--v 收起", rect_of(pg, ".gb-promo-card__lip--v")["display"], "none")
        pg.close()

        # ===== 5. stack 铺满 / btn 不受影响 / lip--h 左移到 50.5% ==========
        for w in (767, 576, 390):
            pg = page(b, "pdp.html", w)
            d = pg.evaluate("""() => {
              const c = document.querySelector('.gb-promo-card--white');
              const body = c.querySelector('.gb-promo-card__body');
              const st = c.querySelector('.gb-promo-card__stack');
              const bt = c.querySelector('.gb-promo-card__btn');
              const cs = getComputedStyle(body);
              const inner = body.getBoundingClientRect().width
                            - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
              return {inner: inner, stack: st.getBoundingClientRect().width,
                      btn: bt.getBoundingClientRect().width};
            }""")
            eq("%d stack 铺满 body 内容宽" % w, d["stack"], d["inner"], tol=0.6)
            eq("%d btn 仍停在 347（没被 stack 的 100%% 带走）" % w,
               d["btn"], min(347.0, d["inner"]), tol=0.6)
            lh = pg.evaluate("""() => {
              const c = document.querySelector('.gb-promo-card--green');
              const l = c.querySelector('.gb-promo-card__lip--h');
              const cb = c.getBoundingClientRect(), lb = l.getBoundingClientRect();
              return {ratio: (lb.left + lb.width / 2 - cb.left) / cb.width,
                      display: getComputedStyle(l).display};
            }""")
            eq("%d lip--h 显示" % w, lh["display"], "block")
            eq("%d lip--h 中心落在卡宽的 50.5%%" % w, lh["ratio"], 0.505, tol=0.004)
            pg.close()
        pg = page(b, "pdp.html", 1440)
        st = rect_of(pg, ".gb-promo-card__stack", ".gb-promo-card--white")
        eq("1440 stack 仍是板上的 347 copy 列", st["w"], 347, tol=0.6)
        pg.close()

        # ===== 6. 白卡 artwork top -8%（ingredients 的同一组件不受影响）=====
        for w in (767, 576, 390):
            pg = page(b, "pdp.html", w)
            d = pg.evaluate("""() => {
              const c = document.querySelector('.gb-promo-card--white');
              const a = c.querySelector('.gb-promo-art'), i = c.querySelector('.gb-promo-art__img');
              const ab = a.getBoundingClientRect(), ib = i.getBoundingClientRect();
              return (ib.top - ab.top) / ab.height;
            }""")
            eq("%d 白卡 promo-art__img 上移 8%%" % w, d, -0.08, tol=0.002)
            pg.close()
        for name in ("science.html", "reviews.html"):
            pg = page(b, name, 390)
            d = pg.evaluate("""() => {
              const a = document.querySelector('.gb-ingredients__disc .gb-promo-art');
              const i = a.querySelector('.gb-promo-art__img');
              const ab = a.getBoundingClientRect(), ib = i.getBoundingClientRect();
              return (ib.top - ab.top) / ab.height;
            }""")
            eq("%s ingredients 复用的 promo-art 仍是 -4%%" % name, d, -0.04, tol=0.002)
            pg.close()

        # ===== 7. list 不再靠右：右侧空隙比左侧多 15 =======================
        # 这条反转过两次：r51 按第一组·7 去掉 auto 左边距 → r56 按第二组·2 改成
        # 正居中 → r57 需求方最终裁决「pc 端居中、手机端去掉居中」，撤回 r56、
        # 回到这里。**这是终版**，别再按板或按 r56 改回去。完整覆盖见 r56check AQ。
        for w in (767, 576, 390):
            pg = page(b, "pdp.html", w)
            d = pg.evaluate("""() => {
              const c = document.querySelector('.gb-promo-card--white');
              const st = c.querySelector('.gb-promo-card__stack');
              const li = c.querySelector('.gb-promo-card__list');
              const sb = st.getBoundingClientRect(), lb = li.getBoundingClientRect();
              return {left: lb.left - sb.left, right: sb.right - lb.right,
                      ml: getComputedStyle(li).marginLeft,
                      mr: getComputedStyle(li).marginRight};
            }""")
            eq("%d list 右侧空隙比左侧多 15（终版）" % w, d["right"] - d["left"], 15, tol=0.6)
            ok_if("%d list 不贴住左边（居中后左移 7.5，不是靠左）" % w,
                  d["left"] > 1, "left=%.2f" % d["left"])
            eq("%d list margin-left" % w, d["ml"], "0px")
            pg.close()
        pg = page(b, "pdp.html", 1440)
        d = pg.evaluate("""() => {
          const c = document.querySelector('.gb-promo-card--white');
          const st = c.querySelector('.gb-promo-card__stack');
          const li = c.querySelector('.gb-promo-card__list');
          const sb = st.getBoundingClientRect(), lb = li.getBoundingClientRect();
          return (lb.left - sb.left) - (sb.right - lb.right);
        }""")
        eq("1440 list 仍然居中（改动只属于 narrow）", d, 0, tol=0.6)
        pg.close()

        b.close()

    print("=" * 72)
    if FAILS:
        print("FAIL — %d / %d 条断言" % (len(FAILS), CHECKED[0]))
        for f in FAILS:
            print("  x", f)
    else:
        print("r52check: %d assertions, 0 failed" % CHECKED[0])
    print("=" * 72)
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
