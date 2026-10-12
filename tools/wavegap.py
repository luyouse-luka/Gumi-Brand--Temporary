#!/usr/bin/env python3
"""Live wave audit: does every section boundary carry the right wave, in the right colours?

  python3 tools/wavegap.py <live-theme-dir>

Resolves each section's real background from the variant its settings produce
(live sections are mostly bare base classes -- their default background is NOT
the variant the static site uses), then checks the gb-wave sitting on each
boundary against the two neighbours. Templates only; no browser, no API.
"""
import json, re, sys, pathlib

C = {'lime': '#b5ed61', 'mint': '#e7f8d0', 'white': '#ffffff',
     'cream': '#faf9f8', 'sand': '#f5f1e9', 'green900': '#004128'}
NAME = {v: k for k, v in C.items()}
NAME[''] = 'transparent'

# base background of each gb-* section, read off customstyle.scss
BASE = {
    'gb-hero': 'mint', 'gb-page-hero': 'mint', 'gb-logo-scroll': 'white',
    'gb-stats': 'cream', 'gb-science': 'sand', 'gb-nutrition': 'lime',
    'gb-product': 'white', 'gb-reviews': 'mint', 'gb-promo': 'sand',
    'gb-vs': 'white', 'gb-app-section': 'cream', 'gb-faq': 'mint',
    'gb-faq-image': 'mint', 'gb-expert': 'white', 'gb-ingredients': 'white',
    'gb-dosed': 'white', 'gb-story': 'white', 'gb-cta-band': 'white',
    'gb-compare': 'white', 'gb-form-section': 'white', 'gb-rich-page': 'white',
    'gb-footer-cta': 'lime',
}
# variants that change the background, keyed by (type, resolved variant)
VAR = {('gb-reviews', 'cream'): 'cream', ('gb-reviews', 'sand'): 'sand',
       ('gb-faq', 'plain'): 'white', ('gb-science', 'cream'): 'cream'}


def variant(t, st):
    """The background-changing modifier this section's settings resolve to."""
    if t == 'gb-reviews':
        b = st.get('background')
        return b if b and b != 'default' else None
    if t == 'gb-faq':
        return 'plain' if st.get('plain') else None
    if t == 'gb-science':
        return 'cream' if st.get('background') == 'cream' else None
    return None


def bg(t, st):
    v = variant(t, st)
    return VAR.get((t, v), BASE.get(t))


def load(p):
    return json.loads(re.sub(r'/\*.*?\*/', '', p.read_text(), flags=re.S))


def cname(h):
    return NAME.get((h or '').lower().strip(), h or 'transparent')


def main(root):
    root = pathlib.Path(root)
    ok = red = 0
    for f in sorted(root.glob('templates/*.json')):
        d = load(f)
        secs, order = d.get('sections', {}), d.get('order', [])
        items = [(k, secs.get(k, {}).get('type'), secs.get(k, {}).get('settings') or {})
                 for k in order]
        if not any(t and t.startswith('gb-') and t != 'gb-wave' for _, t, _ in items):
            continue
        print(f'\n══ {f.name} ══')
        # walk boundaries between consecutive non-wave sections
        i = 0
        while i < len(items):
            k, t, st = items[i]
            if t == 'gb-wave':
                i += 1
                continue
            b = bg(t, st) or '?'
            print(f'  {t:<18} bg={b:<11} [{k}]')
            # find the next real section, collecting waves in between
            j, waves = i + 1, []
            while j < len(items) and items[j][1] == 'gb-wave':
                waves.append(items[j]); j += 1
            if j >= len(items):
                break
            nt, nst = items[j][1], items[j][2]
            above, below = bg(t, st), bg(nt, nst)
            if above is None or below is None:   # non-gb theme section, no truth to check
                i = j; continue
            if not waves:
                same = above == below
                mark = 'ok ' if same else 'RED'
                if same: ok += 1
                else: red += 1
                print(f'   ~~~ (none)                            {mark}'
                      f'{"" if same else f"  <- colour changes {above} -> {below}, needs a wave"}')
            for wk, _, ws in waves:
                wa, wb = cname(ws.get('color_above')), cname(ws.get('color_below'))
                a_ok = wa == above or wa == 'transparent'
                b_ok = wb == below
                good = a_ok and b_ok
                if good: ok += 1
                else: red += 1
                note = ''
                if not good:
                    want = f'{above}->{below}'
                    note = f'  <- want {want}'
                print(f'   ~~~ {ws.get("count","?"):<3} {ws.get("direction","?"):<4} '
                      f'{wa}->{wb:<12} {"ok " if good else "RED"}{note}   [{wk}]')
            i = j
    print(f'\n──────── {ok} ok / {red} red ────────')
    return red


if __name__ == '__main__':
    sys.exit(0 if main(sys.argv[1] if len(sys.argv) > 1 else '.') == 0 else 1)
