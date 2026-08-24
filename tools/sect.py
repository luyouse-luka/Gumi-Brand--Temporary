#!/usr/bin/env python3
"""按区块截图 —— 整页截图动辄一万像素高，看不清也读不动。

    python3 tools/sect.py index.html 768                 # 每个 section 一张
    python3 tools/sect.py index.html 768 .nutrition      # 只截这个选择器
    python3 tools/sect.py index.html 768 1281 .stats     # 同一块，多个宽度

落到 tools/shots/sect/<页>-<宽>-<序号><类名>.png。
截图前会等 1700ms —— wowo 播 0.7s、1500ms 才卸 class，截早了满屏「重影」。
元素截图按边界盒裁，描边光晕本来就在盒外，所以统一带 24px 留白
（见 memory element-screenshot-clips-overflow）。
"""
import os, sys
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "tools", "shots", "sect")
CHROME = os.path.expanduser("~/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome")
PAD = 24


def main():
    args = sys.argv[1:]
    page = next((a for a in args if a.endswith(".html")), "index.html")
    widths = [int(a) for a in args if a.isdigit()] or [1440]
    sel = next((a for a in args if a.startswith(".") or a.startswith("#")), None)
    os.makedirs(OUT, exist_ok=True)
    stem = os.path.splitext(page)[0]

    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=CHROME)
        for w in widths:
            pg = br.new_page(viewport={"width": w, "height": 900})
            pg.add_init_script("Math.random = function () { return 0.5; };")
            pg.goto("file://" + os.path.join(ROOT, page))
            pg.evaluate("() => document.fonts.ready")
            # 滚一遍把所有 wowo 触发掉，否则折线以下的区块停在 opacity:0
            h = pg.evaluate("document.documentElement.scrollHeight")
            y = 0
            while y < h:
                pg.evaluate(f"window.scrollTo(0,{y})")
                pg.wait_for_timeout(60)
                y += 500
            pg.evaluate("window.scrollTo(0,0)")
            pg.wait_for_timeout(1700)

            targets = pg.query_selector_all(sel) if sel else \
                pg.query_selector_all("body > main > section, body > main > div.scallop, "
                                      "body > header, body > footer, body > .footer-cta-wrap")
            for i, el in enumerate(targets):
                box = el.bounding_box()
                if not box or box["height"] < 8:
                    continue
                cls = (el.get_attribute("class") or "sec").split(" ")[0].replace("/", "_")
                clip = {"x": max(0, box["x"] - PAD), "y": max(0, box["y"] - PAD),
                        "width": min(w, box["width"] + PAD * 2),
                        "height": min(8000, box["height"] + PAD * 2)}
                name = f"{stem}-{w}-{i:02d}{cls}.png"
                pg.screenshot(path=os.path.join(OUT, name), clip=clip, full_page=True)
                print(f"  {name}  {round(box['width'])}x{round(box['height'])}")
            pg.close()
        br.close()


if __name__ == "__main__":
    main()
