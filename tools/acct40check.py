#!/usr/bin/env python3
"""Task 40 -- view swap exit, skipped renewal date, autoplay, discount row.

Four of the five items are states or moments that only exist in a browser:

  * the outgoing view now stays on screen for one exit animation. Reading it
    means sampling DURING the swap -- afterwards the DOM is back to one visible
    view and every assertion would pass on the old behaviour too.
  * the phone push travels a whole container width, so `overflow-x: clip` on the
    container is load-bearing, not cosmetic. It is pinned by measuring the page
    width mid-animation, which is the thing that actually breaks without it.
  * the skipped block, the greyed button and the unskip line are one state on a
    board nothing switches at runtime; the probe sets the attribute itself and
    checks a neighbouring block did NOT change, or a rule that greys all four
    would read green.
  * ⚠ reduced_motion must be explicit -- the default collapses the durations and
    the whole motion section would read green on animations that never ran.
"""
import sys, pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
SAND, GREY_BG, GREY_INK = "rgb(245, 241, 233)", "rgb(230, 230, 230)", "rgb(128, 128, 128)"

ok = red = 0


def _chrome():
    hits = sorted((pathlib.Path.home() / ".cache/ms-playwright").glob(
        "chromium-*/chrome-linux64/chrome"))
    if not hits:
        sys.exit("no chromium -- run: npx playwright install chromium")
    return hits[-1]


def check(label, got, want):
    global ok, red
    if got == want:
        print("ok   %-60s %s" % (label, got)); ok += 1
    else:
        print("RED  %-60s got %r want %r" % (label, got, want)); red += 1


def css(pg, sel, prop):
    """A missing element is a red, not a crash."""
    if pg.locator(sel).count() == 0:
        return "NO ELEMENT: " + sel
    return pg.eval_on_selector(sel, "(e,p)=>getComputedStyle(e)[p]", prop)


# --------------------------------------------------------------------------
# 1 -- the swap: two views on screen, both animating, page never widens
# --------------------------------------------------------------------------
MID = """
()=>{const v=[...document.querySelectorAll('[data-acct-view]')];
 const live=v.filter(e=>!e.hidden);
 const out=v.find(e=>e.classList.contains('is-leaving'));
 const inn=v.find(e=>e.classList.contains('is-entering'));
 const anim=e=>{if(!e)return null;const a=e.getAnimations();if(!a.length)return 'no animation';
   const f=a[0].effect,skip=['offset','computedOffset','easing','composite'];
   return [a[0].animationName, f.getTiming().duration,
     f.getKeyframes().map(k=>k.transform||'').join(' | ')]};
 const d=document.documentElement;
 return {live:live.length, outPos:out?getComputedStyle(out).position:null,
         outHits:out?getComputedStyle(out).pointerEvents:null,
         out:anim(out), in:anim(inn),
         widens:d.scrollWidth>d.clientWidth}}
"""

REST = ("()=>[...document.querySelectorAll('[data-acct-view]')]"
        ".filter(e=>!e.hidden).map(e=>e.getAttribute('data-acct-view'))")


def run_swap(b, width, out_name, in_name, travel):
    ctx = b.new_context(viewport={"width": width, "height": 900},
                        reduced_motion="no-preference")
    pg = ctx.new_page()
    pg.goto((ROOT / "account.html").as_uri())
    pg.wait_for_timeout(500)
    tag = "@%d" % width

    check("%s container is positioned" % tag,
          css(pg, "[data-acct-views]", "position"), "relative")
    check("%s container allows artwork overflow" % tag,
          css(pg, "[data-acct-views]", "overflowX"), "visible")

    nav = ".gb-acct-nav" if width > 767 else ".gb-acct-list"
    pg.click(nav + " [data-acct-goto='orders']")
    mid = pg.evaluate(MID)

    # anchor: the overlap is the change. One live view means nothing below is real
    check("%s both views on screen mid-swap" % tag, mid["live"], 2)
    check("%s outgoing view is out of flow" % tag, mid["outPos"], "absolute")
    check("%s outgoing view is not clickable" % tag, mid["outHits"], "none")
    check("%s exit keyframes" % tag,
          mid["out"][0] if isinstance(mid["out"], list) else mid["out"], out_name)
    check("%s exit duration ms" % tag,
          mid["out"][1] if isinstance(mid["out"], list) else mid["out"], 500)
    check("%s enter keyframes" % tag,
          mid["in"][0] if isinstance(mid["in"], list) else mid["in"], in_name)
    check("%s enter travel" % tag,
          travel in (mid["in"][2] if isinstance(mid["in"], list) else ""), True)
    # the reason the container clips: without it the incoming view widens the page
    check("%s page does not widen mid-swap" % tag, mid["widens"], False)

    pg.wait_for_timeout(900)
    check("%s one view left when it settles" % tag, pg.evaluate(REST), ["orders"])

    # a second switch during the exit must not strand the first one. Driven
    # through the API, not the card: at 390 the list lives inside the view that
    # was just swapped away, and routing is acct32check's job anyway.
    pg.evaluate("()=>window.gumiAcct.view.show('details', true)")
    pg.wait_for_timeout(120)
    pg.evaluate("()=>window.gumiAcct.view.show('password', true)")
    pg.wait_for_timeout(900)
    check("%s fast double switch strands nothing" % tag,
          pg.evaluate(REST), ["password"])

    # going straight back while the first exit is still running: the stale exit
    # has to be cancelled, or its animationend fires on the view we returned to
    # and hides it -- an empty page, not a cosmetic glitch
    pg.evaluate("()=>window.gumiAcct.view.show('orders', true)")
    pg.wait_for_timeout(120)
    pg.evaluate("()=>window.gumiAcct.view.show('password', true)")
    pg.wait_for_timeout(900)
    check("%s switching back mid-exit keeps the view" % tag,
          pg.evaluate(REST), ["password"])
    ctx.close()


def run_auth_has_no_exit(b):
    """The auth page deliberately keeps the plain hide -- its two <main>s sit
    above a footer that would jump if one went out of flow."""
    ctx = b.new_context(viewport={"width": 390, "height": 900},
                        reduced_motion="no-preference")
    pg = ctx.new_page()
    pg.goto((ROOT / "account-login.html").as_uri())
    pg.wait_for_timeout(500)
    check("auth: anchor, both views exist",
          pg.locator("[data-acct-view]").count(), 2)
    pg.click("[data-acct-view='login'] .gb-acct-auth__alt a")
    check("auth: no view is left in flow behind the new one",
          pg.evaluate("()=>[...document.querySelectorAll('[data-acct-view]')]"
                      ".filter(e=>!e.hidden).length"), 1)
    check("auth: incoming view still animates",
          pg.evaluate("()=>{const e=document.querySelector"
                      "(\"[data-acct-view='signup']\");"
                      "return e.getAnimations().length>0}"), True)
    ctx.close()


# --------------------------------------------------------------------------
# 2 -- skipped next order
# --------------------------------------------------------------------------
DAYS = ("()=>[...document.querySelectorAll('.gb-acct-schedule__day')]"
        ".map(e=>{const c=getComputedStyle(e);"
        "return c.backgroundColor+' / '+c.color})")


def run_skip(b, width):
    pg = b.new_page(viewport={"width": width, "height": 950})
    pg.goto((ROOT / "account.html").as_uri() + "#detail")
    pg.wait_for_timeout(600)
    pg.mouse.move(0, 0)
    tag = "@%d" % width
    SKIP = ".gb-acct-schedule [data-acct-modal='skip-next']"
    LINE = ".gb-acct-schedule__unskip"

    check("%s anchor: four date blocks" % tag,
          pg.locator(".gb-acct-schedule__day").count(), 4)
    check("%s unskip line is out by default" % tag,
          pg.locator(LINE).is_hidden(), True)
    check("%s all four blocks start sand" % tag,
          set(pg.evaluate(DAYS)), {SAND + " / rgb(16, 24, 40)"})
    check("%s skip button starts green" % tag, css(pg, SKIP, "color"),
          "rgb(0, 86, 53)")

    pg.eval_on_selector(".gb-acct-schedule",
                        "e=>e.setAttribute('data-acct-skipped','')")
    # ⚠ the button carries a $t-base colour transition: read it mid-flight and
    # Chrome serialises the interpolated value as rgba(...), which matches no
    # expected string. 200ms sat exactly on the boundary and flaked.
    pg.wait_for_timeout(500)
    days = pg.evaluate(DAYS)
    check("%s skipped block greys out" % tag, days[0],
          GREY_BG + " / " + GREY_INK)
    # anchor: only the next one. A rule that hit every block would read green above
    check("%s the other three are untouched" % tag, set(days[1:]),
          {SAND + " / rgb(16, 24, 40)"})
    check("%s skipped block border" % tag,
          css(pg, ".gb-acct-schedule__day", "borderTopColor"), GREY_BG)
    check("%s skip button reads disabled" % tag, css(pg, SKIP, "color"), GREY_INK)
    check("%s skip button background" % tag,
          css(pg, SKIP, "backgroundColor"), GREY_BG)
    check("%s skip button is not a target" % tag,
          css(pg, SKIP, "pointerEvents"), "none")
    check("%s unskip line appears" % tag, pg.locator(LINE).is_visible(), True)
    check("%s unskip line text" % tag,
          " ".join(pg.inner_text(LINE).split()),
          "To unskip this order, edit your renewal date")
    check("%s unskip link opens the date picker" % tag,
          pg.get_attribute(LINE + " button", "data-acct-modal"), "edit-date")

    # ⚠ a hidden line makes this click time out and kill the script, which would
    # read as fewer reds rather than as a failure
    try:
        pg.click(LINE + " button", timeout=3000)
        pg.wait_for_timeout(600)
        opened = pg.evaluate("()=>{const e=document.querySelector"
                             "('.gb-acct-modal.is-open');"
                             "return e?e.getAttribute('data-acct-modal-panel'):null}")
    except Exception as e:
        opened = "unreachable (%s)" % type(e).__name__
    check("%s it really opens edit-date" % tag, opened, "edit-date")
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(600)
    pg.close()


# --------------------------------------------------------------------------
# 3 -- the retention video auto-plays (note 34511)
# --------------------------------------------------------------------------
def run_video(b):
    pg = b.new_page(viewport={"width": 1440, "height": 950})
    pg.goto((ROOT / "account.html").as_uri())
    pg.wait_for_timeout(400)
    got = pg.eval_on_selector(
        ".gb-acct-video__media",
        "e=>[e.autoplay,e.muted,e.loop,e.playsInline,e.hasAttribute('src')]")
    check("video autoplays", got[0], True)
    check("video is muted (autoplay is blocked otherwise)", got[1], True)
    check("video loops", got[2], True)
    check("video plays inline", got[3], True)
    check("video still has no source", got[4], False)
    pg.close()


# --------------------------------------------------------------------------
# 4 -- a long discount code tops out against the tag
# --------------------------------------------------------------------------
ROW = """
()=>{const r=document.querySelector('.gb-acct-summary__row--discount');
 const c=r.querySelector('.gb-acct-summary__code');
 const t=r.querySelector('.gb-acct-tag');
 const l=r.firstElementChild;
 const y=e=>Math.round(e.getBoundingClientRect().top*100)/100;
 return [Math.round(c.getBoundingClientRect().height), y(c)-y(t), y(c)-y(l)]}
"""


def run_discount(b, width):
    pg = b.new_page(viewport={"width": width, "height": 950})
    pg.goto((ROOT / "account.html").as_uri() + "#detail")
    pg.wait_for_timeout(600)
    tag = "@%d" % width
    pg.eval_on_selector(".gb-acct-detail",
                        "e=>e.setAttribute('data-acct-discount','applied')")
    pg.eval_on_selector(".gb-acct-summary__code",
                        "e=>e.textContent="
                        "'THISISADISAVERYVERYVERYVERYVERYLONGDISCOUNTCODE1265'")
    pg.wait_for_timeout(200)
    got = pg.evaluate(ROW)
    # anchor: the code must actually wrap, or top and centre land in the same place
    check("%s long code wraps to several lines" % tag, got[0] > 40, True)
    check("%s code top == tag top" % tag, got[1], 0)
    check("%s code top == label top" % tag, got[2], 0)
    pg.close()


with sync_playwright() as p:
    br = p.chromium.launch(executable_path=str(_chrome()))
    run_swap(br, 1440, "gb-acct-view-out", "gb-acct-view-in", "8px")
    run_swap(br, 390, "gb-acct-view-fade-out", "gb-acct-view-fade-in", " | ")
    run_auth_has_no_exit(br)
    for w in (1440, 390):
        run_skip(br, w)
        run_discount(br, w)
    run_video(br)
    br.close()

print("\n%d ok / %d red" % (ok, red))
sys.exit(1 if red else 0)
