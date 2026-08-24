#!/usr/bin/env python3
"""把 <main> 下的独立波浪搬进它所分隔的**上面那个 section**（一次性脚本）。

用户 2026-08-21 定：波浪要放在对应的 section 模块里 —— 这样 Shopify 上一个 section
模板就能同时吐出模块和它的边缘形状，后台里永远是一条，商家加/删/换序时波浪跟着走。

为什么归**上面**那个 section 而不是下面：nutrition 那道波浪要让上方模块的内容
（包装袋）穿到波浪底下（`.gb-scallop--bleed`），跨不过模块边界，只能归上面。

搬完的形态：

    <section class="gb-product gb-sec-edge gb-sec-edge--lg">
      …
      <div class="gb-scallop gb-scallop--edge gb-scallop--white-to-mint"></div>
    </section>

三件事同时做：
  1. 波浪节点移到宿主 </section> 之前（缩进 +2）
  2. 宿主加 gb-sec-edge（大瓦片再加 --lg；overflow:hidden 的再加 --inset）
  3. 波浪去掉 gb-scallop--lg、加上 gb-scallop--edge
     —— 尺寸改由宿主的 --edge-* 给，一份真值，不会出现「section 说大、波浪说小」

匹配条件是「`</section>` 紧跟着一行波浪」，所以只会命中 <main> 下的那 27 个；
已经在模块内部的 22 个（.gb-hero / .gb-footer-cta-wrap / .gb-footer-wrap）前面
分别是 </div>、另一个 <div> 和 <footer> 开标签，不会被误伤。

    python3 tools/move-scallops.py --dry-run
"""
import io, glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INSET = ("gb-logo-scroll", "gb-nutrition")   # overflow:hidden，border 区会被裁掉
# 有的页在 </section> 与波浪之间空了一行，得允许（漏掉这个会静默少搬两个）
PAT = re.compile(r'</section>\n(?P<gap>(?:[ \t]*\n)*)'
                 r'(?P<ind>[ \t]*)<div class="(?P<cls>gb-scallop[^"]*)"></div>[ \t]*\n')


def owner_open(src, close_idx):
    """从 </section> 往回找配对的 <section …> 开标签。"""
    depth = 0
    region = src[:close_idx + len('</section>')]
    for m in reversed(list(re.finditer(r'<section\b[^>]*>|</section>', region))):
        if m.group(0) == '</section>':
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                return m
    raise AssertionError("找不到配对的 <section>")


def main():
    dry = "--dry-run" in sys.argv
    total = 0
    for f in sorted(glob.glob(os.path.join(ROOT, "*.html"))):
        if os.path.basename(f) == "font-check.html":
            continue
        s = io.open(f, encoding="utf-8").read()
        moved, pos = 0, 0
        while True:
            m = PAT.search(s, pos)
            if not m:
                break
            close_idx = m.start()                                   # </section> 的 '<'
            line_start = s.rfind("\n", 0, close_idx) + 1            # 那一行的行首
            sec_ind = s[line_start:close_idx]
            assert sec_ind.strip() == "", f"{f}: </section> 前有别的东西"

            om = owner_open(s, close_idx)
            oc = re.search(r'class="([^"]*)"', om.group(0))
            assert oc, f"{f}: 宿主 <section> 没有 class"
            owner = oc.group(1).split()
            cls = m.group("cls").split()

            add = ["gb-sec-edge"]
            if "gb-scallop--lg" in cls:
                add.append("gb-sec-edge--lg")
            if any(x in owner for x in INSET):
                add.append("gb-sec-edge--inset")
            new_owner = owner + [a for a in add if a not in owner]

            new_cls = [c for c in cls if c != "gb-scallop--lg"]
            new_cls.insert(1, "gb-scallop--edge")

            if dry:
                print(f'  {os.path.basename(f):22} {" ".join(new_owner):<62} ⇠ {" ".join(new_cls)}')
                pos = m.end()
                moved += 1
                continue

            # ① 先改后面的（下标大的）：删掉原波浪行，把它插到 </section> 行之前
            block = (f'{sec_ind}  <div class="{" ".join(new_cls)}"></div>\n'
                     f'{sec_ind}</section>\n' + m.group("gap"))   # 原来的空行留在 </section> 之后
            s = s[:line_start] + block + s[m.end():]
            # ② 再改前面的（下标小的）宿主开标签
            new_open = om.group(0).replace('class="%s"' % oc.group(1),
                                           'class="%s"' % " ".join(new_owner))
            s = s[:om.start()] + new_open + s[om.end():]
            moved += 1
        if moved and not dry:
            io.open(f, "w", encoding="utf-8").write(s)
        if moved:
            print(f"  {os.path.basename(f):24} {moved} 个")
            total += moved
    print(f"共 {total} 个")


if __name__ == "__main__":
    main()
