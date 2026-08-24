#!/usr/bin/env python3
"""给每条规则补一层平板（576–1280）的数值插值。一次性脚本，跑完就该看 diff。

背景：断点改制后 ≤1280 全部走 @include narrow，也就是**平板拿的是手机稿的数值**。
布局这样是对的（都是单列/堆叠），但字号、间距、内距不对 —— 1280 宽的屏上用 390 稿的
30px 标题明显偏小。

做法：对每条规则，把它 narrow 块里的**纯长度声明**和基础规则里同名声明配对，
生成 `@include tablet { prop: fluid($手机值, $桌面值) }` 插在 narrow 块后面。
fluid() 在 576 处等于手机值、1281 处等于桌面值，中间线性 —— 两张稿都命中，
中间那段不是拍脑袋填的。

只动**直接声明**，不进嵌套选择器；只处理 px / 0 的值；基础规则里没有同名声明的跳过
（那种属性在 PC 档根本不设，插值没有意义）。布局类属性一律不碰，它们该在 narrow 里
对所有窄屏一视同仁。
"""
import re, sys, os

SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "assets", "customstyle.scss")

# 会插值的属性。刻意不含 display / flex-direction / grid-template-columns 这类
# 布局开关 —— 它们是「窄屏怎么排」，不是「多大」，插值没有意义。
RAMP = {
    "font-size", "line-height", "letter-spacing",
    "gap", "row-gap", "column-gap",
    "padding", "padding-top", "padding-right", "padding-bottom", "padding-left",
    "padding-inline", "padding-block",
    "margin-top", "margin-bottom",
    "width", "height", "min-height", "max-height", "flex-basis",
    "border-radius", "top", "right", "bottom", "left",
}
LEN = re.compile(r"^-?\d*\.?\d+px$|^0$")


def tokens(v):
    """把 `64px 0 48px` 拆成 4 个长度；有任何一项不是 px/0 就返回 None。"""
    parts = v.split()
    if not 1 <= len(parts) <= 4:
        return None
    if not all(LEN.match(p) for p in parts):
        return None
    if len(parts) == 1:
        parts = parts * 4
    elif len(parts) == 2:
        parts = [parts[0], parts[1], parts[0], parts[1]]
    elif len(parts) == 3:
        parts = [parts[0], parts[1], parts[2], parts[1]]
    return parts


def arity(v):
    return len(v.split())


def split_body(body):
    """把一段 { … } 的内容按顶层切成 (kind, text) —— kind 是 'decl' 或 'block'。"""
    out, depth, buf = [], 0, ""
    for ch in body:
        buf += ch
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                out.append(("block", buf)); buf = ""
        elif ch == ";" and depth == 0:
            out.append(("decl", buf)); buf = ""
    if buf.strip():
        out.append(("tail", buf))
    return out


def decls_of(text):
    """顶层声明 → {prop: value}，后出现的覆盖先出现的（层叠就是这个顺序）。"""
    got = {}
    for kind, t in split_body(text):
        if kind != "decl":
            continue
        line = re.sub(r"//.*", "", t).strip().rstrip(";").strip()
        if ":" not in line or line.startswith("@") or line.startswith("//"):
            continue
        prop, _, val = line.partition(":")
        prop, val = prop.strip(), val.strip()
        if prop and not prop.startswith("--") and not prop.startswith("&"):
            got[prop] = val
    return got


def find_rules(src):
    """顶层 `选择器 { … }`，返回 (start, brace_open, brace_close)。"""
    i, n = 0, len(src)
    while i < n:
        if src[i] == "{":
            # 往前找选择器起点
            j = src.rfind("\n", 0, i)
            depth, k = 1, i + 1
            while k < n and depth:
                if src[k] == "{": depth += 1
                elif src[k] == "}": depth -= 1
                k += 1
            yield (j + 1, i, k - 1)
            i = k
        else:
            i += 1


def main():
    src = open(SRC).read()
    # 只处理「输出段」，变量与 mixin 定义段不动
    head_end = src.index("// 原 helpers/_mixins.scss 的 :root 输出块")
    head, body = src[:head_end], src[head_end:]

    edits = []      # (插入位置, 文本)
    touched = 0
    for start, bo, bc in find_rules(body):
        sel = body[start:bo].strip()
        if sel.startswith("@") or "{" in sel or not sel:
            continue
        inner = body[bo + 1:bc]
        base = decls_of(inner)
        if not base:
            continue
        # 找这条规则里所有顶层的布局阈值块。narrow(≤768) 装的是手机稿数值，
        # 是插值的下锚点；stack(≤1024) / tight(≤1200) 是**有意写给那两段**的值，
        # 它们设过的属性一律不插值 —— 插了就是把作者写死的中间态抹掉。
        narrows, held = [], set()
        off = bo + 1
        for kind, t in split_body(inner):
            if kind == "block":
                # ⚠ 注释行没有分号，会被 split_body 粘在后面那个块的前面。
                # 直接 t.strip().startswith("@include narrow") 会漏掉所有
                # 「上一行有注释」的块 —— 本文件里这种占了近四成。
                st = re.sub(r"^(\s*//[^\n]*\n)+", "", t).strip()
                inner_body = st[st.index("{") + 1:st.rindex("}")] if "{" in st else ""
                if st.startswith("@include narrow"):
                    narrows.append((off, off + len(t), inner_body))
                elif st.startswith("@include stack") or st.startswith("@include tight"):
                    held |= set(decls_of(inner_body))
                    narrows.append((off, off + len(t), None))   # 只用来定位插入点
            off += len(t)
        if not any(t for _, _, t in narrows):
            continue
        eff = {}
        for _, _, t in narrows:
            if t:
                eff.update(decls_of(t))
        ramps = []
        for prop, mval in eff.items():
            if prop not in RAMP or prop not in base or prop in held:
                continue
            dval = base[prop]
            if mval == dval:
                continue
            mt, dt = tokens(mval), tokens(dval)
            if not mt or not dt or arity(mval) != arity(dval):
                continue
            k = arity(mval)
            vals = [f"fluid({m}, {d})" for m, d in zip(mt[:k], dt[:k])]
            ramps.append(f"{prop}: {' '.join(vals)};")
        if not ramps:
            continue
        touched += 1
        # 插在最后一个阈值块后面 —— 同特异性、更靠后，平板段才压得住
        block = "\n  @include tablet { " + " ".join(ramps) + " }"
        edits.append((narrows[-1][1], block))

    for pos, text in sorted(edits, reverse=True):
        body = body[:pos] + text + body[pos:]

    open(SRC, "w").write(head + body)
    print(f"补了 {touched} 条规则的平板插值层")


if __name__ == "__main__":
    main()
