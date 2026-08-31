# -*- coding: utf-8 -*-
"""Round 54 (build r56) -- exact-match SCSS edits with a count assertion each."""
import sys
P = "/home/ly/project/Gumi-Brand/assets/customstyle.scss"
s = open(P, encoding="utf-8").read()

EDITS = [

# --- AQ  promo list keeps its auto margins at every width (reverses r51) ---
("""  // The phone board hangs the list slightly left of centre. Client-set: drop the
  // auto left margin below 768. With no auto margin left the parent's
  // align-items: center takes over, and the 15 on the right pushes the box 7.5
  // left of centre — which is the board's intent. Until now the lone auto left
  // margin ate all the slack and hung it to the RIGHT instead (390: 24.4 left /
  // 15 right). Closes decision I.
  @include narrow { margin-right: 15px; margin-left: 0; }
  @include tablet { margin-right: fluid(15px, 0px); }
}""",
 """  // Client-set, reversing r51: `margin: 0 auto` survives every tier, so the list
  // is dead centre. The 15 on the right has to go with the override -- one auto
  // margin against a fixed one hangs the box to the RIGHT, which is what 390
  // measured before r51 (24.4 left / 15 right). The board itself hangs the list
  // 7.5 left of centre; that is what r51 reproduced. Reopens decision I.
}""", 1),

# --- AR  the promo panel is only full-screen on phones ---
("""  justify-content: center;
  pointer-events: none;

  @include pc { padding: 24px; }
}""",
 """  justify-content: center;
  pointer-events: none;

  // Client-set: the panel floats from 768 up, so the gutter starts there too.
  @include tablet { padding: 24px; }
  @include pc { padding: 24px; }
}""", 1),

("""  @include pc {
    flex-direction: row;
    justify-content: flex-start;
    width: 1062px;
    height: 528px;
    max-width: 100%;
    max-height: 100%;
    border-radius: $r-xl;
  }
}""",
 """  // Client-set: full-screen is for phones only. 768-1280 has no board, and
  // shrinking the desktop card is not an option -- its two 531 columns carry the
  // bear art at px offsets solved for that width, so a narrower column crops it.
  // This tier shows the PHONE board at its own size instead: 285:19373 is
  // 390x744 and every value in the stacked layout (art 252, the bears, the 71
  // wave inset) is already solved for 390, space-between included -- 744 - 460 -
  // 252 is the board's own 32 gap. Width and tier are decision AT.
  @include tablet {
    width: 390px;
    height: 744px;
    max-height: 100%;
    border-radius: $r-xl;
  }

  @include pc {
    flex-direction: row;
    justify-content: flex-start;
    width: 1062px;
    height: 528px;
    max-width: 100%;
    max-height: 100%;
    border-radius: $r-xl;
  }
}""", 1),

# --- AS  the enquiry select becomes a button + ul listbox ---
("""  // appearance:none takes the UA's hover highlight with it, so without this the
  // control gives no feedback until it is focused.
  @include hover { border-color: $c-gray-500; }
}

.gb-field__input--area {""",
 """  // appearance:none takes the UA's hover highlight with it, so without this the
  // control gives no feedback until it is focused.
  @include hover { border-color: $c-gray-500; }
}

// Client-set: draw the enquiry select as a button + ul listbox (main.js
// selectBox) so the chevron can rotate -- a native popup paints itself and a
// background-image cannot be transformed. The native control stays in the DOM
// underneath as the form's value carrier; with the script dead it is simply
// still visible and nothing here applies.
.gb-select {
  position: relative;
  z-index: $z-base;

  &.is-open { z-index: $z-sticky; }   // the open list has to clear the fields below
}

// visually-hidden, NOT display:none -- the same reason as .gb-form__check: the
// control still has to submit, validate and answer enquiryPrefill.
.gb-select__native { @include visually-hidden; }

.gb-select__button {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  // The chevron is an element now; the 40 that made room for the painted one
  // would count twice. 14 is the board's own gap to the right edge.
  padding-right: 14px;
  background-image: none;
  text-align: left;

  &[aria-expanded="true"] { border-color: $c-green; }
}

.gb-select__value {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.gb-select__arrow {
  flex: 0 0 20px;
  width: 20px;
  height: 20px;
  transition: trans(transform);

  .gb-select.is-open & { transform: rotate(180deg); }
}

.gb-select__list {
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  right: 0;
  z-index: 1;
  max-height: 224px;
  margin: 0;
  padding: 4px;
  overflow-y: auto;
  list-style: none;
  background: $c-white;
  border: 1px solid $c-gray-300;
  border-radius: $r-sm;
  box-shadow: 0 4px 12px $c-ink-05;

  // visibility, not display: display cannot transition, and the closed list must
  // stay out of hit-testing while the fade runs.
  opacity: 0;
  visibility: hidden;
  transform: translateY(-4px);
  transition: trans(opacity, transform), visibility 0s linear $t-base;

  &:focus-visible { outline: none; }   // the ring belongs on the active option

  .gb-select.is-open & {
    opacity: 1;
    visibility: visible;
    transform: none;
    transition: trans(opacity, transform), visibility 0s;
  }
}

.gb-select__option {
  padding: 8px 10px;
  border-radius: $r-xs;
  cursor: pointer;
  transition: trans(background-color, color);

  @include hover { background: $c-lime-100; }

  &[aria-selected="true"] { color: $c-green; }

  // Keyboard position. The list holds focus and moves aria-activedescendant, so
  // there is no :focus on an option to style.
  &.is-active {
    background: $c-lime-150;
    color: $c-green;
  }
}

.gb-field__input--area {""", 1),

# --- AR (cont.)  the pinned card's wave is pinned too ---
('  @include pc {\n    order: 0;\n    width: 531px;\n    height: 100%;\n    background: $c-cream;\n\n    &::before,\n    &::after { content: none; }\n  }\n}',
 "  // The card is pinned to the phone board's 390 in this tier, so its wave has to\n  // be pinned with it: --sc-w is a viewport ramp, and an unpinned one draws a\n  // desktop-scale wave inside a phone-size card (1280 measured a 268.8 pitch\n  // against the board's 144.85). 144.64 is the ramp's own floor, i.e. the value\n  // every phone width already resolves to.\n  @include tablet { --sc-w: 144.64px; }\n\n  @include pc {\n    order: 0;\n    width: 531px;\n    height: 100%;\n    background: $c-cream;\n\n    &::before,\n    &::after { content: none; }\n  }\n}", 1),

# --- build bump ---
('$build: "20260828-r55";', '$build: "20260831-r56";', 1),
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
