#!/usr/bin/env python3
"""r107 ask 5 -- the hero wave drifting 496px below the banner on live mobile.

  python3 tools/_apply_r107c.py
"""
import pathlib, sys

SCSS = pathlib.Path('assets/customstyle.scss')
edits = []


def sub(path, old, new, label, count=1):
    edits.append((path, old, new, label, count))


sub(SCSS, """  @include narrow { margin-bottom: calc(496px - var(--sc-res, 0px)); }
}
""",
    """  @include narrow { margin-bottom: calc(496px - var(--sc-res, 0px)); }
}

// Live only. r105 replaced the hero's built-in scallop with a flow
// .gb-wave-section AFTER the hero's own wrapper, so the reserve above -- which
// exists for the bear, not for the wave -- pushed the wave 496 down with it and
// the wave stopped touching the banner. 228:5932 draws it ON the hero's bottom
// edge (572..608) with the "Hovering Bear/Bear 2" block (572..1068) overlapping.
// So the reserve has to sit BELOW the wave: the hero gives it up, the wave
// section carries what is left after its own height.
// ⚠ Both selectors are inert on the static build -- there is no .shopify-section
//   there, and the hero keeps its absolutely positioned scallop child.
@include narrow {
  .shopify-section:has(+ .gb-wave-section) .gb-hero { margin-bottom: 0; }
  .shopify-section:has(> .gb-hero) + .gb-wave-section {
    margin-bottom: calc(496px - var(--sc-lg-h));
  }
}
""",
    "5. live hero wave rejoins the banner")

for path, old, new, label, count in edits:
    text = path.read_text(encoding='utf-8')
    n = text.count(old)
    if n != count:
        sys.exit(f'ABORT [{label}] {path}: anchor found {n} time(s), expected {count}')
    path.write_text(text.replace(old, new, count), encoding='utf-8')
    print(f'  ok  {label:<40} {path}')
print(f'\n{len(edits)} edit(s) applied')
