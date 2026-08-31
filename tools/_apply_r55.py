# -*- coding: utf-8 -*-
"""Round 53 (build r55) -- exact-match SCSS edits with a count assertion each."""
import sys
P = "/home/ly/project/Gumi-Brand/assets/customstyle.scss"
s = open(P, encoding="utf-8").read()

EDITS = [

# --- G2.1  promo artwork no longer grows into the scallop on sub-390 phones ---
("""  @include narrow { width: 303px; }
  @include tablet { width: fluid(303px, 427px); }""",
 """  // 303 is the 390 board value. The art half is aspect-ratio 1 and shrinks with
  // the card, but a fixed 303 does not, so below ~380 the picture (110% tall and
  // pulled up 8%) runs into .gb-promo-card__lip--h sitting at the half's bottom.
  // 303/350 keeps 390 and every wider phone byte-identical and scales under it.
  @include narrow { width: min(303px, 86.571%); }
  @include tablet { width: fluid(303px, 427px); }""", 1),

# --- G2.3  vs table runs full width on phones ---
("""  @include narrow {
    flex-direction: column;
    gap: 16px;
    width: 100%;
    max-width: 400px;
    margin-inline: auto;
  }
}""",
 """  @include narrow {
    flex-direction: column;
    gap: 16px;
    width: 100%;
    max-width: 400px;
    margin-inline: auto;
  }
  // Client-set: full width on phones. It must stay inside `mobile` and after the
  // narrow block (same specificity, source order decides): .gb-vs__bear is a
  // percentage of this box and its right edge lands at 103.2% of it, so an
  // uncapped table pushes the bear off screen from ~660 up (767 measured a
  // 771px document in a 767px window).
  @include mobile { max-width: 100%; }
}""", 1),

# --- G2.6a  bear meter fills the card on phones ---
("""  grid-template-columns: repeat(20, 1fr);
  gap: 8px 4px;
  width: 100%;
  max-width: 347px;
}""",
 """  grid-template-columns: repeat(20, 1fr);
  gap: 8px 4px;
  width: 100%;
  max-width: 347px;

  @include narrow { max-width: 100%; }   // client-set
}""", 1),

# --- G2.6b  drawer CTA gets a cap ---
("""  @include narrow { width: 100%; order: 2; }
}""",
 """  @include narrow { width: 100%; order: 2; }

  // The drawer is full-bleed, so without a cap this button ran the whole 727 at
  // 767. No board value exists (390 draws it at the full 350); 520 is the same
  // cap .gb-product__cta carries, and 390 stays under it either way. Left-
  // aligned on purpose -- an auto margin would centre it away from the links.
  .gb-btn.gb-btn--lg { max-width: 520px; }
}""", 1),

# --- G2.7a  footer newsletter cap on phones ---
("""  @include narrow { width: 100%; margin-top: 16px; }
}""",
 """  @include narrow { width: 100%; max-width: 340px; margin-top: 16px; }   // client-set
}""", 1),

# --- G2.7b  deco bear b: top as a percentage ---
("""  // right as a percentage on the client's ask (28 / 390 = 7.18%), matching what
  // --a and the base rule already do. top stays in px on purpose: it resolves
  // against .gb-footer-cta-wrap, whose height is the CTA's copy block, not a
  // design constant -- one extra line of type (or the licensed PP Palma, 4.7%
  // wider than the trial) would slide a percentage bear down with it.
  @include narrow { width: 188px; right: 7.18%; top: 457px; }
  @include tablet { top: fluid(300px, 408px); }""",
 """  // right as a percentage on the client's ask (28 / 390 = 7.18%), matching what
  // --a and the base rule already do.
  @include narrow { width: 188px; right: 7.18%; top: 87.211%; }
  // px here on purpose: fluid() interpolates with calc() and a percentage cannot
  // be ramped that way. 768-1280 therefore keeps the old absolute ramp.
  @include tablet { top: fluid(300px, 408px); }""", 1),

(""".gb-deco-bear--b {
  right: 3.41%;
  top: 408px;
  width: 440px;""",
 """// Client-set: top as a percentage. ⚠ It resolves against .gb-footer-cta-wrap,
// whose height is the CTA copy block rather than a design constant, so the bear
// now moves with the copy. Both values are anchored on their own board and are
// exact there (1440: 408/573.94; 390: 457/524.02); away from the boards the bear
// drifts -- measured -7.4 at 1281 and up to +56 at 320. See PROJECT-STATUS AK.
.gb-deco-bear--b {
  right: 3.41%;
  top: 71.087%;
  width: 440px;""", 1),

# --- G2.8  ink outline radius: fill the counters ---
("""  text-shadow: ink-outline(0.125em, $c-lime);   // Figma: 7px @ 56px""",
 """  // Client-set: 0.125em (Figma's 7px @ 56px) left the page ground showing inside
  // the 0 and in the notch between "50" and "%" -- the counter's inscribed circle
  // is wider than the dilation radius. 0.145em is the smallest step that closes
  // every hole (measured: 272 stray px at 0.125, 61 at 0.135, 0 at 0.145) and
  // grows the outline by 1.1px at 56. em, so the phone tier scales with it.
  text-shadow: ink-outline(0.145em, $c-lime);""", 1),

# --- G3.1a  tight science group: cards pushed down ---
("""  .gb-science__inner { gap: 22px; }
  @include narrow { .gb-science__inner { gap: 48px; } }   // client-set
  @include tablet { .gb-science__inner { gap: fluid(32px, 22px); } }""",
 """  .gb-science__inner { gap: 22px; }
  @include narrow { .gb-science__inner { gap: 48px; } }   // client-set
  @include tablet { .gb-science__inner { gap: fluid(32px, 22px); } }

  // Client-set, and it stacks on the gap above rather than replacing it: 22 + 26
  // at desktop, 48 + 26 on phones.
  .gb-science__cards { margin-top: 26px; }""", 1),

# --- G3.1b  card copy gets its own top margin ---
(""".gb-science-card__text {
  font-size: 16px;""",
 """.gb-science-card__text {
  // Client-set, unscoped in the brief while the line above it named the tight
  // group explicitly -- so it applies to all six cards, index included.
  margin-top: 6px;
  font-size: 16px;""", 1),

# --- G3.1c  figure drops to 36/40 on phones ---
("""  text-shadow: ink-outline(0.145em, $c-lime);
  // Client-set: 56/44 at every width, phone included -- one spec for both card
  // groups. 228:5932 says 56/44 and the mobile boards disagree (36/40 on the
  // nutrient cards), which is why neither group carries a narrow tier now.
}""",
 """  text-shadow: ink-outline(0.145em, $c-lime);

  // Client-set, and it reverses the earlier "56/44 at every width" call: the
  // phone tier now matches what 324:58044 draws on the nutrient cards. ls is
  // given as -1%, which CSS has no unit for -- -0.36px is that at 36.
  // The tablet ramp is not in the brief; without it 767/768 would jump 36 -> 56.
  @include narrow { font-size: 36px; line-height: 40px; letter-spacing: -0.36px; }
  @include tablet {
    font-size: fluid(36px, 56px);
    line-height: fluid(40px, 44px);
    letter-spacing: fluid(-0.36px, 0px);
  }
}""", 1),

# --- G3.2  faq image body drops its gutter below the desktop board ---
("""    gap: 32px;
    padding-inline: 0;
  }
  @include tablet { gap: fluid(32px, 16px); }
}""",
 """    gap: 32px;
    padding-inline: 0;
  }
  // Client-set: the 32 gutter is a desktop-board value only. narrow already
  // zeroed it, so this carries the same call across 768-1280.
  @include tablet { gap: fluid(32px, 16px); padding-inline: 0; }
}""", 1),

# --- G3.5  checkbox: hide the native control, draw it on ::before ---
("""  input[type="checkbox"] {
    flex: 0 0 20px;
    width: 20px;
    height: 20px;
    margin-top: 2px;
    accent-color: $c-green;
  }

  a {
    color: $c-ink;
    text-decoration: underline;
    transition: trans(color);

    @include hover { color: $c-green; }
  }
}""",
 """  // The native box paints its accent-color instantly -- transition never applies
  // to it. Client-set: hide the input and draw the box on ::before instead.
  // visually-hidden, NOT display:none: the latter drops the control out of the
  // tab order and takes the browser's required-field message with it.
  &::before {
    content: "";
    flex: 0 0 20px;
    width: 20px;
    height: 20px;
    margin-top: 2px;
    border: 1px solid $c-gray-300;
    border-radius: 4px;
    background: $c-white no-repeat center / 12px 12px;
    transition: trans(background-color, border-color);
  }

  input[type="checkbox"] { @include visually-hidden; }

  a {
    color: $c-ink;
    text-decoration: underline;
    transition: trans(color);

    @include hover { color: $c-green; }
  }
}

// Flat, not nested: the drawn box is a pseudo-element of the label, so the state
// has to be read off the input from the label itself.
.gb-form__check:has(input[type="checkbox"]:checked)::before {
  background-color: $c-green;
  border-color: $c-green;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12' fill='none'%3E%3Cpath d='M10 3L4.5 8.5L2 6' stroke='%23ffffff' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
}

// The real control is off-screen, so its focus ring would be too.
.gb-form__check:has(input[type="checkbox"]:focus-visible)::before {
  outline: 2px solid $c-green;
  outline-offset: 2px;
}""", 1),

# --- G3.6  note link underline ---
("""  a {
    font-weight: 500;
    color: $c-ink;
    transition: trans(color);

    @include hover { color: $c-green; }
  }
}

.gb-form__disclaimer {""",
 """  a {
    font-weight: 500;
    color: $c-ink;
    text-decoration: underline;   // client-set
    transition: trans(color);

    @include hover { color: $c-green; }
  }
}

.gb-form__disclaimer {""", 1),

# --- G3.7  disclaimer margin on phones ---
("""  @include narrow { font-size: 16px; line-height: 24px; letter-spacing: -0.32px; margin: 16px 0; }
  @include tablet {
    font-size: fluid(16px, 14px); line-height: fluid(24px, 20px); letter-spacing: fluid(-0.32px, -0.28px);
    margin: fluid(16px, 0px) 0;
  }""",
 """  // client-set margin (was 16px 0); the -2 bottom pulls the block back onto the
  // submit button's own spacing
  @include narrow { font-size: 16px; line-height: 24px; letter-spacing: -0.32px; margin: 16px 0 -2px; }
  @include tablet {
    font-size: fluid(16px, 14px); line-height: fluid(24px, 20px); letter-spacing: fluid(-0.32px, -0.28px);
    margin: fluid(16px, 0px) 0 fluid(-2px, 0px);
  }""", 1),

# --- G2.4  dialog takes initial focus itself, not the close button ---
(""":focus-visible { outline: 2px solid $c-green; outline-offset: 2px; }""",
 """:focus-visible { outline: 2px solid $c-green; outline-offset: 2px; }

// The dialog itself takes initial focus (main.js), which is what keeps the close
// button from painting a ring the moment the modal appears. A container is not
// an interactive control, so it gets no ring of its own.
[role="dialog"][tabindex="-1"]:focus,
[role="dialog"][tabindex="-1"]:focus-visible { outline: none; }""", 1),

# --- build bump ---
('$build: "20260828-r54";', '$build: "20260828-r55";', 1),
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
