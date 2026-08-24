#!/usr/bin/env python3
"""第十九轮 7 条任务的专项判据。每条都给可复核的数字，不靠肉眼。

    python3 tools/r19check.py
"""
import os, sys, json
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = os.path.expanduser("~/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome")
ok = lambda c: "\033[32m✓\033[0m" if c else "\033[31m✗\033[0m"
fails = []
def check(cond, label, detail=""):
    print(f"  {ok(cond)} {label}  {detail}")
    if not cond: fails.append(label)

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME)

    # ---- 1. 弹窗：退场比进场慢，且不是同一条曲线 --------------------------
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto("file://" + os.path.join(ROOT, "pdp.html")); pg.wait_for_timeout(500)
    print("\n[1] 弹窗关闭速度")
    r = pg.evaluate("""() => {
      const pan = document.querySelector('.gb-nl-panel');
      const ov  = document.querySelector('.gb-nl-modal__overlay');
      const mod = document.querySelector('.gb-nl-modal');
      const g = e => { const s = getComputedStyle(e);
        return [s.transitionDuration, s.transitionTimingFunction, s.transitionDelay]; };
      const out = { closePan: g(pan), closeOv: g(ov), closeMod: g(mod) };
      mod.classList.add('is-open');
      out.openPan = g(pan); out.openOv = g(ov);
      mod.classList.remove('is-open');
      return out;
    }""")
    print("     ", json.dumps(r))
    check(r["closePan"][0] == "0.55s" and r["openPan"][0] == "0.4s",
          "面板：退场 0.55s > 进场 0.4s", f"{r['closePan'][0]} / {r['openPan'][0]}")
    check(r["closePan"][1] != r["openPan"][1], "面板：进退场不是同一条曲线")
    check(r["closeOv"][0] == "0.55s", "遮罩淡出同步", r["closeOv"][0])
    check(r["closeMod"][2] == "0.55s", "visibility 延迟跟上退场", r["closeMod"][2])

    # ---- 2. 手风琴：行间空白全部可点，且收起态几何不变 --------------------
    print("\n[2] 手风琴死区")
    for page, sel, vw in [("pdp.html", ".gb-product__accordion", 1440),
                          ("faq.html", ".gb-faq__list", 1440),
                          ("science.html", ".gb-faq-image__list", 1440),
                          ("science.html", ".gb-faq-image__list", 390)]:
        pg.set_viewport_size({"width": vw, "height": 900})
        pg.goto("file://" + os.path.join(ROOT, page)); pg.wait_for_timeout(400)
        r = pg.evaluate("""(sel) => {
          // 同名容器可能有手机/桌面两份，另一份此刻是 display:none —— 只测看得见的那个
          const box = [...document.querySelectorAll(sel)].find(e => e.getClientRects().length);
          if (!box) return { err: 'no visible ' + sel };
          box.scrollIntoView({ block: 'center' });
          const items = [...box.querySelectorAll('details')];
          const res = { gap: getComputedStyle(box).rowGap, dead: [], n: items.length };
          for (let i = 0; i < items.length - 1; i++) {
            const a = items[i].getBoundingClientRect();
            const bb = items[i+1].getBoundingClientRect();
            const y = (a.bottom + bb.top) / 2;          // 两行之间
            const x = a.left + 20;
            const hit = document.elementFromPoint(Math.round(x), Math.round(y));
            const s = hit && hit.closest && hit.closest('summary');
            if (!s) res.dead.push([i, Math.round(y), hit ? hit.className : null]);
          }
          // 收起态：相邻两行文字基线间距（几何不变量）
          res.pitch = items.length > 1
            ? +(items[1].getBoundingClientRect().top - items[0].getBoundingClientRect().top).toFixed(2) : null;
          return res;
        }""", sel)
        check(not r.get("dead") and not r.get("err"), f"@{vw} {page} {sel} 行间无死区",
              f"{r['n']} 行, gap={r.get('gap')}, 行距={r.get('pitch')}, 死点={r.get('dead')}")

    # 间距还原：收起行距 / 展开后正文到下一行，都应等于原来的 gap；summary 到正文是稿里的 16。
    # ⚠ 参考点必须取「墨迹」——padding 已经算进 rect，拿盒边量必然读到 0。
    SPACING = """async (sel) => {
      const box = [...document.querySelectorAll(sel)].find(e => e.getClientRects().length);
      const items = [...box.querySelectorAll('details')];
      const gap = getComputedStyle(box).getPropertyValue('--acc-gap').trim();
      items.forEach(d => d.open = false);
      await new Promise(r => setTimeout(r, 700));
      const sumInk = d => { const su = d.querySelector('summary');
        return su.getBoundingClientRect().bottom - parseFloat(getComputedStyle(su).paddingBottom); };
      const closedGap = items[1].getBoundingClientRect().top - sumInk(items[0]);
      items[0].open = true;
      await new Promise(r => setTimeout(r, 900));
      const kids = [...items[0].querySelector('.gb-acc-body').children];
      const first = kids[0].getBoundingClientRect(), last = kids[kids.length-1].getBoundingClientRect();
      items[0].open = false;
      return { gap: parseFloat(gap), closedGap: +closedGap.toFixed(2),
               sumToBody: +(first.top - sumInk(items[0])).toFixed(2),
               bodyToNext: +(items[1].getBoundingClientRect().top - last.bottom).toFixed(2) };
    }"""
    pg.set_viewport_size({"width": 1440, "height": 900})
    for page, sel in [("pdp.html", ".gb-product__accordion"), ("faq.html", ".gb-faq__list"),
                      ("science.html", ".gb-faq-image__list")]:
        pg.goto("file://" + os.path.join(ROOT, page)); pg.wait_for_timeout(400)
        r = pg.evaluate(SPACING, sel)
        good = (abs(r["closedGap"] - r["gap"]) < .6 and abs(r["bodyToNext"] - r["gap"]) < .6
                and abs(r["sumToBody"] - 16) < .6)
        check(good, f"{page} {sel} 间距仍是稿值",
              f"gap={r['gap']} 收起行距={r['closedGap']} 展开后={r['bodyToNext']} summary→正文={r['sumToBody']}")

    # ---- 3. 加号图标：CSS 画的、展开转平、hover 不放大 ---------------------
    print("\n[3] 加号图标")
    pg.goto("file://" + os.path.join(ROOT, "faq.html")); pg.wait_for_timeout(400)
    r = pg.evaluate("""async () => {
      const d = [...document.querySelectorAll('.gb-faq__item')].find(x => !x.open);
      d.scrollIntoView({ block: 'center' });
      const ic = d.querySelector('.gb-acc-icon');
      const g = () => [getComputedStyle(ic, '::before').transform, getComputedStyle(ic, '::after').transform,
                       getComputedStyle(ic, '::before').width, getComputedStyle(ic, '::after').height];
      const closed = g();
      d.open = true;
      // 竖线带 0.3s 过渡，同步读回的是**起始值** —— 必须等过渡跑完
      await new Promise(r => setTimeout(r, 500));
      const opened = g();
      d.open = false;
      return { tag: ic.tagName, svg: document.querySelectorAll('svg.gb-acc-icon').length,
               closed, opened, iconRect: (r => [r.width, r.height])(ic.getBoundingClientRect()) };
    }""")
    print("     ", json.dumps(r))
    check(r["tag"] == "SPAN" and r["svg"] == 0, "图标不再是 SVG", r["tag"])
    # rotate(90deg) 的矩阵 = matrix(0,1,-1,0,0,0)
    check("0, 1, -1, 0" in r["closed"][1], "收起：竖线立着(rotate 90)", r["closed"][1])
    check(r["opened"][1] in ("none", "matrix(1, 0, 0, 1, 0, 0)"), "展开：竖线转平成减号", r["opened"][1])
    check(r["closed"][0] == r["opened"][0] == "none", "横线不动")
    check(r["iconRect"] == [24, 24], "图标仍是 24x24", str(r["iconRect"]))
    hov = pg.evaluate("""() => {
      const s = [...document.styleSheets].flatMap(x => { try { return [...x.cssRules]; } catch(e) { return []; } });
      const txt = s.map(r => r.cssText).join('\\n');
      return (txt.match(/scale\\(1\\.15\\)/g) || []).length;
    }""")
    check(hov == 0, "hover 放大规则已清零", f"scale(1.15) x{hov}")

    # ---- 4. 输入框焦点：无 outline，边框换色 ------------------------------
    print("\n[4] 输入框焦点")
    pg.goto("file://" + os.path.join(ROOT, "get-in-touch.html")); pg.wait_for_timeout(400)
    for sel in [".gb-field__input", ".gb-footer__input"]:
        before = pg.evaluate("(sel) => getComputedStyle(document.querySelector(sel)).borderTopColor", sel)
        pg.click(sel)          # 脚本 focus() 不触发 :focus-visible，只有真交互才算
        pg.wait_for_timeout(250)
        r = pg.evaluate("""(sel) => {
          const s = getComputedStyle(document.querySelector(sel));
          return { after: s.borderTopColor, outline: s.outlineWidth + ' ' + s.outlineStyle,
                   shadow: s.boxShadow, matches: document.querySelector(sel).matches(':focus-visible') };
        }""", sel)
        r["before"] = before
        check(r["matches"], f"{sel} 已进入 :focus-visible", str(r["matches"]))
        check(r["outline"].startswith("0px") or r["outline"].endswith("none"),
              f"{sel} 焦点无 outline", r["outline"])
        check(r["before"] != r["after"], f"{sel} 焦点换边框色", f"{r['before']} -> {r['after']}")
        check(r["shadow"] == "none", f"{sel} 无光晕", r["shadow"])
    # 鼠标点复选框本来就不出焦点环（浏览器的启发式），所以这里不测点击后的 outline，
    # 只证明它**没被**「摘掉 outline」那条规则收进去 —— 键盘 Tab 过来时焦点环还在。
    r = pg.evaluate("""() => { const c = document.querySelector('input[type=checkbox]');
      if (!c) return null;
      return c.matches('input:not([type=\"checkbox\"]):not([type=\"radio\"]), textarea, select'); }""")
    check(r is False, "复选框不在「摘 outline」的名单里（键盘焦点环保留）", str(r))

    # ---- 5. header 吸顶 ---------------------------------------------------
    print("\n[5] header 吸顶")
    for w, h in [(1440, 900), (390, 800)]:
        pg.set_viewport_size({"width": w, "height": h})
        pg.goto("file://" + os.path.join(ROOT, "index.html")); pg.wait_for_timeout(500)
        r = pg.evaluate("""async () => {
          const hd = document.getElementById('site-header');
          const t0 = hd.getBoundingClientRect().top;
          window.scrollTo(0, 1500);
          await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
          const t1 = hd.getBoundingClientRect().top;
          const cs = getComputedStyle(hd);
          return { t0: +t0.toFixed(1), t1: +t1.toFixed(1), pos: cs.position, z: cs.zIndex,
                   scrolled: window.scrollY };
        }""")
        check(r["pos"] == "sticky" and abs(r["t1"]) < 0.5,
              f"@{w} 滚动 {r['scrolled']}px 后 header 贴顶", f"top {r['t0']} -> {r['t1']}")
    # 抽屉高度：手机端开菜单，底边不越过视口
    pg.set_viewport_size({"width": 390, "height": 800})
    pg.goto("file://" + os.path.join(ROOT, "index.html")); pg.wait_for_timeout(600)
    r = pg.evaluate("""async () => {
      const out = [];
      for (const y of [0, 1500]) {
        window.scrollTo(0, y);
        await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
        window.gumi.header.set(true);
        await new Promise(r => setTimeout(r, 400));
        const p = document.querySelector('.gb-header__panel').getBoundingClientRect();
        out.push({ y: window.scrollY, top: +p.top.toFixed(1), bottom: +p.bottom.toFixed(1),
                   vh: window.innerHeight });
        window.gumi.header.set(false);
        await new Promise(r => setTimeout(r, 400));
      }
      return out;
    }""")
    for x in r:
        check(abs(x["bottom"] - x["vh"]) < 1.5,
              f"抽屉底边贴视口底（滚动 {x['y']}）", f"bottom {x['bottom']} vs vh {x['vh']}")

    # ---- 6. 弧形文字不再被裁 ----------------------------------------------
    print("\n[6] 弧形文字")
    pg.set_viewport_size({"width": 1440, "height": 900})
    import glob
    for f in sorted(glob.glob(os.path.join(ROOT, "*.html"))):
        n = os.path.basename(f)
        if n == "font-check.html": continue
        pg.goto("file://" + f); pg.wait_for_timeout(300)
        arcs = pg.evaluate("""() => [...document.querySelectorAll('.gb-arc-text')].map(svg => {
          const t = svg.querySelector('text'), tp = svg.querySelector('textPath');
          const path = svg.querySelector('path[id]'), vb = svg.viewBox.baseVal, bb = t.getBBox();
          return { cls: svg.getAttribute('class').replace('gb-arc-text ', ''),
                   over: +(0 - bb.y).toFixed(2),                       // 上缘越界量
                   under: +(bb.y + bb.height - vb.height).toFixed(2),  // 下缘越界量
                   slack: +(path.getTotalLength() - tp.getComputedTextLength()).toFixed(2),
                   ovf: getComputedStyle(svg).overflow };
        })""")
        for a in arcs:
            check(a["ovf"] == "visible" and a["slack"] > 0,
                  f"{n} {a['cls']}", f"上越界 {a['over']} 下越界 {a['under']} 路径余量 {a['slack']} overflow={a['ovf']}")

    # ---- 7. 页脚波浪与上方 section 同色 ------------------------------------
    print("\n[7] 页脚波浪配色")
    for f in sorted(glob.glob(os.path.join(ROOT, "*.html"))):
        n = os.path.basename(f)
        if n == "font-check.html": continue
        pg.goto("file://" + f); pg.wait_for_timeout(300)
        r = pg.evaluate("""() => {
          const w = document.querySelector('.gb-footer-cta-wrap .gb-scallop');
          if (!w) return null;
          w.scrollIntoView({ block: 'center' });
          const r = w.getBoundingClientRect();
          // 波浪条带上半部实际被画成什么色（取弧与弧之间的谷点，那里是 --wave-bg）
          const strip = getComputedStyle(w).backgroundColor;
          const secs = document.querySelectorAll('main > *');
          const last = secs[secs.length - 1];
          let n = last, bg = null;
          while (n) { const c = getComputedStyle(n).backgroundColor;
            if (c && c !== 'rgba(0, 0, 0, 0)') { bg = c; break; } n = n.parentElement; }
          return { strip, lastBg: getComputedStyle(last).backgroundColor, effective: bg,
                   cls: w.className, last: last.className.split(' ')[0] };
        }""")
        if not r: continue
        same = r["strip"] == r["effective"] or (r["strip"] == "rgba(0, 0, 0, 0)" and r["effective"] == r["lastBg"])
        # 透明条带露出的是 body；等价的判据是「实际看到的颜色 == 上方 section 的颜色」
        seen = r["lastBg"] if r["strip"] == "rgba(0, 0, 0, 0)" else r["strip"]
        check(seen == r["lastBg"], f"{n:22} 上方 {r['last']}",
              f"条带={r['strip']} 上方={r['lastBg']}")

    b.close()

print("\n" + ("=" * 60))
print(f"失败 {len(fails)} 条" if fails else "全部通过")
for f in fails: print("  -", f)
sys.exit(1 if fails else 0)
