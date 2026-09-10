#!/usr/bin/env python3
"""account.scss hover/transition parity (global rule 13).

Writing a hover with no transition is the most common way to ship a half-done
interactive state: the colour still changes, it just snaps. This pairs them up
per rule block -- every property a hover block assigns has to appear in that
same block's own `transition`, because a transition on an ancestor does not
reach a descendant's own property change.

`transition: trans(a, b)` is the house helper; it expands to `a $t-base
$ease-out, b $t-base $ease-out`, so the property names are the arguments.
"""
import re, sys, pathlib

SRC = pathlib.Path(__file__).resolve().parent.parent / "assets" / "account.scss"

# properties whose change needs no easing to read correctly
EXEMPT = {"cursor", "pointer-events", "z-index", "text-decoration",
          "text-decoration-line", "visibility", "content", "display",
          "background-image", "outline-offset", "font-weight", "font-family",
          "transition", "transition-duration", "will-change",
          # link-underline flips the origin so the rule wipes out the way it came
          # in; the origin itself is meant to jump, the scaleX beside it eases
          "transform-origin"}
# `background: <colour>` is a shorthand for background-color, and a
# `transition: background-color` covers it
ALIAS = {"background": "background-color", "border": "border-color"}
LEAF = re.compile(r"(:{1,2}[\w-]+(\([^)]*\))?|\[[^\]]*\])+$")
DECL = re.compile(r"^(-{0,2}[a-z][\w-]*)\s*:\s*(.+)$", re.S)


def strip(t):
    t = re.sub(r"/\*.*?\*/", "", t, flags=re.S)
    return re.sub(r"//[^\n]*", "", t)


def blocks(text):
    """Yield (selector-path, list of (prop, value), inside_hover) per brace block."""
    out, stack, buf = [], [], []
    for ch in text:
        if ch in "{};":
            head = " ".join("".join(buf).split()); buf = []
            if ch == "{":
                kind = "hover" if re.match(r"@include\s+hover\b", head) else (
                       "at" if head.startswith("@") else "sel")
                stack.append([kind, head, []])
            elif ch == "}":
                if stack:
                    k, h, decls = stack.pop()
                    path = " ".join(x[1] for x in stack if x[0] == "sel")
                    out.append((path if k == "hover" else (path + " " + h).strip(),
                                decls, k == "hover" or
                                any(x[0] == "hover" for x in stack)))
            else:
                m = DECL.match(head)
                if m and not head.startswith(("@", "$")) and stack:
                    stack[-1][2].append((m.group(1), m.group(2)))
        else:
            buf.append(ch)
    return out


def leaf(path):
    """Owner of the property a hover block changes.

    Two shapes both land here: a hover on an ancestor changing a descendant's
    property (take the descendant), and a nested `&:not(...)` (which owns
    nothing of its own -- walk back to the class it qualifies).
    """
    parts = path.split()
    while parts:
        last = parts[-1].lstrip("&")
        base = LEAF.sub("", last)
        if base:
            return base
        parts = parts[:-1]
    return path


def transition_props(decls):
    props = set()
    for p, v in decls:
        if p not in ("transition", "transition-property"):
            continue
        m = re.search(r"trans\(([^)]*)\)", v)
        if m:
            props |= {a.strip() for a in m.group(1).split(",") if a.strip()}
        else:
            for part in v.split(","):
                w = part.strip().split()
                if w:
                    props.add(w[0])
    return props


def main():
    text = strip(SRC.read_text())
    bl = blocks(text)
    # transition set per selector path, merged across that path's own blocks
    trans = {}
    for path, decls, in_hover in bl:
        if in_hover:
            continue
        got = transition_props(decls)
        if got:
            trans.setdefault(path, set()).update(got)
            trans.setdefault(leaf(path), set()).update(got)

    red = ok = 0
    for path, decls, in_hover in bl:
        if not in_hover:
            continue
        have = trans.get(path, set()) | trans.get(leaf(path), set())
        for p, v in decls:
            if p in EXEMPT or p.startswith("--"):
                continue
            p = ALIAS.get(p, p)
            if p in have or ALIAS.get(p, p) in have or "all" in have:
                ok += 1
            else:
                print("RED  hover with no transition  %s { %s }" % (path or "(root)", p))
                red += 1
    print("\n%d hover properties covered / %d red" % (ok, red))
    sys.exit(1 if red else 0)


main()
