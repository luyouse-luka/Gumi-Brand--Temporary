"""全站：任何 [data-line-reveal] 元素的行盒数必须等于文字行数。
多出的行盒 = 行尾有不可折叠的空白（U+00A0）把自己挤到了下一行 —— 第 10 条那个病。"""
import os, sys
from playwright.sync_api import sync_playwright
ROOT = "/home/ly/project/Gumi-Brand"
CHROME = os.path.expanduser("~/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome")
SETTLE = (".wowo,.gb-float-art,[data-line-reveal],.gb-line-mask__inner,.gb-ink-halo{"
          "opacity:1!important;transform:none!important;animation:none!important}")
PROBE = r"""() => {
  const bad = [], seen = [];
  document.querySelectorAll('[data-line-reveal]').forEach(h => {
    const words = [...h.querySelectorAll('.gb-line-word')];
    if (!words.length) return;
    const lh = parseFloat(getComputedStyle(h).lineHeight);
    if (!lh) return;
    const r = h.getBoundingClientRect();
    const boxes = Math.round(r.height / lh);
    /* ⚠ 两个都不能直接数：
       - .gb-line-word 的 offsetTop —— 词是 inline-block，自己内部折行时仍只有一个
         top，视觉上却是两行（science 的 "Aussie-approved." 在 1281 就是这样）。
       - 整个元素的 Range —— .gb-ink-halo 是同一份文案的描边副本，会把行数翻倍。
       取「内容层的词」的 Range 行盒，并按容差聚类吸收亚像素差。 */
    const tops = [];
    words.forEach(w => {
      if (w.closest('.gb-ink-halo')) return;
      const rg = document.createRange(); rg.selectNodeContents(w);
      for (const rr of rg.getClientRects()) {
        if (rr.width > 0.5 && rr.height > 0.5) tops.push(rr.top);
      }
    });
    tops.sort((p, q) => p - q);
    let lines = 0, last = -1e9;
    for (const t of tops) { if (t - last > 3) { lines++; last = t; } }
    seen.push(1);
    if (boxes !== lines) bad.push({cls: (h.className||'').split(' ')[0],
                                   boxes, lines, h: +r.height.toFixed(1), lh});
  });
  return {n: seen.length, bad};
}"""
pages = [p for p in sorted(os.listdir(ROOT)) if p.endswith(".html") and not p.startswith("_")]
widths = [int(x) for x in sys.argv[1].split(",")]
fails, checked = [], 0
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=CHROME)
    for page in pages:
        for w in widths:
            pg = b.new_page(viewport={"width": w, "height": 1000})
            pg.goto("file://" + os.path.join(ROOT, page))
            pg.add_style_tag(content=SETTLE)
            pg.evaluate("() => document.fonts.ready")
            pg.evaluate("() => document.querySelectorAll('[data-line-reveal]').forEach(e => e.scrollIntoView())")
            pg.wait_for_timeout(520)
            d = pg.evaluate(PROBE); pg.close()
            checked += d["n"]
            for x in d["bad"]:
                fails.append("%-22s @%-5d %-26s %d 个行盒 / %d 行文字 (h=%s lh=%s)"
                             % (page, w, x["cls"], x["boxes"], x["lines"], x["h"], x["lh"]))
    b.close()
print("=" * 76)
print("检查了 %d 个 [data-line-reveal]×档位 组合" % checked)
if fails:
    print("FAIL — %d 处有多余空行盒：" % len(fails))
    for f in fails[:40]: print("  ✗", f)
else:
    print("全过：没有任何行揭示元素出现多余的空行盒")
print("=" * 76)
raise SystemExit(1 if fails else 0)
