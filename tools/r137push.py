#!/usr/bin/env python3
"""Three-way comparison before the r137 push, and the push list itself.

  baseline = baseline-20260910-r136   (live when this round started)
  remote   = prepush-r137             (live right now)
  local    = work-r137                (a copy of remote + this round's assets)

⚠ `local` is a COPY of `remote`, not an independent tree, so the push predicate is
`local != remote`. Using `local != baseline` -- correct only when local descends
from baseline -- would list the other party's files as things for us to push back.
"""
import hashlib, pathlib, sys

S = pathlib.Path('/home/ly/project/Gumi-Brand-shopify')
BASE, REMOTE, LOCAL = S/'baseline-20260910-r136', S/'prepush-r137', S/'work-r137'

def md5(p):
    return hashlib.md5(p.read_bytes()).hexdigest() if p.is_file() else None

if not (REMOTE/'sections').is_dir():
    sys.exit('ABORT: prepush-r137 is not a theme pull')

push, conflict = [], []
for lp in sorted(LOCAL.rglob('*')):
    if not lp.is_file(): continue
    rel = lp.relative_to(LOCAL)
    b, r, l = md5(BASE/rel), md5(REMOTE/rel), md5(lp)
    if l == r: continue                       # we did not change it
    push.append(str(rel))
    if r != b:                                # they moved it too
        conflict.append(f'{rel}  (baseline {b and b[:8]} / remote {r and r[:8]})')

theirs = [str(rp.relative_to(REMOTE)) for rp in sorted(REMOTE.rglob('*'))
          if rp.is_file() and md5(BASE/rp.relative_to(REMOTE)) != md5(rp)]

print(f'ours     ({len(push)}): ' + ', '.join(push))
print(f'\ntheirs   ({len(theirs)}) since baseline-20260910-r136 was taken:')
for t in theirs: print(f'  {t}')
print(f'\nCONFLICT ({len(conflict)}):')
for c in conflict: print(f'  {c}')

if conflict:
    sys.exit('\nABORT: a file we changed also changed on live. Merge by hand.')

print('\n=== push ===')
print('shopify theme push --store je1ka9-er.myshopify.com --theme 180348977399 '
      '--nodelete --allow-live --path work-r137 \\\n    '
      + ' \\\n    '.join(f'--only {p}' for p in push))
