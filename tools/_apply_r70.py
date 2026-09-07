#!/usr/bin/env python3
"""r70: three liquid gaps on the live theme (docs/LIVE-GAP.md section 3).

Writes into the working copy passed as argv[1] (a pulled theme dir), then the
caller mirrors the touched files into the repo's liquid/.
"""
import re
import sys
from pathlib import Path

STATIC = Path(__file__).resolve().parent.parent
theme = Path(sys.argv[1] if len(sys.argv) > 1 else
             '/home/ly/project/Gumi-Brand-shopify/work-r70')

DISCLAIMER = ('Testimonials featured in videos or other promotional materials '
              'may include individuals who received compensation, free product, '
              'or other incentives')


def edit(path, old, new, count=1):
    p = theme / path
    s = p.read_text()
    n = s.count(old)
    if n != count:
        sys.exit('FAIL %s: anchor found %d times, expected %d' % (path, n, count))
    p.write_text(s.replace(old, new, count))
    print('  ok  %s' % path)


# ---- 1. gb-stats: the four decorative arrows, absolute inside .gb-stats__bear
index = (STATIC / 'index.html').read_text()
arrows = re.findall(
    r'<span class="gb-stats__arrow gb-stats__arrow--\d" aria-hidden="true">.*?</span>',
    index)
if len(arrows) != 4:
    sys.exit('FAIL: expected 4 arrow spans in index.html, got %d' % len(arrows))

edit('sections/gb-stats.liquid',
     '            </picture>\n          </div>\n        </div>',
     '            </picture>\n          </div>\n' +
     ''.join('          %s\n' % a for a in arrows) +
     '        </div>')

# ---- 2. gb-reviews: legal disclaimer, last child of .gb-reviews__inner
edit('sections/gb-reviews.liquid',
     '    </div>\n  </div>\n</section>',
     '    </div>\n'
     '    {%- if s.disclaimer != blank -%}\n'
     '      <p class="gb-reviews__disclaimer wowo fadeInUp">{{ s.disclaimer | escape }}</p>\n'
     '    {%- endif -%}\n'
     '  </div>\n</section>')

edit('sections/gb-reviews.liquid',
     '    { "type": "text", "id": "aria_label", "label": "Carousel aria label", "default": "Customer reels" }',
     '    { "type": "text", "id": "aria_label", "label": "Carousel aria label", "default": "Customer reels" },\n'
     '    { "type": "textarea", "id": "disclaimer", "label": "Disclaimer", "default": "%s" }'
     % DISCLAIMER)

# ---- 3. gb-expert: newline_to_br emits a bare <br>, which breaks on desktop
# too. The board only breaks this title below 767. Both spellings are replaced
# because the live render cannot be read back (storefront password) -- either
# one is a no-op on the output the other matches.
edit('sections/gb-expert.liquid',
     """{%- liquid
  assign s = section.settings""",
     """{%- liquid
  assign s = section.settings
  assign title_html = s.title | escape | newline_to_br
  assign title_html = title_html | replace: '<br />', '<br class="gb-br-narrow">'
  assign title_html = title_html | replace: '<br>', '<br class="gb-br-narrow">'""")

edit('sections/gb-expert.liquid',
     '{{ s.title | escape | newline_to_br }}',
     '{{ title_html }}')

print('r70 applied to %s' % theme)
