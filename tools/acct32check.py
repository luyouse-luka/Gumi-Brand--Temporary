#!/usr/bin/env python3
"""Task 32 -- the reactivation flow.

Two requirements, both from the boards:
  note 28323  the cancelled card's CTA goes into the reactivation flow, i.e.
              the detail view opened in its own state, not the active one
  34192+34040 the restart panel picks a date, and the earliest one is tomorrow

The three list cards share one detail view, so "opens in the right state" is
the whole point of the change -- asserting the view is merely visible would
pass just as well before it.
"""
import sys, pathlib, datetime
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent


def _chrome():
    base = pathlib.Path.home() / ".cache/ms-playwright"
    hits = sorted(base.glob("chromium-*/chrome-linux64/chrome"))
    if not hits:
        sys.exit("no chromium under %s -- run: npx playwright install chromium" % base)
    return hits[-1]


CARDS = [("active", "Manage Subscription"),
         ("paused", "Manage Subscription"),
         ("cancelled", "Re-Activate Subscription")]

ok = red = 0


def check(label, got, want):
    global ok, red
    if got == want:
        print("ok   %-58s %s" % (label, got)); ok += 1
    else:
        print("RED  %-58s got %r want %r" % (label, got, want)); red += 1


def reach_subscriptions(pg, w):
    nav = ".gb-acct-nav" if w > 767 else ".gb-acct-list"
    pg.click(nav + " [data-acct-goto='subscriptions']")
    pg.wait_for_timeout(700)


def run(b, w):
    tag = "@%d" % w
    pg = b.new_page(viewport={"width": w, "height": 900})
    pg.goto((ROOT / "account.html").as_uri())
    pg.wait_for_timeout(400)

    # --- anchors: without these the assertions below could pass on nothing ---
    reach_subscriptions(pg, w)
    states = pg.eval_on_selector_all(
        "[data-acct-view='subscriptions'] .gb-acct-sub[data-acct-sub-state]",
        "els=>els.map(e=>e.getAttribute('data-acct-sub-state'))")
    check("anchor: three cards" + tag, states, ["active", "paused", "cancelled"])

    # every card's CTA now routes; the cancelled one used to be href="#"
    ctas = pg.eval_on_selector_all(
        "[data-acct-view='subscriptions'] .gb-acct-sub__cta",
        "els=>els.map(e=>[e.tagName,e.getAttribute('data-acct-goto'),"
        "e.getAttribute('href'),e.textContent.trim()])")
    check("cta count" + tag, len(ctas), 3)
    for i, (state, text) in enumerate(CARDS):
        if i >= len(ctas):
            break
        check("cta %s is a routing button%s" % (state, tag),
              [ctas[i][0], ctas[i][1], ctas[i][2]], ["BUTTON", "detail", None])
        check("cta %s label%s" % (state, tag), ctas[i][3], text)

    # --- each card opens the detail view in its own state ---
    for state, _ in CARDS:
        pg.goto((ROOT / "account.html").as_uri())
        pg.wait_for_timeout(400)
        reach_subscriptions(pg, w)
        pg.click("[data-acct-view='subscriptions'] "
                 ".gb-acct-sub[data-acct-sub-state='%s'] .gb-acct-sub__cta" % state)
        pg.wait_for_timeout(700)
        pg.mouse.move(0, 0)
        shown = pg.evaluate(
            "()=>{const e=document.querySelector(\"[data-acct-view='detail']\");"
            "return e?!e.hidden:null}")
        check("card %s reaches detail%s" % (state, tag), shown, True)
        check("detail state after %s%s" % (state, tag),
              pg.get_attribute(".gb-acct-detail", "data-acct-sub-state"), state)

        # the state has to actually change what is on screen, or the attribute
        # is just a label: these three elements are state-exclusive on the boards
        vis = pg.evaluate(
            "()=>{const v=s=>{const e=document.querySelector(s);"
            "return e?e.checkVisibility({visibilityProperty:true}):false};"
            "return [v(\"[data-acct-modal='restart']\"),"
            "v(\"[data-detail-only='cancelled']\"),"
            "v(\"[data-detail-only='paused']\")]}")
        check("restart button visible only when cancelled%s (%s)" % (tag, state),
              vis[0], state == "cancelled")
        check("cancelled-only block%s (%s)" % (tag, state),
              vis[1], state == "cancelled")
        check("paused-only block%s (%s)" % (tag, state),
              vis[2], state == "paused")

    # --- restart panel: calendar present, tomorrow is the floor, click writes back ---
    pg.goto((ROOT / "account.html").as_uri())
    pg.wait_for_timeout(400)
    reach_subscriptions(pg, w)
    pg.click("[data-acct-view='subscriptions'] "
             ".gb-acct-sub[data-acct-sub-state='cancelled'] .gb-acct-sub__cta")
    pg.wait_for_timeout(700)
    pg.click(".gb-acct-detail [data-acct-modal='restart']")
    pg.wait_for_timeout(500)
    check("restart panel open" + tag,
          pg.evaluate("()=>{const e=document.querySelector"
                      "(\"[data-acct-modal-panel='restart']\");"
                      "return e?e.classList.contains('is-open'):null}"), True)
    check("calendar rendered in restart" + tag,
          pg.evaluate("()=>{const e=document.querySelector"
                      "(\"[data-acct-modal-panel='restart'] [data-acct-cal]\");"
                      "return e?e.querySelectorAll('.flatpickr-day').length>27:null}"),
          True)

    # The calendar drops out of the field on click, so "rendered" above is not
    # enough on its own -- it is in the DOM the whole time.
    READ = ("()=>{const c=document.querySelector"
            "(\"[data-acct-modal-panel='restart'] [data-acct-cal]\");"
            "const f=document.querySelector"
            "(\"[data-acct-modal-panel='restart'] .gb-acct-field\");"
            "if(!c||!f)return null;"
            "return [c.checkVisibility({visibilityProperty:true}),"
            "Math.round(c.getBoundingClientRect().height),"
            "Math.round(f.getBoundingClientRect().height)]}")
    check("calendar starts shut" + tag, pg.evaluate(READ), [False, 0, 70])
    check("field reads as clickable" + tag,
          pg.eval_on_selector("[data-acct-modal-panel='restart'] .gb-acct-field__input",
                              "e=>getComputedStyle(e).cursor"), "pointer")
    pg.click("[data-acct-modal-panel='restart'] .gb-acct-field__input")
    pg.wait_for_timeout(700)
    pg.mouse.move(0, 0)
    opened = pg.evaluate(READ)
    check("clicking the input opens it" + tag, opened and opened[0], True)
    check("opened calendar has height" + tag, bool(opened) and opened[1] > 300, True)
    pg.click("[data-acct-modal-panel='restart'] .gb-acct-field__input")
    pg.wait_for_timeout(700)
    check("clicking again shuts it" + tag, pg.evaluate(READ), [False, 0, 70])
    pg.click("[data-acct-modal-panel='restart'] .gb-acct-field__input")
    pg.wait_for_timeout(700)
    check("calendar drives the restart field" + tag,
          pg.get_attribute("[data-acct-modal-panel='restart'] [data-acct-cal]",
                           "data-acct-cal-for"), "acct-f-restart")

    # note 34040: they cannot restart until the next day
    today = datetime.date.today()
    floor = pg.evaluate(
        "()=>{const d=[...document.querySelectorAll"
        "(\"[data-acct-modal-panel='restart'] .flatpickr-day:not(.flatpickr-disabled):not(.prevMonthDay):not(.nextMonthDay)\")];"
        "if(!d.length)return null;"
        "const x=new Date(d[0].getAttribute('aria-label'));const p2=n=>(n<10?'0':'')+n;"
        "return x.getFullYear()+'-'+p2(x.getMonth()+1)+'-'+p2(x.getDate())}")
    check("earliest selectable day is tomorrow or later" + tag,
          bool(floor) and floor > today.isoformat(), True)

    # ⚠ a shut calendar makes this click time out and kill the script, which
    # would read as fewer reds rather than as a failure
    d = datetime.date.fromisoformat(floor)
    try:
        pg.click("[data-acct-modal-panel='restart'] .flatpickr-day:not(.flatpickr-disabled):not(.prevMonthDay):not(.nextMonthDay)",
                 timeout=3000)
        pg.wait_for_timeout(200)
        got = pg.input_value("#acct-f-restart")
    except Exception as e:
        got = "unreachable (%s)" % type(e).__name__
    check("clicking a day writes the field" + tag, got, d.strftime("%d/%m/%Y"))
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(400)
    pg.close()


def main():
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=str(_chrome()))
        for w in (390, 1440):
            run(b, w)
        b.close()
    print("\n%d ok / %d red" % (ok, red))
    sys.exit(1 if red else 0)


main()
