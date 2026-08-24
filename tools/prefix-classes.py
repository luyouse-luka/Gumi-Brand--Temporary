#!/usr/bin/env python3
"""给全站模块类加 gb- 前缀（任务文档第 7 条）。一次性脚本，跑完看 diff + computed-style 判据。

为什么要前缀：上 Shopify 主题后，.product / .reviews / .faq / .header / .btn / .field
这种通用词跟主题自带样式和 app 注入的样式撞名是迟早的事，撞了以后是「线上偶发错乱」，
最难查。加前缀是一次性买断。

**不改**动效与状态工具类 —— main.js 与 Terra 的 wowo 约定都挂在这些名字上：
  wowo / animated / fadeIn* / zoomIn / zoomOut / bounceIn / delay-in-N
  is-* / no-js / js
font-check.html 里的 ok / bad / lbl / sub 是那一页自带 <style> 的页内类，不进主题，也不改。

改名范围按「块名」走：一个块名 B 连带它所有 B__元素 / B--修饰 一起改。
匹配用 (?<![\\w-])B(?=__|--|非单词字符)，所以 footer 不会误伤 footer-cta
（后者自己也在名单里，且按长度倒序先匹配）。

HTML 只动 class="…" 里的 token；SCSS/CSS 只动 `.B` 这种选择器写法（避免把注释里的
英文单词 product / header 也改了）；JS 里改的是明确列出的那几处。
"""
import re, os, sys, glob, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 不加前缀的（用户 2026-08-21 指定）
KEEP = {
    "wowo", "animated", "no-js", "js",
    "fadeIn", "fadeInUp", "fadeInDown", "fadeInLeft", "fadeInRight",
    "zoomIn", "zoomOut", "bounceIn",
    # font-check.html 页内类
    "ok", "bad", "lbl", "sub",
}
KEEP_PREFIX = ("is-", "delay-in-", "has-")


def block_of(token):
    return re.split(r"__|--", token, 1)[0]


# HTML 里永远不会出现、但确实是我们的类（JS 运行时生成的）
EXTRA = {"pop-word"}          # popText 模块把每个词包进 <span class="pop-word">


def collect_blocks():
    names = set(EXTRA)
    for f in glob.glob(os.path.join(ROOT, "*.html")):
        for m in re.finditer(r'class="([^"]*)"', open(f).read()):
            for t in m.group(1).split():
                names.add(block_of(t))
    # SCSS 里可能有 HTML 还没用上的块（例如给客户图预留的 .reel__media-img）
    scss = open(os.path.join(ROOT, "assets", "customstyle.scss")).read()
    used = {block_of(m.group(1)) for m in re.finditer(r"(?<![\w-])\.([a-zA-Z][\w-]*)", scss)}
    names |= {n for n in used if n in names or any(
        re.search(r"(?<![\w-])\.%s(__|--)" % re.escape(n), scss) for _ in [0])}
    out = set()
    for n in names:
        if n in KEEP or n.startswith(KEEP_PREFIX) or n.startswith("gb-"):
            continue
        if not re.fullmatch(r"[a-zA-Z][\w-]*", n):
            continue
        out.add(n)
    return sorted(out, key=lambda s: (-len(s), s))


def make_re(names):
    alt = "|".join(re.escape(n) for n in names)
    return re.compile(r"(?<![\w-])(%s)(?=__|--|[^\w-]|$)" % alt)


def main():
    names = collect_blocks()
    rx = make_re(names)
    print(f"要加前缀的块名 {len(names)} 个：")
    print("  " + " ".join(names))
    if "--dry-run" in sys.argv:
        return

    counts = {}

    # 1) HTML —— 只动 class="…"
    for f in sorted(glob.glob(os.path.join(ROOT, "*.html"))):
        s = open(f).read()
        n = [0]

        def fix_attr(m):
            toks = m.group(1).split()
            new = []
            for t in toks:
                b = block_of(t)
                if b in names:
                    new.append("gb-" + t); n[0] += 1
                else:
                    new.append(t)
            return 'class="%s"' % " ".join(new)

        s = re.sub(r'class="([^"]*)"', fix_attr, s)

        # 页内 <style> 和探针脚本里的选择器也要跟着改 —— font-check.html 自带
        # 一段 <style>（.banner / .spec）和十几处 querySelector('.hero__bear')，
        # 只改 class 属性会让那一页的样式和自检探针一起变成假阴性。
        sel_rx = re.compile(r"(?<![\w-])\.(%s)(?=__|--|[^\w-]|$)"
                            % "|".join(re.escape(x) for x in names))

        def fix_sel(m):
            inner, c = sel_rx.subn(lambda q: ".gb-" + q.group(1), m.group(0))
            n[0] += c
            return inner

        s = re.sub(r"<style\b.*?</style>", fix_sel, s, flags=re.S)
        s = re.sub(r"(?:querySelector|querySelectorAll|closest|matches)\((['\"])[^'\"]*\1\)",
                   fix_sel, s)
        open(f, "w").write(s)
        counts[os.path.basename(f)] = n[0]

    # 2) SCSS —— 只动 `.名字`
    p = os.path.join(ROOT, "assets", "customstyle.scss")
    s = open(p).read()
    s, k = re.subn(r"(?<![\w-])\.(%s)(?=__|--|[^\w-]|$)" % "|".join(re.escape(x) for x in names),
                   lambda m: "." + "gb-" + m.group(1), s)
    open(p, "w").write(s)
    counts["customstyle.scss"] = k

    # 3) JS —— 逐处点名，别用正则扫（"pop-word" 这种是拼出来的，不是选择器）
    p = os.path.join(ROOT, "assets", "main.js")
    s = open(p).read()
    js_map = [
        ('querySelectorAll(".bear-meter")', 'querySelectorAll(".gb-bear-meter")'),
        ('"bear-meter__bear"', '"gb-bear-meter__bear"'),
        ('querySelector(".header__link")', 'querySelector(".gb-header__link")'),
        ('querySelector(".header__toggle")', 'querySelector(".gb-header__toggle")'),
        ('span.className = "pop-word";', 'span.className = "gb-pop-word";'),
        ('el.classList.add("pop-word");', 'el.classList.add("gb-pop-word");'),
    ]
    jn = 0
    for a, b in js_map:
        if a not in s:
            print(f"!! main.js 里找不到：{a}")
        else:
            s = s.replace(a, b); jn += s.count(b)
    open(p, "w").write(s)
    counts["main.js"] = jn

    for k2, v in counts.items():
        print(f"  {k2:28} {v}")


if __name__ == "__main__":
    main()
