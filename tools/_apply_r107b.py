#!/usr/bin/env python3
"""r107 asks 3-4. Every replacement asserts its anchor.

  python3 tools/_apply_r107b.py
"""
import pathlib, sys

SCSS = pathlib.Path('assets/customstyle.scss')
edits = []


def sub(path, old, new, label, count=1):
    edits.append((path, old, new, label, count))


# --- 3. .gb-product__tag shrinks to its text -------------------------------
sub(SCSS, """.gb-product__tag {
  align-self: flex-start;
  padding: 6px 12px;""",
    """.gb-product__tag {
  // Live wraps every block in div.shopify-block, so the tag is a plain <p> in
  // normal flow, not a flex item -- align-self cannot reach it there and the
  // green plate runs the whole column.
  display: inline-flex;
  width: auto;
  align-self: flex-start;
  padding: 6px 12px;""",
    "3. gb-product__tag inline-flex")

# --- 4. /404's product-list re-gutters to the site's own --pad-x ------------
sub(SCSS, """.gb-page-wrapper [data-testid="product-list"] {
  padding-block-end: 120px;""",
    """.gb-page-wrapper [data-testid="product-list"] {
  // Client r107: Horizon leaves this section on its own 40/40/16 gutters while
  // every gb-* module runs --pad-x (80/20/20). Redeclaring --page-margin here
  // re-gutters the header, the grid and the cards in one line, safe-area floor
  // kept -- the same move r106 made on /collections/all, scoped to this section
  // because main-404 above it was not named.
  --page-margin: max(var(--pad-x), var(--safe-area-inset-left, 0px), var(--safe-area-inset-right, 0px));
  padding-block-end: 120px;""",
    "4. 404 product-list gutters")

for path, old, new, label, count in edits:
    text = path.read_text(encoding='utf-8')
    n = text.count(old)
    if n != count:
        sys.exit(f'ABORT [{label}] {path}: anchor found {n} time(s), expected {count}')
    path.write_text(text.replace(old, new, count), encoding='utf-8')
    print(f'  ok  {label:<40} {path}')
print(f'\n{len(edits)} edit(s) applied')
