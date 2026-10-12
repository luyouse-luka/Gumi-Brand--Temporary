#!/usr/bin/env python3
"""Three-way comparison before the r107 push, and the push list itself.

  baseline = baseline-r106   (what live looked like when this round started)
  remote   = prepush-r107 (what live looks like now)
  local    = work-r107   (what this round changed)

local != baseline  -> ours, goes in the push list
remote != baseline -> theirs, must be pulled forward, never overwritten
both changed       -> conflict, stop
"""
import hashlib, pathlib, sys

S = pathlib.Path('/home/ly/project/Gumi-Brand-shopify')
BASE, REMOTE, LOCAL = S / 'baseline-r106', S / 'prepush-r107', S / 'work-r107'

def md5(p):
    return hashlib.md5(p.read_bytes()).hexdigest() if p.is_file() else None

if not (REMOTE / 'sections').is_dir():
    sys.exit('ABORT: prepush-r107 is not a theme pull')

ours, theirs, conflict, push = [], [], [], []
for lp in sorted(LOCAL.rglob('*')):
    if not lp.is_file(): continue
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
print(f'\ntheirs   ({len(theirs)}) since baseline-r106 was taken:')
for t in theirs: print(f'  {t}')
print(f'\nCONFLICT ({len(conflict)}):')
for c in conflict: print(f'  {c}')
print(f'\n--- push list ({len(push)}) ---')
for p in push: print(f'  {p}')

if conflict:
    sys.exit('\nABORT: a file we changed also changed on live. Merge by hand.')

# Order does not matter this round -- templates carry both the old pair and the
# new colours, so either build of the section renders the same thing.
order = ([p for p in push if p.startswith('sections/')],
         [p for p in push if p.startswith('templates/')])
for step, group in enumerate(order, 1):
    if not group: continue
    print(f'\n=== step {step} ===')
    print('shopify theme push --store je1ka9-er.myshopify.com --theme 180348977399 '
          '--nodelete --allow-live --path work-r107 \\\n    '
          + ' \\\n    '.join(f'--only {g}' for g in group))
