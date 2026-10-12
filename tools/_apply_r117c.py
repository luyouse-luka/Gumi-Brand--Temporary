#!/usr/bin/env python3
"""Round 117, item 7: the banner reveals before what sits under it.

On the first pass the banner and the modules below it are both in view, so wowo
starts them together -- and the banner is the slower of the two, because its own
media carries delay-in-1 while the modules below it usually carry none. The page
therefore reads bottom-up on phones. Hold everything outside the banner back by
one beat, on that first pass only; scroll-triggered reveals are untouched.
"""
import pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
JS = ROOT / 'assets/main.js'


def sub(old, new):
    t = JS.read_text(encoding='utf-8')
    if t.count(old) != 1:
        sys.exit(f'ABORT anchor {t.count(old)}x\n  {old[:90]!r}')
    JS.write_text(t.replace(old, new, 1), encoding='utf-8')
    print('  ok')


sub("""  var wowo = {
    run: function () {
      var wTop = window.pageYOffset || document.documentElement.scrollTop;
      var wHeight = window.innerHeight;
      var wBottom = wTop + wHeight;
      var els = document.querySelectorAll(".wowo:not(.animated)");
""",
    """  var wowo = {
    // Client r117: on the first pass the banner and the modules under it are
    // both in view, so they start together -- and the banner loses, because its
    // media carries delay-in-1 while the modules below it usually carry none.
    // The phone then reads bottom-up. Hold the rest back by one beat so the
    // banner lands first. Self-chosen value, no board backing -- see the
    // "awaiting design sign-off" list.
    FIRST_HOLD: 400,
    BANNER: ".gb-hero, .gb-page-hero",
    firstRun: true,

    run: function () {
      var wTop = window.pageYOffset || document.documentElement.scrollTop;
      var wHeight = window.innerHeight;
      var wBottom = wTop + wHeight;
      // Held elements are excluded so a scroll landing mid-hold cannot start
      // the same reveal a second time.
      var els = document.querySelectorAll(".wowo:not(.animated):not([data-wowo-hold])");
      var first = this.firstRun;
      this.firstRun = false;
""")

sub("""        if (meTop > wTop - meHeight && meBottom < wBottom + meHeight) {
          this.play(el);
        }
      }
    },

    play: function (el) {
      el.classList.add("animated");
      setTimeout(function () {
        el.classList.remove("wowo", "animated");
      }, 1500);
    },
""",
    """        if (meTop > wTop - meHeight && meBottom < wBottom + meHeight) {
          if (first && el.closest && !el.closest(this.BANNER)) {
            this.hold(el, this.FIRST_HOLD);
          } else {
            this.play(el);
          }
        }
      }
    },

    play: function (el) {
      el.classList.add("animated");
      setTimeout(function () {
        el.classList.remove("wowo", "animated");
      }, 1500);
    },

    hold: function (el, ms) {
      var self = this;
      el.setAttribute("data-wowo-hold", "");
      setTimeout(function () {
        el.removeAttribute("data-wowo-hold");
        self.play(el);
      }, ms);
    },
""")
print('done')
