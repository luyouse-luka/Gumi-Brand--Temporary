#!/usr/bin/env python3
"""Round 32: .gb-promo-modal rebuilt against 336:27146 / 285:19012 / 285:19204.

    python3 tools/r32check.py

Every number below is a Figma bbox relative to the panel (desktop) or to the
390x744 board (mobile), so a failure means the implementation drifted from the
board, not that the assertion is stale.

The bear art is the one that keeps regressing: both groups carry a rotation
(and 38585 a mirror) in Figma, so the four separate rotated-bbox pieces the
component used to ship left every piece upright with the glows detached. It is
now ONE flat export placed by the two groups' union bbox — see the changelog.
"""
import os, sys, json
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = os.path.expanduser("~/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome")
TOL = 1.0

OPEN = """() => {
  const m = document.getElementById('promo-modal');
  m.classList.add('is-open'); m.setAttribute('aria-hidden', 'false');
}"""
REVEAL = """() => { document.querySelector('[data-promo-form]').requestSubmit(); }"""
GEO = """() => {
  const r = s => { const e = document.querySelector(s); if (!e) return null;
                   const b = e.getBoundingClientRect();
                   return [b.x, b.y, b.width, b.height]; };
  const cs = (s, p) => { const e = document.querySelector(s); return e ? getComputedStyle(e)[p] : null; };
  return {
    panel:  r('.gb-promo-panel'),   art:    r('.gb-promo-panel__art'),
    content:r('.gb-promo-panel__content'),
    head:   r('.gb-promo-panel__head'), logo: r('.gb-promo-panel__logo'),
    close:  r('.gb-promo-panel__close'), body: r('.gb-promo-panel__body'),
    title:  r('.gb-promo-panel__title'), lead: r('.gb-promo-panel__lead'),
    stage:  r('.gb-promo-panel__stage'),
    field:  r('[data-promo-panel]:not([hidden]) .gb-promo-panel__field'),
    btn:    r('[data-promo-panel]:not([hidden]) .gb-promo-panel__submit, [data-promo-panel]:not([hidden]) .gb-promo-panel__copy'),
    dismiss:r('[data-promo-panel]:not([hidden]) .gb-promo-panel__dismiss'),
    bears:  r('.gb-promo-panel__bears'),
    icons:  document.querySelectorAll('.gb-promo-panel__field svg').length,
    inputBorder: cs('.gb-promo-panel__input', 'borderTopWidth'),
    inputBg:     cs('.gb-promo-panel__input', 'backgroundColor'),
    imgs:   [...document.querySelectorAll('.gb-promo-panel__art img')].map(i => i.currentSrc.split('/').pop()),
    divider: cs('.gb-promo-panel__divider', 'display'),
  };
}"""

# (label, key, [x, y, w, h] relative to the anchor, anchor)
# desktop: the whole card is 336:27146; everything textual lives in the right
# column 336:27155, so those anchor on .gb-promo-panel__content, not the panel
DESK_EMAIL = [
    ("panel  336:27146",  "panel",  [None, None, 1062, 528], None),
    ("column 336:27155",  "content",[531,  0, 531, 528], "panel"),
    ("head   336:27156",  "head",   [0,   0, 531,  64], "content"),
    ("logo   336:27157",  "logo",   [None, 20, 93, 24], "content"),  # ABS, centred
    ("close  336:27162",  "close",  [483, 16,  32,  32], "content"),
    ("body   336:27163",  "body",   [0, 128, 531, 400], "content"),
    ("title  336:27165",  "title",  [None, 128, None, 96], "content"),
    ("lead   336:27166",  "lead",   [None, 256, None, 56], "content"),
    ("stage  336:27167",  "stage",  [64, 344, 403, 152], "content"),
    ("input  336:27169",  "field",  [64, 344, 403, 44], "content"),
    ("button 336:27170",  "btn",    [64, 400, 403, 52], "content"),
    ("dsmiss 336:27171",  "dismiss",[64, 472, 403, 24], "content"),
    # union bbox of Group 38585 + Group 38584 inside the Image frame
    ("bears  27148+27151","bears",  [-86.84, 13, 624.54, 481.17], "art"),
]
# mobile anchor = .gb-promo-panel (390x744, 285:19012)
MOB_EMAIL = [
    ("panel  285:19012",  "panel",  [None, None, 390, 744], None),
    ("head   285:19014",  "head",   [0,   0, 390,  64], "panel"),
    ("logo   285:19015",  "logo",   [149, 20,  93,  24], "panel"),
    ("close  285:19020",  "close",  [342, 16,  32,  32], "panel"),
    ("body   285:19021",  "body",   [0, 128, 390, 332], "panel"),
    ("title  285:19024",  "title",  [None, 128, None, 80], "panel"),
    ("lead   285:19025",  "lead",   [None, 240, None, 48], "panel"),
    ("stage  285:19026",  "stage",  [40, 320, 310, 140], "panel"),
    ("input  285:19028",  "field",  [40, 320, 310, 44], "panel"),
    ("button 285:19029",  "btn",    [40, 376, 310, 44], "panel"),
    ("dsmiss 285:19030",  "dismiss",[40, 440, 310, 20], "panel"),
    ("art    285:19031",  "art",    [0, 492, 390, 252], "panel"),
    ("bears  19040+19043","bears",  [-17, -37, 384.83, 296.49], "art"),
]
MOB_CODE = [
    ("body   285:19212",  "body",   [0, 128, 390, 292], "panel"),
    ("stage  285:19217",  "stage",  [40, 320, 310, 100], "panel"),
    ("input  285:19219",  "field",  [40, 320, 310, 44], "panel"),
    ("button 285:19224",  "btn",    [40, 376, 310, 44], "panel"),
]

fails = []

def check(tag, geo, table):
    for label, key, want, anchor in table:
        got = geo.get(key)
        if not got:
            fails.append(f"{tag} {label}: element missing"); continue
        base = geo[anchor] if anchor else [0, 0, 0, 0]
        rel = [got[0] - base[0], got[1] - base[1], got[2], got[3]]
        for i, w in enumerate(want):
            if w is None: continue
            if abs(rel[i] - w) > TOL:
                fails.append("%s %s: %s %.2f, board %.2f" %
                             (tag, label, "xywh"[i], rel[i], w))

def centred(tag, geo, key, anchor):
    e, a = geo[key], geo[anchor]
    off = (e[0] - a[0]) - (a[2] - e[2]) / 2
    if abs(off) > TOL:
        fails.append("%s %s: off centre by %.2f" % (tag, key, off))

with sync_playwright() as p:
    br = p.chromium.launch(executable_path=CHROME)
    for w, h, tag, table in [(1440, 768, "1440", DESK_EMAIL), (390, 744, " 390", MOB_EMAIL)]:
        pg = br.new_page(viewport={"width": w, "height": h}, device_scale_factor=2)
        pg.goto("file://" + os.path.join(ROOT, "index.html"))
        pg.wait_for_timeout(1800)
        pg.evaluate(OPEN)
        pg.wait_for_timeout(600)
        geo = pg.evaluate(GEO)
        check(tag, geo, table)
        centred(tag, geo, "logo", "head")

        # the mail icon is visible:false on both boards; the input carries no
        # border of its own (the field around it does)
        if geo["icons"]:
            fails.append("%s field: %d svg icon(s), board has none" % (tag, geo["icons"]))
        if geo["inputBorder"] != "0px":
            fails.append("%s input: border %s, want 0px" % (tag, geo["inputBorder"]))
        if geo["inputBg"] not in ("rgba(0, 0, 0, 0)", "transparent"):
            fails.append("%s input: background %s, want transparent" % (tag, geo["inputBg"]))
        # one flat export, not four rotated-bbox pieces
        if len(geo["imgs"]) != 1 or not geo["imgs"][0].startswith("promo-bears."):
            fails.append("%s art: %s, want a single promo-bears.*" % (tag, geo["imgs"]))
        # the scalloped seam is desktop-only (it splits the two columns)
        want_div = "block" if w >= 1281 else "none"
        if geo["divider"] != want_div:
            fails.append("%s divider: %s, want %s" % (tag, geo["divider"], want_div))

        if w == 390:
            pg.evaluate(REVEAL)
            pg.wait_for_timeout(400)
            check(tag + "c", pg.evaluate(GEO), MOB_CODE)
        pg.close()
    br.close()

if fails:
    print("FAIL (%d)" % len(fails))
    for f in fails: print("  " + f)
    sys.exit(1)
print("r32 OK — %d assertions, desktop + mobile, both states" %
      (len(DESK_EMAIL) + len(MOB_EMAIL) + len(MOB_CODE) + 12))
