# -*- coding: utf-8 -*-
"""Rebuild the pre-round state by applying round 55's (old, new) pairs backwards.

Reverse order matters: a later pair's `new` is often an earlier pair's context.
"""
import ast, sys

def literal_edits(path):
    tree = ast.parse(open(path, encoding="utf-8").read())
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "EDITS":
            return ast.literal_eval(node.value)
    return None

def appended_edits(path):
    tree = ast.parse(open(path, encoding="utf-8").read())
    out = []
    for node in ast.walk(tree):
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and node.func.attr == "append" and getattr(node.func.value, "id", "") == "EDITS"):
            out.append(ast.literal_eval(node.args[0]))
    return out

def undo(path, edits, what):
    s = open(path, encoding="utf-8").read()
    for old, new, cnt in reversed(edits):
        if s.count(new) != cnt:
            sys.exit("cannot reverse %s (count=%d): %s" % (what, s.count(new), new.strip().splitlines()[0][:70]))
        s = s.replace(new, old, cnt)
    open(path, "w", encoding="utf-8").write(s)
    print("reversed %d %s edits" % (len(edits), what))

undo("assets/customstyle.scss", literal_edits("tools/_apply_r57.py"), "scss")

js = appended_edits("tools/_apply_r57_js.py")
if len(js) != 4:
    sys.exit("expected 4 js pairs, found %d" % len(js))
undo("assets/main.js", js, "js")

n = 0
for p in ("get-in-touch.html", "referral.html"):
    h = open(p, encoding="utf-8").read()
    new = ' name="country" data-select="bare">'
    if h.count(new) != 1:
        sys.exit("cannot reverse html: " + p)
    open(p, "w", encoding="utf-8").write(h.replace(new, ' name="country">', 1))
    n += 1
print("reversed html on %d pages" % n)
