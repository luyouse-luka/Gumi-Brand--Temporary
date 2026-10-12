#!/usr/bin/env python3
"""Read-back judge for a Shopify asset push. Run it after `theme pull` and
before rolling the baseline.

    python3 tools/acctpush.py <baseline-dir> <verify-dir> <pushed-path>...

A pushed path may be written `<theme-path>=<local-path>` to also assert the file
came back byte-identical to what was sent -- "it exists" reads green on a stale
version, and the theme path differs from the local one for every image
(`assets/x.png` in the theme, `images/x.png` in the static site).

⚠ Assertion 0 is not decoration: a half-finished pull leaves most files absent,
and "nothing else changed" is then true on an empty set. That is how a broken
push read green on 2026-09-08.
"""
import hashlib, pathlib, sys

if len(sys.argv) < 4:
    sys.exit(__doc__)
BASE, VERIFY = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
PUSHED = sys.argv[3:]

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def tree(root):
    return {str(p.relative_to(root)): p for p in root.rglob('*') if p.is_file()}

base, ver = tree(BASE), tree(VERIFY)
ok = red = 0

def check(label, got, want):
    global ok, red
    if got == want:
        print("ok   %-54s %s" % (label, got)); ok += 1
    else:
        print("RED  %-54s got %r want %r" % (label, got, want)); red += 1

check("pull came back whole (files >= baseline)", len(ver) >= len(base), True)
if len(ver) < len(base):
    sys.exit("\nABORT: short pull -- every assertion below would pass on an empty set")

SRC = {}
for i, spec in enumerate(PUSHED):
    if "=" in spec:
        PUSHED[i], SRC[spec.split("=", 1)[0]] = spec.split("=", 1)

for rel in PUSHED:
    dst = VERIFY / rel
    check("landed: %s" % rel, dst.exists(), True)
    src = SRC.get(rel)
    if src and dst.exists():
        check("byte-identical: %s" % rel, sha(dst), sha(pathlib.Path(src)))

missing = sorted(set(base) - set(ver))
check("no baseline file disappeared", missing[:5] if missing else [], [])
changed = sorted(r for r in base if r in ver and r not in PUSHED and sha(base[r]) != sha(ver[r]))
check("no collateral edits", changed[:5] if changed else [], [])
added = sorted(set(ver) - set(base) - set(PUSHED))
check("nothing added beyond the push list", added[:5] if added else [], [])

print("\n%d ok / %d red" % (ok, red))
sys.exit(1 if red else 0)
