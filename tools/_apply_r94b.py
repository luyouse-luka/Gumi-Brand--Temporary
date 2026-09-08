#!/usr/bin/env python3
"""r94b: styles for the two classes the live section emits and we never had."""
import io, sys

P = 'assets/customstyle.scss'
s = io.open(P, encoding='utf-8').read(); o = s

def sub(a, b, tag):
    global s
    if s.count(a) != 1:
        sys.exit(f'ANCHOR FAIL ({s.count(a)}): {tag}')
    s = s.replace(a, b)

# .is-voted -- the live section's inline script adds it on click; the static
# build never does, so this state only ever shows up on the storefront.
sub("""  transition: trans(color, transform);

  svg { flex: none; width: 16px; height: 16px; }

  @include hover { color: $c-green; }
  &:active { transform: scale(0.94); }
}""",
"""  transition: trans(color, transform);

  svg { flex: none; width: 16px; height: 16px; stroke-width: 1.33333; transition: trans(stroke-width); }

  @include hover { color: $c-green; }
  &:active { transform: scale(0.94); }

  // Live only: sections/gb-app-section.liquid's inline script toggles .is-voted
  // and persists it in localStorage. Same 0-2-0 as the :hover above, so it has
  // to stay after it. Self-set values -- no board covers a voted state.
  &.is-voted {
    color: $c-green;
    svg { stroke-width: 2; }
  }
}""", '.is-voted')

# .gb-crev__empty -- live-only too: the static build always ships cards.
sub(""".gb-crev__list {
  display: flex;""",
""".gb-crev__empty {
  font-size: 16px;
  line-height: 24px;
  letter-spacing: -0.32px;
  color: $c-gray-700;
  text-align: center;
  padding: 32px 0;

  @include narrow { font-size: 14px; line-height: 20px; letter-spacing: -0.28px; padding: 24px 0; }
  @include tablet {
    font-size: fluid(14px, 16px);
    line-height: fluid(20px, 24px);
    letter-spacing: fluid(-0.28px, -0.32px);
    padding: fluid(24px, 32px) 0;
  }
}

.gb-crev__list {
  display: flex;""", '.gb-crev__empty')

assert s != o
io.open(P, 'w', encoding='utf-8').write(s)
print('scss patched: 2 anchors')
