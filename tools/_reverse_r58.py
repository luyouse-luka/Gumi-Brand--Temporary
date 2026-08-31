# -*- coding: utf-8 -*-
"""Rebuild the pre-round state by applying round 56's (old, new) pairs backwards."""
import ast, sys
tree = ast.parse(open("tools/_apply_r58.py", encoding="utf-8").read())
edits = None
for node in ast.walk(tree):
    if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "EDITS":
        edits = ast.literal_eval(node.value)
if not edits:
    sys.exit("no EDITS found")
s = open("assets/customstyle.scss", encoding="utf-8").read()
for old, new, cnt in reversed(edits):
    if s.count(new) != cnt:
        sys.exit("cannot reverse (count=%d): %s" % (s.count(new), new.strip().splitlines()[0][:70]))
    s = s.replace(new, old, cnt)
open("assets/customstyle.scss", "w", encoding="utf-8").write(s)
print("reversed %d scss edits" % len(edits))
