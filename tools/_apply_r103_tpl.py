#!/usr/bin/env python3
"""r103: the 25 live waves gain the two colours their named pair stood for.

The pair setting is gone from the schema, so each instance has to carry the
actual values or it would fall back to the schema defaults and every boundary
would repaint itself. The old `pair` key is left in place: while both spellings
are present either build of gb-wave.liquid renders the same thing, so the
section push and the template push can land in either order.
"""
import json, pathlib, re, sys

SRC = pathlib.Path('/home/ly/project/Gumi-Brand-shopify/baseline-r102')
OUT = pathlib.Path('/home/ly/project/Gumi-Brand-shopify/work-r103')

LIME, LIME150, GREEN900, CREAM, SAND, WHITE = (
    '#b5ed61', '#e7f8d0', '#004128', '#faf9f8', '#f5f1e9', '#ffffff')
# docs/SCALLOP.md §2.3 -- named "block above-to-block below"
PAIR = {
    'to-lime':        ('',        LIME),      # empty above: the footer CTA case
    'to-green':       (LIME,      GREEN900),
    'to-white':       (LIME150,   WHITE),
    'to-cream':       (WHITE,     CREAM),
    'mint-to-lime':   (LIME150,   LIME),
    'mint-to-cream':  (LIME150,   CREAM),
    'sand-to-lime':   (SAND,      LIME),
    'sand-to-white':  (SAND,      WHITE),
    'lime-to-white':  (LIME,      WHITE),
    'white-to-mint':  (WHITE,     LIME150),
    'white-to-sand':  (WHITE,     SAND),
    'white-to-cream': (WHITE,     CREAM),
    'cream-to-mint':  (CREAM,     LIME150),
    'cream-to-white': (CREAM,     WHITE),
    'cream-to-sand':  (CREAM,     SAND),
}

OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'templates').mkdir(exist_ok=True)
n = 0
for src in sorted(SRC.glob('templates/*.json')):
    raw = src.read_text(encoding='utf-8')
    head = ''
    m = re.match(r'(\s*/\*.*?\*/\s*)', raw, re.S)
    if m: head, raw = m.group(1), raw[len(m.group(1)):]
    d = json.loads(raw)
    touched = []
    for key, sec in (d.get('sections') or {}).items():
        if sec.get('type') != 'gb-wave': continue
        st = sec.get('settings') or {}
        # Kept, not popped: while templates carry both spellings either build of
        # the section renders the right colours, so the two pushes need no
        # ordering and there is no window where every wave repaints itself.
        pair = st.get('pair')
        if pair is None:
            sys.exit(f'ABORT {src.name}/{key}: no "pair" setting -- already migrated?')
        if pair not in PAIR:
            sys.exit(f'ABORT {src.name}/{key}: unknown pair "{pair}"')
        above, below = PAIR[pair]
        st['color_above'], st['color_below'] = above, below
        sec['settings'] = st
        touched.append(f'{key}={pair}->{above or "(empty)"}/{below}')
        n += 1
    if not touched: continue
    (OUT / 'templates' / src.name).write_text(
        head + json.dumps(d, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(f'  {src.name:34} {len(touched)}')
    for x in touched: print(f'      {x}')
print(f'\n{n} wave instances converted')
