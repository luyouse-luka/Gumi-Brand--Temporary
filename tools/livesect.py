#!/usr/bin/env python3
"""Third layer: sections that exist on both sides but differ inside.

Usage: livesect.py <live-theme-dir>
Modifier tokens the theme builds with {% assign %} / {{ }} are suppressed --
gb-stat--{{ b.variant }} cannot be matched literally and is not a real gap.
"""
import re, sys, pathlib, collections

SITE = pathlib.Path("/home/ly/project/Gumi-Brand")
LIVE = pathlib.Path(sys.argv[1])

PAGES = ["index", "pdp", "science", "reviews", "how-gumi-works", "our-story",
         "faq", "get-in-touch", "referral", "privacy-policy", "shipping"]
TOK = re.compile(r'\bgb-[a-z0-9-]+(?:__[a-z0-9-]+)?(?:--[a-z0-9-]+)?\b')
CLS = re.compile(r'class="([^"]*)"')
CHILD = re.compile(r'^    <(section|div|header|footer|aside|article)\b([^>]*)>')

def site_blocks(page):
    """(root class, tokens inside) for each direct child of <main>."""
    lines = (SITE / f"{page}.html").read_text(encoding="utf-8", errors="replace").splitlines()
    i = next(n for n, l in enumerate(lines) if l.strip().startswith("<main"))
    j = next(n for n, l in enumerate(lines) if l.strip().startswith("</main"))
    starts = [n for n in range(i + 1, j) if CHILD.match(lines[n])]
    out = []
    for k, n in enumerate(starts):
        end = starts[k + 1] if k + 1 < len(starts) else j
        body = "\n".join(lines[n:end])
        m = CLS.search(CHILD.match(lines[n]).group(2))
        g = re.search(r'\bgb-[a-z0-9-]+', m.group(1) if m else "")
        toks = set()
        for c in CLS.finditer(body):
            toks |= set(TOK.findall(c.group(1)))
        out.append((g.group(0) if g else "?", toks))
    return out

RENDER = re.compile(r"\{%-?\s*(?:render|include)\s+'([^']+)'")

def expand(f, seen=None):
    """Section source plus every snippet it renders -- gb-sub lives in a snippet."""
    seen = seen or set()
    if f.name in seen or not f.exists():
        return ""
    seen.add(f.name)
    text = f.read_text(encoding="utf-8", errors="replace")
    for name in RENDER.findall(text):
        text += expand(LIVE / "snippets" / f"{name}.liquid", seen)
    return text

def dynamic_prefixes(text):
    """Class prefixes the theme completes at render time."""
    return set(re.findall(r'\b(gb-[a-z0-9-]+)(?:--|__)\{[{%]', text))

total = 0
for page in PAGES:
    for root, toks in site_blocks(page):
        f = LIVE / "sections" / f"{root}.liquid"
        if not f.exists():
            continue
        text = expand(f)
        live = set(TOK.findall(text))
        dyn = dynamic_prefixes(text)
        missing = sorted(t for t in toks - live
                         if re.split(r'__|--', t)[0] not in dyn)
        if missing:
            total += len(missing)
            print(f"\n=== {page}.html  {root}  ->  sections/{root}.liquid")
            for t in missing:
                print(f"    - {t}")
print(f"\ntotal tokens present in static block but absent from its live section: {total}")
