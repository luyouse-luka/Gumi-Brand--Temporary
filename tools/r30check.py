#!/usr/bin/env python3
"""Task 30 regression: the four items from the 2026-09-15 brief.

1 account buttons hover the way the rest of the site does
2 the three grey CSS fills are the exported placeholder image
3 the share icons no longer lift
4 Copy is capped so the code field keeps the row

⚠ Item 1's target is not a taste call: customstyle.scss's .gb-btn comment sets
the house rule (flip to lime, no lift, no fade), so each assertion below reads
the live hover colour rather than trusting the source.

⚠ Item 4 fails silently in source review: .gb-acct-btn is width:100% and
flex-basis:auto resolves off it, so the button took the whole row while every
declaration still looked right. The assertion is the measured input width.
"""
import pathlib
import sys

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / "account.html"
LIME = "rgb(181, 237, 97)"
GREEN900 = "rgb(0, 65, 40)"
ok = red = 0


def _chrome():
    base = pathlib.Path.home() / ".cache/ms-playwright"
    hits = sorted(base.glob("chromium-*/chrome-linux64/chrome"))
    if not hits:
        sys.exit("no chromium under %s -- run: npx playwright install chromium" % base)
    return hits[-1]


def check(label, got, want):
    global ok, red
    if got == want:
        ok += 1
    else:
        red += 1
        print("  RED  %-58s want %r got %r" % (label, want, got))


CS = "([sel, p]) => getComputedStyle(document.querySelector(sel)).getPropertyValue(p)"


def hover_style(pg, sel, props):
    """Resting -> hovered computed values. The pointer is parked afterwards:
    it stays where it landed and Playwright honours (hover: hover), so the next
    measurement would read a hover colour as if it were the resting one."""
    rest = {p: pg.evaluate(CS, [sel, p]) for p in props}
    pg.hover(sel)
    pg.wait_for_timeout(350)
    hov = {p: pg.evaluate(CS, [sel, p]) for p in props}
    pg.mouse.move(0, 0)
    pg.wait_for_timeout(350)
    return rest, hov


def goto(pg, view):
    pg.evaluate("v => { location.hash = '#' + v; }", view)
    pg.wait_for_timeout(500)


def run(pw):
    b = pw.chromium.launch(executable_path=str(_chrome()))
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(PAGE.as_uri())
    pg.wait_for_timeout(400)

    # ── 1 · button hover parity ──────────────────────────────────────────────
    print("1 -- buttons hover like the rest of the site")

    # every one of these faded or darkened before; none of them may do either now
    BTNS = [
        ("overview", ".gb-acct-order__cta", False),
        ("detail",   "[data-acct-view='detail'] .gb-acct-btn:not(.gb-acct-btn--ghost)", True),
        ("detail",   "[data-acct-view='detail'] .gb-acct-btn--ghost", True),
        ("referral", ".gb-acct-referral__copy", True),
    ]
    for view, sel, want_border in BTNS:
        if view == "detail":
            goto(pg, "subscriptions")
            pg.click("[data-acct-view='subscriptions'] .gb-acct-sub__cta[data-acct-goto='detail']")
            pg.wait_for_timeout(500)
        else:
            goto(pg, view)
        name = sel.split()[-1]
        check("anchor: %s is on screen" % name, pg.is_visible(sel), True)
        props = ["background-color", "color", "opacity", "border-top-color"]
        rest, hov = hover_style(pg, sel, props)
        check("%s hovers to lime" % name, hov["background-color"], LIME)
        check("%s ink flips to green-900" % name, hov["color"], GREEN900)
        check("%s does not fade" % name, hov["opacity"], "1")
        check("%s resting fill is not lime" % name, rest["background-color"] != LIME, True)
        if want_border:
            check("%s border travels with the fill" % name,
                  hov["border-top-color"], LIME)

    # Logout only exists on the phone tier
    ph = b.new_page(viewport={"width": 390, "height": 844})
    ph.goto(PAGE.as_uri())
    ph.wait_for_timeout(400)
    check("anchor: Logout is on screen", ph.is_visible(".gb-acct-logout"), True)
    rest, hov = hover_style(ph, ".gb-acct-logout",
                            ["background-color", "color", "border-top-color"])
    check("Logout hovers to lime", hov["background-color"], LIME)
    check("Logout ink flips to green-900", hov["color"], GREEN900)
    check("Logout border travels too", hov["border-top-color"], LIME)
    # the old value; green-on-green is a change the eye does not read
    check("Logout no longer darkens to green-900",
          hov["background-color"] != "rgb(0, 65, 40)", True)

    # a disabled button must not react at all
    goto(pg, "details")
    dis = "[data-acct-view='details'] .gb-acct-btn[data-acct-save]"
    check("anchor: Save starts disabled", pg.eval_on_selector(dis, "e => e.disabled"), True)
    rest, hov = hover_style(pg, dis, ["background-color", "opacity"])
    check("a disabled button ignores hover", hov["background-color"], rest["background-color"])
    check("a disabled button does not fade", hov["opacity"], "1")

    # ── 2 · grey fills are images now ────────────────────────────────────────
    print("2 -- the grey blocks are placeholder images")
    goto(pg, "subscriptions")
    for sel, w, h in ((".gb-acct-sub__thumb", 64, 64),):
        check("%s is an <img>" % sel, pg.eval_on_selector(sel, "e => e.tagName"), "IMG")
        check("%s actually loaded" % sel,
              pg.eval_on_selector(sel, "e => e.naturalWidth > 0"), True)
        check("%s keeps its box" % sel,
              pg.eval_on_selector(sel, "e => [e.offsetWidth, e.offsetHeight]"), [w, h])
        check("%s has no CSS fill left" % sel,
              pg.evaluate(CS, [sel, "background-color"]), "rgba(0, 0, 0, 0)")

    goto(pg, "order")
    it = "[data-acct-view='order'] .gb-acct-item__thumb"
    check("item thumb is an <img>", pg.eval_on_selector(it, "e => e.tagName"), "IMG")
    check("item thumb actually loaded",
          pg.eval_on_selector(it, "e => e.naturalWidth > 0"), True)
    check("item thumb keeps its box",
          pg.eval_on_selector(it, "e => [e.offsetWidth, e.offsetHeight]"), [40, 40])
    check("item thumb has no CSS fill left",
          pg.evaluate(CS, [it, "background-color"]), "rgba(0, 0, 0, 0)")

    goto(pg, "referral")
    hero = ".gb-acct-referral__hero"
    check("hero is an <img>", pg.eval_on_selector(hero, "e => e.tagName"), "IMG")
    check("hero actually loaded", pg.eval_on_selector(hero, "e => e.naturalWidth > 0"), True)
    check("hero has no CSS fill left",
          pg.evaluate(CS, [hero, "background-color"]), "rgba(0, 0, 0, 0)")
    # 400x400 attrs would make it square without the CSS ratio
    check("hero is still 16/9",
          pg.eval_on_selector(hero, "e => Math.abs(e.offsetWidth / e.offsetHeight - 16/9) < 0.02"),
          True)
    check("every thumbnail points at one shared swatch",
          pg.eval_on_selector_all("img[src*='product-placeholder']", "els => els.length"), 14)

    # ── 3 · share icons no longer lift ───────────────────────────────────────
    print("3 -- the share icons hover without moving")
    s = ".gb-acct-referral__social-link"
    check("anchor: four share icons", pg.eval_on_selector_all(s, "e => e.length"), 4)
    rest, hov = hover_style(pg, s, ["transform", "color"])
    check("no lift on hover", hov["transform"], "none")
    check("still changes colour", hov["color"] != rest["color"], True)

    # ── 4 · Copy is capped, the field keeps the row ──────────────────────────
    print("4 -- Copy is capped so the code field is readable")
    row = pg.eval_on_selector(".gb-acct-referral__field", "e => e.offsetWidth")
    cw = pg.eval_on_selector(".gb-acct-referral__copy", "e => e.offsetWidth")
    iw = pg.eval_on_selector("#acct-refer-code", "e => e.offsetWidth")
    check("Copy is capped at 120", cw <= 120, True)
    check("Copy still fits its label",
          pg.eval_on_selector(".gb-acct-referral__copy",
                              "e => e.scrollWidth <= e.clientWidth + 1"), True)
    check("the field now takes most of the row", iw > row * 0.6, True)
    check("the two share the row on one line",
          pg.eval_on_selector_all(".gb-acct-referral__field > *",
                                  "els => new Set(els.map(e => Math.round("
                                  "e.getBoundingClientRect().top))).size"), 1)

    # narrow keeps the deliberate stacked full-width button
    ph.evaluate("() => { location.hash = '#referral'; }")
    ph.wait_for_timeout(500)
    check("on 390 Copy goes back to full width",
          ph.eval_on_selector(".gb-acct-referral__copy",
                              "e => e.offsetWidth === e.parentElement.offsetWidth"), True)

    check("no page errors", errs, [])
    ph.close()
    b.close()


with sync_playwright() as pw:
    run(pw)

print("\nr30: %d ok / %d red" % (ok, red))
sys.exit(1 if red else 0)
