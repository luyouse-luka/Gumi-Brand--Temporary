#!/usr/bin/env python3
"""r102: move every module's trailing scallop to a standalone Gumi Wave section.

Reads the theme's templates, inserts a gb-wave section at each boundary a wave
currently occupies, and switches the module's own scallop setting off.

The boundary list is the LIVE measurement from tools/wavemap.py, not the liquid:
several sections hard-code a modifier their setting cannot express, and index's
--bleed wave sits on a different side than the static build's.

Arc count follows the drawn size -- the design's small pitch is 4.77 arcs across
1440 and the large one 2.74, so small -> 5 and large -> 3.
"""
import json, pathlib, re, sys

SRC = pathlib.Path('/home/ly/project/Gumi-Brand-shopify/baseline-r100')
OUT = pathlib.Path('/home/ly/project/Gumi-Brand-shopify/work-r102')

# host section key, where to put the wave, arcs, colour pair, direction, setting to clear
M = {
 'templates/index.json': [
   ('hero',             'after',  3, 'to-white',      'down', ('scallop_variant', 'none')),
   ('science',          'before', 5, 'cream-to-sand', 'up',   ('leading_scallop', 'none')),
   ('science',          'after',  3, 'sand-to-lime',  'up',   ('trailing_scallop', 'none')),
   ('nutrition',        'after',  3, 'lime-to-white', 'up',   ('scallop_variant', 'none')),
   ('featured_product', 'after',  3, 'white-to-mint', 'up',   ('scallop_variant', 'none')),
 ],
 'templates/product.json': [
   ('product',  'after', 3, 'white-to-sand', 'up', ('scallop_variant', 'none')),
   ('reviews',  'after', 5, 'sand-to-white', 'up', ('scallop_variant', 'none')),
   ('vs',       'after', 5, 'to-cream',      'up', ('scallop_variant', 'none')),
   ('app_slot', 'after', 3, 'cream-to-mint', 'up', ('scallop_variant', 'none')),
 ],
 'templates/page.science.json': [
   ('hero',        'after', 5, 'to-white',       'down', ('show_scallop', False)),
   ('nutrients',   'after', 3, 'cream-to-white', 'up',   ('trailing_scallop', 'none')),
   ('ingredients', 'after', 3, 'white-to-mint',  'up',   ('trailing_scallop', 'none')),
 ],
 'templates/page.reviews.json': [
   ('hero',              'after', 5, 'to-white',       'down', ('show_scallop', False)),
   ('expert',            'after', 5, 'white-to-cream', 'up',   ('show_scallop', False)),
   ('gb_product_tj33wK', 'after', 3, 'white-to-sand',  'up',   ('scallop_variant', 'none')),
   ('ingredients',       'after', 3, 'white-to-mint',  'up',   ('trailing_scallop', 'none')),
 ],
 'templates/page.how-gumi-works.json': [
   ('hero',              'after', 5, 'to-white',       'down', ('show_scallop', False)),
   ('dosed',             'after', 3, 'white-to-cream', 'up',   ('show_scallop', False)),
   ('gb_product_MRd8JG', 'after', 3, 'white-to-sand',  'up',   ('scallop_variant', 'none')),
 ],
 'templates/page.our-story.json':      [('hero', 'after', 5, 'to-white', 'down', ('show_scallop', False))],
 'templates/page.faq.json':            [('hero', 'after', 5, 'to-white', 'down', ('show_scallop', False))],
 'templates/page.get-in-touch.json':   [('hero', 'after', 5, 'to-white', 'down', ('show_scallop', False))],
 'templates/page.referral.json':       [('hero', 'after', 5, 'to-white', 'down', ('show_scallop', False))],
 'templates/page.privacy-policy.json': [('hero', 'after', 5, 'to-white', 'down', ('show_scallop', False))],
 'templates/page.shipping.json':       [('hero', 'after', 5, 'to-white', 'down', ('show_scallop', False))],
}

OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'templates').mkdir(exist_ok=True)
total = 0
for rel, waves in M.items():
    src = SRC / rel
    raw = src.read_text(encoding='utf-8')
    # Shopify writes /* … */ headers into these files; keep them byte-for-byte.
    head = ''
    m = re.match(r'(\s*/\*.*?\*/\s*)', raw, re.S)
    if m:
        head = m.group(1); raw = raw[len(head):]
    d = json.loads(raw)
    order, secs = d['order'], d['sections']

    for host, where, arcs, pair, direction, (setting, off) in waves:
        if host not in secs:
            sys.exit(f'ABORT {rel}: no section "{host}"')
        if setting not in (secs[host].get('settings') or {}):
            sys.exit(f'ABORT {rel}/{host}: no setting "{setting}"')
        key = f'wave_{host}_{where}'
        if key in secs:
            sys.exit(f'ABORT {rel}: "{key}" already exists')
        secs[key] = {'type': 'gb-wave',
                     'settings': {'count': str(arcs), 'direction': direction, 'pair': pair}}
        i = order.index(host)
        order.insert(i if where == 'before' else i + 1, key)
        secs[host]['settings'][setting] = off
        total += 1

    dst = OUT / rel
    # 2-space indent and a trailing newline is what the Online Store Editor writes.
    dst.write_text(head + json.dumps(d, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(f'  {rel:38} +{len(waves)} wave(s)')

print(f'\n{total} waves migrated across {len(M)} templates')
