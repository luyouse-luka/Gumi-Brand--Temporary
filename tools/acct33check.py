#!/usr/bin/env python3
"""Task 33 -- the burger's click route, the header's open colour and the two
header icons' opacity hover are all gone, and the burger itself is now the
site header's cart icon.

Both are negative assertions, so every one of them is paired with an anchor:
the burger and the panel both still have to be in the page, or "nothing opens"
would read green on a header that no longer exists.

What survives on purpose is the account icon's hover panel (Task 29 req 4).
⚠ The consequence this pins down: a touch device has no route to that panel.
Every link in it is still reachable from .gb-acct-nav / .gb-acct-list, so this
is a lost shortcut, not lost navigation. Requested, not a bug -- HANDOFF 5c.
"""
import sys, pathlib, re
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
BAR_REST = "rgb(231, 248, 208)"          # $c-lime-150, the only colour left

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
        print("ok   %-58s %s" % (label, got)); ok += 1
    else:
        print("RED  %-58s got %r want %r" % (label, got, want)); red += 1


def source_checks():
    css = (ROOT / "assets/account.css").read_text()
    js = (ROOT / "assets/account.js").read_text()
    html = (ROOT / "account.html").read_text()
    # anchor first: the selector family has to be there for its absence to mean
    # anything -- a renamed header would make all three of these trivially true
    check("anchor: header rules exist", bool(re.search(r"^\.gb-acct-header \{", css, re.M)), True)
    check("no .gb-acct-header.is-open rule", ".gb-acct-header.is-open" in css, False)
    check("no header background transition",
          bool(re.search(r"\.gb-acct-header \{[^}]*transition", css)), False)
    check("anchor: the menu markup is still authored", 'class="gb-acct-menu"' in html, True)
    check("no data-acct-menu-toggle in the page", "data-acct-menu-toggle" in html, False)
    cart = re.search(r"<a class=\"gb-acct-header__link gb-acct-header__cart\".*?>",
                     html, re.S)
    check("anchor: the cart tag parses", bool(cart), True)
    check("no aria-* toggle state on it",
          bool(cart) and ("aria-controls" in cart.group() or
                          "aria-expanded" in cart.group()), False)
    check("the burger class is gone for good", "gb-acct-header__burger" in html, False)
    # the icon is the site header's, not a second drawing of the same thing
    site = re.search(r"gb-header__icon\" href=\"#\" data-modal=\"gb-cart\"[^>]*>(<svg.*?</svg>)",
                     (ROOT / "index.html").read_text(), re.S)
    mine = re.search(r"gb-acct-header__cart\"[^>]*>(<svg.*?</svg>)", html, re.S)
    check("anchor: both cart icons found", bool(site) and bool(mine), True)
    check("the account cart icon is the site header's, glyph for glyph",
          bool(site) and bool(mine) and site.group(1) == mine.group(1), True)
    # ⚠ main.js owns [data-modal]; account.js owns the lock. One would unlock the
    # other, and there is no cart drawer on this page anyway.
    check("it does not wire itself to main.js's modal",
          bool(cart) and "data-modal" in cart.group(), False)
    check("no menu toggle left in the script", "data-acct-menu-toggle" in js, False)
    check("acctNav module gone", "acctNav" in js, False)
    # req 2: the icons' own hover. Anchor on the block, or a renamed class would
    # make "no hover in it" true by finding nothing.
    scss = (ROOT / "assets/account.scss").read_text()
    blk = re.search(r"\n\.gb-acct-header__link \{(.*?)\n\}\n", scss, re.S)
    check("anchor: the .gb-acct-header__link block exists", bool(blk), True)
    check("no hover left in it", bool(blk) and "@include hover" in blk.group(1), False)
    check("its dead opacity transition went too",
          bool(blk) and "transition" in blk.group(1), False)


def run(b, w):
    tag = "@%d" % w
    errs = []
    pg = b.new_page(viewport={"width": w, "height": 900})
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto((ROOT / "account.html").as_uri())
    pg.wait_for_timeout(400)

    # --- anchors ---
    check("anchor: cart icon present" + tag, pg.locator(".gb-acct-header__cart").count(), 1)
    check("anchor: panel present" + tag, pg.locator(".gb-acct-menu").count(), 1)
    check("cart is an inert link" + tag,
          pg.eval_on_selector(".gb-acct-header__cart",
                              "e=>[e.tagName,e.getAttribute('aria-label'),"
                              "e.getAttribute('aria-expanded'),e.getAttribute('aria-controls')]"),
          ["A", "Cart", None, None])

    bar = "e=>getComputedStyle(e).backgroundColor"
    vis = "e=>getComputedStyle(e).visibility"
    check("bar colour at rest" + tag,
          pg.eval_on_selector(".gb-acct-header", bar), BAR_REST)
    check("panel hidden at rest" + tag, pg.eval_on_selector(".gb-acct-menu", vis), "hidden")

    # --- the requirement: clicking the burger does nothing ---
    pg.click(".gb-acct-header__cart")
    pg.wait_for_timeout(500)
    check("click leaves the panel hidden" + tag,
          pg.eval_on_selector(".gb-acct-menu", vis), "hidden")
    check("click leaves [hidden] on the panel" + tag,
          pg.eval_on_selector(".gb-acct-menu", "e=>e.hasAttribute('hidden')"), True)
    check("click does not tint the bar" + tag,
          pg.eval_on_selector(".gb-acct-header", bar), BAR_REST)
    check("click adds no state class" + tag,
          pg.eval_on_selector(".gb-acct-header", "e=>e.className"), "gb-acct-header")
    # the pointer is sitting on the burger right now, which is the whole test
    check("the cart icon does not fade under the pointer" + tag,
          pg.eval_on_selector(".gb-acct-header__cart", "e=>getComputedStyle(e).opacity"), "1")
    # Escape used to close the menu; with no menu state there is nothing to bind
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(200)
    check("Escape changes nothing" + tag,
          pg.eval_on_selector(".gb-acct-menu", vis), "hidden")

    # --- what Task 29 built stays: the icon's hover panel ---
    pg.hover(".gb-acct-header__link--account")
    pg.wait_for_timeout(500)
    check("hovering the icon still drops the panel" + tag,
          pg.eval_on_selector(".gb-acct-menu", vis), "visible")
    check("and the bar keeps its one colour" + tag,
          pg.eval_on_selector(".gb-acct-header", bar), BAR_REST)
    check("the account icon does not fade either" + tag,
          pg.eval_on_selector(".gb-acct-header__link--account",
                              "e=>getComputedStyle(e).opacity"), "1")
    # what still answers the pointer, so the icon is not left with no feedback
    check("its lime rule still comes up" + tag,
          pg.eval_on_selector(".gb-acct-header__link--account",
                              "e=>getComputedStyle(e,'::after').opacity"), "1")

    check("no script errors" + tag, errs, [])
    check("acctNav no longer exported" + tag,
          pg.evaluate("()=>'acctNav' in (window.gumiAcct||{})"), False)
    pg.close()


def touch_run(b):
    """Documents the cost: with no hover, the panel has no route at all."""
    ctx = b.new_context(viewport={"width": 390, "height": 844},
                        has_touch=True, is_mobile=True)
    pg = ctx.new_page()
    pg.goto((ROOT / "account.html").as_uri())
    pg.wait_for_timeout(400)
    check("touch context really reports no hover",
          pg.evaluate("()=>matchMedia('(hover: hover)').matches"), False)
    pg.tap(".gb-acct-header__cart")
    pg.wait_for_timeout(500)
    check("tapping the cart icon opens nothing",
          pg.eval_on_selector(".gb-acct-menu", "e=>getComputedStyle(e).display"), "none")
    ctx.close()


def main():
    source_checks()
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=str(_chrome()))
        for w in (390, 1440):
            run(b, w)
        touch_run(b)
        b.close()
    print("\n%d ok / %d red" % (ok, red))
    sys.exit(1 if red else 0)


main()
