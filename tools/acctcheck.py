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
# Playwright's build number moves whenever the package is reinstalled, and
# this box is shared -- pinning one made the whole run die mid-task.
def _chrome():
    base = pathlib.Path.home() / ".cache/ms-playwright"
    hits = sorted(base.glob("chromium-*/chrome-linux64/chrome"))
    if not hits:
        sys.exit("no chromium under %s -- run: npx playwright install chromium" % base)
    return hits[-1]

CHROME = _chrome()

OPEN_MENU = "open-menu"
GOTO_SUBS = "goto-subscriptions"
STATE_PREPARING = "state-preparing"
STATE_RENEWAL = "state-renewal"
GOTO_DETAIL = "goto-detail"
DETAIL_PAUSED = "detail-paused"
DETAIL_CANCELLED = "detail-cancelled"
DETAIL_DISCOUNT = "detail-discount"
DETAIL_LONGCODE = "detail-longcode"
GOTO_ORDERS = "goto-orders"
GOTO_ORDER = "goto-order"
GOTO_DETAILS = "goto-details"
GOTO_PASSWORD = "goto-password"
GOTO_HELP = "goto-help"
DETAILS_DIRTY = "details-dirty"
HELP_OPEN2 = "help-open-2"
# 2284:28878, the board's own worst case (note 34044)
LONG_CODE = "THISISADISAVERYVERYVERYVERYVERYLONGDISCOUNTCODE1265"

# All three views stay in the DOM; only one is shown. Detail checks are scoped
# so querySelector cannot reach the hidden copies in the other two.
D = "[data-acct-view='detail'] "
S = "[data-acct-view='subscriptions'] "
OH = "[data-acct-view='orders'] "
OD = "[data-acct-view='order'] "
MD = "[data-acct-view='details'] "
CP = "[data-acct-view='password'] "
HP = "[data-acct-view='help'] "
# state-scoped prefixes: the anchor selector is asserted visible in each group
# before any absence is claimed inside it
P = ".gb-acct-detail[data-acct-sub-state='paused'] "
C = ".gb-acct-detail[data-acct-sub-state='cancelled'] "
A = ".gb-acct-detail[data-acct-discount='applied'] "

# group key -> list of checks
#   ("css",  selector, prop, expected)
#   ("text", selector, [strings])
#   ("vis",  selector, bool)   element MUST exist; bool is whether it is shown
#   ("shown", selector, bool)  element MUST exist; bool is NOT having [hidden].
#                              Views are asserted this way, not with "vis": until
#                              Task 4 fills them they are empty and measure 0 tall,
#                              so a size test cannot tell "switched off" from "empty".
#   ("absent", selector)        element must not render at all
#   ("nofit", selector)         element's content must not overflow its own box,
#                               and the page must not scroll sideways
#   ("rect", selector, edge, px) distance from the viewport edge ("left"/"right")
#                               or the box's own "width", +/-1. Use this when the
#                               number to hold is where the ink lands, not which
#                               property puts it there.
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
        # Decision C (2026-09-10) turned four of these into real rows. The two
        # left dead have no board at all, not even a phone one, so building
        # them would mean inventing content (global rule 3).
        ("text", ".gb-acct-nav__link[aria-disabled='true']",
         ["Refer a Friend", "Contact Preferences"]),
        # Two-column shell (2284:27842). The asymmetric 244/352 gutters are
        # identical on all three desktop boards, so they are intended. They are
        # produced by 952 centred inside the shell's --pad-x, so assert where the
        # columns land -- the padding alone no longer carries the number.
        ("css", ".gb-acct__inner", "column-gap", "32px"),
        ("css", ".gb-acct__inner", "max-width", "952px"),
        ("css", ".gb-acct__inner", "padding-top", "48px"),
        ("css", ".gb-acct__inner", "padding-right", "108px"),
        ("css", ".gb-acct__inner", "padding-bottom", "144px"),
        ("rect", ".gb-acct-nav", "left", 244),
        ("rect", ".gb-acct__views", "right", 352),
        # The band and the wave cancel the shell padding and stay full-bleed.
        ("rect", ".gb-acct__wave", "left", 0),
        ("rect", ".gb-acct__wave", "right", 0),
        # default view
        ("shown", "[data-acct-view='overview']", True),
        ("shown", "[data-acct-view='subscriptions']", False),
        ("shown", "[data-acct-view='detail']", False),

        # -- Task 4: Overview, desktop (2284:27765) --
        ("css", ".gb-acct-ov", "row-gap", "16px"),
        # lime band 2284:27679, 203 tall from the top of the 80 header
        ("css", ".gb-acct::before", "height", "196px"),
        ("css", ".gb-acct__wave", "top", "187px"),
        ("css", ".gb-acct::before", "background-color", "rgb(231, 248, 208)"),
        # board fill 2284:27678 -- body is plain white, white cards need contrast
        ("css", ".gb-acct", "background-color", "rgb(250, 249, 248)"),
        # greeting 2284:27766 -- a card here, bare text on the phone
        ("css", ".gb-acct-hello", "background-color", "rgb(218, 246, 176)"),
        ("css", ".gb-acct-hello", "border-radius", "14px"),
        ("css", ".gb-acct-hello", "padding-top", "24px"),
        ("css", ".gb-acct-hello", "padding-left", "32px"),
        ("css", ".gb-acct-hello", "row-gap", "8px"),
        ("css", ".gb-acct-hello", "height", "136px"),
        ("css", ".gb-acct-hello__title", "font-size", "24px"),
        ("css", ".gb-acct-hello__title", "line-height", "30px"),
        ("css", ".gb-acct-hello__title", "letter-spacing", "-0.24px"),
        ("css", ".gb-acct-hello__title", "font-weight", "800"),
        ("css", ".gb-acct-hello__title", "color", "rgb(51, 51, 51)"),
        ("css", ".gb-acct-hello__sub", "font-size", "14px"),
        ("css", ".gb-acct-hello__sub", "line-height", "22px"),
        ("css", ".gb-acct-hello__sub", "color", "rgb(102, 102, 102)"),
        # order card 2284:27770, board shows the shipped state
        ("css", ".gb-acct-order", "background-color", "rgb(0, 86, 53)"),
        ("css", ".gb-acct-order", "border-radius", "8px"),
        ("css", ".gb-acct-order", "padding-top", "24px"),
        ("css", ".gb-acct-order", "padding-left", "32px"),
        ("css", ".gb-acct-order__label", "font-size", "20px"),
        ("css", ".gb-acct-order__label", "line-height", "30px"),
        ("css", ".gb-acct-order__label", "letter-spacing", "-0.4px"),
        ("css", ".gb-acct-order__label", "color", "rgb(255, 255, 255)"),
        ("css", ".gb-acct-order__status", "font-size", "20px"),
        ("css", ".gb-acct-order__status", "color", "rgb(181, 237, 97)"),
        ("css", ".gb-acct-order__note", "font-size", "14px"),
        ("css", ".gb-acct-order__note", "line-height", "22px"),
        ("css", ".gb-acct-order__cta", "height", "40px"),
        ("css", ".gb-acct-order__cta", "background-color", "rgb(255, 255, 255)"),
        ("css", ".gb-acct-order__cta", "color", "rgb(0, 86, 53)"),
        ("css", ".gb-acct-order__cta", "font-size", "16px"),
        ("text", ".gb-acct-order__cta", ["View Order"]),
        # refer card 2284:27780
        ("css", ".gb-acct-refer", "background-color", "rgb(245, 241, 233)"),
        ("css", ".gb-acct-refer", "border-radius", "8px"),
        ("css", ".gb-acct-refer", "padding-left", "32px"),
        ("css", ".gb-acct-refer", "column-gap", "16px"),
        ("css", ".gb-acct-refer__img", "width", "80px"),
        ("css", ".gb-acct-refer__img", "height", "80px"),
        ("css", ".gb-acct-refer__tag", "background-color", "rgb(203, 243, 144)"),
        ("css", ".gb-acct-refer__tag", "border-radius", "4px"),
        ("css", ".gb-acct-refer__tag", "color", "rgb(0, 65, 40)"),
        ("css", ".gb-acct-refer__action", "width", "40px"),
        ("css", ".gb-acct-refer__action", "background-color", "rgb(255, 255, 255)"),
        # the phone board's standalone Logout button is not on the desktop board --
        # Logout lives in the side rail there (Task 3)
        ("vis", ".gb-acct-logout", False),
    ],
    # -- Task 4: the two other order states (2284:27450 / 2284:27548) --
    # No JS switches these; the state is authored on the element. Asserting them
    # needs the attribute set from the outside, which is what SET_STATE does.
    ("account.html", 1440, STATE_PREPARING): [
        ("text", ".gb-acct-order__status", ["Preparing, Aug 13"]),
        ("text", ".gb-acct-order__note", ["We’re preparing your order."]),
        ("css", ".gb-acct-order", "background-color", "rgb(0, 86, 53)"),
        ("text", ".gb-acct-order__cta", ["View Order"]),
    ],
    ("account.html", 1440, STATE_RENEWAL): [
        # light card, dark text -- the inverse of the other two
        ("css", ".gb-acct-order", "background-color", "rgb(203, 243, 144)"),
        ("css", ".gb-acct-order__label", "background-color", "rgb(167, 231, 70)"),
        ("css", ".gb-acct-order__label", "border-radius", "4px"),
        ("css", ".gb-acct-order__label", "color", "rgb(0, 86, 53)"),
        ("css", ".gb-acct-order__status", "color", "rgb(0, 86, 53)"),
        ("css", ".gb-acct-order__cta", "background-color", "rgb(0, 86, 53)"),
        ("css", ".gb-acct-order__cta", "color", "rgb(255, 255, 255)"),
        ("text", ".gb-acct-order__label", ["It’s upcoming!"]),
        ("text", ".gb-acct-order__status", ["Renewal Date, Sep 13"]),
        ("text", ".gb-acct-order__cta", ["Manage Subscription"]),
    ],
    # -- Task 3: clicking a nav item swaps the view --
    ("account.html", 1440, GOTO_SUBS): [
        ("shown", "[data-acct-view='overview']", False),
        ("shown", "[data-acct-view='subscriptions']", True),
        ("css", ".gb-acct-nav__link.is-current", "background-color", "rgb(243, 243, 243)"),
        ("text", ".gb-acct-nav__link.is-current", ["My Subscriptions"]),

        # -- Task 5: My Subscriptions list (2284:28000) --
        ("css", ".gb-acct-subs", "row-gap", "16px"),
        ("css", ".gb-acct-intro", "background-color", "rgb(218, 246, 176)"),
        ("css", ".gb-acct-intro", "border-radius", "14px"),
        ("css", ".gb-acct-intro", "padding-top", "24px"),
        ("css", ".gb-acct-intro", "padding-left", "32px"),
        ("css", ".gb-acct-intro", "min-height", "136px"),
        ("css", ".gb-acct-intro__title", "font-size", "24px"),
        ("css", ".gb-acct-intro__title", "line-height", "30px"),
        ("css", ".gb-acct-intro__title", "font-weight", "800"),
        ("css", ".gb-acct-intro__title", "letter-spacing", "-0.24px"),
        ("css", ".gb-acct-intro__title", "color", "rgb(51, 51, 51)"),
        ("css", ".gb-acct-intro__sub", "font-size", "14px"),
        ("css", ".gb-acct-intro__sub", "line-height", "22px"),
        ("css", ".gb-acct-intro__sub", "color", "rgb(102, 102, 102)"),
        ("css", ".gb-acct-intro__sub", "max-width", "409px"),
        # 28000 has no back button: the side rail is the way out on desktop
        ("vis", ".gb-acct-intro__back", False),
        ("css", ".gb-acct-subs__list", "row-gap", "24px"),

        ("css", ".gb-acct-sub", "background-color", "rgb(255, 255, 255)"),
        ("css", ".gb-acct-sub", "border-top-width", "1px"),
        ("css", ".gb-acct-sub", "border-top-color", "rgb(230, 230, 230)"),
        ("css", ".gb-acct-sub", "border-radius", "12px"),
        ("css", ".gb-acct-sub__head", "padding-top", "20px"),
        ("css", ".gb-acct-sub__head", "padding-left", "20px"),
        ("css", ".gb-acct-sub__head", "justify-content", "space-between"),
        ("css", ".gb-acct-sub__head", "border-bottom-width", "1px"),
        ("css", ".gb-acct-sub__head", "border-bottom-color", "rgb(230, 230, 230)"),
        ("css", ".gb-acct-sub__title", "font-size", "16px"),
        ("css", ".gb-acct-sub__title", "line-height", "24px"),
        ("css", ".gb-acct-sub__title", "font-weight", "500"),
        ("css", ".gb-acct-sub__title", "letter-spacing", "-0.32px"),
        ("css", ".gb-acct-sub__title", "color", "rgb(26, 26, 26)"),

        # badge: 24 tall, radius 52, Inter 12/18 upper, 4/6/4/4 + gap 4
        ("css", ".gb-acct-pill", "height", "24px"),
        ("css", ".gb-acct-pill", "border-radius", "52px"),
        ("css", ".gb-acct-pill", "padding-left", "4px"),
        ("css", ".gb-acct-pill", "padding-right", "6px"),
        ("css", ".gb-acct-pill", "column-gap", "4px"),
        ("css", ".gb-acct-pill", "font-size", "12px"),
        ("css", ".gb-acct-pill", "line-height", "18px"),
        ("css", ".gb-acct-pill", "font-weight", "500"),
        ("css", ".gb-acct-pill", "text-transform", "uppercase"),
        ("css", ".gb-acct-pill__dot", "width", "16px"),
        ("css", ".gb-acct-pill__dot", "background-color", "rgb(255, 255, 255)"),
        # 11.742387 authored as 11.74 lands on the 1/64 grid as 11.7344, and a
        # border width is used at whole pixels, so 3.07 reads back as 3
        ("css", ".gb-acct-pill__dot::before", "width", "11.7344px"),
        ("css", ".gb-acct-pill__dot::before", "border-top-width", "3px"),
        ("css", "[data-acct-sub-state='active'] .gb-acct-pill", "background-color", "rgb(203, 243, 144)"),
        ("css", "[data-acct-sub-state='active'] .gb-acct-pill", "color", "rgb(0, 86, 53)"),
        ("css", "[data-acct-sub-state='active'] .gb-acct-pill__dot::before", "background-color", "rgb(181, 237, 97)"),
        ("css", "[data-acct-sub-state='active'] .gb-acct-pill__dot::before", "border-top-color", "rgb(0, 86, 53)"),
        ("css", "[data-acct-sub-state='paused'] .gb-acct-pill", "background-color", "rgb(255, 239, 195)"),
        ("css", "[data-acct-sub-state='paused'] .gb-acct-pill", "color", "rgb(253, 135, 26)"),
        ("css", "[data-acct-sub-state='paused'] .gb-acct-pill__dot::before", "background-color", "rgb(253, 245, 96)"),
        ("css", "[data-acct-sub-state='paused'] .gb-acct-pill__dot::before", "border-top-color", "rgb(253, 135, 26)"),
        ("css", "[data-acct-sub-state='cancelled'] .gb-acct-pill", "background-color", "rgb(204, 204, 204)"),
        ("css", "[data-acct-sub-state='cancelled'] .gb-acct-pill", "color", "rgb(77, 77, 77)"),
        ("css", "[data-acct-sub-state='cancelled'] .gb-acct-pill__dot::before", "background-color", "rgb(255, 255, 255)"),
        ("css", "[data-acct-sub-state='cancelled'] .gb-acct-pill__dot::before", "border-top-color", "rgb(102, 102, 102)"),

        ("css", ".gb-acct-sub__body", "padding-top", "24px"),
        ("css", ".gb-acct-sub__body", "row-gap", "24px"),
        ("css", ".gb-acct-sub__meta", "flex-direction", "row"),
        ("css", ".gb-acct-sub__meta", "column-gap", "16px"),
        ("css", ".gb-acct-sub__meta-item", "column-gap", "8px"),
        ("css", ".gb-acct-sub__icon", "width", "20px"),
        ("css", ".gb-acct-sub__icon", "height", "20px"),
        ("css", ".gb-acct-sub__meta-text", "row-gap", "4px"),
        ("css", ".gb-acct-sub__meta-label", "font-size", "14px"),
        ("css", ".gb-acct-sub__meta-label", "line-height", "20px"),
        ("css", ".gb-acct-sub__meta-label", "color", "rgb(102, 102, 102)"),
        ("css", ".gb-acct-sub__meta-value", "color", "rgb(26, 26, 26)"),
        ("css", ".gb-acct-sub__rule", "height", "1px"),
        ("css", ".gb-acct-sub__rule", "background-color", "rgb(230, 230, 230)"),
        ("css", ".gb-acct-sub__summary", "row-gap", "16px"),
        ("css", ".gb-acct-sub__product", "column-gap", "16px"),
        ("css", ".gb-acct-sub__product", "max-width", "308px"),
        ("css", ".gb-acct-sub__thumb", "width", "64px"),
        ("css", ".gb-acct-sub__thumb", "height", "64px"),
        ("css", ".gb-acct-sub__thumb", "border-radius", "4.57px"),
        ("css", ".gb-acct-sub__thumb", "background-color", "rgb(217, 217, 217)"),
        ("css", ".gb-acct-sub__product-text", "row-gap", "6px"),
        ("css", ".gb-acct-sub__product-name", "font-size", "14px"),
        ("css", ".gb-acct-sub__product-name", "color", "rgb(26, 26, 26)"),
        ("css", ".gb-acct-sub__product-qty", "font-size", "12px"),
        ("css", ".gb-acct-sub__product-qty", "line-height", "18px"),
        ("css", ".gb-acct-sub__product-qty", "color", "rgb(102, 102, 102)"),
        ("css", ".gb-acct-sub__totals", "justify-content", "space-between"),
        ("css", ".gb-acct-sub__more", "font-size", "12px"),
        ("css", ".gb-acct-sub__more", "color", "rgb(102, 102, 102)"),
        ("css", ".gb-acct-sub__total", "column-gap", "8px"),
        ("css", ".gb-acct-sub__total", "font-size", "14px"),
        ("css", ".gb-acct-sub__total", "color", "rgb(26, 26, 26)"),
        ("css", ".gb-acct-sub__foot", "padding-top", "4px"),
        ("css", ".gb-acct-sub__foot", "padding-left", "24px"),
        ("css", ".gb-acct-sub__foot", "padding-bottom", "24px"),
        ("css", ".gb-acct-sub__cta", "height", "44px"),
        ("css", ".gb-acct-sub__cta", "border-radius", "72px"),
        ("css", ".gb-acct-sub__cta", "background-color", "rgb(0, 86, 53)"),
        ("css", ".gb-acct-sub__cta", "color", "rgb(255, 255, 255)"),
        ("css", ".gb-acct-sub__cta", "font-size", "16px"),
        ("css", ".gb-acct-sub__cta", "font-weight", "500"),

        # 28127 / 28152 / 28159: paused dims the order summary, cancelled dims
        # the meta row as well. Nothing else on the card changes opacity.
        ("css", "[data-acct-sub-state='active'] .gb-acct-sub__summary", "opacity", "1"),
        ("css", "[data-acct-sub-state='paused'] .gb-acct-sub__meta", "opacity", "1"),
        ("css", "[data-acct-sub-state='paused'] .gb-acct-sub__summary", "opacity", "0.4"),
        ("css", "[data-acct-sub-state='cancelled'] .gb-acct-sub__meta", "opacity", "0.4"),
        ("css", "[data-acct-sub-state='cancelled'] .gb-acct-sub__summary", "opacity", "0.4"),
        # note 28323 and the phone board both drop the renewal line when
        # cancelled; the desktop board drops shipping instead (see SPEC 8)
        ("vis", "[data-acct-sub-state='active'] [data-acct-sub-renewal]", True),
        ("vis", "[data-acct-sub-state='cancelled'] [data-acct-sub-renewal]", False),
        ("vis", "[data-acct-sub-state='cancelled'] [data-acct-sub-shipping]", True),

        ("text", S + ".gb-acct-intro__title", ["My Subscriptions"]),
        ("text", S + ".gb-acct-sub__title", ["My Subscription"] * 3),
        ("text", S + ".gb-acct-pill", ["ACTIVE", "PAUSED", "CANCELLED"]),
        ("text", S + ".gb-acct-sub__more", ["+4 More Products"] * 3),
        # note 28321: paused shows the date it is paused until. Only the phone
        # boards (28315 / 34056) carry it; the desktop board left the sample
        # date alone (SPEC 8).
        ("text", "[data-acct-sub-state='paused'] .gb-acct-sub__meta-value",
         ["17 Aug 2026", "123 Express Ln, VIC 3121"]),
        ("text", "[data-acct-sub-state='active'] .gb-acct-sub__meta-value",
         ["19 Jul 2026", "123 Express Ln, VIC 3121"]),
        ("text", S + ".gb-acct-sub__cta",
         ["Manage Subscription", "Manage Subscription", "Re-Activate Subscription"]),
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
        ("text", ".gb-acct-list__link[aria-disabled='true']", ["Refer a Friend"]),

        # -- Task 4: Overview, phone (2284:27604) --
        # The greeting is bare here (2284:27610), not the desktop's lime card
        ("css", ".gb-acct-hello", "background-color", "rgba(0, 0, 0, 0)"),
        ("css", ".gb-acct-hello", "padding-left", "0px"),
        ("css", ".gb-acct__inner", "padding-top", "8px"),
        # Phone gutters come from the shell now, not from __inner's own padding.
        ("rect", ".gb-acct__views", "left", 20),
        ("rect", ".gb-acct__views", "right", 20),
        ("rect", ".gb-acct__wave", "left", 0),
        ("rect", ".gb-acct__wave", "right", 0),
        ("css", ".gb-acct-ov", "padding-top", "32px"),
        ("css", ".gb-acct-hello__title", "font-size", "20px"),
        ("css", ".gb-acct-hello__title", "line-height", "24px"),
        ("css", ".gb-acct-hello__title", "letter-spacing", "-0.2px"),
        ("css", ".gb-acct-hello__sub", "font-size", "12px"),
        ("css", ".gb-acct-hello__sub", "line-height", "18px"),
        # no back arrow: 2284:27611 is visible=false on the board
        ("absent", ".gb-acct-hello__back"),
        # lime band 2284:27606, 240 tall from the top of the 64 header
        ("css", ".gb-acct::before", "height", "176px"),
        ("css", ".gb-acct__wave", "top", "176px"),
        # 2284:27653: the photo is wider than its clip, so the global
        # img{max-width:100%} must not apply or the rotation spins a squashed box
        ("css", ".gb-acct-hello__bear", "max-width", "none"),
        # 156.3 comes back as 156.297: computed lengths are quantised to 1/64px
        ("css", ".gb-acct-hello__bear", "width", "156.297px"),
        # order card shrinks its type and pads 24 all round instead of 24/32
        ("css", ".gb-acct-order", "padding-left", "24px"),
        ("css", ".gb-acct-order__label", "font-size", "16px"),
        ("css", ".gb-acct-order__label", "line-height", "24px"),
        ("css", ".gb-acct-order__status", "font-size", "18px"),
        ("css", ".gb-acct-order__status", "line-height", "26px"),
        ("css", ".gb-acct-order__note", "font-size", "12px"),
        ("css", ".gb-acct-order__note", "line-height", "18px"),
        # refer card 2284:27639
        ("css", ".gb-acct-refer", "padding-left", "16px"),
        ("css", ".gb-acct-refer__img", "width", "66px"),
        ("css", ".gb-acct-refer__action", "width", "32px"),
        # standalone Logout button 2284:27648, phone only
        ("vis", ".gb-acct-logout", True),
        ("css", ".gb-acct-logout", "height", "52px"),
        ("css", ".gb-acct-logout", "border-radius", "72px"),
        ("css", ".gb-acct-logout", "background-color", "rgb(0, 86, 53)"),
        ("css", ".gb-acct-logout", "color", "rgb(255, 255, 255)"),
        ("css", ".gb-acct-logout", "font-size", "16px"),
        ("css", ".gb-acct-logout", "line-height", "28px"),
        ("css", ".gb-acct-logout", "letter-spacing", "0.48px"),
    ],
    # -- Task 5: My Subscriptions list, phone (2284:28305 / 34046) --
    ("account.html", 390, GOTO_SUBS): [
        ("shown", "[data-acct-view='subscriptions']", True),
        # the card drops on the phone -- plain text on the lime band, and the
        # back button that 27604 keeps hidden is visible here
        ("css", ".gb-acct-intro", "background-color", "rgba(0, 0, 0, 0)"),
        ("css", ".gb-acct-intro", "padding-top", "0px"),
        ("css", ".gb-acct-intro", "min-height", "0px"),
        ("css", ".gb-acct-intro", "row-gap", "16px"),
        ("vis", ".gb-acct-intro__back", True),
        ("css", ".gb-acct-intro__back", "width", "32px"),
        ("css", ".gb-acct-intro__back", "height", "32px"),
        ("css", ".gb-acct-intro__back", "border-radius", "40px"),
        ("css", ".gb-acct-intro__back", "background-color", "rgb(255, 255, 255)"),
        ("css", ".gb-acct-intro__text", "row-gap", "8px"),
        ("css", ".gb-acct-intro__title", "font-size", "20px"),
        ("css", ".gb-acct-intro__title", "line-height", "24px"),
        ("css", ".gb-acct-intro__title", "letter-spacing", "-0.2px"),
        ("css", ".gb-acct-intro__sub", "font-size", "12px"),
        ("css", ".gb-acct-intro__sub", "line-height", "18px"),
        ("css", ".gb-acct-subs__list", "row-gap", "32px"),
        ("css", ".gb-acct-sub__body", "padding-top", "20px"),
        ("css", ".gb-acct-sub__meta", "flex-direction", "column"),
        ("css", ".gb-acct-sub__meta", "row-gap", "16px"),
        ("css", ".gb-acct-sub__foot", "padding-top", "8px"),
        ("css", ".gb-acct-sub__foot", "padding-left", "16px"),
        ("css", ".gb-acct-sub__foot", "padding-bottom", "20px"),
        # 28316: same three states as desktop, same dimming
        ("css", "[data-acct-sub-state='cancelled'] .gb-acct-sub__meta", "opacity", "0.4"),
        ("vis", "[data-acct-sub-state='cancelled'] [data-acct-sub-renewal]", False),
    ],
    # -- Task 6: Subscription Detail, ACTIVE (2284:27792) --
    # Every selector is scoped to the view: the other two views stay in the DOM
    # behind [hidden], and querySelector would reach their copies first.
    ("account.html", 1440, GOTO_DETAIL): [
        ("shown", "[data-acct-view='detail']", True),
        ("shown", "[data-acct-view='subscriptions']", False),
        ("css", ".gb-acct-detail", "row-gap", "16px"),
        # 27792 sets no tracking on this one, so it must not inherit the card's
        # -0.32 the way it did before r/Task 24. Not the 14px tier's -0.28 either.
        ("css", D + ".gb-acct-schedule__title", "letter-spacing", "normal"),

        # 27860: same lime card as the list page, but the back button shows on
        # desktop too and the subtitle is replaced by a pencil
        ("vis", D + ".gb-acct-intro__back", True),
        ("css", D + ".gb-acct-intro", "min-height", "136px"),
        ("css", D + ".gb-acct-intro", "row-gap", "16px"),
        ("css", D + ".gb-acct-intro__text", "flex-direction", "row"),
        ("css", D + ".gb-acct-intro__text", "column-gap", "8px"),
        ("css", D + ".gb-acct-intro__title", "font-size", "24px"),
        ("css", D + ".gb-acct-intro__edit", "width", "20px"),
        ("css", D + ".gb-acct-intro__edit", "height", "20px"),
        ("css", D + ".gb-acct-intro__edit", "color", "rgb(51, 51, 51)"),
        ("absent", D + ".gb-acct-intro__sub"),

        # 27866: the detail head pads 24 at the sides, the list head pads 20
        ("css", D + ".gb-acct-sub__head", "padding-left", "24px"),
        ("css", D + ".gb-acct-sub__body", "padding-top", "24px"),
        ("css", D + ".gb-acct-sub__body", "row-gap", "24px"),

        # 27871 / 27882 / 27966 / 27973: icon + label/value + optional Edit
        ("css", D + ".gb-acct-row", "justify-content", "space-between"),
        ("css", D + ".gb-acct-row", "column-gap", "4px"),
        ("css", D + ".gb-acct-row__main", "column-gap", "8px"),
        ("css", D + ".gb-acct-row__icon", "width", "20px"),
        ("css", D + ".gb-acct-row__icon", "height", "20px"),
        ("css", D + ".gb-acct-row__icon", "color", "rgb(102, 102, 102)"),
        ("css", D + ".gb-acct-row__text", "row-gap", "4px"),
        ("css", D + ".gb-acct-row__label", "font-size", "14px"),
        ("css", D + ".gb-acct-row__label", "line-height", "20px"),
        ("css", D + ".gb-acct-row__label", "color", "rgb(102, 102, 102)"),
        # 27877 is 18/26, bigger than every other value on the card
        ("css", D + ".gb-acct-row__date", "font-size", "18px"),
        ("css", D + ".gb-acct-row__date", "line-height", "26px"),
        ("css", D + ".gb-acct-row__date", "letter-spacing", "-0.36px"),
        ("css", D + ".gb-acct-row__date", "color", "rgb(26, 26, 26)"),
        ("css", D + ".gb-acct-row__note", "margin-top", "4px"),
        ("css", D + ".gb-acct-row__note", "color", "rgb(102, 102, 102)"),
        # 27887 / 27971 / 27978 are navy, not the gray-900 the list card uses
        ("css", D + ".gb-acct-row__value", "color", "rgb(16, 24, 40)"),

        # 27888 / 27960 / 27998: blue, underlined
        ("css", D + ".gb-acct-link", "color", "rgb(3, 116, 165)"),
        ("css", D + ".gb-acct-link", "text-decoration-line", "underline"),
        ("css", D + ".gb-acct-link", "font-size", "14px"),
        ("css", D + ".gb-acct-link", "line-height", "20px"),
        ("css", D + ".gb-acct-link--sm", "font-size", "12px"),
        ("css", D + ".gb-acct-link--sm", "line-height", "18px"),

        ("css", D + ".gb-acct-btn", "height", "44px"),
        ("css", D + ".gb-acct-btn", "border-radius", "72px"),
        ("css", D + ".gb-acct-btn", "background-color", "rgb(0, 86, 53)"),
        ("css", D + ".gb-acct-btn", "color", "rgb(255, 255, 255)"),
        ("css", D + ".gb-acct-btn", "column-gap", "8px"),
        ("css", D + ".gb-acct-btn", "padding-left", "40px"),
        ("css", D + ".gb-acct-btn", "font-size", "16px"),
        ("css", D + ".gb-acct-btn", "font-weight", "500"),
        ("css", D + ".gb-acct-btn__icon", "width", "20px"),
        # 27996 is the only outline button on the page: 2px stroke, no fill
        ("css", D + ".gb-acct-btn--ghost", "background-color", "rgba(0, 0, 0, 0)"),
        ("css", D + ".gb-acct-btn--ghost", "border-top-width", "2px"),
        ("css", D + ".gb-acct-btn--ghost", "border-top-color", "rgb(0, 86, 53)"),
        ("css", D + ".gb-acct-btn--ghost", "color", "rgb(0, 86, 53)"),
        ("css", D + ".gb-acct-detail__actions", "row-gap", "8px"),

        # 27890: the row frame is a fixed 62 while its text column measures 68,
        # so the last line hangs 6 into the 24 gap. Reproduced, not corrected.
        ("css", D + ".gb-acct-product", "height", "62px"),
        ("css", D + ".gb-acct-product", "column-gap", "4px"),
        ("css", D + ".gb-acct-product__thumb", "width", "62px"),
        ("css", D + ".gb-acct-product__thumb", "height", "62px"),
        ("css", D + ".gb-acct-product__thumb", "border-radius", "4.43px"),
        ("css", D + ".gb-acct-product__thumb", "background-color", "rgb(217, 217, 217)"),
        ("css", D + ".gb-acct-product__info", "row-gap", "8px"),
        ("css", D + ".gb-acct-product__info", "align-items", "flex-end"),
        ("css", D + ".gb-acct-product__top", "justify-content", "space-between"),
        ("css", D + ".gb-acct-product__name", "column-gap", "3px"),
        ("css", D + ".gb-acct-product__name", "max-width", "212px"),
        ("css", D + ".gb-acct-product__name", "color", "rgb(16, 24, 40)"),
        ("css", D + ".gb-acct-product__qty", "text-align", "center"),
        ("css", D + ".gb-acct-product__meta", "width", "217px"),
        ("css", D + ".gb-acct-product__meta", "justify-content", "space-between"),
        ("css", D + ".gb-acct-product__meta", "column-gap", "6px"),
        ("css", D + ".gb-acct-product__flavour", "color", "rgb(102, 102, 102)"),
        ("css", D + ".gb-acct-product__price", "column-gap", "2px"),
        ("css", D + ".gb-acct-product__was", "text-decoration-line", "line-through"),
        ("css", D + ".gb-acct-product__was", "color", "rgb(102, 102, 102)"),
        ("css", D + ".gb-acct-product__was", "font-size", "12px"),
        ("css", D + ".gb-acct-product__now", "color", "rgb(26, 26, 26)"),
        ("css", D + ".gb-acct-product__now", "font-weight", "500"),
        ("css", D + ".gb-acct-product__now", "letter-spacing", "-0.12px"),

        ("css", D + ".gb-acct-detail__add", "row-gap", "16px"),
        ("css", D + ".gb-acct-detail__deadline", "font-size", "12px"),
        ("css", D + ".gb-acct-detail__deadline", "line-height", "18px"),
        ("css", D + ".gb-acct-detail__deadline", "color", "rgb(102, 102, 102)"),

        ("css", D + ".gb-acct-summary", "row-gap", "12px"),
        ("css", D + ".gb-acct-summary__head", "row-gap", "16px"),
        ("css", D + ".gb-acct-summary__lines", "row-gap", "8px"),
        ("css", D + ".gb-acct-summary__row", "justify-content", "space-between"),
        ("css", D + ".gb-acct-summary__row", "font-size", "14px"),
        ("css", D + ".gb-acct-summary__row", "color", "rgb(102, 102, 102)"),
        ("css", D + ".gb-acct-summary__discount", "column-gap", "8px"),
        ("vis", D + ".gb-acct-summary__kind", True),
        ("text", D + ".gb-acct-summary__kind", ["Automatic"]),
        ("css", D + ".gb-acct-tag", "background-color", "rgb(203, 243, 144)"),
        ("css", D + ".gb-acct-tag", "border-radius", "4px"),
        ("css", D + ".gb-acct-tag", "padding-left", "8px"),
        ("css", D + ".gb-acct-tag", "padding-top", "2px"),
        ("css", D + ".gb-acct-tag", "color", "rgb(0, 65, 40)"),
        ("css", D + ".gb-acct-summary__total", "font-size", "16px"),
        ("css", D + ".gb-acct-summary__total", "line-height", "24px"),
        ("css", D + ".gb-acct-summary__total", "color", "rgb(1, 19, 7)"),

        ("css", D + ".gb-acct-schedule", "row-gap", "24px"),
        ("css", D + ".gb-acct-schedule__title", "font-size", "14px"),
        ("css", D + ".gb-acct-schedule__title", "font-weight", "500"),
        ("css", D + ".gb-acct-schedule__title", "color", "rgb(26, 26, 26)"),
        ("css", D + ".gb-acct-schedule__days", "column-gap", "16px"),
        # the desktop strip is the phone block scaled 1.1554 -- every metric
        # (8 radius, 1 border, 24/12 padding, 16/24 type) carries the factor
        ("css", D + ".gb-acct-schedule__day", "background-color", "rgb(245, 241, 233)"),
        ("css", D + ".gb-acct-schedule__day", "border-top-color", "rgb(230, 230, 230)"),
        ("css", D + ".gb-acct-schedule__day", "border-radius", "9.24px"),
        ("css", D + ".gb-acct-schedule__day", "font-size", "18.49px"),
        ("css", D + ".gb-acct-schedule__day", "line-height", "27.73px"),
        ("css", D + ".gb-acct-schedule__day", "color", "rgb(16, 24, 40)"),

        # 27858 gaps 48 to the link while 27859 gaps 16 inside, so the link
        # carries the extra 32 itself
        ("css", ".gb-acct-detail__cancel", "margin-top", "32px"),
        ("css", ".gb-acct-detail__cancel", "text-align", "center"),

        ("text", D + ".gb-acct-intro__title", ["My Subscription"]),
        ("text", D + ".gb-acct-row__label",
         ["Next renewal date", "Frequency", "Shipping", "Payment Method"]),
        ("text", D + ".gb-acct-row__date", ["19 Jul 2026"]),
        ("text", D + ".gb-acct-row__note", ["Est Delivery 3-6 business days"]),
        ("text", D + ".gb-acct-btn", ["Edit Date", "I need it now", "Add Items", "Skip next order"]),
        ("text", D + ".gb-acct-product__now", ["$121.50"] * 4),
        ("text", D + ".gb-acct-schedule__day", ["19 Jun", "17 Jul", "14 Aug", "11 Sep"]),
        ("text", ".gb-acct-detail__cancel", ["Cancel Subscription"]),
        # every Edit entry point carries its modal hook, Task 8 wires them
        ("vis", D + "[data-acct-modal='edit-name']", True),
        ("vis", D + "[data-acct-modal='edit-date']", True),
        ("vis", D + "[data-acct-modal='need-now']", True),
        ("vis", D + "[data-acct-modal='edit-frequency']", True),
        ("vis", D + "[data-acct-modal='edit-product']", True),
        ("vis", D + "[data-acct-modal='add-product']", True),
        ("vis", D + "[data-acct-modal='discount-add']", True),
        ("vis", D + "[data-acct-modal='shipping-current']", True),
        ("vis", D + "[data-acct-modal='edit-payment']", True),
        ("vis", D + "[data-acct-modal='skip-next']", True),
        ("vis", D + "[data-acct-modal='cancel-offer-skip']", True),
        # -- Task 7: the state-only pieces must stay out of the base state.
        # Each negative below is paired with the positive above so a wrong
        # selector cannot make it pass by matching nothing (global rule 6).
        ("absent", D + "[data-acct-modal='restart']"),
        ("absent", D + "[data-acct-modal='discount-applied']"),
        ("absent", D + ".gb-acct-detail__restart-note"),
        ("absent", D + ".gb-acct-product__stock"),
        ("vis", D + ".gb-acct-product--oos .gb-acct-product__was", True),
        ("absent", D + ".gb-acct-summary__code"),
        ("vis", D + ".gb-acct-row--renewal", True),
        ("vis", D + ".gb-acct-summary__row--discount", True),
    ],
    # -- Task 6: Subscription Detail, phone (2284:28330) --
    ("account.html", 390, GOTO_DETAIL): [
        ("shown", "[data-acct-view='detail']", True),
        # 28337: no lime card here either, and the title row gaps 16 not 8
        ("css", D + ".gb-acct-intro", "min-height", "0px"),
        ("css", D + ".gb-acct-intro", "background-color", "rgba(0, 0, 0, 0)"),
        ("css", D + ".gb-acct-intro__text", "column-gap", "16px"),
        ("css", D + ".gb-acct-intro__title", "font-size", "20px"),
        ("css", D + ".gb-acct-intro__title", "line-height", "24px"),
        ("vis", D + ".gb-acct-intro__back", True),
        # 28345 pads 20 all round, unlike the desktop head
        ("css", D + ".gb-acct-sub__head", "padding-left", "20px"),
        ("css", D + ".gb-acct-sub__body", "padding-top", "20px"),
        # 28466 is the unscaled block the desktop one is derived from
        ("css", D + ".gb-acct-schedule__day", "border-radius", "8px"),
        ("css", D + ".gb-acct-schedule__day", "font-size", "16px"),
        ("css", D + ".gb-acct-schedule__day", "line-height", "24px"),
        ("css", D + ".gb-acct-schedule__days", "column-gap", "8px"),
        # 28433 drops the "Automatic" label and shows the tag alone
        ("vis", D + ".gb-acct-summary__kind", False),
    ],
    # -- Task 7: PAUSED (2284:28627 / 28774) --
    # Every negative here is anchored: the state selector itself is asserted
    # visible first, so a typo in it cannot turn the absences green.
    ("account.html", 390, DETAIL_PAUSED): [
        ("vis", ".gb-acct-detail[data-acct-sub-state='paused']", True),
        # note 34042: no skipping while the subscription is paused
        ("absent", "%s[data-acct-modal='skip-next']" % P),
        # everything else the active state has is still there
        ("vis", "%s[data-acct-modal='edit-date']" % P, True),
        ("vis", "%s[data-acct-modal='need-now']" % P, True),
        ("vis", "%s[data-acct-modal='cancel-offer-skip']" % P, True),
        ("vis", "%s.gb-acct-row--renewal" % P, True),
        ("text", D + ".gb-acct-pill", ["PAUSED"]),
        ("css", D + ".gb-acct-pill", "background-color", "rgb(255, 239, 195)"),
        # 28647: only the label changes, the date and the delivery line stay
        ("text", D + ".gb-acct-row__label",
         ["Subscription restarts", "Frequency", "Shipping", "Payment Method"]),
        ("text", D + ".gb-acct-row__date", ["19 Jul 2026"]),
        # 28627 shows no disabled treatment at all: this is the anchor for the
        # cancelled group's colour assertions
        ("vis", "%s.gb-acct-intro__edit" % P, True),
        ("css", P + ".gb-acct-row .gb-acct-link", "color", "rgb(3, 116, 165)"),
        ("css", P + ".gb-acct-schedule__day", "background-color", "rgb(245, 241, 233)"),
        ("css", P + "[data-acct-modal='add-product']", "background-color", "rgb(0, 86, 53)"),
    ],
    # -- Task 7: PAUSED at desktop -- no board exists, so this only proves the
    # state mechanism is not breakpoint-bound
    ("account.html", 1440, DETAIL_PAUSED): [
        ("vis", ".gb-acct-detail[data-acct-sub-state='paused']", True),
        ("absent", "%s[data-acct-modal='skip-next']" % P),
        ("text", D + ".gb-acct-pill", ["PAUSED"]),
    ],
    # -- Task 7: CANCELLED (2284:34058) --
    ("account.html", 390, DETAIL_CANCELLED): [
        ("vis", ".gb-acct-detail[data-acct-sub-state='cancelled']", True),
        ("absent", "%s.gb-acct-row--renewal" % C),
        ("absent", "%s[data-acct-modal='edit-date']" % C),
        ("absent", "%s[data-acct-modal='need-now']" % C),
        ("absent", "%s.gb-acct-summary__row--discount" % C),
        ("absent", "%s.gb-acct-detail__cancel" % C),
        ("vis", "%s[data-acct-modal='restart']" % C, True),
        ("vis", "%s.gb-acct-detail__restart-note" % C, True),
        ("vis", "%s.gb-acct-product__stock" % C, True),
        # 34058 keeps Skip -- the opposite of PAUSED
        ("vis", "%s[data-acct-modal='skip-next']" % C, True),
        ("text", D + ".gb-acct-pill", ["CANCELLED"]),
        ("text", D + "[data-acct-modal='restart']", ["Restart Subscription"]),
        ("text", D + ".gb-acct-detail__restart-note",
         ["You will be bale to make changes to your subscription once restarted."]),
        ("text", D + ".gb-acct-product__stock", ["Out of stock"]),
        ("css", D + ".gb-acct-product__stock", "color", "rgb(221, 101, 94)"),
        ("css", D + ".gb-acct-product__stock", "font-size", "12px"),
        ("css", D + ".gb-acct-detail__restart-note", "text-align", "center"),
        ("css", D + ".gb-acct-detail__restart-note", "font-size", "12px"),
        # only the first row swaps: one price, no strikethrough beside it.
        # innerText of a rendered <p> skips its display:none children, so this
        # reads the shown price rather than both.
        ("absent", "%s.gb-acct-product--oos .gb-acct-product__was" % C),
        ("text", D + ".gb-acct-product--oos .gb-acct-product__price", ["$00.00"]),
        # 34058 also draws the whole card disabled -- 7 Edit links, both grey
        # buttons, the date blocks, and the out-of-stock name struck through
        ("absent", "%s.gb-acct-intro__edit" % C),
        ("css", C + ".gb-acct-row .gb-acct-link", "color", "rgba(128, 128, 128, 0.4)"),
        ("css", C + ".gb-acct-row .gb-acct-link", "text-decoration-line", "none"),
        ("css", C + ".gb-acct-product .gb-acct-link", "pointer-events", "none"),
        ("css", C + "[data-acct-modal='add-product']", "background-color", "rgb(230, 230, 230)"),
        ("css", C + "[data-acct-modal='add-product']", "color", "rgb(128, 128, 128)"),
        ("css", C + "[data-acct-modal='skip-next']", "background-color", "rgb(230, 230, 230)"),
        ("css", C + "[data-acct-modal='skip-next']", "border-top-width", "1px"),
        ("css", C + ".gb-acct-schedule__day", "background-color", "rgb(230, 230, 230)"),
        ("css", C + ".gb-acct-schedule__day", "color", "rgb(128, 128, 128)"),
        ("css", C + ".gb-acct-product--oos .gb-acct-product__label", "color", "rgb(221, 101, 94)"),
        ("css", C + ".gb-acct-product--oos .gb-acct-product__label",
         "text-decoration-line", "line-through"),
        # 34094: the quantity is not struck through with it
        ("css", C + ".gb-acct-product--oos .gb-acct-product__qty", "color", "rgb(16, 24, 40)"),
        ("css", C + ".gb-acct-product--oos .gb-acct-product__qty",
         "text-decoration-line", "none"),
        # the Restart button and the discount link are the two things left live
        ("css", C + "[data-acct-modal='restart']", "background-color", "rgb(0, 86, 53)"),
        ("css", C + "[data-acct-modal='discount-add']", "color", "rgb(3, 116, 165)"),
    ],
    # -- Task 7: discount code applied (2284:28478), note 30921 --
    ("account.html", 390, DETAIL_DISCOUNT): [
        ("vis", ".gb-acct-detail[data-acct-discount='applied']", True),
        ("vis", "%s.gb-acct-summary__code" % A, True),
        ("vis", "%s[data-acct-modal='discount-applied']" % A, True),
        ("absent", "%s[data-acct-modal='discount-add']" % A),
        ("text", D + ".gb-acct-summary__code", ["DISCOUNTCODE"]),
        ("text", D + "[data-acct-modal='discount-applied']", ["Edit discount code"]),
        # 28582: right-aligned in a fixed 118 so a long code wraps in place (28878)
        ("css", D + ".gb-acct-summary__code", "width", "118px"),
        ("css", D + ".gb-acct-summary__code", "text-align", "right"),
        ("css", D + ".gb-acct-summary__code", "font-size", "12px"),
        ("css", D + ".gb-acct-summary__code", "color", "rgb(102, 102, 102)"),
        # the invariant the long-code group is measured against: a code that
        # fits on one line leaves the block at the active state's own height
        ("css", D + ".gb-acct-summary", "height", "150px"),
    ],
    # -- Task 7: a 51-character code must wrap inside its own 118, not push the
    # tag off the row or widen the page (2284:28774, note 34044) --
    ("account.html", 390, DETAIL_LONGCODE): [
        ("vis", ".gb-acct-detail[data-acct-discount='applied']", True),
        ("nofit", D + ".gb-acct-summary__code"),
        ("nofit", D + ".gb-acct-summary__row--discount"),
        ("css", D + ".gb-acct-summary__code", "width", "118px"),
        # 28878 wraps to 4 lines of 18 inside the 118, which is what takes the
        # block from 150 to the board's 198 -- height, not just "it fits"
        ("css", D + ".gb-acct-summary__code", "height", "72px"),
        ("css", D + ".gb-acct-summary", "height", "198px"),
        ("vis", D + ".gb-acct-tag", True),
    ],
    ("account.html", 1440, DETAIL_LONGCODE): [
        ("nofit", D + ".gb-acct-summary__code"),
        ("nofit", D + ".gb-acct-summary__row--discount"),
        ("css", D + ".gb-acct-summary__code", "height", "72px"),
        ("css", D + ".gb-acct-summary", "height", "198px"),
    ],
    ("account.html", 390, OPEN_MENU): [
        ("css", "[data-acct-menu]", "width", "164px"),
        ("css", "[data-acct-menu]", "height", "184px"),
        ("css", ".gb-acct-header", "background-color", "rgb(246, 254, 236)"),
        ("text", ".gb-acct-menu__link",
         ["Account", "My Subscriptions", "My Details", "Log Out"]),
    ],

    # -- Task 16: the five views added by decision C (2026-09-10).
    # Only the page heading changes between phone and desktop -- 20/24 -> 24/30,
    # measured on 27792 vs 28330. Every other step (16/24, 14/20, 12/18) is the
    # same on both, which is why these groups assert the title size at both
    # widths and nothing else about type.
    ("account.html", 1440, GOTO_ORDERS): [
        ("shown", "[data-acct-view='orders']", True),
        ("shown", "[data-acct-view='overview']", False),
        ("text", OH + ".gb-acct-intro__title", ["Order History"]),
        ("text", OH + ".gb-acct-intro__sub",
         ["Review, track, or create a return for your orders."]),
        ("css", OH + ".gb-acct-intro__title", "font-size", "24px"),
        ("css", OH + ".gb-acct-intro__title", "line-height", "30px"),
        ("vis", ".gb-acct-nav__link[data-acct-goto='orders'].is-current", True),
        # -- Task 20 --
        # Five cards. Three carry different statuses and the last two repeat the
        # second verbatim -- the board's own duplication, SPEC 8.
        ("text", OH + ".gb-acct-card__title",
         ["Order #12345679", "Order #12345680", "Order #12345681",
          "Order #12345680", "Order #12345680"]),
        ("text", OH + ".gb-acct-hist__value",
         ["Aug 14, 2026", "Shipped", "$89.99",
          "Aug 15, 2026", "Delivered", "$45.00",
          "Aug 16, 2026", "Cancelled", "$0.00",
          "Aug 15, 2026", "Delivered", "$45.00",
          "Aug 15, 2026", "Delivered", "$45.00"]),
        # every status is #1a1a1a on the board -- no colour tells them apart
        ("css", OH + ".gb-acct-hist__value", "color", "rgb(26, 26, 26)"),
        ("css", OH + ".gb-acct-hist__label", "color", "rgb(102, 102, 102)"),
        ("css", OH + ".gb-acct-hist__row", "column-gap", "4px"),
        ("css", OH + ".gb-acct-hist", "row-gap", "8px"),
        ("css", OH + ".gb-acct-cards", "row-gap", "24px"),
        ("css", OH + ".gb-acct-stack", "row-gap", "32px"),
        ("text", OH + ".gb-acct-btn",
         ["View Order", "View Order", "View Order", "View Order", "View Order"]),
        # 45 = a 1px rule on top + 12 + 20 + 12. The board draws top only
        # (individualStrokeWeights right/bottom/left are 0).
        ("css", OH + ".gb-acct-pager", "height", "45px"),
        ("css", OH + ".gb-acct-pager", "border-top-width", "1px"),
        ("css", OH + ".gb-acct-pager", "border-top-color", "rgb(234, 236, 240)"),
        ("css", OH + ".gb-acct-pager", "border-bottom-width", "0px"),
        ("css", OH + ".gb-acct-pager", "padding-left", "16px"),
        ("text", OH + ".gb-acct-pager__label", ["Page 1 of 10"]),
        # the board's letterSpacing is 0, which computes as normal, not 0px
        ("css", OH + ".gb-acct-pager__label", "letter-spacing", "normal"),
        ("css", OH + ".gb-acct-pager__label", "color", "rgb(77, 77, 77)"),
        ("css", OH + ".gb-acct-pager__btn", "width", "36px"),
        ("css", OH + ".gb-acct-pager__btn", "height", "36px"),
        ("css", OH + ".gb-acct-pager__btn", "border-radius", "8px"),
        ("nofit", OH + ".gb-acct-stack"),
    ],
    ("account.html", 390, GOTO_ORDERS): [
        ("css", OH + ".gb-acct-intro__title", "font-size", "20px"),
        ("css", OH + ".gb-acct-intro__title", "line-height", "24px"),
        ("vis", OH + ".gb-acct-intro__back", True),
        ("css", OH + ".gb-acct-card", "width", "350px"),
        ("css", OH + ".gb-acct-card", "height", "230px"),
        ("nofit", OH + ".gb-acct-stack"),
    ],
    # -- Task 18: My Details (2284:27081; 27116 is the same board, decision O) --
    # Three cards at gap 24, then Save, then the note -- the outer column is
    # gap 32. The phone board's Save is #e6e6e6 on #808080: it ships disabled and
    # acctForm wakes it when a field actually changes (note 27446).
    ("account.html", 1440, GOTO_DETAILS): [
        ("shown", "[data-acct-view='details']", True),
        ("text", MD + ".gb-acct-intro__title", ["Your details"]),
        ("css", MD + ".gb-acct-intro__title", "font-size", "24px"),
        ("vis", ".gb-acct-nav__link[data-acct-goto='details'].is-current", True),
        ("css", MD + ".gb-acct-profile", "row-gap", "32px"),
        ("css", MD + ".gb-acct-cards", "row-gap", "24px"),
        ("text", MD + ".gb-acct-card__title", ["Email", "Your name", "Phone number"]),
        # 27081 writes two sentences; the second one was missing until Task 24.
        ("text", MD + ".gb-acct-card__note",
         ["You will receive a confirmation email where we will ask you to verify "
          "your new email address. All emails from us will be sent to your new address.",
          "Opt in to order updates via text message"]),
        # the board labels the phone field "Email*" -- copy-paste slip, SPEC 8
        ("text", MD + ".gb-acct-field__label",
         ["Email*", "First name*", "Last name*", "Phone number*"]),
        ("css", MD + ".gb-acct-field__input", "height", "44px"),
        ("css", MD + ".gb-acct-field__input", "border-radius", "8px"),
        ("css", MD + ".gb-acct-field__box", "height", "44px"),
        ("text", MD + ".gb-acct-field__prefix", ["AU"]),
        ("css", MD + ".gb-acct-field__prefix", "color", "rgb(77, 77, 77)"),
        ("css", MD + ".gb-acct-card__note", "font-size", "12px"),
        ("css", MD + ".gb-acct-card__note", "line-height", "18px"),
        ("css", MD + ".gb-acct-card__note", "color", "rgb(102, 102, 102)"),
        # decision AC: no desktop board, so the two name fields sit side by side
        # the way sign-up's 35059 does. One row of 70 proves it; 156 would mean
        # they stacked.
        ("css", MD + ".gb-acct-profile__row", "height", "70px"),
        ("text", MD + ".gb-acct-profile__note", ['You will receive an email confirmation to verify changes.']),
        ("css", MD + ".gb-acct-profile__note", "text-align", "center"),
        ("css", MD + ".gb-acct-profile__note", "font-size", "12px"),
        ("vis", MD + ".gb-acct-btn[data-acct-save]", True),
        # #e6e6e6 on #808080 is the board's Save. Reading green here would mean
        # acctForm never ran, so this doubles as the JS liveness check.
        ("css", MD + ".gb-acct-btn[data-acct-save]", "background-color", "rgb(230, 230, 230)"),
        ("css", MD + ".gb-acct-btn[data-acct-save]", "color", "rgb(128, 128, 128)"),
        ("css", MD + ".gb-acct-btn[data-acct-save]", "border-top-color", "rgb(230, 230, 230)"),
        ("nofit", MD + ".gb-acct-profile"),
    ],
    # The grey Save above only proves it starts asleep. Typing into one field
    # has to wake it, or the gate is simply dead.
    ("account.html", 1440, DETAILS_DIRTY): [
        ("css", MD + ".gb-acct-btn[data-acct-save]", "background-color", "rgb(0, 86, 53)"),
        ("css", MD + ".gb-acct-btn[data-acct-save]", "color", "rgb(255, 255, 255)"),
    ],
    ("account.html", 390, GOTO_DETAILS): [
        ("css", MD + ".gb-acct-intro__title", "font-size", "20px"),
        # the phone board stacks them: 70 + 16 + 70
        ("css", MD + ".gb-acct-profile__row", "height", "156px"),
        ("css", MD + ".gb-acct-card", "width", "350px"),
        ("nofit", MD + ".gb-acct-profile"),
    ],
    # -- Task 17: Change Password (2284:27151) --
    # The board dresses this page in the Order Card component, so .gb-acct-card
    # is built once and Task 20 reuses it. 350 = 348 + two 1px edges: the card's
    # strokesIncludedInLayout is true, so it is a real border.
    ("account.html", 1440, GOTO_PASSWORD): [
        ("shown", "[data-acct-view='password']", True),
        ("text", CP + ".gb-acct-intro__title", ["Change Password"]),
        ("css", CP + ".gb-acct-intro__title", "font-size", "24px"),
        ("vis", ".gb-acct-nav__link[data-acct-goto='password'].is-current", True),
        ("css", CP + ".gb-acct-card", "border-radius", "12px"),
        ("css", CP + ".gb-acct-card", "border-top-width", "1px"),
        ("css", CP + ".gb-acct-card", "border-top-color", "rgb(230, 230, 230)"),
        ("css", CP + ".gb-acct-card", "background-color", "rgb(255, 255, 255)"),
        ("css", CP + ".gb-acct-card__body", "padding-top", "20px"),
        ("css", CP + ".gb-acct-card__body", "padding-left", "20px"),
        ("css", CP + ".gb-acct-card__group", "row-gap", "16px"),
        ("css", CP + ".gb-acct-card__foot", "padding-top", "8px"),
        ("css", CP + ".gb-acct-card__foot", "padding-left", "16px"),
        ("css", CP + ".gb-acct-card__foot", "padding-bottom", "20px"),
        ("text", CP + ".gb-acct-card__title", ["Need to update your password?"]),
        ("css", CP + ".gb-acct-card__title", "font-size", "16px"),
        ("css", CP + ".gb-acct-card__title", "font-weight", "500"),
        ("css", CP + ".gb-acct-card__title", "color", "rgb(26, 26, 26)"),
        # The board's copy reads "instructions ro reset it" -- typo, see SPEC 8
        ("text", CP + ".gb-acct-card__text", ['Click the button below and we’ll send you an email with instructions to reset it.']),
        ("css", CP + ".gb-acct-card__text", "font-weight", "400"),
        ("css", CP + ".gb-acct-card__text", "color", "rgb(102, 102, 102)"),
        ("text", CP + ".gb-acct-btn", ["Change Password"]),
        ("css", CP + ".gb-acct-btn", "height", "44px"),
        ("css", CP + ".gb-acct-btn", "border-radius", "72px"),
        ("css", CP + ".gb-acct-page", "row-gap", "16px"),
        ("nofit", CP + ".gb-acct-card"),
    ],
    ("account.html", 390, GOTO_PASSWORD): [
        ("css", CP + ".gb-acct-intro__title", "font-size", "20px"),
        ("css", CP + ".gb-acct-card", "width", "350px"),
        ("css", CP + ".gb-acct-card__body", "padding-top", "20px"),
        ("css", CP + ".gb-acct-page", "row-gap", "24px"),
        ("nofit", CP + ".gb-acct-card"),
    ],
    # -- Task 19: Help (2284:27170) --
    # Seven accordion rows, the first one open. Every heading on the board reads
    # literally "Accordion Open" / "Accordion Closed" and the body reads "Text
    # here" -- placeholder, SPEC 8b, not copy to invent.
    ("account.html", 1440, GOTO_HELP): [
        ("shown", "[data-acct-view='help']", True),
        ("text", HP + ".gb-acct-intro__title", ["Help"]),
        ("css", HP + ".gb-acct-intro__title", "font-size", "24px"),
        ("vis", ".gb-acct-nav__link[data-acct-goto='help'].is-current", True),
        ("text", HP + ".gb-acct-card__title", ["Popular Questions"]),
        ("text", HP + ".gb-acct-faq__q",
         ["Accordion Open", "Accordion Closed", "Accordion Closed", "Accordion Closed",
          "Accordion Closed", "Accordion Closed", "Accordion Closed"]),
        # only the open row's answer renders, so this doubles as "exactly one open"
        ("text", HP + ".gb-acct-faq__a", ["Text here"]),
        ("css", HP + ".gb-acct-faq", "row-gap", "16px"),
        # 45 = 1px rule + 20 + 24; the first row has no rule above it
        ("css", HP + ".gb-acct-faq__item + .gb-acct-faq__item", "border-top-width", "1px"),
        ("css", HP + ".gb-acct-faq__item + .gb-acct-faq__item", "border-top-color", "rgb(1, 19, 7)"),
        ("css", HP + ".gb-acct-faq__item + .gb-acct-faq__item", "padding-top", "20px"),
        ("css", HP + ".gb-acct-faq__item + .gb-acct-faq__item", "height", "45px"),
        ("css", HP + ".gb-acct-faq__q", "font-size", "16px"),
        ("css", HP + ".gb-acct-faq__q", "color", "rgb(1, 19, 7)"),
        ("css", HP + ".gb-acct-faq__a", "color", "rgb(77, 77, 77)"),
        # the sand card closes this page and Order Detail alike -- r8, not the
        # white cards' 12
        ("css", HP + ".gb-acct-help", "border-radius", "8px"),
        ("css", HP + ".gb-acct-help", "background-color", "rgb(245, 241, 233)"),
        ("css", HP + ".gb-acct-help", "padding-top", "20px"),
        ("css", HP + ".gb-acct-help", "row-gap", "24px"),
        ("text", HP + ".gb-acct-help__title", ["Need help with your order?"]),
        ("css", HP + ".gb-acct-help__title", "font-size", "14px"),
        ("css", HP + ".gb-acct-help__title", "color", "rgb(26, 26, 26)"),
        ("css", HP + ".gb-acct-help__lines", "row-gap", "8px"),
        ("text", HP + ".gb-acct-help__link", ["visit FAQ page"]),
        ("css", HP + ".gb-acct-help__link", "color", "rgb(3, 116, 165)"),
        ("css", HP + ".gb-acct-stack", "row-gap", "32px"),
        ("nofit", HP + ".gb-acct-card"),
    ],
    ("account.html", 390, GOTO_HELP): [
        ("css", HP + ".gb-acct-intro__title", "font-size", "20px"),
        ("css", HP + ".gb-acct-card", "width", "350px"),
        ("nofit", HP + ".gb-acct-help"),
    ],
    # A single-open accordion that never closes the previous row would still
    # pass every check above, so the swap is driven once.
    ("account.html", 1440, HELP_OPEN2): [
        ("text", HP + ".gb-acct-faq__a", ["Text here"]),
        ("vis", HP + ".gb-acct-faq__item:nth-child(2).is-open", True),
        ("absent", HP + ".gb-acct-faq__item:nth-child(1).is-open"),
    ],
    # Order Detail has no nav row of its own -- Task 20 gives it one on the
    # order card's View Order button. Until then the hash is the only way in.
    # -- Task 21: Order Detail (2284:27304) --
    # One tall white card: header meta, then four rules separating Order Items /
    # Order Summary / Shipping Information / Payment Information, then Download
    # Invoice in the foot. The sand help card below it is Task 19's.
    ("account.html", 1440, GOTO_ORDER): [
        ("shown", "[data-acct-view='order']", True),
        ("text", OD + ".gb-acct-intro__title", ["Order #12345678"]),
        ("css", OD + ".gb-acct-intro__title", "font-size", "24px"),
        ("text", OD + ".gb-acct-hist__label", ["Order Date:", "Status:", "Total:"]),
        ("text", OD + ".gb-acct-hist__value", ["Aug 13, 2026", "Preparing", "$121.50"]),
        # section headings are w400 #011307 -- NOT .gb-acct-card__title's w500 #1a1a1a
        ("text", OD + ".gb-acct-sect",
         ["Order Items:", "Order Summary", "Shipping Information", "Payment Information"]),
        ("css", OD + ".gb-acct-sect", "font-size", "16px"),
        ("css", OD + ".gb-acct-sect", "font-weight", "400"),
        ("css", OD + ".gb-acct-sect", "color", "rgb(1, 19, 7)"),
        ("css", OD + ".gb-acct-rule", "height", "1px"),
        ("css", OD + ".gb-acct-rule", "background-color", "rgb(230, 230, 230)"),
        ("text", OD + ".gb-acct-item__name", ['Superfood Greens Gummies'] * 4),
        ("text", OD + ".gb-acct-item__flavour", ["Flavour"] * 4),
        ("text", OD + ".gb-acct-item__qty", ["Quantity: 1"] * 4),
        ("text", OD + ".gb-acct-item__tag",
         ["Subscription", "One-off purchase", "Subscription", "Subscription"]),
        ("text", OD + ".gb-acct-item__price", ["$134.50"] * 4),
        # the board strikes the LOWER of the two prices -- SPEC 8
        ("text", OD + ".gb-acct-item__was", ["$133.50"] * 4),
        ("css", OD + ".gb-acct-item__was", "text-decoration-line", "line-through"),
        ("css", OD + ".gb-acct-item__name", "color", "rgb(16, 24, 40)"),
        ("css", OD + ".gb-acct-item__thumb", "width", "40px"),
        ("css", OD + ".gb-acct-item__thumb", "border-radius", "2.86px"),
        ("css", OD + ".gb-acct-items", "row-gap", "24px"),
        ("css", OD + ".gb-acct-item__main", "column-gap", "12px"),
        ("text", OD + ".gb-acct-recap__label",
         ["Subtotal", "Promo code discount", "Shipping"]),
        ("text", OD + ".gb-acct-recap__value", ["$00.00", "-$00.00", "$00.00"]),
        ("text", OD + ".gb-acct-recap__total span", ["Total", "$00.00"]),
        ("css", OD + ".gb-acct-recap__total", "font-size", "16px"),
        ("css", OD + ".gb-acct-recap__total", "color", "rgb(1, 19, 7)"),
        ("css", OD + ".gb-acct-recap__rows", "row-gap", "8px"),
        ("text", OD + ".gb-acct-info__label",
         ["Shipping Address", "Shipping Method", "Payment Method", "Billing Address"]),
        ("text", OD + ".gb-acct-info__value",
         ['Susanna Rose, 12 Charnwood Rd, Unit 10, St Kilda VIC 3182, Australia', "Shipping & Standard: $12.98", 'Susanna Rose, 12 Charnwood Rd, Unit 10, St Kilda VIC 3182, Australia']),
        ("css", OD + ".gb-acct-info__label", "color", "rgb(26, 26, 26)"),
        ("css", OD + ".gb-acct-info__value", "color", "rgb(102, 102, 102)"),
        ("css", OD + ".gb-acct-info", "row-gap", "8px"),
        ("text", OD + ".gb-acct-info__card span", ["\u2022\u2022\u2022\u2022", "5467"]),
        ("css", OD + ".gb-acct-info__logo", "width", "23px"),
        ("css", OD + ".gb-acct-info__logo", "height", "16px"),
        # decision I: note 27444 says "Only do if very very very cheap" -- built
        # as drawn, flagged for the design side rather than silently dropped
        ("text", OD + ".gb-acct-btn", ["Download Invoice"]),
        ("vis", OD + ".gb-acct-help", True),
        ("nofit", OD + ".gb-acct-stack"),
    ],
    ("account.html", 390, GOTO_ORDER): [
        ("css", OD + ".gb-acct-intro__title", "font-size", "20px"),
        ("css", OD + ".gb-acct-card", "width", "350px"),
        ("nofit", OD + ".gb-acct-stack"),
        ("nofit", OD + ".gb-acct-items"),
    ],

    # -- Task 14: Log in, desktop (2284:35137) --
    # These two pages carry the SITE header, not the account one: the board's
    # instance is Header Navigation Desktop/Closed, the same component the 11
    # MVP pages use (Menu / logo / Shop now / two icons). The account header is
    # a different component and its burger opens the account menu, which a
    # logged-out visitor has no use for.
    ("account-login.html", 1440, None): [
        # anchor first -- every absence below is only meaningful once this exists
        ("vis", ".gb-acct-auth", True),
        ("absent", ".gb-acct-nav"),
        ("absent", ".gb-acct-header"),
        ("vis", ".gb-header__cta", True),
        ("text", ".gb-header__cta", ["Shop now"]),
        ("css", ".gb-header__cta", "background-color", "rgb(0, 86, 53)"),
        # 2284:35137 fill
        ("css", ".gb-acct-auth", "background-color", "rgb(250, 249, 248)"),
        # 35188 / 35189
        ("text", ".gb-acct-auth__title", ["Log in"]),
        ("css", ".gb-acct-auth__title", "font-size", "32px"),
        ("css", ".gb-acct-auth__title", "line-height", "40px"),
        ("css", ".gb-acct-auth__title", "letter-spacing", "-0.32px"),
        ("css", ".gb-acct-auth__title", "font-weight", "800"),
        ("css", ".gb-acct-auth__title", "color", "rgb(27, 28, 30)"),
        ("text", ".gb-acct-auth__sub", ["Log in to manage your subscription"]),
        ("css", ".gb-acct-auth__sub", "font-size", "18px"),
        ("css", ".gb-acct-auth__sub", "line-height", "28px"),
        ("css", ".gb-acct-auth__sub", "letter-spacing", "-0.36px"),
        ("css", ".gb-acct-auth__sub", "color", "rgb(101, 101, 101)"),
        # 35179 pads 64/96 and puts 48 between the heading and the container
        ("css", ".gb-acct-auth", "padding-top", "64px"),
        ("css", ".gb-acct-auth", "padding-bottom", "96px"),
        ("css", ".gb-acct-auth", "row-gap", "48px"),
        # 35190: 1280 wide, 32 each side, 32 between the form, the alt line and
        # the note
        ("css", ".gb-acct-auth__inner", "max-width", "1280px"),
        ("css", ".gb-acct-auth__inner", "padding-left", "32px"),
        ("css", ".gb-acct-auth__inner", "row-gap", "32px"),
        ("css", ".gb-acct-auth__form", "width", "480px"),
        ("css", ".gb-acct-auth__form", "row-gap", "32px"),
        ("css", ".gb-acct-auth__fields", "row-gap", "24px"),
        # 196:17634, the same input component the modals already use
        ("text", ".gb-acct-auth__form .gb-acct-field__label", ["Email", "Password"]),
        ("css", ".gb-acct-auth__form .gb-acct-field__input", "height", "44px"),
        ("css", ".gb-acct-auth__form .gb-acct-field__input", "border-radius", "8px"),
        ("css", ".gb-acct-auth__form .gb-acct-field__input",
         "border-top-color", "rgb(204, 204, 204)"),
        ("css", ".gb-acct-auth__form .gb-acct-field__input", "font-size", "16px"),
        # 35202: underlined, and it is a link here (35129 on sign-up is not)
        ("text", ".gb-acct-auth__aside", ["Forgot your password?"]),
        ("css", ".gb-acct-auth__aside", "font-size", "16px"),
        ("css", ".gb-acct-auth__aside", "line-height", "24px"),
        ("css", ".gb-acct-auth__aside", "color", "rgb(128, 128, 128)"),
        ("css", ".gb-acct-auth__aside", "text-decoration-line", "underline"),
        # 35203
        ("text", ".gb-acct-auth__submit", ["Log in"]),
        ("css", ".gb-acct-auth__submit", "height", "52px"),
        ("css", ".gb-acct-auth__submit", "background-color", "rgb(0, 86, 53)"),
        ("css", ".gb-acct-auth__submit", "color", "rgb(255, 255, 255)"),
        ("css", ".gb-acct-auth__submit", "font-size", "16px"),
        ("css", ".gb-acct-auth__submit", "line-height", "28px"),
        ("css", ".gb-acct-auth__submit", "letter-spacing", "0.48px"),
        # 35204: only the trailing run is green and underlined
        ("text", ".gb-acct-auth__alt", [u"Don\u2019t have an account? Sign up"]),
        ("css", ".gb-acct-auth__alt", "font-size", "16px"),
        ("css", ".gb-acct-auth__alt", "color", "rgb(102, 102, 102)"),
        ("css", ".gb-acct-auth__alt a", "color", "rgb(0, 86, 53)"),
        ("css", ".gb-acct-auth__alt a", "text-decoration-line", "underline"),
        # 35205
        ("css", ".gb-acct-auth__note", "background-color", "rgb(245, 241, 233)"),
        ("css", ".gb-acct-auth__note", "border-radius", "8px"),
        ("css", ".gb-acct-auth__note", "padding-top", "24px"),
        ("css", ".gb-acct-auth__note", "padding-left", "24px"),
        ("css", ".gb-acct-auth__note", "row-gap", "4px"),
        ("text", ".gb-acct-auth__note-title",
         [u"Ordered before but haven\u2019t set up an account?"]),
        ("css", ".gb-acct-auth__note-title", "font-size", "16px"),
        ("css", ".gb-acct-auth__note-title", "font-weight", "500"),
        ("css", ".gb-acct-auth__note-title", "color", "rgb(27, 28, 30)"),
        ("text", ".gb-acct-auth__note-text",
         [u"No worries\u2014just sign up with the same email and we\u2019ll link "
          u"your order history automatically."]),
        ("css", ".gb-acct-auth__note-text", "font-size", "16px"),
        ("css", ".gb-acct-auth__note-text", "color", "rgb(101, 101, 101)"),
        ("nofit", ".gb-acct-auth"),
    ],
    # -- Task 14: Log in, phone (2284:34993) --
    ("account-login.html", 390, None): [
        ("vis", ".gb-acct-auth", True),
        ("absent", ".gb-acct-nav"),
        # 35002 / 35004: smaller, and the ink is $c-ink here, not $c-gray-850
        ("css", ".gb-acct-auth__title", "font-size", "24px"),
        ("css", ".gb-acct-auth__title", "line-height", "30px"),
        ("css", ".gb-acct-auth__title", "letter-spacing", "-0.24px"),
        ("css", ".gb-acct-auth__title", "color", "rgb(1, 19, 7)"),
        ("css", ".gb-acct-auth__sub", "font-size", "16px"),
        ("css", ".gb-acct-auth__sub", "line-height", "24px"),
        ("css", ".gb-acct-auth__sub", "letter-spacing", "-0.32px"),
        ("css", ".gb-acct-auth__sub", "color", "rgb(102, 102, 102)"),
        # 34999: 64 top and bottom, 20 each side
        ("css", ".gb-acct-auth", "padding-top", "64px"),
        ("css", ".gb-acct-auth", "padding-bottom", "64px"),
        ("css", ".gb-acct-auth__inner", "padding-left", "20px"),
        # 35005: the phone board spaces the button, the alt line and the note
        # 48 apart, not the desktop's 32
        ("css", ".gb-acct-auth__inner", "row-gap", "48px"),
        ("css", ".gb-acct-auth__form", "row-gap", "32px"),
        ("css", ".gb-acct-auth__aside", "font-size", "14px"),
        ("css", ".gb-acct-auth__aside", "line-height", "20px"),
        ("css", ".gb-acct-auth__aside", "color", "rgb(128, 128, 128)"),
        ("css", ".gb-acct-auth__alt", "font-size", "14px"),
        ("css", ".gb-acct-auth__alt", "line-height", "20px"),
        # 35016 stays 52 tall on the phone board, unlike .gb-btn--lg which the
        # site drops to 44 below 768
        ("css", ".gb-acct-auth__submit", "height", "52px"),
        # 35018
        ("css", ".gb-acct-auth__note", "padding-top", "16px"),
        ("css", ".gb-acct-auth__note", "padding-left", "20px"),
        ("css", ".gb-acct-auth__note-title", "font-size", "14px"),
        ("css", ".gb-acct-auth__note-title", "font-weight", "400"),
        ("css", ".gb-acct-auth__note-title", "color", "rgb(1, 19, 7)"),
        ("css", ".gb-acct-auth__note-text", "font-size", "14px"),
        ("css", ".gb-acct-auth__note-text", "color", "rgb(102, 102, 102)"),
        ("nofit", ".gb-acct-auth"),
    ],
    # -- Task 14: Sign up, desktop (2284:35059) --
    # The heading on this one board is Lexend 36/44; every other heading in the
    # account set, this page's own phone board included, is PP Palma. Treated as
    # a board slip and built to match Log in -- logged in SPEC section 8.
    ("account-signup.html", 1440, None): [
        ("vis", ".gb-acct-auth", True),
        ("absent", ".gb-acct-nav"),
        ("absent", ".gb-acct-header"),
        ("vis", ".gb-header__cta", True),
        ("css", ".gb-header__cta", "background-color", "rgb(0, 86, 53)"),
        ("text", ".gb-acct-auth__title", ["Sign up"]),
        ("css", ".gb-acct-auth__title", "font-size", "32px"),
        ("css", ".gb-acct-auth__title", "font-weight", "800"),
        ("text", ".gb-acct-auth__sub",
         ["Sign up to edit, skip or manage your subscription"]),
        ("css", ".gb-acct-auth__sub", "font-size", "18px"),
        # 35116: two 224 columns, 32 apart
        ("text", ".gb-acct-auth__form .gb-acct-field__label",
         ["First name*", "Last name*", "Email*", "Password"]),
        ("css", ".gb-acct-auth__row", "column-gap", "32px"),
        ("css", ".gb-acct-auth__row .gb-acct-field", "width", "224px"),
        # 35129: same slot as Log in's Forgot line but static text, no underline
        ("text", ".gb-acct-auth__aside", ["Must be at least 8 characters"]),
        ("css", ".gb-acct-auth__aside", "text-decoration-line", "none"),
        ("text", ".gb-acct-auth__submit", ["Sign up"]),
        ("css", ".gb-acct-auth__submit", "height", "52px"),
        ("text", ".gb-acct-auth__alt", ["Already have an account? Log in"]),
        ("css", ".gb-acct-auth__alt a", "color", "rgb(0, 86, 53)"),
        ("nofit", ".gb-acct-auth"),
    ],
    # -- Task 14: Sign up, phone (2284:35023) --
    ("account-signup.html", 390, None): [
        ("vis", ".gb-acct-auth", True),
        ("absent", ".gb-acct-nav"),
        ("css", ".gb-acct-auth__title", "font-size", "24px"),
        # 35038-35045: the two name fields stack, they do not stay side by side
        ("css", ".gb-acct-auth__row .gb-acct-field", "width", "350px"),
        ("css", ".gb-acct-auth__row", "row-gap", "24px"),
        ("text", ".gb-acct-auth__aside", ["Must be at least 8 characters"]),
        ("css", ".gb-acct-auth__aside", "font-size", "14px"),
        ("nofit", ".gb-acct-auth"),
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
            label = "%s@%d%s" % (page_name, w, " [%s]" % action if action else "")
            # A page that does not exist has to read as red. file:// raises
            # ERR_FILE_NOT_FOUND, which would abort the whole run instead.
            if not (ROOT / page_name).exists():
                print("RED  %-52s page does not exist" % label)
                red += len(checks); continue
            pg = b.new_page(viewport={"width": w, "height": 900})
            pg.goto((ROOT / page_name).as_uri())
            pg.wait_for_timeout(400)
            if action:
                if action in (GOTO_DETAIL, DETAIL_PAUSED, DETAIL_CANCELLED,
                              DETAIL_DISCOUNT, DETAIL_LONGCODE):
                    # Reached the way a user reaches it: open the list, then the
                    # first card's CTA. Driving it through location.hash would
                    # skip the wiring Task 5 put on that button.
                    nav = ".gb-acct-nav" if w > 767 else ".gb-acct-list"
                    try:
                        pg.click(nav + " [data-acct-goto='subscriptions']", timeout=2000)
                        pg.wait_for_timeout(450)
                        pg.click("[data-acct-view='subscriptions'] "
                                 ".gb-acct-sub__cta[data-acct-goto='detail']", timeout=2000)
                        pg.wait_for_timeout(450)
                    except Exception as e:
                        print("RED  %-52s cannot reach detail: %s" % (label, type(e).__name__))
                        red += len(checks); pg.close(); continue
                    # No board authors two states at once, so the judge sets the
                    # attribute the way a template would.
                    attr = {DETAIL_PAUSED: ("data-acct-sub-state", "paused"),
                            DETAIL_CANCELLED: ("data-acct-sub-state", "cancelled"),
                            DETAIL_DISCOUNT: ("data-acct-discount", "applied"),
                            DETAIL_LONGCODE: ("data-acct-discount", "applied")}.get(action)
                    if attr:
                        n = pg.evaluate(
                            "a=>{const e=document.querySelector('.gb-acct-detail');"
                            "if(!e)return 0;e.setAttribute(a[0],a[1]);return 1}", list(attr))
                        if not n:
                            print("RED  %-52s no .gb-acct-detail to set" % label)
                            red += len(checks); pg.close(); continue
                        pg.wait_for_timeout(450)
                    if action == DETAIL_LONGCODE:
                        # 2284:28878 verbatim -- 51 characters with no break
                        # opportunity. Without it this group would measure the
                        # 12-character placeholder, which fits 118 either way.
                        n = pg.evaluate(
                            "t=>{const e=document.querySelector('.gb-acct-summary__code');"
                            "if(!e)return 0;e.textContent=t;return 1}", LONG_CODE)
                        if not n:
                            print("RED  %-52s no .gb-acct-summary__code to fill" % label)
                            red += len(checks); pg.close(); continue
                        pg.wait_for_timeout(120)
                elif action == HELP_OPEN2:
                    nav = ".gb-acct-nav" if w > 767 else ".gb-acct-list"
                    try:
                        pg.click(nav + " [data-acct-goto='help']", timeout=2000)
                        pg.wait_for_timeout(450)
                        pg.click(HP + ".gb-acct-faq__item:nth-child(2) "
                                 ".gb-acct-faq__q", timeout=2000)
                        pg.wait_for_timeout(400)
                    except Exception as e:
                        print("RED  %-52s cannot open row 2: %s" % (label, type(e).__name__))
                        red += len(checks); pg.close(); continue
                elif action == DETAILS_DIRTY:
                    nav = ".gb-acct-nav" if w > 767 else ".gb-acct-list"
                    try:
                        pg.click(nav + " [data-acct-goto='details']", timeout=2000)
                        pg.wait_for_timeout(450)
                        pg.fill("#acct-md-first", "Changed")
                        pg.wait_for_timeout(400)
                    except Exception as e:
                        print("RED  %-52s cannot dirty the form: %s" % (label, type(e).__name__))
                        red += len(checks); pg.close(); continue
                elif action == GOTO_ORDER:
                    pg.evaluate("()=>{location.hash='#order'}")
                    pg.wait_for_timeout(450)
                elif action in (STATE_PREPARING, STATE_RENEWAL):
                    state = action.split("-", 1)[1]
                    n = pg.evaluate(
                        "s=>{const e=document.querySelector('[data-acct-order-state]');"
                        "if(!e)return 0;e.setAttribute('data-acct-order-state',s);return 1}",
                        state)
                    if not n:
                        print("RED  %-52s no [data-acct-order-state] to set" % label)
                        red += len(checks); pg.close(); continue
                    # long enough for $t-base/$t-slow to land: reading mid-transition
                    # returns an interpolated colour that matches nothing
                    pg.wait_for_timeout(450)
                else:
                    nav = ".gb-acct-nav" if w > 767 else ".gb-acct-list"
                    trigger = {
                        OPEN_MENU: "[data-acct-menu-toggle]",
                        GOTO_SUBS: nav + " [data-acct-goto='subscriptions']",
                        GOTO_ORDERS: nav + " [data-acct-goto='orders']",
                        GOTO_DETAILS: nav + " [data-acct-goto='details']",
                        GOTO_PASSWORD: nav + " [data-acct-goto='password']",
                        GOTO_HELP: nav + " [data-acct-goto='help']",
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
                    # Only what is actually rendered. innerText falls back to
                    # textContent inside a display:none subtree, so from Task 7
                    # on -- where every state ships all its variants and hides
                    # the rest -- an unfiltered read returns the hidden ones too.
                    got = pg.eval_on_selector_all(
                        sel, "els=>els.filter(e=>e.checkVisibility())"
                             ".map(e=>e.innerText.trim())")
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
                elif kind == "nofit":
                    got = pg.evaluate(
                        "s=>{const e=document.querySelector(s);if(!e)return null;"
                        "const d=document.documentElement;"
                        "return [e.scrollWidth-e.clientWidth, d.scrollWidth-d.clientWidth]}", sel)
                    tag = "%s fits(%s)" % (label, sel)
                    if got is None:
                        print("RED  %-52s element not found" % tag); red += 1
                    elif got[0] <= 1 and got[1] <= 1:
                        ok += 1
                    else:
                        print("RED  %-52s overflow self=%s page=%s" % (tag, got[0], got[1])); red += 1
                elif kind == "rect":
                    edge, want = chk[2], chk[3]
                    got = pg.evaluate(
                        "([s,e])=>{const el=document.querySelector(s);if(!el)return null;"
                        "const r=el.getBoundingClientRect();"
                        "return e==='right'?innerWidth-r.right:e==='left'?r.left:r.width}",
                        [sel, edge])
                    tag = "%s rect(%s).%s" % (label, sel, edge)
                    if got is None:
                        print("RED  %-52s element not found" % tag); red += 1
                    elif abs(got - want) <= 1:
                        ok += 1
                    else:
                        print("RED  %-52s want %s, got %s" % (tag, want, round(got, 1))); red += 1
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
