#!/usr/bin/env python3
"""Find copy the mobile boards break by hand (U+2028) that the build runs on.

    python3 tools/hardbreaks.py [page.html ...]

Width alone cannot reproduce these: .gb-nutrition__title fits "in" on the first
line at any measure the board allows, and the board still breaks before it. The
project's answer is <br class="gb-br-narrow">, which only shows below 768 -- the
desktop board runs the same sentence flat.

Reported as MISSING only when the build has the same sentence with no <br> in
the gap. Copy that does not appear on the page at all is reported separately:
that is a content difference, not a line-break one, and gets decided by hand.
"""
import glob, json, os, re, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NODES = os.path.join(ROOT, "figma/nodes")

BOARDS = {
    "index.html":          "228-5932_homepage-mobile",
    "pdp.html":            "324-53792_pdp-mobile",
    "science.html":        "324-58044_science-moble",
    "reviews.html":        "324-64961_reviews",
    "how-gumi-works.html": "324-70523_how-gumi-works",
    "our-story.html":      "324-73673_our-story",
    "faq.html":            "324-76169_faq",
    "get-in-touch.html":   "326-80318_get-in-touch",
    "referral.html":       "326-81540_referral",
    "shipping.html":       "326-83129_shipping",
    "privacy-policy.html": "326-83399_privacy-policy",
}

TAG = re.compile(r"<[^>]+>")
WS = re.compile(r"\s+")


def norm(s):
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("’", "'").replace("‘", "'").replace("&#39;", "'")
    s = s.replace("“", '"').replace("”", '"').replace("&amp;", "&").replace("&nbsp;", " ")
    return WS.sub(" ", s).strip()


def board_breaks(stem):
    d = json.load(open(os.path.join(NODES, stem + ".json")))
    out = []
    seen = set()

    def w(n, vis=True):
        v = vis and n.get("visible", True) is not False
        if v and n["type"] == "TEXT" and " " in n.get("characters", ""):
            c = n["characters"]
            if c not in seen:
                seen.add(c)
                out.append((n["id"], c))
        for k in n.get("children") or []:
            w(k, v)

    for val in d["nodes"].values():
        w(val["document"])
    return out


def check(page):
    stem = BOARDS[page]
    html = open(os.path.join(ROOT, page), encoding="utf-8").read()
    # the rendered text of the page, with <br> kept as a marker
    body = html
    body = re.sub(r"<br[^>]*>", "\x00", body)   # \s eats U+2028, \x00 survives norm()
    body = re.sub(r"<(script|style|svg)\b.*?</\1>", " ", body, flags=re.S | re.I)
    text = TAG.sub(" ", body)
    text = "\x00".join(norm(seg) for seg in text.split("\x00"))

    rows = []
    for nid, chars in board_breaks(stem):
        parts = [norm(p) for p in chars.split(" ")]
        if any(not p for p in parts):
            parts = [p for p in parts if p]
        if len(parts) < 2:
            continue
        joined_hard = "\x00".join(parts)
        joined_soft = " ".join(parts)
        if joined_hard in text:
            rows.append(("ok", nid, parts))
        elif joined_soft in text:
            rows.append(("MISSING", nid, parts))
        else:
            rows.append(("absent", nid, parts))
    return rows


pages = sys.argv[1:] or list(BOARDS)
tot = {"ok": 0, "MISSING": 0, "absent": 0}
for p in pages:
    if p not in BOARDS:
        continue
    rows = check(p)
    bad = [r for r in rows if r[0] != "ok"]
    print(f"\n=== {p} === {len(rows)} hard-broken node(s), "
          f"{sum(1 for r in rows if r[0]=='ok')} ok, "
          f"{sum(1 for r in rows if r[0]=='MISSING')} missing, "
          f"{sum(1 for r in rows if r[0]=='absent')} not on page")
    for st, nid, parts in bad:
        joined = " ⏎ ".join(x[:46] for x in parts)
        print(f"  [{st:<7}] {nid[-11:]:<13} {joined[:110]}")
    for k in tot:
        tot[k] += sum(1 for r in rows if r[0] == k)
print(f"\nTOTAL ok={tot['ok']}  MISSING={tot['MISSING']}  not-on-page={tot['absent']}")
