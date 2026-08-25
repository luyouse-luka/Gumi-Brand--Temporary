#!/usr/bin/env python3
"""Round 31 assertions — one per item in 修改任务文档.txt.

    python3 tools/r31check.py

Every check names the page + width it is measured at, because most of the values
are tier-specific. Anything that cannot be read off computed style (arc shape,
wave position) is verified by screenshot in the round's notes instead.
"""
import os, sys, json
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = os.path.expanduser("~/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome")

# (page, width, selector, property, expected)  expected may be a callable
C = [
    ("pdp.html", 1440, ".gb-nl-tab", "padding", "9px 3px 11px"),
    ("index.html", 1440, ".gb-btn--primary.gb-header__cta", "padding", "0px 42px"),
    ("index.html", 1440, ".gb-header__toggle", "gap", "18px"),
    ("index.html", 1440, ".gb-nav-card__tag", "margin-bottom", "10px"),
    ("index.html", 1440, ".gb-nav-card__tag", "padding", "1px 6px"),
    ("index.html", 1440, ".gb-header", "transition-property", lambda v: "background-color" in v),
    ("index.html", 1440, ".gb-icon-chevron", "transition-duration", "0.35s"),
    ("pdp.html", 1440, ".gb-vs__bear", "transform", lambda v: v.startswith("matrix(0.9702")),
    ("pdp.html", 1440, ".gb-vs__row + .gb-vs__row", "padding-top", "13px"),
    ("pdp.html", 1440, ".gb-vs__value", "padding-right", "1px"),
    ("pdp.html", 1024, ".gb-vs__value", "padding-right", "0px"),
    ("index.html", 1440, ".gb-footer-cta__text", "margin-top", "0px"),
    ("index.html", 1440, ".gb-testimonials", "margin-bottom", "48px"),
    ("index.html", 1440, ".gb-reviews__disclaimer", "margin-top", "0px"),
    ("science.html", 1440, ".gb-science--cream:not(.gb-science--tight)", "padding-bottom", "96px"),
    ("science.html", 1440, ".gb-science--tight .gb-science__inner", "gap", "22px"),
    ("science.html", 1440, ".gb-compare__row", "grid-template-columns", "302px 109px 92px"),
    ("science.html", 1440, ".gb-compare__avatars", "grid-template-columns", "311px 96px 96px"),
    ("science.html", 1440, ".gb-compare__avatar--bear", "transform", lambda v: v.startswith("matrix(1.16138")),
    ("science.html", 1440, ".gb-faq-image__body", "justify-content", "flex-start"),
    ("how-gumi-works.html", 1440, ".gb-dosed__body", "gap", "34px"),
    ("how-gumi-works.html", 390, ".gb-dosed__title", "text-shadow", lambda v: "15px" in v or "14.99" in v),
    ("our-story.html", 1440, ".gb-cta-band__head", "gap", "26px"),
    ("our-story.html", 1440, ".gb-cta-band__content", "padding-top", "54px"),
    ("faq.html", 1440, ".gb-faq--plain", "padding-top", "94px"),
    ("faq.html", 1440, ".gb-faq--plain .gb-faq__item:first-child .gb-faq__row", "padding-top", "0px"),
    ("faq.html", 1440, ".gb-faq--plain .gb-faq__item:first-child .gb-faq__row", "border-top-width", "0px"),
    ("faq.html", 1440, ".gb-acc-body", "padding-top", "10px"),
    ("faq.html", 1440, ".gb-acc-body__text", "font-size", "18px"),
    ("faq.html", 1440, ".gb-acc-body__text", "line-height", "28px"),
    ("faq.html", 1440, ".gb-acc-body__text", "letter-spacing", "-0.36px"),
    ("faq.html", 1440, ".gb-page-hero--center", "padding-top", "64px"),
    ("get-in-touch.html", 1440, ".gb-field__phone select", "padding-right", "23px"),
    ("referral.html", 1440, ".gb-form__note", "letter-spacing", "normal"),
    ("privacy-policy.html", 1440, ".gb-rich-text", "display", "block"),
    ("privacy-policy.html", 1440, ".gb-rich-text > p", "margin-bottom", "20px"),
    # body letter-spacing must be gone, and the nutrition table must track 0
    ("index.html", 1440, "body", "letter-spacing", "normal"),
    ("index.html", 1440, ".gb-nl-table th", "letter-spacing", "normal"),
    # hero: gutters follow --pad-x below 1380, keep the board's 110 above it
    ("index.html", 1440, ".gb-hero__inner", "padding-left", "110px"),
    ("index.html", 1380, ".gb-hero__inner", "padding-left", "80px"),
    ("index.html", 767, ".gb-hero__text", "max-width", "575px"),
    ("index.html", 700, ".gb-hero__btn", "margin-left", "112.5px"),   # auto margins centre it
    ("index.html", 390, ".gb-hero__art", "position", "absolute"),
    ("index.html", 1440, ".gb-hero__art", "position", "absolute"),
    # footer link groups align left once the row wraps
    ("index.html", 900, ".gb-footer__link-groups", "justify-content", "flex-start"),
    ("index.html", 1440, ".gb-footer__link-groups", "justify-content", "flex-end"),
    # cards: one column below 768 with no max-width
    ("science.html", 700, ".gb-science__cards", "max-width", "none"),
    # promo card body paints above the scallop lip
    ("pdp.html", 900, ".gb-promo-card__body", "z-index", "1"),
    # arcs: per-board svg
    ("pdp.html", 1440, ".gb-promo-card__arc.gb-arc-text--pc", "width", "452px"),
    ("pdp.html", 390, ".gb-promo-card__arc.gb-arc-text--pc", "display", "none"),
    ("pdp.html", 390, ".gb-promo-card__arc.gb-arc-text--mob", "width", "278px"),
]

def main():
    bad = 0
    by_page = {}
    for page, w, sel, prop, exp in C:
        by_page.setdefault((page, w), []).append((sel, prop, exp))
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=CHROME)
        for (page, w), items in sorted(by_page.items()):
            pg = br.new_page(viewport={"width": w, "height": 900})
            pg.goto("file://" + os.path.join(ROOT, page))
            pg.evaluate("() => document.fonts.ready")
            pg.wait_for_timeout(250)
            for sel, prop, exp in items:
                got = pg.evaluate(
                    "([s, p]) => { const e = document.querySelector(s);"
                    "  return e ? getComputedStyle(e).getPropertyValue(p) : null; }",
                    [sel, prop])
                if got is None:
                    print(f"❌ {page}@{w} {sel} — 选择器没命中"); bad += 1; continue
                ok = exp(got) if callable(exp) else got == exp
                if not ok:
                    print(f"❌ {page}@{w} {sel} {{{prop}}} = {got!r}, 期望 {exp if not callable(exp) else '(判定函数)'}")
                    bad += 1
            pg.close()
        br.close()
    print(f"\n{len(C)} 条断言：{'✅ 全过' if bad == 0 else f'❌ {bad} 条不过'}")
    return bad

if __name__ == "__main__":
    sys.exit(1 if main() else 0)
