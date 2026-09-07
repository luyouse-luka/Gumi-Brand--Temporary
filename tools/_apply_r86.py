#!/usr/bin/env python3
"""r86: five client-named fixes. Run once from the repo root."""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCSS = ROOT / 'assets/customstyle.scss'


def sub(text, old, new, tag):
    n = text.count(old)
    if n != 1:
        sys.exit('%s: anchor found %d times, expected 1' % (tag, n))
    return text.replace(old, new, 1)


s = SCSS.read_text()

# 1 -- the features list belongs under the head
s = sub(s, """  @include narrow { flex: none; width: 100%; }
}

.gb-product__head {""",
"""  @include narrow { flex: none; width: 100%; }
}

// Live only. The features <ul> is an editor block, so `{% content_for 'blocks' %}`
// emits it at the END of .gb-product__info together with the other four. Order
// pulls it back under the head, where the static site keeps it -- there it is a
// child of .gb-product__head, so neither selector matches and this is a no-op.
// ⚠ Visual order only: the DOM order a screen reader follows is unchanged, and
// the gap above it is .gb-product__info's 24 rather than the head's 16. Moving
// it for real needs sections/gb-product.liquid -- docs/STYLE-GAP.md C12.
.gb-product__info > .gb-product__head { order: -2; }
.gb-product__info > .gb-product__features { order: -1; }

.gb-product__head {""", '1 features order')

# 2 -- the menu lock was taking the sticky header with it
s = sub(s, """html.is-menu-open,
body.is-menu-open {
  @include narrow { overflow: hidden; }
}""",
"""html.is-menu-open {
  @include narrow { overflow: hidden; }
}

// ⚠ NOT `overflow: hidden` on body. The reset gives body `overflow-x: hidden`,
// which the viewport takes over only while html's own overflow is `visible`; the
// moment html is locked that rule starts applying to body itself, body becomes
// the sticky header's scrollport, and since body never scrolls the header snaps
// to its static position -- measured top 0 -> -868 at scrollY 900, i.e. gone for
// as long as the drawer is open. `clip` keeps the horizontal cut the reset wants
// without creating a scroll container.
body.is-menu-open {
  @include narrow { overflow-x: clip; overflow-y: visible; }
}""", '2 menu lock')

# 3 -- smaller mobile marquee slot
s = sub(s, """  @include narrow { width: 106px; height: 44px; }
}""",
"""  // Client r86: one step smaller again. ⚠ The pitch shrinks with it and the
  // duration did not, so the strip crawls ~13% slower here than it did at 106
  // (354px/15s against 408px/15s) -- an `animation-duration: 13s` in this block
  // holds the old speed if that reads wrong.
  @include narrow { width: 88px; height: 36px; }
}""", '3 marquee slot')

s = sub(s, """  .gb-logo-scroll__img {
    width: 106px;
    height: 44px;
    object-fit: contain;
  }""",
"""  .gb-logo-scroll__img {
    width: 88px;
    height: 36px;
    object-fit: contain;
  }""", '3 marquee img')

# 4 -- hover is a colour change, not an underline
for tag, line in (('4a header link', '  @include link-underline($c-lime-stroke, 14px);\n'),
                  ('4b sublink', '  @include link-underline($c-green, 8px);\n'),
                  ('4c footer link', '  @include link-underline($c-white, -3px);\n\n'),
                  ('4d legal links', '    @include link-underline($c-white, -3px);\n')):
    s = sub(s, line, '', tag)

s = sub(s, """// Link hover underline. Pseudo-element + scaleX, not text-decoration:
// text-decoration cannot interpolate, so it can only jump.
@mixin link-underline($color: currentColor, $bottom: -2px, $height: 1px) {
  position: relative;

  &::after {
    content: "";
    position: absolute;
    left: 0;
    right: 0;
    bottom: $bottom;
    height: $height;
    background: $color;
    transform: scaleX(0);
    transform-origin: right center;
    transition: transform $t-fast $ease-out;
  }

  @include hover {
    &::after { transform: scaleX(1); transform-origin: left center; }
  }
}

""", """// Client r86: link hover is a colour change, full stop -- the sliding underline
// this mixin drew is gone from all four users (header link / sublink, footer
// link / legal link), each of which already carried its own hover colour.
// ⚠ The always-on `text-decoration: underline` on inline links (rich text,
// legal copy, cart continue) is a different thing and stays.

""", '4e mixin')

if '@include link-underline' in s or '@mixin link-underline' in s:
    sys.exit('4: link-underline still referenced')

# 5 -- the panel's top edge belongs to the open panel
s = sub(s, """  background: $c-cream;
  border-top: 1px solid $c-sand;
  border-bottom: 1px solid $c-sand;
  border-radius: 0 0 32px 32px;
  overflow: hidden;
  display: grid;
  grid-template-rows: 0fr;             // 0fr -> 1fr animates an auto height
  transition: grid-template-rows $t-panel $ease-in-out;

  > * { min-height: 0; }               // required for the 0fr row to clamp

  .gb-header.is-open & { grid-template-rows: 1fr; }""",
"""  background: $c-cream;
  // Client r86: the top edge belongs to the OPEN panel. Shut, the panel is a 0fr
  // row and this reads as a second hairline right under the bar's own border.
  // Transparent rather than 0 width so the box never steps, and so the colour can
  // fade in on the row's own curve.
  border-top: 1px solid transparent;
  border-bottom: 1px solid $c-sand;
  border-radius: 0 0 32px 32px;
  overflow: hidden;
  display: grid;
  grid-template-rows: 0fr;             // 0fr -> 1fr animates an auto height
  transition: grid-template-rows $t-panel $ease-in-out,
              border-top-color $t-panel $ease-in-out;

  > * { min-height: 0; }               // required for the 0fr row to clamp

  // The narrow block below zeroes border-top's WIDTH, so this colour paints
  // nothing there -- the phone drawer keeps both edges off.
  .gb-header.is-open & { grid-template-rows: 1fr; border-top-color: $c-sand; }""",
   '5 panel border')

SCSS.write_text(s)
print('r86 applied')
