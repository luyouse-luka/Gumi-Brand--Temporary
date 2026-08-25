#!/usr/bin/env python3
"""断点边界连续性判据（第二十九轮）。

新体系的核心性质：fluid() 的起点就是 $bp-narrow + 1，而 fluid($m,$d) 在起点处
精确等于 $m —— 所以 767 → 768 这一步除了「排布本来就该切换」的属性外，
不应该有任何数值跳变。

    python3 tools/r29edge.py 767 768        # 查一对边界
    python3 tools/r29edge.py                # 查全部边界对

读 tools/snap/after/ 的快照，逐元素比对两个宽度的 computed style。
报出的每一条都是真实存在的跳变，附带元素路径，可直接定位。

⚠ 百分比/vw 值会随视口宽度自然变化，不算跳变 —— 这类用「相对变化率」过滤：
   宽度只差 1px，任何按比例走的量变化都远小于 1%。
"""
import json, os, sys, glob
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNAP = os.path.join(ROOT, "tools", "snap")

# 只有这些属性算「跳变」。
# ⚠ 不能收 height —— 边界处排布本来就要重排，高度是重排的**结果**不是原因，
#   收了它会有几千条被动差异把真信号埋掉（第一版实测 3608 条，全是 height）。
WATCH = ["font-size", "line-height", "letter-spacing", "gap", "row-gap", "column-gap",
         "padding-top", "padding-right", "padding-bottom", "padding-left",
         "margin-top", "margin-right", "margin-bottom", "margin-left",
         "border-top-left-radius"]

# 相邻宽度只差 1px，按比例走的量变化 <1%；超过这个比例才是真跳变
TOL_RATIO = 0.02
TOL_ABS = 0.5      # px，低于此值的差异是舍入噪声


def px(v):
    if not v or not v.endswith("px"):
        return None
    try:
        return float(v[:-2])
    except ValueError:
        return None


def compare(tag, w_lo, w_hi):
    lo_dir = os.path.join(SNAP, tag)
    rows = []
    for pa in sorted(glob.glob(os.path.join(lo_dir, f"*.{w_lo}.json"))):
        name = os.path.basename(pa).rsplit(f".{w_lo}.json", 1)[0]
        pb = os.path.join(lo_dir, f"{name}.{w_hi}.json")
        if not os.path.exists(pb):
            print(f"!! 缺 {name}@{w_hi}")
            continue
        da = dict(json.load(open(pa)))
        db = dict(json.load(open(pb)))
        for k in da:
            if k not in db:
                continue
            for p in WATCH:
                va, vb = px(da[k].get(p)), px(db[k].get(p))
                if va is None or vb is None:
                    continue
                d = abs(vb - va)
                if d <= TOL_ABS:
                    continue
                base = max(abs(va), abs(vb), 1.0)
                if d / base <= TOL_RATIO:
                    continue
                rows.append((d, name, k, p, va, vb))
    return rows


def main():
    tag = "after"
    pairs = [(767, 768), (575, 576), (991, 992), (1280, 1281)]
    if len(sys.argv) == 3:
        pairs = [(int(sys.argv[1]), int(sys.argv[2]))]

    worst = 0
    for lo, hi in pairs:
        rows = compare(tag, lo, hi)
        rows.sort(reverse=True)
        print("\n" + "=" * 78)
        print(f"  {lo} → {hi}   共 {len(rows)} 处数值跳变")
        print("=" * 78)
        if not rows:
            print("  ✅ 无跳变，边界连续")
            continue
        worst = max(worst, len(rows))
        by_sel = defaultdict(list)
        for d, name, k, p, va, vb in rows:
            tail = k.split("/")[-1]
            by_sel[(name, tail)].append((p, va, vb, d))
        shown = 0
        for (name, tail), items in sorted(by_sel.items(),
                                          key=lambda x: -max(i[3] for i in x[1])):
            if shown >= 28:
                print(f"  … 另有 {len(by_sel) - shown} 个元素")
                break
            shown += 1
            head = f"{name} {tail}"
            print(f"  {head}")
            for p, va, vb, d in sorted(items, key=lambda x: -x[3])[:4]:
                print(f"      {p:<22} {va:>8.1f} → {vb:<8.1f}  Δ{d:.1f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
