#!/usr/bin/env python3
"""account structure/value checks. Each task appends to CHECKS; run it whole.

Expected values come from the Figma nodes, never from a screenshot:
  desktop header  2284:34627 (closed) / 2284:34854 (expanded)
  mobile  header  2284:34534 (closed) / 2284:34804 (expanded)

Checks are grouped by (page, width, action) so each group costs one page load;
a per-check load made the run time out.
"""
import sys, pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = pathlib.Path.home() / ".cache/ms-playwright/chromium-1217/chrome-linux64/chrome"

OPEN_MENU = "open-menu"

# group key -> list of checks
#   ("css",  selector, prop, expected)
#   ("text", selector, [strings])
#   ("vis",  selector, bool)   element MUST exist; bool is whether it is shown
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
            label = "%s@%d%s" % (page_name, w, " [open]" if action else "")
            if action == OPEN_MENU:
                try:
                    pg.click("[data-acct-menu-toggle]", timeout=2000)
                    pg.wait_for_timeout(450)
                except Exception as e:
                    print("RED  %-52s cannot open menu: %s" % (label, type(e).__name__))
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
