#!/usr/bin/env python3
"""r71 assertions: richtext-in-<p> unwrapping, and defer on our three scripts.

  python3 tools/r71check.py /home/ly/project/Gumi-Brand-shopify/work-r71
"""
import json
import re
import sys
from pathlib import Path

theme = Path(sys.argv[1] if len(sys.argv) > 1 else
             '/home/ly/project/Gumi-Brand-shopify/work-r71')

# (file, setting id, host class) -- the five richtext values that sat in a <p>
HOSTS = [
    ('sections/gb-footer.liquid', 'tagline', 'gb-footer__tagline'),
    ('sections/gb-hero.liquid', 'lead', 'gb-hero__lead'),
    ('sections/gb-nutrition.liquid', 'text', 'gb-highlight-card__text'),
    ('sections/gb-form-section.liquid', 'note', 'gb-form__note'),
    ('sections/gb-product.liquid', 'guarantee_note', 'gb-product__guarantee-note'),
]

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
        return None
    return p.read_text()


# ---- 1. the unwrap snippet
snip = read('snippets/gb-rich-inline.liquid')
check('snippets/gb-rich-inline.liquid exists', snip is not None)
if snip:
    for frag in ("replace: '</p><p>', '<br>'", "replace: '<p>', ''",
                 "replace: '</p>', ''", 'strip_newlines'):
        check('snippet applies %s' % frag, frag in snip)

# ---- 2. every <p> host renders through it, none still prints richtext raw
for rel, sid, cls in HOSTS:
    s = read(rel)
    if s is None:
        check('%s present' % rel, False, 'file missing')
        continue
    host = re.search(r'<p class="%s"[^>]*>(.*?)</p>' % re.escape(cls), s)
    check('%s: <p class="%s"> renders via gb-rich-inline' % (rel.split('/')[-1], cls),
          host is not None and 'gb-rich-inline' in host.group(1),
          repr(host.group(1))[:70] if host else 'host not found')
    check('%s: no raw {{ ...%s }} left inside a <p>' % (rel.split('/')[-1], sid),
          re.search(r'<p class="%s"[^>]*>\{\{[^}]*\b%s\b[^}]*\}\}'
                    % (re.escape(cls), re.escape(sid)), s) is None)

# ---- 3. our three scripts are deferred
sc = read('snippets/gb-scripts.liquid')
check('snippets/gb-scripts.liquid present', sc is not None)
if sc:
    for js in ('lenis.min.js', 'swiper-bundle.min.js', 'main.js'):
        m = re.search(r"<script src=\"\{\{ '%s' \| asset_url \}\}\"([^>]*)>"
                      % re.escape(js), sc)
        check('%s has defer' % js, m is not None and 'defer' in m.group(1),
              repr(m.group(1)) if m else 'tag not found')
    check('no bare (parser-blocking) script tag left in gb-scripts',
          not re.search(r"<script src=\"[^\"]+\">", sc))

# ---- 4. nothing else grew a richtext-in-<p> while we were in here
schema_bad = []
for f in sorted((theme / 'sections').glob('gb-*.liquid')):
    s = f.read_text()
    m = re.search(r'\{%\s*schema\s*%\}(.*?)\{%\s*endschema\s*%\}', s, re.S)
    if not m:
        continue
    d = json.loads(m.group(1))
    rich = [it['id'] for it in d.get('settings', []) if it.get('type') == 'richtext']
    for b in d.get('blocks', []) or []:
        rich += [it['id'] for it in b.get('settings', []) if it.get('type') == 'richtext']
    for rid in set(rich):
        if re.search(r'<p[^>]*>\{\{\s*[a-z_.]*\b%s\b[^}]*\}\}' % re.escape(rid), s):
            schema_bad.append('%s:%s' % (f.name, rid))
check('no richtext setting is printed raw inside a <p> anywhere',
      not schema_bad, ', '.join(schema_bad))

print('\n%d checks, %d failed' % (total, len(fails)))
sys.exit(1 if fails else 0)
