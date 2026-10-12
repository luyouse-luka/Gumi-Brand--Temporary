#!/usr/bin/env python3
"""Read-back check for the r99 push.

Asserts three things against a fresh full pull:
  1  every file in the push list is byte-identical to what we meant to send
  2  nothing else changed against prepush-r103 (the snapshot taken just before)
  3  the file count did not drop -- `--nodelete` held
"""
import hashlib, pathlib, sys

S = pathlib.Path('/home/ly/project/Gumi-Brand-shopify')
PRE, VER, LOCAL = S / 'prepush-r103', S / 'verify-r103', S / 'work-r103'
PUSHED = sorted(str(p.relative_to(LOCAL)) for p in LOCAL.rglob('*') if p.is_file())

def md5(p): return hashlib.md5(p.read_bytes()).hexdigest() if p.is_file() else None

# One-shot: valid only between the push and the baseline roll. Afterwards
# prepush-r103 is gone and verify-r103 has become baseline-r99, so every
# comparison would read as a difference rather than as a missing input.
for d in (PRE, VER):
    if not d.is_dir():
        sys.exit(f'ABORT: {d.name} is gone -- the baseline has already been rolled '
                 f'(verify-r103 -> baseline-r99). This judge only runs between the '
                 f'push and that roll; re-pull both trees to rerun it.')

ok = red = 0
def grade(c, label, detail=''):
    global ok, red
    if c: ok += 1; print(f'  ok   {label}')
    else: red += 1; print(f'  RED  {label}   {detail}')

npre = sum(1 for p in PRE.rglob('*') if p.is_file())
nver = sum(1 for p in VER.rglob('*') if p.is_file())
# Liveness: a pull still in flight leaves most files absent, which would make the
# collateral-change check pass on nothing at all. Refuse to grade a partial tree.
if nver < npre:
    sys.exit(f'ABORT: verify-r103 holds {nver} files, prepush-r103 holds {npre}. '
             'Either the pull is unfinished or files really went missing -- '
             'rerun the pull and check before reading anything into this.')
grade(nver >= npre, f'file count held ({npre} -> {nver})')

print(f'\n--- the {len(PUSHED)} files we pushed ---')
for rel in PUSHED:
    grade(md5(VER / rel) == md5(LOCAL / rel), f'{rel} byte-identical on live',
          f'live {md5(VER/rel)} vs local {md5(LOCAL/rel)}')

print('\n--- everything else must be untouched ---')
stray = []
for p in sorted(VER.rglob('*')):
    if not p.is_file(): continue
    rel = str(p.relative_to(VER))
    if rel in PUSHED: continue
    if md5(PRE / rel) != md5(p): stray.append(rel)
grade(not stray, f'no collateral change ({len(stray)} files differ)', str(stray[:6]))

print(f'\n{ok} ok / {red} red')
sys.exit(1 if red else 0)
