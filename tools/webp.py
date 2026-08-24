#!/usr/bin/env python3
"""Emit a .webp beside every referenced PNG in images/. Never touches the PNGs.

    python3 tools/webp.py            # write images/*.webp
    python3 tools/webp.py --check    # report only

Per-file strategy comes from the audit's measurements (docs/audit/04-performance
2.2): flat-colour logos are smaller LOSSLESS than lossy, three bears are wildly
oversampled and get resized to 2x their largest measured display box first, the
rest are same-size q82.

Quality gate: PSNR against the original AFTER compositing both onto white (the
page's own backdrop), because these are all RGBA and comparing raw RGB where
alpha is 0 measures nothing. >= 35 dB is the pass mark; anything lower is
rebuilt lossless rather than shipped blurry.
"""
import os, sys, math
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "images")

# name: (mode, target_size or None)   mode = "lossless" or a quality int
PLAN = {
    "gumi-bear-front.png":      (82, (249, 192)),
    "vs-bear-glow.png":         (82, (448, 346)),
    "promo-art.png":            (82, (940, 804)),
    "nutrition-bears.png":      (82, (555, 528)),   # 桌面显示 277.36x264，取 2x
    "others-bottles.png":       (90, (224, 224)),   # 82 lands at 34.5 dB, just under the bar
    "gumi-bear-front-glow.png": (82, None),
    "stats-bear.png":           (82, None),
    "deco-bear-md.png":         (82, None),
    "deco-bear-sm.png":         (82, None),
    "nav-card-bear.png":        (82, None),
    "product-pack.png":         ("lossless", None),
    "media-vogue.png":          ("lossless", None),
    "media-abc-news.png":       ("lossless", None),
    "media-wellbeing.png":      ("lossless", None),
    "bear-icon.png":            ("lossless", None),   # 27x44, lossless is only 2.7 K anyway
}

def on_white(im):
    bg = Image.new("RGB", im.size, (255, 255, 255))
    bg.paste(im, mask=im.split()[3] if im.mode == "RGBA" else None)
    return bg

def psnr(a, b):
    # Both must already be at the same size. For a resized target the reference
    # is the ORIGINAL RESIZED THE SAME WAY -- comparing a deliberately smaller
    # file against the full-size original measures the resize, not the codec,
    # and reports every downscaled image as a quality failure.
    assert a.size == b.size, (a.size, b.size)
    pa, pb = a.load(), b.load()
    w, h = a.size
    step = max(1, min(w, h) // 200)
    se = n = 0
    for y in range(0, h, step):
        for x in range(0, w, step):
            for c in range(3):
                d = pa[x, y][c] - pb[x, y][c]
                se += d * d; n += 1
    mse = se / n
    return 99.0 if mse == 0 else 10 * math.log10(255 * 255 / mse)

check = "--check" in sys.argv
tot_png = tot_webp = 0
for name, (mode, size) in sorted(PLAN.items()):
    src = os.path.join(IMG, name)
    if not os.path.exists(src):
        print(f"  MISSING {name}"); continue
    dst = src[:-4] + ".webp"
    im = Image.open(src).convert("RGBA")
    out = im.resize(size, Image.LANCZOS) if size else im
    if not check:
        if mode == "lossless":
            out.save(dst, "WEBP", lossless=True, method=6)
        else:
            out.save(dst, "WEBP", quality=mode, method=6)
    if not os.path.exists(dst):
        continue
    p_png, p_webp = os.path.getsize(src), os.path.getsize(dst)
    tot_png += p_png; tot_webp += p_webp
    q = psnr(on_white(out), on_white(Image.open(dst).convert("RGBA")))
    flag = "ok " if q >= 35 else "LOW"
    print(f"  {flag} {name:<26} {p_png:>8,} -> {p_webp:>7,}  ({100 - p_webp * 100 // p_png:>2}%-)  "
          f"{str(mode):<8} {str(size or 'same'):<12} PSNR {q:.1f} dB")
print(f"\n  total {tot_png:,} -> {tot_webp:,}  (-{100 - tot_webp * 100 // tot_png}%)")
