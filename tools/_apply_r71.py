#!/usr/bin/env python3
"""r71: the two live defects found by tools/liveprobe70.py.

  A) richtext settings inside a <p> host -- the parser closes the host early,
     the text lands outside it and loses the class (measured: .gb-hero__lead
     empty, height 0, text rendering at the browser default 16px).
  B) lenis/swiper/main.js are parser-blocking at 172KB into <body>, so the
     [data-line-reveal] fallback left text fully visible for 4029 ms.

Writes into the working copy passed as argv[1].
"""
import sys
from pathlib import Path

theme = Path(sys.argv[1] if len(sys.argv) > 1 else
             '/home/ly/project/Gumi-Brand-shopify/work-r71')

SNIPPET = """{%- comment -%}
  richtext settings ship their value wrapped in <p>. Inside a <p> host the HTML
  parser closes the host early, so the text ends up as a sibling and loses the
  host's class and every style on it. Unwrap here; paragraph breaks survive as
  <br>. Callers that render into a <div> do not need this.
{%- endcomment -%}
{{- html | strip_newlines | replace: '</p><p>', '<br>' | replace: '<p>', '' | replace: '</p>', '' | strip -}}
"""

# (file, old, new) -- every anchor must be unique in its file
EDITS = [
    ('snippets/gb-scripts.liquid',
     '<script src="{{ \'lenis.min.js\' | asset_url }}"></script>\n'
     '<script src="{{ \'swiper-bundle.min.js\' | asset_url }}"></script>\n'
     '<script src="{{ \'main.js\' | asset_url }}"></script>',
     '{%- comment -%}\n'
     '  defer, not bare: these sit ~172KB into <body>, so parser-blocking tags\n'
     '  held main.js back ~3.6s and [data-line-reveal] text stayed visible that\n'
     '  whole time. defer keeps execution order and runs before DOMContentLoaded.\n'
     '{%- endcomment -%}\n'
     '<script src="{{ \'lenis.min.js\' | asset_url }}" defer></script>\n'
     '<script src="{{ \'swiper-bundle.min.js\' | asset_url }}" defer></script>\n'
     '<script src="{{ \'main.js\' | asset_url }}" defer></script>'),

    ('sections/gb-footer.liquid',
     '<p class="gb-footer__tagline">{{ section.settings.tagline }}</p>',
     '<p class="gb-footer__tagline">{%- render \'gb-rich-inline\', html: section.settings.tagline -%}</p>'),

    ('sections/gb-hero.liquid',
     '<p class="gb-hero__lead" data-line-reveal>{{ s.lead }}</p>',
     '<p class="gb-hero__lead" data-line-reveal>{%- render \'gb-rich-inline\', html: s.lead -%}</p>'),

    ('sections/gb-nutrition.liquid',
     '<p class="gb-highlight-card__text">{{ b.text }}</p>',
     '<p class="gb-highlight-card__text">{%- render \'gb-rich-inline\', html: b.text -%}</p>'),

    ('sections/gb-form-section.liquid',
     '<p class="gb-form__note">{{ s.note }}</p>',
     '<p class="gb-form__note">{%- render \'gb-rich-inline\', html: s.note -%}</p>'),

    ('sections/gb-product.liquid',
     '<p class="gb-product__guarantee-note">{{ section.settings.guarantee_note }}</p>',
     '<p class="gb-product__guarantee-note">{%- render \'gb-rich-inline\', html: section.settings.guarantee_note -%}</p>'),
]

snip = theme / 'snippets/gb-rich-inline.liquid'
snip.write_text(SNIPPET)
print('  new snippets/gb-rich-inline.liquid')

for rel, old, new in EDITS:
    p = theme / rel
    s = p.read_text()
    n = s.count(old)
    if n != 1:
        sys.exit('FAIL %s: anchor found %d times, expected 1' % (rel, n))
    p.write_text(s.replace(old, new, 1))
    print('  ok  %s' % rel)

print('r71 applied to %s' % theme)
