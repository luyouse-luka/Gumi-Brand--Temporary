#!/usr/bin/env python3
"""Task 25 regression: the account修改任务文档 items done this round.

Covers requirements 1 / 7 / 8 / 9. Each assertion is written so a revert makes
it go red -- values are read from the rendered page, never from the source.

⚠ hover must be driven by Playwright: (hover: hover) is always false when a
headless chromium is driven directly, so reading the CSS would pass either way.
"""
import sys, pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent


def _chrome():
    base = pathlib.Path.home() / ".cache/ms-playwright"
    hits = sorted(base.glob("chromium-*/chrome-linux64/chrome"))
    if not hits:
        sys.exit("no chromium under %s -- run: npx playwright install chromium" % base)
    return hits[-1]


URL = (ROOT / "account.html").as_uri()
ok = red = 0


def check(label, got, want):
    global ok, red
    if got == want:
        ok += 1
    else:
        red += 1
        print("  RED  %-46s want %r got %r" % (label, want, got))


def run(pw):
    b = pw.chromium.launch(executable_path=str(_chrome()))
    # no --hide-scrollbars: the lock compensation is only measurable with a real one
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto(URL + "#detail", wait_until="load")
    pg.wait_for_timeout(400)

    # --- req 7: nav is sticky and survives the modal lock -------------------
    nav = pg.locator(".gb-acct-nav")
    check("nav position", nav.evaluate("e => getComputedStyle(e).position"), "sticky")
    check("nav align-self", nav.evaluate("e => getComputedStyle(e).alignSelf"), "start")

    top_before = nav.evaluate("e => Math.round(e.getBoundingClientRect().top)")
    pg.evaluate("window.scrollTo(0, 600)")
    pg.wait_for_timeout(250)
    top_after = nav.evaluate("e => Math.round(e.getBoundingClientRect().top)")
    # stuck to its offset instead of scrolling away with the page
    check("nav sticks while scrolling", top_after == 128, True)
    check("nav actually moved up from start", top_before > top_after, True)

    # body must stay clip (not hidden) or the sticky rail drops to static
    pg.evaluate("document.querySelector('[data-acct-modal=\"edit-date\"]').click()")
    pg.wait_for_timeout(450)
    check("modal open", pg.locator(".gb-acct-modal.is-open").count(), 1)
    check("html locked", pg.evaluate("getComputedStyle(document.documentElement).overflow"), "hidden")
    check("body not hidden (keeps sticky alive)",
          pg.evaluate("getComputedStyle(document.body).overflowY"), "visible")
    check("nav still sticky under lock",
          nav.evaluate("e => getComputedStyle(e).position"), "sticky")

    # --- req 7: panel clips to its radius ----------------------------------
    panel = pg.locator(".gb-acct-modal.is-open .gb-acct-modal__panel")
    # clip, not hidden -- hidden would make the panel a scroll container and cut
    # off any field past the body's fold (shipping-form's suburb, measured y=740).
    check("panel overflow", panel.evaluate("e => getComputedStyle(e).overflow"), "clip")

    # --- req 9: the calendar is inline, inside the panel, and arms Save ----
    # ⚠ Task 38 reversed r31 again: the grid is flatpickr's (the plugin the
    # funkyfood portal uses), skinned to 30465. Which engine draws it is
    # acct38check's business -- what matters here is that it is inline, inside
    # the panel, and still arms Save.
    cal = pg.locator(".gb-acct-modal.is-open [data-acct-cal]")
    check("calendar rendered inline", cal.count(), 1)
    check("calendar is inside the panel",
          pg.evaluate("!!document.querySelector('.gb-acct-modal__panel [data-acct-cal]')"), True)
    check("calendar drives the field",
          cal.get_attribute("data-acct-cal-for"), "acct-f-date")
    check("calendar has a full month of days",
          cal.locator(".flatpickr-day").count() >= 28, True)
    save = pg.locator(".gb-acct-modal.is-open .gb-acct-modal__save")
    check("Save starts disabled", save.evaluate("e => e.disabled"), True)

    # click a real selectable day: the write-back has to fire an input event or
    # the Save gate never sees the change
    before = pg.locator("#acct-f-date").input_value()
    # Task 32: the calendar starts shut, so the days are unreachable until the
    # field is clicked. Without this the click below times out and the whole
    # script dies -- a crash reads as fewer reds, not as a failure.
    pg.locator(".gb-acct-modal.is-open .gb-acct-field__input").first.click()
    pg.wait_for_timeout(700)
    check("calendar opens on field click",
          cal.evaluate("e => e.checkVisibility({visibilityProperty: true})"), True)
    cal.locator(".flatpickr-day:not(.flatpickr-disabled):not(.prevMonthDay):not(.nextMonthDay)").last.click()
    pg.mouse.move(0, 0)
    pg.wait_for_timeout(250)
    check("field written back",
          pg.locator("#acct-f-date").input_value() != before, True)
    check("Save armed after date change", save.evaluate("e => e.disabled"), False)

    # --- req 8: Save closes the panel -------------------------------------
    # r26 note: Task 25 had chained edit-date -> need-now -> edit-frequency.
    # The client corrected that on 2026-09-15 -- no such chain exists; these are
    # ordinary saves, so they close. Only shipping-form (via its form's
    # data-acct-modal-next) and cancel-offer-skip still advance.
    check("edit-date Save is not chained",
          pg.locator(".gb-acct-modal.is-open .gb-acct-modal__save").get_attribute("data-acct-modal"), None)
    save.click()
    pg.wait_for_timeout(600)
    check("save closes the panel", pg.locator(".gb-acct-modal.is-open").count(), 0)
    check("lock released", pg.evaluate("document.documentElement.classList.contains('is-modal-open')"), False)

    # --- req 1 / 8: hover is colour-only, no transform ---------------------
    pg.keyboard.press("Escape")
    pg.goto(URL, wait_until="load")
    pg.wait_for_timeout(300)
    refer = pg.locator(".gb-acct-refer__action").first
    if refer.count():
        refer.hover()
        pg.wait_for_timeout(350)
        check("refer action: no transform on hover",
              refer.evaluate("e => getComputedStyle(e).transform"), "none")
        check("refer action: colour changed on hover",
              refer.evaluate("e => getComputedStyle(e).backgroundColor"), "rgb(181, 237, 97)")

    pg.evaluate("document.querySelector('[data-acct-modal=\"edit-name\"]').click()")
    pg.wait_for_timeout(450)
    cross = pg.locator(".gb-acct-modal.is-open .gb-acct-modal__close")
    cross.hover()
    pg.wait_for_timeout(350)
    check("modal close: no scale on hover",
          cross.evaluate("e => getComputedStyle(e).transform"), "none")
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(500)

    # --- req 8: disabled controls show the not-allowed cursor -------------
    pg.goto(URL + "#orders", wait_until="load")
    pg.wait_for_timeout(350)
    arrow = pg.locator(".gb-acct-pager button:disabled").first
    if arrow.count():
        check("disabled pager cursor", arrow.evaluate("e => getComputedStyle(e).cursor"), "not-allowed")

    # --- req 2: account icon rule + panel are hover-only (34578 vs 34805) ---
    pg.goto(URL, wait_until="load")
    pg.wait_for_timeout(300)
    icon = pg.locator(".gb-acct-header__link--account")
    rule_op = "e => getComputedStyle(e, '::after').opacity"
    check("icon rule hidden at rest", icon.evaluate(rule_op), "0")
    menu = pg.locator(".gb-acct-menu")
    check("panel hidden at rest", menu.evaluate("e => getComputedStyle(e).visibility"), "hidden")
    # board values: 221 wide, flush to the right edge, straight under the header
    check("panel width", menu.evaluate("e => Math.round(e.getBoundingClientRect().width)"), 221)
    check("panel right edge flush",
          menu.evaluate("e => Math.round(window.innerWidth - e.getBoundingClientRect().right)"), 0)
    check("panel background", menu.evaluate("e => getComputedStyle(e).backgroundColor"),
          "rgb(246, 254, 236)")
    icon.hover()
    pg.wait_for_timeout(400)
    check("icon rule shown on hover", icon.evaluate(rule_op), "1")
    check("panel shown on hover", menu.evaluate("e => getComputedStyle(e).visibility"), "visible")

    # --- req 4: three authored order states, switchable by class -----------
    card = pg.locator("[data-acct-view='overview'] .gb-acct-order")
    check("card carries the modifier", card.evaluate("e => e.className.includes('--shipped')"), True)
    shown = "e => [...e.querySelectorAll('[data-state]')].filter(n => getComputedStyle(n).display !== 'none').map(n => n.getAttribute('data-state'))"
    check("only shipped visible", sorted(set(card.evaluate(shown))), ["shipped"])
    # the class alone must drive it -- drop the attribute the preview notes use
    card.evaluate("e => { e.removeAttribute('data-acct-order-state');"
                  " e.className = e.className.replace('--shipped', '--renewal'); }")
    pg.wait_for_timeout(120)
    check("class alone switches to renewal", sorted(set(card.evaluate(shown))), ["renewal"])
    check("renewal skin applied", card.evaluate("e => getComputedStyle(e).backgroundColor"),
          "rgb(203, 243, 144)")

    # --- req 3 / 6: the incoming view animates, and cleans its class up ----
    pg.goto(URL, wait_until="load")
    pg.wait_for_timeout(300)
    check("no entry animation on first paint",
          pg.locator("[data-acct-view='overview']").evaluate("e => e.classList.contains('is-entering')"), False)
    pg.locator("[data-acct-goto='subscriptions']").first.click()
    pg.wait_for_timeout(60)
    subs = pg.locator("[data-acct-view='subscriptions']")
    check("entering class applied on switch", subs.evaluate("e => e.classList.contains('is-entering')"), True)
    check("animation is running",
          subs.evaluate("e => getComputedStyle(e).animationName"), "gb-acct-view-in")
    pg.wait_for_timeout(900)
    check("entering class removed after play",
          subs.evaluate("e => e.classList.contains('is-entering')"), False)

    # phone slides in from the right instead
    pg.set_viewport_size({"width": 390, "height": 844})
    pg.goto(URL, wait_until="load")
    pg.wait_for_timeout(300)
    pg.locator("[data-acct-view='overview'] [data-acct-goto='orders']").first.click()
    pg.wait_for_timeout(60)
    check("phone uses the sideways keyframes",
          pg.locator("[data-acct-view='orders']").evaluate("e => getComputedStyle(e).animationName"),
          "gb-acct-view-in-right")

    b.close()


with sync_playwright() as pw:
    run(pw)

print("\nr25: %d ok / %d red" % (ok, red))
sys.exit(1 if red else 0)
