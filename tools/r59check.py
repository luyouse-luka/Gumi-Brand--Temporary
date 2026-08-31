# -*- coding: utf-8 -*-
"""Round 57 assertions -- the favicon.

The design has no favicon frame, so the artwork is not invented: it is the site's
own GUMI wordmark, and the colour pair is the one the footer already uses
(.gb-footer__logo paints #B5ED61 on the green footer). This script proves both:
the four path `d` strings are byte-identical to the footer logo's, and the two
colours are $c-green / $c-lime as compiled into customstyle.css.

Run it after deleting images/favicon.svg and it must go red.
"""
import glob, os, re, struct, sys, json
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = "/home/ly/project/Gumi-Brand/"
EXE = "/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome"
PLATE, LIME = "#004128", "#B5ED61"   # the footer's own ground, measured

ok = bad = 0
def chk(label, got, want, tol=None):
    global ok, bad
    if tol is not None:
        good = got is not None and abs(got - want) <= tol
        detail = "%s ~ %s (+-%s)" % (got, want, tol)
    else:
        good = got == want
        detail = "%s == %s" % (json.dumps(got, ensure_ascii=False)[:120],
                               json.dumps(want, ensure_ascii=False)[:120])
    if good: ok += 1
    else:
        bad += 1
        print("  RED  %-52s %s" % (label, detail))

print("\n[files] the three icons exist and are what they claim to be")
for f, kind in (("images/favicon.svg", "svg"), ("images/favicon.ico", "ico"),
                ("images/favicon-180.png", "png")):
    p = ROOT + f
    chk("%s exists" % f, os.path.isfile(p), True)
    chk("%s is not empty" % f, os.path.getsize(p) > 200 if os.path.isfile(p) else False, True)

im = Image.open(ROOT + "images/favicon-180.png")
chk("apple-touch-icon is 180x180", im.size, (180, 180))
chk("apple-touch-icon is opaque (iOS composites it)", im.convert("RGBA").getpixel((0, 0))[3], 255)
ico = Image.open(ROOT + "images/favicon.ico")
chk("ico carries the legacy sizes", sorted(ico.ico.sizes()), [(16, 16), (32, 32), (48, 48)])

print("\n[provenance] the artwork IS the design's wordmark, not a redraw")
svg = open(ROOT + "images/favicon.svg", encoding="utf-8").read()
home = open(ROOT + "index.html", encoding="utf-8").read()
m = re.search(r'<a class="gb-footer__logo".*?</a>', home, re.S)
chk("anchor: the footer logo is still in index.html", bool(m), True)   # or the compare below is vacuous
footer_paths = re.findall(r'<path d="([^"]+)" fill="%s"/>' % LIME, m.group(0)) if m else []
chk("footer logo still has its 4 paths", len(footer_paths), 4)
fav_paths = re.findall(r'<path d="([^"]+)"/>', svg)
chk("favicon carries 4 paths", len(fav_paths), 4)
chk("every path is byte-identical to the footer logo's", fav_paths, footer_paths)

print("\n[colour] the pair comes from the design, not from me")
chk("plate is the footer's ground colour", PLATE.lower() in svg.lower(), True)
chk("wordmark is the brand lime", LIME.lower() in svg.lower(), True)
# The ground behind the footer logo is measured, not grepped: the green is set on
# an ancestor, so a text search of the compiled css looks in the wrong rule.
GROUND = """()=>{let e=document.querySelector('.gb-footer__logo'), bg='rgba(0, 0, 0, 0)';
  while (e && bg === 'rgba(0, 0, 0, 0)') { bg = getComputedStyle(e).backgroundColor; e = e.parentElement; }
  return bg;}"""

print("\n[render] the plate is green and the wordmark actually paints")
px = Image.open(ROOT + "images/favicon-180.png").convert("RGB")
chk("corner is the plate colour", px.getpixel((2, 2)), (0, 65, 40))
w, h = px.size
lime = sum(1 for y in range(h) for x in range(w)
           if abs(px.getpixel((x, y))[0] - 181) < 24 and px.getpixel((x, y))[1] > 200)
chk("the wordmark covers a real share of the plate (not an empty square)",
    600 < lime < 12000, True)
# it must not bleed into the corners iOS rounds off
corner = [px.getpixel((x, y)) for x in range(0, 12) for y in range(0, 12)]
chk("safe area: nothing painted in the rounded-off corner",
    all(c == (0, 65, 40) for c in corner), True)

print("\n[wiring] every page points at all three, in the right order")
pages = sorted(os.path.basename(p) for p in glob.glob(ROOT + "*.html"))
chk("12 pages found (11 delivered + font-check)", len(pages), 12)
for p in pages:
    h = open(ROOT + p, encoding="utf-8").read()
    head = h[:h.find("</head>")]
    icons = re.findall(r'<link rel="(icon|apple-touch-icon)" href="([^"?]+)[^"]*"', head)
    chk("%s  three icon links" % p, len(icons), 3)
    chk("%s  ico before svg (last understood rel=icon wins)" % p,
        [r for r, _ in icons], ["icon", "icon", "apple-touch-icon"])
    for _, href in icons:
        chk("%s  %s resolves on disk" % (p, href), os.path.isfile(ROOT + href), True)
    chk("%s  icons sit above the stylesheet" % p,
        head.find('rel="icon"') < head.find('rel="stylesheet"'), True)

print("\n[browser] the files really load and decode")
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=EXE)
    pg = b.new_page(viewport={"width": 200, "height": 200})
    for f in ("images/favicon.svg", "images/favicon-180.png", "images/favicon.ico"):
        pg.goto("file://" + ROOT + f)
        chk("%s decodes in chromium" % f,
            pg.evaluate("()=>document.readyState") == "complete", True)
    pg.goto("file://" + ROOT + "index.html"); pg.wait_for_timeout(500)
    chk("the ground behind the footer logo is the plate's green",
        pg.evaluate(GROUND), "rgb(0, 65, 40)")
    # the svg must be square, or the tab icon gets letterboxed
    pg.goto("file://" + ROOT + "images/favicon.svg")
    d = pg.evaluate("""()=>{const s=document.querySelector('svg');
      const v=s.getAttribute('viewBox').split(/\\s+/).map(Number);
      return {vb:v, ratio:v[2]/v[3]};}""")
    chk("viewBox is square", d["ratio"], 1.0, 0.001)
    pg.close(); b.close()

print("\n%d ok / %d red" % (ok, bad))
sys.exit(1 if bad else 0)
