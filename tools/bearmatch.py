#!/usr/bin/env python3
"""Silhouette IoU: which orientation of which asset does each board bear draw?

Eyeballing a symmetrical-ish gummy bear is unreliable, and Figma's
absoluteBoundingBox lies for rotated nodes (memory figma-rotated-frame-bbox-is-
not-the-artwork), so the judge is the rendered design screenshot's own outline.
"""
from PIL import Image
import numpy as np

SH = 'figma/screenshots/'
DESKTOP = SH + '285-18162_homepage-desktop_1440x10123.png'
MOBILE  = SH + '228-5932_homepage-mobile_390x11543.png'


def crop_mask(path, y0, y1, x0, x1):
    a = np.asarray(Image.open(path).convert('RGB')).astype(int)[y0:y1, x0:x1]
    lime = np.abs(a - np.array([0xb5, 0xed, 0x61])).sum(2) < 90
    green = (a[:, :, 1] > a[:, :, 0] + 18) & (a[:, :, 1] > a[:, :, 2] + 18)
    m = lime | green
    ys, xs = np.where(m)
    return m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def png_mask(path):
    a = np.asarray(Image.open(path).convert('RGBA'))[:, :, 3]
    m = a > 16
    ys, xs = np.where(m)
    return m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def norm(m, H=200):
    im = Image.fromarray((m * 255).astype('uint8'))
    w = max(1, int(round(im.width * H / im.height)))
    return np.asarray(im.resize((w, H), Image.BILINEAR)) > 127


def iou(a, b):
    H, W = max(a.shape[0], b.shape[0]), max(a.shape[1], b.shape[1])
    def pad(m):
        o = np.zeros((H, W), bool)
        dy, dx = (H - m.shape[0]) // 2, (W - m.shape[1]) // 2
        o[dy:dy + m.shape[0], dx:dx + m.shape[1]] = m
        return o
    pa, pb = pad(a), pad(b)
    return (pa & pb).sum() / max(1, (pa | pb).sum())


def rot(m, deg):
    im = Image.fromarray((m * 255).astype('uint8')).rotate(-deg, expand=True, resample=Image.BILINEAR)
    a = np.asarray(im) > 127
    ys, xs = np.where(a)
    return norm(a[ys.min():ys.max() + 1, xs.min():xs.max() + 1])


def report(label, board, asset):
    best = max(((iou(board, rot(asset if not f else asset[:, ::-1], d)), d, f)
                for d in range(-30, 31, 2) for f in (False, True)))
    print(f"{label}\n   as-is {iou(board, asset):.3f}   mirrored {iou(board, asset[:, ::-1]):.3f}"
          f"   best {best[0]:.3f} @ {best[1]:+d}° {'mirrored' if best[2] else 'as-is'}")


if __name__ == '__main__':
    deco_d = norm(crop_mask(DESKTOP, 2435, 2635, 1090, 1250))
    deco_m = norm(crop_mask(MOBILE, 2438, 2572, 218, 325))
    ctr_d  = norm(crop_mask(DESKTOP, 1770, 2170, 560, 900))
    ctr_m  = norm(crop_mask(MOBILE, 1845, 2120, 70, 320))
    a_ctr  = norm(png_mask('images/stats-bear.png'))
    a_deco = norm(png_mask('images/stats-bear-deco.png'))

    print(f"ratios  deco稿桌面 {deco_d.shape[1]/deco_d.shape[0]:.3f}  deco稿手机 {deco_m.shape[1]/deco_m.shape[0]:.3f}"
          f"  中央稿桌面 {ctr_d.shape[1]/ctr_d.shape[0]:.3f}  中央稿手机 {ctr_m.shape[1]/ctr_m.shape[0]:.3f}"
          f"  素材中央 {a_ctr.shape[1]/a_ctr.shape[0]:.3f}  素材deco {a_deco.shape[1]/a_deco.shape[0]:.3f}\n")
    report("中央熊 稿桌面 vs images/stats-bear.png", ctr_d, a_ctr)
    report("中央熊 稿手机 vs images/stats-bear.png", ctr_m, a_ctr)
    report("装饰熊 稿桌面 vs images/stats-bear.png", deco_d, a_ctr)
    report("装饰熊 稿手机 vs images/stats-bear.png", deco_m, a_ctr)
    report("装饰熊 稿桌面 vs images/stats-bear-deco.png", deco_d, a_deco)
    print()
    print(f"稿手机装饰熊 vs 稿桌面装饰熊   as-is {iou(deco_m, deco_d):.3f}   mirrored {iou(deco_m, deco_d[:, ::-1]):.3f}")
    print(f"稿手机中央熊 vs 稿桌面中央熊   as-is {iou(ctr_m, ctr_d):.3f}   mirrored {iou(ctr_m, ctr_d[:, ::-1]):.3f}")
