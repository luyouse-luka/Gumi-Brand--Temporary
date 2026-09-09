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
STATE_PREPARING = "state-preparing"
STATE_RENEWAL = "state-renewal"

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

        ("text", ".gb-acct-intro__title", ["My Subscriptions"]),
        ("text", ".gb-acct-sub__title", ["My Subscription"] * 3),
        ("text", ".gb-acct-pill", ["ACTIVE", "PAUSED", "CANCELLED"]),
        ("text", ".gb-acct-sub__more", ["+4 More Products"] * 3),
        # note 28321: paused shows the date it is paused until. Only the phone
        # boards (28315 / 34056) carry it; the desktop board left the sample
        # date alone (SPEC 8).
        ("text", "[data-acct-sub-state='paused'] .gb-acct-sub__meta-value",
         ["17 Aug 2026", "123 Express Ln, VIC 3121"]),
        ("text", "[data-acct-sub-state='active'] .gb-acct-sub__meta-value",
         ["19 Jul 2026", "123 Express Ln, VIC 3121"]),
        ("text", ".gb-acct-sub__cta",
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

        # -- Task 4: Overview, phone (2284:27604) --
        # The greeting is bare here (2284:27610), not the desktop's lime card
        ("css", ".gb-acct-hello", "background-color", "rgba(0, 0, 0, 0)"),
        ("css", ".gb-acct-hello", "padding-left", "0px"),
        ("css", ".gb-acct__inner", "padding-top", "8px"),
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
                if action in (STATE_PREPARING, STATE_RENEWAL):
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
                    trigger = {
                        OPEN_MENU: "[data-acct-menu-toggle]",
                        GOTO_SUBS: ("%s [data-acct-goto='subscriptions']"
                                    % (".gb-acct-nav" if w > 767 else ".gb-acct-list")),
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
