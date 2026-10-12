#!/usr/bin/env python3
"""Render snippets/gb-lines.liquid through a real Liquid engine.

  pip3 install python-liquid && python3 tools/r99liquid.py

tools/r99lines.py re-implements the filter chain in Python; this one feeds the
actual snippet source to an engine, so it also checks the Liquid semantics the
re-implementation assumes -- chiefly whether newline_to_br keeps the newline it
replaced and what strip_newlines does to \\r. It is python-liquid, not Shopify's
Ruby implementation, so it cannot settle Shopify-only behaviour; that still
needs a store round-trip.
"""
import pathlib, sys
from liquid import Environment

SNIPPET = pathlib.Path('/home/ly/project/Gumi-Brand-shopify/work-r99/snippets/gb-lines.liquid')
env = Environment()
tpl = env.from_string(SNIPPET.read_text(encoding='utf-8'))

N = '<br class="gb-br-narrow">'
W = '<br class="gb-br-wide">'
CASES = [
    ('no break',              'Page title',                       'Page title'),
    ('mobile break',          'Nutrition that fits\nin your pocket', f'Nutrition that fits{N}in your pocket'),
    ('bare break',            "Aussies are obsessed.//\nHere's why.", "Aussies are obsessed.<br>Here&#39;s why."),
    ('wide break',            'One pouch. Once a^^\nday.',          f'One pouch. Once a{W}day.'),
    ('three kinds',           'a\nb//\nc^^\nd',                     f'a{N}b<br>c{W}d'),
    ('trailing space + //',   'Vitamins//  \n& Minerals',           'Vitamins<br>&amp; Minerals'),
    ('space before break',    'foo \nbar',                          f'foo{N}bar'),
    ('crlf',                  'foo//\r\nbar',                       'foo<br>bar'),
    ('two breaks',            "Made with more care than a\nvitamin gummy probably needs.\nThat's on purpose.",
                              f'Made with more care than a{N}vitamin gummy probably needs.{N}That&#39;s on purpose.'),
    ('legacy richtext',       '<p>Made with care.</p>',             'Made with care.'),
    ('legacy two paras',      '<p>Made with care.</p><p>On purpose.</p>', f'Made with care.{N}On purpose.'),
    ('legacy inline tags',    '<p>Real <em>fruit</em>, real veg.</p>', 'Real <em>fruit</em>, real veg.'),
    ('legacy inline_richtext','Nutrition <strong>that fits</strong>', 'Nutrition <strong>that fits</strong>'),
    ('injected tag',          'Hi <img src=x onerror=alert(1)>',    'Hi &lt;img src=x onerror=alert(1)&gt;'),
    ('ampersand',             'Vitamins & Minerals',                'Vitamins &amp; Minerals'),
    ('blank',                 '',                                   ''),
]
def norm(s):
    # python-liquid escapes the apostrophe as &#x27;, Shopify as &#39;; same character.
    return s.replace('&#x27;', '&#39;')

ok = red = 0
for name, src, want in CASES:
    got = norm(tpl.render(text=src))
    if got == want: ok += 1; print(f'  ok   {name}')
    else:
        red += 1
        print(f'  FAIL {name}\n       in   {src!r}\n       want {want!r}\n       got  {got!r}')

print('\n--- Liquid primitives this snippet leans on ---')
for expr, label in [("{{ t | newline_to_br }}", 'newline_to_br keeps the newline'),
                    ("{{ t | strip_newlines }}", 'strip_newlines drops \\r too'),
                    ("{{ t | escape }}", 'escape leaves // and ^^ alone')]:
    probe = 'a//\r\nb^^'
    print(f'  {label:38} {env.from_string(expr).render(t=probe)!r}')
print(f'\n{ok} ok / {red} red')
sys.exit(1 if red else 0)
