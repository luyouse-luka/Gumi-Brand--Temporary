# -*- coding: utf-8 -*-
"""Rebuild the pre-round state by applying round 54's (old, new) pairs backwards.

Reverse order matters: a later pair's `new` is often an earlier pair's context.
"""
import ast, sys

def edits_of(path, name="EDITS"):
    tree = ast.parse(open(path, encoding="utf-8").read())
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == name:
            try: return ast.literal_eval(node.value)
            except ValueError: return None
    return None

def undo(path, edits, what):
    s = open(path, encoding="utf-8").read()
    for old, new, cnt in reversed(edits):
        if s.count(new) != cnt:
            sys.exit("cannot reverse %s (count=%d): %s" % (what, s.count(new), new.strip().splitlines()[0][:70]))
        s = s.replace(new, old, cnt)
    open(path, "w", encoding="utf-8").write(s)
    print("reversed %d %s edits" % (len(edits), what))

undo("assets/customstyle.scss", edits_of("tools/_apply_r56.py"), "scss")

# the js file builds its EDITS with .append(), so it is not a literal
src = open("tools/_apply_r56_js.py", encoding="utf-8").read()
tree = ast.parse(src)
js = []
for node in ast.walk(tree):
    if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
            and node.func.attr == "append" and getattr(node.func.value, "id", "") == "EDITS"):
        js.append(ast.literal_eval(node.args[0]))
if len(js) != 4:
    sys.exit("expected 4 js pairs, found %d" % len(js))
undo("assets/main.js", js, "js")

p = "get-in-touch.html"
h = open(p, encoding="utf-8").read()
new = 'name="enquiry" required data-select>'
if h.count(new) != 1:
    sys.exit("cannot reverse html")
open(p, "w", encoding="utf-8").write(h.replace(new, 'name="enquiry" required>', 1))
print("reversed html")
