#!/usr/bin/env python3
"""Task 38 -- the three calendars now run on flatpickr, skinned to board 30621.

What this has to prove, beyond "it renders":
  * the look did not move. Every token here was read off the hand-written
    .gb-acct-cal before it was deleted, so a drift in the skin shows up as red
    rather than as "looks about right".
  * the behaviours Task 31/32 settled survived the swap: shut by default and
    slides open on the field, tomorrow is the first selectable day, a past field
    value selects nothing and lands on the first month that has a live day, and
    picking a day dispatches input so acctForm un-disables Save.
  * flatpickr's own stylesheet is NOT loaded, so the layout rules in
    account.scss are load-bearing. The column geometry assertion is what fails
    if someone deletes them as "cosmetic".

Dates are computed, never hardcoded: minDate is tomorrow, so a literal would
rot overnight.
"""
import sys, pathlib, re
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
GRAY_700 = "rgb(77, 77, 77)"    # #4d4d4d
GRAY_400 = "rgb(128, 128, 128)" # #808080
GRAY_300 = "rgb(204, 204, 204)" # #cccccc
GREEN = "rgb(0, 86, 53)"        # #005635
WHITE = "rgb(255, 255, 255)"

ok = red = 0


def _chrome():
    base = pathlib.Path.home() / ".cache/ms-playwright"
    hits = sorted(base.glob("chromium-*/chrome-linux64/chrome"))
    if not hits:
        sys.exit("no chromium under %s" % base)
    return hits[-1]


def check(label, got, want):
    global ok, red
    if got == want:
        print("ok   %-60s %s" % (label, got)); ok += 1
    else:
        print("RED  %-60s got %r want %r" % (label, got, want)); red += 1


def css(pg, sel, prop):
    # A missing element must read red, not raise: a crash here stops the run and
    # the remaining assertions never report at all.
    if pg.locator(sel).count() == 0:
        return "NO ELEMENT: " + sel
    return pg.eval_on_selector(sel, "(e,p)=>getComputedStyle(e)[p]", prop)


def goto(b, width, hash_="#detail", **kw):
    pg = b.new_page(viewport={"width": width, "height": 950}, **kw)
    pg.goto((ROOT / "account.html").as_uri() + hash_)
    pg.wait_for_timeout(700)
    return pg


def open_cal(pg, panel, field):
    """Open a panel and slide its field calendar out."""
    pg.click("[data-acct-modal='%s']" % panel)
    pg.wait_for_timeout(500)
    pg.click("#" + field)
    pg.wait_for_timeout(900)     # 400ms slide + settle
    pg.mouse.move(0, 0)          # click leaves the pointer hovering a day


# --------------------------------------------------------------------------
def run_wiring(b):
    """1 -- all three calendars are flatpickr, and nothing hand-written is left."""
    pg = goto(b, 1440)

    check("no hand-written cal markup left in the page",
          "gb-acct-cal__" in pg.content(), False)
    check("flatpickr is loaded", pg.evaluate("typeof flatpickr"), "function")
    check("acctCal still exported",
          pg.evaluate("!!(window.gumiAcct && window.gumiAcct.cal)"), True)

    # three roots, each with a plugin instance attached
    check("three calendar roots", pg.locator("[data-acct-cal]").count(), 3)
    check("every root got a flatpickr instance",
          pg.evaluate("[...document.querySelectorAll('[data-acct-cal]')]"
                      ".every(r=>!!r._fp)"), True)

    # the holiday panel drives no field, so it carries its own input
    check("holiday root has its own input",
          pg.locator("[data-acct-cal]:not([data-acct-cal-for]) "
                     "[data-acct-cal-input]").count(), 1)
    pg.close()


def run_tokens(b):
    """2 -- the skin still reads the board's values (30621-30631)."""
    pg = goto(b, 390)
    open_cal(pg, "edit-date", "acct-f-date")
    P = "[data-acct-modal-panel='edit-date'] "

    for label, sel, prop, want in [
        ("cal ring",        ".gb-acct-cal", "boxShadow", "%s 0px 0px 0px 1px inset" % GRAY_300),
        ("cal radius",      ".gb-acct-cal", "borderRadius", "8px"),
        # 30623 pads 20/24; the 22 is client-set (Task 45), see acct45check
        ("30623 padding",   ".flatpickr-calendar", "padding", "20px 22px"),
        ("30625 head 32",   ".flatpickr-months", "height", "32px"),
        ("30624 gap 12",    ".flatpickr-months", "marginBottom", "12px"),
        ("title size",      ".flatpickr-current-month", "fontSize", "16px"),
        ("title weight",    ".flatpickr-current-month", "fontWeight", "500"),
        ("title tracking",  ".flatpickr-current-month", "letterSpacing", "-0.32px"),
        ("title ink",       ".flatpickr-current-month", "color", GRAY_700),
        ("year matches title", ".cur-year", "fontSize", "16px"),
        ("arrow box",       ".flatpickr-next-month", "height", "40px"),
        ("arrow ink",       ".flatpickr-next-month", "color", GRAY_400),
        ("weekday size",    ".flatpickr-weekday", "fontSize", "14px"),
        ("weekday weight",  ".flatpickr-weekday", "fontWeight", "500"),
        ("weekday ink",     ".flatpickr-weekday", "color", GRAY_700),
        ("day 40 circle",   ".flatpickr-day", "borderRadius", "20px"),
        ("day weight 400",  ".flatpickr-day:not(.flatpickr-disabled)", "fontWeight", "400"),
        ("day ink",         ".flatpickr-day:not(.flatpickr-disabled)", "color", GRAY_700),
        ("dead day ink",    ".flatpickr-day.flatpickr-disabled", "color", GRAY_400),
    ]:
        check("390 %s" % label, css(pg, P + sel, prop), want)

    # the 40x40 slot is geometry, not a font size -- read the rect
    box = pg.eval_on_selector(P + ".flatpickr-day",
                              "e=>{const r=e.getBoundingClientRect();"
                              "return [Math.round(r.width),Math.round(r.height)]}")
    check("390 day slot is 40x40", box, [40, 40])

    # ⚠ flatpickr's own stylesheet is not loaded, so the grid rules in
    # account.scss are the only thing laying this out. "Evenly spaced" is NOT
    # enough of a test: with display:block the day spans sit flush against each
    # other, which is also even -- at a 40 pitch instead of the column's 43.14.
    # The pitch has to be the container divided by seven.
    geo = pg.evaluate("""()=>{const c=document.querySelector(
        "[data-acct-modal-panel='edit-date'] .dayContainer");
        const d=[...c.querySelectorAll('.flatpickr-day')].slice(0,8)
          .map(e=>e.getBoundingClientRect().left);
        return {w:c.getBoundingClientRect().width,
                pitch:d[1]-d[0], wrap:Math.round(d[7]-d[0]),
                even:new Set(d.slice(0,7).map((v,i,a)=>i?Math.round((v-a[i-1])*10):0)
                     .slice(1)).size}}""")
    check("390 day columns are the container / 7",
          abs(geo["pitch"] - geo["w"] / 7) < 0.5, True)
    check("390 columns are evenly pitched", geo["even"], 1)
    check("390 row wraps after 7", geo["wrap"], 0)
    check("390 grid rules are live", css(pg, P + ".dayContainer", "display"), "grid")
    pg.close()


def run_behaviour(b, width):
    """3 -- everything Task 31/32 settled still holds."""
    tag = "@%d" % width
    pg = goto(b, width)
    P = "[data-acct-modal-panel='edit-date'] "

    # shut by default, and it is the field that opens it
    pg.click("[data-acct-modal='edit-date']")
    pg.wait_for_timeout(500)
    shut = pg.eval_on_selector(P + ".gb-acct-cal--field",
                               "e=>Math.round(e.getBoundingClientRect().height)")
    check("%s calendar starts shut" % tag, shut, 0)
    pg.click("#acct-f-date")
    pg.wait_for_timeout(900)
    pg.mouse.move(0, 0)
    open_h = pg.eval_on_selector(P + ".gb-acct-cal--field",
                                 "e=>Math.round(e.getBoundingClientRect().height)")
    check("%s field click slides it out" % tag, open_h > 300, True)

    # a past field value (the boards ship 19/07/2026) selects nothing ...
    check("%s past value selects no day" % tag,
          pg.locator(P + ".flatpickr-day.selected").count(), 0)
    # ... and the view lands on the month that holds the first live day
    want_month = pg.evaluate("""()=>{const d=new Date();d.setHours(0,0,0,0);
        d.setDate(d.getDate()+1);
        return d.toLocaleString('en',{month:'long'})+' '+d.getFullYear()}""")
    shown = pg.eval_on_selector(P + ".flatpickr-current-month",
                                "e=>e.querySelector('.cur-month').textContent.trim()"
                                "+' '+e.querySelector('.cur-year').value")
    check("%s opens on the first live month" % tag, shown, want_month)

    # tomorrow is the first selectable day (note 30923)
    state = pg.evaluate("""()=>{const t=new Date();t.setHours(0,0,0,0);
        const fmt=d=>d.toLocaleString('en',{month:'long'})+' '+d.getDate()+', '+d.getFullYear();
        const tom=new Date(t); tom.setDate(t.getDate()+1);
        const pick=l=>{const e=[...document.querySelectorAll(
          "[data-acct-modal-panel='edit-date'] .flatpickr-day")]
          .find(x=>x.getAttribute('aria-label')===l);
          return e?e.classList.contains('flatpickr-disabled'):null};
        return {today:pick(fmt(t)), tomorrow:pick(fmt(tom))}}""")
    check("%s today is out" % tag, state["today"], True)
    check("%s tomorrow is in" % tag, state["tomorrow"], False)

    # picking writes dd/mm/yyyy back AND dispatches input, or Save stays grey
    save = P + "[data-acct-save]"
    check("%s Save starts disabled" % tag, pg.locator(save).is_disabled(), True)
    # Save rides on the plugin's own events, not on anything we re-dispatch --
    # record what actually reaches the field.
    pg.evaluate("""()=>{window.__fired=[];const i=document.getElementById('acct-f-date');
        ['input','change'].forEach(t=>i.addEventListener(t,()=>window.__fired.push(t)))}""")
    pg.click(P + ".flatpickr-day:not(.flatpickr-disabled):not(.prevMonthDay)")
    pg.wait_for_timeout(400)
    fired = pg.evaluate("window.__fired")
    val = pg.input_value("#acct-f-date")
    check("%s the pick fired change on the field" % tag,
          "change" in fired, True)
    check("%s writes dd/mm/yyyy" % tag, bool(re.match(r"^\d{2}/\d{2}/\d{4}$", val)), True)
    check("%s Save un-disabled by the pick" % tag, pg.locator(save).is_disabled(), False)
    check("%s picked day is marked" % tag,
          pg.locator(P + ".flatpickr-day.selected").count(), 1)
    check("%s selected fill" % tag,
          css(pg, P + ".flatpickr-day.selected", "backgroundColor"), GREEN)
    check("%s selected ink" % tag,
          css(pg, P + ".flatpickr-day.selected", "color"), WHITE)

    # neighbouring-month days stay dead, same as the hand-written grid
    check("%s prev-month day is not clickable" % tag,
          css(pg, P + ".flatpickr-day.prevMonthDay", "pointerEvents"), "none")

    # Mo..Su, with the board's own 'Sat'
    check("%s weekday order" % tag,
          pg.evaluate("""()=>[...document.querySelectorAll(
              "[data-acct-modal-panel='edit-date'] .flatpickr-weekday")]
              .map(e=>e.textContent.trim()).join(' ')"""),
          "Mo Tu We Th Fr Sat Su")

    # arrows are spans; they had to be given a role and a name back
    check("%s prev arrow is labelled" % tag,
          pg.eval_on_selector(P + ".flatpickr-prev-month", "e=>e.getAttribute('aria-label')"),
          "Previous month")
    check("%s next arrow is focusable" % tag,
          pg.eval_on_selector(P + ".flatpickr-next-month", "e=>e.getAttribute('tabindex')"), "0")

    pg.keyboard.press("Escape")
    pg.wait_for_timeout(500)

    # --- the other two instances -----------------------------------------
    # restart lives behind the cancelled detail state and cancel-holiday behind
    # the cancel flow; routing is acct32check's job, so open them directly.
    pg.evaluate("()=>window.gumiAcct.modal.open('restart')")
    pg.wait_for_timeout(500)
    R = "[data-acct-modal-panel='restart'] "
    check("%s restart calendar starts shut" % tag,
          pg.eval_on_selector(R + ".gb-acct-cal--field",
                              "e=>Math.round(e.getBoundingClientRect().height)"), 0)
    pg.click("#acct-f-restart")
    pg.wait_for_timeout(900)
    pg.mouse.move(0, 0)
    check("%s restart draws a grid" % tag,
          pg.locator(R + ".flatpickr-day").count() >= 28, True)
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(500)

    # the holiday panel's calendar is always on show -- no field to open it
    pg.evaluate("()=>window.gumiAcct.modal.open('cancel-holiday')")
    pg.wait_for_timeout(700)
    H = "[data-acct-modal-panel='cancel-holiday'] "
    check("%s holiday calendar is visible unprompted" % tag,
          pg.locator(H + ".flatpickr-calendar").is_visible(), True)
    check("%s holiday calendar has no field wrapper" % tag,
          pg.locator(H + ".gb-acct-cal--field").count(), 0)
    # ⚠ board 30669 fills exactly one day. A calendar with no field of its own
    # has no past value to disagree with, so it opens on the first selectable
    # day -- unlike edit-date, which opens with nothing picked.
    check("%s holiday opens with one day filled" % tag,
          pg.locator(H + ".flatpickr-day.selected").count(), 1)
    check("%s holiday's filled day is tomorrow" % tag,
          pg.eval_on_selector(H + ".flatpickr-day.selected", "e=>e.getAttribute('aria-label')"),
          pg.evaluate("""()=>{const d=new Date();d.setHours(0,0,0,0);
              d.setDate(d.getDate()+1);
              return d.toLocaleString('en',{month:'long'})+' '+d.getDate()+', '+d.getFullYear()}"""))
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(400)
    pg.close()


def run_no_plugin(b):
    """4 -- the page survives flatpickr failing to load."""
    pg = b.new_page(viewport={"width": 1440, "height": 950})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.route("**/flatpickr.min.js*", lambda r: r.abort())
    pg.goto((ROOT / "account.html").as_uri() + "#detail")
    pg.wait_for_timeout(900)

    check("no plugin: page did not throw", errs, [])
    check("no plugin: account.js still finished",
          pg.evaluate("!!window.gumiAcct"), True)
    # the rest of the page has to keep working
    pg.click("[data-acct-modal='edit-date']")
    pg.wait_for_timeout(500)
    check("no plugin: panels still open",
          pg.evaluate("()=>{const e=document.querySelector('.gb-acct-modal.is-open');"
                      "return e?e.getAttribute('data-acct-modal-panel'):null}"), "edit-date")
    check("no plugin: no calendar drawn",
          pg.locator(".flatpickr-calendar").count(), 0)
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(300)
    pg.close()


with sync_playwright() as p:
    b = p.chromium.launch(executable_path=str(_chrome()))
    run_wiring(b)
    run_tokens(b)
    for w in (1440, 390):
        run_behaviour(b, w)
    run_no_plugin(b)
    b.close()

print("\n%d ok / %d red" % (ok, red))
sys.exit(1 if red else 0)
