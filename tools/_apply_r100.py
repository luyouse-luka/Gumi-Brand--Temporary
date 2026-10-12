#!/usr/bin/env python3
"""r100: .gb-wave -- a wave the merchant places, with a chosen number of arcs."""
import pathlib, sys

p = pathlib.Path('assets/customstyle.scss')
t = p.read_text(encoding='utf-8')

anchor = """.gb-scallop--edge     { bottom: 0; }
.gb-scallop--edge-top { bottom: 100%; }
"""
block = anchor + """
// Merchant-placed wave ------------------------------------------------------
// Everything is drawn by .gb-scallop; this only retunes the pitch, so a wave
// added from the theme editor carries an exact number of arcs across the
// viewport instead of however many the design's fixed pitch happens to fit.
//
//   <div class="gb-scallop gb-wave gb-scallop--white-to-cream" style="--wave-n:3">
//
// The 58 built-in waves are untouched: they never carry .gb-wave, so --wave-w
// still comes from :root as before.
//
// It stays in the flow and owns its height -- .gb-scallop is position:relative
// and only --edge/--edge-top take it out, which is what lets the merchant drop
// it between any two sections without the section above reserving room for it in
// padding-bottom. That reservation is the thing most easily got wrong about the
// built-in waves (see docs/SCALLOP.md §3); this variant does not have it.
//
// ⚠ 100vw counts the scrollbar, so on desktop the last arc would be clipped and
//   the count read short. --scrollbar-w is measured by scrollbarProbe in main.js;
//   it is 0 where the scrollbar is an overlay (mobile), which is correct there.
//   ⚠ Headless Chromium reports 0 as well, so the subtraction cannot be verified
//   locally -- see docs/SCALLOP.md.
//
// Band: the near-zero run of --sc-lg-band, so the height is essentially the arc
// amplitude. Reusing --sc-band would add a solid strip that grows the box without
// changing the wave, which reads as a stray coloured bar at 5 arcs.
.gb-wave {
  --wave-w: calc((100vw - var(--scrollbar-w, 0px)) / var(--wave-n, 5));
  --wave-band: #{clamp(0.5px, 0.139vw, 2px)};
  --wave-h: calc(var(--wave-w) * 0.24008 + var(--wave-band));
}
"""
if t.count(anchor) != 1:
    sys.exit(f'ABORT: anchor x{t.count(anchor)}')
t = t.replace(anchor, block)

old_build = '$build: "20260908-r98";'
if t.count(old_build) != 1:
    sys.exit('ABORT: build token not found')
t = t.replace(old_build, '$build: "20260908-r99";')

p.write_text(t, encoding='utf-8')
print('scss patched')
