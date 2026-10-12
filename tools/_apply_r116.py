#!/usr/bin/env python3
"""Round 116 edits. Every replacement asserts its anchor count first.

1  $build -> 20260908-r116
2  .gb-highlight-card__media:has(img) drops the grey placeholder -- it is what
   the rounded corners anti-alias into the edge (hairline on the green card).
3  main.js: Tab runs toggle -> menu -> rest of the bar -> page.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCSS = ROOT / 'assets/customstyle.scss'
JS = ROOT / 'assets/main.js'


def sub(path, old, new, n=1):
    txt = path.read_text(encoding='utf-8')
    got = txt.count(old)
    if got != n:
        sys.exit(f'ABORT {path.name}: anchor found {got}x, expected {n}\n  {old[:90]!r}')
    path.write_text(txt.replace(old, new, n), encoding='utf-8')
    print(f'  ok  {path.name}: {n} replacement(s)')


print('1. $build')
sub(SCSS, '$build: "20260908-r115";', '$build: "20260908-r116";')

print('2. highlight-card media hairline')
sub(SCSS,
    """  img, video, picture { @include cover-img; }
}

// Scalloped lip along the bottom of the image, in the card's own green.""",
    """  // The grey placeholder sits under the photo inside the same clip box, so the
  // rounded corners anti-alias it into the edge -- a pale hairline on the green
  // card (worst corner pixel luminance 91 against the card's 65). Live fills
  // this with an <img>; the board ships a flat grey box, so the static site
  // never matches and keeps the placeholder.
  &:has(img) { background: none; }

  img, video, picture { @include cover-img; }
}

// Scalloped lip along the bottom of the image, in the card's own green.""")

print('3. tab order: menu before the rest of the bar')
sub(JS,
    """      el.addEventListener("focusout", function (e) {
        // A null relatedTarget is the browser chrome, or a click on dead space
        // inside the panel; neither means the user has left the menu.
        if (e.relatedTarget && !el.contains(e.relatedTarget)) { self.set(false); }
      });
    },""",
    """      el.addEventListener("focusout", function (e) {
        // A null relatedTarget is the browser chrome, or a click on dead space
        // inside the panel; neither means the user has left the menu.
        if (e.relatedTarget && !el.contains(e.relatedTarget)) { self.set(false); }
      });

      // The panel is the last child of <header>, so in source order the bar's
      // own controls (logo, Shop now, account, cart) sit between the toggle and
      // the menu. Reroute the two seams so Tab runs
      //   toggle -> menu -> rest of the bar -> page.
      // Only rendered stops count: the other breakpoint's list is display:none
      // on an ancestor, which leaves each link's own computed display intact --
      // getClientRects() is the one test that sees through that.
      var bar = el.querySelector(".gb-header__bar");
      var shown = function (root, skip) {
        var all = root.querySelectorAll(FOCUSABLE), out = [];
        for (var i = 0; i < all.length; i++) {
          if (all[i] !== skip && all[i].getClientRects().length) { out.push(all[i]); }
        }
        return out;
      };
      el.addEventListener("keydown", function (e) {
        if (e.key !== "Tab" || !el.classList.contains("is-open")) { return; }
        // The phone drawer covers the bar and inerts it: there is no second
        // group to interleave, and the panel already holds every stop.
        if (!panel || !bar || bar.hasAttribute("inert")) { return; }
        var inPanel = shown(panel), inBar = shown(bar, toggle);
        if (!inPanel.length || !inBar.length) { return; }
        var last = inPanel[inPanel.length - 1], a = document.activeElement;
        // toggle.focus() re-enters the focus handler, but set() early-returns
        // on an unchanged state, so reopening here is a no-op.
        if (!e.shiftKey && a === toggle) { e.preventDefault(); inPanel[0].focus(); }
        else if (!e.shiftKey && a === last) { e.preventDefault(); inBar[0].focus(); }
        else if (e.shiftKey && a === inPanel[0]) { e.preventDefault(); toggle.focus(); }
        else if (e.shiftKey && a === inBar[0]) { e.preventDefault(); last.focus(); }
      });
    },""")
print('done')
