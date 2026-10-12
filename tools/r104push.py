#!/usr/bin/env python3
"""Three-way comparison before the r104 push, and the push list itself.

  baseline = baseline-r103        (live as this round started)
  remote   = live-20260908-0512   (live now)
  local    = work-r104            (what this round changed)

local != baseline  -> ours, goes in the push list
remote != baseline -> theirs, pull forward, never overwrite
both changed       -> conflict, stop

Order matters on the wire and the list is printed in it: the stylesheet defines
.gb-wave--sm/--lg, the section emits those classes, and only then may the
templates name a board size. Landing templates first leaves every wave asking
for a size nothing implements yet.
"""
import hashlib, pathlib, sys

S = pathlib.Path('/home/ly/project/Gumi-Brand-shopify')
# Baseline is the tree AFTER our gb-footer push (r104 a), so that file reads as
# already-landed rather than as a conflict between remote and local.
BASE, REMOTE, LOCAL = S / 'verify-r104', S / 'prepush-r104b', S / 'work-r104'
ORDER = ('assets/', 'snippets/', 'sections/', 'templates/')


def md5(p):
    return hashlib.md5(p.read_bytes()).hexdigest() if p.is_file() else None


if not (REMOTE / 'sections').is_dir():
    sys.exit('ABORT: the remote tree is not a theme pull')

ours, theirs, conflict, push = [], [], [], []
for lp in sorted(LOCAL.rglob('*')):
    if not lp.is_file():
        continue
    rel = lp.relative_to(LOCAL)
    b, r, l = md5(BASE / rel), md5(REMOTE / rel), md5(lp)
    if l == b:
        continue
    ours.append(str(rel))
    if r != b:
        conflict.append(f'{rel}  (baseline {b and b[:8]} / remote {r and r[:8]})')
    else:
        push.append(str(rel))

for rp in sorted(REMOTE.rglob('*')):
    if not rp.is_file():
        continue
    rel = rp.relative_to(REMOTE)
    if md5(BASE / rel) != md5(rp):
        theirs.append(str(rel))

print(f'ours     ({len(ours)}): ' + ', '.join(ours))
print(f'\ntheirs   ({len(theirs)}) since {BASE.name} was taken:')
for t in theirs:
    print(f'  {t}')
print(f'\nCONFLICT ({len(conflict)}):')
for c in conflict:
    print(f'  {c}')

push.sort(key=lambda p: next((i for i, pre in enumerate(ORDER) if p.startswith(pre)), len(ORDER)))
print(f'\n--- push list ({len(push)}), dependency order ---')
for p in push:
    print(f'  {p}')
print('\n--- command ---')
print('shopify theme push --store je1ka9-er.myshopify.com --theme 180348977399 \\\n  '
      + ' \\\n  '.join(f'--only {p}' for p in push) + ' \\\n  --nodelete --allow-live')
sys.exit(1 if conflict else 0)
