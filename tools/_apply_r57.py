# -*- coding: utf-8 -*-
"""Round 55 (build r57) -- exact-match SCSS edits with a count assertion each."""
import sys
P = "/home/ly/project/Gumi-Brand/assets/customstyle.scss"
s = open(P, encoding="utf-8").read()

EDITS = [

# --- I (closed)  pc centred, phones NOT centred -- r56's centring is withdrawn ---
("""  // Client-set, reversing r51: `margin: 0 auto` survives every tier, so the list
  // is dead centre. The 15 on the right has to go with the override -- one auto
  // margin against a fixed one hangs the box to the RIGHT, which is what 390
  // measured before r51 (24.4 left / 15 right). The board itself hangs the list
  // 7.5 left of centre; that is what r51 reproduced. Reopens decision I.
}""",
 """  // Client-set, FINAL (r57 withdraws r56 and restores r51): centred on pc, not
  // centred on phones. Dropping the auto left margin hands centring to the
  // parent's align-items, and the 15 on the right then pushes the box 7.5 left
  // of centre -- the board's own "hangs slightly left of centre". Decision I is
  // closed on this answer; do not "fix" it back to dead centre.
  @include narrow { margin-right: 15px; margin-left: 0; }
  // margin-left has to be zeroed HERE TOO, which r51 did not do: one auto margin
  // against a fixed one absorbs the slack the other way, so this tier hung RIGHT
  // (768 measured +30.7 from centre, 1280 +43.7) between a phone tier hanging
  // left and a centred pc tier. Zeroed, the 15 ramps to 0 and the ends meet.
  @include tablet { margin-right: fluid(15px, 0px); margin-left: 0; }
}""", 1),

# --- AV  the phone field's country code gets the same drawn control ---
("""  // Keyboard position. The list holds focus and moves aria-activedescendant, so
  // there is no :focus on an option to style.
  &.is-active {
    background: $c-lime-150;
    color: $c-green;
  }
}""",
 """  // Keyboard position. The list holds focus and moves aria-activedescendant, so
  // there is no :focus on an option to style.
  &.is-active {
    background: $c-lime-150;
    color: $c-green;
  }
}

// Client-set: the phone field's country code is the same widget (data-select
// "bare"). It sits inside .gb-field__phone's own border, so the trigger carries
// no box -- only the typography the native select had.
.gb-select--bare {
  .gb-select__button {
    gap: 3px;              // the native drew a 20 chevron inside a 23 padding-right
    padding-right: 0;
    font-family: $font-brand-stack;
    font-size: 16px;
    line-height: 24px;
    letter-spacing: -0.32px;
    color: $c-gray-700;
    transition: trans(color);

    @include hover { color: $c-ink; }
  }

  // Hang the list off the phone FIELD's bottom edge, not off the trigger: the
  // trigger is a 24 line box centred in a 22 content box, so its own 100% stops
  // 10px short of the field's border edge. 10 + the default 4 gap = 14.
  // Left-aligned and content-wide -- the trigger is only as wide as "AU".
  .gb-select__list {
    top: calc(100% + 14px);
    left: 0;
    right: auto;
    width: max-content;
    min-width: 100%;
  }
}""", 1),

# --- AV (cont.)  the hidden native must not keep the phone block's padding ---
('  select {\n    appearance: none;\n    border: 0;\n    background: transparent;\n    padding-right: 23px;',
 "  // :not() so the hidden native underneath the drawn control does not keep this\n  // block's 23 padding-right -- .gb-select__native's visually-hidden is only\n  // 0-1-0 and would lose to `.gb-field__phone select` (measured 23px wide, not 1).\n  // The fallback path is unaffected: with no script there is no .gb-select__native.\n  select:not(.gb-select__native) {\n    appearance: none;\n    border: 0;\n    background: transparent;\n    padding-right: 23px;", 1),

# --- build bump ---
('$build: "20260831-r56";', '$build: "20260831-r57";', 1),
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
