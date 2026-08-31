#!/usr/bin/env python3
"""Round-49 assertions — 修改任务文档.txt 第 1-8 条。

    python3 tools/r50check.py

判据取法与理由：

1. 第 2 条（deco-bear pc 固定宽高）不只断言 1440 的两个数，还要断言 **1920 与
   1440 一模一样** —— 「固定」的意思就是它不再随视口长大，只在 1440 上量等于
   没量。另加两个接缝断言（767/768、1280/1281），因为把 pc 钉成 px 会在
   1280/1281 造出 94→106 的跳档，那是这次改动**新引入**的风险。

2. 第 3 条（Swiper）的核心判据是 **slide 矩形 == stage 矩形**。原来的 slide 是
   position:absolute + inset:0，换成 swiper-slide 之后靠的是 wrapper 的
   height:100% 一路传下来；这条链断了的话页面看着还在，只是图片高度塌掉，
   而任何「有没有 swiper-initialized」的断言都照样全绿。
   liveness：先断言 `typeof Swiper === "function"`。脚本 404 时 gallery 模块
   会安静早退，下面所有交互断言都会变成「没变化 == 通过」。

3. 第 4 条（弹窗关闭抖动）在**淡出中途**采样，并同时断言那一刻 panel 的
   opacity 仍是 1 —— 量一个已经看不见的元素有没有位移是没有意义的。
   另加两条反向断言：锁最终必须解除（否则「没位移」可以靠永不解锁作弊），
   以及淡出期间重新打开时锁不许被那次关闭的定时器解掉。

4. 第 8 条同时断言两组卡片：95% 组回到板值 56/44，50% 组（--nutrient）保持
   自己的 36/40。只查前者会漏掉「把两组一起带回 56」这个真正的风险。
"""
import os
import sys

from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXE = os.path.expanduser("~/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome")

LIME = "rgb(181, 237, 97)"
GREEN = "rgb(0, 86, 53)"
GREEN900 = "rgb(0, 65, 40)"
WHITE = "rgb(255, 255, 255)"
INK = "rgb(1, 19, 7)"

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


def px(v):
    return float(str(v).replace("px", ""))


def page(b, name, w, h=1000):
    pg = b.new_page(viewport={"width": w, "height": h})
    pg.goto("file://" + os.path.join(ROOT, name))
    pg.wait_for_timeout(500)
    return pg


CS = """(a) => { const e = document.querySelector(a[0]); return e ? getComputedStyle(e)[a[1]] : null; }"""


def main():
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=EXE,
                               ignore_default_args=["--hide-scrollbars"])

        # ===== 1. .gb-stats__note margin-top ==============================
        for w, want in ((1440, -34), (1281, -34), (768, -34), (767, -16), (390, -16)):
            pg = page(b, "index.html", w)
            eq("%d .gb-stats__note margin-top" % w,
               px(pg.evaluate(CS, [".gb-stats__note", "marginTop"])), want, tol=0.1)
            pg.close()

        # ===== 2. .gb-stats__deco-bear 固定宽高 ============================
        RATIO = 583.0 / 387.0
        sizes = {}
        for w in (1920, 1441, 1440, 1281, 1280, 1024, 768, 767, 575, 390):
            pg = page(b, "index.html", w)
            d = pg.evaluate("""() => {
              const e = document.querySelector('.gb-stats__deco-bear');
              const cs = getComputedStyle(e);
              return {w: parseFloat(cs.width), h: parseFloat(cs.height)};
            }""")
            sizes[w] = d
            eq("%d deco-bear 宽高比 = 387/583" % w, d["h"] / d["w"], RATIO, tol=0.01)
            pg.close()
        eq("1440 deco-bear 宽", sizes[1440]["w"], 106, tol=0.5)
        eq("1440 deco-bear 高", sizes[1440]["h"], 159.68, tol=0.5)
        # 「固定」= 视口再宽也不长大。只量 1440 等于没量。
        eq("1920 deco-bear 宽与 1440 相同（不再随视口长大）", sizes[1920]["w"], sizes[1440]["w"], tol=0.05)
        eq("1920 deco-bear 高与 1440 相同", sizes[1920]["h"], sizes[1440]["h"], tol=0.05)
        eq("1441 deco-bear 宽与 1440 相同", sizes[1441]["w"], sizes[1440]["w"], tol=0.05)
        eq("767 deco-bear 宽（narrow 定值）", sizes[767]["w"], 81.6, tol=0.1)
        eq("390 deco-bear 宽不变", sizes[390]["w"], 81.6, tol=0.1)
        # 接缝：把 pc 钉成 px 会在 1280/1281 造出跳档，这是本轮新引入的风险
        eq("768 deco-bear 接住 767 的 81.6（无缝）", sizes[768]["w"], 81.6, tol=0.7)
        eq("1280 deco-bear 接住 1281 的 106（无缝）", sizes[1280]["w"], 106, tol=0.7)
        eq("1281 deco-bear 宽", sizes[1281]["w"], 106, tol=0.5)
        ok_if("768→1280 deco-bear 单调变宽",
              sizes[768]["w"] < sizes[1024]["w"] < sizes[1280]["w"],
              "%.1f %.1f %.1f" % (sizes[768]["w"], sizes[1024]["w"], sizes[1280]["w"]))

        # ===== 3. Swiper ==================================================
        GAL = ("index.html", "pdp.html", "reviews.html", "how-gumi-works.html", "our-story.html")
        for name in GAL:
            pg = page(b, name, 1440)
            # liveness：脚本没加载的话 gallery 会安静早退，下面全部恒真。
            # 直接中止而不是记一条 fail —— 后面的交互断言会先撞出 traceback，
            # 真正的原因反而被埋在栈里。
            if pg.evaluate("() => typeof Swiper") != "function":
                print("ABORT %s: assets/swiper-bundle.min.js 没加载上 — 图廊会安静"
                      "早退，下面每一条断言都会变成恒真" % name)
                sys.exit(2)
            d = pg.evaluate("""() => {
              const st = document.querySelector('[data-gallery-track]');
              const sl = [...st.querySelectorAll('.swiper-slide')];
              const r = e => { const b = e.getBoundingClientRect();
                               return [+b.x.toFixed(1), +b.y.toFixed(1), +b.width.toFixed(1), +b.height.toFixed(1)]; };
              return {init: st.classList.contains('swiper-initialized'),
                      fade: st.classList.contains('swiper-fade'),
                      n: sl.length,
                      active: sl.findIndex(e => e.classList.contains('swiper-slide-active')),
                      op: sl.map(e => getComputedStyle(e).opacity),
                      stage: r(st), slide: r(sl[0]), last: r(sl[4]),
                      cursor: getComputedStyle(sl[0]).cursor,
                      ease: getComputedStyle(sl[0]).transitionTimingFunction,
                      prop: getComputedStyle(sl[0]).transitionProperty};
            }""")
            eq("%s stage 已初始化" % name, d["init"], True)
            eq("%s 是 fade 效果" % name, d["fade"], True)
            eq("%s 5 张 slide" % name, d["n"], 5)
            eq("%s 首屏 active = 0" % name, d["active"], 0)
            eq("%s 只有 active 不透明" % name, d["op"], ["1", "0", "0", "0", "0"])
            # 真正的结构判据：wrapper 的 height:100% 传下来了没有
            eq("%s slide 矩形 == stage 矩形" % name, d["slide"], d["stage"])
            eq("%s 第 5 张 slide 也铺满 stage" % name, d["last"], d["stage"])
            eq("%s slide cursor = grab" % name, d["cursor"], "grab")
            eq("%s 交叉淡入用的是本站曲线" % name, d["ease"], "cubic-bezier(0.33, 1, 0.68, 1)")
            eq("%s slide 过渡的是 opacity" % name, d["prop"], "opacity")
            pg.close()

        pg = page(b, "pdp.html", 1440)
        idx = lambda: pg.evaluate("() => document.querySelector('[data-gallery-track]').swiper.activeIndex")
        thumbs = lambda: pg.evaluate(
            """() => [...document.querySelectorAll('[data-gallery-go]')]
                     .map(e => e.classList.contains('is-active') && e.getAttribute('aria-current') === 'true')""")
        pg.click('[data-gallery-go="2"]'); pg.wait_for_timeout(450)
        eq("点缩略图 3 → 第 3 张", idx(), 2)
        eq("缩略图 3 变成 active", thumbs(), [False, False, True, False, False])
        # 淡出时长必须还是 0.3s —— Swiper 把它写成行内样式，CSS 里读不到
        pg.click('[data-gallery-go="0"]')
        dur = pg.evaluate("""() => getComputedStyle(
            document.querySelector('[data-gallery-track] .swiper-slide')).transitionDuration""")
        eq("换片时的淡入时长仍是 0.3s", dur, "0.3s")
        pg.wait_for_timeout(450)

        box = pg.locator("[data-gallery-track]").bounding_box()
        cx, cy = box["x"] + box["width"] * 0.7, box["y"] + box["height"] / 2

        def drag(dx, dy=0, steps=12):
            pg.mouse.move(cx, cy)
            pg.mouse.down()
            pg.mouse.move(cx + dx, cy + dy, steps=steps)
            pg.mouse.up()
            pg.wait_for_timeout(450)

        eq("拖动前在第 1 张", idx(), 0)
        drag(-200); eq("左拖 200 → 前进一张", idx(), 1)
        drag(-400); eq("左拖 400 也只前进一张（不按距离多跳）", idx(), 2)
        drag(-10);  eq("拖 10px 不算滑动", idx(), 2)
        drag(0, -200); eq("竖着拖不换片（那是在滚页面）", idx(), 2)
        drag(200); eq("右拖 → 退一张", idx(), 1)
        drag(200); eq("再右拖 → 回第 1 张", idx(), 0)
        drag(200); eq("已在第 1 张，右拖不循环到最后", idx(), 0)
        for _ in range(6):
            drag(-200)
        eq("连拖到底停在第 5 张，不循环", idx(), 4)

        pg.evaluate("() => document.querySelector('[data-gallery-track]').focus()")
        pg.keyboard.press("ArrowLeft"); pg.wait_for_timeout(400)
        eq("stage 有焦点时 ArrowLeft 退一张", idx(), 3)
        pg.keyboard.press("ArrowRight"); pg.wait_for_timeout(400)
        eq("stage 有焦点时 ArrowRight 进一张", idx(), 4)
        # Swiper 自带的 keyboard 模块挂在 document 上，会抢走整页的方向键
        before = idx()
        # ⚠ document.body.focus() 对没有 tabindex 的 body 是空操作，焦点会留在
        # stage 上，下面两条就变成在验「焦点仍在 stage」——先 blur 再断言前提。
        pg.evaluate("() => document.activeElement && document.activeElement.blur()")
        ok_if("测「焦点不在 stage」之前焦点确实已经移开",
              pg.evaluate("() => document.activeElement !== document.querySelector('[data-gallery-track]')"))
        y0 = pg.evaluate("() => window.scrollY")
        pg.keyboard.press("ArrowDown"); pg.wait_for_timeout(350)
        ok_if("焦点不在 stage 上时方向键仍然滚页面",
              pg.evaluate("() => window.scrollY") > y0)
        pg.keyboard.press("ArrowLeft"); pg.wait_for_timeout(350)
        eq("焦点不在 stage 上时 ArrowLeft 不换片", idx(), before)
        pg.close()

        # ===== 4. 弹窗关闭时内容不许横移 ====================================
        PANEL = """(sel) => {
          const p = document.querySelector(sel);
          const b = p.getBoundingClientRect();
          return {x: +b.x.toFixed(2), w: +b.width.toFixed(2),
                  op: getComputedStyle(p).opacity,
                  locked: document.documentElement.classList.contains('is-modal-open'),
                  clientW: document.documentElement.clientWidth};
        }"""
        for name, mid, panel, mid_ms, done_ms in (
                ("index.html", "reel-video", ".gb-rv-panel", 120, 700),
                ("index.html", "nutritional-label", ".gb-nl-panel", 250, 900),
                ("pdp.html", "nutritional-label", ".gb-nl-panel", 250, 900)):
            pg = page(b, name, 1440)
            gap = pg.evaluate("() => window.innerWidth - document.documentElement.clientWidth")
            if gap <= 0:
                print("ABORT %s: no real scrollbar (gap=%s) — every assertion below "
                      "would pass on a broken build" % (name, gap))
                sys.exit(2)
            tag = "%s/%s" % (name.split(".")[0], mid)
            pg.evaluate("(m) => document.querySelector('[data-modal=\"' + m + '\"]').click()", mid)
            pg.wait_for_timeout(700)
            a = pg.evaluate(PANEL, panel)
            eq("%s 打开后已上锁" % tag, a["locked"], True)
            eq("%s 打开后 panel 可见" % tag, a["op"], "1")
            pg.evaluate("() => document.querySelector('[data-modal-close]').click()")
            pg.wait_for_timeout(mid_ms)
            m = pg.evaluate(PANEL, panel)
            # liveness：淡出中途 panel 必须仍然看得见，否则量的是个隐形元素
            ok_if("%s 淡出中途 panel 仍可见（判据前提）" % tag,
                  float(m["op"]) > 0.05, "opacity=%s" % m["op"])
            eq("%s 淡出中途 panel 没有横移" % tag, m["x"], a["x"], tol=0.05)
            eq("%s 淡出中途视口宽度没变" % tag, m["clientW"], a["clientW"])
            pg.wait_for_timeout(done_ms)
            f = pg.evaluate(PANEL, panel)
            # 反向断言：锁必须真的解开，否则「没位移」可以靠永不解锁作弊
            eq("%s 淡出结束后已解锁" % tag, f["locked"], False)
            eq("%s 解锁后滚动条回来了" % tag, f["clientW"], a["clientW"] - gap)
            eq("%s 解锁时 panel 已经看不见" % tag, f["op"], "0")
            pg.close()

        # 淡出中途重新打开：那次关闭挂起的定时器不许把锁解掉
        pg = page(b, "index.html", 1440)
        pg.evaluate("() => document.querySelector('[data-modal=\"reel-video\"]').click()")
        pg.wait_for_timeout(500)
        pg.evaluate("() => document.querySelector('.gb-rv-panel__close').click()")
        pg.wait_for_timeout(80)
        pg.evaluate("() => document.querySelector('[data-modal=\"reel-video\"]').click()")
        pg.wait_for_timeout(600)
        eq("淡出中途重新打开后仍然锁着",
           pg.evaluate("() => document.documentElement.classList.contains('is-modal-open')"), True)
        pg.close()

        # ===== 5. .gb-rv-panel__video hover =================================
        pg = page(b, "index.html", 1440)
        pg.evaluate("() => document.querySelector('[data-modal=\"reel-video\"]').click()")
        pg.wait_for_timeout(600)
        v = ".gb-rv-panel__video"
        eq("rv video 静止色", pg.evaluate(CS, [v, "color"]), INK)
        d = pg.evaluate(CS, [v, "transitionDuration"])
        ok_if("rv video 有过渡", d not in ("0s", "0s, 0s", None), str(d))
        pg.hover(v)
        pg.wait_for_timeout(400)
        eq("rv video hover 后变色", pg.evaluate(CS, [v, "color"]), GREEN)
        # 读 svg 里那条 path 真正渲染出来的 fill，不只是父元素的 color：需求写的是
        # 「hover svg 需要变色」。glyph 用 fill="currentColor"，底板 rect 是写死的
        # white —— 白底板 + 变色三角是有意的，两条一起钉住才说明白。
        eq("rv video hover 后 svg 三角真的变色",
           pg.evaluate("""() => getComputedStyle(
             document.querySelector('.gb-rv-panel__video svg path')).fill"""), GREEN)
        eq("rv video 的白色底板不跟着变",
           pg.evaluate("""() => getComputedStyle(
             document.querySelector('.gb-rv-panel__video svg rect')).fill"""), WHITE)
        pg.close()

        # ===== 6. 按钮 hover ================================================
        pg = page(b, "science.html", 1440)
        band = pg.evaluate("""() => getComputedStyle(
            document.querySelector('.gb-footer-cta__btn').closest('.gb-footer-cta')).backgroundColor""")
        eq("footer CTA 底色仍是 lime（下面这条 hover 的前提）", band, LIME)
        eq("footer CTA 按钮静止底色", pg.evaluate(CS, [".gb-footer-cta__btn", "backgroundColor"]), GREEN)
        pg.hover(".gb-footer-cta__btn")
        pg.wait_for_timeout(400)
        # 需求方第五十轮撤回了「照抄 --primary」：这颗按钮坐在 lime 底板上，翻成
        # lime 会和底板同色。恢复成翻白底。
        eq("footer CTA hover 底色翻白（不是 --primary 的 lime）",
           pg.evaluate(CS, [".gb-footer-cta__btn", "backgroundColor"]), WHITE)
        eq("footer CTA hover 文字色", pg.evaluate(CS, [".gb-footer-cta__btn", "color"]), GREEN)
        eq("footer CTA hover 边框也翻白",
           pg.evaluate(CS, [".gb-footer-cta__btn", "borderTopColor"]), WHITE)
        # header 上那颗 --primary 必须还是原样，需求只说照抄它
        pg.hover(".gb-header__cta")
        pg.wait_for_timeout(400)
        eq("header CTA hover 未受影响", pg.evaluate(CS, [".gb-header__cta", "backgroundColor"]), LIME)

        eq("logo 静止 opacity", pg.evaluate(CS, [".gb-header__logo", "opacity"]), "1")
        eq("logo 没有 transition 了",
           pg.evaluate(CS, [".gb-header__logo", "transitionDuration"]), "0s")
        pg.hover(".gb-header__logo")
        pg.wait_for_timeout(400)
        eq("logo hover 后 opacity 不变", pg.evaluate(CS, [".gb-header__logo", "opacity"]), "1")
        pg.close()

        # ===== 7a. highlight card 文字居中 ==================================
        for w in (1440, 1281, 1024, 768, 767, 390):
            pg = page(b, "index.html", w)
            d = pg.evaluate("""() => {
              const out = [];
              document.querySelectorAll('.gb-highlight-card__text').forEach(t => {
                const b = t.getBoundingClientRect();
                const p = t.parentElement.getBoundingClientRect();
                const cs = getComputedStyle(t.parentElement);
                const left = b.left - (p.left + parseFloat(cs.paddingLeft));
                const right = (p.right - parseFloat(cs.paddingRight)) - b.right;
                out.push([+left.toFixed(2), +right.toFixed(2)]);
              });
              return out;
            }""")
            ok_if("%d highlight 文字块共 3 段" % w, len(d) == 3, str(len(d)))
            for i, (l, r) in enumerate(d):
                eq("%d highlight 文字块 #%d 左右留白相等" % (w, i), l, r, tol=0.6)
            pg.close()

        # ===== 7b. 产品图 sticky：每一页，不只 PDP =========================
        for name, w, sticky in [(n, w, st)
                                for n in ("pdp.html", "index.html", "reviews.html",
                                          "our-story.html", "how-gumi-works.html")
                                for w, st in ((1440, True), (1281, True), (1280, True),
                                              (1024, True), (768, True),
                                              (767, False), (390, False))]:
            pg = page(b, name, w)
            d = pg.evaluate("""() => {
              const m = document.querySelector('.gb-product__media');
              const cs = getComputedStyle(m);
              return {pos: cs.position, top: cs.top,
                      mediaX: m.getBoundingClientRect().x,
                      infoX: document.querySelector('.gb-product__info').getBoundingClientRect().x,
                      head: parseFloat(getComputedStyle(document.querySelector('.gb-header__bar')).height)};
            }""")
            eq("%s@%d media position" % (name, w), d["pos"], "sticky" if sticky else "static")
            # 只在两栏并排时才有「左右」可言：767 以下是上下堆叠的
            if sticky:
                ok_if("%s@%d 图在左、信息在右" % (name, w), d["mediaX"] < d["infoX"],
                      "media %.0f / info %.0f" % (d["mediaX"], d["infoX"]))
            pinned = d["pos"] == "sticky"
            if sticky and pinned:
                eq("%s@%d media top = 表头高 + 24" % (name, w), px(d["top"]), d["head"] + 24, tol=0.6)
            # 判据是「滚动之后还在不在视口顶」，不是「CSS 写了 sticky」
            pg.evaluate("""() => window.scrollTo(0, document.querySelector('.gb-product__inner')
                                                     .getBoundingClientRect().top + window.scrollY + 400)""")
            pg.wait_for_timeout(350)
            t = pg.evaluate("() => document.querySelector('.gb-product__media').getBoundingClientRect().top")
            if not sticky:
                ok_if("%s@%d 滚动后 media 跟着滚走" % (name, w), t < -100, "top=%.1f" % t)
            elif pinned:
                eq("%s@%d 滚动后 media 钉在偏移位置" % (name, w), t, px(d["top"]), tol=1.5)
            else:
                # position 那条已经记下了；这里不要再抛 ValueError 把报告埋掉
                FAILS.append("%s@%d 滚动后 media 没钉住（position 不是 sticky，top=%.1f）" % (name, w, t))
            pg.close()

        # ===== 8. science 数字：桌面板值不动，手机端第五十三轮改回 36/40 =====
        # 第四十九轮把手机端拉回板值 56/44；第五十三轮需求方再次反转，两组卡的
        # 手机档一起回到 324:58044 的 36/40/-1%。桌面档一个字都不许动，所以这里
        # 按档分别钉，并且额外钉住 768-1280 的斜坡（没有斜坡就会 767/768 跳 20px）。
        TIER = {1440: (56, 44, "normal"), 1281: (56, 44, "normal"),
                767: (36, 40, "-0.36px"), 575: (36, 40, "-0.36px"), 390: (36, 40, "-0.36px")}
        ramp = {}
        for w in (1440, 1281, 1024, 768, 767, 575, 390):
            pg = page(b, "science.html", w)
            d = pg.evaluate("""() => {
              const g = s => { const e = document.querySelector(s); const c = getComputedStyle(e);
                return [parseFloat(c.fontSize), parseFloat(c.lineHeight), c.letterSpacing]; };
              return {stat: g('.gb-science-card:not(.gb-science-card--nutrient) .gb-science-card__value'),
                      nut:  g('.gb-science-card--nutrient .gb-science-card__value')};
            }""")
            ramp[w] = (d["stat"][0], d["nut"][0])
            if w in TIER:
                fs, lh, ls = TIER[w]
                eq("%d 95%% 卡字号 %d" % (w, fs), d["stat"][0], fs, tol=0.05)
                eq("%d 95%% 卡行高 %d" % (w, lh), d["stat"][1], lh, tol=0.05)
                eq("%d 95%% 卡字距" % w, d["stat"][2], ls)
                # 两组卡共用一条规则，规格必须一致
                eq("%d 50%% 卡（nutrient）与 95%% 同规格 %d" % (w, fs), d["nut"][0], fs, tol=0.05)
                eq("%d 50%% 卡行高 %d" % (w, lh), d["nut"][1], lh, tol=0.05)
                eq("%d 50%% 卡字距" % w, d["nut"][2], ls)
            pg.close()
        # 斜坡：768-1280 必须落在两端之间且单调，否则接缝会跳
        for w in (768, 1024):
            for i, name in ((0, "95%%"), (1, "50%%")):
                ok_if("%d %s 卡字号落在 36-56 之间" % (w, name),
                      36 - 0.05 <= ramp[w][i] <= 56 + 0.05,
                      "got %.2f" % ramp[w][i])
        ok_if("768<1024<1281 字号单调不倒挂",
              ramp[768][0] <= ramp[1024][0] <= ramp[1281][0],
              "768=%.2f 1024=%.2f 1281=%.2f" % (ramp[768][0], ramp[1024][0], ramp[1281][0]))
        ok_if("767/768 接缝连续（<=1.2px）", abs(ramp[768][0] - ramp[767][0]) <= 1.2,
              "767=%.2f 768=%.2f" % (ramp[767][0], ramp[768][0]))
        # 首页那三张 95% 也一起量：需求点名的是这个类，两页都挂了它
        pg = page(b, "index.html", 390)
        eq("390 首页 95%% 卡字号 36",
           px(pg.evaluate(CS, [".gb-science-card__value", "fontSize"])), 36, tol=0.05)
        pg.close()


        # ===== 9. 其余轮播也全部跑在 Swiper 上 =============================
        # 判据不是「有没有 swiper-initialized」——那对一个塌成 0 高、或者右边空
        # 一大片的轨道照样成立。真正要钉的是几何：卡片间距 == CSS 里声明的
        # column-gap，且**轨道两侧都不许留空**（Swiper 的 loop 是重排现有 slide，
        # 5 张卡填不满 1440 的 4.3 个位置，右边会空 232px —— 本轮就是踩了这个才
        # 改用「居中 + 中间张起步 + rewind」）。
        RAIL = """(sel) => {
          const t = document.querySelector(sel);
          if (!t) return null;
          const sw = t.swiper;
          const sl = [...t.querySelectorAll('.swiper-slide')];
          const W = document.documentElement.clientWidth;
          const b = sl.map(e => e.getBoundingClientRect());
          return {live: !!sw, n: sl.length,
                  gap: getComputedStyle(t).columnGap,
                  space: sw ? sw.params.spaceBetween : null,
                  rewind: sw ? sw.params.rewind : null,
                  loop: sw ? sw.params.loop : null,
                  active: sw ? sw.activeIndex : null,
                  real: sw ? sw.realIndex : null,
                  wrap: getComputedStyle(t.querySelector('.swiper-wrapper')).display,
                  xs: b.map(r => +r.x.toFixed(1)),
                  // ⚠ sorted by x, not by DOM order: Swiper's loop reorders the
                  // slides, so b[1] is not necessarily the one to the right of b[0].
                  pitch: b.length > 1
                    ? +(b.map(r => r.x).sort((p, q) => p - q)[1]
                        - b.map(r => r.x).sort((p, q) => p - q)[0]).toFixed(2)
                    : null,
                  leftGap: +Math.max(0, Math.min(...b.map(r => r.left))).toFixed(1),
                  rightGap: +Math.max(0, W - Math.max(...b.map(r => r.right))).toFixed(1),
                  h: +b[0].height.toFixed(1)};
        }"""
        for name in ("index.html", "pdp.html", "our-story.html", "how-gumi-works.html"):
            for w in (1440, 1280, 1024, 768, 767, 390):
                pg = page(b, name, w)
                d = pg.evaluate(RAIL, ".gb-reels")
                tag = "%s@%d reels" % (name.split(".")[0], w)
                eq("%s 跑在 Swiper 上" % tag, d["live"], True)
                # 第五十二轮由需求方裁决（待决 AG）：reels 要无缝无限循环，
                # 代价是必须加卡 —— Swiper 11 的 loop 是重排现有 slide，
                # 卡数不到可见张数的两倍就会在一侧留空。5 → 10 张占位卡，
                # 改跑 loop，rewind 随之关掉。无缝性判在 r53check §2。
                eq("%s 10 张卡（loop 的下限：可见 4.3 张的两倍以上）" % tag, d["n"], 10)
                eq("%s 用 Swiper 的 loop" % tag, d["loop"], True)
                eq("%s 不再用 rewind（loop 永远走不到死头）" % tag, d["rewind"], False)
                eq("%s 从第一张起步（loop 下无「整组居中」可言）" % tag, d["real"], 0)
                # spaceBetween 必须等于 SCSS 里声明的那个数，不是写死在 JS 里的
                eq("%s spaceBetween == CSS 的 column-gap" % tag, d["space"], px(d["gap"]), tol=0.05)
                eq("%s 卡片步距 == 卡宽 + gap" % tag,
                   d["pitch"], (228 if w <= 767 else 304) + px(d["gap"]), tol=0.6)
                eq("%s 轨道左边没有空档" % tag, d["leftGap"], 0, tol=0.6)
                eq("%s 轨道右边没有空档" % tag, d["rightGap"], 0, tol=0.6)
                eq("%s 无横向溢出" % tag,
                   pg.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth"), 0)
                pg.close()

        # expert 轨：≤991 是 Swiper，≥992 Swiper 必须被销毁、wrapper 变回三列网格
        for w, live in ((1440, False), (1281, False), (1024, False), (992, False),
                        (991, True), (768, True), (767, True), (390, True)):
            pg = page(b, "reviews.html", w)
            d = pg.evaluate(RAIL, ".gb-expert__cards")
            nav = pg.evaluate(CS, [".gb-expert__nav", "display"])
            tag = "expert@%d" % w
            eq("%s Swiper 是否在跑" % tag, d["live"], live)
            eq("%s wrapper 的 display" % tag, d["wrap"], "flex" if live else "grid")
            eq("%s 三张卡" % tag, d["n"], 3)
            eq("%s 导航按钮" % tag, nav, "flex" if live else "none")
            if live:
                eq("%s spaceBetween == CSS 的 column-gap" % tag, d["space"], px(d["gap"]), tol=0.05)
                eq("%s 卡片步距 == 305 + gap" % tag, d["pitch"], 305 + px(d["gap"]), tol=0.6)
                # 「右边不许留空」只在卡片放不下时才是不变量。991 处 3 x 305 + 2 x 19.5
                # = 954 装得进 976 的轨道，剩 22 —— 基线也是这样，不是空档。
                if 305 * d["n"] + px(d["gap"]) * (d["n"] - 1) > w - 15:
                    eq("%s 轨道右边没有空档" % tag, d["rightGap"], 0, tol=0.6)
                else:
                    eq("%s 卡片装得下时靠左排齐" % tag, d["xs"][0], 0, tol=0.6)
                # 767 以下居中，所以左右都露边；768 起靠左排，左边贴齐
                eq("%s 起步位置" % tag, d["active"], 1 if w <= 767 else 0)
            pg.close()

        # 交互：箭头走一张、rewind 不会卡死、拖拽不会误开弹窗
        pg = page(b, "how-gumi-works.html", 1440)
        # 第五十二轮起 reels 跑 loop：realIndex 才是「第几张」，activeIndex 会被
        # 重排带偏。没有末尾可言，所以原来那条「走到末尾绕回第一张」换成
        # 「走满一圈回到起点」—— 无缝的定义就是这个。
        rid = lambda: pg.evaluate("() => document.querySelector('.gb-reels').swiper.realIndex")
        eq("reels 首屏停在第一张", rid(), 0)
        pg.click("[data-slider-next]"); pg.wait_for_timeout(600)
        eq("箭头前进一张", rid(), 1)
        # ⚠ 间隔必须大于 Swiper 的 speed（400ms），否则动画途中的点击会被吞掉，
        # 走的张数少于点的次数 —— 260ms 时实测只走到 6。
        for _ in range(9):
            pg.click("[data-slider-next]"); pg.wait_for_timeout(500)
        eq("走满一圈回到起点（10 张，无缝）", rid(), 0)
        ok_if("loop 的轨道两个箭头都不置灰",
              pg.evaluate("""() => ![...document.querySelectorAll('[data-slider-prev],[data-slider-next]')]
                                     .some(e => e.disabled)"""))
        box = pg.locator(".gb-reels").bounding_box()
        cx, cy = box["x"] + box["width"] / 2, box["y"] + box["height"] / 2
        pg.evaluate("() => document.querySelector('.gb-reels').focus()")
        before = rid()
        pg.keyboard.press("ArrowRight"); pg.wait_for_timeout(700)
        ok_if("轨道有焦点时方向键能翻", rid() != before, "still %s" % before)
        # 点一张卡要能开 reel 弹窗；拖一下则不许开
        pg.click(".gb-reel.swiper-slide-active"); pg.wait_for_timeout(700)
        eq("点卡片打开 reel 弹窗",
           pg.evaluate("() => document.querySelector('.gb-rv-modal').classList.contains('is-open')"), True)
        pg.evaluate("() => document.querySelector('.gb-rv-panel__close').click()")
        pg.wait_for_timeout(800)
        pg.mouse.move(cx, cy); pg.mouse.down()
        pg.mouse.move(cx - 300, cy, steps=14); pg.mouse.up()
        pg.wait_for_timeout(800)
        eq("拖拽结束不许把弹窗一起点开",
           pg.evaluate("() => document.querySelector('.gb-rv-modal').classList.contains('is-open')"), False)
        pg.close()

        b.close()

    print("=" * 72)
    if FAILS:
        print("FAIL — %d / %d 条断言" % (len(FAILS), CHECKED[0]))
        for f in FAILS:
            print("  x", f)
    else:
        print("r50check: %d assertions, 0 failed" % CHECKED[0])
    print("=" * 72)
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
