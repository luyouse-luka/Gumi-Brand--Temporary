#!/usr/bin/env python3
"""CTA 板的圆瓣几何判据 —— 从渲染像素里量，不读 CSS。

    python3 tools/platecheck.py                 # 默认 14 档
    python3 tools/platecheck.py 390,767,768,1440

为什么必须量像素：这块板的病就是「声明看着没错、画出来变形」。读回
`border-image` 的值只能证明规则存在，证明不了圆瓣还是不是圆的。这里截图、按颜色
抠出板的轮廓、逐列（逐行）取边缘位置，再验四条与实现无关的不变量。

设计源（Figma 导出的两条 fillGeometry 路径上读下来的）：

  1280 x 392.957     r 58.8848  px 89.4023  py 91.7291   顶 14 瓣 / 侧 4 瓣
  350.852 x 507.512  r 39.9189  px 67.7535  py 61.0963   顶  5 瓣 / 侧 8 瓣

轮廓的构造是「半径固定的圆瓣，圆心在距边 r 的线上按固定间距排开，与内矩形取并集」。
九宫格 border-image 把四角按原尺寸画死、四边用 `round` 平铺一个瓣周期，于是**瓣数**
跟着盒子走，而不是**瓣形**跟着盒子走。

判据（刻意不预测浏览器的取整 —— 实测 Chrome 的 `round` 落点与 round()/ceil() 都对不上，
1100 处 3.43 个周期它取了 4 个；把浏览器的实现细节写进断言，改版就会误报）：

  1. 谷深与解析式相符。这是**瓣形**的判据，且与平铺缩放无关：瓣被缩放 s 时
     间距也是 p·s，两者在 d = r - r·sqrt(1 - (p/2r)^2) 里约掉。旧的拉伸实现会改变它。
  2. 间距均匀（相邻尖点间距的极差 < 2px）—— 拉伸会带出梯度。
  3. 缩放 s = 实测间距/设计间距 落在 ±20% 内，且 span/间距 接近整数（说明确实是整数
     次平铺）。±20% 是 `round` 在周期数只有 3–4 个时的固有粒度，不是实现缺陷；
     实测全档区间是 [0.86, 1.07]。⚠ 旧实现在这一项上是 0.44 与 2.07。
  4. 两块设计稿自己的宽度必须复现稿上的瓣数（390 → 顶 5 / 侧 8；1440 → 顶 14 / 侧 4）。

活性自检：把 `.gb-cta-band__plate` 改回 `mask-size: 100% 100%` 的整轮廓，
第 1、3、4 条应立刻报红。
"""
import io
import math
import os
import sys

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = os.path.expanduser("~/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome")
SETTLE = (".wowo,.gb-float-art,[data-line-reveal],.gb-line-mask__inner,.gb-ink-halo{"
          "opacity:1!important;transform:none!important;animation:none!important}")
PAGE = "our-story.html"
GREEN = (0x00, 0x56, 0x35)          # $c-green
DPR = 2
TOL_S = 0.20

PC = dict(r=58.8848, px=89.4023, py=91.7291)
MOB = dict(r=39.9189, px=67.7535, py=61.0963)
BP_NARROW = 767

FAILS = []


def geom(vw):
    return MOB if vw <= BP_NARROW else PC


def valley_depth(r, p):
    return r - math.sqrt(max(0.0, r * r - (p / 2) ** 2))


def shoot(widths):
    out = {}
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME)
        for w in widths:
            pg = b.new_page(viewport={"width": w, "height": 1400}, device_scale_factor=DPR)
            pg.goto("file://" + os.path.join(ROOT, PAGE))
            pg.add_style_tag(content=SETTLE)
            pg.evaluate("() => document.fonts.ready")
            pg.wait_for_timeout(450)
            el = pg.query_selector(".gb-cta-band__plate")
            el.scroll_into_view_if_needed()
            pg.wait_for_timeout(250)
            box = el.bounding_box()
            png = pg.screenshot(clip={"x": box["x"], "y": box["y"],
                                      "width": box["width"], "height": box["height"]})
            css = pg.evaluate("""() => { const e = document.querySelector('.gb-cta-band__plate');
                const s = getComputedStyle(e);
                return {rep: s.borderImageRepeat, mask: s.webkitMaskImage || s.maskImage,
                        bg: s.backgroundImage}; }""")
            out[w] = (png, box, css)
            pg.close()
        b.close()
    return out


def edges(png):
    im = Image.open(io.BytesIO(png)).convert("RGB")
    w, h = im.size
    px = im.load()

    def green(x, y):
        c = px[x, y]
        return (abs(c[0] - GREEN[0]) < 40 and abs(c[1] - GREEN[1]) < 40
                and abs(c[2] - GREEN[2]) < 40)

    top = []
    for x in range(w):
        y = 0
        while y < h and not green(x, y):
            y += 1
        top.append(y)
    left = []
    for y in range(h):
        x = 0
        while x < w and not green(x, y):
            x += 1
        left.append(x)
    return top, left, w, h


def analyse(prof, n):
    """尖点位置（CSS px）、间距列表、谷深"""
    base = min(prof)
    apex, i = [], 0
    while i < n:
        if prof[i] <= base + 1:
            j = i
            while j + 1 < n and prof[j + 1] <= base + 1:
                j += 1
            apex.append((i + j) / 2.0 / DPR)
            i = j + 1
        else:
            i += 1
    if len(apex) < 2:
        return apex, [], None
    pitches = [apex[k + 1] - apex[k] for k in range(len(apex) - 1)]
    valleys = []
    for k in range(len(apex) - 1):
        a, b_ = int(apex[k] * DPR), int(apex[k + 1] * DPR)
        if b_ - a > 3:
            valleys.append((max(prof[a:b_]) - base) / DPR)
    return apex, pitches, (sum(valleys) / len(valleys) if valleys else None)


def judge(tag, w, apex, pitches, valley, span, r, p):
    n = len(apex)
    if n < 2 or not pitches:
        FAILS.append("%d %s: 只找到 %d 个尖点" % (w, tag, n))
        return n, float("nan")
    pitch = sum(pitches) / len(pitches)
    d_pred = valley_depth(r, p)
    if valley is None or abs(valley - d_pred) > 1.5:
        FAILS.append("%d %s: 谷深 %.2f ≠ 解析值 %.2f —— 瓣形不对"
                     % (w, tag, valley or 0, d_pred))
    if max(pitches) - min(pitches) > 2.0:
        FAILS.append("%d %s: 间距不均匀，极差 %.2f（%s）"
                     % (w, tag, max(pitches) - min(pitches), [round(x, 1) for x in pitches]))
    s = pitch / p
    if abs(s - 1) > TOL_S:
        FAILS.append("%d %s: 缩放 s=%.3f 超出 ±%d%%" % (w, tag, s, TOL_S * 100))
    k = span / pitch
    if abs(k - round(k)) > 0.08:
        FAILS.append("%d %s: 边段不是整数次平铺（span/间距 = %.3f）" % (w, tag, k))
    return n, s


def main(widths):
    shots = shoot(widths)
    rows = []
    for w in widths:
        png, box, css = shots[w]
        top, left, pw, ph = edges(png)
        g = geom(w)
        r = g["r"]
        ha, hp, hv = analyse(top, pw)
        va, vp, vv = analyse(left, ph)
        nh, sh = judge("顶边", w, ha, hp, hv, box["width"] - 2 * r, r, g["px"])
        nv, sv = judge("侧边", w, va, vp, vv, box["height"] - 2 * r, r, g["py"])
        if css["rep"] != "round":
            FAILS.append("%d: border-image-repeat 是 %r，不是 round" % (w, css["rep"]))
        if css["mask"] not in (None, "none"):
            FAILS.append("%d: 板上还挂着 mask（%s）——旧的拉伸实现回来了" % (w, css["mask"][:40]))
        rows.append((w, box["width"], box["height"], nh, sh, hv, nv, sv, vv))
    print("%6s %11s %6s %8s %7s %6s %8s %7s" %
          ("视口", "板宽×高", "顶瓣", "顶缩放", "顶谷深", "侧瓣", "侧缩放", "侧谷深"))
    for w, bw, bh, nh, sh, hv, nv, sv, vv in rows:
        print("%6d %5.0f×%-5.0f %6d %8.3f %7.1f %6d %8.3f %7.1f"
              % (w, bw, bh, nh, sh, hv or 0, nv, sv, vv or 0))
    # 两块稿必须复现
    for vw, wt, ws in ((390, 5, 8), (1440, 14, 4)):
        for w, bw, bh, nh, sh, hv, nv, sv, vv in rows:
            if w != vw:
                continue
            if nh != wt:
                FAILS.append("%d: 顶边应是稿上的 %d 瓣，实测 %d" % (vw, wt, nh))
            if nv != ws:
                FAILS.append("%d: 侧边应是稿上的 %d 瓣，实测 %d" % (vw, ws, nv))
    print("=" * 78)
    if FAILS:
        print("FAIL — %d" % len(FAILS))
        for f in FAILS:
            print("  ✗", f)
    else:
        print("platecheck: 瓣形、间距、平铺、两块稿的瓣数全部符合")
    print("=" * 78)
    return 1 if FAILS else 0


if __name__ == "__main__":
    ws = [int(x) for x in sys.argv[1].split(",")] if len(sys.argv) > 1 else \
         [390, 500, 575, 700, 767, 768, 900, 1024, 1100, 1200, 1280, 1281, 1440, 1600]
    raise SystemExit(main(ws))
