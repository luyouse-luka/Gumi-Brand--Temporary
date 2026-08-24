#!/usr/bin/env python3
"""重建首页 hero 的 images/gumi-bear-front-glow.png（第二十轮）。

    python3 tools/make-hero-glow.py            # 写 images/gumi-bear-front-glow.png
    python3 tools/make-hero-glow.py --check    # 只报几何，不写文件

为什么要脚本而不是手工合成：光晕**不是照片自带的**，是稿里单独一条描边。
Figma 332:16444「Background」（467.886 x 759.180，clipsContent，整体旋转 7.92°）里放了两样：

  332:16445  VECTOR   439.066 x 732.078 @ (13.979, 13.791)
                      fillGeometry 是空的，只有 strokeWeight 26.2137 / CENTER / #b5ed61
                      —— 光圈向外扩 13.107、向内压 13.107
  332:16446  RECTANGLE 1010.919 x 780.649 @ (-271.928, -13.757)，IMAGE fill，scaleMode FILL
                      源图 images/gumi-bear-front.png（1200x927，比例与该矩形一致，
                      所以 FILL 等于直接拉伸，不裁）

旧文件是照着照片 alpha 描的一圈约 12px（屏幕上 10.4px），不到设计 26.2px 的 40%，
而且贴着照片的每个凹凸走；设计那条是平滑贴纸轮廓，腿缝被粗描边糊平。

输出尺寸 559x910 = 设计墨迹 466.0 x 758.5 的 1.2x，与旧文件同一采样率，
LCP 字节数不变（旧 787K/76K webp，新 741K/77K webp）。要提到 2x 就把 OUT_W 改成 932，
webp 会涨到约 123K —— 那是 docs/audit/04-performance 里 P2 那条「欠采样」的解法，
和本轮的几何修复是两件事，别顺手一起改。
"""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NODES = os.path.join(ROOT, "figma", "nodes", "285-18162_homepage-desktop.json")
SRC   = os.path.join(ROOT, "images", "gumi-bear-front.png")
OUT   = os.path.join(ROOT, "images", "gumi-bear-front-glow.png")
CHROME = os.path.expanduser("~/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome")

BG_W, BG_H       = 467.8861389160156, 759.1803588867188   # 332:16444 size
GLOW_DX, GLOW_DY = 13.979483604431152, 13.790689468383789 # 332:16445 relativeTransform
IMG_X, IMG_Y     = -271.92828369140625, -13.756697654724121
IMG_W, IMG_H     = 1010.9190063476562, 780.6486206054688  # 332:16446 size
LIME             = "#b5ed61"
SUPERSAMPLE      = 2      # 先 2x 渲染再降采样，边缘比直接渲染干净
OUT_W            = 559    # 1.2x of 466.0，与旧文件同采样率


def find(node, nid):
    if node.get("id") == nid:
        return node
    for c in node.get("children") or []:
        r = find(c, nid)
        if r:
            return r
    return None


def glow_path():
    doc = json.load(io.open(NODES, encoding="utf-8"))
    for v in doc["nodes"].values():
        n = find(v["document"], "332:16445")
        if n:
            sg = n.get("strokeGeometry") or []
            assert len(sg) == 1, f"strokeGeometry 有 {len(sg)} 段，脚本只处理 1 段"
            return sg[0]["path"]
    raise SystemExit("在 285-18162 里找不到 332:16445（hero glow 矢量）")


def main():
    check = "--check" in sys.argv
    d = glow_path()
    print(f"glow strokeGeometry: {len(d)} 字符")
    print(f"Background {BG_W:.3f} x {BG_H:.3f}  glow@({GLOW_DX:.3f},{GLOW_DY:.3f})  "
          f"img {IMG_W:.3f}x{IMG_H:.3f}@({IMG_X:.3f},{IMG_Y:.3f})")
    if check:
        return

    from playwright.sync_api import sync_playwright
    from PIL import Image
    import numpy as np

    html = (
        "<!doctype html><meta charset=utf-8><style>"
        "html,body{margin:0;padding:0;background:transparent}"
        f"#box{{position:relative;width:{BG_W}px;height:{BG_H}px;overflow:hidden}}"
        "#box svg{position:absolute;left:0;top:0}"
        f"#box img{{position:absolute;left:{IMG_X}px;top:{IMG_Y}px;width:{IMG_W}px;height:{IMG_H}px}}"
        "</style><div id=box>"
        f'<svg width="{BG_W}" height="{BG_H}" viewBox="0 0 {BG_W} {BG_H}">'
        f'<g transform="translate({GLOW_DX} {GLOW_DY})">'
        f'<path fill="{LIME}" fill-rule="nonzero" d="{d}"/></g></svg>'
        f'<img src="file://{SRC}" alt=""></div>'
    )
    tmp = os.path.join(ROOT, "tools", ".hero-glow.html")
    io.open(tmp, "w", encoding="utf-8").write(html)
    raw = os.path.join(ROOT, "tools", ".hero-glow.png")
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME)
        pg = b.new_page(viewport={"width": 600, "height": 820},
                        device_scale_factor=SUPERSAMPLE)
        pg.goto("file://" + tmp)
        pg.wait_for_timeout(600)
        pg.locator("#box").screenshot(path=raw, omit_background=True)
        b.close()

    im = Image.open(raw).convert("RGBA")
    a = np.array(im)[..., 3]
    ys, xs = np.nonzero(a > 2)
    crop = im.crop((int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1))
    print(f"墨迹盒 {crop.width}x{crop.height} px @{SUPERSAMPLE}x "
          f"= 设计 {crop.width / SUPERSAMPLE:.2f} x {crop.height / SUPERSAMPLE:.2f}")
    out_h = round(crop.height * OUT_W / crop.width)
    crop.resize((OUT_W, out_h), Image.LANCZOS).save(OUT, optimize=True)
    os.remove(tmp); os.remove(raw)
    print(f"写入 {OUT}  {OUT_W}x{out_h}  {os.path.getsize(OUT) // 1024} K")
    print("接着跑： python3 tools/webp.py")


if __name__ == "__main__":
    main()
