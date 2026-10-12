#!/usr/bin/env python3
"""Round 116: fill the science CTA setting the r115 section already reads.

  python3 tools/_apply_r116_tpl.py --src <latest pull dir> --out <push dir>

templates/*.json is a red line (Online Store Editor owns it). This round the
user authorised this one file explicitly. Same discipline as r102/r104/r113:
build off the LATEST pull, touch only the target settings, abort if the section
is not what we expect. indent=2 round-trips this file byte-for-byte, so the
diff is exactly the keys set below and nothing else.

r115 shipped .gb-science__cta plus the section's cta_label/cta_url settings but
could not fill them (templates were not authorised then), so the button has
been invisible live ever since. Label and link match the Shop Now already on
the same page (section `ingredients`).
"""
import argparse, json, re, shutil, sys
from pathlib import Path

TARGET = 'templates/page.science.json'
SECTION = 'nutrients'
WANT = {'cta_label': 'Shop Now', 'cta_url': '/collections/all'}

ap = argparse.ArgumentParser()
ap.add_argument('--src', required=True, help='latest theme pull, the base to build on')
ap.add_argument('--out', required=True)
a = ap.parse_args()
src, out = Path(a.src), Path(a.out)
if not (src / TARGET).exists():
    sys.exit(f'ABORT: {src / TARGET} missing -- pass the pull directory')

raw = (src / TARGET).read_text(encoding='utf-8')
m = re.match(r'(\s*/\*.*?\*/\s*)', raw, re.S)
head, body = (m.group(1), raw[len(m.group(1)):]) if m else ('', raw)
d = json.loads(body)

sec = d.get('sections', {}).get(SECTION)
if sec is None or sec.get('type') != 'gb-science':
    sys.exit(f'ABORT: sections.{SECTION} is not a gb-science section -- live has moved')
st = sec.setdefault('settings', {})
if st.get('tight') is not True:
    sys.exit(f'ABORT: sections.{SECTION} is not the tight variant (tight={st.get("tight")!r})')
if st.get('background') != 'cream':
    sys.exit(f'ABORT: sections.{SECTION} background is {st.get("background")!r}, expected cream')

for k, v in WANT.items():
    print(f'  set  {SECTION}.{k}: {st.get(k)!r} -> {v!r}')
    st[k] = v

new = head + json.dumps(d, indent=2, ensure_ascii=False) + '\n'
# round-trip guard: re-reading must give back exactly what we intended
chk = json.loads(re.sub(r'\A\s*/\*.*?\*/\s*', '', new, flags=re.S))
assert chk['sections'][SECTION]['settings']['cta_label'] == WANT['cta_label']
(out / 'templates').mkdir(parents=True, exist_ok=True)
(out / TARGET).write_text(new, encoding='utf-8')
print(f'  wrote {out / TARGET}')
