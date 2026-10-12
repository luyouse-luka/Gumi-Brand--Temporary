#!/usr/bin/env python3
"""account Task 31 regression: the three items from the 2026-09-15 brief.

1 icons were being clipped by their own viewBox (see tools/iconclip.py, which
  carries the general assertion); Edit renewal date now uses the board's own
  calendar rather than a generic one. ⚠ Task 38 reversed HOW it is drawn: the
  client asked for funkyfood's plugin with this skin, so flatpickr is back and
  the three "no vendor picker" assertions below became their opposite. The look
  is still 30465's -- acct38check pins every token of it.
2 desktop panel copy fills the wider panel, and a dropdown in a panel that does
  not scroll opens downwards
3 every modal locks the page, and closing one leaves the scroll position -- and
  with it the sticky nav and header -- exactly where it was

⚠ Item 3's old failure is invisible to a source review: the lock itself was
correct, the jump came from close()'s focus() scrolling the trigger back into
view the instant the lock came off, so the page moved after the panel had gone.

⚠ Item 2's dropdown assertion must be measured, not read off the class list:
main.js decides the direction from the nearest clipping ancestor at open time,
and .gb-acct-modal__body clips whenever overflow-y is auto, scrolling or not.
"""
import json
import pathlib
import sys

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / "account.html"
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
        print("  RED  %-56s want %r got %r" % (label, want, got))


def open_panel(pg, name):
    # clicked through the DOM, not by Playwright: its click scrolls the trigger
    # into view first, which is the very thing item 3 measures
    pg.evaluate("(n) => document.querySelector(`[data-acct-modal='${n}']`).click()", name)
    pg.mouse.move(0, 0)          # a resting pointer reads hover state as static
    pg.wait_for_timeout(700)


RECT = """() => {
  const r = s => { const e = document.querySelector(s);
    if (!e) return null;
    const b = e.getBoundingClientRect();
    return [Math.round(b.x), Math.round(b.y)]; };
  return {html: document.documentElement.classList.contains('is-modal-open'),
          body: document.body.classList.contains('is-modal-open'),
          y: window.scrollY, nav: r('.gb-acct-nav'), hdr: r('.gb-acct-header')};
}"""


def lock_section(b, _unused, w):
    """Every panel locks the page, and the sticky rail never moves -- neither
    when the panel opens nor when it closes.

    ⚠ Runs at prefers-reduced-motion: no-preference ON PURPOSE. Lenis owns the
    wheel site-wide and scrolls with window.scrollTo, which overflow:hidden does
    not stop -- but smoothScroll.init() returns early under `reduce`, so a probe
    on the default setting never starts Lenis and reads a missing pause as
    green. That is exactly how Task 8/31/33 all shipped this green while the
    real browser scrolled. The Lenis anchor below is what keeps it honest.
    """
    ctx = b.new_context(viewport={"width": w, "height": 950},
                        reduced_motion="no-preference")
    pg = ctx.new_page()
    pg.goto(PAGE.as_uri() + "#detail")
    pg.wait_for_timeout(900)
    tag = "@%d" % w
    check("Lenis is actually running" + tag,
          pg.evaluate("() => !!(window.gumi && window.gumi.smoothScroll"
                      " && window.gumi.smoothScroll.lenis)"), True)
    print("[3%s] scroll lock and a still page on close" % tag)
    # below 768 the rail is display:none, so comparing its rect to itself would
    # be a green that means nothing. Say which one is really under test.
    rail_live = pg.eval_on_selector(".gb-acct-nav",
                                    "e=>getComputedStyle(e).display") != "none"
    check("rail is rendered at this width" + tag, rail_live, w > 767)
    names = pg.evaluate("""() => Array.from(
        document.querySelectorAll('[data-acct-modal]'),
        e => e.getAttribute('data-acct-modal'))""")
    check("triggers found" + tag, len(names) >= 10, True)
    for name in names:
        pg.evaluate("window.scrollTo(0, 600)")
        pg.wait_for_timeout(150)
        if not pg.evaluate("""(n) => {
              const t = document.querySelector(`[data-acct-modal='${n}']`);
              return !!t && t.checkVisibility({visibilityProperty: true});
            }""", name):
            continue                       # chained panel, reached from another
        rest = pg.evaluate(RECT)
        before = rest["y"]
        open_panel(pg, name)
        state = pg.evaluate(RECT)
        check("%s locks html%s" % (name, tag), state["html"], True)
        check("%s locks body%s" % (name, tag), state["body"], True)
        check("%s does not move the page%s" % (name, tag), state["y"], before)
        # the requirement in so many words: opening must not shift the rail
        if rail_live:
            check("%s leaves the rail where it was%s" % (name, tag),
                  state["nav"], rest["nav"])
        check("%s leaves the sticky header where it was%s" % (name, tag),
              state["hdr"], rest["hdr"])
        # the wheel is the real lock test; scrollTo goes through overflow:hidden.
        # Lenis needs its rAF loop to land, so these waits are generous.
        pg.mouse.move(w // 2, 450)                 # over the panel
        pg.mouse.wheel(0, 600)
        pg.wait_for_timeout(700)
        check("%s holds against the wheel%s" % (name, tag),
              pg.evaluate("window.scrollY"), before)
        # ⚠ and over the backdrop, which no panel-local data-lenis-prevent covers
        pg.mouse.move(max(8, w // 2 - 420), 500)
        pg.mouse.wheel(0, 600)
        pg.wait_for_timeout(700)
        check("%s holds over the backdrop too%s" % (name, tag),
              pg.evaluate("window.scrollY"), before)
        # the keyboard is a second real route and does not go through the wheel
        pg.keyboard.press("PageDown")
        pg.wait_for_timeout(300)
        check("%s holds against PageDown%s" % (name, tag),
              pg.evaluate("window.scrollY"), before)
        pg.keyboard.press("Escape")
        pg.wait_for_timeout(800)
        after = pg.evaluate(RECT)
        check("%s releases the lock%s" % (name, tag), after["html"], False)
        check("%s leaves the scroll position%s" % (name, tag), after["y"], before)
        if rail_live:
            check("%s leaves the sticky nav%s" % (name, tag), after["nav"], state["nav"])
        check("%s leaves the sticky header%s" % (name, tag), after["hdr"], state["hdr"])
        # the wheel has to come back, or every panel leaves the page dead
        check("%s hands the wheel back%s" % (name, tag),
              pg.evaluate("() => { const l = window.gumi.smoothScroll.lenis;"
                          " return l ? l.isStopped !== true : null; }"), True)
    ctx.close()


def main():
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=str(_chrome()))

        # --- 1: Edit Date shows the board's calendar, drawn by the plugin ---
        pg = b.new_page(viewport={"width": 1440, "height": 950})
        pg.goto(PAGE.as_uri() + "#detail")
        pg.wait_for_timeout(800)
        print("[1] Edit renewal date")
        open_panel(pg, "edit-date")
        panel = pg.locator(".gb-acct-modal.is-open")
        cal = panel.locator("[data-acct-cal]")
        # anchor first: an absent element would pass every assertion below it
        check("panel is open", panel.count(), 1)
        check("calendar present without touching the field", cal.count(), 1)
        # ⚠ REVERSED on 2026-09-16 (Task 32): the client asked for the calendar to
        # stay shut until the input is clicked -- Task 31 read "the calendar only
        # appears after clicking the input" as a complaint when it was the ask.
        # Kept as an assertion rather than deleted: putting it back would red here.
        check("calendar is shut on open",
              cal.evaluate("e => e.checkVisibility({visibilityProperty: true})"), False)
        pg.locator(".gb-acct-modal.is-open .gb-acct-field__input").first.click()
        pg.wait_for_timeout(700)
        pg.mouse.move(0, 0)
        check("clicking the field opens the calendar",
              cal.evaluate("e => e.checkVisibility({visibilityProperty: true})"), True)
        check("month grid is drawn",
              cal.locator(".flatpickr-day").count() >= 28, True)
        check("calendar drives the renewal field",
              cal.get_attribute("data-acct-cal-for"), "acct-f-date")
        # Task 38: the plugin draws it, one instance per calendar
        check("plugin drew this calendar",
              cal.locator(".flatpickr-calendar").count(), 1)
        check("plugin script is loaded",
              pg.evaluate("typeof window.flatpickr"), "function")
        # the field's shipped date has already passed, so nothing is preselected
        # and the month opens on the first one that can be picked
        check("no day selected while the field's date is past",
              cal.locator(".flatpickr-day.selected").count(), 0)
        check("opens on a month with selectable days",
              cal.locator(".flatpickr-day:not(.flatpickr-disabled):not(.prevMonthDay):not(.nextMonthDay)").count() > 0, True)
        pg.keyboard.press("Escape")
        pg.wait_for_timeout(700)

        # --- 2a: copy fills the desktop panel ---------------------------------
        print("[2] desktop panel fit and dropdown direction")
        for name in ("skip-next", "need-now", "edit-payment"):
            open_panel(pg, name)
            w = pg.evaluate("""() => {
              const c = document.querySelector('.gb-acct-modal.is-open .gb-acct-modal__copy');
              // the containing block is the parent's CONTENT box -- its border
              // box is a padding wider and the assertion would be off by it
              const p = c.parentElement, cs = getComputedStyle(p);
              const avail = p.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
              return {copy: Math.round(c.getBoundingClientRect().width),
                      avail: Math.round(avail)};
            }""")
            # the board's component keeps 30 of slack on the right at any width
            check("%s copy tracks the panel" % name, w["copy"], w["avail"] - 30)
            pg.keyboard.press("Escape")
            pg.wait_for_timeout(700)

        # --- 2b: a dropdown in a panel that does not scroll opens downwards ---
        for name in ("edit-frequency", "edit-product"):
            open_panel(pg, name)
            r = pg.evaluate("""() => {
              const panel = document.querySelector('.gb-acct-modal.is-open .gb-acct-modal__panel');
              const body = panel.querySelector('.gb-acct-modal__body');
              const btn = panel.querySelector('.gb-select__button');
              if (!btn) return null;
              btn.click();
              const sel = btn.closest('.gb-select');
              const li = sel.querySelector('.gb-select__list').getBoundingClientRect();
              const bt = btn.getBoundingClientRect();
              return {up: sel.classList.contains('is-up'),
                      below: li.top >= bt.bottom - 1,
                      clippedByPanel: li.bottom > panel.getBoundingClientRect().bottom + 1,
                      bodyOverflow: body.style.overflowY || getComputedStyle(body).overflowY};
            }""")
            check("%s has a select" % name, r is not None, True)
            if r:
                check("%s body stops clipping when it need not scroll" % name,
                      r["bodyOverflow"], "visible")
                check("%s dropdown opens downwards" % name, r["up"], False)
                check("%s list sits below its button" % name, r["below"], True)
                check("%s list is not clipped by the panel" % name,
                      r["clippedByPanel"], False)
            pg.keyboard.press("Escape")
            pg.wait_for_timeout(700)

        # --- 3: every modal locks, and closing restores nothing ---------------
        # ⚠ Task 33 widened this: it used to run at 1440 only, and it only
        # compared the sticky rects open-vs-closed, never rest-vs-open -- so a
        # modal that shoved the rail on the way IN would have read green.
        lock_section(b, None, 1440)
        lock_section(b, None, 390)
        b.close()

    print("\nacct31: %d ok / %d red" % (ok, red))
    sys.exit(1 if red else 0)


if __name__ == "__main__":
    main()
