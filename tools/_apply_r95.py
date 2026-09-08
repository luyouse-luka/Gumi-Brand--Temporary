#!/usr/bin/env python3
"""r95: pin the star <img> sizes -- the live star.svg has no intrinsic size."""
import io, sys

P = 'assets/customstyle.scss'
s = io.open(P, encoding='utf-8').read(); o = s

def sub(a, b, tag):
    global s
    if s.count(a) != 1:
        sys.exit(f'ANCHOR FAIL ({s.count(a)}): {tag}')
    s = s.replace(a, b)

sub(""".gb-crev__stars {
  display: flex;
  flex: none;

  img { flex: none; }
}""",
""".gb-crev__stars {
  display: flex;
  flex: none;

  // ⚠ Sized here, not left to the file: the live star.svg ships a viewBox and
  // nothing else, so its intrinsic size falls back to 150 and Horizon's
  // `img { width: 100%; height: auto }` -- which we never override -- resolves
  // the 100% against this flex box and feeds it back in. Measured 1500x1500 per
  // star on the storefront, 10533px of section. The static build hid it because
  // its own star file carries real dimensions.
  img { flex: none; width: 32px; height: 32px; }
}""", '.gb-crev__stars img')

sub(""".gb-crev-card__rating {
  display: flex;
  flex: none;

  img { flex: none; }
}""",
""".gb-crev-card__rating {
  display: flex;
  flex: none;

  // Same as .gb-crev__stars -- see the note there.
  img { flex: none; width: 20px; height: 20px; }
}""", '.gb-crev-card__rating img')

sub('$build: "20260908-r94";', '$build: "20260908-r95";', '$build')

assert s != o
io.open(P, 'w', encoding='utf-8').write(s)
print('scss patched: 3 anchors')
