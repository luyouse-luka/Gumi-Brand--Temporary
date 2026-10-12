#!/usr/bin/env python3
"""r104: point the 25 live waves at the board sizes, and fix two colours.

Read live -> change only the named keys -> write back. Nothing else in these
templates is touched, which is the condition the templates/*.json red line is
relaxed under (docs/PUSH-LOG.md).

`count` moves from an arc count to a board size, so each boundary renders at the
height the design drew it. Live already pads the block above by the net value --
the wave is in flow and --sc-res does not fire -- so restoring the height
restores the gap between the two blocks as well.

Sizes come from the static build measured per boundary (tools/r104map.py):
h 129 -> lg, h 96.9 -> sm.
"""
import argparse, json, pathlib, re, sys

# The source must be the FRESHEST pull, not a fixed snapshot: the other team
# edits these templates from the admin while we work (2026-09-08, they fixed
# get-in-touch's form_type between our pull and our push). Rebuilding against a
# stale tree would quietly revert whatever they changed in the meantime.
ap = argparse.ArgumentParser()
ap.add_argument('--src', required=True, help='directory of the latest theme pull')
args = ap.parse_args()
SRC = pathlib.Path(args.src)
OUT = pathlib.Path('/home/ly/project/Gumi-Brand-shopify/work-r104')
if not (SRC / 'templates').is_dir():
    sys.exit(f'ABORT: {SRC} is not a theme pull')

# template -> section id -> {key: new value}
# Only the keys listed here are written; a key already holding the target value
# is reported as a no-op rather than silently counted as a change.
PLAN = {
    'index.json': {
        'wave_hero_after':            {'count': 'lg'},   # hero -> logos
        'wave_science_before':        {'count': 'sm'},
        'wave_science_after':         {'count': 'lg'},
        # Colour left alone on purpose: the board bleeds the product art through
        # the arcs here (--edge-top --bleed), which an in-flow wave cannot do.
        # Emptying the top colour would show the page ground, not the lime block.
        'wave_nutrition_after':       {'count': 'lg'},
        'wave_featured_product_after': {'count': 'lg'},
    },
    'page.faq.json':           {'wave_hero_after': {'count': 'sm'}},
    'page.get-in-touch.json':  {'wave_hero_after': {'count': 'sm'}},
    'page.how-gumi-works.json': {
        'wave_hero_after':  {'count': 'lg'},
        'wave_dosed_after': {'count': 'lg'},
        # Board has white -> mint here; live was painting white -> sand.
        'wave_gb_product_MRd8JG_after': {'count': 'sm', 'color_below': '#e7f8d0'},
    },
    'page.our-story.json':     {'wave_hero_after': {'count': 'lg'}},
    'page.privacy-policy.json': {'wave_hero_after': {'count': 'sm'}},
    'page.referral.json':      {'wave_hero_after': {'count': 'sm'}},
    'page.reviews.json': {
        'wave_hero_after':   {'count': 'lg'},
        'wave_expert_after': {'count': 'sm'},
        # wave_gb_product_tj33wK_after is deliberately absent: live has no
        # app-section on this page, so this boundary has no counterpart on the
        # board. Listed in the changelog for the client to rule on.
        'wave_ingredients_after': {'count': 'sm'},
    },
    'page.science.json': {
        # Board is mint -> cream under this hero; live was mint -> white.
        'wave_hero_after':        {'count': 'lg', 'color_below': '#faf9f8'},
        'wave_nutrients_after':   {'count': 'lg'},
        'wave_ingredients_after': {'count': 'lg'},
    },
    'page.shipping.json':      {'wave_hero_after': {'count': 'sm'}},
    'product.json': {
        'wave_product_after': {'count': 'lg'},
        'wave_reviews_after': {'count': 'sm'},
        'wave_vs_after':      {'count': 'sm'},
        'wave_app_slot_after': {'count': 'sm'},
    },
}

(OUT / 'templates').mkdir(parents=True, exist_ok=True)
changed = noop = 0
for name, plan in PLAN.items():
    src = SRC / 'templates' / name
    raw = src.read_text(encoding='utf-8')
    # Shopify ships these with a leading /* ... */ banner that json cannot read.
    head = ''
    m = re.match(r'(\s*/\*.*?\*/\s*)', raw, re.S)
    if m:
        head, raw = m.group(1), raw[len(m.group(1)):]
    d = json.loads(raw)
    for sid, keys in plan.items():
        sec = d['sections'].get(sid)
        if sec is None or sec.get('type') != 'gb-wave':
            sys.exit(f'ABORT {name}: {sid} is not a gb-wave section -- live has moved')
        st = sec.setdefault('settings', {})
        for k, v in keys.items():
            if st.get(k) == v:
                noop += 1
                print(f'  --   {name:<26} {sid:<30} {k} already {v!r}')
            else:
                print(f'  set  {name:<26} {sid:<30} {k}: {st.get(k)!r} -> {v!r}')
                st[k] = v
                changed += 1
    (OUT / 'templates' / name).write_text(head + json.dumps(d, indent=2, ensure_ascii=False) + '\n',
                                          encoding='utf-8')

print(f'\n{changed} setting(s) changed, {noop} already correct, '
      f'{len(PLAN)} template(s) written to {OUT}/templates')
