#!/usr/bin/env python3
"""Invariant-tier regression judge by rectangle multiset, against a cssnap baseline.

    python3 tools/r42rect.py r41 1440
    python3 tools/r42rect.py r41m 390

Why not `cssnap.py diff`: its diff is path-keyed, so adding or removing a single
DOM node shifts every later sibling's index and the comparison lines up different
elements — thousands of false differences. r42 both removes a node (.gb-app-slot)
and adds nine (the expert rail's loop clones), so the judge has to be
order-insensitive. HANDOFF "桌面绝不能被动到" prescribes exactly this shape.

Why not just re-run cssnap: it captures 340 properties x 3 pseudo-states per
element and gets OOM-killed on this box when the other tenants are busy (r42's
first attempt died at 2 of 12 files). Rectangles alone are ~100x smaller, so this
runs where cssnap cannot.

The capture conditions are copied from cssnap.py verbatim — same element set,
same animation/opacity kill, same pinned Math.random. Diverging on any of those
would manufacture differences that have nothing to do with the change.
"""
import collections
import json
import os
import sys

from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNAP = os.path.join(ROOT, "tools", "snap")
CHROME = os.path.expanduser("~/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome")

# identical element set and rounding to cssnap.py's PROBE, minus the properties
PROBE = """() => {
  const out = [];
  const els = document.querySelectorAll('body, body *');
  for (let i = 0; i < els.length; i++) {
    const el = els[i];
    if (el.tagName === 'SCRIPT' || el.tagName === 'STYLE') continue;
    const r = el.getBoundingClientRect();
    out.push([Math.round(r.x*10)/10, Math.round(r.y*10)/10,
              Math.round(r.width*10)/10, Math.round(r.height*10)/10]);
  }
  return {rects: out,
          bodyH: Math.round(document.body.getBoundingClientRect().height*10)/10};
}"""

KILL = ("*,*::before,*::after{animation:none!important;"
        "transition:none!important;opacity:1!important}")


def pages():
    import glob
    return sorted(os.path.basename(p) for p in glob.glob(os.path.join(ROOT, "*.html")))


def baseline(tag, name, width):
    """rect multiset + body height out of a cssnap snapshot"""
    path = os.path.join(SNAP, tag, f"{name}.{width}.json")
    if not os.path.exists(path):
        return None, None
    rows = json.load(open(path))
    counter = collections.Counter(
        tuple(s["#rect"]) for _, s in rows if isinstance(s, dict) and "#rect" in s)
    body = None
    for p, s in rows:
        if p == "/html[0]/body[1]" and isinstance(s, dict) and "#rect" in s:
            body = s["#rect"][3]
            break
    return counter, body


def main(tag, width):
    missing, drift = [], []
    with sync_playwright() as pw:
        br = pw.chromium.launch(executable_path=CHROME)
        pg = br.new_page(viewport={"width": width, "height": 900})
        pg.add_init_script("Math.random = function () { return 0.5; };")
        for name in pages():
            want, wantBody = baseline(tag, name, width)
            if want is None:
                missing.append(name)
                continue
            pg.goto("file://" + os.path.join(ROOT, name))
            pg.evaluate("() => document.fonts.ready")
            pg.add_style_tag(content=KILL)
            pg.wait_for_timeout(120)
            got = pg.evaluate(PROBE)
            have = collections.Counter(tuple(r) for r in got["rects"])
            gone = sum((want - have).values())
            new = sum((have - want).values())
            dh = round(got["bodyH"] - wantBody, 1) if wantBody is not None else None
            flag = "  " if (gone == 0 and new == 0 and dh == 0) else "!!"
            print(f"{flag} {name:<22} only-in-{tag}: {gone:<5} only-in-now: {new:<5} "
                  f"bodyH {wantBody} -> {got['bodyH']} ({dh:+})")
            # A raw count says nothing: removing one box shifts every later
            # element up by its height, so hundreds of rects "differ" while the
            # layout is untouched. Re-check the leftovers with that shift undone
            # -- whatever still fails to line up is real geometry change.
            if (gone or new) and dh:
                old_only, new_only = want - have, have - want
                # elements below the removed box moved up by |dh|; put them back
                back = collections.Counter(
                    (x, round(y - dh, 1), w, h) for (x, y, w, h) in new_only.elements())
                left_new = back - old_only
                left_old = old_only - back
                print(f"     └─ with the {dh:+} shift undone: "
                      f"{sum(left_new.values())} new / {sum(left_old.values())} old "
                      f"rect(s) still unexplained")
                for r, n in list(left_old.items())[:6]:
                    print(f"          was: {r} x{n}")
                for r, n in list(left_new.items())[:6]:
                    print(f"          now: {r} x{n}")
            if gone or new or dh:
                drift.append((name, gone, new, dh))
        pg.close()
        br.close()

    print("=" * 76)
    if missing:
        print(f"!! no baseline for {len(missing)} page(s): {', '.join(missing)}")
    if not drift:
        print(f"✅ {width}: rectangle multiset identical to {tag} on every page")
    else:
        print(f"⚠ {width}: {len(drift)} page(s) differ from {tag} — each one has to be "
              f"explained by this round's change, or it is a regression")
    return 1 if (drift or missing) else 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1], int(sys.argv[2])))
