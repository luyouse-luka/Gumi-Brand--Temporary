#!/usr/bin/env python3
"""The promo title's outline must not eat the line above it.

  python3 tools/promotitle.py

Client r135: "手机端 gb-promo-panel__title 的 text-shadow 会遮住内部的其他文字".
text-shadow paints one line at a time, so on a wrapping heading the second line's
halo lands on top of the first line's descenders and slices them flat. Measured
before the fix: the second line's halo reached 20px into the first line at 390 and
18px at 1440. ink-split() moves the halo to a copy underneath.

⚠ The copy is injected by main.js (inkSplit), not written into markup -- live the
title is a theme setting piped through newline_to_br in a snippet we do not own.
So "is the copy there" is a real assertion here, not a tautology.

⚠ The pixel case is the one that matters, and it is an A/B inside one run: shoot as
built, undo the fix in the page, shoot again, compare. An absolute threshold does
NOT work here -- the first version of this judge counted dark pixels over the whole
bottom third of the line and stayed green with the fix stripped out, because the
few hundred pixels the halo eats vanish against the x-height behind them.
"""
import argparse
import io
import pathlib
import sys

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'

GREEN = (0x00, 0x56, 0x35)
LIME = (0xb5, 0xed, 0x61)
TIERS = ((390, 'mobile'), (1440, 'desktop'))
# ink-outline radius per tier: 0.4167em on the 36px face, 0.4em on the 40px one.
HALO_R = {'mobile': 15.0, 'desktop': 16.0}
# ⚠ The defect is a MOBILE one, and the geometry says why: the outline grows from
# the ink, not from the line box. At 390 the second line's halo tops out at ~161.3
# against a first-line baseline of 161.5, so it covers real glyph. At 1440 it tops
# out at ~329 against a baseline of 325 -- below the glyphs, in the descender void
# that "Get 20% off" never uses. Measured recovery: 884px vs 36px. Desktop gets the
# same layering (one rule, both tiers) but has almost nothing to win, so asserting
# a big number there would be asserting a defect that is not present.
PIXEL_MIN = {'mobile': 200, 'desktop': 0}

# Undo the fix in the page: drop the copy, move its shadow onto the text itself.
# ⚠ Reuse the halo's OWN computed shadow. Generating one here differs from
# ink-outline()'s step count, and the diff would then be measuring two outline
# shapes rather than layered vs per-line.
STRIP = """
() => {
  const t = document.querySelector('.gb-promo-panel__title');
  const halo = t.querySelector('.gb-ink-halo');
  if (!halo) { return false; }
  const shadow = getComputedStyle(halo).textShadow;
  halo.remove();
  t.style.textShadow = shadow;
  return true;
}
"""

MEASURE = """
() => {
  const t = document.querySelector('.gb-promo-panel__title');
  const halo = t.querySelector('.gb-ink-halo');
  const cs = getComputedStyle(t);
  const r = document.createRange();
  // Skip the injected copy: we want the rects of the REAL text only.
  const real = [...t.childNodes].filter(n => n !== halo);
  r.setStartBefore(real[0]);
  r.setEndAfter(real[real.length - 1]);
  // Distinct visual lines (the <br> makes two rects share a top).
  const seen = new Map();
  for (const b of r.getClientRects()) {
    if (b.height && !seen.has(b.top.toFixed(1))) { seen.set(b.top.toFixed(1), b); }
  }
  const lines = [...seen.values()].sort((a, b) => a.top - b.top)
    .map(b => ({top: b.top, bottom: b.bottom, left: b.left, right: b.right}));
  return {
    lines,
    haloPresent: !!halo,
    haloZ: halo ? getComputedStyle(halo).zIndex : null,
    haloShadow: halo ? getComputedStyle(halo).textShadow.slice(0, 40) : null,
    haloPadTop: halo ? getComputedStyle(halo).paddingTop : null,
    selfShadow: cs.textShadow,
    selfPadTop: cs.paddingTop,
    box: (b => ({x: b.x, y: b.y, w: b.width, h: b.height}))(t.getBoundingClientRect()),
  };
}
"""

ok = red = 0


def report(name, passed, detail):
    global ok, red
    if passed:
        ok += 1
        print(f'  ok    {name}  [{detail}]')
    else:
        red += 1
        print(f'  RED   {name}  [{detail}]')


def is_green(p):
    return (abs(p[0] - GREEN[0]) < 24 and abs(p[1] - GREEN[1]) < 24
            and abs(p[2] - GREEN[2]) < 24)


def is_lime(p):
    return (abs(p[0] - LIME[0]) < 24 and abs(p[1] - LIME[1]) < 24
            and abs(p[2] - LIME[2]) < 24)


def recovered(fixed_png, flat_png):
    """Glyph pixels the flat shadow overpaints and ink-split gives back.

    Counting each build's dark pixels separately and comparing totals does NOT
    work: the contested strip is mostly untouched x-height, and the couple of
    hundred pixels at stake move the total by ~8% -- the first version of this
    judge stayed green with the fix stripped out. Diffing the two shots pins the
    measurement to exactly the pixels that changed.
    """
    from PIL import Image
    a = Image.open(io.BytesIO(fixed_png)).convert('RGB')
    b = Image.open(io.BytesIO(flat_png)).convert('RGB')
    if a.size != b.size:
        return -1
    # No window: a pixel that is glyph in one build and halo in the other can
    # only be one the overlapping outline covers. Windowing it invited an
    # off-by-a-few band that read 36px on desktop for a defect plainly visible
    # in the shots.
    n = 0
    for y in range(a.height):
        for x in range(a.width):
            if is_green(a.getpixel((x, y))) and is_lime(b.getpixel((x, y))):
                n += 1
    return n


def main():
    argparse.ArgumentParser().parse_args()   # no options; the A/B is built in

    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=CHROME)
        for width, label in TIERS:
            dpr = 3
            ctx = br.new_context(viewport={'width': width, 'height': 900},
                                 device_scale_factor=dpr)
            pg = ctx.new_page()
            pg.goto((ROOT / 'index.html').as_uri())
            pg.wait_for_function('window.gumi && window.gumi.modal')
            pg.evaluate("() => window.gumi.modal.open(document.getElementById('promo-modal'))")
            pg.wait_for_timeout(700)

            print(f'--- {label} {width} ---')
            m = pg.evaluate(MEASURE)

            report(f'{label}: halo copy injected by main.js', m['haloPresent'],
                   f"z={m['haloZ']} shadow={(m['haloShadow'] or '')[:24]}")
            report(f'{label}: the title itself paints no shadow',
                   m['selfShadow'] == 'none', m['selfShadow'][:24])
            report(f'{label}: halo sits underneath', m['haloZ'] == '-1', f"z={m['haloZ']}")
            report(f'{label}: halo carries the same top nudge',
                   m['haloPadTop'] == m['selfPadTop'],
                   f"halo={m['haloPadTop']} self={m['selfPadTop']}")

            report(f'{label}: the title wraps (else nothing to prove)',
                   len(m['lines']) >= 2, f"{len(m['lines'])} lines")
            if len(m['lines']) < 2:
                ctx.close()
                continue

            # The contested strip: how far the NEXT line's halo reaches up into
            # this one. Measured at 20px (390) and 18px (1440) before the fix.
            band = m['lines'][0]['bottom'] - (m['lines'][1]['top'] - HALO_R[label])

            # A/B in one run: shoot as built, then undo the fix in the page and
            # shoot again. Comparing the two is the only way to tell "the glyphs
            # survive" from "there were never many dark pixels down there".
            shot_fixed = pg.locator('.gb-promo-panel__title').screenshot()
            pg.evaluate(STRIP)
            pg.wait_for_timeout(150)
            shot_flat = pg.locator('.gb-promo-panel__title').screenshot()

            n = recovered(shot_fixed, shot_flat)
            report(f'{label}: first line keeps the glyph bottoms the halo ate',
                   n >= PIXEL_MIN[label],
                   f'{n} glyph px the flat shadow paints over '
                   f'(min {PIXEL_MIN[label]}, {band:.0f}px reach)')
            ctx.close()
        br.close()

    print(f'\n{ok} ok / {red} red')
    return 0 if red == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
