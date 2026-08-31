# -*- coding: utf-8 -*-
"""Round 55 assertions (build r57) -- the client's follow-up ruling.

  I (closed)  .gb-promo-card__list: centred on pc, NOT centred on phones
              -- withdrawn from r56, back to r51. Covered by r56check's AQ
              section and by r40check / r52check; not repeated here.
  AV          the phone field's country code is the same drawn control, in its
              `bare` variant (no box of its own), on get-in-touch + referral

Green against the current build; run tools/_reverse_r57.py first and it must go
red in bulk.
"""
import sys, json
from playwright.sync_api import sync_playwright

EXE = "/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome"
ROOT = "file:///home/ly/project/Gumi-Brand/"
PAGES = ("get-in-touch.html", "referral.html")

ok = bad = 0
def chk(label, got, want, tol=None):
    global ok, bad
    if tol is not None:
        good = got is not None and abs(got - want) <= tol
        detail = "%s ~ %s (+-%s)" % (got, want, tol)
    else:
        good = got == want
        detail = "%s == %s" % (json.dumps(got, ensure_ascii=False), json.dumps(want, ensure_ascii=False))
    if good: ok += 1
    else:
        bad += 1
        print("  RED  %-56s %s" % (label, detail))

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=EXE)

    def page(url, w, h=900):
        pg = b.new_page(viewport={"width": w, "height": h})
        pg.goto(ROOT + url); pg.wait_for_timeout(600)
        pg.evaluate("()=>document.querySelectorAll('.wowo').forEach(e=>e.classList.add('animated'))")
        pg.wait_for_timeout(200)
        return pg

    print("\n[AV] country code drawn as the same widget, bare variant")
    for f in PAGES:
        pg = page(f, 1440)

        d = pg.evaluate("""()=>{const ph=document.querySelector('.gb-field__phone');
          if(!ph) return null;
          const w=ph.querySelector('.gb-select'), n=ph.querySelector('select');
          const btn=ph.querySelector('.gb-select__button'), li=ph.querySelector('.gb-select__list');
          const cb=btn&&getComputedStyle(btn), cn=n&&getComputedStyle(n);
          return {wrap:!!w, bare:w&&w.classList.contains('gb-select--bare'),
            cls:btn&&btn.className, tag:btn&&btn.tagName, type:btn&&btn.type,
            aria:btn&&btn.getAttribute('aria-label'),
            labelledby:btn?btn.getAttribute('aria-labelledby'):'X',
            listAria:li&&li.getAttribute('aria-label'),
            text:btn&&btn.textContent.trim(),
            fs:cb&&cb.fontSize, lh:cb&&cb.lineHeight, ls:cb&&cb.letterSpacing, col:cb&&cb.color,
            bw:cb&&cb.borderTopWidth, bg:cb&&cb.backgroundColor, bi:cb&&cb.backgroundImage,
            pr:cb&&cb.paddingRight, gap:cb&&cb.columnGap,
            nName:n&&n.getAttribute('name'), nOpts:n?n.options.length:0,
            nTab:n&&n.getAttribute('tabindex'), nDisp:cn&&cn.display,
            nW:n?+n.getBoundingClientRect().width.toFixed(1):null,
            liN:li?li.children.length:0,
            liText:li?[].map.call(li.children,e=>e.textContent):[],
            natives:n?[].map.call(n.options,o=>o.text):[],
            role:li&&li.getAttribute('role'), lenis:li&&li.hasAttribute('data-lenis-prevent'),
            arrow:!!(btn&&btn.querySelector('.gb-select__arrow'))};}""")
        chk("%s  wrapper built" % f, bool(d and d["wrap"]), True)
        # Without this the pre-round liveness run dies on the first missing node
        # instead of reporting the rest as red.
        if not (d and d["wrap"]):
            for lbl in ("trigger classes", "typography", "aria", "native carrier",
                        "list", "open by click", "geometry", "stacking",
                        "focus-within", "escape", "form value", "overflow"):
                chk("%s  %s (widget absent)" % (f, lbl), False, True)
            pg.close()
            continue
        chk("%s  bare variant" % f, d and d["bare"], True)
        # a bare trigger must NOT carry the field-box classes: the phone field
        # already draws the border, a second 44px white box inside it would show
        chk("%s  trigger carries no field-box classes" % f, d["cls"], "gb-select__button")
        chk("%s  trigger is a button" % f, d["tag"], "BUTTON")
        chk("%s  type=button" % f, d["type"], "button")
        chk("%s  no border of its own" % f, d["bw"], "0px")
        chk("%s  transparent" % f, d["bg"], "rgba(0, 0, 0, 0)")
        chk("%s  no painted chevron left" % f, d["bi"], "none")
        chk("%s  chevron is an element" % f, d["arrow"], True)
        # typography must match what .gb-field__phone select had
        chk("%s  font-size 16" % f, d["fs"], "16px")
        chk("%s  line-height 24" % f, d["lh"], "24px")
        chk("%s  letter-spacing -0.32" % f, d["ls"], "-0.32px")
        chk("%s  colour gray-700" % f, d["col"], "rgb(77, 77, 77)")
        # the native drew a 20 chevron inside padding-right:23 -> 3 of clear space
        chk("%s  padding-right 0" % f, d["pr"], "0px")
        chk("%s  gap 3" % f, d["gap"], "3px")
        # no <label for> on this control, so the aria-label has to be carried over
        chk("%s  aria-label carried to the button" % f, d["aria"], "Country code")
        chk("%s  aria-label carried to the list" % f, d["listAria"], "Country code")
        chk("%s  no dangling aria-labelledby" % f, d["labelledby"], None)
        chk("%s  shows the selected option" % f, d["text"], "AU")
        # the native control is still the form's value carrier
        chk("%s  native kept, name=country" % f, d["nName"], "country")
        chk("%s  native out of the tab order" % f, d["nTab"], "-1")
        chk("%s  native visually-hidden, not display:none" % f, d["nDisp"] != "none", True)
        chk("%s  native is 1px" % f, d["nW"], 1.0, 0.5)
        chk("%s  one li per option" % f, d["liN"], d["nOpts"])
        chk("%s  option text mirrors the native" % f, d["liText"], d["natives"])
        chk("%s  role=listbox" % f, d["role"], "listbox")
        chk("%s  list opts out of Lenis" % f, d["lenis"], True)

        # open it
        pg.click(".gb-field__phone .gb-select__button"); pg.wait_for_timeout(350)
        d = pg.evaluate("""()=>{const ph=document.querySelector('.gb-field__phone');
          const w=ph.querySelector('.gb-select'), li=ph.querySelector('.gb-select__list');
          const btn=ph.querySelector('.gb-select__button'), a=ph.querySelector('.gb-select__arrow');
          const pb=ph.getBoundingClientRect(), lb=li.getBoundingClientRect();
          const bb=btn.getBoundingClientRect(), cl=getComputedStyle(li);
          const hit=document.elementFromPoint(lb.left+lb.width/2, lb.top+lb.height/2);
          return {open:w.classList.contains('is-open'), vis:cl.visibility, op:cl.opacity,
            rot:getComputedStyle(a).transform,
            gapFromField:+(lb.top-pb.bottom).toFixed(2),
            leftOnTrigger:+(lb.left-bb.left).toFixed(2),
            widerThanTrigger: lb.width >= bb.width - 0.5,
            onTop: hit ? (hit.className||hit.tagName) : null,
            fieldBorder:getComputedStyle(ph).borderTopColor,
            focus:document.activeElement===li};}""")
        chk("%s  click opens it" % f, d["open"], True)
        chk("%s  list visible" % f, d["vis"], "visible")
        chk("%s  chevron rotated" % f, d["rot"], "matrix(-1, 0, 0, -1, 0, 0)")
        # it hangs off the FIELD's bottom edge, not off the 24px trigger inside it
        chk("%s  4 clear of the field's bottom edge" % f, d["gapFromField"], 4.0, 0.6)
        chk("%s  left-aligned to the trigger" % f, d["leftOnTrigger"], 0.0, 0.6)
        chk("%s  list is at least as wide as the trigger" % f, d["widerThanTrigger"], True)
        # the open list has to win over whatever field follows it
        chk("%s  the open list is the top layer" % f, "gb-select__option" in (d["onTop"] or ""), True)
        # focus is inside the phone box, so the box itself must read as focused
        chk("%s  field border goes green (focus-within)" % f, d["fieldBorder"], "rgb(0, 86, 53)")
        chk("%s  focus moves to the listbox" % f, d["focus"], True)

        # Escape closes and hands focus back
        pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
        d = pg.evaluate("""()=>{const ph=document.querySelector('.gb-field__phone');
          const fd=document.querySelector('form');
          return {open:ph.querySelector('.gb-select').classList.contains('is-open'),
            focus:document.activeElement===ph.querySelector('.gb-select__button'),
            posted:new FormData(fd).get('country')};}""")
        chk("%s  Escape closes" % f, d["open"], False)
        chk("%s  Escape returns focus to the trigger" % f, d["focus"], True)
        chk("%s  the form still posts country" % f, d["posted"], "AU")
        pg.close()

        # no horizontal overflow with the list open, at every tier
        for w in (320, 390, 767, 768, 1024, 1440):
            p2 = page(f, w)
            p2.click(".gb-field__phone .gb-select__button"); p2.wait_for_timeout(300)
            over = p2.evaluate("()=>document.documentElement.scrollWidth - document.documentElement.clientWidth")
            chk("%s %d  open list causes no h-overflow" % (f, w), over <= 1, True)
            p2.close()

    # two widgets on one page must not drive each other
    print("\n[AV] the two widgets on get-in-touch are independent")
    pg = page("get-in-touch.html", 1440)
    if not pg.query_selector(".gb-field__phone .gb-select__button"):
        for lbl in ("country opens alone", "outside click closes it", "two boxes"):
            chk(lbl + " (widget absent)", False, True)
        pg.close(); b.close()
        print("\n%d ok / %d red" % (ok, bad)); sys.exit(1)
    pg.click(".gb-field__phone .gb-select__button"); pg.wait_for_timeout(300)
    d = pg.evaluate("""()=>({country:document.querySelector('.gb-field__phone .gb-select').classList.contains('is-open'),
      enquiry:document.getElementById('enquiry').closest('.gb-select').classList.contains('is-open')})""")
    chk("opening country leaves enquiry closed", [d["country"], d["enquiry"]], [True, False])
    pg.click("#enquiry-button"); pg.wait_for_timeout(300)
    d = pg.evaluate("""()=>({country:document.querySelector('.gb-field__phone .gb-select').classList.contains('is-open'),
      enquiry:document.getElementById('enquiry').closest('.gb-select').classList.contains('is-open')})""")
    chk("opening enquiry closes country (outside click)", [d["country"], d["enquiry"]], [False, True])
    chk("two independent boxes registered",
        pg.evaluate("()=>window.gumi.selectBox.boxes.length"), 2)
    pg.close()

    b.close()

print("\n%d ok / %d red" % (ok, bad))
sys.exit(1 if bad else 0)
