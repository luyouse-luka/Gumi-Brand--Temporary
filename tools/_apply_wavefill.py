#!/usr/bin/env python3
"""Fill in every wave the live theme is still missing, and fix the two that are wrong.

  python3 tools/_apply_wavefill.py --src <latest pull>

Read live -> change only the named keys -> write back (the r104/r105 rule).
Three jobs, all of them template data only -- no liquid, no css, no js:

1  CTA wave on the 9 templates that have no board (404, article, blog,
   collection, list-collections, page.contact, page, password, search).
   r105 left these alone on purpose; the client has now called for them.
   Top colour empty, because what sits above differs per template.

2  Four boundaries inside designed pages where the background changes with no
   wave to carry it.

3  Two that are wrong: how-gumi-works' reviews is sand where the board says
   cream (so the wave above it reads white->cream against a sand block -- fix
   the block, not the wave, per SCALLOP.md 6), and reviews' product->ingredients
   wave paints a sand band between two white blocks. The board has no wave there
   at all; it was kept back when the page had no app-section above it, and the
   other team has since added one.
"""
import argparse, json, pathlib, re, sys

LIME, MINT, WHITE, CREAM = '#b5ed61', '#e7f8d0', '#ffffff', '#faf9f8'

ap = argparse.ArgumentParser()
ap.add_argument('--src', required=True, help='directory of the latest theme pull')
ap.add_argument('--out', default='/home/ly/project/Gumi-Brand-shopify/work-wavefill')
args = ap.parse_args()
SRC, OUT = pathlib.Path(args.src), pathlib.Path(args.out)
if not (SRC / 'templates').is_dir():
    sys.exit(f'ABORT: {SRC} is not a theme pull')

# 1 -- CTA wave, above the gb-footer-cta, top colour left empty
CTA = ['404.json', 'article.json', 'blog.json', 'collection.json',
       'list-collections.json', 'page.contact.json', 'page.json',
       'password.json', 'search.json']

# 2 -- (template, new id, section it goes above, count, above, below)
INSERT = [
    ('index.json', 'wave_logos_after', 'stats', 'sm', WHITE, CREAM),
    ('page.how-gumi-works.json', 'wave_gb_reviews_Ne3FPP_after',
     'gb_product_MRd8JG', 'lg', CREAM, WHITE),
    ('page.our-story.json', 'wave_cta_after', 'reviews', 'lg', WHITE, CREAM),
    ('page.reviews.json', 'wave_customer_reviews_after',
     'gb_product_tj33wK', 'lg', CREAM, WHITE),
]

# 3a -- settings on non-wave sections
EDIT = {'page.how-gumi-works.json': {'gb_reviews_Ne3FPP': {'background': 'cream'}}}
# 3b -- waves to remove entirely
DROP = {'page.reviews.json': ['wave_gb_product_tj33wK_after']}


def split_head(raw):
    m = re.match(r'(\s*/\*.*?\*/\s*)', raw, re.S)
    return (m.group(1), raw[len(m.group(1)):]) if m else ('', raw)


def wave(count, above, below):
    return {'type': 'gb-wave',
            'settings': {'count': count, 'direction': 'up', 'overlap': False,
                         'color_above': above, 'color_below': below}}


names = sorted(set(CTA) | {t for t, *_ in INSERT} | set(EDIT) | set(DROP))
(OUT / 'templates').mkdir(parents=True, exist_ok=True)
added = edited = dropped = 0

for name in names:
    src = SRC / 'templates' / name
    if not src.exists():
        sys.exit(f'ABORT: {name} is not in the pull')
    raw = src.read_text(encoding='utf-8')
    tail = '\n' if raw.endswith('\n') else ''   # keep the file's own ending; Shopify writes none
    head, body = split_head(raw)
    d = json.loads(body)
    secs, order = d['sections'], d['order']

    # 3b: drop
    for sid in DROP.get(name, []):
        sec = secs.get(sid)
        if sec is None or sec.get('type') != 'gb-wave':
            sys.exit(f'ABORT {name}: {sid} is not a gb-wave -- live has moved')
        secs.pop(sid); order.remove(sid)
        print(f'  drop {name:<26} {sid}')
        dropped += 1

    # 3a: edit settings on a normal section
    for sid, keys in EDIT.get(name, {}).items():
        sec = secs.get(sid)
        if sec is None:
            sys.exit(f'ABORT {name}: {sid} is gone -- live has moved')
        st = sec.setdefault('settings', {})
        for k, v in keys.items():
            print(f'  set  {name:<26} {sid:<24} {k}: {st.get(k)!r} -> {v!r}')
            st[k] = v
            edited += 1

    # 1: CTA wave
    if name in CTA:
        cta = next((s for s in order if secs.get(s, {}).get('type') == 'gb-footer-cta'), None)
        if cta is None:
            sys.exit(f'ABORT {name}: no gb-footer-cta to sit above')
        i = order.index(cta)
        if i and secs.get(order[i - 1], {}).get('type') == 'gb-wave':
            sys.exit(f'ABORT {name}: a wave already sits above the CTA -- re-read live')
        sid = 'wave_footer_cta_before'
        if sid in secs:
            sys.exit(f'ABORT {name}: {sid} already taken')
        secs[sid] = wave('sm', '', LIME)
        order.insert(i, sid)
        print(f'  add  {name:<26} {sid} above {cta}   (transparent) -> {LIME}')
        added += 1

    # 2: interior boundaries
    for t, sid, below_id, count, above, below in INSERT:
        if t != name:
            continue
        if below_id not in order:
            sys.exit(f'ABORT {name}: {below_id} is gone -- live has moved')
        i = order.index(below_id)
        if i and secs.get(order[i - 1], {}).get('type') == 'gb-wave':
            sys.exit(f'ABORT {name}: a wave already sits above {below_id} -- re-read live')
        if sid in secs:
            sys.exit(f'ABORT {name}: {sid} already taken')
        secs[sid] = wave(count, above, below)
        order.insert(i, sid)
        print(f'  add  {name:<26} {sid} above {below_id}   {count}  {above} -> {below}')
        added += 1

    (OUT / 'templates' / name).write_text(
        head + json.dumps(d, indent=2, ensure_ascii=False) + tail, encoding='utf-8')

print(f'\n{added} added, {edited} setting(s) changed, {dropped} dropped, '
      f'{len(names)} template(s) -> {OUT}/templates')
