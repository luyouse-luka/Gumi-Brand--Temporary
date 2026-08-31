#!/usr/bin/env python3
"""CTA 板的九宫格接缝判据 —— 找比板色浅的贯穿发丝线。

    python3 tools/seamcheck.py                # 默认 5 档宽 × 8 档 DPR
    python3 tools/seamcheck.py 1100,1440

为什么需要它：`border-image` 的四个区块（角 / 边 / 中）各自抗锯齿，两条半透明边
加起来不足一格不透明度，于是在**离边 r 的那个矩形**上会渲染出一条比板色浅的发丝线。
它**只在某些设备像素比下出现**（实测 1100 处 DPR 1.25 / 1.75 / 2.25 有，1 / 1.5 / 2 / 3 没有），
所以只测整数 DPR 会漏 —— Windows 的 125% / 150% / 175% 缩放正好落在漏掉的那几档。

解法是在图下面垫一层同色实底（`plate-pad()`），并把它内缩到瓣的**谷线**以内，
否则实底会从谷里透出来把轮廓填平。谷深与平铺缩放无关，见 platecheck.py 的说明。

活性自检：删掉 `@include plate-pad(...)` 两处，1100 的 DPR 1.25 / 1.75 / 2.25 应立刻报红。
⚠ 与 `tools/platecheck.py` 是一对 —— 这条管「有没有多余的浅色线」，
那条管「实底有没有从谷里透出来把瓣形填平」。两条都要跑。
"""

import io, os, sys
from playwright.sync_api import sync_playwright
from PIL import Image
ROOT="/home/ly/project/Gumi-Brand"
CHROME=os.path.expanduser("~/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome")
SETTLE=(".wowo,.gb-float-art,[data-line-reveal],.gb-line-mask__inner,.gb-ink-halo{"
        "opacity:1!important;transform:none!important;animation:none!important}")
GREEN=(0x00,0x56,0x35)
def grab(w,dpr):
    with sync_playwright() as pw:
        b=pw.chromium.launch(executable_path=CHROME)
        pg=b.new_page(viewport={"width":w,"height":1400},device_scale_factor=dpr)
        pg.goto("file://"+ROOT+"/our-story.html"); pg.add_style_tag(content=SETTLE)
        pg.evaluate("() => document.fonts.ready"); pg.wait_for_timeout(420)
        el=pg.query_selector(".gb-cta-band__plate"); el.scroll_into_view_if_needed()
        pg.wait_for_timeout(220); box=el.bounding_box()
        png=pg.screenshot(clip={"x":box["x"],"y":box["y"],"width":box["width"],"height":box["height"]})
        b.close()
    return Image.open(io.BytesIO(png)).convert("RGB"), box
def seams(w,dpr):
    im,box=grab(w,dpr); W,H=im.size; px=im.load()
    r=39.9189 if w<=767 else 58.8848
    band=int(r*dpr)          # 只看边带（无内容），从轮廓下 2px 到 band
    rows={}
    for x in range(W):
        y=0
        while y<H and max(abs(px[x,y][i]-GREEN[i]) for i in range(3))>60: y+=1
        if y>=H: continue
        for yy in range(y+2, min(band+3,H)):
            c=px[x,yy]
            if c[1]>GREEN[1]+4: rows.setdefault(yy,[]).append(c[1]-GREEN[1])
    # 只报「贯穿性」的行：占板宽 30% 以上
    return box,[(round(y/dpr,1),len(v),max(v)) for y,v in sorted(rows.items()) if len(v)>W*0.3]
print("%-6s %-6s %-13s %s" % ("视口","DPR","板尺寸","贯穿发丝线 (CSS y, 像素数, 最亮Δ)"))
bad=0
WS=[int(x) for x in sys.argv[1].split(",")] if len(sys.argv)>1 else [390,767,900,1100,1440]
for w in WS:
    for dpr in (1,1.25,1.5,1.75,2,2.25,2.5,3):
        box,sm=seams(w,dpr)
        if sm: bad+=len(sm)
        print("%-6d %-6s %-13s %s" % (w,dpr,"%.0fx%.0f"%(box["width"],box["height"]),
              sm if sm else "无"))
print("=" * 66)
print("发现贯穿发丝线：%d 条" % bad)
raise SystemExit(1 if bad else 0)
