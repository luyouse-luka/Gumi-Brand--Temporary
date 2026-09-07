#!/usr/bin/env python3
"""Where does the theme's own CSS out-rank ours on live?

    python3 tools/losers.py --password 1234                 # all pages
    python3 tools/losers.py --password 1234 --page pdp

Only live can answer this: the static site loads customstyle.css alone, so no
rule of Horizon's exists to beat. The cascade is read out of Chrome via CDP
(CSS.getMatchedStylesForNode), not re-implemented here -- specificity of
:not(), :is() and layers is exactly what this probe must not get wrong.

A hit means: customstyle.css declares P on this element AND something else wins
it. That is the CSS-fixable defect class -- no structure, no liquid, just
specificity. Declarations we deliberately leave to the theme show up too, so
every hit still needs reading.
"""
import argparse, collections, json, pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
SITE = 'https://gumi.com.au'
PAGES = {'index': '/', 'pdp': '/products/superfood-greens-gummies',
         'science': '/pages/science', 'reviews': '/pages/reviews',
         'how-gumi-works': '/pages/how-gumi-works', 'our-story': '/pages/our-story',
         'faq': '/pages/faq', 'get-in-touch': '/pages/get-in-touch',
         'referral': '/pages/referral', 'privacy-policy': '/pages/privacy-policy',
         'shipping': '/pages/shipping'}

OURS = 'customstyle'
# Inherited/animated properties churn per element and say nothing about the
# cascade fight we are looking for.
IGNORE = {'-webkit-locale', 'transition', 'animation', 'content'}

# Chrome hands back longhandProperties for every shorthand it can expand -- but a
# shorthand whose value contains var() is pending-substitution and expands to
# nothing, so `border-color: var(--x)` would never meet our `border: 1px solid`.
# These are the shorthands that actually appear in Horizon with a var() value.
_S = ['top', 'right', 'bottom', 'left']
SHORTHAND = {
    'border-color': ['border-%s-color' % s for s in _S],
    'border-width': ['border-%s-width' % s for s in _S],
    'border-style': ['border-%s-style' % s for s in _S],
    'border': ['border-%s-%s' % (s, k) for s in _S for k in ('width', 'style', 'color')],
    'padding': ['padding-' + s for s in _S],
    'margin': ['margin-' + s for s in _S],
    'inset': _S,
    'border-radius': ['border-top-left-radius', 'border-top-right-radius',
                      'border-bottom-right-radius', 'border-bottom-left-radius'],
    'gap': ['row-gap', 'column-gap'],
    'overflow': ['overflow-x', 'overflow-y'],
    'flex': ['flex-grow', 'flex-shrink', 'flex-basis'],
    'background': ['background-color', 'background-image', 'background-position',
                   'background-size', 'background-repeat'],
}


# Logical properties resolve to the same computed longhand as their physical
# twin (horizontal-tb / ltr here), so `summary { padding-block }` and our
# `padding-top` are the same fight. Comparing the NAMES makes every one of them
# look like an untouched property and the leak list fills with false alarms.
LOGICAL = {}
for _l, _p in (('block-start', 'top'), ('block-end', 'bottom'),
               ('inline-start', 'left'), ('inline-end', 'right')):
    for _b in ('margin', 'padding'):
        LOGICAL['%s-%s' % (_b, _l)] = ['%s-%s' % (_b, _p)]
    LOGICAL['border-%s-width' % _l] = ['border-%s-width' % _p]
    LOGICAL['border-%s-style' % _l] = ['border-%s-style' % _p]
    LOGICAL['border-%s-color' % _l] = ['border-%s-color' % _p]
    LOGICAL['inset-' + _l] = [_p]
for _b in ('margin', 'padding'):
    LOGICAL[_b + '-block'] = [_b + '-top', _b + '-bottom']
    LOGICAL[_b + '-inline'] = [_b + '-left', _b + '-right']
LOGICAL.update({'block-size': ['height'], 'inline-size': ['width'],
                'min-block-size': ['min-height'], 'min-inline-size': ['min-width'],
                'max-block-size': ['max-height'], 'max-inline-size': ['max-width'],
                'inset-block': ['top', 'bottom'], 'inset-inline': ['left', 'right']})


def longhands(p):
    lp = p.get('longhandProperties')
    if lp:
        out = []
        for x in lp:
            for n in LOGICAL.get(x['name'], [x['name']]):
                out.append((n, x['value']))
        return out
    names = SHORTHAND.get(p['name']) or LOGICAL.get(p['name'])
    if names:
        return [(n, p['value']) for n in names]
    return [(p['name'], p['value'])]


LEAKS = False
# Reveal timing and vendor transition plumbing: real declarations, but they are
# not what "does the theme restyle our modules" is asking.
LEAK_SKIP = {'animation-delay', 'transition-property', 'transition-duration',
             'transition-timing-function', 'transition-delay', 'transition-behavior',
             'grid-column-end'}
_CLS = {}


def same(a, b):
    z = lambda v: '0' if v in ('0', '0px', '0%') else v.replace(' ', '')
    return z(a) == z(b)


def gbclass(cdp, nid):
    if nid not in _CLS:
        try:
            attrs = cdp.send('DOM.getAttributes', {'nodeId': nid})['attributes']
            d = dict(zip(attrs[0::2], attrs[1::2]))
            gb = [c for c in (d.get('class') or '').split() if c.startswith('gb-')]
            _CLS[nid] = '.' + '.'.join(gb[:2]) if gb else '?'
        except Exception:
            _CLS[nid] = '?'
    return _CLS[nid]


def scan(page, tag, out):
    _CLS.clear()          # node ids are per document; a stale cache renames elements
    cdp = page.context.new_cdp_session(page)
    sheets = {}
    cdp.on('CSS.styleSheetAdded', lambda e: sheets.__setitem__(
        e['header']['styleSheetId'], e['header'].get('sourceURL') or 'inline'))
    cdp.send('DOM.enable'); cdp.send('CSS.enable')
    doc = cdp.send('DOM.getDocument', {'depth': -1, 'pierce': False})
    root = doc['root']['nodeId']
    ids = cdp.send('DOM.querySelectorAll', {'nodeId': root, 'selector': '[class*="gb-"]'})['nodeIds']

    for nid in ids:
        try:
            m = cdp.send('CSS.getMatchedStylesForNode', {'nodeId': nid})
        except Exception:
            continue
        # cascade order: matchedCSSRules is ordered lowest -> highest precedence
        winner = {}          # prop -> (sheet, selector, value, important)
        ours = {}            # prop -> (selector, value)
        for entry in m.get('matchedCSSRules', []):
            rule = entry['rule']
            href = sheets.get(rule.get('styleSheetId'), '')
            name = href.split('/')[-1].split('?')[0] or ('ua' if rule.get('origin') == 'user-agent' else 'inline')
            sel = ', '.join(s['text'] for s in rule['selectorList']['selectors'])
            for p in rule['style'].get('cssProperties', []):
                if p.get('disabled') or not p.get('parsedOk', True): continue
                # Only authored declarations carry `text`; the rest of the list is
                # the longhand expansion Chrome already did for them. Walking the
                # authored ones and expanding via longhandProperties is what makes
                # `border: 1px solid #ccc` comparable with `border-color: var(...)`
                # -- compare the shorthand NAMES and the two never meet.
                if 'text' not in p: continue
                imp = bool(p.get('important'))
                for prop, val in longhands(p):
                    if prop in IGNORE or prop.startswith('--') or val == '': continue
                    cur = winner.get(prop)
                    if cur is None or imp or not cur[3]:
                        winner[prop] = (name, sel, val, imp)
                    if OURS in name:
                        ours[prop] = (sel, val)
        inline = m.get('inlineStyle')
        if inline:
            for p in inline.get('cssProperties', []):
                if 'text' in p and not p.get('disabled'):
                    winner[p['name']] = ('inline-attr', '', p['value'], bool(p.get('important')))

        for prop, (sheet, sel, val, imp) in winner.items():
            if OURS in sheet or sheet in ('ua', 'inline-attr') and not LEAKS: pass
            if OURS in sheet: continue
            if prop in ours:
                oursel, ourval = ours[prop]
                if same(ourval, val): continue
                out[(oursel, prop, ourval, val, sel, sheet)].add(tag)
            elif LEAKS and sheet not in ('ua', 'inline-attr') and prop not in LEAK_SKIP:
                # theme CSS reaching a gb-* element we never styled for that property
                out[(gbclass(cdp, nid), prop, '-', val, sel, sheet)].add(tag)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--password', required=True)
    ap.add_argument('--page', action='append')
    ap.add_argument('--width', type=int, default=1440)
    ap.add_argument('--leaks', action='store_true',
                    help='also report theme declarations on gb-* elements we never style')
    a = ap.parse_args()
    global LEAKS
    LEAKS = a.leaks
    pages = a.page or list(PAGES)
    out = collections.defaultdict(set)

    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME)
        ctx = b.new_context(viewport={'width': a.width, 'height': 1000})
        r = ctx.request.post(SITE + '/password', form={
            'form_type': 'storefront_password', 'utf8': '✓', 'password': a.password})
        if r.status in (429, 503):
            raise SystemExit('Cloudflare (HTTP %d) -- back off' % r.status)
        for name in pages:
            pg = ctx.new_page()
            pg.goto(SITE + PAGES[name], wait_until='networkidle', timeout=45000)
            pg.wait_for_timeout(500)
            scan(pg, name, out)
            pg.close()
            print('scanned ' + name)
        b.close()

    print('\n%d losing declarations\n' % len(out))
    rows = sorted(out.items(), key=lambda kv: (-len(kv[1]), kv[0][0], kv[0][1]))
    for (oursel, prop, ourval, val, sel, sheet), tags in rows:
        print('  %-34s %-22s ours=%-20s -> %-20s' % (oursel[:34], prop, ourval[:20], val[:20]))
        print('        beaten by [%s] %s   [%s]' % (sheet, sel[:64], ', '.join(sorted(tags))))


if __name__ == '__main__':
    main()
