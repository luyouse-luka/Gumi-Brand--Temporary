#!/usr/bin/env python3
"""Unit-test the replace chain in snippets/gb-lines.liquid.

Re-implements the filter pipeline in Python and drives it with every input shape
the settings can hold. Catches ordering bugs (a later replace eating an earlier
one's output) without a store round-trip; it does NOT prove Liquid's own
newline_to_br / strip_newlines behave as assumed -- that needs a dev theme.
"""
import html as _html, re, sys

def escape(s):                 # Liquid `escape`
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
             .replace('"', '&quot;').replace("'", '&#39;'))
def newline_to_br(s):          # Liquid inserts <br /> and KEEPS the newline
    return s.replace('\n', '<br />\n')
def strip_newlines(s):
    return s.replace('\n', '').replace('\r', '')

def gb_lines(text):
    out = text.strip()
    if '</' in out:
        out = strip_newlines(out).replace('</p><p>', '<br>').replace('<p>', '').replace('</p>', '')
    else:
        out = strip_newlines(newline_to_br(escape(out)))
    out = out.replace('<br />', '<br>')
    for _ in range(3):
        out = out.replace(' <br>', '<br>')
    out = out.replace('//<br>', '@@B@@').replace('^^<br>', '@@W@@')
    out = out.replace('<br>', '<br class="gb-br-narrow">')
    out = out.replace('@@B@@', '<br>').replace('@@W@@', '<br class="gb-br-wide">')
    return out.strip()

N = '<br class="gb-br-narrow">'
W = '<br class="gb-br-wide">'
CASES = [
    ('no break',            'Page title',                    'Page title'),
    ('mobile break',        'Nutrition that fits\nin your pocket',
                            f'Nutrition that fits{N}in your pocket'),
    ('bare break',          "Aussies are obsessed.//\nHere's why.",
                            "Aussies are obsessed.<br>Here&#39;s why."),
    ('wide break',          'One pouch. Once a^^\nday.',      f'One pouch. Once a{W}day.'),
    ('three kinds',         'a\nb//\nc^^\nd',                 f'a{N}b<br>c{W}d'),
    ('trailing spaces',     'Vitamins//  \n& Minerals',       'Vitamins<br>&amp; Minerals'),
    ('space before break',  'foo \nbar',                      f'foo{N}bar'),
    ('crlf',                'foo//\r\nbar',                   'foo<br>bar'),
    # leftover values from before the setting type changed
    ('legacy richtext',     '<p>Made with care.</p>',        'Made with care.'),
    ('legacy two paras',    '<p>Made with care.</p><p>On purpose.</p>',
                            f'Made with care.{N}On purpose.'),
    ('legacy inline tags',  '<p>Real <em>fruit</em>, real veg.</p>',
                            'Real <em>fruit</em>, real veg.'),
    ('legacy inline_richtext', 'Nutrition <strong>that fits</strong>',
                            'Nutrition <strong>that fits</strong>'),
    # author HTML must not survive the plain-text branch
    ('injected tag',        'Hi <img src=x onerror=alert(1)>',
                            'Hi &lt;img src=x onerror=alert(1)&gt;'),
    ('ampersand',           'Vitamins & Minerals',            'Vitamins &amp; Minerals'),
    ('blank',               '',                               ''),
]

ok = red = 0
for name, src, want in CASES:
    got = gb_lines(src)
    if got == want: ok += 1; print(f'  ok   {name}')
    else:
        red += 1
        print(f'  FAIL {name}\n       in   {src!r}\n       want {want!r}\n       got  {got!r}')
print(f'\n{ok} ok / {red} red')

# The static build's real strings, round-tripped: what must an editor type?
print('\n--- what the admin has to contain, per field ---')
FIELDS = [
    ('gb-footer.tagline',          "Made with more care than a\nvitamin gummy probably needs.\nThat's on purpose.", 2),
    ('gb-hero.lead',               'Real fruit, real veg, real vitamins,\nhiding in a gumi bear.', 1),
    ('gb-reviews.title',           "Aussies are obsessed.//\nHere's why.", 1),
    ('gb-stats.title',             '60+ whole foods.//\nNo juicer, no fuss.', 1),
    ('gb-nutrition.title',         'Nutrition that fits\nin your pocket', 1),
]
for fid, src, want_n in FIELDS:
    got = gb_lines(src)
    n = got.count('<br')
    print(f'  {"ok " if n == want_n else "RED"} {fid:24} {n} break(s)  {got[:76]}')
sys.exit(1 if red else 0)
