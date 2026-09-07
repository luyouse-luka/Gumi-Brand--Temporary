#!/usr/bin/env python3
"""account.scss keeps its own copy of the tokens (decision 5). This proves the
copy still matches customstyle.scss, so drift fails loudly instead of silently."""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "customstyle.scss"
DST = ROOT / "assets" / "account.scss"
# only the tokens account actually mirrors; $build is deliberately per-file
WATCH = re.compile(
    r'^\$(c-[\w-]+|bp-[\w-]+|font-[\w-]+|sans-fallback)\s*:\s*([^;/]+?)\s*(?://.*)?;', re.M)

def grab(p):
    if not p.exists():
        print(f"RED  missing file: {p}")
        return None
    return {m.group(1): m.group(2).strip() for m in WATCH.finditer(p.read_text())}

a, b = grab(SRC), grab(DST)
if a is None or b is None:
    sys.exit(1)

missing = sorted(set(a) - set(b))
drifted = sorted(k for k in set(a) & set(b) if a[k] != b[k])
extra   = sorted(set(b) - set(a))

for k in missing: print(f"RED  missing in account.scss: ${k} = {a[k]}")
for k in drifted: print(f"RED  drifted: ${k}  customstyle={a[k]}  account={b[k]}")
for k in extra:   print(f"note account-only token: ${k} = {b[k]}")
ok = len(set(a) & set(b)) - len(drifted)
print(f"\n{ok} ok / {len(missing)+len(drifted)} red")
sys.exit(1 if missing or drifted else 0)
