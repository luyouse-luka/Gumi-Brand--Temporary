#!/usr/bin/env python3
"""Task 34 -- the 2026-09-16 07:06 requirement doc.

Seven values, so most of this is computed-style reads. The two that need a
browser rather than a grep:
  * the auth links now answer the pointer with colour, not opacity -- the read
    has to happen with the pointer actually resting on the link
  * .gb-header__cta is customstyle's, and only wins here because account.css
    loads after it. Asserting the 32 without also asserting the MVP pages still
    read 40 would let a customstyle edit pass as this change.
"""
import sys, pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
LIME = "rgb(181, 237, 97)"     # #b5ed61
CREAM = "rgb(250, 249, 248)"   # #faf9f8

ok = red = 0


def _chrome():
    base = pathlib.Path.home() / ".cache/ms-playwright"
    hits = sorted(base.glob("chromium-*/chrome-linux64/chrome"))
    if not hits:
        sys.exit("no chromium under %s" % base)
    return hits[-1]


def check(label, got, want):
    global ok, red
    if got == want:
        print("ok   %-56s %s" % (label, got)); ok += 1
    else:
        print("RED  %-56s got %r want %r" % (label, got, want)); red += 1


def css(pg, sel, prop):
    return pg.eval_on_selector(sel, "(e,p)=>getComputedStyle(e)[p]", prop)


def run_login(b):
    pg = b.new_page(viewport={"width": 1440, "height": 950})
    pg.goto((ROOT / "account-login.html").as_uri())
    pg.wait_for_timeout(500)

    # --- 1: the two auth links colour instead of fading --------------------
    for sel, tag in (("a.gb-acct-auth__aside", "aside"),
                     (".gb-acct-auth__alt a", "alt")):
        check("anchor: %s exists" % tag, pg.locator(sel).count() >= 1, True)
        rest = [css(pg, sel, "color"), css(pg, sel, "opacity")]
        check("%s at rest is not lime" % tag, rest[0] != LIME, True)
        check("%s at rest is fully opaque" % tag, rest[1], "1")
        pg.hover(sel)
        pg.wait_for_timeout(500)
        check("%s goes lime on hover" % tag, css(pg, sel, "color"), LIME)
        check("%s no longer fades" % tag, css(pg, sel, "opacity"), "1")
        # a colour change with no transition is a half-done state (rule 13)
        check("%s eases the colour" % tag,
              "color" in css(pg, sel, "transitionProperty"), True)
        pg.mouse.move(0, 0)
        pg.wait_for_timeout(500)
    check("the aside starts the row, not stretched",
          css(pg, "a.gb-acct-auth__aside", "alignSelf"), "flex-start")

    # --- 3: header CTA + note width ---------------------------------------
    check("header CTA padding", css(pg, ".gb-header__cta", "padding"), "0px 32px")
    check("note width", css(pg, ".gb-acct-auth__note", "width"), "472px")
    # ⚠ the form beside it keeps 480 -- they used to share one rule
    check("the block above it keeps 480",
          css(pg, ".gb-acct-auth__alt", "width"), "480px")
    pg.close()


def run_mvp(b):
    """The override must not have leaked onto the main line."""
    pg = b.new_page(viewport={"width": 1440, "height": 950})
    pg.goto((ROOT / "index.html").as_uri())
    pg.wait_for_timeout(400)
    check("anchor: the MVP page has the same CTA",
          pg.locator(".gb-header__cta").count() >= 1, True)
    check("MVP pages still read the client's 40",
          css(pg, ".gb-header__cta", "padding"), "0px 40px")
    pg.close()


def run_account(b):
    pg = b.new_page(viewport={"width": 1440, "height": 950})
    pg.goto((ROOT / "account.html").as_uri())
    pg.wait_for_timeout(500)

    # --- 2: the wave under the green band ---------------------------------
    check("anchor: the to-green wave is in the page",
          pg.locator(".gb-scallop--to-green").count() >= 1, True)
    check("--wave-bg is cream",
          pg.eval_on_selector(".gb-scallop--to-green",
                              "e=>getComputedStyle(e).getPropertyValue('--wave-bg').trim()"),
          "#faf9f8")

    # --- 4: three spacing values ------------------------------------------
    check("header icons gap", css(pg, ".gb-acct-header__icons", "columnGap"), "24px")
    pg.evaluate("() => { location.hash = '#subscriptions'; }")
    pg.wait_for_timeout(700)
    check("subscription card row-gap",
          css(pg, "[data-acct-view='subscriptions'] .gb-acct-sub__body", "rowGap"), "23.5px")
    pg.evaluate("() => { location.hash = '#detail'; }")
    pg.wait_for_timeout(700)
    check("schedule days padding",
          css(pg, "[data-acct-view='detail'] .gb-acct-schedule__days", "padding"), "0px 4px")
    # the 4 is inside the row, so the days must not have got narrower boxes than
    # the row they sit in -- a padding that clips is worse than no padding
    fits = pg.eval_on_selector(
        "[data-acct-view='detail'] .gb-acct-schedule__days",
        "e => e.scrollWidth <= e.clientWidth + 1")
    check("and nothing overflows because of it", fits, True)

    # --- 4b: the nav dot, drawn in CSS (34631) ----------------------------
    pg.evaluate("() => { location.hash = '#overview'; }")
    pg.wait_for_timeout(600)
    rows = pg.eval_on_selector_all(
        ".gb-acct-nav__link",
        """els => els.map(e => { const d = getComputedStyle(e, '::before');
             return [d.content, d.width, d.height, d.backgroundColor, d.borderTopLeftRadius]; })""")
    check("anchor: every nav row is there", len(rows), 9)
    # ⚠ 16.67 authored reads back as 16.6562 -- Chrome snaps lengths to 1/64px.
    # Asserting "16.67px" here reds on a correct file.
    DOT = ['""', "16.6562px", "16.6562px", "rgb(217, 217, 217)", "50%"]
    bad = [r for r in rows if r != DOT]
    check("every row draws the same 16.67 dot in #d9d9d9", bad, [])
    # the board starts the label at 48 from the row's left edge: 16 + 20 + 12
    label = pg.eval_on_selector(
        ".gb-acct-nav__link",
        """e => { const r = document.createRange(); r.selectNodeContents(e);
             return Math.round(r.getBoundingClientRect().left
                               - e.getBoundingClientRect().left); }""")
    check("the label still starts at 48", label, 48)
    # ⚠ a pseudo-element is invisible to the text judges; make sure it did not
    # push the row taller or make it scroll
    geo = pg.eval_on_selector(".gb-acct-nav__link",
                              "e => [Math.round(e.getBoundingClientRect().height),"
                              " e.scrollWidth <= e.clientWidth + 1]")
    check("row height unchanged and nothing overflows", geo, [40, True])
    # the disabled row keeps the dot -- all nine are identical on the board
    dis = pg.eval_on_selector('.gb-acct-nav__link[aria-disabled="true"]',
                              "e => getComputedStyle(e, '::before').backgroundColor")
    check("the disabled row keeps its dot too", dis, "rgb(217, 217, 217)")
    pg.close()


def main():
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=str(_chrome()))
        run_login(b)
        run_mvp(b)
        run_account(b)
        b.close()
    print("\nacct34: %d ok / %d red" % (ok, red))
    sys.exit(1 if red else 0)


main()
