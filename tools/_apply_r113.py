#!/usr/bin/env python3
"""r113: footer link hover colour, and the menu's tab order."""
import pathlib, sys

SCSS = pathlib.Path('assets/customstyle.scss')
JS = pathlib.Path('assets/main.js')


def sub(text, old, new, n=1, label=''):
    got = text.count(old)
    if got != n:
        sys.exit(f'ABORT [{label}]: anchor found {got}x, expected {n}\n---\n{old}\n---')
    return text.replace(old, new, n)


s = SCSS.read_text(encoding='utf-8')
s = sub(s, '$build: "20260908-r112";', '$build: "20260908-r113";', 1, 'build')

# r86 dropped the sliding underline from all four link users on the grounds that
# each already changed colour. True of the header pair on cream; false here --
# $c-lime-100 -> $c-white on $c-green-900 is a change nobody can see.
s = sub(s,
        """  @include hover { color: $c-white; }
}

.gb-footer__social {""",
        """  // r86 took the underline off on the grounds that the colour change carried
  // the hover on its own. It does not here: #f4fce7 -> #ffffff on #004128 is
  // invisible. The brand lime is the one accent the dark footer already uses.
  @include hover { color: $c-lime; }
}

.gb-footer__social {""", 1, 'footer link hover')

s = sub(s,
        """  // Bare <a> in the board with no class of their own; hover matches footer__link
  a {
    transition: trans(color);

    @include hover { color: $c-white; }
  }""",
        """  // Bare <a> in the board with no class of their own; hover matches footer__link
  a {
    transition: trans(color);

    @include hover { color: $c-lime; }
  }""", 1, 'legal link hover')

SCSS.write_text(s, encoding='utf-8')

j = JS.read_text(encoding='utf-8')

j = sub(j,
        """      var close = el.querySelector(".gb-header__panel-close");
      if (close) {
        close.addEventListener("click", function () { self.set(false); });
      }

      document.addEventListener("keydown", function (e) {
        if (e.key === "Escape") self.set(false);
      });""",
        """      var close = el.querySelector(".gb-header__panel-close");
      if (close) {
        close.addEventListener("click", function () { self.set(false); toggle.focus(); });
      }

      document.addEventListener("keydown", function (e) {
        if (e.key !== "Escape" || !el.classList.contains("is-open")) { return; }
        self.set(false);
        toggle.focus();      // else focus is stranded on what just slid away
      });""", 1, 'escape + close focus')

j = sub(j,
        """      var items = el.querySelectorAll("[data-collapsible]");
      for (var i = 0; i < items.length; i++) {
        (function (item) {
          var btn = item.querySelector(".gb-header__link");
          if (!btn) return;
          btn.addEventListener("click", function () {
            var open = item.classList.toggle("is-open");
            btn.setAttribute("aria-expanded", open ? "true" : "false");
          });
        })(items[i]);
      }
    },
""",
        """      var items = el.querySelectorAll("[data-collapsible]");
      for (var i = 0; i < items.length; i++) {
        (function (item) {
          var btn = item.querySelector(".gb-header__link");
          if (!btn) return;
          btn.addEventListener("click", function () {
            self.expand(item, !item.classList.contains("is-open"));
          });
        })(items[i]);
      }

      // Keyboard reveal. The panel and each sublist are shut by geometry (a 0fr
      // grid row, translateX on the drawer), never by display, so everything
      // inside keeps its place in the tab order while invisible -- measured 6
      // dead stops on desktop, 19 in the phone drawer. Open what the focus lands
      // in rather than skipping it: the menu is meant to be reachable by Tab.
      var panel = el.querySelector(".gb-header__panel");
      el.addEventListener("focusin", function (e) {
        var sub = e.target.closest && e.target.closest(".gb-header__sublist");
        var item = sub && sub.closest("[data-collapsible]");
        if (item) { self.expand(item, true); }
        if (panel && panel.contains(e.target)) { self.set(true); }
      });
      el.addEventListener("focusout", function (e) {
        // A null relatedTarget is the browser chrome, or a click on dead space
        // inside the panel; neither means the user has left the menu.
        if (e.relatedTarget && !el.contains(e.relatedTarget)) { self.set(false); }
      });
    },

    expand: function (item, open) {
      item.classList.toggle("is-open", open);
      var btn = item.querySelector(".gb-header__link");
      if (btn) { btn.setAttribute("aria-expanded", open ? "true" : "false"); }
    },
""", 1, 'focus handlers + expand')

j = sub(j,
        """    set: function (open) {
      // Measure the real scrollbar width while it is still on screen: the lock
      // below removes it and the viewport would widen by that much, shunting the
      // page sideways. The is-menu-open rule pads the freed width back in.
      if (open) {
        var scrollbarW = window.innerWidth - document.documentElement.clientWidth;
        document.documentElement.style.setProperty("--scrollbar-w", scrollbarW + "px");
      }
      var wasOpen = this.el.classList.contains("is-open");
      this.el.classList.toggle("is-open", open);""",
        """    set: function (open) {
      var wasOpen = this.el.classList.contains("is-open");
      // focusin fires on every Tab step inside an open panel. Re-running the
      // open path would remeasure --scrollbar-w with the bar already locked --
      // it reads 0 there, the compensation padding drops and the page steps
      // sideways.
      if (open === wasOpen) { return; }
      // Measure the real scrollbar width while it is still on screen: the lock
      // below removes it and the viewport would widen by that much, shunting the
      // page sideways. The is-menu-open rule pads the freed width back in.
      if (open) {
        var scrollbarW = window.innerWidth - document.documentElement.clientWidth;
        document.documentElement.style.setProperty("--scrollbar-w", scrollbarW + "px");
      }
      this.el.classList.toggle("is-open", open);""", 1, 'set guard')

j = sub(j,
        """      var token = ++this.lockToken;
      if (open) {
        document.documentElement.classList.add("is-menu-open");
        document.body.classList.add("is-menu-open");
        return;
      }""",
        """      // The phone drawer is fixed and full-viewport, so it covers the bar while
      // the bar's own links stay tabbable behind it -- 4 more dead stops. Read
      // the panel's used position rather than repeat the breakpoint here.
      var panel = this.el.querySelector(".gb-header__panel");
      var bar = this.el.querySelector(".gb-header__bar");
      var covered = !!(panel && getComputedStyle(panel).position === "fixed");
      var token = ++this.lockToken;
      if (open) {
        if (bar && covered) {
          // Opened from the bar (a click on the toggle): hand focus to the
          // drawer BEFORE inerting the bar, or the browser drops it to <body>.
          if (bar.contains(document.activeElement)) {
            var into = panel.querySelector(".gb-header__panel-close");
            if (into) { into.focus(); }
          }
          bar.setAttribute("inert", "");
        }
        document.documentElement.classList.add("is-menu-open");
        document.body.classList.add("is-menu-open");
        return;
      }
      if (bar) { bar.removeAttribute("inert"); }""", 1, 'bar inert')

j = sub(j,
        """      // Token, not a stored timer id: reopening mid-exit must not let the stale
      // callback unlock the drawer that replaced this one.
      var panel = this.el.querySelector(".gb-header__panel");
      var ms = (wasOpen && panel) ? modalExitMs(panel) : 0;""",
        """      // Token, not a stored timer id: reopening mid-exit must not let the stale
      // callback unlock the drawer that replaced this one.
      var ms = (wasOpen && panel) ? modalExitMs(panel) : 0;""", 1, 'panel hoisted')

JS.write_text(j, encoding='utf-8')
print('r113 applied')
