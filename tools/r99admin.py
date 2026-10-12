#!/usr/bin/env python3
"""Turn the static build's hand-set line breaks into what an editor must type.

Reverse of snippets/gb-lines.liquid: reads every <br>-bearing element out of the
static pages and prints the plain-text form that reproduces it, per page and per
field. Feeds both the schema `default` values and the admin re-entry checklist.
"""
import collections, html, pathlib, re, sys
from html.parser import HTMLParser

VOID = {'br','img','input','meta','link','hr','source','area','base','col','embed',
        'param','track','wbr','path','circle','rect','use','stop','polygon','line','ellipse'}

# host class -> (section, setting) it is rendered from
FIELD = {
    'gb-footer__tagline':      ('gb-footer',    'tagline'),
    'gb-page-hero__title':     ('gb-page-hero', 'title'),
    'gb-hero__lead':           ('gb-hero',      'lead'),
    'gb-usp__label':           ('gb-hero',      'block usp > label'),
    'gb-reviews__title':       ('gb-reviews',   'title'),
    'gb-science__title':       ('gb-science',   'title'),
    'gb-nutrition__title':     ('gb-nutrition', 'title'),
    'gb-highlight-card__text': ('gb-nutrition', 'block card > text'),
    'gb-stats__title':         ('gb-stats',     'title'),
    'gb-stat__label':          ('gb-stats',     'block stat > label'),
    'gb-promo-card__title':    ('gb-promo',     'block card > title'),
    'gb-dosed__title':         ('gb-dosed',     'block row > title'),
    'gb-expert__title':        ('gb-expert',    'title'),
}
# Rendered on the static pages but absent from the live theme, or not a setting.
SKIP = {'gb-ink-halo': 'duplicate of gb-dosed__title, same setting',
        'gb-testimonial__lead': 'module not on live',
        'gb-promo-panel__title': 'module not on live',
        'gb-promo-panel__lead': 'module not on live'}

class Grab(HTMLParser):
    def __init__(s): super().__init__(convert_charrefs=False); s.stack=[]; s.buf={}; s.out=[]
    def _cls(s): return s.stack[-1][1] if s.stack else ''
    def handle_starttag(s, t, a):
        d = dict(a)
        if t == 'br':
            c = d.get('class', '')
            s.buf.setdefault(id(s.stack[-1]) if s.stack else 0, [])
            mark = '\n' if 'gb-br-narrow' in c else ('^^\n' if 'gb-br-wide' in c else '//\n')
            s._add(mark)
        elif t in VOID:
            pass
        else:
            s.stack.append([t, d.get('class',''), []])
    def handle_endtag(s, t):
        for i in range(len(s.stack)-1, -1, -1):
            if s.stack[i][0] == t:
                node = s.stack[i]
                if any(x in ('\n','^^\n','//\n') for x in node[2]):
                    gb = [c for c in node[1].split() if c.startswith('gb-')]
                    s.out.append((gb[0] if gb else f'<{t}>', ''.join(node[2])))
                del s.stack[i:]
                return
    def _add(s, txt):
        if s.stack: s.stack[-1][2].append(txt)
    def handle_data(s, d): s._add(d)
    def handle_entityref(s, n): s._add(html.unescape('&%s;' % n))
    def handle_charref(s, n): s._add(html.unescape('&#%s;' % n))

rows = collections.defaultdict(dict)     # (section,setting) -> {text: [pages]}
skipped = collections.Counter()
for f in sorted(pathlib.Path('/home/ly/project/Gumi-Brand').glob('*.html')):
    if f.stem == 'font-check': continue
    g = Grab(); g.feed(f.read_text(encoding='utf-8'))
    for cls, txt in g.out:
        # keep only the innermost host: a wrapper repeats its child's text
        txt = re.sub(r'[ \t]+', ' ', txt).strip()
        txt = re.sub(r' *\n *', '\n', txt)
        if cls in SKIP: skipped[cls] += 1; continue
        if cls not in FIELD: skipped[cls] += 1; continue
        rows[FIELD[cls]].setdefault(txt, []).append(f.stem)

print('=== admin re-entry checklist ===\n')
n = 0
for (sec, setting), variants in sorted(rows.items()):
    for txt, pages in sorted(variants.items(), key=lambda kv: kv[1]):
        n += 1
        breaks = txt.count('\n')
        print(f'{n:2}. {sec} > {setting}')
        print(f'    pages : {", ".join(sorted(set(pages)))}')
        print(f'    breaks: {breaks}   (schema default form below)')
        for line in txt.split('\n'):
            print(f'      | {line}')
        print(f'    json  : "{txt.replace(chr(10), chr(92)+"n")}"')
        print()
print(f'{n} field values to re-enter\n')
if skipped:
    print('--- not a setting / not on live ---')
    for k, v in skipped.most_common():
        print(f'  {k:26} x{v}  {SKIP.get(k, "hard-coded in the build")}')
