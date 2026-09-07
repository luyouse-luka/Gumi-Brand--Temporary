#!/usr/bin/env python3
"""Static site vs live theme: which gb-* modules exist on each side.

Usage: livediff.py <live-theme-dir>
Class tokens are the only shared vocabulary between the two sides -- the static
pages are HTML, the theme is Liquid, so nothing else lines up.
"""
import re, sys, pathlib, collections

SITE = pathlib.Path("/home/ly/project/Gumi-Brand")
LIVE = pathlib.Path(sys.argv[1])

PAGES = ["index", "pdp", "science", "reviews", "how-gumi-works", "our-story",
         "faq", "get-in-touch", "referral", "privacy-policy", "shipping"]

CLS = re.compile(r'class\s*=\s*"([^"]*)"')
TOK = re.compile(r'\bgb-[a-z0-9-]+(?:__[a-z0-9-]+)?(?:--[a-z0-9-]+)?\b')

def tokens(text):
    out = set()
    for m in CLS.finditer(text):
        out |= set(TOK.findall(m.group(1)))
    return out

# static side, per page
site = {}
for p in PAGES:
    f = SITE / f"{p}.html"
    site[p] = tokens(f.read_text(encoding="utf-8", errors="replace"))

# live side, every liquid/json file
live = set()
live_where = collections.defaultdict(set)
for d in ("sections", "snippets", "blocks", "layout", "templates"):
    for f in sorted((LIVE / d).glob("*")):
        if f.suffix not in (".liquid", ".json"):
            continue
        # live side scans the WHOLE file, not just class="": Liquid builds class
        # strings via {% assign %} and passes them as {% form class: %} arguments.
        # A token absent from the entire file is the only sound "not implemented".
        t = set(TOK.findall(f.read_text(encoding="utf-8", errors="replace")))
        live |= t
        for tok in t:
            live_where[tok].add(f"{d}/{f.name}")

all_site = set().union(*site.values())
missing = sorted(all_site - live)
extra = sorted(live - all_site)

# group by block (the part before __ or --)
def block(t):
    return re.split(r'__|--', t)[0]

by_block = collections.defaultdict(list)
for t in missing:
    by_block[block(t)].append(t)

print(f"static gb-* tokens: {len(all_site)}   live gb-* tokens: {len(live)}")
print(f"missing on live: {len(missing)}   live-only: {len(extra)}\n")

print("=== BLOCKS MISSING ENTIRELY ON LIVE ===")
for b in sorted(by_block):
    present = {t for t in live if block(t) == b}
    if not present:
        pages = sorted(p for p in PAGES if any(block(t) == b for t in site[p]))
        print(f"  {b:34s} {len(by_block[b]):3d} tokens   pages: {','.join(pages)}")

print("\n=== BLOCKS PARTIALLY ON LIVE (module exists, some tokens absent) ===")
for b in sorted(by_block):
    present = {t for t in live if block(t) == b}
    if present:
        print(f"  {b:34s} missing {len(by_block[b]):3d} / have {len(present):3d}")
        for t in by_block[b]:
            print(f"      - {t}")

print("\n=== LIVE-ONLY TOKENS (theme has, static does not) ===")
for t in extra:
    print(f"  {t:44s} {','.join(sorted(live_where[t]))}")
