#!/usr/bin/env python3
"""Rebuild the pre-r60 state so r60check can be shown to fail.

Removes the cart drawer everywhere: markup + trigger on the 11 pages, the SCSS
block, and the three colour tokens it introduced. Backs up first and restores on
`--restore`, then the recompiled css must match byte for byte.

    python3 tools/_reverse_r60.py            # go back
    python3 tools/_reverse_r60.py --restore  # come forward again
"""
import io, os, re, sys, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BAK = "/tmp/claude-1007/-home-ly/c407d37d-7492-4d75-a13f-f42a23eae5d0/scratchpad/r60bak"
PAGES = ["index.html", "pdp.html", "science.html", "reviews.html",
         "how-gumi-works.html", "our-story.html", "faq.html",
         "get-in-touch.html", "referral.html", "privacy-policy.html",
         "shipping.html"]
FILES = PAGES + ["assets/customstyle.scss"]

TRIGGER_NEW = '<a class="gb-header__icon" href="#" data-modal="gb-cart" aria-label="Cart">'
TRIGGER_OLD = '<a class="gb-header__icon" href="#" aria-label="Cart">'


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
    for f in PAGES:
        p = os.path.join(ROOT, f)
        s = io.open(p, encoding="utf-8").read()
        s = s.replace(TRIGGER_NEW, TRIGGER_OLD)
        i = s.find('    <div class="gb-cart" id="gb-cart"')
        assert i >= 0, f + ": no drawer to remove"
        # anchored at line start: '      </div>' contains '    </div>' as a substring
        j = s.index('\n    </div>\n\n', i) + len('\n    </div>\n\n')
        s = s[:i] + s[j:]
        assert 'gb-cart' not in s, f + ": drawer fragments left behind"
        io.open(p, "w", encoding="utf-8").write(s)

    p = os.path.join(ROOT, "assets", "customstyle.scss")
    s = io.open(p, encoding="utf-8").read()
    i = s.index("// ==========================================================================\n// Cart drawer\n")
    j = s.index("// ==========================================================================\n// Motion\n")
    s = s[:i] + s[j:]
    for line in ('$c-blue:        #0374a5;   // 341:42573 only — cart delivery interval + "Continue Shopping"\n',
                 "$c-gray-400:    #808080;   // 341:42573 stepper border / disabled checkout label\n",
                 "$c-gray-150:    #e6e6e6;   // 341:42573 cart line rule / disabled checkout fill\n"):
        assert s.count(line) == 1, "token not found: " + line[:20]
        s = s.replace(line, "")
    assert "gb-cart" not in s, "cart rules left in the scss"
    io.open(p, "w", encoding="utf-8").write(s)
    print("reversed: drawer removed from 11 pages + scss")


if __name__ == "__main__":
    restore() if "--restore" in sys.argv else reverse()
