#!/usr/bin/env python3
"""Round 117, item 5: collection + 404 shells align with the header above 1440.

Horizon lays these sections out as a full-bleed grid whose content column is
min(--page-width, 100vw - 2*--page-margin). r106/r107 already redeclared
--page-margin so the gutter matches ours; --page-width was left at the theme's
value, which body.page-width-narrow sets to 1360. Our own shell is 1280, so the
two agree only while the gutter is the binding constraint -- i.e. up to 1440.
Past that the grid sits 40px inside the header. Redeclare the second variable
the same way.
"""
import pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
SCSS = ROOT / 'assets/customstyle.scss'


def sub(old, new):
    t = SCSS.read_text(encoding='utf-8')
    if t.count(old) != 1:
        sys.exit(f'ABORT anchor {t.count(old)}x\n  {old[:90]!r}')
    SCSS.write_text(t.replace(old, new, 1), encoding='utf-8')
    print('  ok')


print('5a. /collections/all')
sub("""  // The theme declares --page-margin on <body>; redeclaring it here re-gutters
  // every section on this template at once, and keeps the safe-area floor.
  --page-margin: max(var(--pad-x), var(--safe-area-inset-left, 0px), var(--safe-area-inset-right, 0px));""",
    """  // The theme declares --page-margin on <body>; redeclaring it here re-gutters
  // every section on this template at once, and keeps the safe-area floor.
  --page-margin: max(var(--pad-x), var(--safe-area-inset-left, 0px), var(--safe-area-inset-right, 0px));

  // Client r117: the gutter alone only aligns while it is the binding side.
  // Horizon's content column is min(--page-width, 100vw - 2*--page-margin), and
  // body.page-width-narrow puts --page-width at 1360 against our 1280 shell --
  // identical up to 1440, then the grid creeps 40 inside the header. Same move
  // as the line above, on the other half of the formula.
  --page-width: #{$w-container};""")

print('5b. /404 product list')
sub("""  // because main-404 above it was not named.
  --page-margin: max(var(--pad-x), var(--safe-area-inset-left, 0px), var(--safe-area-inset-right, 0px));
  padding-block-end: 120px;""",
    """  // because main-404 above it was not named.
  --page-margin: max(var(--pad-x), var(--safe-area-inset-left, 0px), var(--safe-area-inset-right, 0px));
  // Client r117: and the width half of the same formula -- see the note on
  // #MainContent[data-template^="collection"].
  --page-width: #{$w-container};
  padding-block-end: 120px;""")
print('done')
