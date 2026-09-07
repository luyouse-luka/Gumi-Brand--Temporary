#!/usr/bin/env python3
"""Dump a subtree of any board with absolute geometry, styles and fills.

    python3 tools/r65node.py <board-stem> --find "Autoship"     locate
    python3 tools/r65node.py <board-stem> --node 324:52801      dump
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load(stem):
    d = json.load(open(os.path.join(ROOT, "figma", "nodes", stem + ".json")))
    root = d["nodes"][list(d["nodes"].keys())[0]]["document"]
    idx, parent = {}, {}
    def ix(n, p=None):
        idx[n["id"]] = n
        if p: parent[n["id"]] = p
        for c in n.get("children") or []: ix(c, n["id"])
    ix(root)
    return idx, parent, root

def fmt(n, depth):
    bb = n.get("absoluteBoundingBox") or {}
    bits = ["%s%s <%s> %s" % ("  " * depth, n.get("name", "?"), n["type"], n["id"])]
    if bb:
        bits.append("    box x=%.1f y=%.1f w=%.1f h=%.1f"
                    % (bb.get("x", 0), bb.get("y", 0), bb.get("width", 0), bb.get("height", 0)))
    lay = []
    for k in ("layoutMode", "itemSpacing", "counterAxisAlignItems", "primaryAxisAlignItems",
              "paddingLeft", "paddingRight", "paddingTop", "paddingBottom",
              "layoutSizingHorizontal", "layoutSizingVertical"):
        if n.get(k) not in (None, "NONE", 0): lay.append("%s=%s" % (k, n[k]))
    if lay: bits.append("    layout " + " ".join(lay))
    if n.get("cornerRadius") is not None: lay2 = ["radius=%s" % n["cornerRadius"]]
    else: lay2 = []
    if n.get("rectangleCornerRadii"): lay2.append("radii=%s" % n["rectangleCornerRadii"])
    for f in (n.get("fills") or []):
        if f.get("visible") is False: continue
        if f.get("type") == "SOLID":
            c = f["color"]
            lay2.append("fill=#%02X%02X%02X@%.2f" % (round(c["r"]*255), round(c["g"]*255),
                                                     round(c["b"]*255), f.get("opacity", 1)))
        else: lay2.append("fill=%s" % f.get("type"))
    for st in (n.get("strokes") or []):
        if st.get("type") == "SOLID":
            c = st["color"]
            lay2.append("stroke=#%02X%02X%02X/%s" % (round(c["r"]*255), round(c["g"]*255),
                                                     round(c["b"]*255), n.get("strokeWeight")))
    if n.get("effects"):
        for e in n["effects"]:
            if e.get("visible") is False: continue
            lay2.append("%s r=%s off=%s,%s" % (e.get("type"), e.get("radius"),
                        (e.get("offset") or {}).get("x"), (e.get("offset") or {}).get("y")))
    if lay2: bits.append("    box2 " + " ".join(lay2))
    st = n.get("style") or {}
    if st:
        bits.append("    text %s %s/%s lh=%s ls=%s align=%s"
                    % (st.get("fontFamily"), st.get("fontSize"), st.get("fontWeight"),
                       st.get("lineHeightPx"), st.get("letterSpacing"),
                       st.get("textAlignHorizontal")))
    if n.get("characters"):
        bits.append("    chars %r" % n["characters"][:110])
        if n.get("characterStyleOverrides") and any(n["characterStyleOverrides"]):
            bits.append("    ⚠ characterStyleOverrides present: %s" % n.get("styleOverrideTable"))
    return "\n".join(bits)

stem = sys.argv[1]
idx, parent, root = load(stem)

if "--find" in sys.argv:
    q = sys.argv[sys.argv.index("--find") + 1].lower()
    for nid, n in idx.items():
        if q in (n.get("characters") or "").lower() or q in (n.get("name") or "").lower():
            chain = []
            p = nid
            while p:
                chain.append("%s<%s>%s" % (idx[p].get("name", "?"), idx[p]["type"], p))
                p = parent.get(p)
            print(" / ".join(reversed(chain[:6])))
            print()
elif "--node" in sys.argv:
    nid = sys.argv[sys.argv.index("--node") + 1]
    maxd = int(sys.argv[sys.argv.index("--depth") + 1]) if "--depth" in sys.argv else 99
    def walk(n, d=0):
        if n.get("visible") is False or d > maxd: return
        print(fmt(n, d))
        for c in n.get("children") or []: walk(c, d + 1)
    walk(idx[nid])
