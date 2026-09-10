#!/usr/bin/env python3
"""prefers-reduced-motion coverage for the account pages (global rule 13 tail).

account.scss deliberately does NOT repeat a blanket reduce rule: customstyle.scss
already ships one at the top (`*, *::before, *::after { ... !important }`) and
account.css loads after it, so every account transition is already flattened.
Writing a second copy would be dead code -- this proves the first one reaches.

Read twice on purpose: under `reduce` the durations must collapse, and under
`no-preference` the SAME selectors must still carry their real durations. One
reading alone cannot tell "reduce works" from "the element has no transition".
"""
import sys, pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent


def _chrome():
    hits = sorted((pathlib.Path.home() / ".cache/ms-playwright").glob(
        "chromium-*/chrome-linux64/chrome"))
    if not hits:
        sys.exit("no chromium installed -- run: npx playwright install chromium")
    return hits[-1]


# page -> selectors that must have a real transition when motion is allowed
TARGETS = {
    "account.html": [".gb-acct-header__logo", ".gb-acct-nav__link",
                     ".gb-acct-logout", ".gb-acct-field__input",
                     ".gb-acct-modal__panel", ".gb-acct-link"],
    "account-login.html": [".gb-acct-auth__submit", "a.gb-acct-auth__aside",
                           ".gb-acct-auth__alt a", ".gb-acct-field__input"],
    "account-signup.html": [".gb-acct-auth__submit", ".gb-acct-field__input"],
}
GET = ("s=>{const e=document.querySelector(s);if(!e)return null;"
       "const c=getComputedStyle(e);"
       "return [c.transitionDuration, c.transitionDelay, c.animationDuration]}")


def secs(v):
    return sum(float(x.strip().rstrip("s")) for x in v.split(",") if x.strip())


def main():
    ok = red = 0
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=str(_chrome()))
        for page, sels in TARGETS.items():
            read = {}
            for mode in ("no-preference", "reduce"):
                ctx = b.new_context(viewport={"width": 1440, "height": 900},
                                    reduced_motion=mode)
                pg = ctx.new_page()
                pg.goto((ROOT / page).as_uri())
                pg.wait_for_timeout(300)
                read[mode] = {s: pg.evaluate(GET, s) for s in sels}
                ctx.close()
            for s in sels:
                base, red_ = read["no-preference"][s], read["reduce"][s]
                tag = "%s %s" % (page, s)
                if base is None or red_ is None:
                    print("RED  %-50s element not found" % tag); red += 1
                    continue
                # the invariant: motion-allowed must actually carry motion, or
                # the reduce reading below proves nothing
                if secs(base[0]) < 0.05:
                    print("RED  %-50s no real transition to reduce (%s)" % (tag, base[0]))
                    red += 1
                    continue
                if secs(red_[0]) > 0.001 or secs(red_[1]) > 0.001:
                    print("RED  %-50s reduce not applied: %s / delay %s"
                          % (tag, red_[0], red_[1])); red += 1
                else:
                    ok += 1
        b.close()
    print("\n%d ok / %d red" % (ok, red))
    sys.exit(1 if red else 0)


main()
