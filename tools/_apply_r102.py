#!/usr/bin/env python3
"""r102: wave clearance driven by :has() instead of hard-coded per module.

Every module that hosts an --edge wave reserves its height in padding-bottom.
Both facts it needs -- whether there is a wave, and which size -- are decided
elsewhere (a per-instance setting, and the liquid), so the hard-coded reserve
drifted in six places and would be simply wrong the moment a boundary moves to a
Gumi Wave section, which sits in the flow and needs no reserve at all.

Replaces the 22 sites with one variable and lets :has() set it.
"""
import pathlib, re, sys

p = pathlib.Path('assets/customstyle.scss')
t = p.read_text(encoding='utf-8')

RULES = """
// Wave clearance ------------------------------------------------------------
// An --edge wave is absolutely positioned, so its host leaves the room for it in
// its own padding-bottom. Which room is not something the module can know on its
// own: whether it emits a wave is a per-instance setting and the size lives in
// the liquid. Reading both off the DOM keeps the two in step, and gives 0 for a
// boundary that has moved to a Gumi Wave section -- that one is in the flow and
// owns its height, so nothing above it must reserve anything.
// ⚠ --edge-top is deliberately not matched: it hangs off the host's TOP edge and
//   its room belongs to the section ABOVE, which cannot see it from here. The one
//   place that mattered (index, stats -> science) is migrated to a Gumi Wave.
// Specificity does the picking, not source order: the --lg rule is 0-2-0 inside
// :has() against the base rule's 0-1-0.
:where(section, div, footer):has(> .gb-scallop--edge) { --sc-res: var(--sc-h); }
:where(section, div, footer):has(> .gb-scallop--edge.gb-scallop--lg) { --sc-res: var(--sc-lg-h); }
"""
anchor = '.gb-scallop--edge     { bottom: 0; }\n.gb-scallop--edge-top { bottom: 100%; }\n'
if t.count(anchor) != 1:
    sys.exit(f'ABORT: edge anchor x{t.count(anchor)}')
t = t.replace(anchor, anchor + RULES)

# The module reserves. Everything outside the .gb-scallop rules themselves.
head, sep, tail = t.partition(RULES)
n = len(re.findall(r'var\(--sc-h\)|var\(--sc-lg-h\)', tail))
tail = tail.replace('var(--sc-lg-h)', 'var(--sc-res, 0px)').replace('var(--sc-h)', 'var(--sc-res, 0px)')
t = head + sep + tail
print(f'{n} reserve sites rewritten')

# --lg no longer carries a size: :has() decides it. Keep the class, drop the body.
old = '.gb-page-hero--lg { --hero-wave: var(--sc-res, 0px); }'
if t.count(old) != 1:
    sys.exit('ABORT: page-hero--lg not found in expected form')
t = t.replace(old, '// .gb-page-hero--lg no longer sets a wave size -- :has() reads it off the child.')

if t.count('$build: "20260908-r99";') != 1:
    sys.exit('ABORT: build token')
t = t.replace('$build: "20260908-r99";', '$build: "20260908-r100";')

p.write_text(t, encoding='utf-8')
print('scss patched')
