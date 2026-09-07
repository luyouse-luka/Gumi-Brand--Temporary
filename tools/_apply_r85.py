#!/usr/bin/env python3
"""r85: nine client-named fixes. Run once from the repo root."""
import pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCSS = ROOT / 'assets/customstyle.scss'
JS = ROOT / 'assets/main.js'

def sub(text, old, new, tag):
    n = text.count(old)
    if n != 1:
        sys.exit('%s: anchor found %d times, expected 1' % (tag, n))
    return text.replace(old, new)

s = SCSS.read_text()

# 1 -- thumb focus mirrors the active thumb
s = sub(s, """  &.is-active { border-color: $c-green; }

  @include hover { opacity: 0.75; }""",
"""  &.is-active { border-color: $c-green; }

  // Client r85: focus reads as the active thumb rather than a ring. The rail
  // scrolls, and an overflow on either axis forces the other to auto too, so
  // .gb-product__thumbs clipped the global 2px/2px outline on all four sides --
  // the same reason .gb-reel dropped its ring in r81.
  &:focus-visible { outline: none; border-color: $c-green; }

  @include hover { opacity: 0.75; }""", '1 thumb focus')

# 2 -- guarantee icons are <img> on live
s = sub(s, """  svg { width: 34px; height: 32px; color: $c-cream; }""",
"""  // Same <img> swap as .gb-product__taste-item -- see the note there.
  // blocks/_gb-guarantee.liquid renders <img width="80">, which the svg-only
  // rule never sized; the static site still ships the svg.
  svg, img { width: 34px; height: 32px; object-fit: contain; color: $c-cream; }""",
   '2 guarantee icon')

# 3 -- the plan stroke has to paint over the children
s = sub(s, """// ⚠ inset shadow, NOT border: the board's stroke is strokeAlign INSIDE, so it
// paints over the 90/76 box instead of adding to it. A real border would also
// push the banner 1px in and make the popular card 336 where the board is 334.
.gb-sub__plan {
  box-shadow: inset 0 0 0 1px $c-green;
  border-radius: 16px;
  // the banner is flush with the top corners, so the card has to clip it
  overflow: hidden;
""",
"""// ⚠ Overlay ring, NOT a border: the board's stroke is strokeAlign INSIDE, so
// it paints over the 90/76 box instead of adding to it. A real border would also
// push the banner 1px in and make the popular card 336 where the board is 334.
// ⚠ And not the inset shadow it was until r85 either: an inset shadow paints
// UNDER the children, and --sub's .gb-sub__panel fills the card edge to edge, so
// the stroke only ever showed on --once, whose background sits on the card.
.gb-sub__plan {
  position: relative;
  border-radius: 16px;
  // the banner is flush with the top corners, so the card has to clip it
  overflow: hidden;

  &::after {
    content: "";
    position: absolute;
    inset: 0;
    border: 1px solid $c-green;
    border-radius: inherit;
    pointer-events: none;
  }
""", '3 sub plan ring')

# 4 -- divider
s = sub(s, """.gb-footer__divider {
  height: 1px;
  background: $c-lime;""",
""".gb-footer__divider {
  height: 1px;
  background: $c-lime;
  opacity: 0.2;""", '4 footer divider')

# 5 -- panel top edge (desktop dropdown only)
s = sub(s, """  background: $c-cream;
  border-bottom: 1px solid $c-sand;
  border-radius: 0 0 32px 32px;""",
"""  background: $c-cream;
  border-top: 1px solid $c-sand;
  border-bottom: 1px solid $c-sand;
  border-radius: 0 0 32px 32px;""", '5 panel border-top')

s = sub(s, """    border-radius: 0;
    border-bottom: 0;""",
"""    border-radius: 0;
    // Both edges off: the phone drawer is full-viewport from y=0, so the top
    // hairline would land under the status bar and the board draws neither.
    border-top: 0;
    border-bottom: 0;""", '5b panel border-top narrow')

# 6 -- panel columns top-aligned
s = sub(s, """.gb-header__panel-inner {
  @include container;
  display: flex;
  justify-content: space-between;
  align-items: center;""",
""".gb-header__panel-inner {
  @include container;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;""", '6 panel-inner align')

# 7 -- the logo is an <img> whenever settings.logo is uploaded
s = sub(s, """  svg { width: 124px; height: 32px; }

  @include narrow {
    svg { width: 93px; height: 24px; }
  }""",
"""  // <img> as well as <svg>: snippets/gb-logo.liquid swaps to an <img> the
  // moment settings.logo is uploaded, and its width/height attributes carry the
  // desktop pair only -- svg-only rules left the phone drawer at 124x32.
  svg, img { width: 124px; height: 32px; object-fit: contain; }

  @include narrow {
    svg, img { width: 93px; height: 24px; }
  }""", '7 header logo')

s = sub(s, """  svg { display: block; width: 93px; height: 24px; }""",
"""  svg, img { display: block; width: 93px; height: 24px; object-fit: contain; }""",
   '7b panel logo')

s = sub(s, """.gb-footer__logo svg {
  width: 193px;
  height: 50px;""",
""".gb-footer__logo svg,
.gb-footer__logo img {
  width: 193px;
  height: 50px;
  object-fit: contain;""", '7c footer logo')

# 8 -- nav card artwork stops overhanging on phones
s = sub(s, """  pointer-events: none;
  z-index: 1;

  .gb-header.is-open & { display: block; }""",
"""  pointer-events: none;
  z-index: 1;

  // Client r85: the phone drawer's card is far narrower than the desktop one, so
  // the 135.2% overhang ran the artwork outside it.
  @include narrow { width: 100%; }

  .gb-header.is-open & { display: block; }""", '8 nav card art')

# 9 -- a rail that fits does not scroll
s = sub(s, """// Grey box with a play glyph is the design's own placeholder for the reel.""",
"""// Too few cards to fill the track: main.js leaves Swiper off -- there is nothing
// to scroll and `loop` has no room to wrap -- and marks the rail .is-static.
// Without Swiper the slide margins that carried the spacing are gone, so the gap
// has to come off the wrapper; `inherit` keeps the responsive column-gap above as
// its single source instead of restating the ramp.
[data-slider].is-static > [data-slider-track] > .swiper-wrapper {
  justify-content: center;
  column-gap: inherit;
}

// Nothing left for them to do, and the desktop board draws no nav wherever the
// whole set is already side by side.
[data-slider].is-static .gb-reels__nav { display: none; }

// Grey box with a play glyph is the design's own placeholder for the reel.""",
   '9 reels static')

SCSS.write_text(s)

j = JS.read_text()
j = sub(j, """      if (!(until > 0)) { create(); return; }

      // Rails that only exist below a breakpoint. matchMedia rather than
      // Swiper's own `breakpoints: {enabled: false}`: disabling leaves the loop
      // duplicates in the DOM, and above the threshold those show up as extra
      // grid cells.
      var mq = matchMedia("(max-width: " + until + "px)");
      var apply = function () { if (mq.matches) { create(); } else { destroy(); } };
      if (mq.addEventListener) { mq.addEventListener("change", apply); }
      else if (mq.addListener) { mq.addListener(apply); }
      apply();""",
"""      // Client r85: a rail whose cards already fit the track has nothing to
      // scroll, and `loop` has no room to wrap -- Swiper parks the set against
      // the left edge instead of centring it. Measured, not counted: the card
      // width is a vw ramp, so "enough cards" is a different number at every
      // viewport (four fit at 1440, no count fits at 390).
      // ⚠ loop rails only. `rewind` is built to dead-end at any count, and the
      // expert rail's three cards fit their track in the last 30px before it
      // becomes a grid -- going static there is a layout nobody asked for.
      var fits = function () {
        if (!loop) { return false; }
        var sl = track.querySelectorAll(".swiper-slide");
        if (!sl.length) { return false; }
        var total = 0;
        for (var i = 0; i < sl.length; i++) {
          total += sl[i].getBoundingClientRect().width;
        }
        var gap = parseFloat(getComputedStyle(track).columnGap) || 0;
        return total + gap * (sl.length - 1) <= track.clientWidth;
      };

      // Rails that only exist below a breakpoint. matchMedia rather than
      // Swiper's own `breakpoints: {enabled: false}`: disabling leaves the loop
      // duplicates in the DOM, and above the threshold those show up as extra
      // grid cells.
      var mq = until > 0 ? matchMedia("(max-width: " + until + "px)") : null;
      var apply = function () {
        var railed = !mq || mq.matches;
        var stat = railed && fits();
        if (railed && !stat) { create(); } else { destroy(); }
        root.classList.toggle("is-static", stat);
      };
      if (mq) {
        if (mq.addEventListener) { mq.addEventListener("change", apply); }
        else if (mq.addListener) { mq.addListener(apply); }
      }
      // Width only: the mobile toolbar sliding away fires resize at the same
      // width, and tearing the rail down on that is a visible jump.
      var lastW = window.innerWidth;
      window.addEventListener("resize", function () {
        if (window.innerWidth === lastW) { return; }
        lastW = window.innerWidth;
        apply();
      });
      apply();""", '9 slider fits')
JS.write_text(j)
print('r85 applied')
