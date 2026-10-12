#!/usr/bin/env python3
"""Task 27 regression: the three items in account修改任务文档 (2026-09-15 03:53).

⚠ Item 1 REVERSES the 2026-09-10 ruling that the desktop panel keeps the board's
390 (SPEC 待裁决 E). Desktop now follows funkyfood's account portal.
⚠ Item 3 replaced the account's own acctSelect with the site's .gb-select
(main.js selectBox); the first block below fails if a second implementation
comes back.

Run it alone -- concurrent chromiums make the 2s modal clicks flake.
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
        print("  RED  %-52s want %r got %r" % (label, want, got))


def open_panel(pg, name, wait=500):
    pg.evaluate("n => window.gumiAcct.modal.open(n)", name)
    pg.wait_for_timeout(wait)


# transform with the transition switched off, so the value is the rule's, not a
# frame of the animation
REST_Y = """(name) => {
  const m = document.querySelector(`[data-acct-modal-panel='${name}']`);
  const p = m.querySelector('.gb-acct-modal__panel');
  const h = Math.round(p.getBoundingClientRect().height);
  p.style.transition = 'none';
  m.classList.remove('is-open');
  const t = new DOMMatrixReadOnly(getComputedStyle(p).transform);
  m.classList.add('is-open');
  p.style.transition = '';
  return [Math.round(t.f), h];
}"""


def run(pw):
    b = pw.chromium.launch(executable_path=str(_chrome()))

    # ===== desktop =========================================================
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto(URL, wait_until="load")
    pg.wait_for_timeout(500)

    # --- item 1: funkyfood's account portal sizes the desktop panel --------
    # .delivery-*-pop-up .content is 520 wide; its cancel flow caps at 90vh
    open_panel(pg, "shipping-form")
    panel = pg.locator(".gb-acct-modal.is-open .gb-acct-modal__panel")
    check("desktop panel is 520 wide",
          panel.evaluate("e => Math.round(e.getBoundingClientRect().width)"), 520)
    check("desktop panel caps at 90vh",
          panel.evaluate("e => getComputedStyle(e).maxHeight"), "810px")
    check("no 720 cap left",
          pg.evaluate("() => getComputedStyle(document.querySelector("
                      "'.gb-acct-modal.is-open .gb-acct-modal__panel')).maxHeight !== '720px'"), True)

    # --- item 3: State is the site's dropdown, not a second implementation --
    P = "[data-acct-modal-panel='shipping-form'] "
    # negative assertion: the "State handed to selectBox" check right below is its
    # anchor -- on a page that failed to load both counts would be 0 anyway
    check("acctSelect is gone",
          pg.evaluate("() => document.querySelectorAll('[class*=gb-acct-select]').length"), 0)
    check("State handed to selectBox",
          pg.locator(P + "select").evaluate("e => e.classList.contains('gb-select__native')"), True)
    btn = pg.locator(P + ".gb-select__button")
    check("button carries the current value", btn.inner_text().strip(), "VIC")
    check("label points at the button, not the hidden select",
          pg.evaluate("""() => {
            const l = document.querySelector('label[for="acct-sh-state"]');
            const b = document.querySelector("%s.gb-select__button");
            return l === null && b.getAttribute('aria-labelledby').includes('acct-sh-state');
          }""" % P), True)

    lst = pg.locator(P + ".gb-select__list")
    # the collapse is the point of the request: visibility + opacity, never a
    # display swap -- display cannot transition
    check("closed list is transitioned out, not display:none",
          lst.evaluate("e => [getComputedStyle(e).display !== 'none',"
                       " getComputedStyle(e).visibility, getComputedStyle(e).opacity]"),
          [True, "hidden", "0"])
    check("the fade has a duration",
          lst.evaluate("e => getComputedStyle(e).transitionDuration !== '0s'"), True)
    btn.click()
    pg.wait_for_timeout(450)
    check("opens", lst.evaluate("e => [getComputedStyle(e).visibility, getComputedStyle(e).opacity]"),
          ["visible", "1"])
    check("all eight states listed", pg.locator(P + ".gb-select__option").count(), 8)
    # the native control keeps a painted arrow for the no-JS case; the button
    # has a real <svg>, so it must turn that one off or two chevrons show
    check("exactly one chevron",
          pg.evaluate("""() => [...document.querySelectorAll('.gb-select__button')]
                 .every(b => getComputedStyle(b).backgroundImage === 'none'
                             && b.querySelector('.gb-select__arrow'))"""), True)
    check("no-JS fallback keeps an arrow on the native control",
          pg.locator(P + "select").evaluate(
              "e => getComputedStyle(e).backgroundImage.startsWith('url(')"), True)
    check("flips up rather than out of the scroll body",
          pg.locator(P + ".gb-select").evaluate("e => e.classList.contains('is-up')"), True)
    pg.locator(P + ".gb-select__option").nth(1).click()
    pg.wait_for_timeout(450)
    check("write-back reaches the native control", pg.locator(P + "select").input_value(), "NSW")
    check("collapses again", lst.evaluate("e => getComputedStyle(e).visibility"), "hidden")
    check("the pick arms Save",
          pg.locator(P + "[data-acct-save]").evaluate("e => !e.disabled"), True)

    # --- item 3: focus is a green border, not a ring -----------------------
    inp = pg.locator(P + "#acct-sh-suburb")
    inp.focus()
    pg.wait_for_timeout(200)
    check("input focus: no outline ring",
          inp.evaluate("e => getComputedStyle(e).outlineStyle"), "none")
    check("input focus: green border like every other page",
          inp.evaluate("e => getComputedStyle(e).borderColor"), "rgb(0, 86, 53)")
    check("border colour transitions",
          inp.evaluate("e => getComputedStyle(e).transitionProperty.includes('border-color')"), True)
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(700)

    # the textarea is named in the brief alongside the inputs
    open_panel(pg, "cancel-reason")
    area = pg.locator(".gb-acct-modal.is-open .gb-acct-field__input--area")
    if area.count():
        area.focus()
        pg.wait_for_timeout(200)
        check("textarea focus: no outline ring",
              area.evaluate("e => getComputedStyle(e).outlineStyle"), "none")
        check("textarea focus: green border",
              area.evaluate("e => getComputedStyle(e).borderColor"), "rgb(0, 86, 53)")
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(700)

    # --- item 2: desktop keeps the 8px lift, it is not a drawer ------------
    open_panel(pg, "edit-product")
    y, h = pg.evaluate(REST_Y, "edit-product")
    check("desktop entry stays a lift", y, 8)
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(700)

    # --- item 3a: suburb autocomplete is deliberately absent ---------------
    # anchor first, or "no autocomplete widget" is true for the wrong reason
    check("suburb field still there",
          pg.locator("#acct-sh-suburb").count(), 1)
    check("no autocomplete attached",
          pg.evaluate("() => !window.google && !document.querySelector('.pac-container')"), True)

    # ===== phone ===========================================================
    pg.set_viewport_size({"width": 390, "height": 844})
    pg.goto(URL, wait_until="load")
    pg.wait_for_timeout(500)

    # --- item 2: Edit Product comes up from the bottom edge ----------------
    open_panel(pg, "edit-product")
    panel = pg.locator(".gb-acct-modal.is-open .gb-acct-modal__panel")
    check("settles flush to the bottom edge",
          panel.evaluate("e => getComputedStyle(e).transform"), "none")
    # REST_Y leaves the panel mid-transition, so it goes after the settled read
    y, h = pg.evaluate(REST_Y, "edit-product")
    check("phone drawer starts fully off-screen", y == h, True)
    check("it is not the old 16px nudge", y > 16, True)
    check("still a bottom sheet",
          panel.evaluate("e => [getComputedStyle(e).borderTopLeftRadius,"
                         " getComputedStyle(e).borderBottomLeftRadius]"), ["12px", "0px"])
    check("the slide has a duration",
          panel.evaluate("e => getComputedStyle(e).transitionDuration.split(',')[1].trim() !== '0s'"), True)
    check("phone panel keeps the board's 390",
          panel.evaluate("e => Math.round(e.getBoundingClientRect().width)"), 390)
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(700)

    b.close()


with sync_playwright() as pw:
    run(pw)

print("\nr27: %d ok / %d red" % (ok, red))
sys.exit(1 if red else 0)
