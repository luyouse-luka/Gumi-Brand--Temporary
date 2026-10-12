#!/usr/bin/env python3
"""r107 asks 6-8. Every replacement asserts its anchor.

  python3 tools/_apply_r107d.py
"""
import pathlib, sys

SCSS = pathlib.Path('assets/customstyle.scss')
edits = []


def sub(old, new, label, count=1):
    edits.append((old, new, label, count))


# --- 6. line reveal 1.4s -> 0.7s, halo kept in step -------------------------
sub("""  animation: gm-line-up 1.4s var(--e-power4-out) both;""",
    """  // Client r107: 0.7s, the same as .wowo's fadeInUp. At 1.4s the banner title
  // landed 249-600ms AFTER the copy below it (the more lines, the worse), which
  // read as the title lagging. The 150ms per-line stagger is what makes it read
  // as line-by-line, so that stays.
  animation: gm-line-up 0.7s var(--e-power4-out) both;""",
    "6a. gm-line-up 1.4s -> 0.7s")

# ⚠ the halo window must ride the same curve for the same duration, or the
# outline arrives after its own glyphs.
sub("""  animation: gm-halo-up 1.4s var(--e-power4-out) both;""",
    """  animation: gm-halo-up 0.7s var(--e-power4-out) both;   // must match gm-line-up""",
    "6b. gm-halo-up follows")

# --- 7. no focus ring from OPENING a drawer on a touch device ---------------
sub("""// Inputs are the exception: focus is a border colour change.""",
    """// ⚠ The cart drawer is NOT one of ours -- it is Horizon's <theme-drawer> /
// <dialog>, so the line above does not apply to it: the dialog hands initial
// focus to its first focusable child, which is .gb-cart__close, and Safari
// counts that as keyboard focus and paints the ring. The drawer then opens
// looking like its close button is selected.
// Client r107: drop the ring where there is no keyboard for it to describe.
// Desktop keyboard users keep it -- (pointer: coarse) is the touch screen only.
// ⚠ Reported on small-screen Safari and NOT reproducible here: this machine has
//   chromium only, and :focus-visible heuristics differ per engine. Verify on a
//   real device.
@media (pointer: coarse) {
  .gb-cart__close,
  .gb-header__icon,
  .gb-header__panel-close,
  .gb-nl-panel__close,
  .gb-promo-panel__close,
  .gb-rv-panel__close {
    &:focus-visible { outline: none; }
  }
}

// Inputs are the exception: focus is a border colour change.""",
    "7. no ring from opening a drawer on touch")

# --- 8. drop all nine press-shrinks, and the transitions they were the only
#        user of. Round 73 kept these when it removed the press-DOWN; the client
#        has now called them too.
for old, new, label in [
    ("""  transition: trans(background, transform);

  svg {
    width: 16px;
    height: 16px;
    stroke: currentColor;
  }

  @include hover { background: rgba(1, 19, 7, 0.8); }
  &:active { transform: scale(0.94); }""",
     """  transition: trans(background);

  svg {
    width: 16px;
    height: 16px;
    stroke: currentColor;
  }

  @include hover { background: rgba(1, 19, 7, 0.8); }""",
     "8a. gb-rv-panel__close"),

    ("""  transition: trans(color, transform);

  svg { width: 24px; height: 24px; }

  @include hover { color: $c-green; }
  &:active { transform: scale(0.92); }""",
     """  transition: trans(color);

  svg { width: 24px; height: 24px; }

  @include hover { color: $c-green; }""",
     "8b. gb-cart__close"),

    ("""  transition: trans(color, transform);

  svg { width: 16px; height: 20px; }

  @include hover { color: $c-coral; }
  &:active { transform: scale(0.92); }""",
     """  transition: trans(color);

  svg { width: 16px; height: 20px; }

  @include hover { color: $c-coral; }""",
     "8c. gb-cart-item__remove"),

    ("""  transition: trans(color, transform);

  svg { width: 16px; height: 16px; }

  @include hover { color: $c-green; }
  &:active { transform: scale(0.88); }""",
     """  transition: trans(color);

  svg { width: 16px; height: 16px; }

  @include hover { color: $c-green; }""",
     "8d. gb-cart-item__step"),

    ("""  transition: trans(opacity, transform);

  svg { width: 24px; height: 24px; }

  @include hover { opacity: 0.6; }
  &:active { transform: scale(0.92); }""",
     """  transition: trans(opacity);

  svg { width: 24px; height: 24px; }

  @include hover { opacity: 0.6; }""",
     "8e. gb-header__icon"),

    ("""  transition: trans(opacity, transform);

  svg { display: block; width: 24px; height: 24px; }

  @include hover { opacity: 0.6; }
  &:active { transform: scale(0.92); }""",
     """  transition: trans(opacity);

  svg { display: block; width: 24px; height: 24px; }

  @include hover { opacity: 0.6; }""",
     "8f. gb-header__panel-close"),

    # .gb-reel's own transition had no other user -- hover/focus scale the CHILD
    ("""  overflow: hidden;                // clips the scaled image back inside the radius
  transition: trans(transform);

  &:active { transform: scale(0.99); }
""",
     """  overflow: hidden;                // clips the scaled image back inside the radius
""",
     "8g. gb-reel"),

    ("""  transition: trans(opacity, transform);

  @include hover { opacity: 0.75; }
  &:active { transform: scale(0.95); }""",
     """  transition: trans(opacity);

  @include hover { opacity: 0.75; }""",
     "8h. gb-reels__btn"),

    ("""  transition: trans(color, transform);

  svg { flex: none; width: 16px; height: 16px; stroke-width: 1.33333; transition: trans(stroke-width); }

  @include hover { color: $c-green; }
  &:active { transform: scale(0.94); }""",
     """  transition: trans(color);

  svg { flex: none; width: 16px; height: 16px; stroke-width: 1.33333; transition: trans(stroke-width); }

  @include hover { color: $c-green; }""",
     "8i. gb-crev-card__vote"),
]:
    sub(old, new, label)

text = SCSS.read_text(encoding='utf-8')
for old, new, label, count in edits:
    n = text.count(old)
    if n != count:
        sys.exit(f'ABORT [{label}]: anchor found {n} time(s), expected {count}')
    text = text.replace(old, new, count)
    print(f'  ok  {label}')
SCSS.write_text(text, encoding='utf-8')
print(f'\n{len(edits)} edit(s) applied')
