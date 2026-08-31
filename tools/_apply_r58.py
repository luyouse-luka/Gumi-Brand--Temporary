# -*- coding: utf-8 -*-
"""Round 56 (build r58) -- exact-match SCSS edits with a count assertion each."""
import sys
P = "/home/ly/project/Gumi-Brand/assets/customstyle.scss"
s = open(P, encoding="utf-8").read()

EDITS = [

# --- white card's vertical scallop hangs further out, like the green one ---
("""  // Client-set. The white card keeps the symmetric -63 (half of the 126 box);
  // this one hangs further out, leaving 31 of the scallop inside the card.
  .gb-promo-card__lip--v { right: -95px; }
}

.gb-promo-card--white {
  .gb-promo-card__lip { color: $c-white; }
  .gb-promo-card__lip--v { left: -63px; }
}""",
 """  // Client-set. Both cards now hang the scallop further out than the symmetric
  // -63 (half of the 126 box): this one leaves 31 of it inside, the white card 26.
  .gb-promo-card__lip--v { right: -95px; }
}

.gb-promo-card--white {
  .gb-promo-card__lip { color: $c-white; }
  // Client-set r58 (-63 -> -100): 26 of the 126 box bites into the cream half,
  // matching the green card's 31. Deliberately untiered -- .gb-promo-card__lip--v
  // is display:none below 768, so this one declaration IS every tier that paints
  // it, and the bite stays 26 from 768 to 1440 while the card itself shrinks.
  // The phone tier draws .gb-promo-card__lip--h instead and is NOT affected.
  .gb-promo-card__lip--v { left: -100px; }
}""", 1),

# --- build bump ---
('$build: "20260831-r57";', '$build: "20260831-r58";', 1),
]

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
print("scss: %d edits applied" % len(EDITS))
