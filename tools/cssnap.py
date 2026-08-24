#!/usr/bin/env python3
"""全站 computed-style 快照 —— CSS 改结构/断点时唯一有效的判据。

    python3 tools/cssnap.py before            # 存快照到 tools/snap/before/
    python3 tools/cssnap.py after             # 存快照
    python3 tools/cssnap.py diff before after # 逐项比对

为什么不 diff 产物：改断点、搬 @media、改选择器名都会让产物文本大变而渲染不变
（见 memory css-refactor-computed-style-judge）。所以判据取「每个元素最终算出来的样式」。

⚠ 伪元素必须一起采 —— 本项目大量视觉由 ::before/::after 承担（扇贝、描边、箭头）。
⚠ 采样宽度默认取两张设计稿的宽度 390 / 1440：迁移断点时这两档必须逐字节不变，
   中间档（576–1280）本来就是要改的，不进不变量。
"""
import json, os, sys, glob, hashlib
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNAP = os.path.join(ROOT, "tools", "snap")
CHROME = os.path.expanduser("~/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome")
WIDTHS = [390, 1440]

# 采这些属性：布局、盒子、排版、装饰。全量 getComputedStyle 有 340+ 项，
# 噪声（如 -webkit-locale）多且慢，取这一组足以抓住任何肉眼可见的变化。
PROPS = """[
 'display','position','top','right','bottom','left','float','clear','z-index',
 'width','height','min-width','max-width','min-height','max-height',
 'margin-top','margin-right','margin-bottom','margin-left',
 'padding-top','padding-right','padding-bottom','padding-left',
 'border-top-width','border-right-width','border-bottom-width','border-left-width',
 'border-top-color','border-right-color','border-bottom-color','border-left-color',
 'border-top-left-radius','border-top-right-radius','border-bottom-left-radius','border-bottom-right-radius',
 'flex-direction','flex-wrap','flex-grow','flex-shrink','flex-basis','order',
 'justify-content','align-items','align-self','align-content','gap','row-gap','column-gap',
 'grid-template-columns','grid-template-rows','grid-column','grid-row',
 'font-family','font-size','font-weight','font-style','line-height','letter-spacing',
 'text-align','text-transform','text-decoration-line','white-space','word-break',
 'color','background-color','background-image','background-size','background-position','background-repeat',
 'opacity','visibility','overflow-x','overflow-y','transform','transform-origin',
 'box-shadow','text-shadow','filter','mix-blend-mode','object-fit','object-position',
 'aspect-ratio','content','mask-image','-webkit-mask-image','pointer-events','cursor'
]"""

PROBE = """(props) => {
  const out = [];
  const els = document.querySelectorAll('body, body *');
  for (let i = 0; i < els.length; i++) {
    const el = els[i];
    if (el.tagName === 'SCRIPT' || el.tagName === 'STYLE') continue;
    // 路径而不是 class：改 class 名的那一轮里 class 本身会变，路径不会
    let path = '', n = el, guard = 0;
    while (n && n.nodeType === 1 && guard++ < 40) {
      const p = n.parentElement;
      const idx = p ? Array.prototype.indexOf.call(p.children, n) : 0;
      path = '/' + n.tagName.toLowerCase() + '[' + idx + ']' + path;
      n = p;
    }
    for (const pe of [null, '::before', '::after']) {
      const cs = getComputedStyle(el, pe);
      if (pe && (cs.content === 'none' || cs.content === 'normal') && cs.display === 'none') continue;
      const rec = {};
      for (const p of props) rec[p] = cs.getPropertyValue(p);
      const r = pe ? null : el.getBoundingClientRect();
      if (r) { rec['#rect'] = [Math.round(r.x*10)/10, Math.round(r.y*10)/10,
                               Math.round(r.width*10)/10, Math.round(r.height*10)/10]; }
      out.push([path + (pe || ''), rec]);
    }
  }
  return out;
}"""


def pages():
    return sorted(os.path.basename(p) for p in glob.glob(os.path.join(ROOT, "*.html")))


def capture(tag):
    out = os.path.join(SNAP, tag)
    os.makedirs(out, exist_ok=True)
    props = json.loads(PROPS.replace("'", '"'))
    with sync_playwright() as pw:
        br = pw.chromium.launch(executable_path=CHROME)
        for w in WIDTHS:
            pg = br.new_page(viewport={"width": w, "height": 900})
            # main.js 的 word-pop / float-art 用 Math.random 撒抖动，不钉死的话
            # 同一份 CSS 连采两次就有 260+ 处「差异」，真信号会被埋掉
            pg.add_init_script("Math.random = function () { return 0.5; };")
            for name in pages():
                pg.goto("file://" + os.path.join(ROOT, name))
                pg.evaluate("() => document.fonts.ready")
                # 入场动画会把 opacity 停在中途 —— 全部关掉再采，
                # 否则同一份 CSS 两次采样都对不上（见 memory headless-transition-reads-start-value）
                pg.add_style_tag(content="*,*::before,*::after{animation:none!important;"
                                         "transition:none!important;opacity:1!important}")
                pg.wait_for_timeout(120)
                data = pg.evaluate(PROBE, props)
                with open(os.path.join(out, f"{name}.{w}.json"), "w") as f:
                    json.dump(data, f, sort_keys=True)
                print(f"  {tag} {name} @{w}: {len(data)} 项")
            pg.close()
        br.close()


def diff(a, b):
    bad = 0
    for w in WIDTHS:
        for name in pages():
            pa = os.path.join(SNAP, a, f"{name}.{w}.json")
            pb = os.path.join(SNAP, b, f"{name}.{w}.json")
            if not (os.path.exists(pa) and os.path.exists(pb)):
                print(f"!! 缺快照 {name}@{w}")
                bad += 1
                continue
            da = dict(json.load(open(pa)))
            db = dict(json.load(open(pb)))
            keys = set(da) | set(db)
            hits = []
            for k in sorted(keys):
                if k not in da:
                    hits.append((k, "只在 " + b, "", ""))
                    continue
                if k not in db:
                    hits.append((k, "只在 " + a, "", ""))
                    continue
                for p in sorted(set(da[k]) | set(db[k])):
                    va, vb = da[k].get(p), db[k].get(p)
                    if va != vb:
                        hits.append((k, p, va, vb))
            if hits:
                bad += len(hits)
                print(f"\n## {name} @{w} —— {len(hits)} 处不同")
                for k, p, va, vb in hits[:25]:
                    print(f"   {k}\n      {p}: {va}  ->  {vb}")
                if len(hits) > 25:
                    print(f"   … 另有 {len(hits)-25} 处")
    print(f"\n{'✅ 完全一致' if bad == 0 else f'❌ 共 {bad} 处差异'}")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] == "diff":
        sys.exit(diff(sys.argv[2], sys.argv[3]))
    if len(sys.argv) == 2:
        capture(sys.argv[1])
        sys.exit(0)
    print(__doc__)
    sys.exit(2)
