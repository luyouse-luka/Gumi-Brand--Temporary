#!/usr/bin/env python3
"""Three-way comparison before the r99 push, and the push list itself.

  baseline = live-r99   (what live looked like when this round started)
  remote   = prepush-r99 (what live looks like now)
  local    = work-r99   (what this round changed)

local != baseline  -> ours, goes in the push list
remote != baseline -> theirs, must be pulled forward, never overwritten
both changed       -> conflict, stop
"""
import hashlib, pathlib, sys

S = pathlib.Path('/home/ly/project/Gumi-Brand-shopify')
BASE, REMOTE, LOCAL = S / 'live-r99', S / 'prepush-r99', S / 'work-r99'

def md5(p):
    return hashlib.md5(p.read_bytes()).hexdigest() if p.is_file() else None

if not (REMOTE / 'sections').is_dir():
    sys.exit('ABORT: prepush-r99 is not a theme pull')

ours, theirs, conflict, push = [], [], [], []
for lp in sorted(LOCAL.rglob('*.liquid')):
    rel = lp.relative_to(LOCAL)
    b, r, l = md5(BASE / rel), md5(REMOTE / rel), md5(lp)
    if l == b:
        continue                      # we did not touch it
    ours.append(str(rel))
    if r != b:
        conflict.append(f'{rel}  (baseline {b and b[:8]} / remote {r and r[:8]})')
    else:
        push.append(str(rel))

# everything they changed anywhere in the theme, ours or not
for rp in sorted(REMOTE.rglob('*')):
    if not rp.is_file(): continue
    rel = rp.relative_to(REMOTE)
    if md5(BASE / rel) != md5(rp):
        theirs.append(str(rel))

print(f'ours     ({len(ours)}): ' + ', '.join(ours))
print(f'\ntheirs   ({len(theirs)}) since live-r99 was taken:')
for t in theirs: print(f'  {t}')
print(f'\nCONFLICT ({len(conflict)}):')
for c in conflict: print(f'  {c}')
print(f'\n--- push list ({len(push)}) ---')
for p in push: print(f'  {p}')

if conflict:
    sys.exit('\nABORT: a file we changed also changed on live. Merge by hand.')

order = [p for p in push if p.startswith('snippets/')], [p for p in push if p.startswith('sections/')]
for step, group in enumerate(order, 1):
    if not group: continue
    print(f'\n=== step {step} ===')
    print('shopify theme push --store je1ka9-er.myshopify.com --theme 180348977399 '
          '--nodelete --allow-live --path work-r99 \\\n    '
          + ' \\\n    '.join(f'--only {g}' for g in group))
