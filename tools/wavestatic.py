#!/usr/bin/env python3
"""Static-site wave truth: section order per page and the scallop each section carries.

  python3 tools/wavestatic.py [page.html ...]

Regex over the markup rather than a DOM parse -- SVG self-closing tags wreck
depth counting here (see memory note), and every section marker is on one line.
"""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SEC = re.compile(r'<(?:section|footer|div)\b[^>]*class="([^"]*\bgb-[a-z-]+[^"]*)"', re.I)
SCAL = re.compile(r'class="([^"]*\bgb-scallop\b[^"]*)"')


def base(cls):
    for c in cls.split():
        if re.fullmatch(r'gb-[a-z-]+', c) and c != 'gb-scallop':
            return c
    return None


def page(p):
    html = p.read_text(errors='replace')
    marks = []
    for m in re.finditer(r'<(section|footer)\b[^>]*class="([^"]*)"', html, re.I):
        b = base(m.group(2))
        if b:
            marks.append((m.start(), b, m.group(2)))
    # scallops, mapped to the nearest preceding section marker
    out = []
    for i, (pos, b, cls) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(html)
        mods = []
        for s in SCAL.finditer(html, pos, end):
            mods.append([c[12:] for c in s.group(1).split() if c.startswith('gb-scallop--')])
        out.append((b, cls, mods))
    return out


for f in (sys.argv[1:] or sorted(str(x) for x in ROOT.glob('*.html'))):
    p = pathlib.Path(f)
    if p.name == 'font-check.html':
        continue
    print(f'\n══ {p.name} ══')
    for b, cls, mods in page(p):
        variant = ' '.join(c for c in cls.split() if c.startswith(b + '--'))
        print(f'  {b:<20} {variant}')
        for m in mods:
            print(f'      ~~~ {" ".join(m) or "(bare)"}')
