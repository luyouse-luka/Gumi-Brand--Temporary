#!/usr/bin/env python3
"""Task 42 -- the pre-rendered calendar shell, and a cursor on days you cannot pick.

Two things that only the live theme exposes:

  * `snippets/gb-account-flatpickr-cal.liquid` pre-renders a static
    `.flatpickr-calendar` inside the container so the modal has one before the
    plugin loads. flatpickr APPENDS its own rather than adopting it, so the live
    page showed two. The static page has no shell, which is why three rounds of
    calendar work never saw this -- the probe therefore builds the live shape
    itself and drives `_arm` through it.
  * the disabled days had `pointer-events: none`, which also kills the cursor
    ([[cursor-not-allowed-vs-pointer-events]]). Dropping it is only safe if
    flatpickr really refuses the click, so that is asserted as behaviour, not
    just as a declaration.

⚠ Nothing here hardcodes a date. The count of disabled days in the open month is
derived from today, and the CSS assertions run on a day the probe marks itself,
so they still fire on the last day of a month when the view opens on the next
one and there is no naturally disabled day on screen.
"""
import sys, pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
GRAY_400 = "rgb(128, 128, 128)"
TRANSPARENT = "rgba(0, 0, 0, 0)"

ok = red = skip = 0


def check(label, got, want):
    global ok, red
    if got == want:
        print("ok   %-58s %s" % (label, got)); ok += 1
    else:
        print("RED  %-58s got %r want %r" % (label, got, want)); red += 1


def note(label, why):
    global skip
    print("SKIP %-58s %s" % (label, why)); skip += 1


def _chrome():
    hits = sorted((pathlib.Path.home() / ".cache/ms-playwright").glob(
        "chromium-*/chrome-linux64/chrome"))
    if not hits:
        sys.exit("no chromium -- run: npx playwright install chromium")
    return str(hits[-1])


def goto(b, width=1440):
    pg = b.new_page(viewport={"width": width, "height": 950})
    pg.goto((ROOT / "account.html").as_uri() + "#detail")
    pg.wait_for_timeout(700)
    return pg


def open_cal(pg, panel, field):
    # restart sits behind the cancelled detail state; routing into it is
    # acct32check's job, so open the panel directly like acct38check does.
    pg.evaluate("(p)=>window.gumiAcct.modal.open(p)", panel)
    pg.wait_for_timeout(500)
    pg.click("#" + field)
    pg.wait_for_timeout(900)     # 400ms slide + settle
    pg.mouse.move(0, 0)          # a click leaves the pointer hovering a day


# --------------------------------------------------------------------------
# 1 -- a container that already holds a shell must end up with exactly one
# --------------------------------------------------------------------------
# Reproduces snippets/gb-account-flatpickr-cal.liquid: the hidden input plus a
# static calendar, both inside .gb-acct-cal[data-acct-cal].
LIVE_SHAPE = """
()=>{
 const host=document.querySelector("[data-acct-cal]").parentElement;
 const root=document.createElement('div');
 root.className='gb-acct-cal';
 root.setAttribute('data-acct-cal','');
 root.innerHTML='<input class="gb-acct-sr flatpickr-input" type="text" data-acct-cal-input'
   +' aria-label="Choose a date" tabindex="-1">'
   +'<div class="flatpickr-calendar animate inline" data-probe-shell tabindex="-1"></div>';
 host.appendChild(root);
 const before={cals:root.querySelectorAll('.flatpickr-calendar').length,
               shell:root.querySelectorAll('[data-probe-shell]').length};
 const t=new Date(); t.setHours(0,0,0,0);
 const min=new Date(t.getFullYear(), t.getMonth(), t.getDate()+1);
 window.gumiAcct.cal._arm(root, min);
 return {before, after:{cals:root.querySelectorAll('.flatpickr-calendar').length,
                        shell:root.querySelectorAll('[data-probe-shell]').length,
                        armed:!!root._fp}};}
"""


def run_shell(b):
    pg = goto(b)
    r = pg.evaluate(LIVE_SHAPE)
    # Anchor: without these the assertions below pass on a container that never
    # had a shell in it -- which is exactly the static page's shape.
    check("probe really injected a shell", r["before"], {"cals": 1, "shell": 1})
    check("shell is gone after _arm", r["after"]["shell"], 0)
    check("exactly one calendar left", r["after"]["cals"], 1)
    check("flatpickr still armed the root", r["after"]["armed"], True)

    # And the three real roots are untouched by the change.
    check("three real roots, one calendar each", pg.evaluate(
        "[...document.querySelectorAll('[data-acct-cal]')]"
        ".filter(r=>!r.querySelector('[data-probe-shell]'))"
        ".every(r=>r.querySelectorAll('.flatpickr-calendar').length===1)"), True)
    pg.close()


# --------------------------------------------------------------------------
# 2 -- cursor on days that cannot be picked
# --------------------------------------------------------------------------
# ⚠ A prevMonthDay/nextMonthDay carries .flatpickr-disabled too, and its own
# rule (pointer-events: none) comes later, so only a disabled day of the OPEN
# month gets the cursor. The selector has to say so.
IN_MONTH = (".flatpickr-day.flatpickr-disabled"
            ":not(.prevMonthDay):not(.nextMonthDay)")


def run_cursor(b, panel, field):
    pg = goto(b, 390)
    open_cal(pg, panel, field)
    P = "[data-acct-modal-panel='%s'] " % panel
    tag = "[%s]" % panel

    # CSS, on a day the probe marks itself -- independent of what month is open.
    marked = pg.evaluate("""(p)=>{
      const d=document.querySelector(p+'.flatpickr-day:not(.flatpickr-disabled)'
        +':not(.prevMonthDay):not(.nextMonthDay)');
      if(!d) return null;
      d.classList.add('flatpickr-disabled');
      const c=getComputedStyle(d);
      const out={cursor:c.cursor, pe:c.pointerEvents, bg:c.backgroundColor};
      d.classList.remove('flatpickr-disabled');
      return out;}""", P)
    check(tag + " disabled day exists to mark", marked is not None, True)
    if marked:
        check(tag + " disabled day cursor", marked["cursor"], "not-allowed")
        check(tag + " disabled day keeps pointer events", marked["pe"], "auto")
        check(tag + " disabled day has no fill", marked["bg"], TRANSPARENT)

    # The overflow days must stay inert -- a click on one moves the month.
    over = pg.locator(P + ".flatpickr-day.prevMonthDay, "
                      + P + ".flatpickr-day.nextMonthDay")
    if over.count():
        check(tag + " overflow days stay inert", pg.eval_on_selector(
            P + ".flatpickr-day.prevMonthDay, " + P + ".flatpickr-day.nextMonthDay",
            "e=>getComputedStyle(e).pointerEvents"), "none")
    else:
        note(tag + " overflow days stay inert", "month fills the grid exactly")

    # Behaviour: dropping pointer-events is only safe if the plugin refuses the
    # click. Derived from today, so it does not rot.
    state = pg.evaluate("""(p)=>{
      const days=[...document.querySelectorAll(p+`""" + IN_MONTH.replace("`", "") + """`)];
      const head=document.querySelector(p+'.flatpickr-current-month .cur-month');
      const yr=document.querySelector(p+'.flatpickr-current-month .cur-year');
      const t=new Date();
      const openMonth=new Date(head.textContent.trim()+' 1, '+yr.value).getMonth();
      return {n:days.length, today:t.getDate(),
              sameMonth:openMonth===t.getMonth(),
              first:days.length?days[0].textContent:null};}""", P)

    if state["sameMonth"]:
        check(tag + " disabled days = days already past", state["n"], state["today"])
    else:
        note(tag + " disabled days = days already past",
             "view opened on the next month (today is its last day)")

    if state["n"]:
        before = pg.input_value("#" + field)
        pg.click(P + IN_MONTH, force=True)     # force: the plugin, not CSS, refuses it
        pg.wait_for_timeout(400)
        pg.mouse.move(0, 0)
        check(tag + " clicking a disabled day changes nothing",
              pg.input_value("#" + field), before)
        check(tag + " and selects nothing", pg.evaluate(
            "(p)=>document.querySelectorAll(p+'.flatpickr-day.selected').length", P), 0)
    else:
        note(tag + " clicking a disabled day changes nothing",
             "no disabled day on screen this month")
    pg.close()


with sync_playwright() as b_:
    b = b_.chromium.launch(executable_path=_chrome())
    run_shell(b)
    run_cursor(b, "edit-date", "acct-f-date")
    run_cursor(b, "restart", "acct-f-restart")
    b.close()

print("\n%d ok / %d red / %d skipped" % (ok, red, skip))
sys.exit(1 if red else 0)
