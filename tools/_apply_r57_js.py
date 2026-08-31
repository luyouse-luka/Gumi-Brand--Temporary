# -*- coding: utf-8 -*-
"""Round 55 (build r57) -- main.js edits: the drawn select grows a `bare` variant."""
import sys
P = "/home/ly/project/Gumi-Brand/assets/main.js"
s = open(P, encoding="utf-8").read()

EDITS = []

# 1) variant + aria-label fallback
EDITS.append(("""      var self = this;
      var id = native.id || ("gb-select-" + this.boxes.length);

      var wrap = document.createElement("div");
      wrap.className = "gb-select";""",
"""      var self = this;
      var id = native.id || ("gb-select-" + this.boxes.length);
      // "bare" = the phone field's country code: same widget with no box of its
      // own, because .gb-field__phone already draws the border around it.
      var bare = native.getAttribute("data-select") === "bare";
      var aria = native.getAttribute("aria-label");

      var wrap = document.createElement("div");
      wrap.className = bare ? "gb-select gb-select--bare" : "gb-select";""", 1))

EDITS.append(("""      btn.className = "gb-field__input gb-field__input--select gb-select__button";""",
              """      btn.className = bare ? "gb-select__button"
                           : "gb-field__input gb-field__input--select gb-select__button";""", 1))

# 2) a bare control has no <label for>, only aria-label -- carry it over
EDITS.append(("""        label.addEventListener("click", function () { btn.focus(); });
        btn.setAttribute("aria-labelledby", label.id + " " + btn.id);
      }""",
"""        label.addEventListener("click", function () { btn.focus(); });
        btn.setAttribute("aria-labelledby", label.id + " " + btn.id);
      } else if (aria) {
        btn.setAttribute("aria-label", aria);
      }""", 1))

EDITS.append(("""      if (label) { list.setAttribute("aria-labelledby", label.id); }""",
              """      if (label) { list.setAttribute("aria-labelledby", label.id); }
      else if (aria) { list.setAttribute("aria-label", aria); }""", 1))

fails = []
for old, new, n in EDITS:
    c = s.count(old)
    if c != n:
        fails.append((c, n, old.strip().splitlines()[0][:80]))
        continue
    s = s.replace(old, new, n)
if fails:
    for c, n, head in fails:
        print("MISMATCH count=%d expected=%d :: %s" % (c, n, head))
    sys.exit(1)
open(P, "w", encoding="utf-8").write(s)
print("js: %d edits applied" % len(EDITS))
