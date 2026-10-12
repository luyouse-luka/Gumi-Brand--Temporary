#!/usr/bin/env python3
"""r112: promo logo <img>, hCaptcha gap, short-viewport panel scroll."""
import pathlib, sys

SCSS = pathlib.Path('assets/customstyle.scss')
JS = pathlib.Path('assets/main.js')


def sub(text, old, new, n=1, label=''):
    got = text.count(old)
    if got != n:
        sys.exit(f'ABORT [{label}]: anchor found {got}x, expected {n}\n---\n{old}\n---')
    return text.replace(old, new, n)


s = SCSS.read_text(encoding='utf-8')

s = sub(s, '$build: "20260908-r110";', '$build: "20260908-r112";', 1, 'build')

# 1. the head logo is an <img> the moment settings.logo is uploaded (it is),
#    and only <svg> was sized -- same trap .gb-header__logo already handles.
s = sub(s,
        """  svg { display: block; height: 100%; width: auto; }
}

.gb-promo-panel__close {""",
        """  // <img> as well as <svg>: snippets/gb-logo.liquid swaps to an <img> once
  // settings.logo is uploaded, and its width/height attributes carry the 124x32
  // pair, which overflows this 24-tall row by 8.
  svg, img { display: block; height: 100%; width: auto; }
}

.gb-promo-panel__close {""", 1, 'logo img')

# 2. the invisible hCaptcha container is a 0-height flex item that still earns a
#    whole gap. r109's :empty guard cannot see it: it holds an iframe + textarea.
s = sub(s,
        """// Shopify drops its bot-challenge container straight into {% form %} as a direct
// child. With the challenge invisible it paints nothing, but it is NOT
// display:none -- so it stays a flex item and eats one whole 32px gap between
// the fields and the submit button.
// ⚠ :empty is a guard, not decoration. The moment hCaptcha puts a real widget in
//   there (checkbox mode) the rule stops matching and the challenge shows --
//   folding a live captcha away would make the form impossible to submit.
// ⚠ Written from Shopify's documented behaviour: the container is not present on
//   this store right now, so the rule is inert here and could not be measured.
.gb-form > [class*="captcha"]:empty,
.gb-form > .shopify-challenge__container:empty { display: none; }""",
        """// Shopify's bot protection appends <div class="h-captcha" data-size="invisible">
// as the form's last child, but only after a field takes focus. It paints
// nothing (height 0) yet it is still a flex item, so it earns one whole gap:
// measured 788 -> 820 on the contact form, 108 -> 120 in the promo panel.
// ⚠ Take it out of flow, do NOT hide it. The widget is invisible but live, and
//   it raises its challenge inside this very container -- display:none would
//   make the form impossible to submit. Absolute positioning drops it out of
//   flex layout while leaving it rendered.
// ⚠ Keyed on data-size="invisible" so a checkbox-mode widget still lays out
//   normally, gap and all.
.h-captcha[data-size="invisible"] { position: absolute; }""", 1, 'captcha')

# 3. short viewports: on mobile the content column and the bear strip stack, so
#    they outgrow the screen with nothing to scroll (the panel clipped them).
s = sub(s,
        """  background: $c-sand;
  overflow: hidden;
  pointer-events: auto;""",
        """  background: $c-sand;
  overflow: hidden;
  pointer-events: auto;
  // Mobile stacks the content column over the bear strip (460 + 252), so any
  // viewport under 712 cut the bears off with nothing to scroll. Hand the scroll
  // to the panel here; overflow-x stays clipped for the art's scallop. Desktop
  // is a row that never outgrows the panel, and scrolls its content column
  // instead -- see .gb-promo-panel__content.
  @include narrow { overflow: hidden auto; }""", 1, 'panel scroll')

s = sub(s,
        """.gb-promo-panel__content {
  order: 1;
  position: relative;
  flex-shrink: 0;
  max-height: 100%;
  display: flex;
  flex-direction: column;
  gap: 64px;                 // 285:19013 / 336:27155 both space head to body by 64
  overflow-y: auto;

  @include panel-wide { order: 0; width: 531px; height: 100%; }
}""",
        """.gb-promo-panel__content {
  order: 1;
  position: relative;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: 64px;                 // 285:19013 / 336:27155 both space head to body by 64

  // Desktop only: the panel is a row here, so this column is the one thing that
  // can scroll. On mobile the panel itself scrolls and a cap here would make a
  // second, nested scroller.
  @include panel-wide { order: 0; width: 531px; height: 100%; max-height: 100%; overflow-y: auto; }
}""", 1, 'content scroll')

SCSS.write_text(s, encoding='utf-8')

j = JS.read_text(encoding='utf-8')
j = sub(j,
        'PREVENT: ".gb-product__thumbs, .gb-header__panel, .gb-nl-panel__body, '
        '.gb-select__list, .gb-cart__body, .gb-cart__empty, .gb-field__input--area",',
        'PREVENT: ".gb-product__thumbs, .gb-header__panel, .gb-nl-panel__body, '
        '.gb-select__list, .gb-cart__body, .gb-cart__empty, .gb-field__input--area, '
        '.gb-promo-panel",', 1, 'lenis prevent')
JS.write_text(j, encoding='utf-8')

print('r112 applied')
