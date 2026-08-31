#!/usr/bin/env python3
"""Round-52 assertions — 手机抽屉关闭时不得横跳（第四十九轮起的「顺带发现」，本轮授权修）。

    python3 tools/r53check.py

与 r50check 第 4 条同构，病也同形：`is-menu-open` 从前是在摘掉 `is-open` 的同一帧
摘掉的，滚动条当场回来，抽屉的包含块随之变窄，而它此刻还在滑出、完全看得见 ——
用户看到它横跳一个滚动条的宽度。

判据取法：

1. **必须拿回真实滚动条**。Playwright 默认给 headless chromium 传 `--hide-scrollbars`，
   `innerWidth - clientWidth` 恒为 0：没有宽度可失去，再坏的写法也不会位移，
   判据会全绿地放过坏页面。这里 `ignore_default_args` 掉那个 flag，gap 仍为 0 就 abort。
   （手机真机是 overlay 滚动条、本来就不占宽，所以用例跑在 **700 宽的桌面窗口**里。）

2. **在滑出中途采样，并同时断言那一刻抽屉还看得见**（高度 > 0）——
   量一个已经收完的元素有没有位移是没有意义的。

3. **两条反向断言**：锁最终必须解开（否则「没位移」可以靠永不解锁作弊），
   以及滑出途中重新打开时，锁不许被上一次关闭挂起的定时器解掉。
"""
import os
import sys

from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXE = os.path.expanduser("~/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome")

CASES = [("index", 700), ("faq", 700), ("pdp", 700)]

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


STATE = """() => {
  const p = document.querySelector('.gb-header__panel');
  const b = p.getBoundingClientRect();
  return {x: +b.x.toFixed(2), w: +b.width.toFixed(2), h: +b.height.toFixed(2),
          client: document.documentElement.clientWidth,
          locked: document.documentElement.classList.contains('is-menu-open'),
          open: document.getElementById('site-header').classList.contains('is-open')};
}"""


def main():
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=EXE,
                               ignore_default_args=["--hide-scrollbars"])
        for name, w in CASES:
            pg = b.new_page(viewport={"width": w, "height": 900})
            pg.goto("file://" + os.path.join(ROOT, name + ".html"))
            pg.wait_for_timeout(700)

            gap = pg.evaluate("() => window.innerWidth - document.documentElement.clientWidth")
            if gap <= 0:
                print("ABORT %s@%d: 没有真实滚动条（innerWidth - clientWidth = %s），"
                      "所有断言都会恒真通过。" % (name, w, gap))
                sys.exit(2)

            pg.click(".gb-header__toggle")
            pg.wait_for_timeout(600)
            opened = pg.evaluate(STATE)
            ok_if("%s 抽屉打开了" % name, opened["open"] and opened["h"] > 0, str(opened))
            ok_if("%s 打开时页面已锁" % name, opened["locked"])

            # 关闭：手机档 toggle 被抽屉盖住，只有面板自己的关闭按钮可点
            pg.click(".gb-header__panel-close")
            pg.wait_for_timeout(80)
            mid = pg.evaluate(STATE)
            # 采样那一刻抽屉必须还看得见，否则下面两条没有意义
            ok_if("%s 滑出中途抽屉仍可见（判据前提）" % name,
                  mid["h"] > 1 and mid["x"] + mid["w"] > 1,
                  "h=%s right=%s" % (mid["h"], mid["x"] + mid["w"]))
            # ⚠ 只量宽度，不量 x：手机档的抽屉是 translateX 滑出的，x 在这段时间里
            # 本来就在动。锁解除让 fixed 盒子的包含块变宽 —— 那是**宽度**的事。
            eq("%s 滑出中途抽屉宽度不变" % name, mid["w"], opened["w"], tol=0.6)
            eq("%s 滑出中途视口宽不变（锁还在）" % name, mid["client"], opened["client"])
            ok_if("%s 滑出中途仍锁着" % name, mid["locked"])

            # 反向：锁最终必须解开，否则「没位移」可以靠永不解锁作弊
            pg.wait_for_timeout(1100)          # $t-drawer 是 0.7s
            done = pg.evaluate(STATE)
            ok_if("%s 滑出结束后锁已解除" % name, not done["locked"])
            eq("%s 解锁后视口宽回到有滚动条的宽度" % name, done["client"], opened["client"] - gap)
            ok_if("%s 抽屉已滑出视口" % name, done["x"] + done["w"] <= 1,
                  "right=%s" % (done["x"] + done["w"]))

            # 反向：滑出途中重开，旧的挂起回调不许把新抽屉的锁解掉
            pg.click(".gb-header__toggle")
            pg.wait_for_timeout(600)
            pg.click(".gb-header__panel-close")
            pg.wait_for_timeout(60)
            pg.click(".gb-header__toggle")          # 上一次的解锁还挂着
            pg.wait_for_timeout(1100)               # 等它超时
            again = pg.evaluate(STATE)
            ok_if("%s 滑出途中重开：锁不许被旧定时器解掉" % name,
                  again["open"] and again["locked"], str(again))
            pg.close()

        # ===== 2. reels 的无缝循环（待决 AG，第五十二轮由需求方裁决）=========
        # Swiper 11 的 loop 是重排现有 slide 而不是复制 DOM，卡数不到可见张数的
        # 两倍就会在一侧留空（第五十轮实测 1440 处右边空 232.5px，正是因此才改用
        # rewind）。本轮把 reels 从 5 张加到 10 张占位卡换回 loop。
        #
        # 判据不取「两侧不留空」而取「两侧都真的溢出」：留空是正数、贴边是 0、
        # 盖满是负数，前两者对一个刚好排满的轨道也成立，只有负数才说明轨道两头
        # 都还有卡可推 —— 无缝的定义就是这个。
        # 而且**走动之后也要成立**：静止那一帧排得满，不代表推几张之后还满。
        RAIL = """() => {
          const t = document.querySelector('.gb-reels');
          const sw = t.swiper;
          const b = [...t.querySelectorAll('.swiper-slide')].map(e => e.getBoundingClientRect());
          const tb = t.getBoundingClientRect();
          return {loop: sw ? sw.params.loop : null, rewind: sw ? sw.params.rewind : null,
                  real: sw ? sw.realIndex : null, n: b.length,
                  perView: +(tb.width / (b[0].width + (sw ? sw.params.spaceBetween : 0))).toFixed(2),
                  left: +(Math.min(...b.map(r => r.left)) - tb.left).toFixed(1),
                  right: +(tb.right - Math.max(...b.map(r => r.right))).toFixed(1),
                  arrowsDead: [...document.querySelectorAll('[data-slider-prev],[data-slider-next]')]
                                .some(e => e.disabled)};
        }"""
        for name in ("index", "pdp", "our-story", "how-gumi-works"):
            for w in (1440, 1280, 992, 768, 767, 390):
                pg = b.new_page(viewport={"width": w, "height": 1000})
                pg.goto("file://" + os.path.join(ROOT, name + ".html"))
                pg.wait_for_timeout(800)
                tag = "%s@%d reels" % (name, w)
                d = pg.evaluate(RAIL)
                eq("%s loop 开着" % tag, d["loop"], True)
                eq("%s rewind 关着（两者互斥）" % tag, d["rewind"], False)
                eq("%s 起步在第一张" % tag, d["real"], 0)
                # loop 的硬前提。卡数掉到这条线以下，Swiper 会静默不循环，
                # 而 params.loop 照样报 True —— 只断言 loop 开着是抓不到的。
                ok_if("%s 卡数 > 2 倍可见张数（loop 的前提）" % tag,
                      d["n"] > 2 * d["perView"], "n=%s perView=%s" % (d["n"], d["perView"]))
                ok_if("%s 静止时左侧盖满并溢出" % tag, d["left"] < 0, "left=%s" % d["left"])
                ok_if("%s 静止时右侧盖满并溢出" % tag, d["right"] < 0, "right=%s" % d["right"])
                ok_if("%s 箭头不置灰" % tag, not d["arrowsDead"])
                # 推 8 张之后再看一次：静止那一帧满不代表走起来还满
                # 间隔要大于 Swiper 的 speed（400ms），否则动画途中的点击被吞掉，
                # 实际走的张数少于点的次数。
                for _ in range(8):
                    pg.click("[data-slider-next]")
                    pg.wait_for_timeout(500)
                a = pg.evaluate(RAIL)
                ok_if("%s 走 8 张后左侧仍盖满" % tag, a["left"] < 0, "left=%s" % a["left"])
                ok_if("%s 走 8 张后右侧仍盖满" % tag, a["right"] < 0, "right=%s" % a["right"])
                pg.close()

        # 反向：expert 轨不在这次裁决范围内（≥992 是三列网格，加卡到 loop 尺寸
        # 会把一行三张变成三行，动的是桌面），必须还在 rewind 上。
        pg = b.new_page(viewport={"width": 991, "height": 1000})
        pg.goto("file://" + os.path.join(ROOT, "reviews.html"))
        pg.wait_for_timeout(800)
        d = pg.evaluate("""() => {
          const sw = document.querySelector('.gb-expert__cards').swiper;
          return {loop: sw.params.loop, rewind: sw.params.rewind,
                  n: document.querySelectorAll('.gb-expert-card').length};
        }""")
        eq("expert 轨没有被一起改成 loop", d["loop"], False)
        eq("expert 轨仍用 rewind", d["rewind"], True)
        eq("expert 轨仍是三张卡（桌面的三列网格没被动）", d["n"], 3)
        pg.close()

        b.close()

    print("=" * 72)
    if FAILS:
        print("FAIL — %d / %d 条断言" % (len(FAILS), CHECKED[0]))
        for f in FAILS:
            print("  x", f)
    else:
        print("r53check: %d assertions, 0 failed" % CHECKED[0])
    print("=" * 72)
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
