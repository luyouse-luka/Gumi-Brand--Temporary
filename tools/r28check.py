#!/usr/bin/env python3
"""Task 28 regression: Log in and Sign up on one page.

account-signup.html is gone. Its <main> is now a second [data-acct-view] on
account-login.html, and the two alt links swap between the views in place.

⚠ Two mechanisms here fail SILENTLY if reverted, which is why each has its own
assertion rather than riding on a visual check:

  - `.gb-acct-auth[hidden] { display: none }` -- the block sets display:flex,
    which outranks the UA's [hidden]{display:none}. Without the override BOTH
    views paint, and every other assertion still reads green off the first one.
  - `view.show()` falling back to `views[0]` instead of the hard-coded
    'overview' -- this page has no overview, so an unknown hash used to recurse
    until the stack blew. The console stays silent about it because modules are
    init'd inside a try/catch, so the fallback group below watches for errors.
"""
import pathlib
import sys

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / "account-login.html"
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
        print("  RED  %-54s want %r got %r" % (label, want, got))


# --- 1. the page and the references to the page it replaced --------------------
print("1 -- files")
# anchor: an absence is only meaningful once the thing that replaced it is here
check("the merged page exists", PAGE.is_file(), True)
src = PAGE.read_text(encoding="utf-8")
check("anchor: it carries the view hooks", 'data-acct-goto="signup"' in src, True)

check("account-signup.html is gone", (ROOT / "account-signup.html").exists(), False)
refs = sorted(p.name for p in ROOT.glob("*.html")
              if "account-signup.html" in p.read_text(encoding="utf-8"))
check("no page still links to it", refs, [])
check("neither alt link loads a page", src.count('href="account-signup.html"')
      + src.count('href="account-login.html"'), 0)

VIEW = "[data-acct-view='%s']"
ALT = VIEW + " .gb-acct-auth__alt [data-acct-goto='%s']"

READ = """() => {
  const v = [...document.querySelectorAll('[data-acct-view]')];
  return v.map(e => [e.getAttribute('data-acct-view'),
                     getComputedStyle(e).display,
                     e.hasAttribute('hidden'),
                     e.querySelector('.gb-acct-auth__title').textContent.trim()]);
}"""


def run(pw):
    global ok, red
    b = pw.chromium.launch(executable_path=str(_chrome()))
    errs = []
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.on("pageerror", lambda e: errs.append("pageerror: %s" % e))
    pg.on("console", lambda m: errs.append("console: %s" % m.text)
          if m.type == "error" else None)

    # --- 2. first paint -------------------------------------------------------
    print("2 -- first paint")
    pg.goto(PAGE.as_uri())
    pg.wait_for_timeout(400)
    v = pg.evaluate(READ)
    check("two views, in board order", [r[0] for r in v], ["login", "signup"])
    check("login is laid out", v[0][1] != "none", True)
    check("login carries no [hidden]", v[0][2], False)
    check("login shows the Log in board", v[0][3], "Log in")
    check("signup carries [hidden]", v[1][2], True)
    # the one that silently breaks: display:flex outranks the UA [hidden] rule
    check("signup is really display:none", v[1][1], "none")
    check("signup's board is the Sign up one", v[1][3], "Sign up")
    # first, because a blown stack here leaves both views hidden and every click
    # below times out instead of reporting a readable red
    check("first paint raised no script error", errs, [])

    # --- 3. the links swap the views -----------------------------------------
    print("3 -- clicking the alt links")
    pg.click(ALT % ("login", "signup"))
    pg.wait_for_timeout(500)
    v = pg.evaluate(READ)
    check("login goes away", v[0][1], "none")
    check("signup is laid out", v[1][1] != "none", True)
    check("hash follows the view", pg.evaluate("() => location.hash"), "#signup")
    check("exactly one view visible",
          pg.evaluate("() => [...document.querySelectorAll('[data-acct-view]')]"
                      ".filter(e => getComputedStyle(e).display !== 'none').length"), 1)
    # the sign-up board's own fields, proof the merge kept its form and not a
    # second copy of the login one
    check("sign-up keeps its name row",
          pg.evaluate("s => document.querySelectorAll(s).length",
                      VIEW % "signup" + " .gb-acct-auth__row .gb-acct-field"), 2)
    check("sign-up submit reads Sign up",
          pg.inner_text(VIEW % "signup" + " .gb-acct-auth__submit").strip(), "Sign up")

    pg.click(ALT % ("signup", "login"))
    pg.wait_for_timeout(500)
    v = pg.evaluate(READ)
    check("and back: login is laid out", v[0][1] != "none", True)
    check("and back: signup is display:none", v[1][1], "none")
    check("and back: hash follows", pg.evaluate("() => location.hash"), "#login")

    # --- 4. deep link and unknown hash ---------------------------------------
    print("4 -- hash routing")
    pg.goto(PAGE.as_uri() + "#signup")
    pg.wait_for_timeout(400)
    v = pg.evaluate(READ)
    check("#signup opens on Sign up", [v[0][1], v[1][1] != "none"], ["none", True])

    del errs[:]
    pg.goto(PAGE.as_uri() + "#nope")
    pg.wait_for_timeout(400)
    v = pg.evaluate(READ)
    # views[0], not the hard-coded 'overview' this page does not have
    check("an unknown hash falls back to login", v[0][1] != "none", True)
    check("the fallback did not blow the stack", errs, [])

    # --- 5. the swap is not an instant cut (铁律 13) ---------------------------
    print("5 -- entry motion")
    anim = pg.evaluate("""s => {
      const e = document.querySelector(s);
      e.classList.add('is-entering');
      const c = getComputedStyle(e);
      const out = [c.animationName, c.animationDuration];
      e.classList.remove('is-entering');
      return out;
    }""", VIEW % "login")
    check("the incoming view animates", anim[0], "gb-acct-view-in")
    check("and the animation has a duration", anim[1] != "0s", True)

    pg.set_viewport_size({"width": 390, "height": 844})
    pg.wait_for_timeout(200)
    anim = pg.evaluate("""s => {
      const e = document.querySelector(s);
      e.classList.add('is-entering');
      const n = getComputedStyle(e).animationName;
      e.classList.remove('is-entering');
      return n;
    }""", VIEW % "login")
    check("phone pushes in from the right", anim, "gb-acct-view-in-right")

    # --- 6. no JS: both forms must stay usable -------------------------------
    # The [hidden] attribute is in the HTML, so gating its CSS on .acct-live is
    # the only thing standing between "account.js 404s" and "nobody can register".
    print("6 -- degraded (no JS)")
    nojs = b.new_context(viewport={"width": 1440, "height": 900},
                         java_script_enabled=False)
    npg = nojs.new_page()
    npg.goto(PAGE.as_uri())
    npg.wait_for_timeout(300)
    shown = npg.eval_on_selector_all(
        "[data-acct-view]", "els => els.map(e => getComputedStyle(e).display)")
    check("without JS both forms are laid out", [x != "none" for x in shown], [True, True])
    check("without JS the alt links still point somewhere",
          npg.eval_on_selector_all(".gb-acct-auth__alt a", "a => a.map(e => e.getAttribute('href'))"),
          ["#signup", "#login"])
    nojs.close()

    # --- 7. phone: both links still reachable --------------------------------
    print("7 -- phone")
    pg.goto(PAGE.as_uri())
    pg.wait_for_timeout(400)
    pg.click(ALT % ("login", "signup"))
    pg.wait_for_timeout(500)
    check("the swap works at 390",
          pg.evaluate(READ)[1][1] != "none", True)
    check("no account nav on the auth page",
          pg.evaluate("() => !!document.querySelector('.gb-acct-nav, .gb-acct-list')"), False)

    b.close()


with sync_playwright() as pw:
    run(pw)

print("\nr28: %d ok / %d red" % (ok, red))
sys.exit(1 if red else 0)
