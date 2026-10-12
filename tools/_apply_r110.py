#!/usr/bin/env python3
"""r110 asks 2-6. Every replacement asserts its anchor.

  python3 tools/_apply_r110.py
"""
import pathlib, sys

SCSS = pathlib.Path('assets/customstyle.scss')
edits = []


def sub(old, new, label, count=1):
    edits.append((old, new, label, count))


# --- 6. accordion open/close is too quick ----------------------------------
sub("""$t-drawer:    0.7s;""",
    """$t-drawer:    0.7s;
// Accordion body. Client r110: $t-slow (0.3s) read as a snap rather than a
// slide -- the panel travels a lot more height than a card lift does, so it
// needs longer to read as motion at all.
$t-acc:       0.45s;""",
    "6a. $t-acc variable")

sub("""    transition:
      block-size $t-slow $ease-out,
      content-visibility $t-slow allow-discrete;""",
    """    transition:
      block-size $t-acc $ease-out,
      content-visibility $t-acc allow-discrete;""",
    "6b. accordion uses $t-acc")

# --- 4. taste list stacks below 370 -----------------------------------------
sub("""".gb-product__taste-list {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  width: 350px;
  max-width: 100%;
}""".strip('"'),
    """.gb-product__taste-list {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  width: 350px;
  max-width: 100%;

  // Client r110: one per row under 370. A layout threshold, so it carries the
  // arrangement only and no values -- the item keeps its own 106 width below.
  @media (max-width: 370px) {
    flex-direction: column;
    justify-content: flex-start;
  }
}""",
    "4. taste-list stacks under 370")

# --- 5. review card title stays on one line on mobile -----------------------
sub(""".gb-crev-card__title {
  font-size: 16px;
  font-weight: 500;
  line-height: 24px;
  letter-spacing: -0.32px;
  color: $c-ink;
}""",
    """.gb-crev-card__title {
  font-size: 16px;
  font-weight: 500;
  line-height: 24px;
  letter-spacing: -0.32px;
  color: $c-ink;

  // Client r110: one line on mobile, clipped with an ellipsis. min-width:0 is
  // required, not decoration -- the title is a flex item and its default
  // min-width:auto refuses to shrink below the text, so the ellipsis never
  // appears and the row overflows instead.
  @include narrow {
    min-width: 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
}""",
    "5. crev-card__title one line on mobile")

text = SCSS.read_text(encoding='utf-8')
for old, new, label, count in edits:
    n = text.count(old)
    if n != count:
        sys.exit(f'ABORT [{label}]: anchor found {n} time(s), expected {count}')
    text = text.replace(old, new, count)
    print(f'  ok  {label}')
SCSS.write_text(text, encoding='utf-8')
print(f'\n{len(edits)} edit(s) applied')
