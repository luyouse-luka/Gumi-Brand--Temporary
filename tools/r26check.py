#!/usr/bin/env python3
"""Task 26 regression: the six items in account修改任务文档 (2026-09-15 03:31).

⚠ Item 2 of that round REVERSED Task 25's req 9: there is no
edit-date -> need-now -> edit-frequency chain. The first block below locks the
revert so it cannot come back.

Run it alone -- three concurrent chromiums make acctmodal's 2s clicks flake.
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
        print("  RED  %-48s want %r got %r" % (label, want, got))


def open_panel(pg, name, wait=500):
    pg.evaluate("n => window.gumiAcct.modal.open(n)", name)
    pg.wait_for_timeout(wait)


def run(pw):
    b = pw.chromium.launch(executable_path=str(_chrome()))
    pg = b.new_page(viewport={"width": 390, "height": 900})
    pg.goto(URL, wait_until="load")
    pg.wait_for_timeout(500)

    # --- item 2: the Task 25 chain is gone -------------------------------
    for panel in ("edit-date", "need-now"):
        open_panel(pg, panel)
        save = pg.locator(".gb-acct-modal.is-open .gb-acct-modal__save")
        check("%s: not chained" % panel, save.get_attribute("data-acct-modal"), None)
        check("%s: closes instead" % panel,
              save.get_attribute("data-acct-modal-close") is not None, True)
        pg.keyboard.press("Escape")
        pg.wait_for_timeout(600)
    # the two that legitimately still advance
    check("shipping-form still advances",
          pg.evaluate("() => !!document.querySelector(\"[data-acct-modal-next='shipping-success']\")"), True)

    # --- item 1: frequency is a ul/li dropdown, not a bare <select> -------
    # ⚠ r27 swapped the account's own acctSelect for the site's .gb-select
    # (main.js selectBox). Same requirement, shared component.
    open_panel(pg, "edit-frequency")
    P = "[data-acct-modal-panel='edit-frequency'] "
    check("native select taken over",
          pg.locator(P + "select").evaluate("e => e.classList.contains('gb-select__native')"), True)
    btn = pg.locator(P + ".gb-select__button")
    check("button shows current value", btn.inner_text().strip(), "Ships every 4 weeks")
    lst = pg.locator(P + ".gb-select__list")
    check("list closed at rest",
          lst.evaluate("e => [getComputedStyle(e).visibility, getComputedStyle(e).opacity]"),
          ["hidden", "0"])
    save = pg.locator(P + "[data-acct-save]")
    check("Save gated at rest", save.evaluate("e => e.disabled"), True)
    btn.click()
    pg.wait_for_timeout(400)
    check("list opens", lst.evaluate("e => [getComputedStyle(e).visibility, getComputedStyle(e).opacity]"),
          ["visible", "1"])
    check("list transitions (not an instant swap)",
          lst.evaluate("e => getComputedStyle(e).transitionDuration !== '0s'"), True)
    check("chevron rotates",
          pg.locator(P + ".gb-select__arrow").evaluate("e => getComputedStyle(e).transform"),
          "matrix(-1, 0, 0, -1, 0, 0)")
    pg.locator(P + ".gb-select__option").nth(2).click()
    pg.wait_for_timeout(500)
    check("value written back to the select", pg.locator(P + "select").input_value(), "Ships every 6 weeks")
    check("Save armed by the pick", save.evaluate("e => e.disabled"), False)
    check("list closed again", lst.evaluate("e => getComputedStyle(e).visibility"), "hidden")
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(600)

    # --- item 1/4: the chevron is no longer stretched ---------------------
    # board art is 10x5; a 10x5 viewBox in a 20x20 box doubled its height
    check("every chevron sits in a square viewBox",
          pg.evaluate("""() => [...document.querySelectorAll('.gb-select__arrow')]
                                 .every(s => s.getAttribute('viewBox') === '0 0 20 20')"""), True)

    # --- item 3: edit-product ---------------------------------------------
    open_panel(pg, "edit-product")
    P = "[data-acct-modal-panel='edit-product'] "
    thumb = pg.locator(P + ".gb-acct-prod__thumb")
    check("thumb is a real image", thumb.evaluate("e => e.tagName"), "IMG")
    check("thumb actually loaded", thumb.evaluate("e => e.naturalWidth > 0"), True)
    check("Flavour + Size are dropdowns", pg.locator(P + ".gb-select__button").count(), 2)
    check("each has placeholder options",
          pg.locator(P + "select").first.evaluate("e => e.options.length >= 2"), True)

    # Task 46: qty stepping moved to the theme; the static click must be inert
    v0 = pg.locator(P + "[data-acct-qty-value]").input_value()
    pg.locator(P + "[data-acct-qty='up']").click()
    pg.wait_for_timeout(300)
    check("qty click is inert on the front end", pg.locator(P + "[data-acct-qty-value]").input_value(), v0)
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(700)

    # --- item 3: panel height follows funkyfood ---------------------------
    # ⚠ r27 moved the source from .product-pop-up (720) to the account portal's
    # own drawer cap (85vh under 575). 900-tall viewport -> 765.
    check("phone sheet capped at 85vh",
          pg.locator("[data-acct-modal-panel='edit-product'] .gb-acct-modal__panel")
            .evaluate("e => getComputedStyle(e).maxHeight"), "765px")
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(600)

    # --- item 4: qty glyphs share one coordinate system -------------------
    # the minus kept a 14x2 viewBox cut from the board; 14px-square CSS stretched
    # its stroke 7x vertically
    boxes = pg.evaluate("""() => [...document.querySelectorAll('.gb-acct-qty__btn svg')]
                                   .map(s => s.getAttribute('viewBox'))""")
    check("all qty glyphs are 14x14", sorted(set(boxes)), ["0 0 14 14"])

    # --- item 5: disabled controls signal not-allowed ---------------------
    pg.goto(URL + "#detail", wait_until="load")
    pg.wait_for_timeout(500)
    pg.evaluate("() => document.querySelector('.gb-acct-detail')"
                ".setAttribute('data-acct-sub-state', 'cancelled')")
    pg.wait_for_timeout(300)
    check("cancelled row carries the cursor",
          pg.evaluate("""() => {
            const el = document.querySelector(
              ".gb-acct-detail[data-acct-sub-state='cancelled'] [data-acct-modal='add-product']");
            if (!el) return 'no such button';
            // pointer-events:none means the element is not the hit target -- the
            // cursor has to resolve on its parent instead
            return getComputedStyle(el.parentElement).cursor;
          }"""), "not-allowed")
    pg.evaluate("() => document.querySelector('.gb-acct-detail')"
                ".setAttribute('data-acct-sub-state', 'active')")

    # --- item 4: link hover is a colour move, with a transition -----------
    link = pg.locator(".gb-acct-link--sm").first
    if link.count():
        check("link has a transition",
              link.evaluate("e => getComputedStyle(e).transitionDuration !== '0s'"), True)
        link.hover()
        pg.wait_for_timeout(400)
        check("link hover changes colour, not opacity",
              link.evaluate("e => [getComputedStyle(e).color, getComputedStyle(e).opacity]"),
              ["rgb(0, 86, 53)", "1"])

    # Unverified codes never create an applied state.
    pg.goto(URL + "#detail", wait_until="load")
    pg.wait_for_timeout(500)
    det = pg.locator(".gb-acct-detail")
    check("discount starts at none", det.get_attribute("data-acct-discount"), "none")
    pg.locator("[data-acct-modal='discount-add']").first.click()
    pg.wait_for_timeout(500)
    LP = ".gb-acct-modal.is-open "
    ap = pg.locator(LP + "[data-acct-apply]")
    check("Apply gated while empty", ap.evaluate("e => e.disabled"), True)
    pg.fill(LP + "[data-acct-discount-input]", "CEO90")
    pg.wait_for_timeout(250)
    check("Apply armed by input", ap.evaluate("e => e.disabled"), False)
    ap.click()
    pg.wait_for_timeout(700)
    check("waits for API validation",
          pg.locator(".gb-acct-modal.is-open").get_attribute("data-acct-modal-panel"), "discount-add")
    check("no unverified confirmation line",
          "Discount CEO90 applied $35.25 off" in pg.locator(".gb-acct-modal.is-open").inner_text(), False)
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(700)
    check("detail remains unapplied", det.get_attribute("data-acct-discount"), "none")
    check("edit link needs a verified discount",
          pg.locator("[data-discount-only='applied']").first.is_visible(), False)
    check("summary needs a verified discount",
          pg.locator(".gb-acct-summary__row--discount").first.is_visible(), False)

    b.close()


with sync_playwright() as pw:
    run(pw)

print("\nr26: %d ok / %d red" % (ok, red))
sys.exit(1 if red else 0)
