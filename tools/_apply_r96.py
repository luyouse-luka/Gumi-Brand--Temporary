#!/usr/bin/env python3
"""r96: 7 client items. Exact-anchor read-modify-write; each sub() must hit once."""
import sys, pathlib

SCSS = pathlib.Path('assets/customstyle.scss')
JS = pathlib.Path('assets/main.js')


def sub(text, old, new, tag, n=1):
    hits = text.count(old)
    if hits != n:
        sys.exit(f'ABORT {tag}: anchor found {hits}x, expected {n}')
    print(f'  ok  {tag}')
    return text.replace(old, new)


s = SCSS.read_text()

# --- 1. .gb-faq__list --acc-gap back to the board's 24 (reverses r64 item 3) ---
s = sub(s, """.gb-faq__list {
  --acc-gap: 16px;      // client-set (was 24)
""", """.gb-faq__list {
  --acc-gap: 24px;      // client-set r96 (r64 had set 16)
""", '1 faq --acc-gap 24')

# --- 2. header panel: no border at all while shut ---
s = sub(s, """  // Client r86: the top edge belongs to the OPEN panel. Shut, the panel is a 0fr
  // row and this reads as a second hairline right under the bar's own border.
  // Transparent rather than 0 width so the box never steps, and so the colour can
  // fade in on the row's own curve.
  border-top: 1px solid transparent;
  // r87 extends r86 to the bottom edge: shut, the panel is a 0fr row and BOTH
  // hairlines stack under the bar's own border.
  border-bottom: 1px solid transparent;""",
"""  // Client r86/r87: both edges belong to the OPEN panel. r96 takes the WIDTH to
  // zero rather than the colour to transparent -- shut, a transparent 1px border
  // still boxes the 0fr row 2px tall and its own $c-cream background paints
  // there, i.e. a cream hairline under the bar on every page.
  border-top: 0 solid $c-sand;
  border-bottom: 0 solid $c-sand;""", '2a panel border 0 width')

s = sub(s, """  transition: grid-template-rows $t-panel $ease-in-out,
              border-top-color $t-panel $ease-in-out,
              border-bottom-color $t-panel $ease-in-out;""",
"""  transition: grid-template-rows $t-panel $ease-in-out,
              border-top-width $t-panel $ease-in-out,
              border-bottom-width $t-panel $ease-in-out;""", '2b panel transition width')

s = sub(s, """  // The narrow block below zeroes border-top's WIDTH, so this colour paints
  // nothing there -- the phone drawer keeps both edges off.
  .gb-header.is-open & {
    grid-template-rows: 1fr;
    border-top-color: $c-sand;
    border-bottom-color: $c-sand;
  }""",
"""  // ⚠ 0-2-0, so it outranks the narrow block's own `border-*: 0` below no matter
  // where that sits -- the drawer has to re-zero it inside its own is-open rule.
  .gb-header.is-open & {
    grid-template-rows: 1fr;
    border-top-width: 1px;
    border-bottom-width: 1px;
  }""", '2c panel is-open width')

s = sub(s, """    .gb-header.is-open & { transform: translateX(0); }
  }
}""",
"""    // Re-zeroed because the base is-open rule above is 0-2-0 and would paint a
    // sand hairline across the top and bottom of the full-viewport drawer.
    .gb-header.is-open & { transform: translateX(0); border-width: 0; }
  }
}""", '2d drawer re-zero')

# --- 3. page-hero lead: one colour everywhere (#4d4d4d) ---
s = sub(s, """.gb-page-hero__lead--lg {
  font-size: 20px;
  line-height: 30px;
  letter-spacing: -0.4px;
  color: $c-gray-900;""",
""".gb-page-hero__lead--lg {
  font-size: 20px;
  line-height: 30px;
  letter-spacing: -0.4px;
  color: $c-gray-700;   // client r96: one lead colour site-wide (board: #1a1a1a)""",
    '3a lead--lg colour')

s = sub(s, """  font-weight: 500;
  letter-spacing: -0.36px;
  color: $c-gray-800;

  // #333333 and weight 500 are desktop-only; the mobile boards are 400/#1a1a1a,
  // which is what --lg gives -- restated here because this variant comes later.
  @include narrow { font-weight: 400; color: $c-gray-900; }""",
"""  font-weight: 500;
  letter-spacing: -0.36px;
  color: $c-gray-700;   // client r96 (board: #333333)

  // Weight 500 is desktop-only; the mobile boards are 400. Colour no longer
  // steps here -- r96 puts every lead on #4d4d4d.
  @include narrow { font-weight: 400; }""", '3b lead--text-page colour')

# --- 4. tight science cards open up 16 -> 22 ---
s = sub(s, """  // Client-set, and it stacks on the gap above rather than replacing it: 22 + 26
  // at desktop, 48 + 26 on phones.
  .gb-science__cards { margin-top: 26px; }
}""",
"""  // Client-set, and it stacks on the gap above rather than replacing it: 22 + 26
  // at desktop, 48 + 26 on phones.
  .gb-science__cards { margin-top: 26px; }

  // Client r96. The base card is 16 at every width; only the tight board opens up.
  .gb-science-card { gap: 22px; }
}""", '4 tight card gap 22')

# --- 5. page-hero title: 30px right inset on phones ---
s = sub(s, """  // Was a hard 48/56 on `tight`, which put a 30 → 48 step right on 768.
  // Type belongs on the value tier, interpolated end to end.
  @include narrow { font-size: 30px; line-height: 36px; letter-spacing: -0.3px; }
  @include tablet {
    font-size: fluid(30px, 56px);
    line-height: fluid(36px, 64px);
    letter-spacing: fluid(-0.3px, -0.56px);
  }
}""",
"""  // Was a hard 48/56 on `tight`, which put a 30 → 48 step right on 768.
  // Type belongs on the value tier, interpolated end to end.
  // Client r96: 30px of right inset on phones so the long left-aligned headings
  // (science, reviews) break before the gutter. Ramped to 0 or 1281 steps.
  @include narrow { font-size: 30px; line-height: 36px; letter-spacing: -0.3px; padding-right: 30px; }
  @include tablet {
    font-size: fluid(30px, 56px);
    line-height: fluid(36px, 64px);
    letter-spacing: fluid(-0.3px, -0.56px);
    padding-right: fluid(30px, 0);
  }
}""", '5a title padding-right')

s = sub(s, """  .gb-page-hero__title {
    @include narrow { font-size: 36px; line-height: 40px; letter-spacing: -0.36px; }""",
"""  .gb-page-hero__title {
    // ⚠ Not inside a media query on purpose: @media carries no specificity, so
    // this 0-2-0 rule cancels the base's phone AND tablet inset in one line.
    // A one-sided inset on centred text just shifts it off centre.
    padding-right: 0;

    @include narrow { font-size: 36px; line-height: 40px; letter-spacing: -0.36px; }""",
    '5b centre variant cancels inset')

# --- 0. review cards fade in when the pager reveals them ---
s = sub(s, """.gb-crev-card {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding-bottom: 32px;
  border-bottom: 1px solid $c-ink-05;

  // Paged out by main.js. The UA's [hidden] rule is display:none at 0-0-0 and
  // loses to the flex above, so it has to be restated here.
  &[hidden] { display: none; }
}""",
""".gb-crev-card {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding-bottom: 32px;
  border-bottom: 1px solid $c-ink-05;

  // Client r96: the pager only strips [hidden], and display:none -> flex cannot
  // transition. An animation can: display:none cancels it, so restoring display
  // replays it from the top -- which is exactly the reveal. `backwards` and not
  // `both`, so nothing is left pinned on the element afterwards
  // ([[finished-animation-fill-blocks-transition]]). Works under the live
  // section's own inline script too; it strips the same attribute.
  animation: gm-crev-in $t-slow $ease-out backwards;

  // Paged out by main.js. The UA's [hidden] rule is display:none at 0-0-0 and
  // loses to the flex above, so it has to be restated here.
  &[hidden] { display: none; }

  @media (prefers-reduced-motion: reduce) { animation: gm-fade-in 0.4s ease-out backwards; }
}

@keyframes gm-crev-in {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: none; }
}""", '0 crev card reveal animation')

SCSS.write_text(s)

# --- 6. expert rail: first/last card align to the track edges ---
j = JS.read_text()
j = sub(j, """          centeredSlides: centre,""",
"""          centeredSlides: centre,
          // Client r96: with three cards a centred rail parks the first (and
          // the last) in the middle, leaving a card's worth of empty track at
          // one edge -- most visible right after `rewind` wraps round. This
          // pins the end slides to the track edges and leaves every interior
          // position centred, so the board's peek-each-side is unchanged.
          // Ignored above 767 where the breakpoint turns centring off.
          centeredSlidesBounds: centre,""", '6 centeredSlidesBounds')
JS.write_text(j)
print('done')
