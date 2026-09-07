# -*- coding: utf-8 -*-
"""Round 58 assertions (build r59) -- the cart drawer.

Boards: 341:42573 / 336:36516 filled, 341:42749 / 336:34942 empty.

Sections: mount, provenance (inline icons vs the exported source), geometry,
type, colour, empty state, behaviour, responsive.

Green against the current build; run tools/_reverse_r60.py first and it must go
red in bulk.
"""
import sys, json, os, re, io
from playwright.sync_api import sync_playwright

EXE = "/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome"
DIR = "/home/ly/project/Gumi-Brand/"
ROOT = "file://" + DIR
PAGES = ("index.html", "pdp.html", "science.html", "reviews.html",
         "how-gumi-works.html", "our-story.html", "faq.html",
         "get-in-touch.html", "referral.html", "privacy-policy.html",
         "shipping.html")

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


print("\n[mount] drawer + trigger on the 11 delivery pages")
for f in PAGES:
    s = io.open(DIR + f, encoding="utf-8").read()
    chk(f + " drawer present", s.count('id="gb-cart"'), 1)
    chk(f + " trigger wired", s.count('data-modal="gb-cart"'), 1)
    chk(f + " drawer before scripts",
        'id="gb-cart"' in s and s.index('id="gb-cart"') < s.index('assets/main.js'), True)
fc = io.open(DIR + "font-check.html", encoding="utf-8").read()
chk("font-check has no drawer", 'id="gb-cart"' in fc, False)
chk("font-check has no cart icon", 'aria-label="Cart"' in fc, False)


print("\n[provenance] inline icon paths come from the exported board assets")
ICONS = DIR + "figma/assets-raw/icons/"
idx = io.open(DIR + "index.html", encoding="utf-8").read()
if 'id="gb-cart"' in idx:
    cart_html = idx[idx.index('id="gb-cart"'):]
    cart_html = cart_html[:cart_html.index("</body>")]
else:
    cart_html = ""      # reversed state: every provenance assertion below goes red
for stem, n in (("desktop-cart-icon", 1), ("desktop-cart-icon-2", 1),
                ("desktop-cart-icon-3", 1), ("desktop-cart-icon-4", 2),
                ("desktop-cart-icon-5", 2),
                ("desktop-cart-icon-10", 1), ("desktop-cart-frame-1984078213", 2)):
    # r59: desktop-cart-icon-6 (the 16 chevron) is no longer inlined -- the
    # interval is a selectBox now and the module draws the arrow.
    src = io.open(ICONS + stem + ".svg", encoding="utf-8").read()
    d = re.findall(r'<path d="([^"]+)"', src)
    # guard: a missing/renamed export would make the count assertion vacuous
    chk("source %s has one path" % stem, len(d), 1)
    chk("%s used %dx verbatim" % (stem, n), cart_html.count(d[0]), n)
for m in ("visa", "mastercard", "applepay", "amex", "paypal"):
    a = io.open(ICONS + "desktop-cart-payment-method-%s.svg" % m, "rb").read()
    b = io.open(DIR + "images/pay-%s.svg" % m, "rb").read()
    chk("pay-%s byte-identical to export" % m, a == b, True)
chk("pay marks in board order",
    [m for m in re.findall(r'images/pay-(\w+)\.svg', cart_html)],
    ["visa", "mastercard", "applepay", "amex", "paypal"])


with sync_playwright() as p:
    b = p.chromium.launch(executable_path=EXE)

    def page(url, w, h=900, empty=False):
        pg = b.new_page(viewport={"width": w, "height": h})
        pg.goto(ROOT + url); pg.wait_for_timeout(500)
        if empty:
            pg.evaluate("()=>{const e=document.getElementById('gb-cart');"
                        "if(e) e.classList.add('is-empty');}")
        return pg

    def open_cart(pg):
        # Reversed state has no trigger: report it and let the assertions below
        # go red one by one instead of dying on the first click.
        try:
            pg.click(".gb-header__icon[data-modal='gb-cart']", timeout=2000)
        except Exception:
            chk("cart trigger clickable", False, True)
            return
        pg.wait_for_timeout(900)          # $t-drawer is 0.7s

    def box(pg, sel, props):
        r = pg.evaluate("""([s,ps])=>{const e=document.querySelector(s);
          if(!e) return null; const c=getComputedStyle(e), r=e.getBoundingClientRect();
          const o={w:Math.round(r.width*10)/10,h:Math.round(r.height*10)/10};
          ps.forEach(p=>o[p]=c[p]); return o;}""", [sel, props])
        # A missing element must fail every assertion made about it, not throw.
        if r is None:
            r = {"w": None, "h": None}
            r.update((k, None) for k in props)
        return r

    TYPE = ["fontSize", "fontWeight", "lineHeight", "letterSpacing", "color"]

    print("\n[geometry] panel + fixed chrome (1440)")
    pg = page("index.html", 1440)
    open_cart(pg)

    d = box(pg, ".gb-cart__panel", ["backgroundColor", "transform"])
    chk("panel width 391", d["w"], 391)
    chk("panel fills viewport height", d["h"], 900)
    chk("panel white", d["backgroundColor"], "rgb(255, 255, 255)")
    chk("panel slid home", d["transform"], "none")
    chk("panel pinned right",
        pg.evaluate("()=>{const e=document.querySelector('.gb-cart__panel');"
                    "return e?Math.round(innerWidth-e.getBoundingClientRect().right):null;}"), 0)

    d = box(pg, ".gb-cart__head", ["padding", "backgroundColor"])
    chk("head 48 high", d["h"], 48)
    chk("head padding", d["padding"], "12px 20px")
    chk("head cream", d["backgroundColor"], "rgb(250, 249, 248)")
    d = box(pg, ".gb-cart__title", TYPE)
    chk("title 16/400/24/-0.32", [d["fontSize"], d["fontWeight"], d["lineHeight"], d["letterSpacing"]],
        ["16px", "400", "24px", "-0.32px"])
    chk("title ink", d["color"], "rgb(1, 19, 7)")
    chk("close 24 square", [box(pg, ".gb-cart__close", [])["w"], box(pg, ".gb-cart__close", [])["h"]], [24, 24])

    d = box(pg, ".gb-cart__ship", ["padding", "backgroundColor", "gap"] + TYPE)
    chk("ship 48 high", d["h"], 48)
    chk("ship padding", d["padding"], "12px 20px")
    chk("ship lime-200", d["backgroundColor"], "rgb(218, 246, 176)")
    chk("ship gap 8", d["gap"], "8px")
    chk("ship 14/500/20", [d["fontSize"], d["fontWeight"], d["lineHeight"]], ["14px", "500", "20px"])
    chk("ship green-900", d["color"], "rgb(0, 65, 40)")

    d = box(pg, ".gb-cart__bar", ["padding", "gap", "boxShadow"])
    chk("bar 120 high", d["h"], 120)
    chk("bar padding", d["padding"], "16px 20px")
    chk("bar gap 12", d["gap"], "12px")
    chk("bar shadow", d["boxShadow"],
        "rgba(51, 49, 49, 0.05) 0px -4px 28px 0px, rgba(51, 49, 49, 0.01) 0px -4px 10px 0px")

    print("\n[geometry] line items")
    d = box(pg, ".gb-cart__lines", ["padding", "gap"])
    chk("lines padding", d["padding"], "24px 20px")
    chk("lines gap 24", d["gap"], "24px")
    chk("items count", pg.eval_on_selector_all(".gb-cart-item", "e=>e.length"), 2)
    chk("items no gap", box(pg, ".gb-cart__items", ["gap"])["gap"], "normal")
    d = box(pg, ".gb-cart-item", ["padding", "gap", "borderTopWidth", "borderTopColor"])
    chk("item padding", d["padding"], "23px 0px 24px")
    chk("item gap 19", d["gap"], "19px")
    chk("item rule 1px", d["borderTopWidth"], "1px")
    chk("item rule e6e6e6", d["borderTopColor"], "rgb(230, 230, 230)")
    chk("item 184 high", d["h"], 184)
    d = box(pg, ".gb-cart-item__media", [])
    chk("media 56 square", [d["w"], d["h"]], [56, 56])
    chk("main gap 16", box(pg, ".gb-cart-item__main", ["gap"])["gap"], "16px")
    chk("head gap 4", box(pg, ".gb-cart-item__head", ["gap"])["gap"], "4px")
    chk("row gap 15", box(pg, ".gb-cart-item__row", ["gap"])["gap"], "15px")
    d = box(pg, ".gb-cart-item__stepper", ["padding", "gap", "borderColor", "borderRadius", "borderWidth"])
    chk("stepper 102x40", [d["w"], d["h"]], [102, 40])
    chk("stepper padding", d["padding"], "9px 11px")
    chk("stepper gap 8", d["gap"], "8px")
    chk("stepper border 1px 808080", [d["borderWidth"], d["borderColor"]], ["1px", "rgb(128, 128, 128)"])
    chk("stepper radius 8", d["borderRadius"], "8px")
    d = box(pg, ".gb-cart-item__step", [])
    chk("step 16 square", [d["w"], d["h"]], [16, 16])
    d = box(pg, ".gb-cart-item__remove", [])
    chk("remove 18x20 (client r59, board 16)", [d["w"], d["h"]], [18, 20])
    d = box(pg, ".gb-cart-item__price", ["gap", "alignItems"])
    chk("price gap 6 (client r59, board 4)", d["gap"], "6px")
    chk("price baseline-bottom", d["alignItems"], "flex-end")
    chk("was struck", box(pg, ".gb-cart-item__was", ["textDecorationLine"])["textDecorationLine"], "line-through")
    chk("plan gap 4", box(pg, ".gb-cart-item__plan", ["gap"])["gap"], "4px")
    # r59: the interval is a drawn selectBox; measure the trigger, not the
    # native control it hides behind.
    chk("interval trigger gap 2",
        box(pg, ".gb-select--inline .gb-select__button", ["gap"])["gap"], "2px")

    print("\n[type + colour]")
    for sel, want in (
        (".gb-cart__sub",            ["16px", "400", "24px", "-0.32px", "rgb(1, 19, 7)"]),
        (".gb-cart-item__name",      ["14px", "400", "20px", "-0.28px", "rgb(1, 19, 7)"]),
        (".gb-cart-item__variant",   ["14px", "400", "20px", "-0.28px", "rgb(102, 102, 102)"]),
        (".gb-cart-item__count",     ["14px", "400", "20px", "-0.28px", "rgb(26, 26, 26)"]),
        (".gb-cart-item__was",       ["12px", "400", "20px", "normal", "rgb(102, 102, 102)"]),
        (".gb-cart-item__now",       ["14px", "400", "20px", "normal", "rgb(1, 19, 7)"]),
        (".gb-cart-item__plan",      ["14px", "400", "20px", "-0.28px", "rgb(102, 102, 102)"]),
        (".gb-select--inline .gb-select__button", ["14px", "500", "20px", "normal", "rgb(3, 116, 165)"]),
        (".gb-cart__gift-name",      ["14px", "400", "20px", "-0.28px", "rgb(1, 19, 7)"]),
        (".gb-cart__gift-text",      ["12px", "400", "18px", "-0.24px", "rgb(102, 102, 102)"]),
        (".gb-cart__sum",            ["14px", "400", "20px", "normal", "rgb(102, 102, 102)"]),
        (".gb-cart__grand-row",      ["14px", "500", "20px", "normal", "rgb(1, 19, 7)"]),
        (".gb-cart__pay-note",       ["12px", "400", "18px", "normal", "rgb(102, 102, 102)"]),
        (".gb-cart__continue",       ["14px", "400", "20px", "normal", "rgb(3, 116, 165)"]),
        (".gb-cart__bar-total",      ["16px", "500", "24px", "normal", "rgb(1, 19, 7)"]),
    ):
        d = box(pg, sel, TYPE)
        chk(sel.replace(".gb-cart", "") + " type", [d[k] for k in TYPE], want)
    chk("count min-width 30", box(pg, ".gb-cart-item__count", ["minWidth"])["minWidth"], "30px")
    chk("continue underlined",
        box(pg, ".gb-cart__continue", ["textDecorationLine"])["textDecorationLine"], "underline")

    print("\n[geometry] gift + totals + checkout")
    d = box(pg, ".gb-cart__gift", ["padding", "gap", "backgroundColor", "borderColor", "borderRadius"])
    # board says 16 with an INSIDE stroke, so the CSS pad gives the border back
    chk("gift padding 15 + 1 border", d["padding"], "15px")
    chk("gift gap 16", d["gap"], "16px")
    chk("gift sand", d["backgroundColor"], "rgb(245, 241, 233)")
    chk("gift border f3f3f3", d["borderColor"], "rgb(243, 243, 243)")
    chk("gift radius 8", d["borderRadius"], "8px")
    d = box(pg, ".gb-cart__gift-media", [])
    chk("gift media 47 square", [d["w"], d["h"]], [47, 47])
    chk("gift body gap 10 (client r59, board 8)",
        box(pg, ".gb-cart__gift-body", ["gap"])["gap"], "10px")
    d = box(pg, ".gb-cart__totals", ["padding", "gap"])
    chk("totals padding", d["padding"], "24px 20px")
    chk("totals gap 24", d["gap"], "24px")
    chk("sums gap 8", box(pg, ".gb-cart__sums", ["gap"])["gap"], "8px")
    chk("sum rows", pg.eval_on_selector_all(".gb-cart__sum", "e=>e.length"), 3)
    chk("sum-pair gap 19", box(pg, ".gb-cart__sum-pair", ["gap"])["gap"], "19px")
    chk("grand gap 16", box(pg, ".gb-cart__grand", ["gap"])["gap"], "16px")
    chk("pay gap 16", box(pg, ".gb-cart__pay", ["gap"])["gap"], "16px")
    d = box(pg, ".gb-cart__pay-marks", ["gap"])
    chk("marks gap 7", d["gap"], "7px")
    chk("marks span 203", d["w"], 203)
    chk("marks count", pg.eval_on_selector_all(".gb-cart__pay-marks img", "e=>e.length"), 5)
    chk("marks 35x24", pg.evaluate(
        "()=>{const e=document.querySelector('.gb-cart__pay-marks img'); if(!e) return null;"
        "const i=e.getBoundingClientRect(); return [Math.round(i.width),Math.round(i.height)];}"), [35, 24])
    d = box(pg, ".gb-cart__checkout", ["padding", "backgroundColor", "color", "borderRadius",
                                       "textTransform", "letterSpacing", "lineHeight", "fontSize"])
    chk("checkout 52 high", d["h"], 52)
    chk("checkout fills bar", d["w"], 351)
    chk("checkout padding", d["padding"], "0px 64px")
    chk("checkout green", d["backgroundColor"], "rgb(0, 86, 53)")
    chk("checkout white", d["color"], "rgb(255, 255, 255)")
    chk("checkout pill", d["borderRadius"], "999px")
    chk("checkout capitalize", d["textTransform"], "capitalize")
    chk("checkout 16/28/.48", [d["fontSize"], d["lineHeight"], d["letterSpacing"]], ["16px", "28px", "0.48px"])
    chk("bar-pair gap 6", box(pg, ".gb-cart__bar-pair", ["gap"])["gap"], "6px")
    chk("bar-was struck", box(pg, ".gb-cart__bar-was", ["textDecorationLine"])["textDecorationLine"], "line-through")

    print("\n[copy] strings are the board's")
    # textContent, not innerText: the empty state is display:none in this state
    txt = pg.evaluate("()=>{const e=document.getElementById('gb-cart');"
                      "return e?e.textContent:'';}")
    for s in ("Your Cart", "Spend another $20 for FREE Delivery", "Subscribe & Save",
              "Superfood Greens Gummies", "28 Packs", "Delivers every", "4 Weeks",
              "One Time Purchase", "Gift Name Here", "FREE", "Subtotal", "Discount",
              "Automatic", "-$15", "Shipping", "Calculated at checkout", "Total",
              "Discount codes applied at checkout", "Continue Shopping",
              "Secure Checkout", "Oops! Your cart is empty", "Shop Now"):
        chk("copy %r" % s, s in txt, True)
    chk("gift description in full",
        "This here is a gift description that can go over two lines or even possibly three lines depending on what it says." in txt, True)

    print("\n[behaviour] open / close / lock")
    pg2 = page("index.html", 1440)
    st = pg2.evaluate("""()=>{const e=document.getElementById('gb-cart');
      if(!e) return {vis:null,aria:null,open:null,tx:null};
      const pn=document.querySelector('.gb-cart__panel');
      return {vis:getComputedStyle(e).visibility, aria:e.getAttribute('aria-hidden'),
              open:e.classList.contains('is-open'),
              tx:pn&&getComputedStyle(pn).transform};}""")
    chk("starts hidden", st["vis"], "hidden")
    chk("starts aria-hidden", st["aria"], "true")
    chk("starts off-canvas", st["tx"] != "none", True)
    open_cart(pg2)
    st = pg2.evaluate("""()=>{const e=document.getElementById('gb-cart');
      if(!e) return {vis:null,aria:null,open:null,lockH:null,lockB:null,focus:null,scrim:null,exit:null};
      const ov=document.querySelector('.gb-cart__overlay');
      return {vis:getComputedStyle(e).visibility, aria:e.getAttribute('aria-hidden'),
              open:e.classList.contains('is-open'),
              lockH:document.documentElement.classList.contains('is-modal-open'),
              lockB:document.body.classList.contains('is-modal-open'),
              focus:document.activeElement.id,
              scrim:ov&&getComputedStyle(ov).backgroundColor,
              exit:getComputedStyle(e).getPropertyValue('--modal-exit').trim()};}""")
    chk("open sets is-open", st["open"], True)
    chk("open clears aria-hidden", st["aria"], "false")
    chk("open visible", st["vis"], "visible")
    chk("locks html", st["lockH"], True)
    chk("locks body", st["lockB"], True)
    chk("focus moves to dialog", st["focus"], "gb-cart")
    chk("scrim 0.5 black", st["scrim"], "rgba(0, 0, 0, 0.5)")
    chk("scrim faded in", pg2.evaluate(
        "()=>{const e=document.querySelector('.gb-cart__overlay');"
        "return e?getComputedStyle(e).opacity:null;}"), "1")
    chk("--modal-exit declared", st["exit"], "0.7s")
    # Both scroll containers must be registered in smoothScroll.PREVENT, or Lenis
    # eats the wheel and the drawer's contents cannot be scrolled at all.
    chk("scroll areas opt out of Lenis", pg2.evaluate(
        "()=>['.gb-cart__body','.gb-cart__empty'].map(s=>{const e=document.querySelector(s);"
        "return e?e.hasAttribute('data-lenis-prevent'):null;})"), [True, True])
    pg2.keyboard.press("Escape"); pg2.wait_for_timeout(900)
    shut = "()=>{const e=document.getElementById('gb-cart'); return e?!e.classList.contains('is-open'):null;}"
    chk("Esc closes", pg2.evaluate(shut), True)
    chk("Esc unlocks", pg2.evaluate("()=>document.documentElement.classList.contains('is-modal-open')"), False)
    open_cart(pg2)
    pg2.evaluate("()=>{const e=document.querySelector('.gb-cart__overlay'); if(e) e.click();}"); pg2.wait_for_timeout(900)
    chk("scrim click closes", pg2.evaluate(shut), True)
    open_cart(pg2)
    pg2.evaluate("()=>{const e=document.querySelector('.gb-cart__continue'); if(e) e.click();}"); pg2.wait_for_timeout(900)
    chk("Continue Shopping closes", pg2.evaluate(shut), True)

    print("\n[scrim] the page really does dim")
    from PIL import Image
    import io as _io
    def rgb(pg, x, y):
        shot = pg.screenshot(clip={"x": x, "y": y, "width": 2, "height": 2})
        return Image.open(_io.BytesIO(shot)).convert("RGB").getpixel((0, 0))
    pgs = page("index.html", 1440, 768)
    # backgroundColor is the same string whether the overlay is faded in or not,
    # so read what is actually painted over the page.
    lit = rgb(pgs, 400, 400)
    open_cart(pgs)
    dim = rgb(pgs, 400, 400)
    chk("page dims to 50%", dim, tuple(round(c * 0.5) for c in lit))
    chk("scrim covers the viewport", pgs.evaluate(
        "()=>{const r=document.querySelector('.gb-cart__overlay').getBoundingClientRect();"
        "return [r.width,r.height,r.x,r.y];}"), [1440, 768, 0, 0])
    pgs.close()

    print("\n[empty] second state")
    # The hook is a state class, like `is-open`. Pinned here so the judge above
    # cannot keep passing against a stylesheet that has moved to something else.
    css = io.open(DIR + "assets/customstyle.css", encoding="utf-8").read()
    chk("empty state hooks on .is-empty", ".gb-cart.is-empty" in css, True)
    chk("no data-cart hook left", "data-cart" in css, False)
    pg3 = page("index.html", 1440, empty=True)
    open_cart(pg3)
    st = pg3.evaluate("""()=>{const q=s=>document.querySelector(s);
      const d=s=>{const e=q(s); return e?getComputedStyle(e).display:'missing';};
      const co=q('.gb-cart__checkout');
      if(!co) return {body:'missing',ship:'missing',tot:'missing',empty:'missing',
                      bg:null,fg:null,pe:null,bc:null};
      const ck=getComputedStyle(co);
      return {body:d('.gb-cart__body'), ship:d('.gb-cart__ship'), tot:d('.gb-cart__bar-total'),
              empty:d('.gb-cart__empty'), bg:ck.backgroundColor, fg:ck.color,
              pe:ck.pointerEvents, bc:ck.borderTopColor};}""")
    chk("empty hides lines", st["body"], "none")
    chk("empty hides ship bar", st["ship"], "none")
    chk("empty hides bar total", st["tot"], "none")
    chk("empty shows placeholder", st["empty"], "flex")
    chk("checkout disabled fill", st["bg"], "rgb(230, 230, 230)")
    chk("checkout disabled label", st["fg"], "rgb(128, 128, 128)")
    chk("checkout disabled border", st["bc"], "rgb(230, 230, 230)")
    chk("checkout not clickable", st["pe"], "none")
    d = box(pg3, ".gb-cart__empty", ["padding", "gap", "alignItems"])
    chk("empty padding", d["padding"], "32px 20px")
    chk("empty gap 44", d["gap"], "44px")
    chk("empty centred", d["alignItems"], "center")
    chk("empty head gap 24", box(pg3, ".gb-cart__empty-head", ["gap"])["gap"], "24px")
    d = box(pg3, ".gb-cart__empty-title", TYPE + ["textAlign"])
    chk("empty title 20/500/24", [d["fontSize"], d["fontWeight"], d["lineHeight"]], ["20px", "500", "24px"])
    chk("empty title centred", d["textAlign"], "center")
    d = box(pg3, ".gb-cart__shop", ["padding", "letterSpacing", "backgroundColor"])
    chk("shop 44 high", d["h"], 44)
    chk("shop fills", d["w"], 351)
    chk("shop padding", d["padding"], "0px 40px")
    chk("shop tracking -0.32", d["letterSpacing"], "-0.32px")
    chk("shop green", d["backgroundColor"], "rgb(0, 86, 53)")
    chk("cards gap 12", box(pg3, ".gb-cart__cards", ["gap"])["gap"], "12px")
    chk("two cards", pg3.eval_on_selector_all(".gb-cart__cards .gb-nav-card", "e=>e.length"), 2)
    d = box(pg3, ".gb-cart__cards .gb-nav-card", ["padding", "borderRadius", "fontSize", "lineHeight", "letterSpacing"])
    chk("card 169 high on desktop viewport", d["h"], 169)
    chk("card padding 16", d["padding"], "16px")
    chk("card radius 8", d["borderRadius"], "8px")
    chk("card 12/18/-0.24", [d["fontSize"], d["lineHeight"], d["letterSpacing"]], ["12px", "18px", "-0.24px"])
    d = box(pg3, ".gb-cart__cards .gb-nav-card__action", [])
    chk("card action 32", [d["w"], d["h"]], [32, 32])
    art = ("()=>{const e=document.querySelector('.gb-cart__cards .gb-nav-card__art');"
           "return e?getComputedStyle(e).display:null;}")
    chk("card art shown while open", pg3.evaluate(art), "block")
    pg4 = page("index.html", 1440, empty=True)
    chk("card art still gated when shut", pg4.evaluate(art), "none")

    print("\n[responsive] panel width + no sideways overflow")
    for w, want in ((1440, 391), (1281, 391), (1280, 391), (992, 391), (768, 391), (767, 767), (575, 575), (390, 390)):
        pgx = page("index.html", w, 800)
        open_cart(pgx)
        chk("panel %d -> %d" % (w, want), box(pgx, ".gb-cart__panel", [])["w"], want)
        chk("no h-overflow at %d" % w,
            pgx.evaluate("()=>document.documentElement.scrollWidth<=innerWidth"), True)
        chk("scroll area is the body at %d" % w, pgx.evaluate(
            "()=>{const e=document.querySelector('.gb-cart__body');"
            "return e?getComputedStyle(e).overflowY:null;}"), "auto")
        pgx.close()

    b.close()

print("\n%d ok / %d red" % (ok, bad))
sys.exit(1 if bad else 0)
