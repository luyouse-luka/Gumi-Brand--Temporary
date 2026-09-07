#!/usr/bin/env python3
"""r86b: the other two scroll locks, same defect as the menu lock."""
import pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCSS = ROOT / 'assets/customstyle.scss'


def sub(text, old, new, tag):
    n = text.count(old)
    if n != 1:
        sys.exit('%s: anchor found %d times, expected 1' % (tag, n))
    return text.replace(old, new, 1)


s = SCSS.read_text()

# Modal lock -- same shape, same defect (measured header top -868 at 390, -860 at
# 1440). The scrollbar compensation below stays on html alone.
s = sub(s, """html.is-modal-open,
body.is-modal-open {
  overflow: hidden;
}""",
"""html.is-modal-open {
  overflow: hidden;
}

// ⚠ `clip`, NOT `hidden` -- see the note on body.is-menu-open. With html locked,
// body stops handing its overflow to the viewport and a `hidden` here would make
// body the sticky header's scrollport; body never scrolls, so the header drops to
// its static position (measured top -868 at 390, -860 at 1440). The lock itself
// lives on html, which is also the only thing Gecko honours.
body.is-modal-open {
  overflow-x: clip;
  overflow-y: visible;
}""", 'modal lock')

# Horizon's cart drawer -- a SIDE drawer, so the header stays in view next to it
# and this one was visible at every width.
s = sub(s, """html:has(#cart-drawer .theme-drawer__dialog[open]),
html:has(#cart-drawer .theme-drawer__dialog[open]) body {
  overflow: hidden;
}""",
"""html:has(#cart-drawer .theme-drawer__dialog[open]) {
  overflow: hidden;
}

// Same `clip` as the two locks above; this one mattered most -- the cart is a
// side drawer, so the header sits in plain view beside it.
html:has(#cart-drawer .theme-drawer__dialog[open]) body {
  overflow-x: clip;
  overflow-y: visible;
}""", 'cart drawer lock')

SCSS.write_text(s)
print('r86b applied')
