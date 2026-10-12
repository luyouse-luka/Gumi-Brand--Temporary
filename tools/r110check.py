#!/usr/bin/env python3
"""r110 asks 4-6, graded on the static build.

  python3 tools/r110check.py

4  .gb-product__taste-list is one per row under 370, side by side at 370+.
5  .gb-crev-card__title is a single clipped line on mobile, unclamped above.
6  The accordion body takes ~450ms to open, not ~300.
"""
import pathlib, sys
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
fails = []


def check(name, got, want):
    ok = got == want
    print(('  ok   ' if ok else '  FAIL ') + name + ('' if ok else f'   got={got!r} want={want!r}'))
    if not ok:
        fails.append(name)


with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME)

    # --- 4. taste list --------------------------------------------------------
    # ⚠ "370px 以下" includes 370, the same way the project's own narrow tier is
    # max-width: 767px. The first width that must NOT stack is 371.
    for w, want_col in ((360, True), (370, True), (371, False), (390, False), (1440, False)):
        ctx = b.new_context(viewport={'width': w, 'height': 900})
        page = ctx.new_page()
        page.goto((ROOT / 'pdp.html').as_uri())
        page.wait_for_timeout(250)
        got = page.evaluate("""() => {
            const l = document.querySelector('.gb-product__taste-list');
            if (!l) return null;
            const items = [...l.children].map(c => Math.round(c.getBoundingClientRect().top));
            return {dir: getComputedStyle(l).flexDirection,
                    // stacked == every item starts on its own row
                    stacked: new Set(items).size === items.length && items.length > 1,
                    n: items.length};
        }""")
        check(f'taste-list @{w:<5} column', got and got['dir'] == 'column', want_col)
        check(f'taste-list @{w:<5} stacked', got and got['stacked'], want_col)
        ctx.close()

    # --- 5. review card title -------------------------------------------------
    for w, want_clip in ((390, True), (1440, False)):
        ctx = b.new_context(viewport={'width': w, 'height': 900})
        page = ctx.new_page()
        for f in ('reviews.html', 'pdp.html'):
            page.goto((ROOT / f).as_uri())
            page.wait_for_timeout(250)
            got = page.evaluate("""() => {
                const t = document.querySelector('.gb-crev-card__title');
                if (!t) return null;
                const cs = getComputedStyle(t);
                return {ws: cs.whiteSpace, ov: cs.overflow, te: cs.textOverflow,
                        lines: Math.round(t.getBoundingClientRect().height /
                                          parseFloat(cs.lineHeight)),
                        // does it actually fit, i.e. is the ellipsis reachable?
                        clipped: t.scrollWidth > t.clientWidth};
            }""")
            check(f'{f:<14} @{w:<5} title nowrap', got and got['ws'] == 'nowrap', want_clip)
            check(f'{f:<14} @{w:<5} title ellipsis', got and got['te'] == 'ellipsis', want_clip)
            check(f'{f:<14} @{w:<5} title one line', got and got['lines'] <= 1, True)
        ctx.close()

    # --- 1. star ink back to the pre-swap size --------------------------------
    # The <img> holds an external SVG, so getBBox() is out of reach. Measure the
    # content box instead and fold in the ink ratio measured off the file itself
    # (new star.svg fills 24.9/25 wide, 23.81/24 tall inside its viewBox).
    INK_W, INK_H, VB_W, VB_H = 24.9, 23.81, 25.0, 24.0
    OLD_INK = {".gb-crev__stars": (25.5, 24.07), ".gb-crev-card__rating": (15.94, 15.04)}
    ctx = b.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.goto((ROOT / "reviews.html").as_uri())
    page.wait_for_timeout(400)
    for sel, (want_w, want_h) in OLD_INK.items():
        got = page.evaluate(
            "(s) => { const c = document.querySelector(s); if (!c) return null;"
            "  const img = c.querySelector('img'); if (!img) return null;"
            "  const r = c.getBoundingClientRect();"
            "  const cs = getComputedStyle(img);"
            "  const px = parseFloat(cs.paddingLeft) + parseFloat(cs.paddingRight);"
            "  const py = parseFloat(cs.paddingTop) + parseFloat(cs.paddingBottom);"
            # ⚠ clientWidth INCLUDES padding -- subtract it for the real content box
            "  return {content: [img.clientWidth - px, img.clientHeight - py],"
            "          box: Math.round(img.getBoundingClientRect().width * 100) / 100,"
            "          row: Math.round(r.width * 10) / 10}; }", sel)
        if not got:
            check(sel + " present", False, True)
            continue
        cw, ch = got["content"]
        k = min(cw / VB_W, ch / VB_H)
        ink = (round(INK_W * k, 2), round(INK_H * k, 2))
        check("%-22s ink back to pre-swap" % sel,
              abs(ink[0] - want_w) < 0.6 and abs(ink[1] - want_h) < 0.6, True)
        print("       ink now %s, pre-swap was (%s, %s), img box still %s, row %s"
              % (ink, want_w, want_h, got["box"], got["row"]))
    # the board's own frame must not have moved
    check("stars row still 160 (board)", page.evaluate(
        "() => Math.round(document.querySelector('.gb-crev__stars').getBoundingClientRect().width)"), 160)
    check("rating row still 100 (board)", page.evaluate(
        "() => Math.round(document.querySelector('.gb-crev-card__rating').getBoundingClientRect().width)"), 100)
    ctx.close()

    # --- 6. accordion duration ------------------------------------------------
    ctx = b.new_context(viewport={'width': 390, 'height': 844})
    page = ctx.new_page()
    page.goto((ROOT / 'faq.html').as_uri())
    page.wait_for_timeout(500)
    got = page.evaluate("""async () => {
        const it = [...document.querySelectorAll('.gb-faq__item')].find(d => !d.open);
        const sum = it.querySelector('summary');
        const dur = parseFloat(getComputedStyle(
            it.querySelector('.gb-acc-body').parentElement).transitionDuration) || null;
        const h = () => Math.round(it.getBoundingClientRect().height);
        const start = h();
        const t0 = performance.now();
        sum.click();
        let settled = null;
        await new Promise(r => {
            let last = start, same = 0, n = 0;
            const loop = () => {
                const cur = h();
                if (cur === last) { if (++same >= 3 && settled === null && cur !== start)
                                        settled = Math.round(performance.now() - t0); }
                else same = 0;
                last = cur;
                if (++n < 70) requestAnimationFrame(loop); else r();
            };
            requestAnimationFrame(loop);
        });
        return {settled, grew: h() > start};
    }""")
    check('accordion actually animates', got['grew'], True)
    # 0.45s + a frame or two of slack; the old 0.3s would land near 300
    check('accordion settles in 400-560ms',
          got['settled'] is not None and 400 <= got['settled'] <= 560, True)
    print(f'       (measured {got["settled"]} ms; was ~250-300 at $t-slow)')
    ctx.close()
    b.close()

print(f'\n{len(fails)} red')
if fails:
    print('RED:'); [print('  -', f) for f in fails]
    sys.exit(1)
