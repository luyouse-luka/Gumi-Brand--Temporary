#!/usr/bin/env python3
"""Nine views live in one DOM; exactly one may be showing at any moment.

Everything else in tools/ checks a view once it is open. This checks the router
itself: that each hash lands on its own view, that the other eight are hidden,
that an unknown hash falls back rather than showing nothing, and that the three
nav surfaces agree on which sections are reachable.

⚠ A view is asserted by [hidden], not by size: until a view has content it
measures 0 tall, and a size test cannot tell "switched off" from "empty".
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

VIEWS = ["overview", "subscriptions", "detail", "orders", "order",
         "details", "password", "referral", "help"]

# Order History / My Details / Change Password / Help became reachable with
# decision C. Refer a Friend joined them on 2026-09-15 (Task 29), built after
# funkyfood's module -- it still has no board of its own. Contact Preferences
# has none either and stays dead.
NAV_LIVE = ["overview", "subscriptions", "orders", "details", "password",
            "referral", "help"]
NAV_DEAD = ["Contact Preferences"]
LIST_DEAD = []

SHOWN = ("()=>Array.from(document.querySelectorAll('[data-acct-view]'))"
         ".filter(e=>!e.hidden).map(e=>e.getAttribute('data-acct-view'))")


def main():
    ok = red = 0
    def check(cond, msg):
        nonlocal ok, red
        if cond: ok += 1
        else:
            print("RED  " + msg); red += 1

    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=str(_chrome()))
        for w in (1440, 390):
            pg = b.new_page(viewport={"width": w, "height": 900})
            pg.goto((ROOT / "account.html").as_uri())
            pg.wait_for_timeout(400)

            present = pg.evaluate("()=>Array.from(document.querySelectorAll('[data-acct-view]'))"
                                  ".map(e=>e.getAttribute('data-acct-view'))")
            check(sorted(present) == sorted(VIEWS),
                  "@%d views in DOM: want %s, got %s" % (w, sorted(VIEWS), sorted(present)))

            for name in VIEWS:
                pg.evaluate("n=>{location.hash='#'+n}", name)
                # ⚠ Task 40: the outgoing view is held on screen for one exit
                # animation ($t-view, 500ms). Reading before it lands returns
                # two views and the assertion below is still the right one.
                pg.wait_for_timeout(700)
                shown = pg.evaluate(SHOWN)
                check(shown == [name], "@%d #%s shows %s" % (w, name, shown))

            # an unknown hash must land somewhere, not nowhere
            pg.evaluate("()=>{location.hash='#not-a-view'}")
            pg.wait_for_timeout(700)
            check(pg.evaluate(SHOWN) == ["overview"],
                  "@%d unknown hash did not fall back to overview" % w)

            surface = ".gb-acct-nav" if w > 767 else ".gb-acct-list"
            live = pg.evaluate("s=>Array.from(document.querySelectorAll(s+' [data-acct-goto]'))"
                               ".map(e=>e.getAttribute('data-acct-goto'))", surface)
            want = NAV_LIVE if w > 767 else [v for v in NAV_LIVE if v != "overview"]
            check(live == want, "@%d %s reaches %s, want %s" % (w, surface, live, want))

            dead = pg.evaluate("s=>Array.from(document.querySelectorAll(s+' [aria-disabled=\"true\"]'))"
                               ".map(e=>e.textContent.trim())", surface)
            wantd = NAV_DEAD if w > 767 else LIST_DEAD
            check(dead == wantd, "@%d %s dead rows %s, want %s" % (w, surface, dead, wantd))

            pg.close()
        b.close()
    print("\n%d ok / %d red" % (ok, red))
    sys.exit(1 if red else 0)


main()
