#!/usr/bin/env python3
"""Task 45 -- nine client-set spacing nudges, and what each one really moves.

Every value here is client-set, not board-derived, so the board references in
account.scss no longer justify them -- this file is the only record of what was
asked for. Each one is asserted twice: the declaration, and the pixel it moves.

⚠ Two of them are coupled and read wrong on their own:
  * `.gb-acct-row { margin-top: -1px }` is NOT phone-scoped, and it also lifts
    the FIRST row 1px off the body's padding. So the phone gap between rows is
    24 - 1 = 23, not 24.
  * `.gb-acct-sub__body` is also worn by the renewal schedule block
    (account.html:427, `.gb-acct-schedule` has no rules of its own), so the
    phone row-gap moves both. Asserted on both, deliberately.

The 1440 column is the reverse anchor: the desktop keeps 23.5 / `0 4px` / no
strip margin, so a rule that lost its `@include narrow` reads red here.

⚠ `.gb-acct-item__main`'s 12px padding is spent out of the name column, not out
of the row: at 390 the row was already at its column-gap, so the text box lost
the 12 instead. The name still fits on one line with 2px to spare -- that is
asserted, because a longer name there would start wrapping.
"""
import sys, pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
ok = red = 0


def check(label, got, want):
    global ok, red
    if got == want:
        print("ok   %-64s %s" % (label, got)); ok += 1
    else:
        print("RED  %-64s got %r want %r" % (label, got, want)); red += 1


def near(label, got, want, tol=0.6):
    check(label + " ~%s" % want, got is not None and abs(got - want) <= tol, True)


def _chrome():
    hits = sorted((pathlib.Path.home() / ".cache/ms-playwright").glob(
        "chromium-*/chrome-linux64/chrome"))
    if not hits:
        sys.exit("no chromium -- run: npx playwright install chromium")
    return str(hits[-1])


def goto(b, width, hash_="#detail"):
    pg = b.new_page(viewport={"width": width, "height": 950},
                    reduced_motion="no-preference")
    pg.goto((ROOT / "account.html").as_uri() + hash_)
    pg.wait_for_timeout(800)
    return pg


# Picks the bodies by what is on screen, not by a line number: the detail view
# hides rows per subscription state, and a hidden row has no usable rect.
MEAS = """
()=>{
 const cs=e=>getComputedStyle(e), R=e=>e.getBoundingClientRect();
 const vis=e=>e.offsetParent!==null;
 const view=document.querySelector("[data-acct-view='detail']");
 const bodies=[...view.querySelectorAll('.gb-acct-sub__body')].filter(vis);
 const plain=bodies.find(b=>!b.classList.contains('gb-acct-schedule'));
 const sched=bodies.find(b=>b.classList.contains('gb-acct-schedule'));
 const kids=[...plain.children].filter(vis);
 const isRow=e=>e.classList.contains('gb-acct-row');
 const rows=kids.filter(isRow);
 // ⚠ The rows are not all adjacent (an actions block and rules sit between
 // them), so the gap can only be measured across a real sibling pair.
 const pair=kids.findIndex((e,i)=>i&&isRow(e)&&isRow(kids[i-1]));
 const days=sched&&sched.querySelector('.gb-acct-schedule__days');
 const was=view.querySelector('.gb-acct-product__was');
 const now=view.querySelector('.gb-acct-product__now');
 return {
  bodyGap:cs(plain).rowGap, schedGap:sched?cs(sched).rowGap:null,
  rowMT:rows.length?cs(rows[0]).marginTop:null, rowCount:rows.length,
  // what the eye gets: row-gap minus the negative margin
  inkGap:pair>0?+(R(kids[pair]).top-R(kids[pair-1]).bottom).toFixed(2):null,
  // the side effect: the first row starts 1px above the body's content box
  firstOffset:rows.length?+(R(rows[0]).top
     -(R(plain).top+parseFloat(cs(plain).paddingTop))).toFixed(2):null,
  daysPad:days?cs(days).padding:null, daysMargin:days?cs(days).margin:null,
  // negative side margin: the strip reaches past the body's padding
  stripOut:days?+((R(sched).left+parseFloat(cs(sched).paddingLeft))
     -R(days).left).toFixed(2):null,
  nowML:now?cs(now).marginLeft:null,
  priceGap:(was&&now)?+(R(now).left-R(was).right).toFixed(2):null};}
"""


def run_detail(b, width, want_gap):
    pg = goto(b, width)
    tag = " @%d" % width
    r = pg.evaluate(MEAS)

    check("anchor: rows are on screen" + tag, r["rowCount"] >= 2, True)
    check("anchor: two rows are real siblings" + tag, r["inkGap"] is not None, True)
    check("sub__body row-gap" + tag, r["bodyGap"], want_gap)
    check("the schedule block shares it" + tag, r["schedGap"], want_gap)
    check(".gb-acct-row margin-top" + tag, r["rowMT"], "-1px")
    near("gap between rows = row-gap - 1" + tag, r["inkGap"],
         float(want_gap[:-2]) - 1)
    near("first row sits 1px above the body's content box" + tag,
         r["firstOffset"], -1)

    if width == 390:
        check("schedule strip padding" + tag, r["daysPad"], "0px")
        check("schedule strip margin" + tag, r["daysMargin"], "0px -3px")
        near("strip reaches 3px past the body padding" + tag, r["stripOut"], 3)
    else:
        check("schedule strip keeps its padding" + tag, r["daysPad"], "0px 4px")
        check("schedule strip has no margin" + tag, r["daysMargin"], "0px")
        near("strip stays inside the body padding" + tag, r["stripOut"], 0)

    check("product__now margin-left" + tag, r["nowML"], "2px")
    near("was -> now reads 2 gap + 2 margin" + tag, r["priceGap"], 4)
    pg.close()


ITEMS = """
()=>{
 const cs=e=>getComputedStyle(e), R=e=>e.getBoundingClientRect();
 const v=document.querySelector("[data-acct-view='order']");
 const it=v.querySelector('.gb-acct-item'), m=it.querySelector('.gb-acct-item__main');
 const t=m.querySelector('.gb-acct-item__text'), h=t.querySelector('.gb-acct-item__head');
 const tag=t.querySelector('.gb-acct-item__tag'), ns=h.querySelector('.gb-acct-item__names');
 const nm=ns.querySelector('.gb-acct-item__name'), fl=ns.querySelector('.gb-acct-item__flavour');
 const pr=it.querySelector('.gb-acct-item__prices');
 const rules=[...v.querySelectorAll('.gb-acct-rule')];
 const rule=rules[0], prev=rule.previousElementSibling, next=rule.nextElementSibling;
 return {mainPR:cs(m).paddingRight, textGap:cs(t).rowGap, namesGap:cs(ns).rowGap,
  ruleMT:cs(rule).marginTop, rules:rules.length,
  parentGap:cs(rule.parentElement).rowGap,
  gapAbove:+(R(rule).top-R(prev).bottom).toFixed(2),
  gapBelow:+(R(next).top-R(rule).bottom).toFixed(2),
  textInset:+(R(m).right-R(t).right).toFixed(2),
  headToTag:+(R(tag).top-R(h).bottom).toFixed(2),
  nameToFlav:+(R(fl).top-R(nm).bottom).toFixed(2),
  nameLines:nm.getClientRects().length,
  toPrices:+(R(pr).left-R(m).right).toFixed(2)};}
"""


def run_items(b, width):
    pg = goto(b, width, "#order")
    tag = " @%d" % width
    r = pg.evaluate(ITEMS)

    check("anchor: the order view drew its rules" + tag, r["rules"], 4)
    check("anchor: the items column still gaps 24" + tag, r["parentGap"], "24px")

    check("item__main padding-right" + tag, r["mainPR"], "12px")
    near("the text box ends 12 in from main's edge" + tag, r["textInset"], 12)
    check("the name still fits on one line" + tag, r["nameLines"], 1)

    check("item__text row-gap" + tag, r["textGap"], "8px")
    near("measured head -> tag" + tag, r["headToTag"], 8)
    check("item__names row-gap" + tag, r["namesGap"], "0px")
    near("name and flavour line boxes touch" + tag, r["nameToFlav"], 0)

    check("gb-acct-rule margin-top" + tag, r["ruleMT"], "-1px")
    near("the rule sits 1px up in the 24 column" + tag, r["gapAbove"], 23)
    near("and the gap below it is untouched" + tag, r["gapBelow"], 24)
    pg.close()


def run_reasons(b, width):
    pg = goto(b, width)
    pg.evaluate("()=>window.gumiAcct.modal.open('cancel-reason')")
    pg.wait_for_timeout(600)
    r = pg.evaluate("""()=>{
      const p=document.querySelector("[data-acct-modal-panel='cancel-reason']");
      const l=p.querySelector('.gb-acct-reasons');
      const rows=[...l.querySelectorAll('.gb-acct-reason')];
      const R=e=>e.getBoundingClientRect();
      return {n:rows.length, gap:getComputedStyle(l).rowGap,
              ink:rows.length>1?+(R(rows[1]).top-R(rows[0]).bottom).toFixed(2):null};}""")
    tag = " @%d" % width
    check("anchor: the reason rows are built" + tag, r["n"] >= 2, True)
    check("reasons row-gap" + tag, r["gap"], "12.5px")
    near("measured gap between two reason rows" + tag, r["ink"], 12.5)
    pg.close()


def run_calendar(b, width):
    pg = goto(b, width)
    pg.evaluate("()=>window.gumiAcct.modal.open('edit-date')")
    pg.wait_for_timeout(500)
    pg.click("#acct-f-date")
    pg.wait_for_timeout(900)
    pg.mouse.move(0, 0)
    r = pg.evaluate("""()=>{
      const c=document.querySelector("[data-acct-modal-panel='edit-date'] .flatpickr-calendar");
      if(!c) return null;
      const inner=c.querySelector('.flatpickr-rContainer')||c.querySelector('.dayContainer');
      const R=e=>e.getBoundingClientRect();
      return {pad:getComputedStyle(c).padding,
              inset:inner?+(R(inner).left-R(c).left).toFixed(2):null,
              w:+R(c).width.toFixed(1)};}""")
    tag = " @%d" % width
    check("anchor: the calendar is open" + tag, r is not None, True)
    if r:
        check("flatpickr-calendar padding" + tag, r["pad"], "20px 22px")
        near("the grid starts 22 in from the box" + tag, r["inset"], 22)
    pg.close()


with sync_playwright() as p_:
    b = p_.chromium.launch(executable_path=_chrome())
    run_detail(b, 1440, "23.5px")
    run_detail(b, 390, "24px")
    run_items(b, 1440)
    run_items(b, 390)
    run_reasons(b, 390)
    run_calendar(b, 390)
    run_calendar(b, 1440)
    b.close()

print("\n%d ok / %d red" % (ok, red))
sys.exit(1 if red else 0)
