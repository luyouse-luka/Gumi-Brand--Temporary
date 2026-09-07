#!/usr/bin/env python3
"""Every url() in the stylesheet must be a bare filename resolving inside assets/.

Shopify serves assets/ flat from its CDN: a stylesheet there has no images/
sibling to walk up into, so "../images/x.png" 404s the moment the theme goes up
even though it resolves fine over file:// and on the static host. The fonts were
always written this way; .gb-bear-meter__bear was the one that was not (r61).

Checks the scss source and the compiled css, and that each referenced file is
really on disk. data: urls are skipped -- the three masks are inlined on purpose
(css mask url() is CORS-blocked over file://).

    python3 tools/assetpath.py
"""
import io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")
URL = re.compile(r'url\(\s*["\']?([^"\')]+?)["\']?\s*\)')

bad = 0
for name in ("assets/customstyle.scss", "assets/customstyle.css",
             "assets/account.scss", "assets/account.css"):
    path = os.path.join(ROOT, name)
    if not os.path.exists(path):
        print("  SKIP %-28s not built yet" % name)
        continue
    src = io.open(path, encoding="utf-8").read()
    seen = set()
    for raw in URL.findall(src):
        if raw.startswith("data:") or raw.startswith("#"):
            continue
        ref = raw.split("?")[0].split("#")[0]
        if ref in seen:
            continue
        seen.add(ref)
        if "/" in ref:
            print("  RED  %-28s not a bare filename: %s" % (name, raw))
            bad += 1
            continue
        # scss keeps the build token unresolved (#{$build}); the file is the same
        if not os.path.exists(os.path.join(ASSETS, ref)):
            print("  RED  %-28s missing from assets/: %s" % (name, ref))
            bad += 1
    print("  %-28s %d url() refs" % (name, len(seen)))

print("\n  %s" % ("GREEN" if bad == 0 else "RED  %d problem(s)" % bad))
sys.exit(1 if bad else 0)
