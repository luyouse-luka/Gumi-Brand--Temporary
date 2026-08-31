# -*- coding: utf-8 -*-
"""Round 53 assertions (build r55) -- the 13 brief items that landed.

Run against the CURRENT scss it must be all-green; run it against the pre-round
css (invert tools/_apply_r55.py) and it must go red in bulk. A one-way green
script can be a script that verified nothing.
"""
import sys, json
import numpy as np
from PIL import Image
from collections import deque
from playwright.sync_api import sync_playwright

EXE = "/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome"
ROOT = "file:///home/ly/project/Gumi-Brand/"
TMP = "/home/ly/project/Gumi-Brand/tools/_r55_shot.png"   # deleted on exit -- snap chromium cannot read /tmp, so probe files land in the project and
# would otherwise be picked up as this round's changes by the sync script

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
        print("  RED  %-52s %s" % (label, detail))

def holes(path):
    """Sentinel-magenta pixels unreachable from the image border = enclosed gaps."""
    a = np.array(Image.open(path).convert("RGB")).astype(int)
    m = (abs(a[:, :, 0] - 255) < 40) & (a[:, :, 1] < 60) & (abs(a[:, :, 2] - 255) < 40)
    h, w = m.shape
    seen = np.zeros_like(m)
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if m[y, x] and not seen[y, x]: seen[y, x] = True; q.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if m[y, x] and not seen[y, x]: seen[y, x] = True; q.append((y, x))
    while q:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and m[ny, nx] and not seen[ny, nx]:
                seen[ny, nx] = True; q.append((ny, nx))
    return int((m & ~seen).sum())

RECT = """(sel)=>{const e=document.querySelector(sel); if(!e) return null;
  const r=e.getBoundingClientRect(), c=getComputedStyle(e);
  return {x:+r.x.toFixed(1), y:+r.y.toFixed(1), w:+r.width.toFixed(1), h:+r.height.toFixed(1),
    top:+r.top.toFixed(1), bottom:+r.bottom.toFixed(1), right:+r.right.toFixed(1),
    maxW:c.maxWidth, fs:c.fontSize, lh:c.lineHeight, ls:c.letterSpacing,
    mt:c.marginTop, mb:c.marginBottom, pl:c.paddingLeft, pr:c.paddingRight,
    disp:c.display, opacity:c.opacity, td:c.textDecorationLine, cssTop:c.top};}"""

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=EXE)

    def page(url, w, h=900, dsf=1):
        pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=dsf)
        pg.goto(ROOT + url); pg.wait_for_timeout(650)
        pg.evaluate("()=>document.querySelectorAll('.wowo').forEach(e=>{e.classList.add('animated')})")
        pg.wait_for_timeout(250)
        return pg

    # ------------------------------------------------------------------ 2.1
    print("\n[2.1] promo artwork clears the scallop on sub-390 phones")
    # Board widths must not move at all; the narrow ones must gain clearance.
    for w, want_img_w, min_gap in ((767, 333.3, 40), (575, 333.3, 40), (390, 333.3, 3),
                                   (360, None, 3), (320, None, 3)):
        pg = page("pdp.html", w)
        d = pg.evaluate("""()=>{const q=s=>{const e=document.querySelector(s); if(!e) return null;
             const r=e.getBoundingClientRect(); return {y:+r.y.toFixed(1),b:+r.bottom.toFixed(1),w:+r.width.toFixed(1)};};
           const img=q('.gb-promo-card--white .gb-promo-art__img');
           const lip=q('.gb-promo-card--white .gb-promo-card__lip--h');
           return {img, lip, gap: (img&&lip)? +(lip.y-img.b).toFixed(1) : null};}""")
        gap = d["gap"]
        if gap is None: chk("%d gap measurable" % w, None, "number"); pg.close(); continue
        chk("%d img/scallop gap >= %s" % (w, min_gap), gap >= min_gap, True)
        if want_img_w is not None:
            chk("%d board width untouched" % w, d["img"]["w"], want_img_w, tol=0.6)
        pg.close()

    # ------------------------------------------------------------------ 2.3
    print("\n[2.3] vs table full width on phones, capped above them")
    for w, full in ((575, True), (480, True), (390, True), (576, False), (700, False), (767, False)):
        pg = page("pdp.html", w)
        d = pg.evaluate("""()=>{const t=document.querySelector('.gb-vs__table');
          const bear=document.querySelector('.gb-vs__bear');
          const tr=t.getBoundingClientRect();
          return {w:+tr.width.toFixed(1), maxW:getComputedStyle(t).maxWidth,
            bearRight: bear? +bear.getBoundingClientRect().right.toFixed(1) : null,
            doc: document.documentElement.scrollWidth, win: window.innerWidth};}""")
        chk("%d max-width" % w, d["maxW"], "100%" if full else "400px")
        if full:
            chk("%d table fills the container" % w, d["w"], min(w - 40, 535), tol=1)
        # the reason the cap survives above 575: the bear must stay on screen
        chk("%d no horizontal overflow" % w, d["doc"] <= d["win"], True)
        pg.close()

    # ------------------------------------------------------------------ 2.4
    print("\n[2.4] no ring on the close button when a modal opens")
    pg = page("index.html", 1440)
    d = pg.evaluate("""()=>{
      const m=document.querySelector('.gb-promo-modal');
      m.classList.add('is-open'); m.setAttribute('aria-hidden','false');
      m.focus();
      const c=m.querySelector('.gb-promo-panel__close');
      const cs=getComputedStyle(c), ms=getComputedStyle(m);
      return {dialogTabindex: m.getAttribute('tabindex'),
              focusIsDialog: document.activeElement===m,
              closeRing: c.matches(':focus-visible'),
              closeOutline: cs.outlineStyle,
              dialogOutline: ms.outlineStyle};}""")
    chk("dialog is focusable", d["dialogTabindex"], "-1")
    chk("initial focus lands on the dialog", d["focusIsDialog"], True)
    chk("close button is not focus-visible", d["closeRing"], False)
    chk("dialog paints no ring of its own", d["dialogOutline"], "none")
    pg.close()
    # and the real path: main.js open() must not put focus on a control
    pg = page("index.html", 1440)
    d = pg.evaluate("""()=>new Promise(res=>{
      const btn=document.querySelector('[data-modal="nutritional-label"]');
      if(!btn) return res({skip:true});
      btn.click();
      setTimeout(()=>{const a=document.activeElement;
        res({tag:a.tagName, cls:String(a.className||''),
             outline:getComputedStyle(a).outlineStyle,
             closeRing: !!(a.querySelector&&a.querySelector('[data-modal-close]')
                        && a.querySelector('[data-modal-close]').matches(':focus-visible'))});}, 400);})""")
    if not d.get("skip"):
        chk("open() focuses the dialog, not a button", d["tag"], "DIV")
        chk("focus landed on a dialog container", "modal" in d["cls"], True)
        chk("the focused dialog paints no ring", d["outline"], "none")
        # This is the assertion the brief is about: nothing inside the panel may
        # be showing a ring the instant the modal appears.
        chk("no ring on the close button after open()", d["closeRing"], False)
    pg.close()

    # ------------------------------------------------------------------ 2.6
    print("\n[2.6] bear meter + drawer CTA caps")
    for w, meter_max in ((390, "100%"), (575, "100%"), (767, "100%"), (768, "347px"), (1440, "347px")):
        pg = page("science.html", w)
        chk("%d bear-meter max-width" % w, pg.evaluate(RECT, ".gb-bear-meter")["maxW"], meter_max)
        pg.close()
    for w in (767, 575, 390):
        pg = page("index.html", w)
        pg.evaluate("""()=>{const t=document.querySelector('.gb-header__burger,.gb-header__toggle,[data-header-toggle]');
          if(t) t.click();}""")
        pg.wait_for_timeout(850)
        d = pg.evaluate(RECT, ".gb-header__nav .gb-btn.gb-btn--lg")
        chk("%d drawer CTA cap" % w, d["maxW"], "520px")
        chk("%d drawer CTA width" % w, d["w"], min(520.0, w - 40), tol=1)
        pg.close()

    # ------------------------------------------------------------------ 2.7
    print("\n[2.7] footer newsletter cap + deco bear on percentages")
    for w, want in ((390, 340.0), (575, 340.0), (767, 340.0)):
        pg = page("index.html", w)
        d = pg.evaluate(RECT, ".gb-footer__newsletter")
        chk("%d newsletter max-width" % w, d["maxW"], "340px")
        chk("%d newsletter width" % w, d["w"], want, tol=1)
        pg.close()
    # percentages, and exact on their own boards
    for w, want_offset in ((1440, 408.0), (390, 457.0)):
        pg = page("index.html", w)
        d = pg.evaluate("""()=>{const bear=document.querySelector('.gb-deco-bear--b');
          const cb=bear.offsetParent;
          return {cssTop:getComputedStyle(bear).top,
                  offset:+(bear.getBoundingClientRect().y-cb.getBoundingClientRect().y).toFixed(2),
                  cbH:+cb.getBoundingClientRect().height.toFixed(2)};}""")
        # a percentage top resolves to px in computed style, so assert the ratio
        chk("%d bear sits where it did" % w, d["offset"], want_offset, tol=0.6)
        chk("%d bear top is a ratio of the wrap" % w,
            round(d["offset"] / d["cbH"], 4), round(want_offset / d["cbH"], 4), tol=0.001)
        pg.close()
    # the point of the change: it now tracks the container instead of ignoring it
    pg = page("index.html", 1440)
    grew = pg.evaluate("""()=>{const bear=document.querySelector('.gb-deco-bear--b');
      const cb=bear.offsetParent;
      const before=bear.getBoundingClientRect().y-cb.getBoundingClientRect().y;
      cb.style.height=(cb.getBoundingClientRect().height+200)+'px';
      const after=bear.getBoundingClientRect().y-cb.getBoundingClientRect().y;
      return +(after-before).toFixed(1);}""")
    chk("bear follows a taller wrap", grew > 100, True)
    pg.close()

    # ------------------------------------------------------------------ 2.8
    print("\n[2.8] no page ground showing through the figure's outline")
    pg = b.new_page(viewport={"width": 1440, "height": 1000}, device_scale_factor=4)
    pg.goto(ROOT + "science.html"); pg.wait_for_timeout(500)
    pg.evaluate("""()=>{document.querySelectorAll('.gb-science-card').forEach(c=>c.style.background='#ff00ff');
      document.querySelectorAll('.wowo').forEach(e=>{e.classList.add('animated');e.style.opacity=1});}""")
    pg.evaluate("()=>document.querySelectorAll('.gb-science-card__value')[3].scrollIntoView({block:'center'})")
    pg.wait_for_timeout(3500)
    vals = pg.query_selector_all(".gb-science-card__value")
    for i in (0, 3):
        txt = vals[i].inner_text()
        vals[i].screenshot(path=TMP)
        chk("card %d (%s) has no enclosed gaps" % (i, txt), holes(TMP), 0)
    pg.close()

    # ------------------------------------------------------------------ 3.1
    print("\n[3.1] tight science group spacing + phone figure")
    for w in (1440, 390):
        pg = page("science.html", w)
        d = pg.evaluate("""()=>{const s=document.querySelectorAll('.gb-science')[1];
          const cards=s.querySelector('.gb-science__cards');
          const t=document.querySelector('.gb-science-card__text');
          const v=document.querySelector('.gb-science-card__value');
          const cs=getComputedStyle(cards), ts=getComputedStyle(t), vs=getComputedStyle(v);
          return {tightCls:s.className, cardsMt:cs.marginTop, textMt:ts.marginTop,
                  fs:vs.fontSize, lh:vs.lineHeight, ls:vs.letterSpacing};}""")
        chk("%d second group is the tight one" % w, "gb-science--tight" in d["tightCls"], True)
        chk("%d tight cards margin-top" % w, d["cardsMt"], "26px")
        chk("%d card text margin-top" % w, d["textMt"], "6px")
        if w == 390:
            chk("390 figure size", d["fs"], "36px")
            chk("390 figure leading", d["lh"], "40px")
            chk("390 figure tracking", d["ls"], "-0.36px")
        else:
            chk("1440 figure untouched", (d["fs"], d["lh"]), ("56px", "44px"))
        pg.close()
    # the ramp exists, so 767/768 does not jump 36 -> 56
    seam = {}
    for w in (767, 768):
        pg = page("science.html", w)
        seam[w] = float(pg.evaluate(RECT, ".gb-science-card__value")["fs"][:-2])
        pg.close()
    chk("767/768 figure seam is continuous", abs(seam[768] - seam[767]) <= 1.2, True)
    # index carries the unscoped rule too
    pg = page("index.html", 1440)
    chk("index card text also gets 6", pg.evaluate(RECT, ".gb-science-card__text")["mt"], "6px")
    pg.close()

    # ------------------------------------------------------------------ 3.2
    print("\n[3.2] faq image body gutter is a desktop-only value")
    for w, want in ((390, "0px"), (767, "0px"), (768, "0px"), (1280, "0px"), (1281, "32px"), (1440, "32px")):
        pg = page("science.html", w)
        d = pg.evaluate(RECT, ".gb-faq-image__body")
        chk("%d faq body padding-inline" % w, (d["pl"], d["pr"]), (want, want))
        pg.close()

    # ------------------------------------------------------------------ 3.5-3.7
    print("\n[3.5-3.7] contact form: drawn checkbox, underlined note, disclaimer margin")
    pg = page("get-in-touch.html", 1440)
    pg.evaluate("()=>document.querySelector('.gb-form__check').scrollIntoView({block:'center'})")
    pg.wait_for_timeout(200)
    PSEUDO = """()=>{const l=document.querySelector('.gb-form__check');
      const s=getComputedStyle(l,'::before'), i=l.querySelector('input[type=checkbox]');
      return {w:s.width, h:s.height, bg:s.backgroundColor, bc:s.borderTopColor,
        img:s.backgroundImage, tp:s.transitionProperty,
        inputDisplay:getComputedStyle(i).display, inputPos:getComputedStyle(i).position,
        checked:i.checked};}"""
    off = pg.evaluate(PSEUDO)
    chk("drawn box is 20x20", (off["w"], off["h"]), ("20px", "20px"))
    chk("drawn box transitions colour",
        "background-color" in off["tp"] and "border-color" in off["tp"], True)
    chk("unchecked box is empty", off["img"], "none")
    chk("unchecked box is white", off["bg"], "rgb(255, 255, 255)")
    chk("native input is hidden, not removed", off["inputDisplay"] != "none", True)
    chk("native input is taken out of flow", off["inputPos"], "absolute")
    chk("native input is still focusable",
        pg.evaluate("""()=>{const i=document.querySelector('.gb-form__check input');
          i.focus(); return document.activeElement===i;}"""), True)
    # A real click on the DRAWN box has to toggle it -- the native control is
    # off-screen, so the pseudo-element is the only target a user can hit.
    box = pg.query_selector(".gb-form__check").bounding_box()
    pg.mouse.click(box["x"] + 10, box["y"] + 12)
    pg.wait_for_timeout(250)
    on = pg.evaluate(PSEUDO)
    chk("clicking the drawn box toggles the control", on["checked"], True)
    chk("checked box fills green", on["bg"], "rgb(0, 86, 53)")
    chk("checked box border turns green", on["bc"], "rgb(0, 86, 53)")
    chk("checked box draws a tick", on["img"] != "none", True)
    pg.close()
    # the note only lives on referral
    pg = page("referral.html", 1440)
    chk("note link is underlined", pg.evaluate(RECT, ".gb-form__note a")["td"], "underline")
    pg.close()

    for w, mt, mb in ((390, "16px", "-2px"), (1440, "0px", "0px")):
        pg = page("referral.html", w)
        d = pg.evaluate(RECT, ".gb-form__disclaimer")
        chk("%d disclaimer margin" % w, (d["mt"], d["mb"]), (mt, mb))
        pg.close()

    # ------------------------------------------------------------------ 3.8
    print("\n[3.8] rich pages reveal on scroll and end up visible")
    for url in ("privacy-policy.html", "shipping.html"):
        pg = b.new_page(viewport={"width": 1440, "height": 900})
        pg.goto(ROOT + url); pg.wait_for_timeout(900)
        d = pg.evaluate("""()=>{const i=document.querySelector('.gb-rich-page__inner');
          const sec=document.querySelector('.gb-rich-page');
          return {cls:i.className, secOpacity:getComputedStyle(sec).opacity,
                  secBg:getComputedStyle(sec).backgroundColor};}""")
        chk("%s inner carries the reveal" % url, "wowo" in d["cls"] and "fadeInUp" in d["cls"], True)
        # the section itself must stay opaque or its white ground goes with it
        chk("%s section ground survives" % url, d["secOpacity"], "1")
        chk("%s section is still white" % url, d["secBg"], "rgb(255, 255, 255)")
        pg.wait_for_timeout(2200)
        chk("%s content ends visible" % url,
            pg.evaluate("()=>getComputedStyle(document.querySelector('.gb-rich-page__inner')).opacity"), "1")
        pg.close()

    b.close()

import os
if os.path.exists(TMP): os.remove(TMP)

print("\n%d ok / %d red" % (ok, bad))
sys.exit(1 if bad else 0)
