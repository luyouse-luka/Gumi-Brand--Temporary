#!/usr/bin/env python3
"""Query any dumped Figma board for nodes by name / text / id.

    python3 tools/fq.py <board-key|node-file> <pattern> [--depth N] [--tree]

Board keys are the file stem prefix, e.g. "228-5932" or a substring of the
filename ("pdp-mobile"). Pattern is a case-insensitive regex matched against
the node name AND, for TEXT nodes, the characters. An exact "123:456" id is
matched directly.

Prints every layout property that actually drives the render, so a value can be
read off the source instead of eyeballed off a screenshot. Rotation matters:
absoluteBoundingBox is the axis-aligned box of a ROTATED node and is not the
artwork -- rot/det are printed so a mismatch is visible rather than silent.
"""
import json, math, os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NODEDIR = os.path.join(ROOT, "figma/nodes")

LAYOUT_KEYS = (
    "layoutMode", "itemSpacing", "counterAxisSpacing",
    "paddingLeft", "paddingRight", "paddingTop", "paddingBottom",
    "primaryAxisAlignItems", "counterAxisAlignItems",
    "primaryAxisSizingMode", "counterAxisSizingMode",
    "layoutGrow", "layoutAlign", "layoutSizingHorizontal", "layoutSizingVertical",
    "cornerRadius", "rectangleCornerRadii", "clipsContent", "opacity",
)


def resolve(key):
    if os.path.isfile(key):
        return key
    hits = [p for p in glob.glob(os.path.join(NODEDIR, "*.json")) if key.lower() in os.path.basename(p).lower()]
    if not hits:
        sys.exit(f"no board matching {key!r} in {NODEDIR}")
    if len(hits) > 1 and not any(os.path.basename(h).startswith(key) for h in hits):
        sys.exit("ambiguous board key, matches:\n  " + "\n  ".join(os.path.basename(h) for h in hits))
    return sorted(hits)[0]


def load(path):
    d = json.load(open(path))
    roots = [v["document"] for v in d["nodes"].values()]
    return roots


def fmt_fill(n):
    out = []
    for f in (n.get("fills") or []):
        if f.get("visible") is False:
            continue
        if f["type"] == "SOLID":
            c = f["color"]
            a = f.get("opacity", 1) * c.get("a", 1)
            hx = "#%02x%02x%02x" % tuple(round(c[k] * 255) for k in "rgb")
            out.append(hx + ("" if a >= .999 else f"@{a:.2f}"))
        else:
            out.append(f["type"])
    return ",".join(out)


def describe(n, parent_box=None):
    bb = n.get("absoluteBoundingBox") or {}
    rb = n.get("absoluteRenderBounds") or {}
    parts = [f"{n['type']:<9} {n.get('name','')[:34]:<34} {n['id']}"]
    parts.append(f"  box  x={bb.get('x',0):9.2f} y={bb.get('y',0):9.2f} w={bb.get('width',0):8.2f} h={bb.get('height',0):8.2f}")
    if rb:
        parts.append(f"  ink  x={rb.get('x',0):9.2f} y={rb.get('y',0):9.2f} w={rb.get('width',0):8.2f} h={rb.get('height',0):8.2f}")
    rt = n.get("relativeTransform")
    if rt:
        det = rt[0][0] * rt[1][1] - rt[0][1] * rt[1][0]
        rot = math.degrees(math.atan2(rt[1][0], rt[0][0]))
        if abs(rot) > .01 or det < 0:
            parts.append(f"  xform rot={rot:+.3f}deg det={det:+.4f}  matrix=[{rt[0][0]:+.4f} {rt[0][1]:+.4f}; {rt[1][0]:+.4f} {rt[1][1]:+.4f}]")
    lay = " ".join(f"{k}={n[k]}" for k in LAYOUT_KEYS if n.get(k) not in (None, 0, False, "NONE"))
    if lay:
        parts.append("  lay  " + lay)
    fl = fmt_fill(n)
    if fl:
        parts.append(f"  fill {fl}")
    for st in (n.get("strokes") or []):
        if st.get("visible") is not False and st["type"] == "SOLID":
            c = st["color"]
            parts.append("  strk #%02x%02x%02x w=%s align=%s" % (
                round(c["r"] * 255), round(c["g"] * 255), round(c["b"] * 255),
                n.get("strokeWeight"), n.get("strokeAlign")))
            break
    if n["type"] == "TEXT":
        s = n.get("style", {})
        parts.append(f"  type fs={s.get('fontSize')} lh={s.get('lineHeightPx')} ls={s.get('letterSpacing')} w={s.get('fontWeight')} "
                     f"align={s.get('textAlignHorizontal')}/{s.get('textAlignVertical')} case={s.get('textCase','-')} fam={s.get('fontFamily')}")
        txt = n["characters"].replace(" ", "<U+2028>").replace("\n", "<NL>")
        parts.append(f"  text «{txt[:150]}»")
        ov = n.get("characterStyleOverrides") or []
        if any(ov):
            tbl = n.get("styleOverrideTable") or {}
            parts.append(f"  ovr  {len(set(ov)-{0})} override run(s): " +
                         "; ".join(f"{k}={v}" for k, v in tbl.items()))
    if parent_box and bb:
        parts.append(f"  rel  dx={bb.get('x',0)-parent_box['x']:+8.2f} dy={bb.get('y',0)-parent_box['y']:+8.2f}"
                     f"  w%={100*bb.get('width',0)/parent_box['width']:6.2f}  h%={100*bb.get('height',0)/parent_box['height']:6.2f}")
    return "\n".join(parts)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    depth = 0
    for a in sys.argv[1:]:
        if a.startswith("--depth="):
            depth = int(a.split("=")[1])
    if len(args) < 2:
        sys.exit(__doc__)
    path = resolve(args[0])
    pat = args[1]
    rx = re.compile(pat, re.I)
    # Instance children carry a composite id ("I237:12777;237:15247;237:14468"),
    # so a bare "237:14468" has to match the LAST segment, not the whole string.
    is_id = re.fullmatch(r"I?[\d:;\-]+", pat)
    want_id = pat.replace("-", ":")
    print(f"# board: {os.path.basename(path)}\n")

    hits = []

    def walk(n, chain, parent):
        name = n.get("name", "")
        if is_id:
            ok = n["id"] == want_id or n["id"].split(";")[-1] == want_id
        else:
            ok = rx.search(name) or (n["type"] == "TEXT" and rx.search(n.get("characters", "")))
        if ok:
            hits.append((n, chain, parent))
        for c in n.get("children") or []:
            walk(c, chain + [name], n)

    for r in load(path):
        walk(r, [], None)

    if not hits:
        print("no match")
        return
    for n, chain, parent in hits:
        print("  > ".join(x[:22] for x in chain[-4:]) or "(root)")
        pb = (parent or {}).get("absoluteBoundingBox") if parent else None
        print(describe(n, pb))
        if depth or "--tree" in flags:

            def sub(m, d):
                if d > (depth or 2) or m.get("visible") is False:
                    return
                for c in m.get("children") or []:
                    bb = c.get("absoluteBoundingBox") or {}
                    s = c.get("style", {}) if c["type"] == "TEXT" else {}
                    ex = f" fs={s.get('fontSize')} lh={s.get('lineHeightPx')} ls={s.get('letterSpacing')}" if s else ""
                    lay = " ".join(f"{k}={c[k]}" for k in LAYOUT_KEYS if c.get(k) not in (None, 0, False, "NONE"))
                    txt = ""
                    if c["type"] == "TEXT":
                        txt = " «" + c["characters"].replace(" ", "|").replace("\n", "|")[:34] + "»"
                    print("      " + "  " * d + f"{c['type']:<8} {c.get('name','')[:26]:<26} "
                          f"w={bb.get('width',0):7.2f} h={bb.get('height',0):7.2f} {c['id']}{ex} {lay}{txt}")
                    sub(c, d + 1)

            sub(n, 0)
        print()


main()
