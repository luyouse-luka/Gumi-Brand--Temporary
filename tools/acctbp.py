#!/usr/bin/env python3
"""account.scss breakpoint audit (global rule 18).

Two things go wrong silently and this catches both:
  1. the same property written in two value tiers that overlap -- the winner is
     then source order, so one line's size can come from `narrow` while its
     tracking comes from `tablet`;
  2. a number inside a layout threshold (tight/stack/mid), which overlaps the
     value tiers by definition and drags the order-dependence back in.

Tiers and their ranges, from the mixin block at the top of account.scss:
  mobile <=575   narrow <=767   tablet 768-1280   pc >=1281
  panel-wide >=768                       (spans tablet and pc on purpose)
  tight <=1200   stack <=1024   mid <=991         (layout thresholds)
"""
import re, sys, pathlib

SRC = pathlib.Path(__file__).resolve().parent.parent / "assets" / "account.scss"

RANGE = {"mobile": (0, 575), "narrow": (0, 767), "tablet": (768, 1280),
         "pc": (1281, 99999), "panel-wide": (768, 99999),
         "tight": (0, 1200), "stack": (0, 1024), "mid": (0, 991)}
VALUE_TIERS = ("mobile", "narrow", "tablet", "pc", "panel-wide")
THRESHOLDS = ("tight", "stack", "mid")
# what "carries a number". Arrangement-only properties are allowed anywhere.
NUMERIC = re.compile(
    r"^(font-size|line-height|letter-spacing|width|height|min-width|max-width"
    r"|min-height|max-height|gap|row-gap|column-gap|padding|padding-\w+|margin"
    r"|margin-\w+|top|right|bottom|left|inset|border-radius|border-width"
    r"|flex-basis|font-weight|translate|stroke-width|column-count)$")
# a threshold may still pin a box back to a fixed track; these read as
# arrangement even though they look numeric
ARRANGEMENT_OK = re.compile(r"^(grid-template-\w+|grid-\w+|flex-direction|order|flex)$")

FONT_RE = re.compile(r"@include\s+font\s*\(")
# @mixin font($family, $size, $weight: 400, $lh: null, $ls: null)
FONT_ARGS = ["font-family", "font-size", "font-weight", "line-height", "letter-spacing"]


def font_props(head):
    """The properties `@include font(...)` actually emits, by argument count."""
    m = FONT_RE.search(head)
    if not m:
        return []
    depth, args, buf = 1, [], []
    for ch in head[m.end():]:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                break
        if depth == 1 and ch == ",":
            args.append("".join(buf).strip()); buf = []
        else:
            buf.append(ch)
    args.append("".join(buf).strip())
    args = [a for a in args if a != ""]
    # a trailing `null` is the mixin's own @if guard -- it emits nothing
    props = [p for p, a in zip(FONT_ARGS, args) if a != "null"]
    if len(args) >= 2 and "font-weight" not in props:
        props.append("font-weight")           # the default still lands
    return props


TIER_RE = re.compile(r"@include\s+(mobile|narrow|tablet|pc|panel-wide|tight|stack|mid)\b")
DECL_RE = re.compile(r"^(-{0,2}[a-z][\w-]*)\s*:\s*\S")


def overlaps(a, b):
    (a0, a1), (b0, b1) = RANGE[a], RANGE[b]
    return a0 <= b1 and b0 <= a1


def parse(text):
    """-> list of (selector, prop, tier).

    Scanned by token, not by line: `@include narrow { height: 24px; }` is the
    house style and a line-based reader drops every declaration written that
    way -- which is most of them.
    """
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    text = re.sub(r"//[^\n]*", "", text)
    out, stack, buf = [], [], []
    for ch in text:
        if ch in "{};":
            head = " ".join("".join(buf).split())
            buf = []
            if ch == "{":
                m = TIER_RE.search(head)
                if m:
                    stack.append(("tier", m.group(1)))
                elif head.startswith("@media"):
                    stack.append(("tier", "media"))
                elif head.startswith("@"):
                    stack.append(("tier", "at"))      # @include of a plain mixin, @supports
                else:
                    stack.append(("sel", head))
            elif ch == "}":
                if stack:
                    stack.pop()
            else:                                     # ";"
                sel = " ".join(n for k, n in stack if k == "sel") or "(root)"
                tiers = [n for k, n in stack if k == "tier"]
                tier = tiers[-1] if tiers else "base"
                d = DECL_RE.match(head)
                if d and not head.startswith(("@", "$")):
                    out.append((sel, d.group(1), tier))
                else:
                    # @include font() is how nearly every size in this file is
                    # written; without expanding it the size checks see nothing
                    for prop in font_props(head):
                        out.append((sel, prop, tier))
        else:
            buf.append(ch)
    return out


def main():
    decls = parse(SRC.read_text())
    seen, red = {}, 0
    for sel, prop, tier in decls:
        seen.setdefault((sel, prop), set()).add(tier)

    for (sel, prop), tiers in sorted(seen.items()):
        vt = [t for t in tiers if t in VALUE_TIERS]
        for i, a in enumerate(vt):
            for b in vt[i + 1:]:
                if overlaps(a, b):
                    print("RED  overlapping tiers  %s { %s }  in %s + %s" % (sel, prop, a, b))
                    red += 1

    for sel, prop, tier in decls:
        if tier in THRESHOLDS and NUMERIC.match(prop) and not ARRANGEMENT_OK.match(prop):
            print("RED  number inside a layout threshold  %s { %s }  in %s" % (sel, prop, tier))
            red += 1

    tot = sum(len(v) for v in seen.values())
    print("\n%d declarations / %d red" % (tot, red))
    sys.exit(1 if red else 0)


main()
