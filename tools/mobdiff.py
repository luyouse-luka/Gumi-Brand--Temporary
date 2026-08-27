#!/usr/bin/env python3
"""Match every visible Figma TEXT node on a board to the element that renders it,
then diff the type tokens and the box.

    python3 tools/mobdiff.py [page] [node-file] [origin-id] [width]

Matching is a longest-common-subsequence alignment over document order, NOT a
text lookup: the same string occurs many times on this page (three identical
testimonials, "95%" three times), and a dictionary match pairs them arbitrarily,
which then reports type differences that belong to a different element.

Two collapses happen before matching, or the page side does not line up with the
board side at all:
  * [data-line-reveal] hosts absorb their own subtree -- lineReveal splits copy
    into per-word spans, so the innermost text host is a fragment, not the line.
  * aria-hidden ink-halo copies are dropped -- they duplicate every headline.
Alignment differences are only reported for block-level text, since a Figma text
node inside a centred auto-layout frame reads LEFT while the frame does the centring.
"""
import os, sys, json, re, unicodedata, difflib
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = os.path.expanduser("~/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome")
PAGE = sys.argv[1] if len(sys.argv) > 1 else "index.html"
NODEFILE = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "figma/nodes/228-5932_homepage-mobile.json")
ORIGIN = sys.argv[3] if len(sys.argv) > 3 else "237:13125"
WIDTH = int(sys.argv[4]) if len(sys.argv) > 4 else 390


def norm(s):
    s = unicodedata.normalize("NFKC", s or "")
    s = re.sub(r"[‘’]", "'", s)
    s = re.sub(r"[“”]", '"', s)
    s = re.sub(r"[  ]", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()


d = json.load(open(NODEFILE))
root = list(d["nodes"].values())[0]["document"]


def find(n, tid):
    if n["id"] == tid:
        return n
    for c in n.get("children", []):
        r = find(c, tid)
        if r:
            return r
    return None


org = find(root, ORIGIN) or root
ob = org["absoluteBoundingBox"]
ox, oy = ob["x"], ob["y"]

fig = []


def collect(n, parent=None):
    if n.get("visible") is False:
        return
    if n["type"] == "TEXT":
        bb = n["absoluteBoundingBox"]
        st = n.get("style", {})
        # a text node inside a centred auto-layout frame is centred by the frame
        framed = bool(parent and parent.get("layoutMode")
                      and "CENTER" in (str(parent.get("counterAxisAlignItems")) + str(parent.get("primaryAxisAlignItems"))))
        fig.append({
            "id": n["id"], "text": norm(n.get("characters", "")), "raw": n.get("characters", ""),
            "x": bb["x"] - ox, "y": bb["y"] - oy, "w": bb["width"], "h": bb["height"],
            "fs": st.get("fontSize"), "lh": st.get("lineHeightPx"),
            "ls": st.get("letterSpacing") or 0.0, "fw": st.get("fontWeight"),
            "al": st.get("textAlignHorizontal"), "framed": framed,
            "ov": bool(n.get("characterStyleOverrides") and any(n["characterStyleOverrides"])),
        })
    for c in n.get("children", []):
        collect(c, n)


collect(org)
fig.sort(key=lambda f: (round(f["y"], 1), round(f["x"], 1)))

SETTLE = """
.wowo, .gb-float-art, [data-line-reveal], .gb-line-mask__inner, .gb-ink-halo {
  opacity: 1 !important; transform: none !important; animation: none !important;
}
"""
DUMP = """() => {
  const out = [];
  const sy = window.scrollY;
  const seen = new WeakSet();
  const norm = t => (t || '').replace(/[\\u2028\\u2029]/g, ' ').replace(/\\s+/g, ' ').trim();
  // ink-halo copies duplicate every headline and would double every string;
  // the mobile drawer is a separate board (283:14915), not part of this one
  const skip = el => el.getAttribute('aria-hidden') === 'true'
                  || el.classList.contains('gb-header__panel');
  const text = el => {
    if (skip(el)) return '';
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') return '';
    let t = '';
    for (const n of el.childNodes) {
      if (n.nodeType === 3) t += n.nodeValue;
      else if (n.nodeType === 1) t += ' ' + text(n);
    }
    return norm(t);
  };
  const push = (el, t) => {
    const b = el.getBoundingClientRect();
    const cs = getComputedStyle(el);
    out.push({ text: t, tag: el.tagName.toLowerCase(),
               cls: (el.className || '').toString().trim().split(/\\s+/).filter(c => c.startsWith('gb-')).join(' '),
               x: b.x, y: b.y + sy, w: b.width, h: b.height,
               fs: parseFloat(cs.fontSize), lh: cs.lineHeight, ls: cs.letterSpacing,
               fw: cs.fontWeight, al: cs.textAlign, disp: cs.display });
  };
  for (const el of document.querySelectorAll('body *')) {
    if (seen.has(el) || skip(el)) continue;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') continue;
    const t = text(el);
    if (!t) continue;
    // a line-reveal host owns its whole subtree: lineReveal splits copy into
    // per-word spans, so the innermost text host is a fragment, not the line
    if (el.hasAttribute('data-line-reveal')) {
      el.querySelectorAll('*').forEach(c => seen.add(c));
      push(el, t); continue;
    }
    let inner = false;
    for (const c of el.children) if (text(c) === t) { inner = true; break; }
    if (inner) continue;
    push(el, t);
  }
  out.sort((a, b) => (a.y - b.y) || (a.x - b.x));
  return out;
}"""

with sync_playwright() as p:
    br = p.chromium.launch(executable_path=CHROME)
    pg = br.new_page(viewport={"width": WIDTH, "height": 844})
    pg.goto("file://" + os.path.join(ROOT, PAGE))
    pg.add_style_tag(content=SETTLE)
    pg.wait_for_timeout(1200)
    pg.evaluate("document.fonts.ready")
    pg.wait_for_timeout(400)
    impl = pg.evaluate(DUMP)
    br.close()

for e in impl:
    e["n"] = norm(e["text"])

sm = difflib.SequenceMatcher(None, [f["text"] for f in fig], [e["n"] for e in impl], autojunk=False)
pairs, only_fig, only_impl = [], [], []
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        pairs += [(fig[i1 + k], impl[j1 + k]) for k in range(i2 - i1)]
    else:
        only_fig += fig[i1:i2]
        only_impl += impl[j1:j2]


def px(v):
    if v in (None, "normal"):
        return None
    return float(str(v).rstrip("px"))


ALIGN = {"LEFT": "left", "CENTER": "center", "RIGHT": "right", "JUSTIFIED": "justify"}
print(f"# {PAGE} @ {WIDTH}   board TEXT: {len(fig)}   page text: {len(impl)}   aligned: {len(pairs)}\n")

print("## type-token differences")
n = 0
for f, e in pairs:
    bad = []
    if f["fs"] and abs(e["fs"] - f["fs"]) > 0.51:
        bad.append(f"fs {f['fs']:.2f}->{e['fs']:.2f} ({e['fs']-f['fs']:+.2f})")
    lh = px(e["lh"])
    if f["lh"] and lh and abs(lh - f["lh"]) > 0.51:
        bad.append(f"lh {f['lh']:.2f}->{lh:.2f} ({lh-f['lh']:+.2f})")
    ls = px(e["ls"]) or 0.0
    if abs(ls - f["ls"]) > 0.11:
        bad.append(f"ls {f['ls']:.2f}->{ls:.2f} ({ls-f['ls']:+.2f})")
    if int(e["fw"]) != int(f["fw"] or 400):
        bad.append(f"fw {f['fw']}->{e['fw']}")
    # block-level only: an inline run reports the parent's alignment
    if not f["framed"] and e["disp"] in ("block", "flex", "list-item") and abs(e["w"] - f["w"]) < 4:
        want = ALIGN.get(f["al"], "?")
        got = "left" if e["al"] in ("start", "left") else e["al"]
        if want != got:
            bad.append(f"align {f['al']}->{e['al']}")
    if bad:
        n += 1
        print(f"  {f['id']:38s} {e['cls'][:32]:34s} {'; '.join(bad)}")
        print(f"      {f['raw'][:72]!r}")
print(f"  -> {n} of {len(pairs)}\n")

print("## box-height differences > 2px  (a height step is usually a line-count step)")
n = 0
for f, e in pairs:
    if abs(e["h"] - f["h"]) > 2:
        n += 1
        hard = " HARD-BREAK-IN-BOARD" if "\u2028" in f["raw"] else ""
        print(f"  {f['id']:38s} {e['cls'][:32]:34s} h {f['h']:7.2f} -> {e['h']:7.2f} ({e['h']-f['h']:+.2f}){hard}   {f['raw'][:36]!r}")
print(f"  -> {n} of {len(pairs)}\n")

print("## box-width differences > 2px")
n = 0
for f, e in pairs:
    if abs(e["w"] - f["w"]) > 2:
        n += 1
        print(f"  {f['id']:38s} {e['cls'][:32]:34s} w {f['w']:7.2f} -> {e['w']:7.2f} ({e['w']-f['w']:+.2f})   {f['raw'][:36]!r}")
print(f"  -> {n} of {len(pairs)}\n")

print("## on the board, not on the page")
for f in only_fig:
    print(f"  {f['id']:38s} y={f['y']:9.2f} fs={f['fs']} {f['raw'][:72]!r}")
print(f"  -> {len(only_fig)}\n")

print("## on the page, not on the board")
for e in only_impl:
    print(f"  {e['cls'][:34]:36s} y={e['y']:9.2f} {e['text'][:72]!r}")
print(f"  -> {len(only_impl)}")
