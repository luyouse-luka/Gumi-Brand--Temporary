#!/usr/bin/env python3
"""Rebuild the pre-r61 state so r61check can be shown to fail.

Undoes the round's five changes across scss, js and the 11 mounted pages.
Backs up first; `--restore` brings it all forward again and the recompiled css
must then match byte for byte.

    python3 tools/_reverse_r61.py            # go back
    python3 tools/_reverse_r61.py --restore  # come forward again
"""
import io, os, re, sys, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BAK = "/tmp/claude-1007/-home-ly/c407d37d-7492-4d75-a13f-f42a23eae5d0/scratchpad/r61bak"
PAGES = ["index.html", "pdp.html", "science.html", "reviews.html",
         "how-gumi-works.html", "our-story.html", "faq.html",
         "get-in-touch.html", "referral.html", "privacy-policy.html",
         "shipping.html"]
FILES = PAGES + ["assets/customstyle.scss", "assets/main.js"]

# (current, previous) -- applied in reverse
SCSS = [
("""@mixin tablet { @media (min-width: #{$bp-narrow + 1px}) and (max-width: $bp-tablet) { @content; } }
// r59: the promo card keeps its two-column layout all the way down to 768 (it
// is scaled, not reflowed -- see --pp-k), so it needs one query that spans
// tablet and pc rather than the two separate tiers.
@mixin panel-wide { @media (min-width: #{$bp-narrow + 1px}) { @content; } }""",
 """@mixin tablet { @media (min-width: #{$bp-narrow + 1px}) and (max-width: $bp-tablet) { @content; } }"""),

("""  // Client-set (r59): row layout from 768 up. 768-1109 has no board, so instead
  // of reflowing the desktop card into a tier nobody drew, it is scaled as one
  // piece -- 1 at >=1110 (the first width that fits 1062 inside the 24 gutters),
  // and the fraction that fits below that. Every number inside the card stays
  // the board's own. 48 is the wrap's two 24 gutters.
  // ⚠ zoom, not transform: transform would leave the card's old box in the
  // layout and break the centring. A browser without zoom falls back to
  // max-width:100% -- squashed, not broken.
  --pp-k: calc(min(1062px, 100vw - 48px) / 1062px);

  position: fixed;""",
 """  position: fixed;"""),

("""  // Client-set: full-screen is for phones only; from 768 up it is the desktop
  // two-column card, scaled by --pp-k. Decision AT is closed by this -- the
  // earlier answer (show the 390 phone board at its own size in 768-1280) is
  // withdrawn.
  @include panel-wide {
    flex-direction: row;
    justify-content: flex-start;
    width: 1062px;
    height: 528px;
    max-width: 100%;
    max-height: 100%;
    border-radius: $r-xl;
    zoom: var(--pp-k);
  }
}""",
 """  @include tablet {
    width: 390px;
    height: 744px;
    max-height: 100%;
    border-radius: $r-xl;
  }

  @include pc {
    flex-direction: row;
    justify-content: flex-start;
    width: 1062px;
    height: 528px;
    max-width: 100%;
    max-height: 100%;
    border-radius: $r-xl;
  }
}"""),

("""  @include panel-wide {
    order: 0;
    width: 531px;""",
 """  @include tablet { --sc-w: 144.64px; }

  @include pc {
    order: 0;
    width: 531px;"""),

("""  width: 18px;            // client r59, board says 16
  height: 20px;""",
 """  width: 16px;
  height: 20px;"""),

("""  gap: 6px;               // client r59, board says 4
}""",
 """  gap: 4px;
}"""),

("""  gap: 10px;              // client r59, board says 8
}""",
 """  gap: 8px;
}"""),

("""  padding: 24px 20px;

  @include narrow { padding: 26px 20px; }   // client r59
}""",
 """  padding: 24px 20px;
}"""),

("""  // Opens upward when the list would fall past whatever clips it; the entry
  // offset mirrors with it so the list still slides out of the trigger.
  .gb-select.is-up & {
    top: auto;
    bottom: calc(100% + 4px);
    transform: translateY(4px);
  }

  .gb-select.is-up.is-open & { transform: none; }
}""", "}"),

("""
  // 12 up, not 14: the trigger's line box overhangs the field by 10 at the top
  // and 12 at the bottom (22 content box, 24 line box).
  &.is-up .gb-select__list { bottom: calc(100% + 12px); }
}""", "\n}"),
]

JS = [
("""      // Variants that draw no box of their own, because something around them
      // already does: "bare" is the phone field's country code (.gb-field__phone
      // has the border), "inline" is the cart's delivery interval (it is a run of
      // text inside a sentence).
      var variant = native.getAttribute("data-select") || "";
      var boxless = variant === "bare" || variant === "inline";
      var aria = native.getAttribute("aria-label");

      var wrap = document.createElement("div");
      wrap.className = "gb-select" + (variant ? " gb-select--" + variant : "");""",
 """      var bare = native.getAttribute("data-select") === "bare";
      var aria = native.getAttribute("aria-label");

      var wrap = document.createElement("div");
      wrap.className = bare ? "gb-select gb-select--bare" : "gb-select";"""),

("""      btn.className = boxless ? "gb-select__button"
                              : "gb-field__input gb-field__input--select gb-select__button";""",
 """      btn.className = bare ? "gb-select__button"
                           : "gb-field__input gb-field__input--select gb-select__button";"""),

("""        // currentColor, not #4d4d4d: both existing triggers compute to that anyway
        // (.gb-field__input and --bare are both $c-gray-700), and the cart's
        // inline variant needs the chevron to follow its own blue.
        '<path d="M5 7.5L10 12.5L15 7.5" stroke="currentColor" stroke-width="1.667" ' +""",
 """        '<path d="M5 7.5L10 12.5L15 7.5" stroke="#4d4d4d" stroke-width="1.667" ' +"""),

("""      box.wrap.classList.remove("is-up");
      box.wrap.classList.add("is-open");""",
 """      box.wrap.classList.add("is-open");"""),

("""      // AFTER move(): its scrollIntoView can scroll an ancestor out from under a
      // measurement taken before it. A list that would fall past whatever clips
      // it (the cart drawer's scroll area, else the viewport) opens upwards.
      this.move(box, box.native.selectedIndex);
      if (this.wouldOverflow(box)) { box.wrap.classList.add("is-up"); }
      box.list.focus();""",
 """      this.move(box, box.native.selectedIndex);
      box.list.focus();"""),
]


def strip_helpers(s):
    i = s.index("    // Where the list would end up, computed WITHOUT reading its own rect")
    j = s.index("    // Bottom edge of the nearest ancestor that actually clips, or the viewport.")
    k = s.index("\n    },\n", j) + len("\n    },\n")
    return s[:i] + s[k:]


def backup():
    if not os.path.isdir(BAK):
        os.makedirs(BAK)
    for f in FILES:
        dst = os.path.join(BAK, f.replace("/", "__"))
        if not os.path.exists(dst):
            shutil.copy2(os.path.join(ROOT, f), dst)


def restore():
    for f in FILES:
        shutil.copy2(os.path.join(BAK, f.replace("/", "__")), os.path.join(ROOT, f))
    print("restored", len(FILES), "files")


def reverse():
    backup()
    for path, pairs in (("assets/customstyle.scss", SCSS), ("assets/main.js", JS)):
        p = os.path.join(ROOT, path)
        s = io.open(p, encoding="utf-8").read()
        for new, old in pairs:
            assert s.count(new) == 1, "%s: %d hits for %r" % (path, s.count(new), new[:50])
            s = s.replace(new, old)
        if path.endswith(".js"):
            s = strip_helpers(s)
        io.open(p, "w", encoding="utf-8").write(s)

    # 9 more blocks were widened wholesale
    p = os.path.join(ROOT, "assets", "customstyle.scss")
    s = io.open(p, encoding="utf-8").read()
    i = s.index(".gb-promo-panel {")
    j = s.index("// ==========================================================================\n// Cart drawer")
    blk = s[i:j].replace("@include panel-wide {", "@include pc {")
    s = s[:i] + blk + s[j:]
    assert "panel-wide" not in s, "panel-wide left behind"
    io.open(p, "w", encoding="utf-8").write(s)

    # the interval goes back to a plain button carrying the board's own chevron
    src = io.open(os.path.join(ROOT, "figma", "assets-raw", "icons",
                               "desktop-cart-icon-6.svg"), encoding="utf-8").read()
    d = re.findall(r'<path d="([^"]+)"', src)[0]
    chev = ('<svg aria-hidden="true" viewBox="0 0 16 16" fill="none" '
            'xmlns="http://www.w3.org/2000/svg"><path d="%s" stroke="currentColor" '
            'stroke-width="1.33333" stroke-linecap="round" stroke-linejoin="round"/></svg>' % d)
    pat = re.compile(
        r'<select class="gb-cart-item__interval"[^>]*>\s*(?:<option[^>]*>[^<]*</option>\s*)+</select>')
    for f in PAGES:
        p = os.path.join(ROOT, f)
        s = io.open(p, encoding="utf-8").read()
        n = len(pat.findall(s))
        assert n == 2, "%s: %d intervals" % (f, n)
        seen = []
        def sub(m):
            seen.append(1)
            label = "4 Weeks" if len(seen) == 1 else "One Time Purchase"
            return ('<button class="gb-cart-item__interval" type="button">%s%s</button>'
                    % (label, chev))
        io.open(p, "w", encoding="utf-8").write(pat.sub(sub, s))
    print("reversed: scss + js + 11 pages")


if __name__ == "__main__":
    restore() if "--restore" in sys.argv else reverse()
