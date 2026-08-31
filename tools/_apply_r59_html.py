# -*- coding: utf-8 -*-
"""Round 57 -- wire the favicon into every page's <head>.

No $build bump: nothing in customstyle.scss / main.js changed, so the CSS/JS
cache-bust rule does not apply. The icon links carry the current build's ?v= so
they ride the same scheme when it is next bumped.
"""
import glob, sys

BUILD = "20260831-r58"
ANCHOR = '<link rel="stylesheet" href="assets/customstyle.css'
# Order matters: a browser takes the LAST rel="icon" it understands, so the svg
# (which every current browser prefers) comes after the legacy .ico.
BLOCK = (
    '<link rel="icon" href="images/favicon.ico?v=%s" sizes="32x32">\n'
    '<link rel="icon" href="images/favicon.svg?v=%s" type="image/svg+xml">\n'
    '<link rel="apple-touch-icon" href="images/favicon-180.png?v=%s">\n' % (BUILD, BUILD, BUILD)
)

n = 0
for p in sorted(glob.glob("*.html")):
    h = open(p, encoding="utf-8").read()
    if 'rel="icon"' in h:
        print("skip (already wired): %s" % p); continue
    if h.count(ANCHOR) != 1:
        sys.exit("anchor count != 1 in %s" % p)
    open(p, "w", encoding="utf-8").write(h.replace(ANCHOR, BLOCK + ANCHOR, 1))
    n += 1
print("favicon links added to %d pages" % n)
