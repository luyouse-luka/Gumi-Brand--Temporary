# -*- coding: utf-8 -*-
"""Rebuild the pre-round state by applying tools/_apply_r55.py's pairs backwards."""
import ast, glob, sys, os

src = open("tools/_apply_r55.py", encoding="utf-8").read()
tree = ast.parse(src)
edits = None
for node in ast.walk(tree):
    if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "EDITS":
        edits = ast.literal_eval(node.value)
if not edits:
    sys.exit("no EDITS found")

s = open("assets/customstyle.scss", encoding="utf-8").read()
n = 0
for old, new, cnt in reversed(edits):
    if s.count(new) != cnt:
        sys.exit("cannot reverse (count=%d): %s" % (s.count(new), new.strip().splitlines()[0][:70]))
    s = s.replace(new, old, cnt)
    n += 1
open("assets/customstyle.scss", "w", encoding="utf-8").write(s)

# js
j = open("assets/main.js", encoding="utf-8").read()
NEW_JS = """      // Focus the dialog, not its first control. FOCUSABLE lands on the close
      // button, and a script focus with no pointer input before it still counts
      // as :focus-visible -- the ring painted itself the moment the modal
      // appeared. The container carries tabindex="-1" and has rings turned off.
      el.focus();"""
OLD_JS = """      var first = el.querySelector(FOCUSABLE);
      if (first) first.focus();"""
assert j.count(NEW_JS) == 1
open("assets/main.js", "w", encoding="utf-8").write(j.replace(NEW_JS, OLD_JS, 1))

# html
for p in sorted(glob.glob("*.html")):
    h = open(p, encoding="utf-8").read()
    o = h
    h = h.replace('role="dialog" aria-modal="true" tabindex="-1"', 'role="dialog" aria-modal="true"')
    h = h.replace('<div class="gb-rich-page__inner wowo fadeInUp">', '<div class="gb-rich-page__inner">')
    if h != o:
        open(p, "w", encoding="utf-8").write(h)
print("reversed %d scss edits + js + html" % n)
