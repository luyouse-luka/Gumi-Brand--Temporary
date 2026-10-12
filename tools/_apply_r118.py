#!/usr/bin/env python3
"""Round 118: close() works on a dialog that arrived already open.

modal.close() guards on `this.current`, which only open() ever sets. A dialog
whose markup ships is-open therefore cannot be closed at all -- overlay, close
button and Escape are equally dead. Live hits this the moment the last cart line
is removed: cart-items-component replays <template id="empty-cart-template">,
whose .gb-cart carries is-open and whose overlay is wired to OUR
[data-modal-close] (the section's other two branches use the theme's own close
command instead -- three branches, two wirings).

Because that template is injected at runtime, a one-off scan in init() would
miss it; the fallback belongs in close() and in the key handler.
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


print('1. key handler no longer requires `current`')
sub("""      document.addEventListener("keydown", function (e) {
        if (!self.current) return;
        if (e.key === "Escape") { self.close(); return; }
        if (e.key === "Tab") self.trap(e);
      });""",
    """      document.addEventListener("keydown", function (e) {
        if (e.key !== "Escape" && e.key !== "Tab") { return; }
        // Not `current` alone: a dialog that arrived already open never set it.
        var el = self.current || self.showing();
        if (!el) { return; }
        if (e.key === "Escape") { self.close(); return; }
        self.trap(e, el);
      });""")

print('2. close() falls back to whatever of ours is on screen')
sub("""    close: function () {
      var el = this.current;
      if (!el) return;""",
    """    close: function () {
      var el = this.current || this.showing();
      if (!el) return;""")

print('3. showing()')
sub("""    // A token rather than a stored timer id: open() can land inside the wait, and
    // the stale callback must not unlock the modal that replaced this one.""",
    """    // A dialog of ours that is on screen without having gone through open().
    // Two conditions, both load-bearing:
    //   [data-modal-close] inside -- the test for "ours to drive". The live cart
    //     drawer also ships is-open, but two of its three branches wire the
    //     overlay to the theme's own close command; adopting those would have us
    //     fight Horizon over the same drawer.
    //   getClientRects()          -- it has to actually be on screen. That same
    //     drawer sits inside a <dialog> that decides whether it shows, so the
    //     class alone would match a shut drawer and close something invisible.
    showing: function () {
      var all = document.querySelectorAll('[role="dialog"].is-open');
      for (var i = 0; i < all.length; i++) {
        if (all[i].querySelector("[data-modal-close]") && all[i].getClientRects().length) {
          return all[i];
        }
      }
      return null;
    },

    // A token rather than a stored timer id: open() can land inside the wait, and
    // the stale callback must not unlock the modal that replaced this one.""")

print('4. trap() takes the dialog rather than reading current')
sub("""    trap: function (e) {
      var f = this.current.querySelectorAll(FOCUSABLE);""",
    """    trap: function (e, el) {
      var f = (el || this.current).querySelectorAll(FOCUSABLE);""")
print('done')
