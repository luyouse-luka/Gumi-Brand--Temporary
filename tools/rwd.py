#!/usr/bin/env python3
"""窄屏体检 —— 只测「会不会坏」，不截图，跑一遍 11 页 × 10 档不到两分钟。

    python3 tools/rwd.py                 # 全站全宽度
    python3 tools/rwd.py index.html 768  # 指定

三条判据，都不会误报：
  1. 横向溢出   documentElement.scrollWidth > clientWidth
  2. 内容被裁   文字元素越出「最近一个真的会裁的祖先」的可视框；收起的抽屉与
                手风琴已排除（它们本来就该看不见）
  3. 滚轮黑洞   任何自己能纵向滚的元素都必须带 data-lenis-prevent，否则
                Lenis 会把滚轮全吃掉、那个容器再也滚不动。这条**必须逐视口跑**：
                thumbs 只在桌面可滚、header__panel 只在手机可滚，单一视口验不全

shoot.py 那份带截图和 wowo 检查，慢十倍，收尾再跑。这份是改一轮看一眼用的。
"""
import os, sys, glob
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = os.path.expanduser("~/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome")
# 每个断点边界的两侧各取一档，否则交界处的回归漏检
# r29 起新增 767/768（narrow↔tablet）与 991/992（mid，卡片列数）
WIDTHS = [360, 390, 575, 576, 767, 768, 991, 992, 1024, 1200, 1280, 1281, 1440, 1920]

# 只留两条**不会误报**的判据。别再往里加「元素越过视口边」那类 ——
# 抽屉停在 -100%、跑马灯轨道比视口宽、滚动容器里的卡片，全都是有意越界，
# 上一版因此在 95 个组合里报了满屏假阳性，真信号一条没有。
PROBE = """() => {
  const de = document.documentElement, W = de.clientWidth;
  const out = { over: null, clipped: [] };
  if (de.scrollWidth > W + 1) out.over = [de.scrollWidth, W];
  const name = el => el.tagName.toLowerCase() + '.' + (el.className||'').toString().trim().split(/\\s+/)[0];

  // 内容被祖先裁掉：找最近一个真的会裁的祖先，比它的可视框
  const clipperOf = el => {
    for (let n = el.parentElement; n && n !== de; n = n.parentElement) {
      const c = getComputedStyle(n);
      // A horizontal rail nearer than any clipper means the content is reachable
      // by swiping: its off-screen cards are the point of the rail, not a defect
      // (.gb-expert__cards, .gb-reels). Order matters — the clipper test below
      // still wins when the hidden box is the closer of the two. Deliberately
      // only the x axis: overflow-x:hidden forces the other axis to auto, so
      // testing y here would excuse a genuinely clipped box that happens to
      // overflow vertically by a few pixels.
      if (/auto|scroll/.test(c.overflowX) && n.scrollWidth > n.clientWidth + 1) return null;
      // 第五十轮起横轨跑在 Swiper 上：它用 transform 平移而不是滚动，所以
      // scrollWidth 不再溢出，上面那条认不出它。.swiper 的 overflow:hidden 就是
      // 轨道的取景框，框外那几张卡是滑进来的内容，不是缺陷 —— 与上面同一条豁免，
      // 只是换了实现。豁免只认容器本身带 .swiper，卡片内部再被裁照报不误。
      if (n.classList.contains('swiper')) return null;
      if (/hidden|clip/.test(c.overflowX) || /hidden|clip/.test(c.overflowY)) return n;
    }
    return null;
  };
  for (const el of document.querySelectorAll('body *')) {
    if (!el.firstChild || el.firstChild.nodeType !== 3) continue;   // 只看直接装文字的
    if (!el.textContent.trim()) continue;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || parseFloat(cs.opacity) === 0) continue;
    const cl = clipperOf(el);
    if (!cl) continue;
    const a = el.getBoundingClientRect(), b = cl.getBoundingClientRect();
    // 收起的抽屉（停在 -100%）和收起的手风琴（高度 0）本来就该看不见，
    // 不加这两条过滤，报表里 110 个组合全是它们，真信号一条也看不到
    if (b.width < 4 || b.height < 4) continue;
    if (b.right <= 0 || b.left >= W) continue;
    // 元素自己整个停在视口外（抽屉 translateX(-100%)）—— 判 clipper 拦不住它
    if (a.right <= 0 || a.left >= W) continue;
    // SVG 的 textPath 沿路径排字，boundingClientRect 本来就跟墨迹对不上
    if (el.ownerSVGElement || el.tagName === 'svg') continue;
    // .gb-line-mask 是逐行上滑入场的遮罩：揭示前内容 translateY(100%) 蹲在
    // overflow:hidden 框外本来就该看不见（opacity 仍是 1，上面那条挡不住它），
    // 不是溢出 bug。150ms 的探测时机也来不及等它滚入视口触发揭示。
    if (cl.classList.contains('gb-line-mask')) continue;
    const dx = Math.max(0, b.left - a.left, a.right - b.right);
    const dy = Math.max(0, b.top - a.top, a.bottom - b.bottom);
    if (dx > 2 || dy > 2)
      out.clipped.push([name(el), name(cl), Math.round(dx), Math.round(dy),
                        el.textContent.trim().slice(0, 24)]);
  }
  out.clipped = out.clipped.slice(0, 6);

  // 3) 可滚容器必须登记给 Lenis（名单在 assets/main.js 的 smoothScroll.PREVENT）
  out.unguarded = [];
  if (window.gumi && window.gumi.smoothScroll && window.gumi.smoothScroll.lenis) {
    for (const el of document.querySelectorAll('body *')) {
      const cs = getComputedStyle(el);
      const oy = cs.overflowY, ox = cs.overflowX;
      if (oy !== 'auto' && oy !== 'scroll') continue;
      if (el.scrollHeight <= el.clientHeight + 1) continue;   // 现在装得下，滚不起来
      // 横向轨道（只写了 overflow-x:auto）：按规范另一轴的 visible 会被强制算成
      // auto，于是它「纵向也能滚」几十像素 —— 那是副作用不是意图，
      // 滚轮压在轨道上本来就该滚页面。.gb-expert__cards 实测 sw 987>cw 390、
      // 纵向只多 26px，就是这一类。
      if ((ox === 'auto' || ox === 'scroll') && el.scrollWidth > el.clientWidth + 1) continue;
      if (el.closest('[data-lenis-prevent]')) continue;
      out.unguarded.push(name(el));
    }
  }
  return out;
}"""


def run(pages, widths):
    bad = 0
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=CHROME)
        for w in widths:
            pg = br.new_page(viewport={"width": w, "height": 900})
            pg.add_init_script("Math.random = function () { return 0.5; };")
            for f in pages:
                pg.goto("file://" + os.path.join(ROOT, f))
                pg.evaluate("() => document.fonts.ready")
                pg.wait_for_timeout(150)
                r = pg.evaluate(PROBE)
                msg = ""
                if r["over"]:
                    msg += f"  横向溢出 {r['over'][0]}>{r['over'][1]}"
                if r["clipped"]:
                    msg += f"  被裁×{len(r['clipped'])} {r['clipped'][:2]}"
                if r.get("unguarded"):
                    msg += f"  滚轮黑洞 {sorted(set(r['unguarded']))}"
                if msg:
                    bad += 1
                    print(f"{os.path.splitext(f)[0]:20} {w:5}{msg}")
            pg.close()
        br.close()
    print(f"\n{'✅ 全绿' if bad == 0 else f'❌ {bad} 个页面×宽度组合有问题'}")
    return bad


if __name__ == "__main__":
    args = sys.argv[1:]
    pages = [a for a in args if a.endswith(".html")] or \
        [os.path.basename(f) for f in sorted(glob.glob(os.path.join(ROOT, "*.html")))
         if not f.endswith("font-check.html")]
    widths = [int(a) for a in args if a.isdigit()] or WIDTHS
    sys.exit(1 if run(pages, widths) else 0)
