#!/usr/bin/env python3
"""Per-page comparison: static <main> block sequence vs live template sections.

Usage: livepages.py <live-theme-dir>
Names differ by construction (static uses the block class, the theme uses the
section filename), so the mapping below is the only place they meet.
"""
import json, re, sys, pathlib

SITE = pathlib.Path("/home/ly/project/Gumi-Brand")
LIVE = pathlib.Path(sys.argv[1])

# static page -> live template
PAGES = {
    "index":          "index.json",
    "pdp":            "product.json",
    "science":        "page.science.json",
    "reviews":        "page.reviews.json",
    "how-gumi-works": "page.how-gumi-works.json",
    "our-story":      "page.our-story.json",
    "faq":            "page.faq.json",
    "get-in-touch":   "page.get-in-touch.json",
    "referral":       "page.referral.json",
    "privacy-policy": "page.privacy-policy.json",
    "shipping":       "page.shipping.json",
}

# static block class -> live section type (only where the names differ)
ALIAS = {"gb-product-wrap": "gb-product", "gb-vs": None, "gb-promo": None}

MAIN_CHILD = re.compile(r'^    <(section|div|header|footer|aside|article)\b([^>]*)>')

def main_blocks(html):
    """Direct children of <main>, found by indentation -- the pages are formatted
    at two spaces per level, so <main> children sit at exactly four. An HTML
    parser cannot be used here: self-closing SVG tags unbalance the depth count."""
    lines = html.splitlines()
    try:
        i = next(n for n, l in enumerate(lines) if l.strip().startswith("<main"))
        j = next(n for n, l in enumerate(lines) if l.strip().startswith("</main"))
    except StopIteration:
        raise SystemExit("no <main> found -- page layout changed, fix this probe")
    out = []
    for l in lines[i + 1:j]:
        m = MAIN_CHILD.match(l)
        if not m:
            continue
        c = re.search(r'class="([^"]*)"', m.group(2))
        cls = c.group(1) if c else ""
        g = re.search(r'\bgb-[a-z0-9-]+', cls)
        out.append(g.group(0) if g else f"<{m.group(1)} {cls[:40]}>")
    if not out:
        raise SystemExit("no <main> children matched -- indentation changed, fix this probe")
    return out

def live_sections(name):
    f = LIVE / "templates" / name
    d = json.loads(re.sub(r'/\*.*?\*/', '', f.read_text(), flags=re.S))
    order = d.get("order") or list(d.get("sections", {}).keys())
    return [d["sections"][k].get("type") for k in order]

gaps = []
for page, tpl in PAGES.items():
    static = main_blocks((SITE / f"{page}.html").read_text(encoding="utf-8", errors="replace"))
    live = live_sections(tpl)
    liveset = set(live)
    print(f"\n=== {page}.html  ->  {tpl}")
    for b in static:
        target = ALIAS.get(b, b)
        if target is None:
            ok = "MISSING"
        elif target in liveset:
            ok = "ok"
        elif (LIVE / "sections" / f"{target}.liquid").exists():
            ok = "section exists, NOT in template"
        else:
            ok = "MISSING"
        if ok != "ok":
            gaps.append((page, b, ok))
        print(f"    {ok:28s} {b}")
    extra = [s for s in live if s not in {ALIAS.get(b, b) for b in static}]
    if extra:
        print(f"    live-only sections: {', '.join(extra)}")

print("\n=== GAPS ===")
for page, b, why in gaps:
    print(f"  {page:16s} {b:24s} {why}")
print(f"total: {len(gaps)}")
