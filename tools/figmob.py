#!/usr/bin/env python3
"""Dump the visible, in-flow node tree of a mobile board with board-relative geometry.

    python3 tools/figmob.py [node-file] [origin-node-id]

Defaults to the Homepage Mobile board (228:5932) anchored on "Page Content"
(237:13125) so y matches what the browser lays out -- the board also carries a
fake Chrome browser chrome frame above it that the site never renders.
Hidden nodes (visible:false) are dropped: the board keeps whole unused variants
around (a second CTA button, an overline star row) that are not part of the design.
"""
import json, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NODEFILE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "figma/nodes/228-5932_homepage-mobile.json")
ORIGIN = sys.argv[2] if len(sys.argv) > 2 else "237:13125"

d = json.load(open(NODEFILE))
root = list(d["nodes"].values())[0]["document"]


def find(n, tid):
    if n["id"] == tid:
        return n
    for c in n.get("children", []):
        r = find(c, tid)
        if r:
            return r
    return None


org = find(root, ORIGIN) or root
ob = org["absoluteBoundingBox"]
ox, oy = ob["x"], ob["y"]


def emit(n, dep=0):
    if n.get("visible") is False:
        return
    bb = n.get("absoluteBoundingBox")
    geo = ""
    if bb:
        geo = f"x={bb['x']-ox:8.2f} y={bb['y']-oy:9.2f} w={bb['width']:7.2f} h={bb['height']:7.2f}"
    extra = ""
    if n.get("layoutMode"):
        pads = tuple(n.get(k) or 0 for k in ("paddingTop", "paddingRight", "paddingBottom", "paddingLeft"))
        extra += f" | {n['layoutMode'][:1]} gap={n.get('itemSpacing')} pad={pads}"
    if n.get("layoutPositioning") == "ABSOLUTE":
        extra += " | ABS"
    if n["type"] == "TEXT":
        st = n.get("style", {})
        txt = n.get("characters", "").replace("\u2028", "\\n").replace("\n", "\\n")
        extra += (f" | fs={st.get('fontSize')} lh={st.get('lineHeightPx')} ls={st.get('letterSpacing')}"
                  f" w={st.get('fontWeight')} al={st.get('textAlignHorizontal')} :: {txt[:60]!r}")
        if n.get("characterStyleOverrides") and any(n["characterStyleOverrides"]):
            extra += " | HAS-OVERRIDES"
    print(f"{'  '*dep}{n['id']:38s} {n['type']:9s} {n.get('name','')[:30]:32s} {geo}{extra}")
    for c in n.get("children", []):
        emit(c, dep + 1)


emit(org)
