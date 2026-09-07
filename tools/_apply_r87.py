#!/usr/bin/env python3
"""r87: six client-named CSS fixes. Run once from the repo root."""
import pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCSS = ROOT / 'assets/customstyle.scss'


def sub(text, old, new, tag):
    n = text.count(old)
    if n != 1:
        sys.exit('%s: anchor found %d times, expected 1' % (tag, n))
    return text.replace(old, new, 1)


s = SCSS.read_text()

# 1 -- measure cap on the reviews heading
s = sub(s, """.gb-reviews__title {
  font-size: 40px;""",
""".gb-reviews__title {
  // Client r87. .gb-reviews__head is a centred column, so the cap centres itself.
  max-width: 570px;
  font-size: 40px;""", '1 reviews title')

# 2 -- the whole frame belongs to the open panel, not just its top edge
s = sub(s, """  border-top: 1px solid transparent;
  border-bottom: 1px solid $c-sand;
  border-radius: 0 0 32px 32px;
  overflow: hidden;
  display: grid;
  grid-template-rows: 0fr;             // 0fr -> 1fr animates an auto height
  transition: grid-template-rows $t-panel $ease-in-out,
              border-top-color $t-panel $ease-in-out;""",
"""  border-top: 1px solid transparent;
  // r87 extends r86 to the bottom edge: shut, the panel is a 0fr row and BOTH
  // hairlines stack under the bar's own border.
  border-bottom: 1px solid transparent;
  border-radius: 0 0 32px 32px;
  overflow: hidden;
  display: grid;
  grid-template-rows: 0fr;             // 0fr -> 1fr animates an auto height
  transition: grid-template-rows $t-panel $ease-in-out,
              border-top-color $t-panel $ease-in-out,
              border-bottom-color $t-panel $ease-in-out;""", '2 panel borders')

s = sub(s, """  .gb-header.is-open & { grid-template-rows: 1fr; border-top-color: $c-sand; }""",
"""  .gb-header.is-open & {
    grid-template-rows: 1fr;
    border-top-color: $c-sand;
    border-bottom-color: $c-sand;
  }""", '2b panel borders open')

# 3 -- three guarantees will not sit side by side on the narrowest phones
s = sub(s, """.gb-product__guarantees {
  display: flex;
  justify-content: center;
  gap: 30px;

  @include narrow { gap: 16px; }
  @include tablet { gap: fluid(16px, 30px); }
}""",
""".gb-product__guarantees {
  display: flex;
  justify-content: center;
  gap: 30px;

  @include narrow { gap: 16px; }
  @include tablet { gap: fluid(16px, 30px); }

  // Client r87. Layout threshold, so it carries no values of its own -- the gap
  // above still owns the spacing. 369.98 rather than 369 so a fractional
  // viewport between the two still counts as "under 370".
  @media (max-width: 369.98px) {
    flex-direction: column;
    align-items: center;
  }
}""", '3 guarantees stack')

# 4 -- the note's negative pull is a desktop-only device
s = sub(s, """  @include narrow {
    margin-top: -16px;   // client-set
    font-size: 18px;""",
"""  @include narrow {
    font-size: 18px;""", '4a drop narrow margin')

s = sub(s, """  @include tablet { font-size: fluid(18px, 20px); line-height: fluid(26px, 30px); letter-spacing: fluid(-0.36px, -0.4px); }
}

// The bear that rides the cream→sand wave.""",
"""  @include tablet { font-size: fluid(18px, 20px); line-height: fluid(26px, 30px); letter-spacing: fluid(-0.36px, -0.4px); }

  // Client r87: no pull at all below 992, replacing the phone tier's own -16.
  // ⚠ Last on purpose -- `mid` overlaps `narrow`, and only source order decides.
  // The base -34 therefore survives only in 992-1280, so 991/992 steps by 34.
  @include mid { margin-top: 0; }
}

// The bear that rides the cream→sand wave.""", '4b mid margin 0')

# 5 -- the phone figures belong to the tight board alone
s = sub(s, """  // Client-set, and it reverses the earlier "56/44 at every width" call: the
  // phone tier now matches what 324:58044 draws on the nutrient cards. ls is
  // given as -1%, which CSS has no unit for -- -0.36px is that at 36.
  // The tablet ramp is not in the brief; without it 767/768 would jump 36 -> 56.
  @include narrow { font-size: 36px; line-height: 40px; letter-spacing: -0.36px; }
  @include tablet {
    font-size: fluid(36px, 56px);
    line-height: fluid(40px, 44px);
    letter-spacing: fluid(-0.36px, 0px);
  }
}""",
"""}

// ⚠ THIRD reversal of the same figures, and the first one with a scope: r43 put
// the phone tier at 36/40, r49 moved it onto --nutrient, r50 deleted it (56/44
// everywhere), r?? brought it back globally -- and r87 says only the tight board
// keeps it. Everything else is 56/44/0 at every width, which is why there is no
// tablet ramp outside this block: nothing changes across 767/768 there.
// ls is given as -1%, which CSS has no unit for -- -0.36px is that at 36.
.gb-science--tight .gb-science-card__value {
  @include narrow { font-size: 36px; line-height: 40px; letter-spacing: -0.36px; }
  @include tablet {
    font-size: fluid(36px, 56px);
    line-height: fluid(40px, 44px);
    letter-spacing: fluid(-0.36px, 0px);
  }
}""", '5 science value scope')

# 6 -- pane gutter
s = sub(s, """.gb-nl-pane {
  padding: 18px 10px 24px 24px;""",
""".gb-nl-pane {
  // Client r87: right gutter 10 -> 24. ⚠ .gb-nl-panel__body's scrollbar is 16px
  // wide, so where the pane scrolls the copy now clears the edge by 40 against
  // the left's 24; the old 10 made the two read equal.
  padding: 18px 24px 24px 24px;""", '6 nl pane padding')

SCSS.write_text(s)
print('r87 applied')
