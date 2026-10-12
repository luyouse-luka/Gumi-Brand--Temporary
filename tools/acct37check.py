#!/usr/bin/env python3
"""Task 37 -- the chevron in .gb-acct-prod__control, and Close on shipping-success.

Both need a browser, not a grep:
  * .gb-select is drawn by main.js at runtime, so the arrow only exists once
    selectBox has run -- reading the stylesheet would read a rule with no
    element under it. The 20 is now the shared base value, so the invariant is
    "the product control matches a plain field control", not a bare 20.
  * the Close button steps to another panel instead of closing, so the assertion
    is which panel is open afterwards AND that the page is still locked. The
    cross keeps closing for real -- asserted here so a later "tidy up" that
    rewires both shows as red.
"""
import sys, pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROD = ".gb-acct-prod__control .gb-select__arrow"
FIELD = "[data-acct-modal-panel='shipping-form'] .gb-acct-field__control .gb-select__arrow"

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
        print("ok   %-58s %s" % (label, got)); ok += 1
    else:
        print("RED  %-58s got %r want %r" % (label, got, want)); red += 1


def css(pg, sel, prop):
    return pg.eval_on_selector(sel, "(e,p)=>getComputedStyle(e)[p]", prop)


def open_page(b, width):
    pg = b.new_page(viewport={"width": width, "height": 950})
    pg.goto((ROOT / "account.html").as_uri() + "#detail")
    pg.wait_for_timeout(600)
    return pg


def run_arrow(b, width):
    """1 -- the product-tier chevron is back to the shared 20."""
    pg = open_page(b, width)
    tag = "@%d" % width

    pg.click("[data-acct-modal='edit-product']")
    pg.wait_for_timeout(600)
    pg.mouse.move(0, 0)   # click leaves the pointer on the trigger; hover is live here

    # anchor: without selectBox there is no .gb-select at all and every
    # absent-element read below would pass vacuously.
    check("%s selectBox ran (prod arrows exist)" % tag,
          pg.locator(PROD).count() > 0, True)
    for prop, want in (("width", "20px"), ("height", "20px")):
        check("%s prod chevron %s" % (tag, prop), css(pg, PROD, prop), want)
    # flex-basis is what the old rule actually set; computed must not be 10px
    check("%s prod chevron flex-basis" % tag, css(pg, PROD, "flexBasis"), "20px")
    # the rest of the small tier must NOT have followed the arrow back up
    check("%s prod button still 40 tall" % tag,
          css(pg, ".gb-acct-prod__control .gb-select__button", "height"), "40px")
    check("%s prod button still 14px text" % tag,
          css(pg, ".gb-acct-prod__control .gb-select__button", "fontSize"), "14px")

    pg.keyboard.press("Escape")
    pg.wait_for_timeout(500)

    # invariant: a generic field control in another panel reads the same 20, so
    # the product control is no longer a special case rather than re-pinned to a
    # number that happens to match.
    pg.click("[data-acct-modal='shipping-current']")
    pg.wait_for_timeout(500)
    pg.click("[data-acct-modal-panel='shipping-current'] [data-acct-modal='shipping-form']")
    pg.wait_for_timeout(600)
    check("%s generic field chevron exists" % tag, pg.locator(FIELD).count() > 0, True)
    check("%s prod chevron == generic field chevron" % tag,
          css(pg, PROD, "width") == css(pg, FIELD, "width"), True)
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(500)
    pg.close()


def run_close(b, width):
    """2 -- Close on shipping-success steps back to Current Address."""
    pg = open_page(b, width)
    tag = "@%d" % width

    def open_panel(pg):
        return pg.evaluate(
            "()=>{var e=document.querySelector('.gb-acct-modal.is-open');"
            "return e?e.getAttribute('data-acct-modal-panel'):null}")

    def locked(pg):
        return pg.evaluate(
            "()=>document.documentElement.classList.contains('is-modal-open')")

    pg.click("[data-acct-modal='shipping-current']")
    pg.wait_for_timeout(600)
    check("%s Edit opens Current Address" % tag, open_panel(pg), "shipping-current")

    pg.click("[data-acct-modal-panel='shipping-current'] [data-acct-modal='shipping-form']")
    pg.wait_for_timeout(600)
    check("%s Edit opens the form" % tag, open_panel(pg), "shipping-form")

    # phone is required and ships empty; filling it also dirties the form, which
    # is what un-disables Save.
    pg.fill("#acct-sh-phone", "412 345 678")
    pg.wait_for_timeout(400)
    save = "[data-acct-modal-panel='shipping-form'] [data-acct-save]"
    check("%s Save enabled once dirty" % tag, pg.locator(save).is_disabled(), False)

    pg.click(save)
    pg.wait_for_timeout(700)
    check("%s Save reaches success" % tag, open_panel(pg), "shipping-success")

    pg.click("[data-acct-modal-panel='shipping-success'] .gb-acct-modal__foot button")
    pg.wait_for_timeout(700)
    check("%s Close returns to Current Address" % tag, open_panel(pg), "shipping-current")
    check("%s page still locked after the step back" % tag, locked(pg), True)
    check("%s success panel is hidden again" % tag,
          pg.locator("[data-acct-modal-panel='shipping-success']").is_hidden(), True)

    # the returned-to panel has to be usable, not just present
    check("%s Current Address is interactive again" % tag,
          pg.locator("[data-acct-modal-panel='shipping-current'] "
                     "[data-acct-modal='shipping-form']").is_visible(), True)

    pg.keyboard.press("Escape")
    pg.wait_for_timeout(600)
    check("%s Escape still closes everything" % tag, open_panel(pg), None)
    check("%s unlocked after Escape" % tag, locked(pg), False)

    # 3 -- the cross and the backdrop still close for real: only the foot button
    # was rewired. Without this, wiring the cross to the same panel reads green.
    pg.click("[data-acct-modal='shipping-current']")
    pg.wait_for_timeout(500)
    pg.click("[data-acct-modal-panel='shipping-current'] [data-acct-modal='shipping-form']")
    pg.wait_for_timeout(500)
    pg.fill("#acct-sh-phone", "412 345 678")
    pg.click(save)
    pg.wait_for_timeout(700)
    check("%s back at success" % tag, open_panel(pg), "shipping-success")
    pg.click("[data-acct-modal-panel='shipping-success'] .gb-acct-modal__close")
    pg.wait_for_timeout(700)
    check("%s cross still closes outright" % tag, open_panel(pg), None)
    check("%s unlocked after the cross" % tag, locked(pg), False)
    pg.close()


with sync_playwright() as p:
    b = p.chromium.launch(executable_path=str(_chrome()))
    for w in (1440, 390):
        run_arrow(b, w)
        run_close(b, w)
    b.close()

print("\n%d ok / %d red" % (ok, red))
sys.exit(1 if red else 0)
