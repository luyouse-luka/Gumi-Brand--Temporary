#!/usr/bin/env python3
"""account structure/value checks. Each task appends to CHECKS; run it whole.

Expected values come from the Figma nodes, never from a screenshot:
  desktop header  2284:34627 (closed) / 2284:34854 (expanded)
  mobile  header  2284:34534 (closed) / 2284:34804 (expanded)
  desktop nav     2284:27843 (in 27792); identical in 27678 and 28000
  mobile  list    2284:27617 (in 27604)

⚠ All three desktop boards are named "Account Overview Desktop" but are three
different pages -- tell them apart by the 24px heading, not the board name:
  27678 Account Overview / 28000 My Subscriptions / 27792 Subscription Detail

Checks are grouped by (page, width, action) so each group costs one page load;
a per-check load made the run time out.
"""
import sys, pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = pathlib.Path.home() / ".cache/ms-playwright/chromium-1217/chrome-linux64/chrome"

OPEN_MENU = "open-menu"
GOTO_SUBS = "goto-subscriptions"

# group key -> list of checks
#   ("css",  selector, prop, expected)
#   ("text", selector, [strings])
#   ("vis",  selector, bool)   element MUST exist; bool is whether it is shown
#   ("shown", selector, bool)  element MUST exist; bool is NOT having [hidden].
#                              Views are asserted this way, not with "vis": until
#                              Task 4 fills them they are empty and measure 0 tall,
#                              so a size test cannot tell "switched off" from "empty".
#   ("absent", selector)        element must not render at all
GROUPS = {
    # -- Task 2: desktop header, closed (2284:34627) --
    ("account.html", 1440, None): [
        ("css", ".gb-acct-header", "height", "80px"),
        ("css", ".gb-acct-header", "background-color", "rgb(231, 248, 208)"),
        ("css", ".gb-acct-header", "box-shadow", "none"),
        ("css", ".gb-acct-header__bar", "padding-left", "80px"),
        # Figma records paddingTop 32 but the logo sits at y=24 in an 80-tall bar:
        # that padding is measured off the logo's ink bbox, not its layout box.
        # Assert the centring instead.
        ("css", ".gb-acct-header__bar", "align-items", "center"),
        ("css", ".gb-acct-header__icons", "column-gap", "16px"),
        ("css", ".gb-acct-header__logo", "height", "32px"),
        # account icon carries the lime active underline (Line 115, 24x2 #b5ed61)
        ("css", ".gb-acct-header__link--account::after", "background-color", "rgb(181, 237, 97)"),
        ("css", ".gb-acct-header__link--account::after", "height", "2px"),
        ("vis", "[data-acct-menu]", False),
        # the site header must not render here -- the account one replaces it
        ("absent", ".gb-header"),

        # -- Task 3: desktop side nav (2284:27843) --
        # Two separate navigations, not one collapsing set: the desktop rail and
        # the in-page list card both exist and swap at the phone breakpoint.
        ("vis", ".gb-acct-nav", True),
        ("vis", ".gb-acct-list", False),
        ("css", ".gb-acct-nav", "width", "241px"),
        ("css", ".gb-acct-nav", "row-gap", "16px"),
        ("css", ".gb-acct-nav__group", "background-color", "rgb(255, 255, 255)"),
        ("css", ".gb-acct-nav__group", "border-radius", "8px"),
        ("css", ".gb-acct-nav__group", "padding-top", "8px"),
        ("css", ".gb-acct-nav__group", "padding-left", "8px"),
        # 225x40 item: Figma records padding 24 but the fixed 40 height wins, so
        # the real block padding is (40 - 20) / 2. Assert the height instead.
        ("css", ".gb-acct-nav__link", "height", "40px"),
        ("css", ".gb-acct-nav__link", "border-radius", "8px"),
        ("css", ".gb-acct-nav__link", "padding-left", "16px"),
        ("css", ".gb-acct-nav__link", "font-size", "14px"),
        ("css", ".gb-acct-nav__link", "line-height", "20px"),
        ("css", ".gb-acct-nav__link", "letter-spacing", "-0.28px"),
        ("css", ".gb-acct-nav__link", "color", "rgb(26, 26, 26)"),
        ("css", ".gb-acct-nav__link.is-current", "background-color", "rgb(243, 243, 243)"),
        ("text", ".gb-acct-nav__link",
         ["Account Overview", "My Subscriptions", "Order History",
          "My Details", "Change Password",
          "Refer a Friend",
          "Help", "Contact Preferences",
          "Logout"]),
        # Two-column shell (2284:27842). The asymmetric 244/352 gutters are
        # identical on all three desktop boards, so they are intended.
        ("css", ".gb-acct__inner", "column-gap", "32px"),
        ("css", ".gb-acct__inner", "padding-top", "48px"),
        ("css", ".gb-acct__inner", "padding-left", "244px"),
        ("css", ".gb-acct__inner", "padding-right", "352px"),
        ("css", ".gb-acct__inner", "padding-bottom", "144px"),
        # default view
        ("shown", "[data-acct-view='overview']", True),
        ("shown", "[data-acct-view='subscriptions']", False),
        ("shown", "[data-acct-view='detail']", False),
    ],
    # -- Task 3: clicking a nav item swaps the view --
    ("account.html", 1440, GOTO_SUBS): [
        ("shown", "[data-acct-view='overview']", False),
        ("shown", "[data-acct-view='subscriptions']", True),
        ("css", ".gb-acct-nav__link.is-current", "background-color", "rgb(243, 243, 243)"),
        ("text", ".gb-acct-nav__link.is-current", ["My Subscriptions"]),
    ],
    # -- Task 2: desktop header, expanded (2284:34854) --
    ("account.html", 1440, OPEN_MENU): [
        ("css", ".gb-acct-header", "background-color", "rgb(246, 254, 236)"),
        ("css", ".gb-acct-header", "box-shadow", "rgb(245, 241, 233) 0px -1px 0px 0px inset"),
        ("css", "[data-acct-menu]", "width", "221px"),
        ("css", "[data-acct-menu]", "height", "184px"),
        ("css", "[data-acct-menu]", "background-color", "rgb(246, 254, 236)"),
        ("css", "[data-acct-menu]", "border-bottom-left-radius", "8px"),
        ("css", "[data-acct-menu]", "border-top-left-radius", "0px"),
        ("css", "[data-acct-menu]", "padding-top", "4px"),
        ("css", ".gb-acct-menu__link", "height", "44px"),
        ("css", ".gb-acct-menu__link", "padding-left", "14px"),
        ("css", ".gb-acct-menu__link", "font-size", "16px"),
        ("css", ".gb-acct-menu__link", "line-height", "24px"),
        ("css", ".gb-acct-menu__link", "letter-spacing", "-0.32px"),
        ("css", ".gb-acct-menu__link", "color", "rgb(16, 24, 40)"),
        ("text", ".gb-acct-menu__link",
         ["Account Overview", "My Subscriptions", "My Details", "Log Out"]),
        ("vis", "[data-acct-menu]", True),
    ],
    # -- Task 2: mobile header (2284:34534 / 2284:34804) --
    ("account.html", 390, None): [
        ("css", ".gb-acct-header", "height", "64px"),
        ("css", ".gb-acct-header", "box-shadow", "rgb(245, 241, 233) 0px -0.5px 0px 0px inset"),
        ("css", ".gb-acct-header__bar", "padding-left", "20px"),
        ("css", ".gb-acct-header__bar", "align-items", "center"),
        ("css", ".gb-acct-header__logo", "height", "24px"),
        ("vis", "[data-acct-menu]", False),

        # -- Task 3: mobile in-page list card (2284:27617) --
        ("vis", ".gb-acct-nav", False),
        ("vis", ".gb-acct-list", True),
        ("css", ".gb-acct-list", "row-gap", "16px"),
        ("css", ".gb-acct-list__group", "background-color", "rgb(255, 255, 255)"),
        ("css", ".gb-acct-list__group", "border-radius", "8px"),
        # 0 here, unlike the desktop group's 8 -- the phone rows run edge to edge
        ("css", ".gb-acct-list__group", "padding-top", "0px"),
        # 350x68 with padding 24/16 actually applied (no fixed height to fight it)
        ("css", ".gb-acct-list__link", "height", "68px"),
        ("css", ".gb-acct-list__link", "padding-top", "24px"),
        ("css", ".gb-acct-list__link", "padding-left", "16px"),
        ("css", ".gb-acct-list__link", "font-size", "14px"),
        ("css", ".gb-acct-list__link", "line-height", "20px"),
        ("css", ".gb-acct-list__link", "letter-spacing", "-0.28px"),
        # Line 79: 326 wide inside a 350 group, so inset 12 each side, 1px #faf9f8
        ("css", ".gb-acct-list__item + .gb-acct-list__item::before",
         "background-color", "rgb(250, 249, 248)"),
        ("css", ".gb-acct-list__item + .gb-acct-list__item::before", "height", "1px"),
        ("css", ".gb-acct-list__item + .gb-acct-list__item::before", "left", "12px"),
        # The phone card omits Account Overview (you are on it) and Contact
        # Preferences, and Logout is a separate button below (Task 4) -- 6 rows.
        ("text", ".gb-acct-list__link",
         ["My Subscriptions", "Order History",
          "My Details", "Change Password",
          "Refer a Friend",
          "Help"]),
    ],
    ("account.html", 390, OPEN_MENU): [
        ("css", "[data-acct-menu]", "width", "164px"),
        ("css", "[data-acct-menu]", "height", "184px"),
        ("css", ".gb-acct-header", "background-color", "rgb(246, 254, 236)"),
        ("text", ".gb-acct-menu__link",
         ["Account", "My Subscriptions", "My Details", "Log Out"]),
    ],
}

CSS_GET = ("([s,p,pe])=>{const e=document.querySelector(s);"
           "return e?getComputedStyle(e,pe||null).getPropertyValue(p):null}")
# null means "no such element" -- kept distinct from false so a negative
# assertion cannot pass just because the anchor vanished (global rule 6)
# null means "no such element" here too -- an assertion must never pass because
# the anchor is missing (global rule 6)
HIDDEN_GET = ("s=>{const e=document.querySelector(s);return e?!e.hidden:null}")
VIS_GET = ("s=>{const e=document.querySelector(s);if(!e)return null;"
           "const r=e.getBoundingClientRect();"
           "return r.width>0&&r.height>0&&getComputedStyle(e).visibility!=='hidden'}")


def main():
    ok = red = 0
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=str(CHROME))
        for (page_name, w, action), checks in GROUPS.items():
            pg = b.new_page(viewport={"width": w, "height": 900})
            pg.goto((ROOT / page_name).as_uri())
            pg.wait_for_timeout(400)
            label = "%s@%d%s" % (page_name, w, " [%s]" % action if action else "")
            if action:
                trigger = {
                    OPEN_MENU: "[data-acct-menu-toggle]",
                    GOTO_SUBS: ".gb-acct-nav [data-acct-goto='subscriptions']",
                }[action]
                try:
                    pg.click(trigger, timeout=2000)
                    pg.wait_for_timeout(450)
                except Exception as e:
                    print("RED  %-52s cannot click %s: %s" % (label, trigger, type(e).__name__))
                    red += len(checks); pg.close(); continue
            for chk in checks:
                kind, sel = chk[0], chk[1]
                if kind == "css":
                    prop, want = chk[2], chk[3]
                    base, _, pseudo = sel.partition("::")
                    got = pg.evaluate(CSS_GET, [base, prop, "::" + pseudo if pseudo else None])
                    tag = "%s %s{%s}" % (label, sel, prop)
                    if got is None:
                        print("RED  %-52s element not found" % tag); red += 1
                    elif got.strip() == want:
                        ok += 1
                    else:
                        print("RED  %-52s want %s, got %s" % (tag, want, got)); red += 1
                elif kind == "text":
                    want = chk[2]
                    got = pg.eval_on_selector_all(sel, "els=>els.map(e=>e.innerText.trim())")
                    tag = "%s text(%s)" % (label, sel)
                    if got == want:
                        ok += 1
                    else:
                        print("RED  %-52s want %s, got %s" % (tag, want, got)); red += 1
                elif kind == "vis":
                    want = chk[2]
                    got = pg.evaluate(VIS_GET, sel)
                    tag = "%s visible(%s)" % (label, sel)
                    if got is None:
                        print("RED  %-52s element not found (anchor gone)" % tag); red += 1
                    elif got == want:
                        ok += 1
                    else:
                        print("RED  %-52s want visible=%s, got %s" % (tag, want, got)); red += 1
                elif kind == "shown":
                    want = chk[2]
                    got = pg.evaluate(HIDDEN_GET, sel)
                    tag = "%s shown(%s)" % (label, sel)
                    if got is None:
                        print("RED  %-52s element not found (anchor gone)" % tag); red += 1
                    elif got == want:
                        ok += 1
                    else:
                        print("RED  %-52s want shown=%s, got %s" % (tag, want, got)); red += 1
                elif kind == "absent":
                    got = pg.evaluate(VIS_GET, sel)
                    tag = "%s absent(%s)" % (label, sel)
                    if got in (None, False):
                        ok += 1
                    else:
                        print("RED  %-52s still renders" % tag); red += 1
            pg.close()
        b.close()
    print("\n%d ok / %d red" % (ok, red))
    sys.exit(1 if red else 0)


main()
