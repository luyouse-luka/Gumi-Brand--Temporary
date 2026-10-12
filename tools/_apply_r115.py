#!/usr/bin/env python3
"""r115: science CTA, gb-br-wide at every width, rich-table 124, menu opens on
toggle focus. Every replacement asserts its anchor count first."""
import pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
edits = []


def sub(path, old, new, n=1):
    p = ROOT / path
    t = p.read_text()
    got = t.count(old)
    if got != n:
        sys.exit(f'ABORT {path}: anchor x{got}, want x{n}\n---\n{old[:200]}')
    p.write_text(t.replace(old, new, n))
    edits.append(f'{path}  {old.strip().splitlines()[0][:60]}')


S = 'assets/customstyle.scss'

# --- build token ----------------------------------------------------------
sub(S, '$build: "20260908-r113";', '$build: "20260908-r115";')

# --- 2. .gb-br-wide shows at every width ----------------------------------
sub(S, """// The mirror of the above, for copy the two boards break in DIFFERENT places
// rather than one breaking and the other running flat: .gb-dosed__title is
// "One pouch. Once a day. / That's the whole ritual." on 1440 and
// "One pouch. / Once a day. That's / the whole ritual." on 390, so the two
// break points have to be able to hide independently.
.gb-br-wide {
  @include narrow { display: none; }
}""", """// Was the mirror of the above -- a break only the desktop board draws. Client
// r115 wants it at every width, so it hides nowhere and carries no rule at all.
// ⚠ Two consequences: gb-lines' `^^` and `//` now render the same thing, and
// .gb-dosed__title (static build only -- live's copy has no markers) gains a
// fourth break on 390. Nothing else on the site uses the class.""")

# --- 3. rich-table label column -------------------------------------------
sub(S, """  // only grows the fill side instead of stretching both.
  th:first-child { width: 88px; }""", """  // only grows the fill side instead of stretching both.
  // Client r115: 124, not the board's 88.
  th:first-child { width: 124px; }""")

# --- 1. science CTA -------------------------------------------------------
sub(S, """  // Client r96. The base card is 16 at every width; only the tight board opens up.
  .gb-science-card { gap: 22px; }
}""", """  // Client r96. The base card is 16 at every width; only the tight board opens up.
  .gb-science-card { gap: 22px; }

  // 48 - the gaps above. 0-2-0, so these beat the base tier no matter the order.
  .gb-science__cta { margin-top: 26px; }                          // 22 + 26
  @include narrow { .gb-science__cta { margin-top: 0; } }         // 48 already
  @include tablet { .gb-science__cta { margin-top: fluid(16px, 26px); } }
}""")

sub(S, """  @include narrow { gap: 31px; }
  @include tablet { gap: fluid(31px, 24px); }
}

.gb-science-card {""", """  @include narrow { gap: 31px; }
  @include tablet { gap: fluid(31px, 24px); }
}

// Client r115: a CTA 48px under the card grid. It is a flex child of __inner,
// so __inner's own gap already sits above it -- what is set here is only the
// remainder. ⚠ Move either gap and these have to move with it; the --tight
// tier restates all three.
.gb-science__cta {
  margin-top: 0;                                  // base gap is already 48
  @include narrow { margin-top: 2px; }            // 46 + 2
  @include tablet { margin-top: fluid(2px, 0px); }
}

.gb-science-card {""")

# --- 4. menu opens as soon as Tab reaches the toggle ----------------------
J = 'assets/main.js'
sub(J, """      toggle.addEventListener("click", function () {
        self.set(!el.classList.contains("is-open"));
      });""", """      toggle.addEventListener("click", function () {
        self.set(!el.classList.contains("is-open"));
      });

      // Tab landing on the toggle opens the menu, so the next Tab walks its
      // links instead of a shut panel. Pointer focus must NOT open it: focus
      // fires before click, and the click would toggle it straight back shut.
      // :focus-visible is the only thing that tells the two apart.
      toggle.addEventListener("focus", function () {
        if (self.skipFocusOpen) { return; }
        if (toggle.matches && toggle.matches(":focus-visible")) { self.set(true); }
      });

      // .focus() dispatches synchronously, so the flag needs no timer. Without
      // it every close that hands focus back to the toggle reopens the menu --
      // programmatic focus keeps whatever :focus-visible state came before it.
      var refocus = function () {
        self.skipFocusOpen = true;
        toggle.focus();
        self.skipFocusOpen = false;
      };""")

sub(J, """        close.addEventListener("click", function () { self.set(false); toggle.focus(); });""",
       """        close.addEventListener("click", function () { self.set(false); refocus(); });""")

sub(J, """        self.set(false);
        toggle.focus();      // else focus is stranded on what just slid away""",
       """        self.set(false);
        refocus();           // else focus is stranded on what just slid away""")

sub(J, """  var header = {
    lockToken: 0,""", """  var header = {
    lockToken: 0,
    skipFocusOpen: false,""")

print('\n'.join(edits))
print(f'\n{len(edits)} edits applied')
