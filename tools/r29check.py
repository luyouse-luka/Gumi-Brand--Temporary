#!/usr/bin/env python3
"""Task 29 regression: the four items from the 2026-09-15 brief.

1 Change Password slides funkyfood's form out under the button
2 the FAQ answer sits in a wrapper and the row slides (was an instant [hidden] cut)
3 the Help card's email / phone are real links, styled as the board draws them
4 the account menu lives inside the icon, and the icon no longer navigates

⚠ Three things here fail silently if reverted:
  - the .acct-live gate on both collapsed heights. Written flat, a dead script
    would bury six of seven FAQ answers and the whole password form.
  - the icon box running the full bar height. Without it the pointer leaves the
    hover area in the 28px gap and the panel fades while you reach for it -- and
    every static assertion below still passes.
  - the menu's right offset. Its containing block changed from the header to the
    24px icon, so right:0 would park it 120px short of the edge it sits on.
"""
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


HP = "[data-acct-view='help'] "
PW = "[data-acct-view='password'] "
H = lambda pg, sel: pg.eval_on_selector(sel, "e => Math.round(e.getBoundingClientRect().height)")


def run(pw):
    global ok, red
    b = pw.chromium.launch(executable_path=str(_chrome()))
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(PAGE.as_uri())
    pg.wait_for_timeout(400)

    # ── 1 · Change Password ──────────────────────────────────────────────────
    print("1 -- Change Password slides out")
    pg.evaluate("() => { location.hash = '#password'; }")
    pg.wait_for_timeout(500)
    check("anchor: the password view is up", pg.is_visible(PW + ".gb-acct-card"), True)
    check("the form starts collapsed", H(pg, PW + "[data-acct-pw-wrap]"), 0)
    check("the button says it is collapsed",
          pg.get_attribute(PW + "[data-acct-pw-toggle]", "aria-expanded"), "false")
    check("three password fields, all type=password",
          pg.eval_on_selector_all(PW + ".gb-acct-pw__form input",
                                  "els => els.map(e => e.type)"),
          ["password", "password", "password"])

    pg.click(PW + "[data-acct-pw-toggle]")
    # mid-flight: a real animation is running, not an instant cut
    pg.wait_for_timeout(80)
    mid = pg.eval_on_selector(PW + "[data-acct-pw-wrap]",
                              "e => e.getAnimations().length")
    check("the open is animated", mid > 0, True)
    pg.wait_for_timeout(700)
    open_h = H(pg, PW + "[data-acct-pw-wrap]")
    check("the form is open", open_h > 100, True)
    check("the button says it is open",
          pg.get_attribute(PW + "[data-acct-pw-toggle]", "aria-expanded"), "true")

    pg.click(PW + "[data-acct-pw-cancel]")
    pg.wait_for_timeout(700)
    check("Cancel closes it again", H(pg, PW + "[data-acct-pw-wrap]"), 0)
    # ⚠ a zero-height overflow:hidden box is still read aloud and still tabbable
    check("the shut form is out of the a11y tree",
          pg.eval_on_selector(PW + "[data-acct-pw-wrap]",
                              "e => getComputedStyle(e).visibility"), "hidden")
    check("and its inputs cannot be tabbed into",
          pg.eval_on_selector(PW + "#acct-pw-current",
                              "e => { e.focus(); return document.activeElement === e; }"), False)

    # ── 2 · FAQ ──────────────────────────────────────────────────────────────
    print("2 -- FAQ answers slide")
    pg.evaluate("() => { location.hash = '#help'; }")
    pg.wait_for_timeout(500)
    check("seven answers, each in a wrapper",
          pg.eval_on_selector_all(HP + ".gb-acct-faq__panel", "e => e.length"), 7)
    check("the copy sits inside the wrapper",
          pg.eval_on_selector_all(HP + ".gb-acct-faq__panel > .gb-acct-faq__a",
                                  "e => e.length"), 7)
    check("row 1 is open, the rest are not",
          pg.eval_on_selector_all(HP + ".gb-acct-faq__item",
                                  "els => els.map(e => e.classList.contains('is-open'))"),
          [True] + [False] * 6)
    check("a shut row has no height",
          H(pg, HP + ".gb-acct-faq__item:nth-child(2) .gb-acct-faq__panel"), 0)
    check("and a shut row is out of the a11y tree",
          pg.eval_on_selector(HP + ".gb-acct-faq__item:nth-child(2) .gb-acct-faq__panel",
                              "e => getComputedStyle(e).visibility"), "hidden")
    # innerText skips visibility:hidden, so only the open row's copy is readable
    check("only the open row's answer is exposed",
          pg.eval_on_selector(HP + ".gb-acct-faq", "e => e.innerText.split('Text here').length - 1"), 1)

    pg.click(HP + ".gb-acct-faq__item:nth-child(2) .gb-acct-faq__q")
    pg.wait_for_timeout(80)
    check("the row is animated, not cut",
          pg.eval_on_selector(HP + ".gb-acct-faq__item:nth-child(2) .gb-acct-faq__panel",
                              "e => e.getAnimations().length") > 0, True)
    pg.wait_for_timeout(700)
    check("row 2 opened",
          H(pg, HP + ".gb-acct-faq__item:nth-child(2) .gb-acct-faq__panel") > 0, True)
    check("and row 1 closed with it",
          H(pg, HP + ".gb-acct-faq__item:nth-child(1) .gb-acct-faq__panel"), 0)
    check("aria followed", pg.get_attribute(
        HP + ".gb-acct-faq__item:nth-child(2) .gb-acct-faq__q", "aria-expanded"), "true")

    # ── 3 · Help card links ──────────────────────────────────────────────────
    print("3 -- Help card links")
    for view, tag in ((HP, "help"), ("[data-acct-view='order'] ", "order")):
        hrefs = pg.eval_on_selector_all(
            view + ".gb-acct-help__link", "els => els.map(e => e.getAttribute('href'))")
        check("%s: mailto / tel / faq are all links" % tag,
              [h.split(":")[0] for h in hrefs], ["mailto", "tel", "faq.html"])
    st = pg.eval_on_selector(
        HP + ".gb-acct-help__link",
        "e => { const c = getComputedStyle(e); return [c.color, c.textDecorationLine]; }")
    # 27170 draws those runs #0374a5 and UNDERLINE
    check("link colour is the board's", st[0], "rgb(3, 116, 165)")
    check("and they are underlined", st[1], "underline")

    # ── 4 · the account menu ─────────────────────────────────────────────────
    print("4 -- the account menu moved inside the icon")
    box = ".gb-acct-header__link--account"
    check("the menu is inside the icon box",
          pg.eval_on_selector(".gb-acct-menu",
                              "e => !!e.closest('%s')" % box), True)
    check("the icon no longer navigates",
          pg.eval_on_selector(box, "e => e.tagName.toLowerCase()"), "div")
    check("nothing nests an <a> in an <a>",
          pg.evaluate("() => !!document.querySelector('a a')"), False)
    # the mechanism that makes the hover travel continuous
    bar_h, box_h = pg.evaluate(
        "() => [document.querySelector('.gb-acct-header__bar').getBoundingClientRect().height,"
        " document.querySelector('.gb-acct-header__link--account').getBoundingClientRect().height]")
    check("the icon box runs the full bar height", round(box_h), round(bar_h))
    check("the icon itself is still 24",
          pg.eval_on_selector(box + " svg",
                              "e => Math.round(e.getBoundingClientRect().height)"), 24)

    pg.hover(box)
    pg.wait_for_timeout(450)
    check("hovering the icon drops the panel",
          pg.eval_on_selector(".gb-acct-menu", "e => getComputedStyle(e).visibility"), "visible")
    # the offset: its containing block is the 24px icon now
    right_gap = pg.evaluate(
        "() => Math.round(window.innerWidth"
        " - document.querySelector('.gb-acct-menu').getBoundingClientRect().right)")
    check("the panel still sits flush with the viewport edge", right_gap, 0)
    # and the pointer can reach it without the panel fading away
    pg.hover(".gb-acct-menu__link")
    pg.wait_for_timeout(450)
    check("the panel survives the pointer moving onto it",
          pg.eval_on_selector(".gb-acct-menu", "e => getComputedStyle(e).visibility"), "visible")

    check("no script errors anywhere above", errs, [])

    # ── 5 · Refer a Friend ───────────────────────────────────────────────────
    # ⚠ Reverses half of SPEC 决策 C. There is still no board, so this checks the
    # structure the brief asked for, not values taken from a design.
    print("5 -- Refer a Friend")
    RF = "[data-acct-view='referral'] "
    pg.evaluate("() => { location.hash = '#overview'; }")
    pg.wait_for_timeout(400)
    pg.click(".gb-acct-nav [data-acct-goto='referral']")
    pg.wait_for_timeout(750)     # Task 40: the outgoing view lives 500ms
    check("the desktop nav reaches it",
          pg.eval_on_selector_all("[data-acct-view]",
                                  "els => els.filter(e => !e.hidden)"
                                  ".map(e => e.getAttribute('data-acct-view'))"), ["referral"])
    check("the code field is read-only",
          pg.eval_on_selector(RF + "#acct-refer-code", "e => e.readOnly"), True)
    check("it has a code to copy",
          pg.eval_on_selector(RF + "#acct-refer-code", "e => e.value.length > 0"), True)
    check("four share icons, reusing the footer's",
          pg.eval_on_selector_all(RF + ".gb-acct-referral__social-link", "e => e.length"), 4)
    # two elements sharing an id makes the second clip resolve against the first
    check("the lifted SVG ids were renamed",
          pg.evaluate("() => { const ids = [...document.querySelectorAll('[id]')]"
                      ".map(e => e.id).filter(i => /clip/i.test(i));"
                      " return ids.length === new Set(ids).size; }"), True)
    check("the hero placeholder has a box",
          pg.eval_on_selector(RF + ".gb-acct-referral__hero",
                              "e => e.getBoundingClientRect().height > 40"), True)
    check("Contact Preferences was not switched on too",
          pg.eval_on_selector_all(".gb-acct-nav [aria-disabled='true']",
                                  "els => els.map(e => e.textContent.trim())"),
          ["Contact Preferences"])

    pg.click(RF + "[data-acct-copy]")
    pg.wait_for_timeout(300)
    check("Copy says it copied",
          pg.eval_on_selector(RF + "[data-acct-copy]", "e => e.textContent.trim()"), "Copied")

    # the overview card's arrow is the third way in
    pg.evaluate("() => { location.hash = '#overview'; }")
    pg.wait_for_timeout(400)
    pg.click(".gb-acct-refer__action")
    pg.wait_for_timeout(750)     # Task 40: the outgoing view lives 500ms
    check("the overview card's arrow lands here too",
          pg.eval_on_selector_all("[data-acct-view]",
                                  "els => els.filter(e => !e.hidden)"
                                  ".map(e => e.getAttribute('data-acct-view'))"), ["referral"])

    # ── 6 · degraded (no JS) ─────────────────────────────────────────────────
    print("6 -- degraded (no JS)")
    nojs = b.new_context(viewport={"width": 1440, "height": 900}, java_script_enabled=False)
    npg = nojs.new_page()
    npg.goto(PAGE.as_uri())
    npg.wait_for_timeout(300)
    # ⚠ The views themselves still carry an unconditional [hidden] -- without JS
    # only overview is reachable at all. That is a separate, already-logged gap
    # (Task 28, 顺带发现), so reveal them here and measure what THIS task gated:
    # whether the answers and the form are open once their view is on screen.
    npg.eval_on_selector_all("[data-acct-view]", "els => els.forEach(e => e.hidden = false)")
    npg.wait_for_timeout(100)
    check("without JS every FAQ answer is readable",
          npg.eval_on_selector_all(
              ".gb-acct-faq__panel",
              "els => els.every(e => e.getBoundingClientRect().height > 0)"), True)
    check("without JS the password form is open",
          npg.eval_on_selector("[data-acct-pw-wrap]",
                               "e => e.getBoundingClientRect().height > 100"), True)
    nojs.close()

    b.close()


with sync_playwright() as pw:
    run(pw)

print("\nr29: %d ok / %d red" % (ok, red))
sys.exit(1 if red else 0)
