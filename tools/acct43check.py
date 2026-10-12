#!/usr/bin/env python3
"""Task 43 -- a once-only flag must never be a DOM attribute.

The live templates are transcribed from rendered DOM, so `data-acct-watched="1"`
(written by acctForm.watch after it installs the gate) came back in
`snippets/gb-account-modals.liquid` on eight panels and in
`sections/gb-account.liquid` on the details form. On the next load the guard
read its own leftover flag and returned before installing anything: Save stayed
disabled forever, no matter what was picked. Three sibling modules had the same
shape.

Each section therefore does the thing the theme did -- put the flag in the
markup BEFORE the module runs -- and then asserts the feature still works. The
anchor in every section is the untouched state (Save still disabled, quantity
unchanged), or "it works" would read green on a gate that was never armed.
"""
import sys, pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
FLAGS = ["data-acct-watched", "data-acct-bound",
         "data-acct-qty-bound", "data-acct-discount-bound"]

ok = red = 0


def check(label, got, want):
    global ok, red
    if got == want:
        print("ok   %-58s %s" % (label, got)); ok += 1
    else:
        print("RED  %-58s got %r want %r" % (label, got, want)); red += 1


def _chrome():
    hits = sorted((pathlib.Path.home() / ".cache/ms-playwright").glob(
        "chromium-*/chrome-linux64/chrome"))
    if not hits:
        sys.exit("no chromium -- run: npx playwright install chromium")
    return str(hits[-1])


def goto(b, hash_="#detail", width=1440):
    pg = b.new_page(viewport={"width": width, "height": 950})
    pg.goto((ROOT / "account.html").as_uri() + hash_)
    pg.wait_for_timeout(700)
    return pg


# --------------------------------------------------------------------------
# 1 -- the reported bug: Save never un-disables
# --------------------------------------------------------------------------
def run_save_gate(b):
    pg = goto(b)
    # Stamp the flag the way the theme does: in the markup, before the panel is
    # ever opened (modal.open is what calls acctForm.watch).
    pg.evaluate("""()=>{document.querySelector("[data-acct-modal-panel='edit-date']")
                      .setAttribute('data-acct-watched','1')}""")
    pg.evaluate("()=>window.gumiAcct.modal.open('edit-date')")
    pg.wait_for_timeout(500)
    S = "[data-acct-modal-panel='edit-date'] [data-acct-save]"

    # Anchor: an unarmed gate leaves Save enabled, and then "it enables after a
    # change" is true without the gate ever running.
    check("pre-stamped panel: Save starts disabled",
          pg.eval_on_selector(S, "e=>e.disabled"), True)

    pg.fill("#acct-f-date", "25/12/2026")
    pg.wait_for_timeout(300)
    check("pre-stamped panel: Save un-disables on change",
          pg.eval_on_selector(S, "e=>e.disabled"), False)

    # And the gate is really value-based, not a one-way switch.
    pg.fill("#acct-f-date", "19/07/2026")     # back to the markup's value
    pg.wait_for_timeout(300)
    check("pre-stamped panel: Save re-disables when put back",
          pg.eval_on_selector(S, "e=>e.disabled"), True)
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(500)

    # The details form is armed by init(), not by modal.open, so the only honest
    # way to put the flag in front of the module is a fresh node: cloneNode
    # copies attributes and NOT properties, which is exactly the theme's shape.
    # ⚠ Resetting the property on the live form instead would install a second
    # listener and read green either way.
    pg.evaluate("""()=>{const f=document.querySelector('[data-acct-form]').cloneNode(true);
                        f.id='probe-form'; f.setAttribute('data-acct-watched','1');
                        document.body.appendChild(f);
                        window.gumiAcct.form.watch(f);}""")
    D = "#probe-form [data-acct-save]"
    check("pre-stamped details form: Save starts disabled",
          pg.eval_on_selector(D, "e=>e.disabled"), True)
    pg.evaluate("""()=>{const i=document.querySelector('#probe-form [data-acct-field]');
                        i.value=i.value+'x';
                        i.dispatchEvent(new Event('input',{bubbles:true}));}""")
    pg.wait_for_timeout(300)
    check("pre-stamped details form: Save un-disables",
          pg.eval_on_selector(D, "e=>e.disabled"), False)
    pg.close()


# --------------------------------------------------------------------------
# 2 -- nothing writes these flags into the DOM any more
# --------------------------------------------------------------------------
def run_no_dom_flags(b):
    pg = goto(b)
    # Exercise every module that used to stamp one.
    pg.evaluate("()=>window.gumiAcct.modal.open('edit-product')")
    pg.wait_for_timeout(400)
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(400)
    pg.evaluate("()=>{location.hash='#help'}")
    pg.wait_for_timeout(800)
    pg.click("[data-acct-view='help'] [data-acct-accordion] button")
    pg.wait_for_timeout(500)

    for f in FLAGS:
        check("no %s in the DOM" % f,
              pg.evaluate("(f)=>document.querySelectorAll('['+f+']').length", f), 0)
    # Anchor: the flags do exist, as properties -- otherwise the count above is
    # zero because nothing ran at all.
    check("flags live on the elements instead", pg.evaluate(
        "()=>!!document.querySelector('[data-acct-accordion]')._acctBound"), True)
    pg.close()


# --------------------------------------------------------------------------
# 4 -- discount and accordion, the other two that carried a flag
# --------------------------------------------------------------------------
def run_siblings(b):
    pg = goto(b)
    # acctDiscount.bind also runs on modal.open, so stamping the attribute and
    # then opening the panel is the theme's real sequence.
    panel = pg.evaluate("""()=>{const p=[...document.querySelectorAll('[data-acct-modal-panel]')]
        .find(e=>e.querySelector('[data-acct-discount-input]'));
        if(!p) return null;
        p.setAttribute('data-acct-discount-bound','1');
        return p.getAttribute('data-acct-modal-panel');}""")
    check("found a panel with a discount field", panel is not None, True)
    if panel:
        pg.evaluate("(n)=>window.gumiAcct.modal.open(n)", panel)
        pg.wait_for_timeout(500)
        P = "[data-acct-modal-panel='%s'] " % panel
        check("pre-stamped discount: Apply starts disabled",
              pg.eval_on_selector(P + "[data-acct-apply]", "e=>e.disabled"), True)
        pg.fill(P + "[data-acct-discount-input]", "GUMI10")
        pg.wait_for_timeout(300)
        check("pre-stamped discount: Apply un-disables",
              pg.eval_on_selector(P + "[data-acct-apply]", "e=>e.disabled"), False)
        pg.keyboard.press("Escape")
        pg.wait_for_timeout(500)

    pg.evaluate("()=>{location.hash='#help'}")
    pg.wait_for_timeout(800)
    A = "[data-acct-view='help'] [data-acct-accordion] "
    rows = pg.locator(A + "[data-acct-accordion-row], " + A + "details")
    check("help accordion has rows",
          pg.eval_on_selector_all(A + "button", "els=>els.length") > 1, True)

    # acctFaq.bind runs from init(), so the flag can only get in front of it on
    # a fresh node. cloneNode carries attributes, not properties.
    pg.evaluate("""()=>{const r=document.querySelector("[data-acct-view='help'] [data-acct-accordion]")
                        .cloneNode(true);
                        r.id='probe-faq'; r.setAttribute('data-acct-bound','1');
                        r.querySelectorAll("[aria-expanded='true']")
                         .forEach(b=>b.setAttribute('aria-expanded','false'));
                        document.body.appendChild(r);
                        window.gumiAcct.faq.bind(r);}""")
    # ⚠ Asserted as "the guard let it through", not as an open row: the clone
    # sits outside the shell, and _set() flips aria-expanded from slideTo's
    # callback, which needs a real height transition to fire. Before the fix
    # bind() returned on the attribute and never set the property, so this is
    # still the assertion that goes red.
    check("pre-stamped accordion still gets bound",
          pg.evaluate("()=>!!document.getElementById('probe-faq')._acctBound"), True)

    # Anchor: the real accordion still works. ⚠ Row 1 ships open (the board
    # draws it that way), so clicking it CLOSES it -- the click has to land on
    # row 2, same as acctcheck's HELP_OPEN2.
    check("anchor: row 1 ships open",
          pg.eval_on_selector(A + "[data-acct-q]",
                              "e=>e.getAttribute('aria-expanded')"), "true")
    pg.click(A + "#acct-faq-q2")
    pg.wait_for_timeout(700)
    check("anchor: the real accordion moves to row 2", pg.eval_on_selector_all(
        A + "[aria-expanded='true']", "els=>els.map(e=>e.id)"), ["acct-faq-q2"])
    pg.close()


with sync_playwright() as p_:
    b = p_.chromium.launch(executable_path=_chrome())
    run_save_gate(b)
    run_no_dom_flags(b)
    run_siblings(b)
    b.close()

print("\n%d ok / %d red" % (ok, red))
sys.exit(1 if red else 0)
