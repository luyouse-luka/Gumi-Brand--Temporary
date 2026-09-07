"""R65 assertions — the PDP subscription picker against its two boards.

Board values come from figma/nodes (desktop I324:52733;316:18227 at 1440,
mobile I324:53797;191:2419 at 390); nothing here is eyeballed from a screenshot.
"""
import sys
from playwright.sync_api import sync_playwright

CHROME = "/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome"
URL = "file:///home/ly/project/Gumi-Brand/pdp.html"

# selector -> {property: (desktop, mobile)}   None = not asserted at that width
BOARD = {
    ".gb-sub":               {"rowGap": ("20px", "20px")},
    ".gb-sub__heading":      {"fontSize": ("16px", "16px"), "lineHeight": ("24px", "24px"),
                              "letterSpacing": ("-0.32px", "-0.32px"), "fontWeight": ("500", "500")},
    ".gb-sub__plans":        {"rowGap": ("16px", "16px")},
    ".gb-sub__plan--sub":    {"borderTopLeftRadius": ("16px", "8px")},
    ".gb-sub__banner":       {"paddingTop": ("8px", "8px"), "fontSize": ("14px", "12px"),
                              "lineHeight": ("20px", "12px"),
                              "letterSpacing": ("0.56px", "0.48px"),
                              # node style: textCase UPPER — the copy itself is mixed case
                              "textTransform": ("uppercase", "uppercase")},
    ".gb-sub__panel":        {"paddingTop": ("20px", "16px"), "rowGap": ("16px", "16px")},
    ".gb-sub__info":         {"rowGap": ("4px", "2px")},
    ".gb-sub__name":         {"fontSize": ("16px", "16px"), "lineHeight": ("24px", "24px"),
                              "letterSpacing": ("-0.32px", "-0.32px")},
    ".gb-sub__price":        {"columnGap": ("4px", "2px")},
    ".gb-sub__price-now":    {"fontSize": ("16px", "16px"), "letterSpacing": ("-0.32px", "normal")},
    ".gb-sub__price-was":    {"fontSize": ("14px", "12px"), "textDecorationLine": ("line-through", "line-through")},
    ".gb-sub__packs":        {"fontSize": ("14px", "12px"), "lineHeight": ("22px", "18px"),
                              "letterSpacing": ("-0.28px", "-0.24px")},
    ".gb-sub__works":        {"rowGap": ("8px", "8px")},
    ".gb-sub__works-title":  {"fontSize": ("16px", "14px"), "lineHeight": ("24px", "20px")},
    ".gb-sub__points":       {"rowGap": ("6px", "6px")},
    ".gb-sub__point":        {"columnGap": ("8px", "8px"), "fontSize": ("14px", "14px"),
                              "lineHeight": ("20px", "20px"), "letterSpacing": ("-0.28px", "-0.28px")},
    ".gb-sub__every":        {"rowGap": ("8px", "8px")},
    ".gb-sub__every-label":  {"fontSize": ("16px", "14px")},
    ".gb-sub__plan--once":   {"paddingTop": ("20px", "16px"),
                              "borderTopLeftRadius": ("16px", "8px")},
}

RGB = {"$c-green": "rgb(0, 86, 53)", "$c-lime": "rgb(181, 237, 97)",
       "$c-lime-150": "rgb(231, 248, 208)", "$c-ink": "rgb(1, 19, 7)",
       "$c-gray-700": "rgb(77, 77, 77)", "$c-gray-600": "rgb(102, 102, 102)",
       "$c-lime-stroke": "rgb(71, 172, 0)", "$c-white": "rgb(255, 255, 255)"}

COLOUR = [(".gb-sub__banner", "backgroundColor", "$c-green"),
          (".gb-sub__banner", "color", "$c-lime"),
          (".gb-sub__panel", "backgroundColor", "$c-lime-150"),
          (".gb-sub__plan--once", "backgroundColor", "$c-white"),
          (".gb-sub__name", "color", "$c-ink"),
          (".gb-sub__packs", "color", "$c-gray-600"),
          (".gb-sub__point", "color", "$c-gray-700"),
          (".gb-sub__tick", "color", "$c-lime-stroke")]

PROBE = """(args) => {
  const out = {css: {}, geo: {}, dot: {}, sel: {}};
  for (const [sel, props] of Object.entries(args.board)) {
    const el = document.querySelector(sel);
    if (!el) { out.css[sel] = null; continue; }
    const cs = getComputedStyle(el);
    out.css[sel] = {};
    for (const p of Object.keys(props)) out.css[sel][p] = cs[p];
  }
  for (const [sel, prop] of args.colour) {
    const el = document.querySelector(sel);
    out.css[sel + '|' + prop] = el ? getComputedStyle(el)[prop] : null;
  }
  const r = s => { const e = document.querySelector(s);
                   return e ? e.getBoundingClientRect() : null; };
  const bn = r('.gb-sub__banner'), plan = r('.gb-sub__plan--sub'),
        once = r('.gb-sub__plan--once'), btn = r('.gb-sub__every .gb-select__button');
  out.geo = {banner: bn && +bn.height.toFixed(1), once: once && +once.height.toFixed(1),
             drop: btn && +btn.height.toFixed(1), popular: plan && +plan.height.toFixed(1),
             planW: plan && +plan.width.toFixed(1)};
  // the card's stroke is an inset shadow, not a border (board strokeAlign INSIDE)
  const pcs = plan ? getComputedStyle(document.querySelector('.gb-sub__plan--sub')) : null;
  out.stroke = pcs ? {shadow: pcs.boxShadow, border: pcs.borderTopWidth} : null;

  // the radio dot: ring is the label's ::before
  const pick = document.querySelector('.gb-sub__pick');
  const before = pick && getComputedStyle(pick, '::before');
  out.dot = before ? {w: before.width, h: before.height, radius: before.borderRadius,
                      bg: before.backgroundColor, shadow: before.boxShadow,
                      border: before.borderTopWidth + ' ' + before.borderTopColor} : null;

  // selectBox took the native <select> over
  const wrap = document.querySelector('.gb-sub__every .gb-select');
  out.sel = {upgraded: !!wrap,
             hasButton: !!document.querySelector('.gb-sub__every .gb-select__button'),
             hasList: !!document.querySelector('.gb-sub__every .gb-select__list'),
             options: document.querySelectorAll('.gb-sub__every .gb-select__option').length,
             value: (document.querySelector('.gb-sub__every .gb-select__value') || {}).textContent,
             nativeHidden: (() => { const n = document.querySelector('.gb-sub__select');
               return n ? getComputedStyle(n).position === 'absolute' : null; })()};
  return out;
}"""

ok = red = 0
def chk(cond, label):
    global ok, red
    if cond: ok += 1
    else:
        red += 1
        print("  RED  " + label)

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=CHROME)
    p = b.new_context(viewport={"width": 1440, "height": 1000}).new_page()
    for wi, (w, col) in enumerate([(1440, 0), (390, 1)]):
        p.set_viewport_size({"width": w, "height": 1000})
        p.goto(URL, wait_until="load")
        p.wait_for_timeout(500)
        d = p.evaluate(PROBE, {"board": BOARD, "colour": [(s, pr) for s, pr, _ in COLOUR]})

        for sel, props in BOARD.items():
            got = d["css"].get(sel)
            if got is None:
                chk(False, "%d %s missing" % (w, sel)); continue
            for prop, pair in props.items():
                want = pair[col]
                if want is None: continue
                chk(got[prop] == want,
                    "%d %s %s = %s want %s" % (w, sel, prop, got[prop], want))

        for sel, prop, token in COLOUR:
            chk(d["css"].get(sel + "|" + prop) == RGB[token],
                "%d %s %s = %s want %s (%s)" % (w, sel, prop,
                    d["css"].get(sel + "|" + prop), RGB[token], token))

        # board heights: banner 36/28, dropdown 40 both, one-time 90/76,
        # popular card 334/304 — the last one only holds with an INSIDE stroke
        for key, want in (("banner", 36 if w == 1440 else 28),
                          ("drop", 40),
                          ("once", 90 if w == 1440 else 76),
                          ("popular", 334 if w == 1440 else 304)):
            got = d["geo"][key]
            chk(got is not None and abs(got - want) <= 0.6,
                "%d geo %s = %s want %s" % (w, key, got, want))

        st = d["stroke"]
        chk(st and st["border"] == "0px",
            "%d plan should carry no border, got %s" % (w, st and st["border"]))
        chk(st and "inset" in st["shadow"] and "0, 86, 53" in st["shadow"],
            "%d plan inset stroke = %s" % (w, st and st["shadow"]))

        # radio ring 20x20, 1px green, and the checked core is an inset ring
        dot = d["dot"]
        chk(dot and dot["w"] == "20px" and dot["h"] == "20px",
            "%d radio ring size %s" % (w, dot and (dot["w"], dot["h"])))
        chk(dot and dot["border"] == "1px " + RGB["$c-green"],
            "%d radio ring border %s" % (w, dot and dot["border"]))
        chk(dot and dot["bg"] == RGB["$c-green"],
            "%d checked radio fill %s want green" % (w, dot and dot["bg"]))
        chk(dot and "3.5px" in dot["shadow"] and "231, 248, 208" in dot["shadow"],
            "%d checked radio core %s" % (w, dot and dot["shadow"]))

        # selectBox upgraded the native control
        s = d["sel"]
        chk(s["upgraded"], "%d selectBox did not upgrade .gb-sub__select" % w)
        chk(s["hasButton"] and s["hasList"], "%d select button/list missing" % w)
        chk(s["options"] == 4, "%d select options = %s want 4" % (w, s["options"]))
        chk((s["value"] or "").strip() == "4 Weeks",
            "%d select value = %r want '4 Weeks'" % (w, s["value"]))
        chk(s["nativeHidden"], "%d native select not visually-hidden" % w)
    b.close()

print("\n%d ok / %d red" % (ok, red))
sys.exit(1 if red else 0)
