#!/usr/bin/env python3
"""Render the r104 sections through a real Liquid engine.

  pip3 install python-liquid && python3 tools/r104liquid.py

gb-wave gained two board-size options alongside the arc counts, and the two
routes emit different markup: a board size goes on as a CLASS (the stylesheet
holds the pitch), an arc count as the inline --wave-n the stylesheet divides by.
Getting that backwards renders a wave of the wrong height with no error, so the
split is asserted both ways round.

gb-footer is checked for shape only -- its one change is the tagline render, and
that snippet already has its own judge in r99liquid.py.
"""
import json, pathlib, re, sys
from liquid import Environment

S = pathlib.Path('/home/ly/project/Gumi-Brand-shopify/work-r104')
WAVE = S / 'sections/gb-wave.liquid'
FOOTER = S / 'sections/gb-footer.liquid'

env = Environment()
ok = red = 0


def grade(cond, label, detail=''):
    global ok, red
    if cond:
        ok += 1
        print(f'  ok   {label}')
    else:
        red += 1
        print(f'  RED  {label}   {detail}')


def split(path):
    """Body and parsed schema. {% schema %} is a Shopify tag the engine has no
    parser for, so it is cut out rather than rendered."""
    src = path.read_text(encoding='utf-8')
    m = re.search(r'\{%-?\s*schema\s*-?%\}(.*?)\{%-?\s*endschema\s*-?%\}', src, re.S)
    return src[:m.start()], json.loads(m.group(1))


def render(body, **settings):
    return env.from_string(body).render(section={'settings': settings}).strip()


print('--- gb-wave: size routes ---')
body, schema = split(WAVE)
base = dict(direction='up', color_above='#ffffff', color_below='#faf9f8')

for size in ('sm', 'lg'):
    out = render(body, count=size, **base)
    grade(f'gb-wave--{size}' in out, f'count={size} puts the board size on as a class', out)
    grade('--wave-n' not in out, f'count={size} emits no --wave-n', out)

for n in ('3', '5'):
    out = render(body, count=n, **base)
    grade(f'--wave-n:{n};' in out, f'count={n} emits --wave-n:{n}', out)
    grade('gb-wave--' not in out, f'count={n} adds no board-size class', out)

print('\n--- gb-wave: unchanged behaviour ---')
out = render(body, count='sm', direction='down', **{k: v for k, v in base.items() if k != 'direction'})
grade('gb-scallop--down' in out, 'direction=down still adds gb-scallop--down', out)
out = render(body, count='sm', direction='up', color_above='', color_below='#b5ed61')
grade('--wave-bg:transparent' in out and '--wave-under:transparent' in out,
      'empty top colour still yields a transparent top and under', out)
grade('--wave-fg:#b5ed61' in out, 'bottom colour still lands on --wave-fg', out)
out = render(body, count='sm', **base)
grade(out.startswith('<div class="gb-scallop gb-wave gb-wave--sm"'),
      'base classes are kept in order', out)

print('\n--- gb-wave: schema ---')
opt = next(s for s in schema['settings'] if s.get('id') == 'count')
grade([o['value'] for o in opt['options']] == ['sm', 'lg', '3', '5'],
      'count offers the two board sizes first, then the counts', str(opt['options']))
grade(opt['default'] == 'sm', 'default is the small board size', opt['default'])
grade(schema['class'] == 'gb-wave-section', 'section wrapper class unchanged', schema['class'])

print('\n--- gb-footer: shape ---')
fbody, fschema = split(FOOTER)
grade("render 'gb-lines', text: section.settings.tagline" in fbody,
      'tagline renders through gb-lines')
grade('gb-rich-inline' not in fbody.split('tagline')[0][-200:],
      'the reverted gb-rich-inline call is gone from the tagline line')
tag = next(s for s in fschema['settings'] if s.get('id') == 'tagline')
grade(tag['type'] == 'textarea', 'tagline is a textarea so newlines can be typed', tag['type'])
grade('\n' in tag['default'], 'tagline default carries the two breaks', repr(tag['default']))
# The merge must not have dropped what the other team added while we were away.
grade(any(s.get('id') == 'newsletter_success' for s in fschema['settings']),
      'their newsletter_success setting survived the merge')
grade("form.posted_successfully?" in fbody and 'form.errors' in fbody,
      'their newsletter success/error markup survived the merge')

print(f'\n{ok} ok / {red} red')
sys.exit(1 if red else 0)
