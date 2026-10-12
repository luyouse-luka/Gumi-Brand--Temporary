#!/usr/bin/env python3
"""r99: route every line-breakable setting through snippets/gb-lines.liquid.

Each edit asserts its anchor occurs exactly once, so a third-party rewrite of the
file upstream fails loudly here instead of landing a half-applied change.
"""
import pathlib, sys

W = pathlib.Path('/home/ly/project/Gumi-Brand-shopify/work-r99/sections')
n = 0

def sub(fname, old, new):
    global n
    p = W / fname
    t = p.read_text(encoding='utf-8')
    c = t.count(old)
    if c != 1:
        sys.exit(f'ABORT {fname}: anchor x{c}\n  {old[:110]}')
    p.write_text(t.replace(old, new), encoding='utf-8')
    n += 1

# ---- render sites -------------------------------------------------------
sub('gb-footer.liquid',
    """<p class="gb-footer__tagline">{%- render 'gb-rich-inline', html: section.settings.tagline -%}</p>""",
    """<p class="gb-footer__tagline">{%- render 'gb-lines', text: section.settings.tagline -%}</p>""")

sub('gb-page-hero.liquid',
    """<h1 class="gb-page-hero__title" data-line-reveal>{{ s.title | escape }}</h1>""",
    """<h1 class="gb-page-hero__title" data-line-reveal>{%- render 'gb-lines', text: s.title -%}</h1>""")

sub('gb-hero.liquid',
    """<p class="gb-hero__lead" data-line-reveal>{%- render 'gb-rich-inline', html: s.lead -%}</p>""",
    """<p class="gb-hero__lead" data-line-reveal>{%- render 'gb-lines', text: s.lead -%}</p>""")

sub('gb-hero.liquid',
    """<span class="gb-usp__label">{{ b.label }}</span>""",
    """<span class="gb-usp__label">{%- render 'gb-lines', text: b.label -%}</span>""")

sub('gb-reviews.liquid',
    """<h2 class="gb-reviews__title" data-line-reveal>{{ s.title | escape | newline_to_br }}</h2>""",
    """<h2 class="gb-reviews__title" data-line-reveal>{%- render 'gb-lines', text: s.title -%}</h2>""")

sub('gb-science.liquid',
    """<h2 class="gb-science__title" data-line-reveal>{{ s.title }}</h2>""",
    """<h2 class="gb-science__title" data-line-reveal>{%- render 'gb-lines', text: s.title -%}</h2>""")

sub('gb-nutrition.liquid',
    """<h2 class="gb-nutrition__title wowo fadeInUp" data-line-reveal>{{ s.title }}</h2>""",
    """<h2 class="gb-nutrition__title wowo fadeInUp" data-line-reveal>{%- render 'gb-lines', text: s.title -%}</h2>""")

sub('gb-nutrition.liquid',
    """<p class="gb-highlight-card__text">{{ b.text | escape | newline_to_br }}</p>""",
    """<p class="gb-highlight-card__text">{%- render 'gb-lines', text: b.text -%}</p>""")

sub('gb-stats.liquid',
    """<h2 class="gb-stats__title" data-line-reveal>{{ s.title }}</h2>""",
    """<h2 class="gb-stats__title" data-line-reveal>{%- render 'gb-lines', text: s.title -%}</h2>""")

sub('gb-stats.liquid',
    """<p class="gb-stat__label" data-line-reveal>{{ b.label }}</p>""",
    """<p class="gb-stat__label" data-line-reveal>{%- render 'gb-lines', text: b.label -%}</p>""")

sub('gb-promo.liquid',
    """%}">{{ block.settings.title }}</h2>""",
    """%}">{%- render 'gb-lines', text: block.settings.title -%}</h2>""")

# The halo is a duplicate of the same copy painted behind it; both need the breaks.
sub('gb-dosed.liquid',
    """<span class="gb-ink-halo" aria-hidden="true">{{ b.title }}</span>{{ b.title }}</h2>""",
    """<span class="gb-ink-halo" aria-hidden="true">{%- render 'gb-lines', text: b.title -%}</span>"""
    """{%- render 'gb-lines', text: b.title -%}</h2>""")

# gb-expert grew its own inline version of this in r83; the snippet supersedes it.
sub('gb-expert.liquid',
    """  assign title_html = s.title | escape | newline_to_br
  assign title_html = title_html | replace: '<br />', '<br class="gb-br-narrow">'
  assign title_html = title_html | replace: '<br>', '<br class="gb-br-narrow">'
""", "")
sub('gb-expert.liquid',
    """<h2 class="gb-expert__title wowo fadeInUp" data-line-reveal>{{ title_html }}</h2>""",
    """<h2 class="gb-expert__title wowo fadeInUp" data-line-reveal>{%- render 'gb-lines', text: s.title -%}</h2>""")

# ---- setting types ------------------------------------------------------
# text/richtext render as a one-line input, so a newline cannot even be typed.
INFO = ('"info": "Press Enter to break the line on mobile only. '
        'End a line with // to break at every width, or with ^^ to break on desktop only."')

sub('gb-footer.liquid',
    """{ "type": "richtext", "id": "tagline", "label": "Tagline", "default": "<p>Made with more care than a vitamin gummy probably needs. That's on purpose.</p>" },""",
    """{ "type": "textarea", "id": "tagline", "label": "Tagline", "default": "Made with more care than a\\nvitamin gummy probably needs.\\nThat's on purpose.", %s },""" % INFO)

sub('gb-page-hero.liquid',
    """{ "type": "text", "id": "title", "label": "Title", "default": "Page title" },""",
    """{ "type": "textarea", "id": "title", "label": "Title", "default": "Page title", %s },""" % INFO)

sub('gb-hero.liquid',
    """{ "type": "richtext", "id": "lead", "label": "Lead", "default": "<p>Real fruit, real veg, real vitamins, hiding in a gumi bear.</p>" },""",
    """{ "type": "textarea", "id": "lead", "label": "Lead", "default": "Real fruit, real veg, real vitamins,\\nhiding in a gumi bear.", %s },""" % INFO)

sub('gb-hero.liquid',
    """{ "type": "text", "id": "label", "label": "Label", "default": "Clean Ingredients" }""",
    """{ "type": "textarea", "id": "label", "label": "Label", "default": "Clean Ingredients", %s }""" % INFO)

sub('gb-reviews.liquid',
    """{ "type": "text", "id": "title", "label": "Title", "default": "Aussies are obsessed. Here's why." },""",
    """{ "type": "textarea", "id": "title", "label": "Title", "default": "Aussies are obsessed.//\\nHere's why.", %s },""" % INFO)

sub('gb-science.liquid',
    """{ "type": "inline_richtext", "id": "title", "label": "Heading (optional)" },""",
    """{ "type": "textarea", "id": "title", "label": "Heading (optional)", %s },""" % INFO)

sub('gb-nutrition.liquid',
    """{ "type": "richtext", "id": "title", "label": "Title", "default": "<p>Nutrition that fits in your pocket</p>" },""",
    """{ "type": "textarea", "id": "title", "label": "Title", "default": "Nutrition that fits\\nin your pocket", %s },""" % INFO)

sub('gb-stats.liquid',
    """{ "type": "richtext", "id": "title", "label": "Title", "default": "<p>60+ whole foods. No juicer, no fuss.</p>" },""",
    """{ "type": "textarea", "id": "title", "label": "Title", "default": "60+ whole foods.//\\nNo juicer, no fuss.", %s },""" % INFO)

sub('gb-stats.liquid',
    """{ "type": "text", "id": "label", "label": "Label", "default": "Clean Ingredients" },""",
    """{ "type": "textarea", "id": "label", "label": "Label", "default": "Clean Ingredients", %s },""" % INFO)

sub('gb-promo.liquid',
    """{ "type": "text", "id": "title", "label": "Title", "default": "Card title" },""",
    """{ "type": "textarea", "id": "title", "label": "Title", "default": "Card title", %s },""" % INFO)

sub('gb-dosed.liquid',
    """{ "type": "text", "id": "title", "label": "Title", "default": "Row title" },""",
    """{ "type": "textarea", "id": "title", "label": "Title", "default": "Row title", %s },""" % INFO)

sub('gb-expert.liquid',
    """{ "type": "text", "id": "title", "label": "Title", "default": "Recommended\\nby experts" },""",
    """{ "type": "textarea", "id": "title", "label": "Title", "default": "Recommended\\nby experts", %s },""" % INFO)

print(f'{n} edits applied')
