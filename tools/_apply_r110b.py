#!/usr/bin/env python3
"""r110 asks 2-3 -- both live-only (Horizon's own collection markup).

  python3 tools/_apply_r110b.py
"""
import pathlib, sys

SCSS = pathlib.Path('assets/customstyle.scss')

OLD = """#MainContent[data-template^="collection"] {
  // The theme declares --page-margin on <body>; redeclaring it here re-gutters
  // every section on this template at once, and keeps the safe-area floor.
  --page-margin: max(var(--pad-x), var(--safe-area-inset-left, 0px), var(--safe-area-inset-right, 0px));
"""

NEW = """#MainContent[data-template^="collection"] {
  // The theme declares --page-margin on <body>; redeclaring it here re-gutters
  // every section on this template at once, and keeps the safe-area floor.
  --page-margin: max(var(--pad-x), var(--safe-area-inset-left, 0px), var(--safe-area-inset-right, 0px));

  // Client r110: below 768 the grid and the facet bar still ran edge to edge
  // while the h1 sat at --pad-x. Not the --page-margin above failing -- the
  // collection section carries `full_width_on_mobile: true`, which drops the
  // gutter on those two on purpose. That setting lives in templates/*.json,
  // which we never push, so the gutter is restored from here.
  // ⚠ Measured, not guessed: 1440 was already 80/80 on both; only 390 was 0.
  @include narrow {
    .product-grid,
    .facets-toggle { padding-inline: var(--pad-x); }
  }
"""

# --- 3. Horizon's card gallery: no arrows, no quick add ---------------------
ANCHOR2 = """// ==========================================================================
// 404
// =========================================================================="""

ADD2 = """// Client r110: Horizon's product card ships a slideshow and a quick-add button
// inside .card-gallery. Neither is in the boards, and the arrows sit on top of
// the image on touch where there is nothing to click them with.
// ⚠ Custom elements, not classes -- .quick-add is on the component, but
//   <slideshow-arrows> carries no class at all, so the tag name is the only hook.
// ⚠ Scoped to .card-gallery on purpose: the PDP gallery is our own
//   .gb-product__gallery and must keep its controls.
.card-gallery {
  slideshow-arrows,
  quick-add-component { display: none; }
}

// ==========================================================================
// 404
// =========================================================================="""

text = SCSS.read_text(encoding='utf-8')
for old, new, label in [(OLD, NEW, '2. collection mobile gutter'),
                        (ANCHOR2, ADD2, '3. card-gallery arrows + quick add')]:
    n = text.count(old)
    if n != 1:
        sys.exit(f'ABORT [{label}]: anchor found {n} time(s), expected 1')
    text = text.replace(old, new, 1)
    print(f'  ok  {label}')
SCSS.write_text(text, encoding='utf-8')
