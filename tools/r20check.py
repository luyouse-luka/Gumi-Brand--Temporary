#!/usr/bin/env python3
"""第二十轮 8 条任务的专项判据。每条都给可复核的数字，不靠肉眼。

    python3 tools/r20check.py

判据一律「与 Figma 节点数据比」，不与上一版产物比 —— 上一版本身就是错的。
设计侧的数字来源写在每段注释里，节点 JSON 在 figma/nodes/。
"""
import os, sys, json, math
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = os.path.expanduser("~/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome")
ok = lambda c: "\033[32m✓\033[0m" if c else "\033[31m✗\033[0m"
fails = []
def check(cond, label, detail=""):
    print(f"  {ok(cond)} {label}  {detail}")
    if not cond: fails.append(label)
def near(a, b, tol=0.6): return abs(a - b) <= tol

RECTS = """(sels) => {
  const o = {};
  for (const s of sels) {
    const e = [...document.querySelectorAll(s)].find(x => x.getClientRects().length);
    if (!e) { o[s] = null; continue; }
    const r = e.getBoundingClientRect();
    o[s] = { x: r.x + scrollX, y: r.y + scrollY, w: r.width, h: r.height };
  }
  return o;
}"""

def settle(pg):
    pg.wait_for_timeout(400)
    pg.evaluate("()=>{document.querySelectorAll('.wowo').forEach(e=>e.classList.add('animated'));}")
    for y in range(0, pg.evaluate("document.body.scrollHeight"), 400):
        pg.evaluate(f"window.scrollTo(0,{y})"); pg.wait_for_timeout(25)
    pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(700)

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME)
    pg = b.new_page(viewport={"width": 1440, "height": 1000}, device_scale_factor=1)
    pg.goto("file://" + os.path.join(ROOT, "index.html")); settle(pg)

    # ---- 1a. hero 按钮满宽（稿 332:16424 = 380 = 所在列整宽）--------------
    print("\n[1a] hero 按钮满宽")
    r = pg.evaluate(RECTS, ['.gb-hero__btn', '.gb-hero__cta'])
    check(near(r['.gb-hero__btn']['w'], r['.gb-hero__cta']['w']),
          "按钮宽 == .gb-hero__cta 宽", f"{r['.gb-hero__btn']['w']:.1f} / {r['.gb-hero__cta']['w']:.1f}")
    check(near(r['.gb-hero__btn']['w'], 380), "= 稿的 380", f"{r['.gb-hero__btn']['w']:.1f}")

    # ---- 1b. Trustpilot 星（稿 332:16402 = 77x14）-------------------------
    print("\n[1b] 公告条五颗星")
    s = pg.evaluate("""() => {
      const e = document.querySelector('.gb-announcement__stars');
      if (!e) return null;
      const r = e.getBoundingClientRect();
      const plate = getComputedStyle(e.querySelector('.gb-announcement__star-plate')).fill;
      const pt    = getComputedStyle(e.querySelector('.gb-announcement__star-pt')).fill;
      return { w: r.width, h: r.height, n: e.querySelectorAll('.gb-announcement__star-pt > path').length,
               plate, pt, inner: e.previousElementSibling.textContent.trim(),
               next: e.nextElementSibling.textContent.trim() };
    }""")
    check(s is not None, "星条存在")
    if s:
        check(near(s['w'], 77) and near(s['h'], 14), "77 x 14", f"{s['w']:.1f} x {s['h']:.1f}")
        check(s['n'] == 5, "五颗", str(s['n']))
        check(s['plate'] == 'rgb(181, 237, 97)', "方板 = $c-lime", s['plate'])
        check(s['pt'] == 'rgb(0, 86, 53)', "星形 = $c-green", s['pt'])
        check(s['inner'] == 'Excellent' and s['next'] == 'Truspilot', "夹在两段文案中间")

    # ---- 2. hero glow：环宽 = 稿的 26.2137（描边 CENTER）------------------
    # 332:16445 路径 439.066 宽 + 26.2137 描边 = 465.28；换算到 568.05 的槽位
    # = 81.9%。渲染时熊图整体旋转 7.92deg，所以量未旋转的 offsetWidth。
    print("\n[2] hero 光晕尺寸")
    g = pg.evaluate("""() => {
      const el = document.querySelector('.gb-hero__bear');
      const art = document.querySelector('.gb-hero__art');
      return { bearW: el.offsetWidth, bearH: el.offsetHeight, artW: art.offsetWidth,
               natW: el.naturalWidth, natH: el.naturalHeight, src: el.currentSrc.split('/').pop() };
    }""")
    print("     ", json.dumps(g))
    check(near(g['bearW'] / g['artW'] * 100, 82.04, 0.2),
          "熊图占槽位 82.04%（= 466.0 / 568.05，含 glow 描边）", f"{g['bearW']/g['artW']*100:.2f}%")
    check(near(g['natW'] / g['natH'], 466.0 / 758.5, 0.004),
          "资源比例 = 设计墨迹 466.0 : 758.5", f"{g['natW']}x{g['natH']} = {g['natW']/g['natH']:.4f}")

    # ---- 3. logo 轨道（稿 341:47385 行 96 / Logo 79.88 @ +8.06）-----------
    print("\n[3] logo 轨道")
    l = pg.evaluate(RECTS, ['.gb-logo-scroll__item', '.gb-logo-scroll__viewport'])
    pad = pg.evaluate("()=>getComputedStyle(document.querySelector('.gb-logo-scroll__viewport')).paddingTop")
    check(near(l['.gb-logo-scroll__item']['h'], 80), "槽位高 80", f"{l['.gb-logo-scroll__item']['h']:.1f}")
    check(pad == '8px', "viewport 上下内距 8px", pad)
    check(near(l['.gb-logo-scroll__viewport']['h'], 96), "行总高仍是 96（section 高度不变）",
          f"{l['.gb-logo-scroll__viewport']['h']:.1f}")

    # ---- 4. 弧形文字：椭圆 rx118.5261 / ry65.7047，框 278x29，head gap 48 --
    print("\n[4] ONE HANDFUL 弧度")
    a = pg.evaluate("""() => {
      const svg = document.querySelector('.gb-stats__arc');
      const path = svg.querySelector('path');
      const t = svg.querySelector('textPath');
      const r = svg.getBoundingClientRect();
      const bb = path.getBBox();
      return { w: r.width, h: r.height, vb: svg.getAttribute('viewBox'), d: path.getAttribute('d'),
               pathLen: path.getTotalLength(), textLen: t.getComputedTextLength(),
               sag: bb.height, chord: bb.width,
               fs: getComputedStyle(svg.querySelector('text')).fontSize };
    }""")
    print("     ", json.dumps({k: (round(v, 3) if isinstance(v, float) else v) for k, v in a.items()}))
    check(a['vb'] == '0 0 278 29', "viewBox = 稿的 Curved Text 框 278x29", a['vb'])
    check('118.5261 65.7047' in a['d'], "路径是椭圆 rx118.5261 / ry65.7047（不再是 A 338 338）")
    # 设计：半跨 85.5 处落差 20.2px（正圆 R338 只有 11）
    x = 85.5; rx, ry = 118.5261, 65.7047
    drop = ry * (1 - math.sqrt(1 - (x / rx) ** 2))
    check(near(drop, 20.2, 0.5), f"半跨 85.5 处落差 {drop:.2f}px（设计实测 20.2，旧实现 11.0）")
    check(a['pathLen'] > a['textLen'] * 1.05,
          "弧长 > 文字长 5% 以上（textPath 溢出部分不绘制）",
          f"{a['pathLen']:.1f} > {a['textLen']:.1f}")
    hd = pg.evaluate(RECTS, ['.gb-stats__arc', '.gb-stats__title'])
    gap = hd['.gb-stats__title']['y'] - (hd['.gb-stats__arc']['y'] + hd['.gb-stats__arc']['h'])
    check(near(gap, 48), "head gap = 稿的 48（框改回 29 后墨迹间距正好是设计的 52）", f"{gap:.2f}")

    # ---- 5. 加号：墨迹 ~47.9% 高、顶边与数字齐 ----------------------------
    # 设计实测（285:18162 渲染稿）：hero 12/25、stats 60+ 17/35.5、stats 10+ 17/36
    print("\n[5] 60+ 的加号")
    m = pg.evaluate("""() => {
      const out = {};
      for (const [k, sel] of [['stat', '.gb-stat--ingredients .gb-stat__value'],
                              ['usp',  '.gb-usp__value']]) {
        const el = document.querySelector(sel);
        const plus = el.querySelector('.gb-stat__plus, .gb-usp__plus');
        if (!plus) { out[k] = null; continue; }
        const c = document.createElement('canvas').getContext('2d');
        const cs = getComputedStyle(el), ps = getComputedStyle(plus);
        c.font = `${cs.fontWeight} ${cs.fontSize} ${cs.fontFamily}`;
        const dig = c.measureText('6');
        c.font = `${ps.fontWeight} ${ps.fontSize} ${ps.fontFamily}`;
        const pl = c.measureText('+');
        out[k] = { digAsc: dig.actualBoundingBoxAscent, digDesc: dig.actualBoundingBoxDescent,
                   plAsc: pl.actualBoundingBoxAscent, plDesc: pl.actualBoundingBoxDescent,
                   rise: parseFloat(ps.top), fs: parseFloat(ps.fontSize), base: parseFloat(cs.fontSize) };
      }
      return out;
    }""")
    for k, exp in (('stat', 0.479), ('usp', 0.48)):
        v = m[k]
        assert v, k
        digH = v['digAsc'] + v['digDesc']
        plH = v['plAsc'] + v['plDesc']
        # 抬升后加号墨迹顶相对数字墨迹顶（正 = 更低），设计 stats 1.5 / hero 0
        top_off = (v['digAsc']) - (v['plAsc'] - v['rise'])
        print(f"      {k}: 数字墨迹 {digH:.2f}  加号墨迹 {plH:.2f} ({plH/digH*100:.1f}%)  顶边差 {top_off:+.2f}px")
        check(near(plH / digH, exp, 0.035), f"[{k}] 加号墨迹 = 数字的 {exp*100:.0f}%", f"{plH/digH*100:.1f}%")
        check(abs(top_off) <= 2.5, f"[{k}] 加号顶边与数字顶边齐平（±2.5px）", f"{top_off:+.2f}px")

    # ---- 6. 箭头：几何取自 Figma，且是 .gb-stats__bear 的子元素 ------------
    print("\n[6] 四支箭头")
    DESIGN = {  # 合成 组变换x子变换 后的墨迹盒（含 3.56071 居中描边），相对 1192.879x623.113
        '1': (388.720, 50.483, 116.428, 99.951),
        '2': (289.057, 301.848, 125.896, 116.817),
        '3': (771.113, 228.789, 125.350, 116.759),
        '4': (769.726, 500.413, 126.737, 114.385),
    }
    parent = pg.evaluate("()=>[...document.querySelectorAll('.gb-stats__arrow')]"
                         ".map(e=>e.parentElement.className)")
    check(all('gb-stats__bear' in c for c in parent), "四支都在 .gb-stats__bear 里", str(set(parent)))
    # 熊带着 .gb-float-art--d1 的漂浮，箭头现在跟着一起飘 —— 不停掉这条动画，
    # 量到的位置取决于采样那一帧的相位（实测偏 1.8px / 5px，纯噪声）。
    # 只关掉 .gb-float-art 的 animation，别全局 animation:none：那会让靠入场动画
    # 显形的区块停在第 0 帧（见 memory kill-animations-blanks-reveal-blocks）。
    pg.add_style_tag(content=".gb-float-art{animation:none !important;transform:none !important}")
    pg.wait_for_timeout(120)
    G = pg.evaluate(RECTS, ['.gb-stats__grid'])['.gb-stats__grid']
    for k, (dx, dy, dw, dh) in DESIGN.items():
        r = pg.evaluate(RECTS, [f'.gb-stats__arrow--{k}'])[f'.gb-stats__arrow--{k}']
        lx = (r['x'] - G['x']) / G['w'] * 100; ty = (r['y'] - G['y']) / G['h'] * 100
        ex = dx / 1192.879 * 100; ey = dy / 623.113 * 100
        check(near(lx, ex, 0.15) and near(ty, ey, 0.15),
              f"arrow{k} 位置", f"{lx:.3f}% / {ty:.3f}%  设计 {ex:.3f}% / {ey:.3f}%")
        check(near(r['w'] / r['h'], dw / dh, 0.02),
              f"arrow{k} 长宽比（旧实现漏了组的旋转，比例差 2.5 倍）",
              f"{r['w']/r['h']:.4f}  设计 {dw/dh:.4f}")

    # ---- 7. stats -> science 的波浪 --------------------------------------
    print("\n[7] stats 下缘波浪")
    w = pg.evaluate("""() => {
      const sec = document.querySelector('.gb-stats');
      const sc  = sec.querySelector('.gb-scallop--edge');
      const sci = document.querySelector('.gb-science');
      if (!sc) return null;
      const cs = getComputedStyle(sc);
      return { has: sec.classList.contains('gb-sec-edge'),
               bg: cs.getPropertyValue('--wave-bg').trim(), fg: cs.getPropertyValue('--wave-fg').trim(),
               h: sc.getBoundingClientRect().height,
               secBg: getComputedStyle(sec).backgroundColor,
               sciBg: getComputedStyle(sci).backgroundColor };
    }""")
    check(w is not None and w['has'], "gb-stats 带 gb-sec-edge 且有 gb-scallop--edge 子元素")
    if w:
        print("     ", json.dumps(w))
        check(w['bg'] == '#faf9f8' and w['fg'] == '#f5f1e9',
              "配色 = 上 cream / 下 sand（稿 341:47307 Spacer 底色 #faf9f8，下一段 #f5f1e9）")
        check(near(w['h'], 96, 1.5), "高 96 = 稿 Spacer 的高（不带 --lg）", f"{w['h']:.1f}")

    # ---- 手机端：弧字降到 20px、星条不变 -----------------------------------
    print("\n[手机 390]")
    pg2 = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=1)
    pg2.goto("file://" + os.path.join(ROOT, "index.html")); settle(pg2)
    mm = pg2.evaluate("""() => {
      const svg = document.querySelector('.gb-stats__arc');
      const st  = document.querySelector('.gb-announcement__stars').getBoundingClientRect();
      return { fs: getComputedStyle(svg.querySelector('text')).fontSize,
               w: svg.getBoundingClientRect().width, stw: st.width, sth: st.height };
    }""")
    check(mm['fs'] == '20px', "手机稿 236:12453 字号 20", mm['fs'])
    check(near(mm['w'], 278), "弧框仍是 278（手机稿同尺寸）", f"{mm['w']:.1f}")
    check(near(mm['stw'], 77) and near(mm['sth'], 14), "星条 77x14 不变", f"{mm['stw']:.1f}x{mm['sth']:.1f}")

    b.close()

print("\n" + ("\033[31m失败 %d 条：%s\033[0m" % (len(fails), fails) if fails else "\033[32m全部通过\033[0m"))
sys.exit(1 if fails else 0)
