#!/usr/bin/env python3
"""r94: .gb-product / --page top padding swap, .gb-vs card floor under last row."""
import io, sys

P = 'assets/customstyle.scss'
src = io.open(P, encoding='utf-8').read()
orig = src

def sub(old, new, label):
    global src
    if src.count(old) != 1:
        sys.exit(f'ANCHOR FAIL ({src.count(old)} hits): {label}')
    src = src.replace(old, new)

# ---- 1. .gb-product base: back to the board's 96 ramp -----------------------
sub("""  padding: 32px 0 calc(96px + var(--sc-h));

  // Client-set: a flat 32 at the top, every width. --lg and --page both restate
  // padding-top below, so this reaches only the plain tiles.
  // Client-set 46 at the foot. --lg and --page both restate padding-bottom in
  // this tier, so the 46 reaches only the plain tiles (reviews / our-story /
  // how-gumi-works) — which is exactly the :not() the brief named.
  @include narrow { padding: 32px 0 calc(46px + var(--sc-h)); }
  @include tablet { padding: 32px fluid(0, 0) calc(fluid(46px, 96px) + var(--sc-h)); }""",
"""  padding: 96px 0 calc(96px + var(--sc-h));

  // Client-set, second revision: the top is back on the board's ramp (r89 had
  // flattened it to 32 at every width). 52 on mobile is 243:22226's own
  // paddingTop 32 plus the 20 its first child adds, the same pair --lg carries.
  // Client-set 46 at the foot. --lg and --page both restate padding-bottom in
  // this tier, so the 46 reaches only the plain tiles (reviews / our-story /
  // how-gumi-works) — which is exactly the :not() the brief named.
  @include narrow { padding: 52px 0 calc(46px + var(--sc-h)); }
  @include tablet { padding: fluid(52px, 96px) fluid(0, 0) calc(fluid(46px, 96px) + var(--sc-h)); }""",
    '.gb-product base padding')

# ---- 2. --lg: same values, note why the restate stays ----------------------
sub("""  // Client-set: --lg keeps the top ramp the base class used to carry. 52 is
  // 243:22226's own paddingTop 32 plus the 20 its first child (Product image,
  // 191:2214) adds -- the build has no element for that inner frame, so the two
  // collapse into one value here.
  padding-top: 96px;""",
"""  // Restated, not inherited: --lg reads the same ramp as the base class today,
  // but the base has been retuned twice on its own (96 -> 32 -> 96) and --lg
  // stayed put both times. 52 is 243:22226's own paddingTop 32 plus the 20 its
  // first child (Product image, 191:2214) adds -- the build has no element for
  // that inner frame, so the two collapse into one value here.
  padding-top: 96px;""",
    '.gb-product--lg comment')

# ---- 3. --page: client wants 32 on desktop --------------------------------
sub("""  // ⚠ Restated, not inherited: the base class dropped to a flat 32 and the PDP
  // board is unchanged at 96 here.
  padding-top: 96px;
  padding-bottom: calc(96px + var(--sc-lg-h));

  // --lg opens with 52 on mobile (the board's 32 + the inner frame's 20
  // collapsed into one). The PDP's own board starts at 20 instead.
  @include narrow { padding-top: 20px; padding-bottom: calc(64px + var(--sc-lg-h)); }
  @include tablet {
    padding-top: fluid(20px, 96px);
    padding-bottom: calc(fluid(64px, 96px) + var(--sc-lg-h));
  }""",
"""  // Client-set: 32 at the top, against the base class's 96 and the PDP board's
  // own 96. The tier below has to land on 32 too or 1280 -> 1281 steps 64px.
  padding-top: 32px;
  padding-bottom: calc(96px + var(--sc-lg-h));

  // --lg opens with 52 on mobile (the board's 32 + the inner frame's 20
  // collapsed into one). The PDP's own board starts at 20 instead; the client
  // named the desktop end only, so this one is unchanged.
  @include narrow { padding-top: 20px; padding-bottom: calc(64px + var(--sc-lg-h)); }
  @include tablet {
    padding-top: fluid(20px, 32px);
    padding-bottom: calc(fluid(64px, 96px) + var(--sc-lg-h));
  }""",
    '.gb-product--page padding-top')

# ---- 4. gb-vs: floor the trailing track so the card never meets the last row
sub("""  // ⚠ The last track is 1fr, not auto, and it is load-bearing: the columns span
  // 1/-1, so without something to absorb the leftover height they'd shrink to
  // their content and .gb-vs__col--gumi::before (height:100%) would come up
  // short of the 25px of card the board leaves under the last row. Flex used to
  // hand that stretch over for free.
  grid-template-rows: repeat(19, auto) 1fr;""",
"""  // ⚠ The last track absorbs the leftover height: the columns span 1/-1, so
  // without it they'd shrink to their content and .gb-vs__col--gumi::before
  // (height:100%) would end flush with the last row. Flex used to hand that
  // stretch over for free.
  // ⚠ The 25px floor is load-bearing, and 1fr alone was not enough: the leftover
  // is (min-height - content), and content grows as the viewport narrows, so the
  // board's 25px of card under the last row thinned to 0 by 1281 and was gone
  // for the whole 768-1024 tier, where `stack` zeroes min-height outright.
  // minmax keeps the 448 board height wherever there is room for it (1440 still
  // measures 46 below the last row) and pins 25 everywhere else.
  grid-template-rows: repeat(19, auto) minmax(25px, 1fr);""",
    '.gb-vs__table trailing track')

# ---- 5. build token -------------------------------------------------------
sub('$build: "20260907-r93";', '$build: "20260908-r94";', '$build')

assert src != orig
io.open(P, 'w', encoding='utf-8').write(src)
print('scss patched: 5 anchors')
