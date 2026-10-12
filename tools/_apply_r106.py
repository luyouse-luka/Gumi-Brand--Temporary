#!/usr/bin/env python3
"""r106: the ten asks, applied to the source. Every replacement asserts its anchor.

  python3 tools/_apply_r106.py
"""
import pathlib, sys

SCSS = pathlib.Path('assets/customstyle.scss')
JS = pathlib.Path('assets/main.js')
edits = []


def sub(path, old, new, label, count=1):
    edits.append((path, old, new, label, count))


# --- $build ------------------------------------------------------------------
sub(SCSS, '$build: "20260908-r105";', '$build: "20260908-r106";', 'build token')

# --- 1. .gb-page-hero--center desktop padding-top 64 -> 80 (client) -----------
sub(SCSS, """  --hero-wave: var(--sc-res, 0px);
  padding: 64px 0 calc(70px + var(--hero-wave));

  @include narrow { padding: 32px 0 calc(64px + var(--hero-wave)); }
  @include tablet { padding: fluid(32px, 64px) fluid(0, 0) calc(fluid(64px, 70px) + var(--hero-wave)); }""",
    """  --hero-wave: var(--sc-res, 0px);
  // Client r106: 80 on desktop where 324:69636 draws 64. Mobile keeps the
  // board's 32, so only the ramp's top end moves with it.
  padding: 80px 0 calc(70px + var(--hero-wave));

  @include narrow { padding: 32px 0 calc(64px + var(--hero-wave)); }
  @include tablet { padding: fluid(32px, 80px) fluid(0, 0) calc(fluid(64px, 70px) + var(--hero-wave)); }""",
    '1. --center padding-top 80')

# --- 10. reservation for a wave the section above cannot see ------------------
sub(SCSS, """:where(section, div, footer):has(> .gb-scallop--edge) { --sc-res: var(--sc-h); }
:where(section, div, footer):has(> .gb-scallop--edge.gb-scallop--lg) { --sc-res: var(--sc-lg-h); }""",
    """:where(section, div, footer):has(> .gb-scallop--edge) { --sc-res: var(--sc-h); }
:where(section, div, footer):has(> .gb-scallop--edge.gb-scallop--lg) { --sc-res: var(--sc-lg-h); }

// ...and the two boundaries the board models as the LOWER section's Spacer Top.
// Those hang off the next section's top edge, so the room still belongs to the
// section BEFORE them -- which cannot see the wave from inside itself. Read it
// off the next sibling instead. Without this .gb-stats and .gb-nutrition reserve
// nothing and the wave eats their last 96 / 129 px (index only, both static).
// Live models the same two as a Gumi Wave section; the nutrition one carries
// --lap, which pulls itself back over the block above and wants the same room.
// ⚠ `+ *`, not `+ section`: live wraps the module in a div.shopify-section, so
//   the wave's parent is that wrapper on one side and the module on the other.
:where(section, div, footer):has(+ * > .gb-scallop--edge-top) { --sc-res: var(--sc-h); }
:where(section, div, footer):has(+ * > .gb-scallop--edge-top.gb-scallop--lg) { --sc-res: var(--sc-lg-h); }
:where(section, div, footer):has(+ * > .gb-wave--lap) { --sc-res: var(--sc-h); }
:where(section, div, footer):has(+ * > .gb-wave--lg.gb-wave--lap) { --sc-res: var(--sc-lg-h); }""",
    '10. --edge-top / --lap reservation')

# --- 6. the check the board draws on the chosen row ---------------------------
sub(SCSS, """  &.is-active {
    background: $c-lime-150;
    color: $c-green;
  }
}
""",
    """  &.is-active {
    background: $c-lime-150;
    color: $c-green;
  }
}

// 196:18033 marks the chosen row with a check at the far edge (20 box, 13.33 x
// 9.17 ink, 1.667 round stroke). ::after rather than markup: role="option" takes
// its accessible name from the text, and an empty pseudo stays out of it.
// ⚠ Only the default variant. --bare is the phone country code, one option that
//   is always selected, and --inline is the cart's interval list, whose open
//   state the client ruled out of scope in r76.
// The board draws the tick #000 on a #656565 row; ours follows the row's own
// $c-green (see [aria-selected] above) -- black beside green reads as a slip.
.gb-select:not(.gb-select--bare):not(.gb-select--inline) {
  .gb-select__option {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .gb-select__option[aria-selected="true"]::after {
    content: "";
    flex: 0 0 20px;
    width: 20px;
    height: 20px;
    margin-left: auto;
    background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='20' height='20' viewBox='0 0 20 20' fill='none'%3E%3Cpath d='M16.6667 5L7.5 14.1667L3.33333 10' stroke='%23005635' stroke-width='1.667' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") no-repeat center / 20px 20px;
  }
}
""",
    '6. selected-option check')

# --- 4. phone placeholder = every other input's -------------------------------
sub(SCSS, """  input {
    flex: 1 1 auto;
    min-width: 0;
    border: 0;
    background: transparent;
    font-family: $font-brand-stack;
    font-size: 16px;
    line-height: 24px;
    letter-spacing: -0.32px;
    color: $c-gray-700;

    &:focus-visible { outline: none; }
  }
}""",
    """  input {
    flex: 1 1 auto;
    min-width: 0;
    border: 0;
    background: transparent;
    font-family: $font-brand-stack;
    font-size: 16px;
    line-height: 24px;
    letter-spacing: -0.32px;
    color: $c-gray-700;

    // Client r106: this field carried no rule, so it was left on the UA's own
    // grey (#757575 local, rgba(51,51,51,.6) under the theme's reset).
    &::placeholder { color: $c-gray-600; }

    &:focus-visible { outline: none; }
  }
}""",
    '4. phone placeholder')

# --- 3. the consent link takes the label's own grey --------------------------
sub(SCSS, """  input[type="checkbox"] { @include visually-hidden; }

  a {
    color: $c-ink;""",
    """  input[type="checkbox"] { @include visually-hidden; }

  a {
    color: #656565;   // client r106: the label's own grey, not $c-ink""",
    '3. check link colour')

# --- 7. nav card art back to the board's 135.2% on mobile --------------------
sub(SCSS, """  // Client r85: the phone drawer's card is far narrower than the desktop one, so
  // the 135.2% overhang ran the artwork outside it.
  @include narrow { width: 100%; }

""", """""", '7. drop the narrow width override')

# --- 8. cart line media ------------------------------------------------------
sub(SCSS, """.gb-cart-item__media {
  flex: none;
  width: 56px;
  height: 56px;
  background: $c-gray-200;

  img, video, picture { @include cover-img; }
}""",
    """.gb-cart-item__media {
  flex: none;
  width: 56px;
  height: 56px;
  background: $c-gray-200;
  // Client r106. overflow, not radius alone: a square shot fills the box under
  // `contain`, so its own corners would sit outside the rounded edge.
  border-radius: $r-xs;
  overflow: hidden;

  img, video, picture { @include cover-img(contain); }
}""",
    '8. cart media radius + contain')

# --- 9. the collection template's heading and gutters ------------------------
sub(SCSS, """.gb-page-wrapper .product-grid-container {
  padding-block-end: 120px;

  @include narrow { padding-block-end: 64px; }
  @include tablet { padding-block-end: fluid(64px, 120px); }
}""",
    """.gb-page-wrapper .product-grid-container {
  padding-block-end: 120px;

  @include narrow { padding-block-end: 64px; }
  @include tablet { padding-block-end: fluid(64px, 120px); }
}

// Client r106: /collections/all reads as a different site -- Horizon's Inter
// 48/700 black heading inside Horizon's 16/40 gutters, next to gb-* modules that
// are neither.
// ⚠ Hook is theme.liquid's own data-template. The heading and the grid are
//   Horizon's generic `section` / `main-collection`, whose schemas are shared
//   with other templates, so there is no class to scope on the way .gb-404 does.
#MainContent[data-template^="collection"] {
  // The theme declares --page-margin on <body>; redeclaring it here re-gutters
  // every section on this template at once, and keeps the safe-area floor.
  --page-margin: max(var(--pad-x), var(--safe-area-inset-left, 0px), var(--safe-area-inset-right, 0px));

  // Same type and same doubled-class trick as .gb-404 -- the type preset class
  // sits on the .text-block WRAPPER, so a bare `h1` (0-0-1) never wins.
  // ⚠ h1 only, not :is(h1..h6): the product cards are text blocks too, and an
  //   unscoped heading selector puts 56/800 on every product name (the note on
  //   .ui-test-product-list is the same trap).
  .text-block.text-block h1 {
    font-family: $font-brand-stack;
    font-size: 56px;
    font-weight: 800;
    line-height: 64px;
    letter-spacing: -0.56px;
    color: $c-green;

    @include narrow { font-size: 30px; line-height: 36px; letter-spacing: -0.3px; }
    @include tablet {
      font-size: fluid(30px, 56px);
      line-height: fluid(36px, 64px);
      letter-spacing: fluid(-0.3px, -0.56px);
    }
  }
}""",
    '9. collection heading + gutters')

# --- 2. the message box scrolls itself, not the page -------------------------
sub(JS,
    'PREVENT: ".gb-product__thumbs, .gb-header__panel, .gb-nl-panel__body, '
    '.gb-select__list, .gb-cart__body, .gb-cart__empty",',
    'PREVENT: ".gb-product__thumbs, .gb-header__panel, .gb-nl-panel__body, '
    '.gb-select__list, .gb-cart__body, .gb-cart__empty, .gb-field__input--area",',
    '2. textarea opts out of Lenis')

for path, old, new, label, count in edits:
    text = path.read_text(encoding='utf-8')
    n = text.count(old)
    if n != count:
        sys.exit(f'ABORT [{label}] {path}: anchor found {n} time(s), expected {count}')
    path.write_text(text.replace(old, new, count), encoding='utf-8')
    print(f'  ok  {label:<40} {path}')
print(f'\n{len(edits)} edit(s) applied')
