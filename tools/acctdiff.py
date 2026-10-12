#!/usr/bin/env python3
"""Text-token diff: Figma board JSON vs the rendered page.

Pairs every TEXT node on a board with the element that renders the same string,
then compares font-size / line-height / letter-spacing / weight / colour. Only
the text tokens -- geometry is acctcheck.py's job.

Boards live in figma/account/nodes/. Nothing here calls the Figma API.

  python3 tools/acctdiff.py            # every board in BOARDS
  python3 tools/acctdiff.py overview   # only boards whose key contains "overview"
"""
import json, pathlib, re, sys, unicodedata
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
NODES = ROOT / "figma/account/nodes"


def _chrome():
    base = pathlib.Path.home() / ".cache/ms-playwright"
    hits = sorted(base.glob("chromium-*/chrome-linux64/chrome"))
    if not hits:
        sys.exit("no chromium under %s -- run: npx playwright install chromium" % base)
    return str(hits[-1])


CHROME = _chrome()
SHOW_UNMATCHED = False

# board key -> (node json stem, page, viewport, view to switch to or None)
BOARDS = {
    "overview@1440":      ("2284-27678", "account.html",        1440, None),
    "subscriptions@1440": ("2284-28000", "account.html",        1440, "subscriptions"),
    "detail@1440":        ("2284-27792", "account.html",        1440, "detail"),
    "login@1440":         ("2284-35137", "account-login.html",  1440, None),
    "signup@1440":        ("2284-35059", "account-login.html",  1440, "signup"),
    "overview@390":       ("2284-27604", "account.html",        390,  None),
    "subscriptions@390":  ("2284-28305", "account.html",        390,  "subscriptions"),
    "detail@390":         ("2284-28330", "account.html",        390,  "detail"),
    "orders@390":         ("2284-27202", "account.html",        390,  "orders"),
    "order@390":          ("2284-27304", "account.html",        390,  "order"),
    "details@390":        ("2284-27081", "account.html",        390,  "details"),
    "password@390":       ("2284-27151", "account.html",        390,  "password"),
    "help@390":           ("2284-27170", "account.html",        390,  "help"),
    "login@390":          ("2284-34993", "account-login.html",  390,  None),
    "signup@390":         ("2284-35023", "account-login.html",  390,  "signup"),
}

# Frames that are staging, not content: the fake browser chrome on every phone
# board, and the sticky notes. Their text must never pair with anything.
SKIP_ANCESTOR = ("Chrome browser", "note", "Frame 15")
# Substring match as well: the desktop boards stage the browser with Figma's
# Safari component instead of the phone boards' "Chrome browser" instance.
SKIP_SUBSTR = ("Safari", "toolbar")


def norm(s):
    """Fold the differences that are not design decisions."""
    s = unicodedata.normalize("NFKC", s or "")
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-").replace(" ", " ")
    return re.sub(r"\s+", " ", s).strip().lower()


def hexof(fills):
    for f in fills or []:
        if f.get("type") == "SOLID" and f.get("visible", True):
            c = f["color"]
            return "#%02x%02x%02x" % tuple(round(c[k] * 255) for k in "rgb")
    return None


def board_texts(stem):
    hits = list(NODES.glob(stem + "_*.json"))
    if not hits:
        sys.exit("no board json for %s" % stem)
    doc = json.load(open(hits[0], encoding="utf-8"))["document"]
    top = (doc.get("absoluteBoundingBox") or {}).get("y", 0)
    out = []

    def walk(n, chain):
        name = n.get("name", "")
        if name in SKIP_ANCESTOR or any(x in name for x in SKIP_SUBSTR):
            return
        if n.get("visible", True) is False:
            return
        if n.get("type") == "TEXT" and n.get("characters", "").strip():
            st = n.get("style", {})
            out.append({
                "text": n["characters"],
                "key": norm(n["characters"]),
                "size": st.get("fontSize"),
                "lh": st.get("lineHeightPx"),
                "ls": st.get("letterSpacing", 0.0) or 0.0,
                "weight": st.get("fontWeight"),
                "color": hexof(n.get("fills")),
                "overrides": bool(n.get("characterStyleOverrides")),
                "y": (n.get("absoluteBoundingBox") or {}).get("y", 0) - top,
            })
        for c in n.get("children", []):
            walk(c, chain + [name])

    walk(doc, [])
    out.sort(key=lambda d: d["y"])
    return out


READ = """
() => {
  const out = [];
  for (const el of document.querySelectorAll('body *')) {
    // visibilityProperty: the account menu fades via visibility:hidden while
    // keeping display (r-a20), and the default check would measure it as shown.
    if (!el.checkVisibility || !el.checkVisibility({visibilityProperty: true})) continue;
    let own = '';
    for (const n of el.childNodes) if (n.nodeType === 3) own += n.nodeValue;
    // A filled field's text lives in .value, an empty one's in @placeholder;
    // neither is a child text node, so both have to be asked for by name.
    if (!own.trim()) own = el.value || el.getAttribute('placeholder') || '';
    if (!own.trim()) continue;
    const cs = getComputedStyle(el);
    const r = el.getBoundingClientRect();
    out.push({
      // Two names for the same element: `own` is just its own text nodes, which
      // is how Figma splits a sentence that wraps a link; `full` is innerText,
      // which is what carries text-transform. A board string may match either.
      text: (el.innerText || '').trim() || own,
      own: own,
      size: parseFloat(cs.fontSize),
      lh: cs.lineHeight === 'normal' ? null : parseFloat(cs.lineHeight),
      ls: cs.letterSpacing === 'normal' ? 0 : parseFloat(cs.letterSpacing),
      weight: parseInt(cs.fontWeight, 10),
      color: cs.color,
      transform: cs.textTransform,
      y: r.top + scrollY,
      sel: el.tagName.toLowerCase() + (el.className && typeof el.className === 'string'
           ? '.' + el.className.trim().split(/\\s+/).join('.') : ''),
    });
  }
  return out;
}
"""


def rgb2hex(s):
    m = re.match(r"rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)", s or "")
    return "#%02x%02x%02x" % tuple(round(float(m.group(i))) for i in (1, 2, 3)) if m else s


def main():
    global SHOW_UNMATCHED
    SHOW_UNMATCHED = "-u" in sys.argv
    want = [a for a in sys.argv[1:] if not a.startswith("-")]
    keys = [k for k in BOARDS if not want or any(w in k for w in want)]
    pairs = diffs = unmatched = 0
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME)
        for key in keys:
            stem, page, w, view = BOARDS[key]
            board = board_texts(stem)
            pg = b.new_page(viewport={"width": w, "height": 900})
            pg.goto("file://" + str(ROOT / page))
            pg.wait_for_timeout(500)
            if view:
                nav = ".gb-acct-nav" if w > 767 else ".gb-acct-list"
                try:
                    if view == "detail":
                        # ⚠ Task 40: the view being left runs a 500ms exit
                        # animation; reading sooner samples the old view's copy
                        # of the same strings
                        pg.click(nav + " [data-acct-goto='subscriptions']", timeout=3000)
                        pg.wait_for_timeout(750)
                        pg.click("[data-acct-view='subscriptions'] "
                                 ".gb-acct-sub__cta[data-acct-goto='detail']", timeout=3000)
                    else:
                        # the auth page switches views from its alt line, not a nav
                        hook = ".gb-acct-auth__alt" if page == "account-login.html" else nav
                        pg.click(hook + " [data-acct-goto='%s']" % view, timeout=3000)
                    # ⚠ the click leaves the pointer where it landed, and the
                    # incoming view often puts a button right there -- Playwright
                    # DOES honour (hover: hover), so the hover colour gets measured
                    # as if it were the resting one. Park the pointer off-content.
                    pg.mouse.move(0, 0)
                    pg.wait_for_timeout(750)
                except Exception as e:
                    print("SKIP %-20s cannot reach view: %s" % (key, type(e).__name__))
                    pg.close(); continue
            live = pg.evaluate(READ)
            pg.close()

            # index the page by normalised text; same string twice keeps both,
            # paired in document order against the board's top-to-bottom order
            idx = {}
            live.sort(key=lambda e: e["y"])
            for e in live:
                # innerText is already transformed; the board stores the source
                # casing, so fold both ends rather than trusting either
                for k in {norm(e["text"]), norm(e.get("own", ""))}:
                    if k:
                        idx.setdefault(k, []).append(e)
            used = {}

            said = False
            for t in board:
                cand = idx.get(t["key"])
                if not cand:
                    unmatched += 1
                    if SHOW_UNMATCHED:
                        print("   UNPAIRED %-34s %s" % (key, t["text"][:60].replace("\n", " ")))
                    continue
                i = used.get(t["key"], 0)
                if i >= len(cand):
                    unmatched += 1
                    if SHOW_UNMATCHED:
                        print("   UNPAIRED %-34s %s (board has %d, page %d)"
                              % (key, t["text"][:40].replace("\n", " "), i + 1, len(cand)))
                    continue
                used[t["key"]] = i + 1
                e = cand[i]
                pairs += 1
                bad = []
                if t["size"] and abs(e["size"] - t["size"]) > 0.5:
                    bad.append("size %s->%s" % (t["size"], e["size"]))
                if t["lh"] and e["lh"] and abs(e["lh"] - t["lh"]) > 0.6:
                    bad.append("lh %s->%s" % (t["lh"], e["lh"]))
                if abs(e["ls"] - t["ls"]) > 0.05:
                    bad.append("ls %s->%s" % (round(t["ls"], 2), round(e["ls"], 2)))
                if t["weight"] and e["weight"] != t["weight"]:
                    bad.append("weight %s->%s" % (t["weight"], e["weight"]))
                if t["color"] and rgb2hex(e["color"]).lower() != t["color"].lower():
                    bad.append("colour %s->%s" % (t["color"], rgb2hex(e["color"])))
                if bad:
                    if not said:
                        print("\n== %s  (%s, %s @%d)" % (key, stem, page, w)); said = True
                    flag = " [char-overrides]" if t["overrides"] else ""
                    print("   %-42s %s%s" % (t["text"][:42].replace("\n", " "),
                                             "; ".join(bad), flag))
                    diffs += 1
        b.close()
    print("\n%d paired / %d differ / %d board texts unmatched" % (pairs, diffs, unmatched))
    sys.exit(1 if diffs else 0)


main()
