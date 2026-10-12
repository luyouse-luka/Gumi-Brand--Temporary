#!/usr/bin/env python3
"""r107: two client asks. Every replacement asserts its anchor.

  python3 tools/_apply_r107.py
"""
import pathlib, sys

SCSS = pathlib.Path('assets/customstyle.scss')
edits = []


def sub(path, old, new, label, count=1):
    edits.append((path, old, new, label, count))


# --- $build ------------------------------------------------------------------
sub(SCSS, '$build: "20260908-r106";', '$build: "20260908-r107";', 'build token')

# --- 1. .gb-form__check: drop the label's hover colour shift ------------------
# The <a> inside keeps its own hover (rule 13) -- the client named the label.
sub(SCSS, """  // Clicking anywhere in the label toggles the box, so the cursor and the hover
  // feedback belong on the label, not only on the 20px input inside it.
  cursor: pointer;
  transition: trans(color);

  @include hover { color: $c-ink; }
""",
    """  // Clicking anywhere in the label toggles the box, so the cursor belongs on
  // the label, not only on the 20px input inside it.
  // Client r107: no hover colour shift here. The <a> inside keeps its own.
  cursor: pointer;
""",
    "1. gb-form__check drops hover colour")

# --- 2. .gb-page-hero--center desktop padding-top back to the board's 64 ------
sub(SCSS, """  // Client r106: 80 on desktop where 324:69636 draws 64. Mobile keeps the
  // board's 32, so only the ramp's top end moves with it.
  padding: 80px 0 calc(70px + var(--hero-wave));

  @include narrow { padding: 32px 0 calc(64px + var(--hero-wave)); }
  @include tablet { padding: fluid(32px, 80px) fluid(0, 0) calc(fluid(64px, 70px) + var(--hero-wave)); }""",
    """  // 324:69636 draws 64. r106 raised it to 80 on the client's word, r107 put it
  // back. Mobile has always been the board's 32, so only the ramp's top moves.
  padding: 64px 0 calc(70px + var(--hero-wave));

  @include narrow { padding: 32px 0 calc(64px + var(--hero-wave)); }
  @include tablet { padding: fluid(32px, 64px) fluid(0, 0) calc(fluid(64px, 70px) + var(--hero-wave)); }""",
    "2. page-hero--center padding-top 80 -> 64")

for path, old, new, label, count in edits:
    text = path.read_text(encoding='utf-8')
    n = text.count(old)
    if n != count:
        sys.exit(f'ABORT [{label}] {path}: anchor found {n} time(s), expected {count}')
    path.write_text(text.replace(old, new, count), encoding='utf-8')
    print(f'  ok  {label:<40} {path}')
print(f'\n{len(edits)} edit(s) applied')
