#!/usr/bin/env python3
"""定位断点边界上的数值跳变到底出自哪个 class（第二十九轮）。

r29edge.py 用快照路径报「哪个元素在跳」，但路径反推不出 CSS 规则。
这个直接开两个视口读 class + computed style，按 class 聚合，
输出可以直接拿去 grep 的选择器名。

    python3 tools/r29jump.py            # 默认 767 → 768
    python3 tools/r29jump.py 991 992
"""
import os, sys
from collections import defaultdict
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = os.path.expanduser("~/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome")
PROPS = ["font-size", "line-height", "letter-spacing", "gap",
         "padding-top", "padding-bottom", "padding-left", "padding-right",
         "border-top-left-radius"]

# ⚠ 配对必须用 DOM 路径，不能用遍历顺序。lineReveal 按当前宽度把段落拆成
#   逐行遮罩，两个宽度下生成的包装元素个数不同 —— 用 zip 按顺序配对会从第一处
#   分行差异起整体错位，之后每一条都是假的（实测报出 .gb-page-hero__lead
#   「16→18」，而该元素两档实际都是 18）。
#   同理跳过 lineReveal 自己生成的元素：它们只是继承宿主的排版值。
SKIP = "gb-line-mask,gb-line-mask__inner,gb-line-word"
PROBE = """([props, skip]) => {
  const bad = new Set(skip.split(','));
  const out = [];
  for (const el of document.querySelectorAll('body *')) {
    if (el.tagName === 'SCRIPT' || el.tagName === 'STYLE') continue;
    const cls = (el.className && typeof el.className === 'string') ? el.className : '';
    if (cls.split(/\\s+/).some(c => bad.has(c))) continue;
    let path = '', n = el, guard = 0;
    while (n && n.nodeType === 1 && guard++ < 40) {
      const p = n.parentElement;
      // 兄弟里排除 lineReveal 的包装，否则下标仍会随分行数漂移
      const sibs = p ? [...p.children].filter(s => {
        const c = (s.className && typeof s.className === 'string') ? s.className : '';
        return !c.split(/\\s+/).some(x => bad.has(x));
      }) : [];
      path = '/' + n.tagName.toLowerCase() + '[' + Math.max(0, sibs.indexOf(n)) + ']' + path;
      n = p;
    }
    const cs = getComputedStyle(el);
    const rec = {};
    for (const p of props) rec[p] = cs.getPropertyValue(p);
    out.push([path, cls || el.tagName.toLowerCase(), rec]);
  }
  return out;
}"""


def px(v):
    if not v or not v.endswith("px"):
        return None
    try:
        return float(v[:-2])
    except ValueError:
        return None


def main():
    lo, hi = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) == 3 else (767, 768)
    pages = sorted(f for f in os.listdir(ROOT) if f.endswith(".html"))
    # class -> prop -> {(lo值, hi值)}
    jumps = defaultdict(lambda: defaultdict(set))
    with sync_playwright() as pw:
        br = pw.chromium.launch(executable_path=CHROME)
        for name in pages:
            snap = {}
            for w in (lo, hi):
                pg = br.new_page(viewport={"width": w, "height": 900})
                pg.add_init_script("Math.random = function(){return 0.5};")
                pg.goto("file://" + os.path.join(ROOT, name))
                pg.evaluate("() => document.fonts.ready")
                pg.add_style_tag(content="*,*::before,*::after{animation:none!important;"
                                         "transition:none!important;opacity:1!important}")
                pg.wait_for_timeout(80)
                snap[w] = {path: (cls, rec) for path, cls, rec in pg.evaluate(PROBE, [PROPS, SKIP])}
                pg.close()
            only = len(set(snap[lo]) ^ set(snap[hi]))
            if only:
                print(f"!! {name}: {only} 个元素只在单侧出现，这些不参与比对")
            for path in set(snap[lo]) & set(snap[hi]):
                cls_a, ra = snap[lo][path]
                cls_b, rb = snap[hi][path]
                if cls_a != cls_b:
                    continue
                for p in PROPS:
                    va, vb = px(ra.get(p)), px(rb.get(p))
                    if va is None or vb is None:
                        continue
                    d = abs(vb - va)
                    if d <= 0.5 or d / max(abs(va), abs(vb), 1.0) <= 0.02:
                        continue
                    key = " ".join(c for c in cls_a.split() if c.startswith("gb-")) or cls_a
                    jumps[key][p].add((round(va, 1), round(vb, 1)))
        br.close()

    rows = sorted(jumps.items(), key=lambda kv: -max(
        abs(b - a) for pv in kv[1].values() for a, b in pv))
    print(f"\n{lo} → {hi}：{len(rows)} 个 class 上有数值跳变\n")
    print("%-42s %-18s %s" % ("class", "属性", f"{lo} → {hi}"))
    print("-" * 88)
    for cls, props in rows:
        first = True
        for p, pairs in sorted(props.items()):
            for a, b in sorted(pairs):
                print("%-42s %-18s %g → %g" % (cls[:42] if first else "", p, a, b))
                first = False
    return 0


if __name__ == "__main__":
    sys.exit(main())
