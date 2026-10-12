#!/usr/bin/env python3
"""r105: the bleed boundary, and the CTA wave the other team half-migrated.

  python3 tools/_apply_r105_tpl.py --src <latest pull>

Read live -> change only the named keys -> write back, as r104 did. Three jobs:

1  index nutrition -> product goes back to the board's --bleed: the wave laps
   over the lime block (overlap) with an empty top colour, so the pack art shows
   through the gaps between the arcs.
2  The other team lifted the CTA wave out of gb-footer-cta.liquid into a Gumi
   Wave, but only on index and product -- and product's colours were eyeballed
   (#E7F7DA / #BAE97B against the board's #e7f8d0 / #b5ed61).
3  The other 9 designed pages lost that wave entirely when the liquid stopped
   emitting it. They get one back, with the pair the board gives them:
     to-lime       empty top -> lime   (faq, get-in-touch, our-story,
                                        privacy-policy, referral, shipping)
     mint-to-lime  mint -> lime        (how-gumi-works, reviews, science)

⚠ Untouched on purpose: the 11 templates with no board (404, article, blog,
collection, list-collections, page.contact, page, password, search). They lost
the wave too -- listed for the client to rule on, not restored blind.
"""
import argparse, json, pathlib, re, sys

LIME, MINT = '#b5ed61', '#e7f8d0'
ap = argparse.ArgumentParser()
ap.add_argument('--src', required=True, help='directory of the latest theme pull')
args = ap.parse_args()
SRC = pathlib.Path(args.src)
OUT = pathlib.Path('/home/ly/project/Gumi-Brand-shopify/work-r105')
if not (SRC / 'templates').is_dir():
    sys.exit(f'ABORT: {SRC} is not a theme pull')

# --- 1 + 2: settings to change on waves that already exist -------------------
EDIT = {
    'index.json': {
        # the board's --edge-top --lg --lime-to-white --bleed
        'wave_nutrition_after': {'overlap': True, 'color_above': ''},
    },
    'product.json': {
        # theirs, eyeballed; the board's pair is mint -> lime
        'gb_wave_m9NYRN': {'color_above': MINT, 'color_below': LIME},
    },
}

# --- 3: pages that need the CTA wave put back --------------------------------
# value is the top colour; '' means the board's --to-lime, whose top is
# transparent because the block above it differs per page.
ADD = {
    'page.faq.json': '', 'page.get-in-touch.json': '', 'page.our-story.json': '',
    'page.privacy-policy.json': '', 'page.referral.json': '', 'page.shipping.json': '',
    'page.how-gumi-works.json': MINT, 'page.reviews.json': MINT, 'page.science.json': MINT,
}
NEW_ID = 'wave_footer_cta_before'

(OUT / 'templates').mkdir(parents=True, exist_ok=True)
edited = added = 0

for name in sorted(set(EDIT) | set(ADD)):
    src = SRC / 'templates' / name
    raw = src.read_text(encoding='utf-8')
    head = ''
    m = re.match(r'(\s*/\*.*?\*/\s*)', raw, re.S)
    if m:
        head, raw = m.group(1), raw[len(m.group(1)):]
    d = json.loads(raw)

    for sid, keys in EDIT.get(name, {}).items():
        sec = d['sections'].get(sid)
        if sec is None or sec.get('type') != 'gb-wave':
            sys.exit(f'ABORT {name}: {sid} is not a gb-wave -- live has moved')
        st = sec.setdefault('settings', {})
        for k, v in keys.items():
            print(f'  set  {name:<26} {sid:<24} {k}: {st.get(k)!r} -> {v!r}')
            st[k] = v
            edited += 1

    if name in ADD:
        order = d['order']
        cta = next((s for s in order
                    if d['sections'].get(s, {}).get('type') == 'gb-footer-cta'), None)
        if cta is None:
            sys.exit(f'ABORT {name}: no gb-footer-cta to sit above')
        i = order.index(cta)
        before = order[i - 1] if i else None
        if before and d['sections'].get(before, {}).get('type') == 'gb-wave':
            sys.exit(f'ABORT {name}: {before} is already a wave above the CTA -- '
                     'live has moved, re-read before writing')
        d['sections'][NEW_ID] = {
            'type': 'gb-wave',
            'settings': {'count': 'sm', 'direction': 'up',
                         'color_above': ADD[name], 'color_below': LIME},
        }
        order.insert(i, NEW_ID)
        print(f'  add  {name:<26} {NEW_ID} above {cta}   '
              f"top={ADD[name] or '(transparent)'} bottom={LIME}")
        added += 1

    (OUT / 'templates' / name).write_text(
        head + json.dumps(d, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

print(f'\n{edited} setting(s) changed, {added} wave(s) added, '
      f'{len(set(EDIT) | set(ADD))} template(s) written to {OUT}/templates')
