#!/usr/bin/env python3
"""r110 ask 1 -- the stars read bigger since the star.svg swap.

  python3 tools/_apply_r110c.py
"""
import pathlib, sys

SCSS = pathlib.Path('assets/customstyle.scss')
edits = []


def sub(old, new, label):
    edits.append((old, new, label))


NOTE = """  // ⚠ The padding is the point, not the box. Measured ink inside each file:
  // the old star.svg was viewBox 32x32 with the shape filling 79.7% x 75.2%;
  // the replacement (r108, other session) is viewBox 25x24 filled 99.6% x 99.2%.
  // Same container, so the mark itself jumped 25.5 -> 31.87 wide and read as a
  // size change. 10% padding each side hands the old breathing room back.
  // ⚠ The BOX stays at the board's figure -- 324:63950 is 32 and the row frame
  // is 160 (5 x 32) -- so only the ink moves, not the layout."""

sub("""  img { flex: none; width: 32px; height: 32px; }
}""",
    """  img {
    flex: none;
    width: 32px;
    height: 32px;
""" + NOTE + """
    box-sizing: border-box;
    padding: 3.2px;
  }
}""",
    "1a. gb-crev__stars ink back to the pre-swap size")

sub("""  // Same as .gb-crev__stars -- see the note there.
  img { flex: none; width: 20px; height: 20px; }
}""",
    """  // Same as .gb-crev__stars -- see the note there, padding included.
  img {
    flex: none;
    width: 20px;
    height: 20px;
    box-sizing: border-box;
    padding: 2px;
  }
}""",
    "1b. gb-crev-card__rating likewise")

text = SCSS.read_text(encoding='utf-8')
for old, new, label in edits:
    n = text.count(old)
    if n != 1:
        sys.exit(f'ABORT [{label}]: anchor found {n} time(s), expected 1')
    text = text.replace(old, new, 1)
    print(f'  ok  {label}')
SCSS.write_text(text, encoding='utf-8')
