#!/usr/bin/env python3
"""r63 判据 —— .gb-science__cards / .gb-nutrition__cards 的卡片在每一档都等高。

  python3 tools/r63check.py

三条：
  1. 每个容器内所有直接子元素高度相等（容差 0.5px），跨行也要相等
  2. 改动不得引入横向溢出
  3. 源与产物双写：scss 与编译后的 css 各含两条 grid-auto-rows

活性自检：把 css 里的 `grid-auto-rows:1fr` 改成 `auto` 重跑，第 1 条必须转红。
"""
import os, re, io
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = os.path.expanduser("~/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome")
PAGES = ["index.html", "science.html"]
WIDTHS = [1920, 1440, 1280, 1201, 1200, 1199, 992, 768, 767, 576, 575, 390, 360]
TOL = 0.5

PROBE = """() => [...document.querySelectorAll('.gb-science__cards, .gb-nutrition__cards')]
  .map((box, i) => ({
    box: box.className.split(' ')[0], i,
    hs: [...box.children].map(k => +k.getBoundingClientRect().height.toFixed(2)),
  }))"""

ok = red = 0
def check(cond, msg):
    global ok, red
    if cond: ok += 1
    else:
        red += 1
        print("RED  " + msg)

scss = io.open(os.path.join(ROOT, "assets/customstyle.scss"), encoding="utf-8").read()
css  = io.open(os.path.join(ROOT, "assets/customstyle.css"),  encoding="utf-8").read()
# strip // comments first: r64 explains the rule in a comment on
# .gb-science-card, and a bare findall counted that as a third declaration.
scss_code = re.sub(r"//[^\n]*", "", scss)
check(len(re.findall(r"grid-auto-rows:\s*1fr", scss_code)) == 2, "scss 缺 grid-auto-rows: 1fr（应 2 处）")
check(len(re.findall(r"grid-auto-rows:\s*1fr", css))  == 2, "css 产物缺 grid-auto-rows: 1fr（应 2 处）")

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME)
    for page in PAGES:
        pg = b.new_page()
        pg.goto("file://" + os.path.join(ROOT, page))
        for w in WIDTHS:
            pg.set_viewport_size({"width": w, "height": 900})
            pg.wait_for_timeout(160)
            groups = pg.evaluate(PROBE)
            check(len(groups) > 0, f"{page} @{w} 没找到任何 cards 容器（判据取错了页面）")
            for g in groups:
                hs = g["hs"]
                check(len(hs) >= 2, f"{page} @{w} {g['box']}#{g['i']} 只有 {len(hs)} 张卡")
                check(hs and max(hs) - min(hs) <= TOL,
                      f"{page} @{w} {g['box']}#{g['i']} 高度不一致 {hs}")
            over = pg.evaluate("() => [document.documentElement.scrollWidth, document.documentElement.clientWidth]")
            check(over[0] <= over[1] + 1, f"{page} @{w} 横向溢出 {over}")
        pg.close()
    b.close()

print(f"\n{ok} ok / {red} red")
raise SystemExit(1 if red else 0)
