#!/usr/bin/env python3
"""r119 -- three client asks. Read-modify-write, every anchor asserted unique.

1  /collections/all: Horizon's own components still render in Inter.
2  .gb-cart__gift-media: 4px radius, clipped.
3  ?type=press no longer preselects on live -- the id is section-suffixed there.
"""
import pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCSS = ROOT / 'assets/customstyle.scss'
JS = ROOT / 'assets/main.js'


def sub(text, old, new, label):
    n = text.count(old)
    if n != 1:
        sys.exit(f'ABORT {label}: anchor matched {n} times, want 1')
    return text.replace(old, new)


s = SCSS.read_text(encoding='utf-8')

# --- $build -------------------------------------------------------------
s = sub(s, '$build: "20260908-r117";', '$build: "20260908-r119";', 'build')

# --- ask 1: collection font vars ---------------------------------------
s = sub(s, """  --page-width: #{$w-container + $pad-x-desktop * 2};

  // Client r110: below 768 the grid and the facet bar still ran edge to edge""",
"""  --page-width: #{$w-container + $pad-x-desktop * 2};

  // Client r119: Horizon's own components name a font VARIABLE, and every one of
  // those is still Inter -- PP Palma is a custom face, so the theme editor's
  // Typography picker cannot be pointed at it. Only what inherits from <body>
  // reaches the brand face; the price, the Sale badge, the Filter toggle and the
  // in-page skip link all name a variable and land on Inter.
  // ⚠ The variables, not the elements: .product-badges sets
  // `--badge-font-family: var(--font-body--family)` INLINE, which no rule of ours
  // can outrank -- but that var() resolves against whatever is declared here.
  // ⚠ Family only. The weights are Horizon's type scale, and this template has
  // no board to take numbers from.
  @each $v in (--font-body--family, --font-heading--family, --font-paragraph--family,
               --font-subheading--family, --font-accent--family,
               --font-h1--family, --font-h2--family, --font-h3--family,
               --font-h4--family, --font-h5--family, --font-h6--family,
               --button-font-family-primary, --button-font-family-secondary,
               --cart-primary-font-family, --cart-secondary-font-family) {
    #{$v}: #{$font-brand-stack};
  }

  // Client r110: below 768 the grid and the facet bar still ran edge to edge""",
'ask1')

# --- ask 2: gift media radius ------------------------------------------
s = sub(s, """  background: $c-gray-200;   // placeholder, same as the line-item media

  img, video, picture { @include cover-img; }""",
"""  background: $c-gray-200;   // placeholder, same as the line-item media
  // Client r119. overflow alongside it: the shot fills the box under `cover`, so
  // its own square corners would sit outside the rounded edge.
  border-radius: $r-xs;
  overflow: hidden;

  img, video, picture { @include cover-img; }""",
'ask2')

SCSS.write_text(s, encoding='utf-8')

# --- ask 3: prefill selector -------------------------------------------
j = JS.read_text(encoding='utf-8')
j = sub(j, """      var select = form.querySelector("#enquiry");
      if (!select) return;""",
"""      // ⚠ Not #enquiry: the theme's contact section suffixes every field id with
      // its own section id (enquiry-template--...__form), so that id only ever
      // existed on the static page. The name is the stable hook -- Shopify wraps
      // it as contact[...] and the static form posts it bare.
      var select = form.querySelector(
        'select[name="enquiry"], select[name="contact[enquiry]"]');
      if (!select) return;""",
'ask3')
JS.write_text(j, encoding='utf-8')

print('applied: build, ask1 (collection font vars), ask2 (gift media), ask3 (prefill selector)')
