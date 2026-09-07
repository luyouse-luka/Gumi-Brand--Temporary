# -*- coding: utf-8 -*-
"""Round 59 assertions (build r60) -- the client's five follow-ups.

  1  .gb-promo-panel keeps the two-column layout from 768 up (closes AT)
  2  .gb-cart-item__interval opens a dropdown
  6  .gb-cart__lines pads 26/20 on phones

Items 3-5 (remove 18x20, price gap 6, gift-body gap 10) overrode board values
that r60check already asserts; those assertions were updated in place there
rather than duplicated here.

Green against the current build; run tools/_reverse_r61.py first and it must go
red in bulk.
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
        print("  RED  %-58s %s" % (label, detail))


with sync_playwright() as p:
    b = p.chromium.launch(executable_path=EXE)

    def page(url, w, h=900):
        pg = b.new_page(viewport={"width": w, "height": h})
        pg.goto(ROOT + url); pg.wait_for_timeout(500)
        return pg

    def open_cart(pg):
        pg.click(".gb-header__icon[data-modal='gb-cart']", timeout=3000)
        pg.wait_for_timeout(900)

    print("\n[1] promo panel: row from 768 up, scaled as one piece")
    # 1110 is the first width that fits 1062 inside the wrap's two 24 gutters,
    # so the factor is 1 from there on and a fraction below it.
    for w, row, k in ((390, False, 1.0), (767, False, 1.0),
                      (768, True, 720 / 1062.0), (900, True, 852 / 1062.0),
                      (1024, True, 976 / 1062.0), (1109, True, 1061 / 1062.0),
                      (1110, True, 1.0), (1280, True, 1.0), (1281, True, 1.0),
                      (1440, True, 1.0), (1920, True, 1.0)):
        pg = page("index.html", w, 900)
        pg.evaluate("()=>document.getElementById('promo-modal').classList.add('is-open')")
        pg.wait_for_timeout(450)
        d = pg.evaluate("""()=>{const pn=document.querySelector('.gb-promo-panel');
          if(!pn) return null;
          const c=getComputedStyle(pn), r=pn.getBoundingClientRect();
          const art=document.querySelector('.gb-promo-panel__art');
          const ct=document.querySelector('.gb-promo-panel__content');
          const dv=document.querySelector('.gb-promo-panel__divider');
          const ab=getComputedStyle(art,'::before').content;
          return {dir:c.flexDirection, zoom:parseFloat(c.zoom),
                  w:Math.round(r.width), h:Math.round(r.height),
                  art:Math.round(art.getBoundingClientRect().width),
                  content:Math.round(ct.getBoundingClientRect().width),
                  divider:getComputedStyle(dv).display,
                  wave:ab,
                  ovX:document.documentElement.scrollWidth>innerWidth};}""")
        if d is None:
            chk("panel present at %d" % w, False, True); pg.close(); continue
        chk("%d direction" % w, d["dir"], "row" if row else "column")
        chk("%d zoom" % w, d["zoom"], k, tol=0.002)
        chk("%d no h-overflow" % w, d["ovX"], False)
        if row:
            # the card's own numbers never change; only the factor does
            chk("%d panel box" % w, [d["w"], d["h"]],
                [round(1062 * k), round(528 * k)])
            # tol 1: at 1109 the factor puts the column on 530.5
            chk("%d art column" % w, d["art"], 531 * k, tol=1)
            chk("%d content column" % w, d["content"], 531 * k, tol=1)
            chk("%d fits the gutters" % w, d["w"] <= w - 48 + 1, True)
            chk("%d seam drawn" % w, d["divider"], "block")
            chk("%d phone wave off" % w, d["wave"], "none")
        else:
            chk("%d full bleed" % w, [d["w"], d["h"]], [w, 900])
            chk("%d seam hidden" % w, d["divider"], "none")
            chk("%d phone wave on" % w, d["wave"] != "none", True)
        pg.close()

    print("\n[2] delivery interval is a drawn dropdown")
    pg = page("index.html", 1440, 900)
    open_cart(pg)
    d = pg.evaluate("""()=>{const ws=[...document.querySelectorAll('.gb-cart .gb-select--inline')];
      return {n:ws.length,
        natives:ws.map(w=>{const s=w.querySelector('select');
          return {cls:s.className, hidden:s.classList.contains('gb-select__native'),
                  opts:[...s.options].map(o=>o.text), sel:s.options[s.selectedIndex].text,
                  aria:s.getAttribute('aria-label')};}),
        labels:ws.map(w=>w.querySelector('.gb-select__value').textContent),
        roles:ws.map(w=>{const b=w.querySelector('.gb-select__button'),
                          l=w.querySelector('.gb-select__list');
          return [b.getAttribute('aria-haspopup'), b.getAttribute('aria-expanded'),
                  l.getAttribute('role'), l.hasAttribute('data-lenis-prevent')];})};}""")
    chk("two drawn intervals", d["n"], 2)
    OPTS = ["One Time Purchase", "2 Weeks", "4 Weeks", "6 Weeks", "8 Weeks"]
    # Reversed state has no drawn control: every assertion below has to go red
    # on its own rather than the run dying here.
    MISSING = {"opts": None, "hidden": None, "cls": "", "sel": None, "aria": None}
    while len(d["natives"]) < 2: d["natives"].append(dict(MISSING))
    while len(d["labels"]) < 2: d["labels"].append(None)
    while len(d["roles"]) < 2: d["roles"].append(None)
    for i in (0, 1):
        chk("item%d options" % i, d["natives"][i]["opts"], OPTS)
        chk("item%d native hidden" % i, d["natives"][i]["hidden"], True)
        chk("item%d keeps its class" % i,
            "gb-cart-item__interval" in d["natives"][i]["cls"], True)
        chk("item%d aria-label" % i,
            d["natives"][i]["aria"], "Delivery interval for Superfood Greens Gummies")
        chk("item%d listbox wiring" % i, d["roles"][i],
            ["listbox", "false", "listbox", True])
    chk("item0 selected", d["natives"][0]["sel"], "4 Weeks")
    chk("item1 selected", d["natives"][1]["sel"], "One Time Purchase")
    chk("triggers show the selection", d["labels"], ["4 Weeks", "One Time Purchase"])

    t = pg.evaluate("""()=>{const b=document.querySelector('.gb-cart .gb-select--inline .gb-select__button');
      if(!b) return {fs:null,fw:null,lh:null,ls:null,col:null,gap:null,pr:null,
                     arrow:null,stroke:null};
      const c=getComputedStyle(b), a=b.querySelector('.gb-select__arrow');
      const ar=a.getBoundingClientRect();
      return {fs:c.fontSize, fw:c.fontWeight, lh:c.lineHeight, ls:c.letterSpacing,
              col:c.color, gap:c.gap, pr:c.paddingRight,
              arrow:[Math.round(ar.width),Math.round(ar.height)],
              stroke:getComputedStyle(a.querySelector('path')).stroke};}""")
    chk("trigger 14/500/20", [t["fs"], t["fw"], t["lh"]], ["14px", "500", "20px"])
    chk("trigger untracked", t["ls"], "normal")
    chk("trigger blue", t["col"], "rgb(3, 116, 165)")
    chk("trigger gap 2", t["gap"], "2px")
    chk("trigger has no box padding", t["pr"], "0px")
    chk("arrow 16 square", t["arrow"], [16, 16])
    chk("arrow follows the text", t["stroke"], "rgb(3, 116, 165)")

    # choosing writes through to the real control
    pg.eval_on_selector_all(".gb-cart .gb-select--inline .gb-select__button", "e=>{if(e[0])e[0].click()}")
    pg.wait_for_timeout(400)
    pg.eval_on_selector_all(".gb-cart .gb-select--inline .gb-select__option", "e=>{if(e[4])e[4].click()}")
    pg.wait_for_timeout(400)
    d = pg.evaluate("""()=>{const w=document.querySelector('.gb-cart .gb-select--inline');
      if(!w) return {label:null, native:null, open:null};
      return {label:w.querySelector('.gb-select__value').textContent,
              native:w.querySelector('select').value,
              open:w.classList.contains('is-open')};}""")
    chk("choosing updates the trigger", d["label"], "8 Weeks")
    chk("choosing writes to the native control", d["native"], "8 Weeks")
    chk("choosing closes the list", d["open"], False)

    # keyboard
    pg.eval_on_selector_all(".gb-cart .gb-select--inline .gb-select__button", "e=>{if(e[1])e[1].focus()}")
    pg.keyboard.press("ArrowDown"); pg.wait_for_timeout(350)
    chk("ArrowDown opens", pg.evaluate(
        "()=>{const w=document.querySelectorAll('.gb-cart .gb-select--inline')[1];"
        "return w?w.classList.contains('is-open'):null;}"), True)
    pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
    chk("Escape closes the list, not the drawer", pg.evaluate(
        """()=>{const w=document.querySelectorAll('.gb-cart .gb-select--inline')[1];
          return [w?w.classList.contains('is-open'):null,
                  document.getElementById('gb-cart').classList.contains('is-open')];}"""), [False, True])
    pg.close()

    print("\n[2b] the list flips up rather than being clipped")
    for vh in (1000, 900, 768, 700, 640, 560):
        pg = page("index.html", 1440, vh)
        open_cart(pg)
        for i in (0, 1):
            pg.eval_on_selector_all(".gb-cart .gb-select--inline .gb-select__button",
                                    "(e,i)=>{if(e[i])e[i].click()}", i)
            pg.wait_for_timeout(400)
            d = pg.evaluate("""(i)=>{const w=document.querySelectorAll('.gb-cart .gb-select--inline')[i];
              if(!w) return {over:null, under:null, up:null};
              const l=w.querySelector('.gb-select__list');
              const body=document.querySelector('.gb-cart__body');
              const lr=l.getBoundingClientRect(), br=body.getBoundingClientRect();
              return {over:Math.round(Math.max(0,lr.bottom-br.bottom)),
                      under:Math.round(Math.max(0,br.top-lr.top)),
                      up:w.classList.contains('is-up')};}""", i)
            chk("vh%d item%d not clipped below" % (vh, i), d["over"], 0)
            chk("vh%d item%d not clipped above" % (vh, i), d["under"], 0)
            pg.keyboard.press("Escape"); pg.wait_for_timeout(250)
        pg.close()

    print("\n[2c] the two older selects are unchanged")
    pg = page("get-in-touch.html", 1440, 900)
    d = pg.evaluate("""()=>{const out={};
      const e=document.querySelector('#enquiry-button');
      const c=document.querySelector('.gb-field__phone .gb-select__button');
      out.enquiryBoxed = e ? e.classList.contains('gb-field__input') : null;
      out.enquiryArrow = e ? getComputedStyle(e.querySelector('.gb-select__arrow path')).stroke : null;
      out.countryArrow = c ? getComputedStyle(c.querySelector('.gb-select__arrow path')).stroke : null;
      out.enquiryWrap = e ? e.closest('.gb-select').className : null;
      return out;}""")
    chk("enquiry still draws its box", d["enquiryBoxed"], True)
    chk("enquiry arrow still 4d4d4d", d["enquiryArrow"], "rgb(77, 77, 77)")
    chk("country arrow still 4d4d4d", d["countryArrow"], "rgb(77, 77, 77)")
    chk("enquiry wrap has no variant", d["enquiryWrap"], "gb-select")
    pg.close()

    print("\n[6] cart lines pad 26/20 on phones")
    for w, want in ((1440, "24px 20px"), (768, "24px 20px"),
                    (767, "26px 20px"), (390, "26px 20px")):
        pg = page("index.html", w, 900)
        open_cart(pg)
        chk("lines padding at %d" % w, pg.evaluate(
            "()=>{const e=document.querySelector('.gb-cart__lines');"
            "return e?getComputedStyle(e).padding:null;}"), want)
        pg.close()

    b.close()

print("\n%d ok / %d red" % (ok, bad))
sys.exit(1 if bad else 0)
