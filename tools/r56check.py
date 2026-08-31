# -*- coding: utf-8 -*-
"""Round 54 assertions (build r56) -- the three items that were held for a ruling.

  AQ  .gb-promo-card__list keeps `margin: 0 auto` at every width (reverses r51)
  AR  .gb-promo-panel is full-screen on phones only; 768-1280 shows the 390x744
      phone board as a floating card
  AS  the enquiry <select> is drawn as a button + ul listbox with a rotating chevron

Green against the current build; run tools/_reverse_r56.py first and it must go
red in bulk. A one-way green script can be a script that verified nothing.
"""
import sys, json
from playwright.sync_api import sync_playwright

EXE = "/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome"
ROOT = "file:///home/ly/project/Gumi-Brand/"

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

    # ================================================================== AQ
    print("\n[AQ] .gb-promo-card__list: centred on pc, NOT centred on phones (r57 final)")
    # This has flipped twice. r51 dropped the auto left margin below 768 so the
    # parent's align-items centres the box and the 15 on the right pushes it 7.5
    # left -- the board's "hangs slightly left of centre". r56 briefly made it
    # dead centre at every width; r57 withdrew that on the client's final answer.
    # r57 also zeroes margin-left in the TABLET tier, which r51 did not: one auto
    # margin against a fixed one absorbs the slack the other way and hung this
    # tier RIGHT (768 measured +30.7, 1280 +43.7).
    CENTRE = """()=>{const l=document.querySelector('.gb-promo-card--white .gb-promo-card__list');
      if(!l) return null; const p=l.parentElement;
      const a=l.getBoundingClientRect(), b=p.getBoundingClientRect(), c=getComputedStyle(p);
      const left=b.left+parseFloat(c.paddingLeft), right=b.right-parseFloat(c.paddingRight);
      const cl=getComputedStyle(l);
      return {off:+(((a.left+a.right)/2)-((left+right)/2)).toFixed(2),
              ml:cl.marginLeft, mr:parseFloat(cl.marginRight)};}"""
    ramp = {}
    for w in (320, 390, 575, 767, 768, 900, 1024, 1280, 1281, 1440):
        pg = page("pdp.html", w)
        d = pg.evaluate(CENTRE)
        ramp[w] = d
        if w <= 767:
            chk("%d  hangs 7.5 left of centre (board)" % w, d["off"], -7.5, 0.6)
            chk("%d  margin-left dropped" % w, d["ml"], "0px")
            chk("%d  margin-right 15" % w, d["mr"], 15.0, 0.1)
        elif w <= 1280:
            chk("%d  margin-left dropped here too (r57)" % w, d["ml"], "0px")
            # the box is centred by align-items minus half the right margin
            chk("%d  offset is exactly -mr/2" % w, d["off"], -d["mr"] / 2.0, 0.6)
        else:
            chk("%d  centred on pc" % w, d["off"], 0.0, 0.6)
            chk("%d  both margins auto" % w, d["ml"] == "0px", False)
        pg.close()

    # the ramp itself: monotonic 15 -> 0, and continuous at both tier edges
    mrs = [ramp[w]["mr"] for w in (768, 900, 1024, 1280)]
    chk("AQ  tablet ramp is monotonic 15 -> 0", all(a >= b for a, b in zip(mrs, mrs[1:])), True)
    chk("AQ  767/768 continuous", abs(ramp[767]["off"] - ramp[768]["off"]) < 0.6, True)
    chk("AQ  1280/1281 continuous", abs(ramp[1280]["off"] - ramp[1281]["off"]) < 1.0, True)
    chk("AQ  no tier hangs right", max(ramp[w]["off"] for w in ramp) <= 0.6, True)

    # ================================================================== AR
    print("\n[AR] promo panel: full-screen on phones, 390x744 card from 768 up")
    PANEL = """()=>{const m=document.getElementById('promo-modal');
      window.gumi.modal.open(m);
      const pa=m.querySelector('.gb-promo-panel'), wr=m.querySelector('.gb-promo-modal__wrap');
      const r=pa.getBoundingClientRect(), c=getComputedStyle(pa), cw=getComputedStyle(wr);
      return {w:+r.width.toFixed(1), h:+r.height.toFixed(1),
              radius:c.borderTopLeftRadius, pad:cw.paddingTop,
              cx:+((r.left+r.right)/2).toFixed(1), vw:window.innerWidth, vh:window.innerHeight,
              dir:c.flexDirection};}"""
    for w in (320, 390, 575, 767):
        pg = page("index.html", w); d = pg.evaluate(PANEL)
        chk("%d  panel fills the viewport width" % w, d["w"], float(d["vw"]), 0.6)
        chk("%d  panel fills the viewport height" % w, d["h"], float(d["vh"]), 0.6)
        chk("%d  no radius" % w, d["radius"], "0px")
        chk("%d  wrap has no gutter" % w, d["pad"], "0px")
        chk("%d  stacked" % w, d["dir"], "column")
        pg.close()

    for w in (768, 900, 1024, 1280):
        pg = page("index.html", w); d = pg.evaluate(PANEL)
        chk("%d  card is the phone board's 390 wide" % w, d["w"], 390.0, 0.6)
        chk("%d  card is the phone board's 744 tall" % w, d["h"], 744.0, 0.6)
        chk("%d  radius 24" % w, d["radius"], "24px")
        chk("%d  wrap gutter 24" % w, d["pad"], "24px")
        chk("%d  centred" % w, d["cx"], d["vw"] / 2.0, 0.6)
        chk("%d  still the stacked layout" % w, d["dir"], "column")
        pg.close()

    for w in (1281, 1440):
        pg = page("index.html", w); d = pg.evaluate(PANEL)
        chk("%d  desktop card untouched (w)" % w, d["w"], 1062.0, 0.6)
        chk("%d  desktop card untouched (h)" % w, d["h"], 528.0, 0.6)
        chk("%d  two columns" % w, d["dir"], "row")
        pg.close()

    # the pinned card's wave has to be pinned with it
    WAVE = """()=>{const a=document.querySelector('.gb-promo-panel__art');
      const mk=v=>{const e=document.createElement('div'); e.style.width=v; a.appendChild(e);
        const w=e.getBoundingClientRect().width; e.remove(); return +w.toFixed(2);};
      return {scw:mk('var(--sc-w)'), pwr:mk('var(--pw-r)')};}"""
    for w in (390, 768, 900, 1024, 1280):
        pg = page("index.html", w); d = pg.evaluate(WAVE)
        chk("%d  wave pitch on the phone board's 144.85" % w, d["scw"], 144.63, 0.5)
        chk("%d  wave radius on the phone board's 92.65" % w, d["pwr"], 92.66, 0.5)
        pg.close()
    pg = page("index.html", 1440); d = pg.evaluate(WAVE)
    chk("1440  desktop column has no wave to pin", d["scw"], 302.19, 0.5)
    pg.close()

    # short viewport: the cap has to give, not overflow the gutter
    pg = page("index.html", 1024, 600); d = pg.evaluate(PANEL)
    chk("1024x600  height clipped to the gutter", d["h"], 600 - 48.0, 1.0)
    pg.close()

    # ================================================================== AS
    print("\n[AS] enquiry select drawn as button + ul listbox")
    pg = page("get-in-touch.html", 1440)

    d = pg.evaluate("""()=>{const n=document.getElementById('enquiry');
      const wrap=n.closest('.gb-select'), btn=wrap&&wrap.querySelector('.gb-select__button');
      const list=wrap&&wrap.querySelector('.gb-select__list');
      const cn=getComputedStyle(n), cl=list&&getComputedStyle(list);
      return {wrap:!!wrap, tag:n.tagName, nDisp:cn.display, nW:+n.getBoundingClientRect().width.toFixed(1),
        nTab:n.getAttribute('tabindex'),
        btnTag:btn&&btn.tagName, btnType:btn&&btn.type, pop:btn&&btn.getAttribute('aria-haspopup'),
        exp:btn&&btn.getAttribute('aria-expanded'), label:btn&&btn.getAttribute('aria-labelledby'),
        text:btn&&btn.querySelector('.gb-select__value').textContent,
        listTag:list&&list.tagName, role:list&&list.getAttribute('role'),
        lenis:list&&list.hasAttribute('data-lenis-prevent'),
        n_opts:list?list.children.length:0, n_native:n.options.length,
        texts:list?[].map.call(list.children,e=>e.textContent):[],
        natives:[].map.call(n.options,o=>o.text),
        roles:list?[].every.call(list.children,e=>e.getAttribute('role')==='option'):false,
        vis:cl&&cl.visibility, op:cl&&cl.opacity};}""")
    chk("wrapper built", d["wrap"], True)
    chk("native select still in the DOM", d["tag"], "SELECT")
    chk("native hidden visually, NOT display:none", d["nDisp"] != "none", True)
    chk("native is 1px (visually-hidden)", d["nW"], 1.0, 0.5)
    chk("native out of the tab order", d["nTab"], "-1")
    chk("trigger is a real button", d["btnTag"], "BUTTON")
    chk("button type=button (never submits)", d["btnType"], "button")
    chk("aria-haspopup", d["pop"], "listbox")
    chk("aria-expanded starts false", d["exp"], "false")
    chk("button is labelled", bool(d["label"]), True)
    chk("button shows the selected option", d["text"], "Contact Us")
    chk("list is a ul", d["listTag"], "UL")
    chk("role=listbox", d["role"], "listbox")
    chk("list opts out of Lenis", d["lenis"], True)
    chk("one li per native option", d["n_opts"], d["n_native"])
    chk("option text mirrors the native control", d["texts"], d["natives"])
    chk("every child is role=option", d["roles"], True)
    chk("list starts hidden", d["vis"], "hidden")
    chk("list starts transparent", d["op"], "0")

    # Every assertion below needs the widget to exist. Without this guard the
    # pre-round liveness run dies on the first missing node instead of reporting.
    if not d["wrap"]:
        for lbl in ("chevron", "open by click", "choose by click", "keyboard",
                    "escape / outside click", "label", "prefill", "overflow"):
            chk("AS  " + lbl + " (widget absent)", False, True)
        pg.close(); b.close()
        print("\n%d ok / %d red" % (ok, bad)); sys.exit(1)

    # arrow: it must be an element that can rotate, and it must animate
    d = pg.evaluate("""()=>{const a=document.querySelector('#enquiry-button .gb-select__arrow');
      const c=getComputedStyle(a);
      return {tag:a.tagName.toLowerCase(), t:c.transform, tp:c.transitionProperty, td:c.transitionDuration};}""")
    chk("chevron is an element, not a background", d["tag"], "svg")
    chk("chevron unrotated when closed", d["t"], "none")
    chk("chevron transitions transform", "transform" in d["tp"], True)
    chk("chevron transition has a duration", d["td"] != "0s", True)

    # open by click
    pg.click("#enquiry-button"); pg.wait_for_timeout(350)
    d = pg.evaluate("""()=>{const w=document.getElementById('enquiry').closest('.gb-select');
      const l=w.querySelector('.gb-select__list'), a=w.querySelector('.gb-select__arrow');
      const cl=getComputedStyle(l);
      return {open:w.classList.contains('is-open'),
        exp:w.querySelector('.gb-select__button').getAttribute('aria-expanded'),
        vis:cl.visibility, op:cl.opacity, rot:getComputedStyle(a).transform,
        focus:document.activeElement===l, act:l.getAttribute('aria-activedescendant'),
        below:+(l.getBoundingClientRect().top - w.querySelector('.gb-select__button').getBoundingClientRect().bottom).toFixed(1)};}""")
    chk("click opens it", d["open"], True)
    chk("aria-expanded flips", d["exp"], "true")
    chk("list visible", d["vis"], "visible")
    chk("list opaque", d["op"], "1")
    chk("chevron rotated 180", d["rot"], "matrix(-1, 0, 0, -1, 0, 0)")
    chk("focus moves to the listbox", d["focus"], True)
    chk("activedescendant is the selected option", d["act"], "enquiry-opt-0")
    chk("list hangs below the button", d["below"], 4.0, 1.0)

    # choose by click
    pg.click("#enquiry-opt-2"); pg.wait_for_timeout(350)
    d = pg.evaluate("""()=>{const n=document.getElementById('enquiry'), w=n.closest('.gb-select');
      const f=new FormData(document.querySelector('[data-prefill-enquiry]'));
      return {val:n.value, text:w.querySelector('.gb-select__value').textContent,
        open:w.classList.contains('is-open'),
        rot:getComputedStyle(w.querySelector('.gb-select__arrow')).transform,
        sel:w.querySelectorAll('[aria-selected="true"]').length,
        selIdx:[].findIndex.call(w.querySelectorAll('.gb-select__option'),e=>e.getAttribute('aria-selected')==='true'),
        posted:f.get('enquiry'),
        focus:document.activeElement===w.querySelector('.gb-select__button')};}""")
    chk("native value follows the click", d["val"], "press")
    chk("button text follows the click", d["text"], "Press Inquiries")
    chk("list closes on choose", d["open"], False)
    chk("chevron unrotates", d["rot"], "none")
    chk("exactly one aria-selected", d["sel"], 1)
    chk("aria-selected is on the chosen option", d["selIdx"], 2)
    chk("the form still posts the value", d["posted"], "press")
    chk("focus returns to the button", d["focus"], True)

    # keyboard: open, move, commit
    pg.evaluate("()=>document.getElementById('enquiry-button').focus()")
    pg.keyboard.press("ArrowDown"); pg.wait_for_timeout(300)
    chk("ArrowDown on the button opens it",
        pg.evaluate("()=>document.getElementById('enquiry').closest('.gb-select').classList.contains('is-open')"), True)
    pg.keyboard.press("ArrowDown"); pg.wait_for_timeout(120)
    chk("ArrowDown moves the active option",
        pg.evaluate("()=>document.getElementById('enquiry-list').getAttribute('aria-activedescendant')"),
        "enquiry-opt-3")
    pg.keyboard.press("Home"); pg.wait_for_timeout(120)
    chk("Home jumps to the first",
        pg.evaluate("()=>document.getElementById('enquiry-list').getAttribute('aria-activedescendant')"),
        "enquiry-opt-0")
    pg.keyboard.press("Enter"); pg.wait_for_timeout(300)
    d = pg.evaluate("""()=>({val:document.getElementById('enquiry').value,
      open:document.getElementById('enquiry').closest('.gb-select').classList.contains('is-open'),
      focus:document.activeElement===document.getElementById('enquiry-button')})""")
    chk("Enter commits the active option", d["val"], "contact")
    chk("Enter closes", d["open"], False)
    chk("Enter returns focus to the button", d["focus"], True)

    # Escape and outside-click both close
    pg.keyboard.press("ArrowDown"); pg.wait_for_timeout(250)
    pg.keyboard.press("Escape"); pg.wait_for_timeout(250)
    d = pg.evaluate("""()=>({open:document.getElementById('enquiry').closest('.gb-select').classList.contains('is-open'),
      focus:document.activeElement===document.getElementById('enquiry-button')})""")
    chk("Escape closes", d["open"], False)
    chk("Escape returns focus", d["focus"], True)

    pg.click("#enquiry-button"); pg.wait_for_timeout(250)
    pg.click(".gb-form__submit", position={"x": 5, "y": 5}, force=True)
    pg.wait_for_timeout(250)
    chk("a click outside closes",
        pg.evaluate("()=>document.getElementById('enquiry').closest('.gb-select').classList.contains('is-open')"), False)
    pg.close()

    # the label still drives the control
    pg = page("get-in-touch.html", 1440)
    d = pg.evaluate("""()=>{const l=document.querySelector('.gb-field__label[for="enquiry"]');
      const lab=[].find.call(document.querySelectorAll('.gb-field__label'),e=>e.textContent.indexOf('Enquiry')===0);
      return {stale:!!l, id:lab&&lab.id};}""")
    chk("label no longer points at the hidden control", d["stale"], False)
    chk("label has an id for aria-labelledby", d["id"], "enquiry-label")
    pg.click("text=Enquiry Type*"); pg.wait_for_timeout(200)
    chk("clicking the label focuses the button",
        pg.evaluate("()=>document.activeElement===document.getElementById('enquiry-button')"), True)
    pg.close()

    # enquiryPrefill still lands, and it lands on the drawn control too
    pg = page("get-in-touch.html?type=careers", 1440)
    d = pg.evaluate("""()=>({val:document.getElementById('enquiry').value,
      text:document.getElementById('enquiry-button').querySelector('.gb-select__value').textContent})""")
    chk("?type= still preselects the native control", d["val"], "careers")
    chk("?type= shows through on the button", d["text"], "Careers")
    pg.close()

    # (the phone field's country code was left native in r54 and drawn in r55 --
    #  its own assertions live in r57check)
    pg = page("get-in-touch.html", 1440)
    # no horizontal overflow at any tier with the widget in place
    for w in (320, 390, 767, 768, 1024, 1440):
        p2 = page("get-in-touch.html", w)
        p2.click("#enquiry-button"); p2.wait_for_timeout(300)
        over = p2.evaluate("()=>document.documentElement.scrollWidth - document.documentElement.clientWidth")
        chk("%d  open list causes no h-overflow" % w, over <= 1, True)
        p2.close()
    pg.close()

    b.close()

print("\n%d ok / %d red" % (ok, bad))
sys.exit(1 if bad else 0)
