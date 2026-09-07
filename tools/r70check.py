#!/usr/bin/env python3
"""r70 assertions against a theme dir: the three liquid gaps of docs/LIVE-GAP.md.

  python3 tools/r70check.py /home/ly/project/Gumi-Brand-shopify/work-r70
"""
import re
import sys
from pathlib import Path

STATIC = Path(__file__).resolve().parent.parent
theme = Path(sys.argv[1] if len(sys.argv) > 1 else
             '/home/ly/project/Gumi-Brand-shopify/work-r70')

fails = []
total = 0


def check(label, ok, detail=''):
    global total
    total += 1
    print('%s  %s%s' % ('PASS' if ok else 'FAIL', label,
                        '' if ok else '  -- ' + detail))
    if not ok:
        fails.append(label)


def read(rel):
    p = theme / rel
    if not p.exists():
        sys.exit('theme file missing: %s' % rel)
    return p.read_text()


index = (STATIC / 'index.html').read_text()
scss = (STATIC / 'assets/customstyle.scss').read_text()

# ---- 1. gb-stats: four arrows, byte-identical to the static export
stats = read('sections/gb-stats.liquid')
static_arrows = re.findall(
    r'<span class="gb-stats__arrow gb-stats__arrow--\d" aria-hidden="true">.*?</span>',
    index)
check('static site still has 4 arrow spans (anchor for this whole check)',
      len(static_arrows) == 4, 'found %d' % len(static_arrows))
for i, a in enumerate(static_arrows, 1):
    check('arrow--%d present and byte-identical to index.html' % i, a in stats)

bear = re.search(r'<div class="gb-stats__bear">(.*?)\n        </div>', stats, re.S)
check('.gb-stats__bear block located', bear is not None)
if bear:
    inner = bear.group(1)
    art_end = inner.find('</div>')
    first_arrow = inner.find('gb-stats__arrow')
    check('arrows sit inside .gb-stats__bear (CSS anchors % on it)',
          first_arrow > 0)
    check('arrows come after .gb-stats__bear-art closes',
          0 < art_end < first_arrow, 'art_end=%d arrow=%d' % (art_end, first_arrow))
check('arrow CSS is present in the stylesheet we ship',
      '.gb-stats__arrow--4' in scss)

# ---- 2. gb-reviews: disclaimer, last child of .gb-reviews__inner
reviews = read('sections/gb-reviews.liquid')
m = re.search(r'<p class="gb-reviews__disclaimer[^"]*">\{\{ s\.disclaimer \| escape \}\}</p>',
              reviews)
check('disclaimer paragraph rendered from s.disclaimer', m is not None)
check('disclaimer guarded by a blank test',
      '{%- if s.disclaimer != blank -%}' in reviews)
tail = reviews[reviews.find('gb-reviews__disclaimer'):]
check('disclaimer is the last child of .gb-reviews__inner',
      re.match(r'[^<]*</p>\s*\{%- endif -%\}\s*</div>\s*</section>', tail) is not None)

sm = re.search(r'\{% schema %\}(.*?)\{% endschema %\}', reviews, re.S)
check('schema declares the disclaimer setting as textarea',
      sm is not None and '"type": "textarea", "id": "disclaimer"' in sm.group(1))
static_text = re.search(
    r'<p class="gb-reviews__disclaimer[^"]*">([^<]+)</p>', index).group(1)
check('schema default is byte-identical to the static copy',
      sm is not None and ('"default": "%s"' % static_text) in sm.group(1),
      'static: %r' % static_text[:60])
check('disclaimer class carries the reveal classes the static site uses',
      'gb-reviews__disclaimer wowo fadeInUp' in reviews)
check('disclaimer CSS is present in the stylesheet we ship',
      '.gb-reviews__disclaimer {' in scss)

# ---- 3. gb-expert: title breaks only below 767
expert = read('sections/gb-expert.liquid')
check('expert title renders the prepared title_html',
      '{{ title_html }}' in expert)
check('no bare newline_to_br still reaching the h2',
      '{{ s.title | escape | newline_to_br }}' not in expert)
check("replace covers the '<br />' spelling",
      """replace: '<br />', '<br class="gb-br-narrow">'""" in expert)
check("replace covers the '<br>' spelling",
      """replace: '<br>', '<br class="gb-br-narrow">'""" in expert)
check('gb-br-narrow CSS is present in the stylesheet we ship',
      '.gb-br-narrow' in scss)

# ---- nothing else moved
for rel in ('sections/gb-stats.liquid', 'sections/gb-reviews.liquid',
            'sections/gb-expert.liquid'):
    check('%s has no trailing whitespace' % rel,
          not re.search(r'[ \t]+\n', read(rel)))

print('\n%d checks, %d failed' % (total, len(fails)))
sys.exit(1 if fails else 0)
