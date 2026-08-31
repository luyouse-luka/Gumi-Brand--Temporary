# -*- coding: utf-8 -*-
"""Round 56 assertions (build r58) -- the white card's vertical scallop hangs out.

  .gb-promo-card--white .gb-promo-card__lip--v: left -63 -> -100, i.e. 26 of the
  126-wide box bites into the cream half instead of the symmetric 63. Untiered on
  purpose: the lip is display:none below 768, so this one declaration covers every
  tier that paints it. The green card and the phone tier's horizontal lip are the
  control group -- they must not move.

Green against the current build; run tools/_reverse_r58.py first and it must go red.
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

GEO = """()=>{const out={};
  for (const [k,sel] of [['white','.gb-promo-card--white'],['green','.gb-promo-card--green']]) {
    const c=document.querySelector(sel); if(!c){out[k]=null;continue;}
    const half=c.querySelector('.gb-promo-card__art, .gb-promo-card__media');
    const v=half.querySelector('.gb-promo-card__lip--v');
    const h=half.querySelector('.gb-promo-card__lip--h');
    const cb=c.getBoundingClientRect(), hb=half.getBoundingClientRect();
    const vb=v.getBoundingClientRect(), cv=getComputedStyle(v);
    const hh=h.getBoundingClientRect(), ch=getComputedStyle(h);
    out[k]={card:+cb.width.toFixed(1), half:+hb.width.toFixed(1),
      vDisp:cv.display, vW:+vb.width.toFixed(1),
      // how deep the scallop bites into the half it sits in
      vBite:+(k==='white' ? vb.right-hb.left : hb.right-vb.left).toFixed(1),
      // it must stay inside the card, which is overflow:hidden
      vInsideCard:(vb.left>=cb.left-0.5 && vb.right<=cb.right+0.5),
      hDisp:ch.display, hBite:+(hb.bottom-hh.top).toFixed(1), hBottom:ch.bottom};
  }
  return out;}"""

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=EXE)

    def page(url, w, h=1000):
        pg = b.new_page(viewport={"width": w, "height": h})
        pg.goto(ROOT + url); pg.wait_for_timeout(600)
        pg.evaluate("()=>document.querySelectorAll('.wowo').forEach(e=>e.classList.add('animated'))")
        pg.wait_for_timeout(250)
        return pg

    print("\n[r58] white card's vertical scallop: 26 of 126 inside, every tier that paints it")
    for w in (768, 900, 1024, 1200, 1280, 1440):
        pg = page("pdp.html", w); d = pg.evaluate(GEO)
        chk("%d  white bite 26" % w, d["white"]["vBite"], 26.0, 0.6)
        chk("%d  the lip box is still the board's 126" % w, d["white"]["vW"], 126.0, 0.6)
        chk("%d  white lip stays inside the card" % w, d["white"]["vInsideCard"], True)
        # control group: the green card was set in r52 and must not move
        chk("%d  green bite still 31 (r52, untouched)" % w, d["green"]["vBite"], 31.0, 0.6)
        chk("%d  green lip stays inside the card" % w, d["green"]["vInsideCard"], True)
        pg.close()

    # the value is deliberately untiered -- prove it really is one value, not a ramp
    pg = page("pdp.html", 768); a = pg.evaluate(GEO); pg.close()
    pg = page("pdp.html", 1440); z = pg.evaluate(GEO); pg.close()
    chk("bite does not drift between 768 and 1440", a["white"]["vBite"], z["white"]["vBite"], 0.1)

    print("\n[r58] the phone tier is NOT affected (it draws the horizontal lip)")
    for w in (320, 390, 575, 767):
        pg = page("pdp.html", w); d = pg.evaluate(GEO)
        chk("%d  vertical lip not painted" % w, d["white"]["vDisp"], "none")
        chk("%d  horizontal lip painted" % w, d["white"]["hDisp"], "block")
        chk("%d  horizontal lip still at -48" % w, d["white"]["hBottom"], "-48px")
        pg.close()
    # 390 is the board width: pin the phone bite so a later "sync" change is visible
    pg = page("pdp.html", 390); d = pg.evaluate(GEO); pg.close()
    chk("390  phone bite unchanged at 34.4", d["white"]["hBite"], 34.4, 0.6)

    b.close()

print("\n%d ok / %d red" % (ok, bad))
sys.exit(1 if bad else 0)
