#!/usr/bin/env python3
"""Task 39 -- view-swap motion, greeting centring, order head, phone dots, refer card.

Everything here is geometry or a live animation, so it is read out of a browser:

  * the view swap is a one-shot @keyframes on a class that JS strips again, so
    the only honest reading is getAnimations() on the element right after the
    click -- it carries the resolved duration AND which properties the keyframes
    actually animate, which is what "drop the opacity on the phone" means.
  * justify-content, a missing row-gap and a dropped align-items all read as
    positions, not as declarations: asserting the property would pass just as
    well with a later rule winning. Each one is pinned by the distance it moves,
    with an anchor proving the distance could have been non-zero.
  * ⚠ reduced_motion must be set explicitly -- headless defaults collapse every
    duration and the motion section would read green on a dead animation
    (HANDOFF §5, the Task 8/31/33 false-green).
"""
import sys, pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent

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


def num(v):
    """A missing pseudo reads 'auto', which must land as a red, not a crash."""
    try:
        return float(str(v).rstrip("%").rstrip("px"))
    except ValueError:
        return v


def near(label, got, want, tol):
    check("%s (~%s)" % (label, want),
          isinstance(got, (int, float)) and abs(got - want) <= tol, True)
    if not isinstance(got, (int, float)):
        print("     value was %r" % (got,))


# --------------------------------------------------------------------------
# 1 -- the view swap: slower, and the phone slide no longer fades
# --------------------------------------------------------------------------
READ_ANIM = """
()=>{const el=document.querySelector('.gb-acct__view.is-entering');
 if(!el)return 'no view';
 const a=el.getAnimations();
 if(!a.length)return 'no animation';
 const e=a[0].effect;
 const skip=['offset','computedOffset','easing','composite'];
 const props=[...new Set(e.getKeyframes().flatMap(k=>Object.keys(k)))]
   .filter(k=>skip.indexOf(k)<0).sort();
 return [a[0].animationName, e.getTiming().duration, props]}
"""


def run_motion(b, width, name, props):
    ctx = b.new_context(viewport={"width": width, "height": 900},
                        reduced_motion="no-preference")
    pg = ctx.new_page()
    pg.goto((ROOT / "account.html").as_uri())
    pg.wait_for_timeout(500)
    tag = "@%d" % width

    nav = ".gb-acct-nav" if width > 767 else ".gb-acct-list"
    # anchor: without a live animation the two assertions below read 'no animation'
    pg.click(nav + " [data-acct-goto='orders']")
    got = pg.evaluate(READ_ANIM)
    check("%s view swap animation is live" % tag, isinstance(got, list), True)
    if isinstance(got, list):
        check("%s keyframes" % tag, got[0], name)
        check("%s duration ms" % tag, got[1], 500)
        check("%s animated properties" % tag, got[2], props)
    ctx.close()


# --------------------------------------------------------------------------
# 2 -- greeting centres in its fixed 136
# --------------------------------------------------------------------------
HELLO = """
()=>{const h=document.querySelector('.gb-acct-hello');
 const t=h.querySelector('.gb-acct-hello__title');
 const s=h.querySelector('.gb-acct-hello__sub');
 const c=getComputedStyle(h),b=h.getBoundingClientRect();
 const r=n=>Math.round(n*100)/100;
 return [r(t.getBoundingClientRect().top-(b.top+parseFloat(c.paddingTop))),
         r((b.bottom-parseFloat(c.paddingBottom))-s.getBoundingClientRect().bottom)]}
"""

HEAD = """
()=>{const h=document.querySelector('.gb-acct-order__head');
 const l=h.querySelector('.gb-acct-order__label').getBoundingClientRect();
 const s=h.querySelector('.gb-acct-order__status').getBoundingClientRect();
 return [getComputedStyle(h).flexDirection, Math.round((s.top-l.bottom)*100)/100]}
"""

REFER = """
()=>{const f=document.querySelector('.gb-acct-refer');
 const a=f.querySelector('.gb-acct-refer__action').getBoundingClientRect();
 const y=f.querySelector('.gb-acct-refer__body').getBoundingClientRect();
 const c=getComputedStyle(f),b=f.getBoundingClientRect();
 const r=n=>Math.round(n*100)/100;
 return [r(a.top-(b.top+parseFloat(c.paddingTop))), r(y.height-a.height),
         getComputedStyle(document.querySelector('.gb-acct-refer__text')).paddingTop]}
"""

DOTS = """
()=>{const rows=[...document.querySelectorAll('.gb-acct-list__link')];
 if(!rows.length)return 'no rows';
 const seen=rows.map(e=>{const c=getComputedStyle(e,'::before');
   return c.width+'|'+c.height+'|'+c.backgroundColor+'|'+c.borderTopLeftRadius});
 const el=rows[0],g=document.createRange();g.selectNodeContents(el);
 return [rows.length, [...new Set(seen)],
   Math.round((g.getBoundingClientRect().left-el.getBoundingClientRect().left)*100)/100]}
"""


def run_layout(b, width):
    pg = b.new_page(viewport={"width": width, "height": 950})
    pg.goto((ROOT / "account.html").as_uri())
    pg.wait_for_timeout(500)
    pg.mouse.move(0, 0)
    tag = "@%d" % width

    hello = pg.evaluate(HELLO)
    if width > 767:
        # anchor: the box really is taller than its text, so "equal" is a result
        check("%s greeting has spare room to split" % tag, hello[0] > 5, True)
        check("%s greeting is centred in the 136" % tag, hello[0] == hello[1], True)
    else:
        # phone drops the card: min-height 0, nothing to centre
        check("%s phone greeting has no spare room" % tag, hello, [0, 0])

    head = pg.evaluate(HEAD)
    if width > 767:
        check("%s order head stays on one row" % tag, head[0], "row")
    else:
        check("%s order head stacks" % tag, head[0], "column")
        check("%s order head rows touch" % tag, head[1], 0)

    refer = pg.evaluate(REFER)
    # 27780 centres the arrow, 27639 tops it out -- one board each way
    check("%s refer arrow offset" % tag, refer[0],
          0 if width <= 767 else round(refer[1] / 2, 2))
    check("%s refer body is taller than the arrow" % tag, refer[1] > 20, True)
    check("%s refer text padding-top" % tag, refer[2],
          "3px" if width <= 767 else "0px")

    dots = pg.evaluate(DOTS)
    if width > 767:
        # the rail keeps the dot Task 34 added -- a later "dedupe" that moves it
        # to a shared rule must not drop this one
        rail = pg.eval_on_selector(
            ".gb-acct-nav__link", "e=>getComputedStyle(e,'::before').width")
        near("%s rail dot width" % tag, num(rail), 16.67, 0.02)
    else:
        check("%s phone card rows" % tag, dots[0], 6)
        check("%s every phone row draws one identical dot" % tag,
              len(dots[1]), 1)
        w, h, bg, r = dots[1][0].split("|")
        # 'auto' is what an absent ::before reads as -- without this the line
        # above would still pass, all six rows being identically empty
        check("%s phone rows have a ::before at all" % tag, w != "auto", True)
        near("%s phone dot width" % tag, num(w), 16.67, 0.02)
        near("%s phone dot height" % tag, num(h), 16.67, 0.02)
        check("%s phone dot colour" % tag, bg, "rgb(217, 217, 217)")
        check("%s phone dot is round" % tag, r, "50%")
        # 16 padding + 20 slot + 12 gap. Range excludes the pseudo, so this is
        # the label's own left edge.
        near("%s phone label starts at 48" % tag, dots[2], 48, 0.2)
    pg.close()


with sync_playwright() as p:
    br = p.chromium.launch(executable_path=str(_chrome()))
    run_motion(br, 1440, "gb-acct-view-in", ["opacity", "transform"])
    run_motion(br, 390, "gb-acct-view-in-right", ["transform"])
    for w in (1440, 390):
        run_layout(br, w)
    br.close()

print("\n%d ok / %d red" % (ok, red))
sys.exit(1 if red else 0)
