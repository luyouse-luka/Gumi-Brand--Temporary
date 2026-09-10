#!/usr/bin/env python3
"""account modal infrastructure checks: open, focus, Escape, return focus, lock.

Every [data-acct-modal] trigger on the page is exercised -- the list is read from
the DOM rather than hard-coded, so a trigger added by a later task is covered the
moment it lands, and a panel that was never built shows up as a red here instead
of as a dead button on the page.

⚠ The scroll lock reuses the site's own is-modal-open, not a second lock class.
Two things in customstyle.scss are load-bearing and would be lost by rolling a
parallel one (both are re-asserted below so a rewrite cannot drop them):
  body gets overflow-x:clip / overflow-y:visible, NOT hidden -- hidden makes body
    the sticky header's scrollport and .gb-acct-header drops out of the viewport
  padding-right lands on html ONLY -- padding both spends the freed scrollbar
    width twice and pulls the centred layout left by half a scrollbar

⚠ Headless chromium draws overlay scrollbars, so the real "does the page shift"
test cannot run here: it aborts loudly rather than reporting green. The CSS
mechanism itself is still checked by feeding --scrollbar-w a synthetic value.
"""
import sys, pathlib, datetime
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = pathlib.Path.home() / ".cache/ms-playwright/chromium-1217/chrome-linux64/chrome"

PAGE = "account.html"
WIDTHS = (390, 1440)

ok = 0
red = 0
aborted = []


def good(msg):
    global ok
    ok += 1


def bad(msg):
    global red
    red += 1
    print("RED  " + msg)


# Two triggers only exist in a state Task 7 added, so the judge has to put the
# card into that state before claiming the button is missing.
NEEDS_STATE = {
    "restart": ("data-acct-sub-state", "cancelled"),
    "discount-applied": ("data-acct-discount", "applied"),
}
BASE_STATE = (("data-acct-sub-state", "active"), ("data-acct-discount", "none"))


def set_state(pg, pairs):
    pg.evaluate("ps=>{const e=document.querySelector('.gb-acct-detail');"
                "if(e)ps.forEach(p=>e.setAttribute(p[0],p[1]))}", [list(p) for p in pairs])
    pg.wait_for_timeout(450)


def reach_detail(pg, w):
    """Most triggers live in the detail view; get there the way a user does."""
    nav = ".gb-acct-nav" if w > 767 else ".gb-acct-list"
    pg.click(nav + " [data-acct-goto='subscriptions']", timeout=2000)
    pg.wait_for_timeout(450)
    pg.click("[data-acct-view='subscriptions'] .gb-acct-sub__cta[data-acct-goto='detail']",
             timeout=2000)
    pg.wait_for_timeout(450)


def run_width(b, w):
    label = "%s@%d" % (PAGE, w)
    pg = b.new_page(viewport={"width": w, "height": 900})
    pg.goto((ROOT / PAGE).as_uri())
    pg.wait_for_timeout(400)

    # -- the module has to exist and be reachable before anything else is claimed
    api = pg.evaluate("()=>{const m=window.gumiAcct&&window.gumiAcct.modal;return m?"
                      "['open','close','isOpen'].every(k=>typeof m[k]==='function'):false}")
    if not api:
        bad("%s gumiAcct.modal missing open/close/isOpen -- nothing else can be checked"
            % label)
        pg.close()
        return

    reach_detail(pg, w)

    # Only the triggers that sit in the detail view: this loop's anchor is "the
    # button is on screen there", which a trigger living inside another panel
    # (the shipping flow chains three) can never satisfy. Those are driven by
    # check_shipping instead.
    names = pg.evaluate(
        "()=>[...new Set([...document.querySelectorAll("
        "\"[data-acct-view='detail'] [data-acct-modal]\")]"
        ".map(e=>e.getAttribute('data-acct-modal')))]")
    if not names:
        bad("%s no [data-acct-modal] triggers found -- wrong page or wrong view" % label)
        pg.close()
        return

    # ...but a trigger anywhere on the page still has to point at a real panel,
    # or an in-panel button is a dead end that the loop above no longer sees.
    orphans = pg.evaluate(
        "()=>[...new Set([...document.querySelectorAll('[data-acct-modal]')]"
        ".map(e=>e.getAttribute('data-acct-modal')))]"
        ".filter(n=>!document.querySelector("
        "\".gb-acct-modal[data-acct-modal-panel='\"+n+\"']\"))")
    if orphans:
        bad("%s [data-acct-modal] with no panel: %s" % (label, ", ".join(sorted(orphans))))
    else:
        good(label)

    for name in names:
        trig = "[data-acct-view='detail'] [data-acct-modal='%s']" % name
        panel = ".gb-acct-modal[data-acct-modal-panel='%s']" % name
        tag = "%s [%s]" % (label, name)

        set_state(pg, [NEEDS_STATE[name]] if name in NEEDS_STATE else BASE_STATE)

        # anchor: the trigger must be on screen, or every assertion below is
        # about a button nobody can press (global rule 6)
        if not pg.evaluate("s=>{const e=document.querySelector(s);"
                           "return !!(e&&e.getClientRects().length)}", trig):
            bad("%s trigger not visible in the detail view" % tag)
            continue
        good(tag)

        if not pg.evaluate("s=>!!document.querySelector(s)", panel):
            bad("%s no panel [data-acct-modal-panel='%s']" % (tag, name))
            continue
        good(tag)

        pg.click(trig, timeout=2000)
        pg.wait_for_timeout(450)

        st = pg.evaluate("""s=>{const p=document.querySelector(s[0]);
            const back=p&&p.querySelector('.gb-acct-modal__backdrop');
            const box=p&&p.querySelector('.gb-acct-modal__panel');
            const a=document.activeElement;
            return {open:!!(p&&p.classList.contains('is-open')&&!p.hidden),
                    shown:!!(box&&box.getClientRects().length),
                    backdrop:!!(back&&back.getClientRects().length),
                    focusInside:!!(p&&a&&p.contains(a)),
                    role:p?p.getAttribute('role'):null,
                    modalAttr:p?p.getAttribute('aria-modal'):null,
                    htmlLocked:document.documentElement.classList.contains('is-modal-open'),
                    bodyLocked:document.body.classList.contains('is-modal-open'),
                    headerTop:Math.round(document.querySelector('.gb-acct-header')
                              .getBoundingClientRect().top),
                    bodyOX:getComputedStyle(document.body).overflowX,
                    bodyOY:getComputedStyle(document.body).overflowY,
                    htmlOY:getComputedStyle(document.documentElement).overflowY,
                    bodyPad:getComputedStyle(document.body).paddingRight}}""", [panel])

        for key, want in (("open", True), ("shown", True), ("backdrop", True),
                          ("focusInside", True), ("htmlLocked", True), ("bodyLocked", True)):
            if st[key] is want:
                good(tag)
            else:
                bad("%s %s=%s want %s" % (tag, key, st[key], want))

        if st["role"] == "dialog" and st["modalAttr"] == "true":
            good(tag)
        else:
            bad("%s panel is role=%s aria-modal=%s, want dialog/true"
                % (tag, st["role"], st["modalAttr"]))

        # the two traps the site's own lock already solved
        if st["htmlOY"] == "hidden":
            good(tag)
        else:
            bad("%s html overflow-y=%s while open, want hidden" % (tag, st["htmlOY"]))
        if st["bodyOY"] == "visible" and st["bodyOX"] == "clip":
            good(tag)
        else:
            bad("%s body overflow=%s/%s while open, want clip/visible -- hidden here "
                "drops the sticky header" % (tag, st["bodyOX"], st["bodyOY"]))
        if st["bodyPad"] in ("0px", "auto"):
            good(tag)
        else:
            bad("%s body padding-right=%s while open -- the scrollbar width is "
                "already padded on html, paying it twice pulls the layout left"
                % (tag, st["bodyPad"]))
        # sticky header must still be pinned, not scrolled away
        if st["headerTop"] >= 0:
            good(tag)
        else:
            bad("%s sticky header top=%s while open -- the lock took its scrollport"
                % (tag, st["headerTop"]))

        pg.keyboard.press("Escape")
        pg.wait_for_timeout(600)
        after = pg.evaluate("""s=>{const p=document.querySelector(s[0]);
            return {closed:!!(p&&p.hidden&&!p.classList.contains('is-open')),
                    htmlLocked:document.documentElement.classList.contains('is-modal-open'),
                    focusBack:document.activeElement===document.querySelector(s[1])}}""",
                            [panel, trig])
        for key, want in (("closed", True), ("htmlLocked", False), ("focusBack", True)):
            if after[key] is want:
                good(tag)
            else:
                bad("%s after Escape %s=%s want %s" % (tag, key, after[key], want))

    # -- backdrop click closes, and the panel's own click does not
    first = names[0]
    panel = ".gb-acct-modal[data-acct-modal-panel='%s']" % first
    pg.click("[data-acct-view='detail'] [data-acct-modal='%s']" % first, timeout=2000)
    pg.wait_for_timeout(450)
    pg.evaluate("s=>document.querySelector(s+' .gb-acct-modal__panel').click()", panel)
    pg.wait_for_timeout(300)
    if pg.evaluate("s=>document.querySelector(s).classList.contains('is-open')", panel):
        good(label)
    else:
        bad("%s [%s] clicking inside the panel closed it" % (label, first))
    pg.evaluate("s=>document.querySelector(s+' .gb-acct-modal__backdrop').click()", panel)
    pg.wait_for_timeout(600)
    if pg.evaluate("s=>document.querySelector(s).hidden", panel):
        good(label)
    else:
        bad("%s [%s] backdrop click did not close" % (label, first))

    # -- only one panel at a time: opening a second must not leave the first up
    if len(names) > 1:
        pg.click("[data-acct-view='detail'] [data-acct-modal='%s']" % names[0], timeout=2000)
        pg.wait_for_timeout(400)
        pg.evaluate("n=>window.gumiAcct.modal.open(n)", names[1])
        pg.wait_for_timeout(600)
        n_open = pg.evaluate("()=>document.querySelectorAll('.gb-acct-modal.is-open').length")
        if n_open == 1:
            good(label)
        else:
            bad("%s %d panels open at once, want 1" % (label, n_open))
        pg.keyboard.press("Escape")
        pg.wait_for_timeout(600)

    # -- the lock compensates the freed scrollbar width, and does it once.
    #    Headless draws overlay scrollbars, so the width really is 0 here and a
    #    synthetic value is the only way to see the CSS respond at all. It is
    #    written AFTER the first open on purpose: open() measures for real, and
    #    setting it before would just be overwritten.
    set_state(pg, BASE_STATE)
    pg.evaluate("n=>window.gumiAcct.modal.open(n)", names[0])
    pg.wait_for_timeout(400)
    pg.evaluate("()=>document.documentElement.style.setProperty('--scrollbar-w','15px')")
    pad_once = pg.evaluate("()=>getComputedStyle(document.documentElement).paddingRight")
    if pad_once == "15px":
        good(label)
    else:
        bad("%s html padding-right=%s with --scrollbar-w:15px -- the lock rule "
            "does not reach this page" % (label, pad_once))
    body_pad = pg.evaluate("()=>getComputedStyle(document.body).paddingRight")
    if body_pad in ("0px", "auto"):
        good(label)
    else:
        bad("%s body padding-right=%s too -- the freed width is being paid twice"
            % (label, body_pad))
    # second open into an already-locked page must not re-measure: the real
    # scrollbar is gone by now, so a second measurement reads 0 and wipes it
    pg.evaluate("n=>window.gumiAcct.modal.open(n)", names[-1])
    pg.wait_for_timeout(600)
    pad_twice = pg.evaluate("()=>getComputedStyle(document.documentElement).paddingRight")
    if pad_twice == pad_once:
        good(label)
    else:
        bad("%s padding-right changed on the second open: %s -> %s (compensation "
            "must happen once)" % (label, pad_once, pad_twice))
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(600)
    pg.evaluate("()=>document.documentElement.style.removeProperty('--scrollbar-w')")

    # -- the close cross is clickable, so it needs a hover and a transition to
    #    get there (global rule 13). Read through Playwright: a headless page
    #    driven directly reports (hover: hover) as false and never applies it.
    set_state(pg, BASE_STATE)
    pg.evaluate("n=>window.gumiAcct.modal.open(n)", names[0])
    pg.wait_for_timeout(400)
    close_sel = (".gb-acct-modal[data-acct-modal-panel='%s'] .gb-acct-modal__close" % names[0])
    rest = pg.evaluate("s=>{const c=getComputedStyle(document.querySelector(s));"
                       "return [c.color, c.transitionDuration]}", close_sel)
    pg.hover(close_sel)
    pg.wait_for_timeout(450)
    hot = pg.evaluate("s=>getComputedStyle(document.querySelector(s)).color", close_sel)
    if hot != rest[0]:
        good(label)
    else:
        bad("%s close button colour does not change on hover (%s)" % (label, rest[0]))
    if rest[1] not in ("0s", "0s, 0s"):
        good(label)
    else:
        bad("%s close button has no transition -- the hover would jump" % label)
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(600)

    # -- Lenis takes the wheel site-wide and its PREVENT sweep runs once at
    #    main.js init, so a panel body that scrolls has to carry
    #    data-lenis-prevent itself. The shells are empty, so the check gives one
    #    a real overflow first -- otherwise it would pass on an unscrollable box.
    set_state(pg, BASE_STATE)
    pg.evaluate("n=>window.gumiAcct.modal.open(n)", names[0])
    pg.wait_for_timeout(400)
    body_sel = (".gb-acct-modal[data-acct-modal-panel='%s'] .gb-acct-modal__body" % names[0])
    # ⚠ the panel's real content is put back afterwards. Clearing it instead left
    # this panel an empty shell for every check that runs later in the file.
    armed = pg.evaluate("""s=>{const b=document.querySelector(s);if(!b)return null;
        b.insertAdjacentHTML('beforeend','<div data-probe style="height:2000px"></div>');
        return {prevent:b.hasAttribute('data-lenis-prevent'),
                scrollable:b.scrollHeight-b.clientHeight}}""", body_sel)
    if armed is None:
        bad("%s [%s] no __body to test the wheel on" % (label, names[0]))
    else:
        if armed["prevent"]:
            good(label)
        else:
            bad("%s [%s] panel body has no data-lenis-prevent -- Lenis eats the wheel"
                % (label, names[0]))
        if armed["scrollable"] > 100:
            good(label)
        else:
            bad("%s [%s] body did not become scrollable (%s) -- the wheel test below "
                "would pass on nothing" % (label, names[0], armed["scrollable"]))
            armed = None
    if armed:
        box = pg.evaluate("s=>{const r=document.querySelector(s).getBoundingClientRect();"
                          "return [r.x+r.width/2, r.y+r.height/2]}", body_sel)
        pg.mouse.move(box[0], box[1])
        pg.mouse.wheel(0, 300)
        pg.wait_for_timeout(500)
        moved = pg.evaluate("s=>document.querySelector(s).scrollTop", body_sel)
        if moved > 0:
            good(label)
        else:
            bad("%s [%s] wheel over the panel body scrolled it 0px -- Lenis still "
                "has the wheel" % (label, names[0]))
    # Only the probe div goes: rewriting innerHTML would rebuild the real fields
    # and detach the nodes acctForm captured, so Save could never wake up again.
    pg.evaluate("""s=>{const b=document.querySelector(s);if(!b)return;
        const d=b.querySelector('[data-probe]');if(d)d.remove();b.scrollTop=0}""", body_sel)
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(600)

    # -- the real thing, if this browser can show it
    sbw = pg.evaluate("()=>{document.body.style.minHeight='4000px';"
                      "return window.innerWidth-document.documentElement.clientWidth}")
    if sbw == 0:
        aborted.append("%s no real scrollbar (overlay scrollbars) -- the "
                       "page-shift check proves nothing here, verify on a real browser" % label)
    else:
        before = pg.evaluate("()=>document.querySelector('.gb-acct-nav')"
                             ".getBoundingClientRect().left")
        pg.click("[data-acct-view='detail'] [data-acct-modal='%s']" % names[0], timeout=2000)
        pg.wait_for_timeout(450)
        after = pg.evaluate("()=>document.querySelector('.gb-acct-nav')"
                            ".getBoundingClientRect().left")
        if abs(after - before) < 0.5:
            good(label)
        else:
            bad("%s page shifted %.2fpx sideways when the lock removed the scrollbar"
                % (label, after - before))
    check_forms(pg, w, label)
    check_products(pg, w, label)
    check_discount(pg, w, label)
    check_shipping(pg, w, label)
    check_cancel(pg, w, label)
    pg.close()


# ---------------------------------------------------------------------------
# Task 9: the six simple form modals.
#
# Phone values are the boards'. Desktop has no board (SPEC 待裁决 E) and the user
# settled it: keep the board's 390 panel width, take everything else from the
# account's own desktop language. The type scale needs nothing -- board 27792
# proves desktop and phone share it (14/20 labels, 16/24 buttons, 12/18 small,
# 24/30 page title). Container padding is the one real delta, so the modal uses
# the cards' own ramp: 24 desktop / 20 phone, fluid between.
# ---------------------------------------------------------------------------
PAD_DESK = "24px"
PAD_PHONE = "20px"

# hook -> (board node, phone panel height, save is dirty-gated)
FORMS = {
    "edit-name":      ("2284:31330", 246, True),
    "edit-date":      ("2284:31976", 290, True),
    "edit-frequency": ("2284:32135", 290, True),
    "edit-payment":   ("2284:32463", 256, False),
    "skip-next":      ("2284:32621", 236, False),
    "need-now":       ("2284:33350", 256, False),
}


def check_forms(pg, w, label):
    """Structure and behaviour of the six Task 9 panels."""
    pad = PAD_PHONE if w <= 767 else PAD_DESK
    for name in FORMS:
        node, height, gated = FORMS[name]
        tag = "%s [%s]" % (label, name)
        sel = ".gb-acct-modal[data-acct-modal-panel='%s']" % name
        set_state(pg, BASE_STATE)
        pg.evaluate("n=>window.gumiAcct.modal.open(n)", name)
        pg.wait_for_timeout(450)

        got = pg.evaluate("""a=>{const p=document.querySelector(a[0]);
            if(!p)return null;
            const q=s=>p.querySelector(s);
            const cs=e=>e?getComputedStyle(e):null;
            const box=q('.gb-acct-modal__panel');
            const head=q('.gb-acct-modal__head');
            const bodyEl=q('.gb-acct-modal__body');
            const foot=q('.gb-acct-modal__foot');
            const save=q('[data-acct-save]');
            const cancel=q('.gb-acct-modal__foot .gb-acct-link');
            const copy=q('.gb-acct-modal__copy');
            const field=q('.gb-acct-field__input');
            const hb=cs(head), bb=cs(bodyEl), fb=cs(foot), sb=cs(save);
            return {h:Math.round(box.getBoundingClientRect().height),
                    w:Math.round(box.getBoundingClientRect().width),
                    headPadX:hb&&hb.paddingLeft, headPadY:hb&&hb.paddingTop,
                    bodyPad:bb&&bb.paddingLeft, bodyPadY:bb&&bb.paddingTop,
                    bodyBg:bb&&bb.backgroundColor,
                    footPadX:fb&&fb.paddingLeft, footPadY:fb&&fb.paddingTop,
                    hasFoot:!!foot, hasSave:!!save, hasCancel:!!cancel,
                    saveH:save?Math.round(save.getBoundingClientRect().height):null,
                    saveDisabled:save?save.disabled:null,
                    savePad:sb&&sb.paddingLeft,
                    copyW:copy?Math.round(copy.getBoundingClientRect().width):null,
                    fieldH:field?Math.round(field.getBoundingClientRect().height):null,
                    fieldR:field?cs(field).borderTopLeftRadius:null,
                    fieldBorder:field?cs(field).borderTopColor:null}}""", [sel])
        if got is None:
            bad("%s panel missing" % tag)
            continue

        # the phone panel must come out at the board's own height
        if w <= 767:
            if abs(got["h"] - height) <= 2:
                good(tag)
            else:
                bad("%s panel %spx tall, board %s is %s" % (tag, got["h"], node, height))
        # the user settled the desktop width: the board's 390, not wider
        if got["w"] == 390 or w <= 390:
            good(tag)
        else:
            bad("%s panel %spx wide, want the board's 390" % (tag, got["w"]))

        for key, want, why in (
                ("headPadX", pad, "head gutter follows the cards' 24/20 ramp"),
                ("headPadY", "20px", "head is 20 top and bottom on both boards"),
                ("bodyPad", pad, "body gutter follows the cards' 24/20 ramp"),
                ("bodyPadY", pad, "body padding is 24/20 like .gb-acct-sub__body"),
                ("footPadX", pad, "foot gutter follows the cards' 24/20 ramp"),
                ("footPadY", "16px", "foot is 16 top and bottom on the boards")):
            if got[key] == want:
                good(tag)
            else:
                bad("%s %s=%s want %s -- %s" % (tag, key, got[key], want, why))

        if got["bodyBg"] == "rgb(250, 249, 248)":
            good(tag)
        else:
            bad("%s body background %s, board fills it cream #faf9f8" % (tag, got["bodyBg"]))

        for key in ("hasFoot", "hasSave", "hasCancel"):
            if got[key]:
                good(tag)
            else:
                bad("%s %s is false" % (tag, key))

        sel_ap = pg.evaluate("""a=>{const s=document.querySelector(a[0]+' select.gb-acct-field__input');
            return s?[getComputedStyle(s).appearance,
                      !!s.parentElement.querySelector('.gb-acct-field__icon')]:null}""",
                             [sel])
        if sel_ap is None:
            pass                                   # this panel has no <select>
        elif sel_ap == ["none", True]:
            good(tag)
        else:
            bad("%s <select> appearance=%s chevron=%s -- the board draws one "
                "chevron, the UA's own has to be off" % (tag, sel_ap[0], sel_ap[1]))

        if got["saveH"] == 40:
            good(tag)
        else:
            bad("%s save button %spx tall, board is 40" % (tag, got["saveH"]))
        if got["savePad"] == "32px":
            good(tag)
        else:
            bad("%s save padding-inline %s, board is 32" % (tag, got["savePad"]))

        # note 27446: Save only wakes up once the form above it has been touched.
        # The three confirm-only panels have nothing to touch and ship enabled --
        # which is also what their boards draw (green fill, not #e6e6e6).
        if got["saveDisabled"] is gated:
            good(tag)
        else:
            bad("%s save disabled=%s want %s (note 27446)"
                % (tag, got["saveDisabled"], gated))

        if gated and got["fieldH"] is None:
            bad("%s no .gb-acct-field__input to gate Save on" % tag)
        elif gated:
            # <select> does not take fill(); pick the option that is not current
            fsel = sel + " .gb-acct-field__input"
            if pg.evaluate("s=>document.querySelector(s).tagName", fsel) == "SELECT":
                opts = pg.evaluate("s=>{const e=document.querySelector(s);"
                                   "return [...e.options].map(o=>o.value||o.text)}", fsel)
                cur = pg.evaluate("s=>document.querySelector(s).value", fsel)
                other = [o for o in opts if o != cur]
                if not other:
                    bad("%s the select has only one option, nothing to dirty" % tag)
                    pg.keyboard.press("Escape")
                    pg.wait_for_timeout(600)
                    continue
                pg.select_option(fsel, other[0])
            else:
                pg.fill(fsel, "changed by the judge")
            pg.wait_for_timeout(250)
            now = pg.evaluate("a=>document.querySelector(a[0]+' [data-acct-save]').disabled", [sel])
            if now is False:
                good(tag)
            else:
                bad("%s save stayed disabled after the field changed" % tag)
            # and back again: restoring the original value re-locks it
            pg.evaluate("""a=>{const i=document.querySelector(a[0]+' .gb-acct-field__input');
                if(i.tagName==='SELECT'){const d=[...i.options].find(o=>o.defaultSelected);
                  if(d)i.value=d.value||d.text;}
                else i.value=i.defaultValue;
                i.dispatchEvent(new Event('input',{bubbles:true}));
                i.dispatchEvent(new Event('change',{bubbles:true}))}""", [sel])
            pg.wait_for_timeout(250)
            back = pg.evaluate("a=>document.querySelector(a[0]+' [data-acct-save]').disabled", [sel])
            if back is True:
                good(tag)
            else:
                bad("%s save stayed enabled after the field was put back" % tag)
            if got["fieldH"] == 44:
                good(tag)
            else:
                bad("%s field %spx tall, board is 44" % (tag, got["fieldH"]))
            if got["fieldR"] == "8px":
                good(tag)
            else:
                bad("%s field radius %s, board is 8" % (tag, got["fieldR"]))
            if got["fieldBorder"] == "rgb(204, 204, 204)":
                good(tag)
            else:
                bad("%s field border %s, board is #cccccc" % (tag, got["fieldBorder"]))
        else:
            # 320 fixed copy frame, left aligned -- all three copy boards agree
            if got["copyW"] == 320:
                good(tag)
            else:
                bad("%s copy block %spx wide, board frame is 320" % (tag, got["copyW"]))

        pg.keyboard.press("Escape")
        pg.wait_for_timeout(600)


# ---------------------------------------------------------------------------
# Task 10: the three product panels, all 672 bottom sheets.
#
# Notes driving this: 34502 the last product cannot be taken to 0, 34504 taking
# an extra one to 0 turns the action into a removal, 30917 many products means
# the body scrolls while the action stays put, 30913/30915 Flavour is not
# editable yet (待裁决 J) so it is drawn but inert.
# ---------------------------------------------------------------------------
PRODUCTS = {
    # hook: (board, cards, qty floor, CTA label, alert banner?, label at qty 0)
    # ⚠ the zero label is per panel, not automatic: 31145 swaps Save for a
    # removal, but 28942/29399 sit at 0 with the CTA still reading Add products
    # because 0 there means "not chosen", not "take it out".
    "edit-product":   ("2284:30960", 1, 0, "Save", False, "Remove this product"),
    "add-product":    ("2284:28942", 4, 0, "Add products", False, None),
    "product-locked": ("2284:33847", 1, 1, "Save", True, None),
}


def check_products(pg, w, label):
    pad = PAD_PHONE if w <= 767 else PAD_DESK
    for name in PRODUCTS:
        node, ncards, floor, cta, alert, zero_label = PRODUCTS[name]
        tag = "%s [%s]" % (label, name)
        sel = ".gb-acct-modal[data-acct-modal-panel='%s']" % name
        set_state(pg, BASE_STATE)
        pg.evaluate("n=>window.gumiAcct.modal.open(n)", name)
        pg.wait_for_timeout(450)

        got = pg.evaluate("""a=>{const p=document.querySelector(a[0]);
            if(!p)return null;
            const q=s=>p.querySelector(s), qa=s=>[...p.querySelectorAll(s)];
            const cs=e=>e?getComputedStyle(e):null;
            const bodyEl=q('.gb-acct-modal__body');
            const foot=q('.gb-acct-modal__foot');
            const save=q('[data-acct-save]');
            const cards=qa('[data-acct-product]');
            const thumb=q('.gb-acct-prod__thumb');
            const opt=q('.gb-acct-prod__select');
            const qty=q('.gb-acct-qty');
            const bb=cs(bodyEl), fb=cs(foot);
            return {sheet:p.classList.contains('gb-acct-modal--sheet'),
                    bodyOverflow:bb&&bb.overflowY, bodyPadX:bb&&bb.paddingLeft,
                    bodyPadY:bb&&bb.paddingTop,
                    lenis:bodyEl?bodyEl.hasAttribute('data-lenis-prevent'):null,
                    footPadY:fb&&fb.paddingTop,
                    cards:cards.length,
                    ctaText:save?save.textContent.trim():null,
                    ctaDefault:save?save.getAttribute('data-acct-label-default'):null,
                    alert:!!q('.gb-acct-modal__alert'),
                    thumbRatio:thumb?Math.round(thumb.getBoundingClientRect().width
                                 /thumb.getBoundingClientRect().height*100)/100:null,
                    optInert:opt?(opt.getAttribute('aria-disabled')==='true'||opt.disabled===true):null,
                    qtyH:qty?Math.round(qty.getBoundingClientRect().height):null,
                    qtyR:qty?cs(qty).borderTopLeftRadius:null,
                    qtyBorder:qty?cs(qty).borderTopColor:null,
                    floor:q('[data-acct-product]')?
                          q('[data-acct-product]').getAttribute('data-acct-qty-min'):null}}""", [sel])
        if got is None:
            bad("%s panel missing" % tag)
            continue

        if got["sheet"]:
            good(tag)
        else:
            bad("%s is not a --sheet: board %s is the 672 bottom sheet" % (tag, node))
        if got["cards"] == ncards:
            good(tag)
        else:
            bad("%s %s cards, board %s draws %s" % (tag, got["cards"], node, ncards))
        if got["alert"] is alert:
            good(tag)
        else:
            bad("%s alert banner=%s want %s" % (tag, got["alert"], alert))
        # 30917: the body is what scrolls, and it has to hold the wheel itself
        if got["bodyOverflow"] == "auto":
            good(tag)
        else:
            bad("%s body overflow-y=%s, want auto" % (tag, got["bodyOverflow"]))
        if got["lenis"]:
            good(tag)
        else:
            bad("%s body has no data-lenis-prevent -- Lenis eats the wheel" % tag)
        # the sheet's own padding: 32 top and bottom on the board, sides on the
        # account's 24/20 ramp; the foot is 20 here, not the short panels' 16
        if got["bodyPadX"] == pad:
            good(tag)
        else:
            bad("%s body gutter %s want %s" % (tag, got["bodyPadX"], pad))
        if got["bodyPadY"] == "32px":
            good(tag)
        else:
            bad("%s body padding-top %s, board is 32" % (tag, got["bodyPadY"]))
        if got["footPadY"] == "20px":
            good(tag)
        else:
            bad("%s foot padding-top %s, the 80 foot is 20" % (tag, got["footPadY"]))
        if got["ctaText"] == cta:
            good(tag)
        else:
            bad("%s CTA is %r, board says %r" % (tag, got["ctaText"], cta))
        if got["ctaDefault"] == cta:
            good(tag)
        else:
            bad("%s CTA has no data-acct-label-default to restore to" % tag)
        # 196:19033 is a square placeholder, and the card is fluid, so the ratio
        # is the invariant rather than the 136
        if got["thumbRatio"] == 1:
            good(tag)
        else:
            bad("%s thumb aspect %s, board is square" % (tag, got["thumbRatio"]))
        # 30913/30915: drawn, not operable (待裁决 J)
        if got["optInert"]:
            good(tag)
        else:
            bad("%s Flavour is operable -- note 30913 says not yet" % tag)
        for key, want, why in (("qtyH", 42, "board QTY block is 42"),
                               ("qtyR", "8px", "board radius is 8"),
                               ("qtyBorder", "rgb(179, 179, 179)", "board border is #b3b3b3")):
            if got[key] == want:
                good(tag)
            else:
                bad("%s %s=%s want %s -- %s" % (tag, key, got[key], want, why))
        if got["floor"] == str(floor):
            good(tag)
        else:
            bad("%s first card data-acct-qty-min=%s want %s (note 34502)"
                % (tag, got["floor"], floor))

        # -- behaviour: the stepper
        if not got["cards"] or got["floor"] is None:
            bad("%s no stepper to drive -- the behaviour checks cannot run" % tag)
            pg.keyboard.press("Escape")
            pg.wait_for_timeout(600)
            continue
        first = sel + " [data-acct-product]:first-child "
        start = pg.evaluate("s=>parseInt(document.querySelector(s).textContent,10)",
                            first + "[data-acct-qty-value]")
        # Down as far as it goes. The button disables itself at the floor, and
        # Playwright's click waits for "enabled", so this has to stop on the
        # state rather than count clicks.
        down = first + "[data-acct-qty='down']"
        for _ in range(start + 4):
            if pg.evaluate("s=>document.querySelector(s).disabled", down):
                break
            pg.click(down)
            pg.wait_for_timeout(80)
        else:
            bad("%s stepper never bottomed out" % tag)
        # One more, with the attribute lifted. ⚠ A disabled button does not fire
        # click even from script, so leaving it on would test nothing: the JS
        # floor guard would go unexercised on any panel whose button ships
        # disabled in the markup (product-locked does).
        pg.evaluate("""s=>{const b=document.querySelector(s);const was=b.disabled;
            b.disabled=false;b.click();b.disabled=was}""", down)
        pg.wait_for_timeout(120)
        low = pg.evaluate("s=>parseInt(document.querySelector(s).textContent,10)",
                          first + "[data-acct-qty-value]")
        if low == floor:
            good(tag)
        else:
            bad("%s stepper bottomed out at %s, floor is %s (note 34502)"
                % (tag, low, floor))
        after = pg.evaluate("a=>document.querySelector(a[0]+' [data-acct-save]').textContent.trim()",
                            [sel])
        want_after = zero_label if (zero_label and low == 0) else cta
        if after == want_after:
            good(tag)
        else:
            bad("%s CTA at qty=%s is %r, want %r (note 34504)"
                % (tag, low, after, want_after))
        pg.click(first + "[data-acct-qty='up']")
        pg.wait_for_timeout(120)
        back = pg.evaluate("a=>document.querySelector(a[0]+' [data-acct-save]').textContent.trim()",
                           [sel])
        if back == cta:
            good(tag)
        else:
            bad("%s CTA did not go back to %r after stepping up (got %r)"
                % (tag, cta, back))
        # one delegated bind only: a second open must not double every click
        pg.keyboard.press("Escape")
        pg.wait_for_timeout(600)
        pg.evaluate("n=>window.gumiAcct.modal.open(n)", name)
        pg.wait_for_timeout(450)
        # ⚠ bind() runs once per panel at init, so simply reopening cannot produce
        # a double bind and an "open it twice" test would pass no matter what.
        # Call bind again by hand -- that is the case the guard exists for.
        pg.evaluate("a=>window.gumiAcct.qty.bind(document.querySelector(a[0]))", [sel])
        pg.wait_for_timeout(120)
        before = pg.evaluate("s=>parseInt(document.querySelector(s).textContent,10)",
                             first + "[data-acct-qty-value]")
        pg.click(first + "[data-acct-qty='up']")
        pg.wait_for_timeout(120)
        step = pg.evaluate("s=>parseInt(document.querySelector(s).textContent,10)",
                           first + "[data-acct-qty-value]") - before
        if step == 1:
            good(tag)
        else:
            bad("%s one click moved the stepper by %s -- bound more than once" % (tag, step))
        pg.keyboard.press("Escape")
        pg.wait_for_timeout(600)


# ---------------------------------------------------------------------------
# Task 11: the discount panel, two shipped states plus one driven by the input.
#
# 31488 empty / 31648 the same panel with the field filled / 31809 after the code
# took, which clears the field again and adds the chip. So "filled" is not a
# third piece of markup -- it is what the input's value does to Apply, which is
# all a static page can decide (note 30919: whether the code actually exists is
# the back end's call, so Apply going green is not a promise that it works).
# ---------------------------------------------------------------------------
GREEN = "rgb(0, 86, 53)"
GREY = "rgb(230, 230, 230)"

DISCOUNT = {
    # hook: (board, panel height at 390, shipped state, chip?)
    "discount-add":     ("2284:31488", 246, "empty", False),
    "discount-applied": ("2284:31809", 292, "applied", True),
}


def check_discount(pg, w, label):
    for name in DISCOUNT:
        node, height, state, chip = DISCOUNT[name]
        tag = "%s [%s]" % (label, name)
        sel = ".gb-acct-modal[data-acct-modal-panel='%s']" % name
        set_state(pg, BASE_STATE)
        pg.evaluate("n=>window.gumiAcct.modal.open(n)", name)
        pg.wait_for_timeout(450)

        got = pg.evaluate("""a=>{const p=document.querySelector(a[0]);
            if(!p)return null;
            const q=s=>p.querySelector(s);
            const cs=e=>e?getComputedStyle(e):null;
            const box=q('.gb-acct-modal__panel');
            const apply=q('[data-acct-apply]');
            const inp=q('.gb-acct-discount__input');
            const ch=q('.gb-acct-chip');
            const chShown=!!(ch&&ch.getClientRects().length);
            const ab=cs(apply), cb=cs(ch);
            return {h:Math.round(box.getBoundingClientRect().height),
                    state:p.getAttribute('data-acct-discount-state'),
                    hasApply:!!apply, hasInput:!!inp, hasChip:!!ch,
                    applyBg:ab&&ab.backgroundColor, applyDisabled:apply?apply.disabled:null,
                    applyW:apply?Math.round(apply.getBoundingClientRect().width):null,
                    applyH:apply?Math.round(apply.getBoundingClientRect().height):null,
                    applyR:ab&&ab.borderTopLeftRadius,
                    inputVal:inp?inp.value:null,
                    placeholder:inp?inp.getAttribute('placeholder'):null,
                    chipShown:chShown,
                    chipBg:cb&&cb.backgroundColor, chipR:cb&&cb.borderTopLeftRadius,
                    chipText:ch?ch.textContent.replace(/\s+/g,' ').trim():null,
                    chipRemove:!!q('.gb-acct-chip__remove'),
                    save:!!q('[data-acct-save]')}}""", [sel])
        if got is None:
            bad("%s panel missing" % tag)
            continue

        if w <= 767:
            if abs(got["h"] - height) <= 2:
                good(tag)
            else:
                bad("%s panel %spx tall, board %s is %s" % (tag, got["h"], node, height))
        if got["state"] == state:
            good(tag)
        else:
            bad("%s data-acct-discount-state=%s want %s" % (tag, got["state"], state))
        for key in ("hasApply", "hasInput"):
            if got[key]:
                good(tag)
            else:
                bad("%s %s is false" % (tag, key))
        # 31646/31974: the foot carries Cancel only, no action button
        if got["save"] is False:
            good(tag)
        else:
            bad("%s has a [data-acct-save] -- the board's foot is Cancel only" % tag)
        # 31645: 96x44, r8 -- an inline field button, not the 40-tall pill
        for key, want in (("applyW", 96), ("applyH", 44), ("applyR", "8px")):
            if got[key] == want:
                good(tag)
            else:
                bad("%s %s=%s want %s (board 2284:31645)" % (tag, key, got[key], want))
        # both shipped states have an empty field, so Apply starts grey
        if got["inputVal"] == "":
            good(tag)
        else:
            bad("%s input ships with %r, both boards ship it empty" % (tag, got["inputVal"]))
        if got["placeholder"] == "Discount Code":
            good(tag)
        else:
            bad("%s placeholder %r, board says 'Discount Code'" % (tag, got["placeholder"]))
        if got["applyBg"] == GREY and got["applyDisabled"] is True:
            good(tag)
        else:
            bad("%s Apply starts %s disabled=%s, want %s + disabled"
                % (tag, got["applyBg"], got["applyDisabled"], GREY))
        # the chip lives in both panels and the state switches it, so this is a
        # visibility question rather than a presence one
        if got["chipShown"] is chip:
            good(tag)
        else:
            bad("%s chip shown=%s want %s" % (tag, got["chipShown"], chip))
        if chip:
            if got["chipBg"] == "rgb(246, 254, 236)":
                good(tag)
            else:
                bad("%s chip fill %s, board 31969 is #f6feec" % (tag, got["chipBg"]))
            if got["chipR"] == "8px":
                good(tag)
            else:
                bad("%s chip radius %s, board is 8" % (tag, got["chipR"]))
            if got["chipText"] == "Discount CEO90 applied $35.25 off":
                good(tag)
            else:
                bad("%s chip reads %r" % (tag, got["chipText"]))
            if got["chipRemove"]:
                good(tag)
            else:
                bad("%s chip has no remove control (31973 is a bin glyph)" % tag)

        # -- behaviour: Apply follows the field, nothing else
        if not (got["hasApply"] and got["hasInput"]):
            bad("%s no field/Apply pair -- the behaviour checks cannot run" % tag)
            pg.keyboard.press("Escape")
            pg.wait_for_timeout(600)
            continue
        inp = sel + " .gb-acct-discount__input"
        pg.fill(inp, "CEO90")
        pg.wait_for_timeout(250)
        on = pg.evaluate("""a=>{const b=document.querySelector(a[0]+' [data-acct-apply]');
            return [getComputedStyle(b).backgroundColor, b.disabled]}""", [sel])
        if on[0] == GREEN and on[1] is False:
            good(tag)
        else:
            bad("%s Apply is %s disabled=%s with a code typed, want %s + enabled"
                % (tag, on[0], on[1], GREEN))
        # whitespace is not a code
        pg.fill(inp, "   ")
        pg.wait_for_timeout(250)
        ws = pg.evaluate("a=>document.querySelector(a[0]+' [data-acct-apply]').disabled", [sel])
        if ws is True:
            good(tag)
        else:
            bad("%s Apply woke up on whitespace alone" % tag)
        pg.fill(inp, "")
        pg.wait_for_timeout(250)
        off = pg.evaluate("""a=>{const b=document.querySelector(a[0]+' [data-acct-apply]');
            return [getComputedStyle(b).backgroundColor, b.disabled]}""", [sel])
        if off[0] == GREY and off[1] is True:
            good(tag)
        else:
            bad("%s Apply stayed %s disabled=%s after the field was cleared"
                % (tag, off[0], off[1]))
        pg.keyboard.press("Escape")
        pg.wait_for_timeout(600)


# ---------------------------------------------------------------------------
# Task 12: the shipping flow -- current address (32294) -> form (32940/33161)
# -> success (32779).
#
# 32940 and 33161 are the SAME panel with two data fills (Charnwood/3181 vs
# Park Ave/3121), not two panels: the trees are identical node for node. So the
# judge edits the one form using the other board's values, which keeps every
# string it types sourced from a board.
#
# ⚠ The two cards here (address 32448, success 32932) are the one board frame
# whose strokesIncludedInLayout is true: 16 padding + a real 1px border makes
# the board's 178 / 78. Everywhere else on this page the INSIDE hairline must
# NOT add box height, which is why the head and foot use inset box-shadow.
# ---------------------------------------------------------------------------
NAVY = "rgb(16, 24, 40)"          # #101828, the "Current Address" heading
INK = "rgb(1, 19, 7)"             # #011307, the emphasised first line
GREY6 = "rgb(102, 102, 102)"      # #666666
GREY7 = "rgb(77, 77, 77)"         # #4d4d4d, the +61 prefix
CCC = "rgb(204, 204, 204)"

# 32940 label order, and whether the board marks it with a star.
FORM_FIELDS = [
    ("First Name*", True), ("Last Name*", True), ("Phone number*", True),
    ("Company", False), ("Address Line 1*", True), ("Address Line 2", False),
    ("Suburb*", True), ("State*", True), ("Postcode*", True),
    # the board's own spelling -- registered in SPEC 8
    ("Delivery Instrctions", False),
]


def _open(pg, name):
    set_state(pg, BASE_STATE)
    pg.evaluate("n=>window.gumiAcct.modal.open(n)", name)
    pg.wait_for_timeout(450)


def check_shipping(pg, w, label):
    check_ship_current(pg, w, label)
    check_ship_form(pg, w, label)
    check_ship_success(pg, w, label)


def check_ship_current(pg, w, label):
    tag = "%s [shipping-current]" % label
    sel = ".gb-acct-modal[data-acct-modal-panel='shipping-current']"
    _open(pg, "shipping-current")

    got = pg.evaluate(r"""a=>{const p=document.querySelector(a[0]);
        if(!p)return null;
        const q=s=>p.querySelector(s);
        const cs=e=>e?getComputedStyle(e):null;
        const r=e=>e?e.getBoundingClientRect():null;
        const box=q('.gb-acct-modal__panel');
        const title=q('.gb-acct-addr__title');
        const card=q('.gb-acct-addr__card');
        const radio=q('.gb-acct-addr__radio');
        const lines=[...p.querySelectorAll('.gb-acct-addr__line')];
        const edit=q('.gb-acct-addr__card [data-acct-modal]');
        const cb=cs(card), tb=cs(title);
        const lr=lines.map(e=>r(e));
        return {h:Math.round(r(box).height),
                headH:q('.gb-acct-modal__head')?
                      Math.round(r(q('.gb-acct-modal__head')).height):null,
                footH:q('.gb-acct-modal__foot')?
                      Math.round(r(q('.gb-acct-modal__foot')).height):null,
                title:title?title.textContent.trim():null,
                titleColor:tb&&tb.color, titleSize:tb&&tb.fontSize,
                cardH:card?Math.round(r(card).height):null,
                cardPad:cb&&cb.paddingTop, cardBorder:cb&&cb.borderTopWidth,
                cardBorderColor:cb&&cb.borderTopColor, cardR:cb&&cb.borderTopLeftRadius,
                cardBg:cb&&cb.backgroundColor,
                radioW:radio?Math.round(r(radio).width):null,
                radioH:radio?Math.round(r(radio).height):null,
                radioChecked:radio?radio.checked:null,
                radioBg:radio?cs(radio).backgroundColor:null,
                radioR:radio?cs(radio).borderTopLeftRadius:null,
                lineCount:lines.length,
                lineText:lines.map(e=>e.textContent.trim()),
                lineColor:lines.map(e=>cs(e).color),
                clipped:lines.length>5&&lines[5].scrollWidth>lines[5].clientWidth,
                innerGap:lr.length>1?Math.round(lr[1].top-lr[0].bottom):null,
                outerGap:lr.length>5?Math.round(lr[5].top-lr[4].bottom):null,
                editTo:edit?edit.getAttribute('data-acct-modal'):null,
                editColor:edit?cs(edit).color:null,
                save:!!q('[data-acct-save]'),
                saveDisabled:q('[data-acct-save]')?q('[data-acct-save]').disabled:null,
                cancel:!!q('.gb-acct-modal__foot .gb-acct-link')}}""", [sel])
    if got is None:
        bad("%s panel missing" % tag)
        return

    if w <= 767:
        if abs(got["h"] - 394) <= 2:
            good(tag)
        else:
            bad("%s panel %spx tall, board 2284:32294 is 394" % (tag, got["h"]))
    for key, want, why in (("headH", 64, "board head is 64"),
                           ("footH", 72, "board foot is 72")):
        if got[key] == want:
            good(tag)
        else:
            bad("%s %s=%s want %s -- %s" % (tag, key, got[key], want, why))

    if got["title"] == "Current Address":
        good(tag)
    else:
        bad("%s heading %r, board 32447 says 'Current Address'" % (tag, got["title"]))
    # 32447 is #101828 -- the one label on this page that is not #666666
    if got["titleColor"] == NAVY and got["titleSize"] == "14px":
        good(tag)
    else:
        bad("%s heading %s/%s, board 32447 is #101828 14px"
            % (tag, got["titleColor"], got["titleSize"]))

    if got["cardH"] == 178:
        good(tag)
    else:
        bad("%s address card %spx tall, board 32448 is 178 (16 pad + 144 + 1px "
            "border each side, strokesIncludedInLayout)" % (tag, got["cardH"]))
    for key, want in (("cardPad", "16px"), ("cardBorder", "1px"),
                      ("cardBorderColor", CCC), ("cardR", "8px"),
                      ("cardBg", "rgb(255, 255, 255)")):
        if got[key] == want:
            good(tag)
        else:
            bad("%s card %s=%s want %s (board 32448)" % (tag, key, got[key], want))

    for key, want in (("radioW", 16), ("radioH", 16), ("radioChecked", True),
                      ("radioR", "8px"), ("radioBg", "rgb(233, 250, 207)")):
        if got[key] == want:
            good(tag)
        else:
            bad("%s radio %s=%s want %s (board 32450)" % (tag, key, got[key], want))

    want_lines = ["Susanna Rose", "10", "12 Charnwood Road",
                  "St Kilda, Victoria, Australia", "3182",
                  "Delivery instructions: keep in a safe place"]
    if got["lineText"] == want_lines:
        good(tag)
    else:
        bad("%s address lines %r, board 32451 reads %r"
            % (tag, got["lineText"], want_lines))
    # 32453 is #011307, the four under it #666666: a colour split, not a weight one
    if got["lineColor"][:1] == [INK] and set(got["lineColor"][1:]) == {GREY6}:
        good(tag)
    else:
        bad("%s line colours %r, board is #011307 then #666666 throughout"
            % (tag, got["lineColor"]))
    # nested auto-layout: 4 inside the five-line group, 8 out to the instructions
    if got["innerGap"] == 4:
        good(tag)
    else:
        bad("%s gap between address lines %s, board 32452 is 4" % (tag, got["innerGap"]))
    if got["outerGap"] == 8:
        good(tag)
    else:
        bad("%s gap to the delivery line %s, board 32451 is 8 -- flattening the "
            "two groups into one puts it 4 too high" % (tag, got["outerGap"]))

    # 32458 is the one line with maxLines 1 / textTruncation ENDING. Letting it
    # wrap is what puts the card at 198 instead of the board's 178, so the clamp
    # has to be doing work rather than merely being declared.
    if got["clipped"]:
        good(tag)
    else:
        bad("%s the delivery line is not being clipped -- board 32458 truncates "
            "it to one line" % tag)

    # a radio's value never changes; only which one is picked does, so the dirty
    # gate has to read checked-ness or Save can never wake up for an address swap
    if pg.evaluate(r"""a=>{const p=document.querySelector(a[0]);
        const f=p.querySelectorAll('[data-acct-field]');
        const before=window.gumiAcct.form._snapshot(f);
        const r=p.querySelector('.gb-acct-addr__radio');
        r.checked=false;
        const after=window.gumiAcct.form._snapshot(f);
        r.checked=true;
        return before!==after}""", [sel]):
        good(tag)
    else:
        bad("%s _snapshot cannot tell a picked radio from an unpicked one" % tag)

    if got["editTo"] == "shipping-form":
        good(tag)
    else:
        bad("%s Edit opens %r, want shipping-form" % (tag, got["editTo"]))
    if got["editColor"] == "rgb(3, 116, 165)":
        good(tag)
    else:
        bad("%s Edit is %s, board 32459 is #0374a5" % (tag, got["editColor"]))

    for key in ("save", "cancel"):
        if got[key]:
            good(tag)
        else:
            bad("%s foot has no %s -- board 32460 carries both" % (tag, key))
    # 32462 ships #e6e6e6: one address means nothing to pick, so Save stays asleep
    if got["saveDisabled"] is True:
        good(tag)
    else:
        bad("%s Save disabled=%s, board 32462 draws it grey" % (tag, got["saveDisabled"]))

    pg.keyboard.press("Escape")
    pg.wait_for_timeout(600)


def check_ship_form(pg, w, label):
    tag = "%s [shipping-form]" % label
    sel = ".gb-acct-modal[data-acct-modal-panel='shipping-form']"
    _open(pg, "shipping-form")

    got = pg.evaluate(r"""a=>{const p=document.querySelector(a[0]);
        if(!p)return null;
        const q=s=>p.querySelector(s);
        const cs=e=>e?getComputedStyle(e):null;
        const r=e=>e?e.getBoundingClientRect():null;
        const box=q('.gb-acct-modal__panel');
        const bodyEl=q('.gb-acct-modal__body');
        const col=q('.gb-acct-form');
        const rows=[...p.querySelectorAll('.gb-acct-form__row')];
        const labels=[...p.querySelectorAll('.gb-acct-field__label')];
        const ctrl=[...p.querySelectorAll('[data-acct-field]')];
        const pre=q('.gb-acct-field__prefix');
        const area=q('textarea[data-acct-field]');
        const state=q('select[data-acct-field]');
        const post=q('[data-acct-field][name="postcode"]');
        const bb=cs(bodyEl);
        const hd=q('.gb-acct-modal__head'), ft=q('.gb-acct-modal__foot');
        return {sheet:p.classList.contains('gb-acct-modal--sheet'),
                isForm:box.tagName.toLowerCase()==='form',
                next:box.getAttribute('data-acct-modal-next'),
                h:Math.round(r(box).height),
                headH:hd?Math.round(r(hd).height):null,
                footH:ft?Math.round(r(ft).height):null,
                bodyPadY:bb&&bb.paddingTop, bodyPadX:bb&&bb.paddingLeft,
                lenis:!!bodyEl&&bodyEl.hasAttribute('data-lenis-prevent'),
                scrolls:!!bodyEl&&bodyEl.scrollHeight>bodyEl.clientHeight+1,
                colGap:col?cs(col).rowGap:null,
                rowCount:rows.length,
                rowGap:rows.length?cs(rows[0]).columnGap:null,
                rowKids:rows.length?rows[0].children.length:null,
                labels:labels.map(e=>e.textContent.trim()),
                labelKids:labels.map(e=>e.children.length),
                labelColor:[...new Set(labels.map(e=>cs(e).color))],
                required:ctrl.map(e=>e.required),
                fieldH:[...new Set(ctrl.filter(e=>e.tagName!=='TEXTAREA')
                        .map(e=>Math.round(r(e.closest('.gb-acct-field__box')||e).height)))],
                prefix:pre?pre.textContent.trim():null,
                prefixColor:pre?cs(pre).color:null,
                prefixGap:pre?cs(pre.parentElement).columnGap:null,
                areaH:area?Math.round(r(area).height):null,
                areaLenis:area?area.hasAttribute('data-lenis-prevent'):null,
                stateTag:state?state.tagName.toLowerCase():null,
                stateVal:state?state.value:null,
                stateAppearance:state?cs(state).appearance:null,
                stateChevron:!!q('select[data-acct-field] ~ .gb-acct-field__icon'),
                stateOpts:state?state.options.length:null,
                postPattern:post?post.getAttribute('pattern'):null,
                saveDisabled:q('[data-acct-save]')?q('[data-acct-save]').disabled:null,
                saveType:q('[data-acct-save]')?q('[data-acct-save]').type:null,
                backTo:q('.gb-acct-modal__foot [data-acct-modal]')
                       ?q('.gb-acct-modal__foot [data-acct-modal]')
                        .getAttribute('data-acct-modal'):null}}""", [sel])
    if got is None:
        bad("%s panel missing" % tag)
        return

    for key, why in (("sheet", "33087 is the 672 sheet, radius 12 12 0 0"),
                     ("isForm", "Save must go through constraint validation"),
                     ("lenis", "Lenis takes the wheel; the scroll area needs the attribute"),
                     ("scrolls", "the board's 800 column inside a 528 body")):
        if got[key]:
            good(tag)
        else:
            bad("%s %s is false -- %s" % (tag, key, why))
    if got["next"] == "shipping-success":
        good(tag)
    else:
        bad("%s data-acct-modal-next=%r, want shipping-success" % (tag, got["next"]))

    for key, want in (("headH", 64), ("footH", 80)):
        if got[key] == want:
            good(tag)
        else:
            bad("%s %s=%s want %s (board 33088/33126)" % (tag, key, got[key], want))
    # the sheet's own body padding: 32 top and bottom, sides on the 24/20 ramp
    if got["bodyPadY"] == "32px":
        good(tag)
    else:
        bad("%s body padding-top %s, board 33092 is 32" % (tag, got["bodyPadY"]))
    if got["bodyPadX"] == (PAD_PHONE if w <= 767 else PAD_DESK):
        good(tag)
    else:
        bad("%s body gutter %s at %d" % (tag, got["bodyPadX"], w))

    if got["colGap"] == "20px":
        good(tag)
    else:
        bad("%s field column gap %s, board 33093 is 20" % (tag, got["colGap"]))
    if got["rowCount"] == 2 and got["rowKids"] == 2:
        good(tag)
    else:
        bad("%s %s two-up rows (first has %s children), board has 2 of 2"
            % (tag, got["rowCount"], got["rowKids"]))
    if got["rowGap"] == "15px":
        good(tag)
    else:
        bad("%s two-up gap %s, board 33094 is 15" % (tag, got["rowGap"]))

    want_labels = [f[0] for f in FORM_FIELDS]
    if got["labels"] == want_labels:
        good(tag)
    else:
        bad("%s labels %r, board 32940 reads %r" % (tag, got["labels"], want_labels))
    # the star is part of the label's own run: no override in the node, so no
    # separate element and no second colour
    if got["labelKids"] and max(got["labelKids"]) == 0:
        good(tag)
    else:
        bad("%s a label wraps the star in its own element; board 33096 has no "
            "characterStyleOverrides, the * is the same ink" % tag)
    if got["labelColor"] == [GREY6]:
        good(tag)
    else:
        bad("%s label colours %r, board is #666666 throughout" % (tag, got["labelColor"]))

    want_req = [f[1] for f in FORM_FIELDS]
    if got["required"] == want_req:
        good(tag)
    else:
        bad("%s required=%r, the board's stars say %r"
            % (tag, got["required"], want_req))

    if got["fieldH"] == [44]:
        good(tag)
    else:
        bad("%s control heights %r, board's Input is 44" % (tag, got["fieldH"]))

    if got["prefix"] == "+61":
        good(tag)
    else:
        bad("%s phone prefix %r, board 196:17794 is '+61'" % (tag, got["prefix"]))
    # 196:17798, the chevron beside it, is visible=false on the board: the prefix
    # is a label, not a country picker
    if got["prefixColor"] == GREY7:
        good(tag)
    else:
        bad("%s prefix %s, board is #4d4d4d" % (tag, got["prefixColor"]))
    if got["prefixGap"] == "8px":
        good(tag)
    else:
        bad("%s prefix gap %s, board's Input is 8" % (tag, got["prefixGap"]))

    if got["areaH"] == 144:
        good(tag)
    else:
        bad("%s delivery box %spx tall, board 33117 is 144" % (tag, got["areaH"]))
    if got["areaLenis"]:
        good(tag)
    else:
        bad("%s the textarea has no data-lenis-prevent -- Lenis eats its wheel" % tag)

    if got["stateTag"] == "select" and got["stateVal"] == "VIC":
        good(tag)
    else:
        bad("%s State is <%s> value %r, board 33111 shows a chevron and VIC"
            % (tag, got["stateTag"], got["stateVal"]))
    # the board draws exactly one chevron: ours. The UA paints its own on top
    # unless appearance is turned off, and nothing else here would notice.
    if got["stateChevron"]:
        good(tag)
    else:
        bad("%s no .gb-acct-field__icon beside State -- board 33111 draws one" % tag)
    if got["stateAppearance"] == "none":
        good(tag)
    else:
        bad("%s State computes appearance=%s: the UA arrow is still painted on "
            "top of the board's chevron" % (tag, got["stateAppearance"]))
    if got["stateOpts"] and got["stateOpts"] > 1:
        good(tag)
    else:
        bad("%s State has %s options" % (tag, got["stateOpts"]))
    if got["postPattern"]:
        good(tag)
    else:
        bad("%s Postcode has no pattern -- step 3 asks for the format check" % tag)
    if got["saveType"] == "submit":
        good(tag)
    else:
        bad("%s Save is type=%s; only a submit runs the browser's own validation"
            % (tag, got["saveType"]))
    if got["saveDisabled"] is True:
        good(tag)
    else:
        bad("%s Save starts %s, note 27446 gates it on a change"
            % (tag, got["saveDisabled"]))
    if got["backTo"] == "shipping-current":
        good(tag)
    else:
        bad("%s Go Back opens %r, want shipping-current" % (tag, got["backTo"]))

    # -- the sheet is the board's 672 in the board's own viewport
    if w <= 767:
        pg.set_viewport_size({"width": 390, "height": 840})
        pg.wait_for_timeout(300)
        sheet_h = pg.evaluate("a=>Math.round(document.querySelector(a[0]+"
                              "' .gb-acct-modal__panel').getBoundingClientRect().height)",
                              [sel])
        if sheet_h == 672:
            good(tag)
        else:
            bad("%s sheet %spx tall in a 840 viewport, board 33087 is 672"
                % (tag, sheet_h))
        pg.set_viewport_size({"width": w, "height": 900})
        pg.wait_for_timeout(300)

    # -- validation: nothing posts anywhere, but Save must not advance on a form
    #    the board marks required. Every value typed here is 33161's, the second
    #    data fill of this same panel.
    suburb = sel + " [data-acct-field][name='suburb']"
    post = sel + " [data-acct-field][name='postcode']"
    if not pg.evaluate("s=>!!document.querySelector(s)", suburb):
        bad("%s no [name=suburb] to test the required gate on" % tag)
        pg.keyboard.press("Escape")
        pg.wait_for_timeout(600)
        return

    pg.fill(suburb, "")
    pg.wait_for_timeout(250)
    if pg.evaluate("a=>document.querySelector(a[0]+' [data-acct-save]').disabled", [sel]) is False:
        good(tag)
    else:
        bad("%s Save stayed asleep after the form was edited" % tag)
    pg.click(sel + " [data-acct-save]", timeout=2000)
    pg.wait_for_timeout(500)
    st = pg.evaluate(r"""a=>({adv:!!document.querySelector(
        ".gb-acct-modal[data-acct-modal-panel='shipping-success']").classList.contains('is-open'),
        valid:document.querySelector(a[0]+' .gb-acct-modal__panel').checkValidity()})""", [sel])
    if st["adv"] is False and st["valid"] is False:
        good(tag)
    else:
        bad("%s empty Suburb: advanced=%s valid=%s, want no/False"
            % (tag, st["adv"], st["valid"]))

    pg.fill(suburb, "Richmond")
    pg.fill(post, "31")
    pg.wait_for_timeout(250)
    pg.click(sel + " [data-acct-save]", timeout=2000)
    pg.wait_for_timeout(500)
    st = pg.evaluate(r"""a=>({adv:!!document.querySelector(
        ".gb-acct-modal[data-acct-modal-panel='shipping-success']").classList.contains('is-open'),
        valid:document.querySelector(a[0]+' .gb-acct-modal__panel').checkValidity()})""", [sel])
    if st["adv"] is False and st["valid"] is False:
        good(tag)
    else:
        bad("%s postcode '31': advanced=%s valid=%s, want no/False"
            % (tag, st["adv"], st["valid"]))

    # 33100 ships showing its placeholder: Phone is required and empty on the
    # board, so the form as delivered cannot pass. Proving that, then filling it,
    # is what makes the required list above more than a set of attributes.
    if pg.evaluate("a=>document.querySelector(a[0]+' [data-acct-field][name=\"phone\"]').value",
                   [sel]) == "":
        good(tag)
    else:
        bad("%s Phone ships with a value; board 33100 shows its placeholder" % tag)
    pg.fill(sel + " [data-acct-field][name='phone']", "000 000 000")
    pg.fill(post, "3121")
    pg.wait_for_timeout(250)
    pg.click(sel + " [data-acct-save]", timeout=2000)
    pg.wait_for_timeout(600)
    done = pg.evaluate(r"""a=>({adv:!!document.querySelector(
        ".gb-acct-modal[data-acct-modal-panel='shipping-success']").classList.contains('is-open'),
        gone:document.querySelector(a[0]).hidden,
        locked:document.documentElement.classList.contains('is-modal-open')})""", [sel])
    for key, want, why in (("adv", True, "a valid form must reach 32779"),
                           ("gone", True, "the form must not stay up behind it"),
                           ("locked", True, "chaining panels must not drop the lock")):
        if done[key] is want:
            good(tag)
        else:
            bad("%s after a valid Save %s=%s want %s -- %s"
                % (tag, key, done[key], want, why))
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(600)

    # -- and the two links that walk the flow backwards
    _open(pg, "shipping-current")
    pg.click(".gb-acct-modal[data-acct-modal-panel='shipping-current'] "
             ".gb-acct-addr__card [data-acct-modal]", timeout=2000)
    pg.wait_for_timeout(600)
    if pg.evaluate("s=>document.querySelector(s).classList.contains('is-open')", sel):
        good(tag)
    else:
        bad("%s Edit on the address card did not open the form" % tag)
    pg.click(sel + " .gb-acct-modal__foot [data-acct-modal]", timeout=2000)
    pg.wait_for_timeout(600)
    back = pg.evaluate("()=>{const e=document.querySelector('.gb-acct-modal.is-open');"
                       "return e?e.getAttribute('data-acct-modal-panel'):null}")
    if back == "shipping-current":
        good(tag)
    else:
        bad("%s Go Back landed on %r, want shipping-current" % (tag, back))
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(600)


def check_ship_success(pg, w, label):
    tag = "%s [shipping-success]" % label
    sel = ".gb-acct-modal[data-acct-modal-panel='shipping-success']"
    _open(pg, "shipping-success")

    got = pg.evaluate(r"""a=>{const p=document.querySelector(a[0]);
        if(!p)return null;
        const q=s=>p.querySelector(s);
        const cs=e=>e?getComputedStyle(e):null;
        const r=e=>e?e.getBoundingClientRect():null;
        const box=q('.gb-acct-modal__panel');
        const note=q('.gb-acct-note');
        const icon=q('.gb-acct-note__icon');
        const title=q('.gb-acct-note__title');
        const text=q('.gb-acct-note__text');
        const nb=cs(note);
        return {h:Math.round(r(box).height),
                headH:q('.gb-acct-modal__head')?
                      Math.round(r(q('.gb-acct-modal__head')).height):null,
                footH:q('.gb-acct-modal__foot')?
                      Math.round(r(q('.gb-acct-modal__foot')).height):null,
                noteH:note?Math.round(r(note).height):null,
                noteBg:nb&&nb.backgroundColor, noteBorder:nb&&nb.borderTopColor,
                noteWidth:nb&&nb.borderTopWidth, noteR:nb&&nb.borderTopLeftRadius,
                notePad:nb&&nb.paddingTop,
                iconW:icon?Math.round(r(icon).width):null,
                iconGap:(icon&&title)?Math.round(r(title.parentElement).left-r(icon).right):null,
                title:title?title.textContent.trim():null,
                titleColor:title?cs(title).color:null,
                text:text?text.textContent.trim():null,
                textColor:text?cs(text).color:null,
                textGap:(title&&text)?Math.round(r(text).top-r(title).bottom):null,
                save:!!q('[data-acct-save]'),
                close:q('.gb-acct-modal__foot .gb-acct-link')
                      ?q('.gb-acct-modal__foot .gb-acct-link').textContent.trim():null}}""",
                      [sel])
    if got is None:
        bad("%s panel missing" % tag)
        return

    if w <= 767:
        if abs(got["h"] - 254) <= 2:
            good(tag)
        else:
            bad("%s panel %spx tall, board 2284:32779 is 254" % (tag, got["h"]))
    for key, want in (("headH", 64), ("footH", 72)):
        if got[key] == want:
            good(tag)
        else:
            bad("%s %s=%s want %s" % (tag, key, got[key], want))
    # Phone only, like every other board height in this file. At 1440 the panel
    # keeps the board's 390 while the gutters grow to 24, so the note's content
    # box loses 8px and 32937 takes two lines -- the cost of 待裁决 E.
    if w <= 767:
        if got["noteH"] == 78:
            good(tag)
        else:
            bad("%s note %spx tall, board 32932 is 78" % (tag, got["noteH"]))
    elif got["noteH"] >= 78:
        good(tag)
    else:
        bad("%s note %spx tall at %d -- shorter than the board's own 78"
            % (tag, got["noteH"], w))
    for key, want in (("noteBg", "rgb(246, 254, 236)"),
                      ("noteBorder", "rgb(218, 246, 176)"),
                      ("noteWidth", "1px"), ("noteR", "8px"), ("notePad", "16px")):
        if got[key] == want:
            good(tag)
        else:
            bad("%s note %s=%s want %s (board 32932)" % (tag, key, got[key], want))
    if got["iconW"] == 20:
        good(tag)
    else:
        bad("%s tick slot %spx, board 32934 is 20" % (tag, got["iconW"]))
    if got["iconGap"] == 12:
        good(tag)
    else:
        bad("%s icon-to-text gap %s, board 32933 is 12" % (tag, got["iconGap"]))
    if got["title"] == "Success!" and got["titleColor"] == INK:
        good(tag)
    else:
        bad("%s title %r %s, board 32936 is 'Success!' #011307"
            % (tag, got["title"], got["titleColor"]))
    if (got["text"] == "Your shipping details have been updated."
            and got["textColor"] == GREY6):
        good(tag)
    else:
        bad("%s body %r %s, board 32937 is #666666" % (tag, got["text"], got["textColor"]))
    if got["textGap"] == 4:
        good(tag)
    else:
        bad("%s title-to-text gap %s, board 32935 is 4" % (tag, got["textGap"]))
    # 32938 carries Close alone -- the fixed 72 foot with nothing in it but a link
    if got["save"] is False:
        good(tag)
    else:
        bad("%s has a [data-acct-save]; board 32938 is Close only" % tag)
    if got["close"] == "Close":
        good(tag)
    else:
        bad("%s foot link reads %r, board says 'Close'" % (tag, got["close"]))

    pg.keyboard.press("Escape")
    pg.wait_for_timeout(600)


# ---------------------------------------------------------------------------
# Task 13: the cancel funnel and restart.
#
# 29928 / 30286 / 30107 are ONE screen with three different picks, not three
# screens: 29928 selects reason 1, 30286 reason 2, 30107 reason 3. What the pick
# changes is the CTA -- the two reasons that have a second screen read
# "Continue", the terminal one reads "Cancel". That is note 34512 drawn.
#
# ⚠ 30107 is also the board bug: its row 2 label was overwritten, so "Too
# expensive right now" is missing and "I have too much product" appears twice.
# The seven-item list below is 29928/30286's, which agree with each other.
#
# ⚠ The board's July 2026 grid cannot be copied: 1 July 2026 is a Wednesday but
# the board puts it under Su, and one cell reads "32". The calendar is generated
# instead and only its *tokens* come from the board -- see SPEC 8.
# ---------------------------------------------------------------------------
REASONS = [
    ("going-away", "Going away or on holiday", "cancel-holiday", "Continue"),
    ("too-expensive", "Too expensive right now", "cancel-discount", "Continue"),
    ("too-much-product", "I have too much product", None, "Cancel"),
    ("try-once", "I just want to try once without subscribing", None, "Cancel"),
    ("no-difference", "I’m not feeling different in my health yet", None, "Cancel"),
    ("taste-texture", "Taste or texture", None, "Cancel"),
    ("purchased-elsewhere", "I purchased elsewhere", None, "Cancel"),
]

# hook -> (board, phone panel height, head title, foot CTA text)
CANCEL_SCREENS = {
    "cancel-offer-skip": ("2284:29596", 672, "We’re sorry to see you go", "Continue to Skip"),
    "cancel-skipped":    ("2284:29767", 672, "Your next order has been skipped!", "Done"),
    "cancel-reason":     ("2284:29928", 672, "We’re sorry to see you go", "Continue"),
    "cancel-holiday":    ("2284:30465", 672, "Heading away on holiday", "Pause subscription"),
    "cancel-discount":   ("2284:30740", 672, "Too expensive right now", "Claim my 20% discount"),
}

LEAD = "rgb(16, 24, 40)"    # #101828, the first line of every cancel body
GREY8 = "rgb(128, 128, 128)"   # #808080, days outside the rendered month
SEL_ROW = "rgb(230, 245, 225)"  # #e6f5e1, the picked reason


def _panel(name):
    return ".gb-acct-modal[data-acct-modal-panel='%s']" % name


def _click(pg, sel, tag, what):
    """Click, or red -- a missing control must not take the whole run down."""
    if not pg.evaluate("s=>{const e=document.querySelector(s);"
                       "return !!(e&&e.getClientRects().length)}", sel):
        bad("%s %s is not on screen" % (tag, what))
        return False
    pg.click(sel, timeout=2000)
    return True


def check_cancel(pg, w, label):
    check_cancel_screens(pg, w, label)
    check_cancel_reasons(pg, w, label)
    check_calendar(pg, w, label)
    check_cancel_chain(pg, w, label)
    check_restart(pg, w, label)


def check_cancel_screens(pg, w, label):
    """Shell, prose and CTA of the five funnel sheets."""
    for name in CANCEL_SCREENS:
        node, height, title, cta = CANCEL_SCREENS[name]
        tag = "%s [%s]" % (label, name)
        sel = _panel(name)
        _open(pg, name)

        got = pg.evaluate(r"""a=>{const p=document.querySelector(a[0]);
            if(!p)return null;
            const q=s=>p.querySelector(s);
            const cs=e=>e?getComputedStyle(e):null;
            const r=e=>e?e.getBoundingClientRect():null;
            const box=q('.gb-acct-modal__panel');
            const head=q('.gb-acct-modal__head'), foot=q('.gb-acct-modal__foot');
            const bodyEl=q('.gb-acct-modal__body');
            const lead=q('.gb-acct-modal__lead');
            const sub=q('.gb-acct-modal__sub');
            const act=q('[data-acct-cta]');
            const now=q('.gb-acct-modal__foot .gb-acct-link');
            const bb=cs(bodyEl);
            return {sheet:p.classList.contains('gb-acct-modal--sheet'),
                    title:q('.gb-acct-modal__title')?
                          q('.gb-acct-modal__title').textContent.trim():null,
                    headH:head?Math.round(r(head).height):null,
                    footH:foot?Math.round(r(foot).height):null,
                    bodyPadY:bb&&bb.paddingTop, bodyPadX:bb&&bb.paddingLeft,
                    lenis:!!bodyEl&&bodyEl.hasAttribute('data-lenis-prevent'),
                    lead:lead?lead.textContent.trim():null,
                    leadColor:lead?cs(lead).color:null,
                    leadSize:lead?cs(lead).fontSize:null,
                    sub:sub?sub.textContent.trim():null,
                    subColor:sub?cs(sub).color:null,
                    leadGap:(lead&&sub)?Math.round(r(sub).top-r(lead).bottom):null,
                    cta:act?act.textContent.trim():null,
                    ctaH:act?Math.round(r(act).height):null,
                    ctaBg:act?cs(act).backgroundColor:null,
                    now:now?now.textContent.trim():null}}""", [sel])
        if got is None:
            bad("%s panel missing" % tag)
            continue

        if got["sheet"]:
            good(tag)
        else:
            bad("%s is not a --sheet; board %s is the 672 drawer" % (tag, node))
        if got["title"] == title:
            good(tag)
        else:
            bad("%s head reads %r, board %s says %r" % (tag, got["title"], node, title))
        for key, want in (("headH", 64), ("footH", 80)):
            if got[key] == want:
                good(tag)
            else:
                bad("%s %s=%s want %s" % (tag, key, got[key], want))
        if got["bodyPadY"] == "32px":
            good(tag)
        else:
            bad("%s body padding-top %s, the drawer boards are 32" % (tag, got["bodyPadY"]))
        if got["bodyPadX"] == (PAD_PHONE if w <= 767 else PAD_DESK):
            good(tag)
        else:
            bad("%s body gutter %s at %d" % (tag, got["bodyPadX"], w))
        if got["lenis"]:
            good(tag)
        else:
            bad("%s body has no data-lenis-prevent" % tag)

        # every one of the five opens with a 16/24 #101828 lead line
        if got["leadColor"] == LEAD and got["leadSize"] == "16px":
            good(tag)
        else:
            bad("%s lead is %s/%s, the boards are #101828 16/24"
                % (tag, got["leadColor"], got["leadSize"]))
        # ...and the ones with a second line draw it #666666, 16 below
        if got["sub"] is None:
            good(tag)                                    # 29596 has one line only
        elif got["subColor"] == GREY6 and got["leadGap"] == 16:
            good(tag)
        else:
            bad("%s second line is %s, %s below -- boards are #666666 at 16"
                % (tag, got["subColor"], got["leadGap"]))

        if got["cta"] == cta:
            good(tag)
        else:
            bad("%s CTA reads %r, board %s says %r" % (tag, got["cta"], node, cta))
        want_bg = GREY if name == "cancel-reason" else GREEN
        if got["ctaH"] == 40 and got["ctaBg"] == want_bg:
            good(tag)
        else:
            bad("%s CTA is %spx %s, want 40 tall and %s -- the funnel boards draw "
                "it green, but 29928 only does so with a reason picked"
                % (tag, got["ctaH"], got["ctaBg"], want_bg))
        # 29767 is the one screen whose foot has no "Cancel now"
        want_now = None if name == "cancel-skipped" else "Cancel now"
        if got["now"] == want_now:
            good(tag)
        else:
            bad("%s foot link is %r, board %s has %r" % (tag, got["now"], node, want_now))

        if w <= 767:
            pg.set_viewport_size({"width": 390, "height": 840})
            pg.wait_for_timeout(300)
            h = pg.evaluate("a=>Math.round(document.querySelector(a[0]+"
                            "' .gb-acct-modal__panel').getBoundingClientRect().height)", [sel])
            if h == height:
                good(tag)
            else:
                bad("%s sheet %spx in a 840 viewport, board %s is %s"
                    % (tag, h, node, height))
            pg.set_viewport_size({"width": w, "height": 900})
            pg.wait_for_timeout(300)

        pg.keyboard.press("Escape")
        pg.wait_for_timeout(600)

    # 29596's video block is a placeholder: the board's Image rectangle is a flat
    # #d9d9d9 with no imageRef, exactly like the subscription thumbnails.
    tag = "%s [cancel-offer-skip]" % label
    sel = _panel("cancel-offer-skip")
    _open(pg, "cancel-offer-skip")
    vid = pg.evaluate(r"""a=>{const p=document.querySelector(a[0]);
        const v=p.querySelector('.gb-acct-video');
        const play=p.querySelector('.gb-acct-video__play');
        if(!v)return null;
        const r=e=>e.getBoundingClientRect();
        const cs=e=>getComputedStyle(e);
        return {w:Math.round(r(v).width), h:Math.round(r(v).height),
                bg:cs(v).backgroundColor, radius:cs(v).borderTopLeftRadius,
                playW:play?Math.round(r(play).width):null,
                playH:play?Math.round(r(play).height):null,
                playBg:play?cs(play).backgroundColor:null,
                playR:play?cs(play).borderTopLeftRadius:null,
                glyph:!!(play&&play.querySelector('svg'))}}""", [sel])
    if vid is None:
        bad("%s no .gb-acct-video -- board 29750 draws one" % tag)
    else:
        for key, want, why in (("h", 190, "board 29750 is 350x190"),
                               ("bg", "rgb(217, 217, 217)", "board 29751 is a flat #d9d9d9"),
                               ("playW", 62, "board 29752 is 61.8 wide"),
                               ("playH", 39, "board 29752 is 38.6 tall"),
                               ("playBg", "rgb(255, 255, 255)", "board 29752 is white"),
                               ("glyph", True, "board 29753 is the triangle")):
            if vid[key] == want:
                good(tag)
            else:
                bad("%s video %s=%s want %s -- %s" % (tag, key, vid[key], want, why))
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(600)


def check_cancel_reasons(pg, w, label):
    """The seven rows, and the CTA that follows the pick (note 34512)."""
    tag = "%s [cancel-reason]" % label
    sel = _panel("cancel-reason")
    _open(pg, "cancel-reason")

    got = pg.evaluate(r"""a=>{const p=document.querySelector(a[0]);
        if(!p)return null;
        const cs=e=>getComputedStyle(e);
        const r=e=>e.getBoundingClientRect();
        const rows=[...p.querySelectorAll('.gb-acct-reason')];
        const inputs=[...p.querySelectorAll('[data-acct-reason]')];
        const list=p.querySelector('.gb-acct-reasons');
        const cta=p.querySelector('[data-acct-cta]');
        const first=rows[0];
        return {count:rows.length,
                labels:rows.map(e=>e.textContent.trim()),
                values:inputs.map(e=>e.value),
                names:[...new Set(inputs.map(e=>e.name))],
                types:[...new Set(inputs.map(e=>e.type))],
                checked:inputs.filter(e=>e.checked).length,
                listGap:list?cs(list).rowGap:null,
                rowH:first?Math.round(r(first).height):null,
                rowPadY:first?cs(first).paddingTop:null,
                rowPadX:first?cs(first).paddingLeft:null,
                rowGap:first?cs(first).columnGap:null,
                rowR:first?cs(first).borderTopLeftRadius:null,
                rowBg:first?cs(first).backgroundColor:null,
                rowBorder:first?cs(first).borderTopColor:null,
                rowBorderW:first?cs(first).borderTopWidth:null,
                labelColor:first?cs(first.querySelector('.gb-acct-reason__label')).color:null,
                ctaDisabled:cta?cta.disabled:null,
                ctaText:cta?cta.textContent.trim():null}}""", [sel])
    if got is None:
        bad("%s panel missing" % tag)
        return

    want_labels = [r[1] for r in REASONS]
    if got["labels"] == want_labels:
        good(tag)
    else:
        bad("%s rows read %r, boards 29928/30286 read %r" % (tag, got["labels"], want_labels))
    if got["values"] == [r[0] for r in REASONS]:
        good(tag)
    else:
        bad("%s reason values %r" % (tag, got["values"]))
    # one pick, not many: the board fills a single circle
    if got["types"] == ["radio"] and len(got["names"]) == 1:
        good(tag)
    else:
        bad("%s rows are %s across %d names, want one radio group"
            % (tag, got["types"], len(got["names"])))
    # no board shows the screen before a pick, so it ships with none made and the
    # CTA asleep -- SPEC 待裁决 W
    if got["checked"] == 0:
        good(tag)
    else:
        bad("%s ships with %d reasons picked" % (tag, got["checked"]))
    if got["ctaDisabled"] is True:
        good(tag)
    else:
        bad("%s CTA starts disabled=%s: with no reason picked there is nothing "
            "to continue to" % (tag, got["ctaDisabled"]))

    if got["listGap"] == "12px":
        good(tag)
    else:
        bad("%s rows are %s apart, board 30082 is 12" % (tag, got["listGap"]))
    # 30083 has strokesIncludedInLayout true: 12 + 20 + 12 + two 1px borders = 46
    for key, want, why in (("rowH", 46, "board 30083 is 46 with the border counted"),
                           ("rowPadY", "12px", "board pads 12 top and bottom"),
                           ("rowPadX", "16px", "board pads 16 each side"),
                           ("rowGap", "16px", "radio to label is 16"),
                           ("rowR", "8px", "board radius is 8"),
                           ("rowBorderW", "1px", "the stroke is counted in the 46"),
                           ("rowBg", "rgb(255, 255, 255)", "an unpicked row is white"),
                           ("rowBorder", CCC, "an unpicked row is #cccccc"),
                           ("labelColor", NAVY, "the label is #101828")):
        if got[key] == want:
            good(tag)
        else:
            bad("%s row %s=%s want %s -- %s" % (tag, key, got[key], want, why))

    # -- the pick drives the row's fill, the CTA's words and where it goes
    for value, text, nxt, cta_text in REASONS:
        rsel = sel + " [data-acct-reason][value='%s']" % value
        if not pg.evaluate("s=>!!document.querySelector(s)", rsel):
            bad("%s no radio for %r" % (tag, value))
            continue
        if not _click(pg, rsel, tag, "radio %s" % value):
            continue
        pg.wait_for_timeout(300)
        st = pg.evaluate(r"""a=>{const p=document.querySelector(a[0]);
            const inp=p.querySelector(a[1]);
            const row=inp.closest('.gb-acct-reason');
            const cta=p.querySelector('[data-acct-cta]');
            const cs=getComputedStyle(row);
            return {bg:cs.backgroundColor, border:cs.borderTopColor,
                    ctaBg:getComputedStyle(cta).backgroundColor,
                    text:cta.textContent.trim(), disabled:cta.disabled,
                    to:cta.getAttribute('data-acct-modal'),
                    closes:cta.hasAttribute('data-acct-modal-close')}}""",
            [sel, "[data-acct-reason][value='%s']" % value])
        if st["bg"] == SEL_ROW and st["border"] == GREEN:
            good(tag)
        else:
            bad("%s picked %s stays %s/%s, board 30083 fills it #e6f5e1 with a "
                "#005635 edge" % (tag, value, st["bg"], st["border"]))
        if st["text"] == cta_text and st["disabled"] is False and st["ctaBg"] == GREEN:
            good(tag)
        else:
            bad("%s picking %s gives CTA %r disabled=%s %s, boards say %r, live, green"
                % (tag, value, st["text"], st["disabled"], st["ctaBg"], cta_text))
        # note 34512: only the first two have anywhere to go
        if st["to"] == nxt:
            good(tag)
        else:
            bad("%s picking %s points the CTA at %r, want %r (note 34512)"
                % (tag, value, st["to"], nxt))
        if st["closes"] is (nxt is None):
            good(tag)
        else:
            bad("%s picking %s: CTA closes=%s, want %s -- a terminal reason ends "
                "the flow, a branching one must not" % (tag, value, st["closes"], nxt is None))

    pg.keyboard.press("Escape")
    pg.wait_for_timeout(600)


def check_calendar(pg, w, label):
    """30465's date picker. Tokens from the board, the grid from the clock."""
    tag = "%s [cancel-holiday]" % label
    sel = _panel("cancel-holiday")
    _open(pg, "cancel-holiday")

    got = pg.evaluate(r"""a=>{const p=document.querySelector(a[0]);
        const cal=p&&p.querySelector('.gb-acct-cal');
        if(!cal)return null;
        const cs=e=>getComputedStyle(e);
        const r=e=>e.getBoundingClientRect();
        const head=cal.querySelector('.gb-acct-cal__head');
        const title=cal.querySelector('[data-acct-cal-title]');
        const grid=cal.querySelector('table');
        const ths=[...cal.querySelectorAll('thead th')];
        const cells=[...cal.querySelectorAll('tbody button')];
        const sel1=cells.filter(c=>c.getAttribute('aria-pressed')==='true');
        const out=cells.filter(c=>c.dataset.acctCalOut!==undefined);
        const dis=cells.filter(c=>c.disabled);
        const one=cells[0];
        const today=new Date(); today.setHours(0,0,0,0);
        const enabled=cells.filter(c=>!c.disabled);
        return {calW:Math.round(r(cal).width), calH:Math.round(r(cal).height),
                calBg:cs(cal).backgroundColor, calR:cs(cal).borderTopLeftRadius,
                contentPadY:cs(cal.querySelector('.gb-acct-cal__content')).paddingTop,
                contentPadX:cs(cal.querySelector('.gb-acct-cal__content')).paddingLeft,
                headH:head?Math.round(r(head).height):null,
                titleSize:title?cs(title).fontSize:null,
                titleWeight:title?cs(title).fontWeight:null,
                titleColor:title?cs(title).color:null,
                title:title?title.textContent.trim():null,
                dayNames:ths.map(e=>e.textContent.trim()),
                dayWeight:ths.length?cs(ths[0]).fontWeight:null,
                dayColor:ths.length?cs(ths[0]).color:null,
                cellCount:cells.length,
                gridStart:cells.length?cells[0].dataset.acctCalDay:null,
                gridEnd:cells.length?cells[cells.length-1].dataset.acctCalDay:null,
                captionH:cal.querySelector('caption')?
                         Math.round(r(cal.querySelector('caption')).height):null,
                cellH:one?Math.round(r(one).height):null,
                cellR:one?cs(one).borderTopLeftRadius:null,
                colGap:grid?cs(grid).borderSpacing:null,
                selCount:sel1.length,
                selBg:sel1.length?cs(sel1[0]).backgroundColor:null,
                selColor:sel1.length?cs(sel1[0]).color:null,
                selIso:sel1.length?sel1[0].dataset.acctCalDay:null,
                outColor:out.length?cs(out[0]).color:null,
                outDisabled:out.every(c=>c.disabled),
                firstEnabled:enabled.length?enabled[0].dataset.acctCalDay:null,
                disabledCount:dis.length,
                prev:!!cal.querySelector('[data-acct-cal-prev]'),
                next:!!cal.querySelector('[data-acct-cal-next]'),
                todayIso:new Date(today.getTime()-today.getTimezoneOffset()*60000)
                          .toISOString().slice(0,10)}}""", [sel])
    if got is None:
        bad("%s no .gb-acct-cal -- board 30621 draws a date picker" % tag)
        pg.keyboard.press("Escape")
        pg.wait_for_timeout(600)
        return

    for key, want, why in (("calBg", "rgb(255, 255, 255)", "board 30621 is white"),
                           ("calR", "8px", "board radius is 8"),
                           ("contentPadY", "20px", "board 30623 pads 20 top"),
                           ("contentPadX", "24px", "board 30623 pads 24 side"),
                           ("headH", 32, "board 30625 is 32 tall"),
                           ("titleSize", "16px", "30627 is 16/24"),
                           ("titleWeight", "500", "30627 is w500"),
                           ("titleColor", GREY7, "30627 is #4d4d4d"),
                           ("cellH", 40, "30631 cells are 40 tall"),
                           ("cellR", "20px", "30631 radius is 20"),
                           ("dayWeight", "500", "the Mo/Tu row is w500"),
                           ("dayColor", GREY7, "the Mo/Tu row is #4d4d4d"),
                           ("prev", True, "30626 is the back arrow"),
                           ("next", True, "30628 is the forward arrow")):
        if got[key] == want:
            good(tag)
        else:
            bad("%s calendar %s=%s want %s -- %s" % (tag, key, got[key], want, why))

    # 30631..30643 verbatim, "Sat" included: three letters where the rest are two
    want_days = ["Mo", "Tu", "We", "Th", "Fr", "Sat", "Su"]
    if got["dayNames"] == want_days:
        good(tag)
    else:
        bad("%s day row %r, board reads %r (Sat really is three letters)"
            % (tag, got["dayNames"], want_days))

    # the grid is generated, so these are the invariants the board cannot give
    # whole Monday-first weeks, and no more of them than the month needs: an
    # off-by-one at either end silently adds a seventh row of the next month
    start = datetime.date.fromisoformat(got["gridStart"])
    end = datetime.date.fromisoformat(got["gridEnd"])
    view = datetime.date.fromisoformat(got["selIso"]).replace(day=1)
    nxt = (view.replace(day=28) + datetime.timedelta(days=4)).replace(day=1)
    span = (nxt - view).days
    want_start = view - datetime.timedelta(days=view.weekday())
    want_end = want_start + datetime.timedelta(days=((view.weekday() + span + 6) // 7) * 7 - 1)
    if (start, end) == (want_start, want_end):
        good(tag)
    else:
        bad("%s grid runs %s..%s, the whole weeks around this month are %s..%s"
            % (tag, start, end, want_start, want_end))
    if got["cellCount"] == (want_end - want_start).days + 1:
        good(tag)
    else:
        bad("%s %d cells for a %s..%s grid" % (tag, got["cellCount"], start, end))
    # the caption names the grid for a reader without being drawn
    if got["captionH"] in (0, 1):
        good(tag)
    else:
        bad("%s the table caption is %spx tall -- it should not draw" % (tag, got["captionH"]))
    if got["selCount"] == 1:
        good(tag)
    else:
        bad("%s %d days selected, board 30669 fills exactly one" % (tag, got["selCount"]))
    if got["selBg"] == GREEN and got["selColor"] == "rgb(255, 255, 255)":
        good(tag)
    else:
        bad("%s picked day is %s on %s, board is white on #005635"
            % (tag, got["selColor"], got["selBg"]))
    if got["outColor"] == GREY8 and got["outDisabled"]:
        good(tag)
    else:
        bad("%s days outside the month are %s / disabled=%s, board greys them #808080"
            % (tag, got["outColor"], got["outDisabled"]))
    # note 30923: the resume day has to be a whole future day, so today is out
    tomorrow = (datetime.date.fromisoformat(got["todayIso"])
                + datetime.timedelta(days=1)).isoformat()
    if got["firstEnabled"] == tomorrow:
        good(tag)
    else:
        bad("%s first selectable day is %s, note 30923 makes it %s -- today and "
            "earlier are not whole future days" % (tag, got["firstEnabled"], tomorrow))
    if got["selIso"] == tomorrow:
        good(tag)
    else:
        bad("%s opens with %s picked, want the first selectable day %s"
            % (tag, got["selIso"], tomorrow))
    if got["disabledCount"] > 0:
        good(tag)
    else:
        bad("%s nothing is disabled -- the past-day gate is not running" % tag)

    # picking a different day moves the fill
    moved = pg.evaluate(r"""a=>{const p=document.querySelector(a[0]);
        if(!p)return null;
        const cells=[...p.querySelectorAll('.gb-acct-cal tbody button')].filter(c=>!c.disabled);
        if(cells.length<2)return null;
        cells[1].click();
        const on=[...p.querySelectorAll('.gb-acct-cal tbody button')]
                 .filter(c=>c.getAttribute('aria-pressed')==='true');
        return {n:on.length, day:on.length?on[0].dataset.acctCalDay:null,
                want:cells[1].dataset.acctCalDay}}""", [sel])
    if moved is None:
        bad("%s fewer than two selectable days to test the pick on" % tag)
    elif moved["n"] == 1 and moved["day"] == moved["want"]:
        good(tag)
    else:
        bad("%s after clicking %s the fill is on %s (%d selected)"
            % (tag, moved["want"], moved["day"], moved["n"]))

    # the month arrows move the grid
    stepped = pg.evaluate(r"""a=>{const p=document.querySelector(a[0]);
        if(!p||!p.querySelector('[data-acct-cal-title]'))return null;
        const t=()=>p.querySelector('[data-acct-cal-title]').textContent.trim();
        const before=t();
        p.querySelector('[data-acct-cal-next]').click();
        const fwd=t();
        p.querySelector('[data-acct-cal-prev]').click();
        return {before:before, fwd:fwd, back:t()}}""", [sel])
    if stepped is None:
        bad("%s no month title to step" % tag)
    elif stepped["fwd"] != stepped["before"] and stepped["back"] == stepped["before"]:
        good(tag)
    else:
        bad("%s month arrows: %r -> %r -> %r"
            % (tag, stepped["before"], stepped["fwd"], stepped["back"]))

    pg.keyboard.press("Escape")
    pg.wait_for_timeout(600)


def check_cancel_chain(pg, w, label):
    """Walking the funnel keeps one lock and measures the scrollbar once."""
    tag = "%s [cancel-flow]" % label
    set_state(pg, BASE_STATE)
    pg.evaluate("""()=>{window.__sbw=0;
        const st=document.documentElement.style;
        const orig=st.setProperty.bind(st);
        st.setProperty=function(k,v){if(k==='--scrollbar-w')window.__sbw++;
                                     return orig(k,v)}}""")

    # the entry point is the offer, not the reason list
    pg.click("[data-acct-view='detail'] [data-acct-modal='cancel-offer-skip']", timeout=2000)
    pg.wait_for_timeout(500)
    here = pg.evaluate("()=>{const e=document.querySelector('.gb-acct-modal.is-open');"
                       "return e?e.getAttribute('data-acct-modal-panel'):null}")
    if here == "cancel-offer-skip":
        good(tag)
    else:
        bad("%s Cancel Subscription opened %r, board order puts 29596 first"
            % (tag, here))

    steps = [
        (_panel("cancel-offer-skip") + " [data-acct-cta]", "cancel-skipped"),
    ]
    for click_sel, want in steps:
        if not _click(pg, click_sel, tag, "the offer CTA"):
            continue
        pg.wait_for_timeout(600)
        here = pg.evaluate("()=>{const e=document.querySelector('.gb-acct-modal.is-open');"
                           "return e?e.getAttribute('data-acct-modal-panel'):null}")
        if here == want:
            good(tag)
        else:
            bad("%s %s led to %r, want %r" % (tag, click_sel, here, want))

    # back to the offer, then out through "Cancel now" into the reason list
    pg.evaluate("()=>window.gumiAcct.modal.open('cancel-offer-skip')")
    pg.wait_for_timeout(500)
    _click(pg, _panel("cancel-offer-skip") + " .gb-acct-modal__foot .gb-acct-link",
           tag, "'Cancel now' on the offer")
    pg.wait_for_timeout(600)
    here = pg.evaluate("()=>{const e=document.querySelector('.gb-acct-modal.is-open');"
                       "return e?e.getAttribute('data-acct-modal-panel'):null}")
    if here == "cancel-reason":
        good(tag)
    else:
        bad("%s 'Cancel now' on the offer led to %r, want cancel-reason -- note "
            "34516 wants the reason recorded before the cancel" % (tag, here))

    # branch through to the holiday screen, then check the lock survived it all
    if _click(pg, _panel("cancel-reason") + " [data-acct-reason][value='going-away']",
              tag, "the Going away radio"):
        pg.wait_for_timeout(300)
        _click(pg, _panel("cancel-reason") + " [data-acct-cta]", tag, "the reason CTA")
    pg.wait_for_timeout(600)
    st = pg.evaluate("""()=>({open:(document.querySelector('.gb-acct-modal.is-open')||{})
            .getAttribute?.('data-acct-modal-panel')||null,
        n:document.querySelectorAll('.gb-acct-modal.is-open').length,
        locked:document.documentElement.classList.contains('is-modal-open'),
        sbw:window.__sbw,
        headerTop:Math.round(document.querySelector('.gb-acct-header')
                  .getBoundingClientRect().top)})""")
    if st["open"] == "cancel-holiday":
        good(tag)
    else:
        bad("%s Going away led to %r, want cancel-holiday" % (tag, st["open"]))
    if st["n"] == 1:
        good(tag)
    else:
        bad("%s %d panels open after walking the funnel, want 1" % (tag, st["n"]))
    if st["locked"]:
        good(tag)
    else:
        bad("%s the lock was dropped somewhere in the funnel" % tag)
    # ⚠ the whole point of chaining through open(): four screens, one measurement
    if st["sbw"] == 1:
        good(tag)
    else:
        bad("%s --scrollbar-w was written %s times walking four screens -- the "
            "second reading is 0 and wipes the compensation" % (tag, st["sbw"]))
    if st["headerTop"] >= 0:
        good(tag)
    else:
        bad("%s sticky header top=%s during the funnel" % (tag, st["headerTop"]))

    # a terminal reason ends it: the CTA closes rather than opening a sixth screen
    pg.evaluate("()=>window.gumiAcct.modal.open('cancel-reason')")
    pg.wait_for_timeout(500)
    if _click(pg, _panel("cancel-reason") + " [data-acct-reason][value='taste-texture']",
              tag, "the Taste or texture radio"):
        pg.wait_for_timeout(300)
        _click(pg, _panel("cancel-reason") + " [data-acct-cta]", tag, "the reason CTA")
    pg.wait_for_timeout(700)
    end = pg.evaluate("""()=>({n:document.querySelectorAll('.gb-acct-modal.is-open').length,
        locked:document.documentElement.classList.contains('is-modal-open')})""")
    if end["n"] == 0 and end["locked"] is False:
        good(tag)
    else:
        bad("%s a terminal reason left %d panels open (locked=%s) -- note 34512 "
            "says there is no second screen" % (tag, end["n"], end["locked"]))


def check_restart(pg, w, label):
    tag = "%s [restart]" % label
    sel = _panel("restart")
    _open(pg, "restart")

    got = pg.evaluate(r"""a=>{const p=document.querySelector(a[0]);
        if(!p)return null;
        const q=s=>p.querySelector(s);
        const cs=e=>e?getComputedStyle(e):null;
        const r=e=>e?e.getBoundingClientRect():null;
        const body=q('.gb-acct-modal__body');
        const lead=q('.gb-acct-modal__lead');
        const field=q('.gb-acct-field__input');
        const save=q('[data-acct-save]');
        const hint=q('.gb-acct-modal__hint');
        const bb=cs(body);
        return {sheet:p.classList.contains('gb-acct-modal--sheet'),
                h:Math.round(r(q('.gb-acct-modal__panel')).height),
                footH:q('.gb-acct-modal__foot')?
                      Math.round(r(q('.gb-acct-modal__foot')).height):null,
                bodyPadY:bb&&bb.paddingTop,
                bodyGap:q('.gb-acct-flow')?cs(q('.gb-acct-flow')).rowGap:null,
                title:q('.gb-acct-modal__title').textContent.trim(),
                lead:lead?lead.textContent.trim():null,
                value:field?field.value:null,
                icon:!!q('.gb-acct-field__icon'),
                hint:hint?cs(hint).fontSize:null,
                saveDisabled:save?save.disabled:null,
                ungated:p.hasAttribute('data-acct-save-ungated')}}""", [sel])
    if got is None:
        bad("%s panel missing" % tag)
        return

    # 34339 is a 329 card, not the 672 drawer the rest of this task uses
    if got["sheet"] is False:
        good(tag)
    else:
        bad("%s is a --sheet; board 34339 is a centred 329 card" % tag)
    if w <= 767:
        if abs(got["h"] - 329) <= 2:
            good(tag)
        else:
            bad("%s panel %spx tall, board 2284:34192 is 329" % (tag, got["h"]))
    if got["footH"] == 72:
        good(tag)
    else:
        bad("%s foot %s, board 34349 is 72 (not the drawer's 80)" % (tag, got["footH"]))
    # 34344 pads 20 and gaps 15 -- neither the 24/20 card ramp nor the drawer's 32
    if got["bodyGap"] == "15px":
        good(tag)
    else:
        bad("%s body gap %s, board 34344 is 15" % (tag, got["bodyGap"]))
    if got["title"] == "Restart subscoption":
        good(tag)
    else:
        bad("%s title %r -- the board's own misspelling is kept (SPEC 8)"
            % (tag, got["title"]))
    if got["lead"] == "Select a restart date":
        good(tag)
    else:
        bad("%s lead %r, board 34345 says 'Select a restart date'" % (tag, got["lead"]))
    if got["value"] == "22/07/2026":
        good(tag)
    else:
        bad("%s date field %r, board is 22/07/2026" % (tag, got["value"]))
    if got["icon"]:
        good(tag)
    else:
        bad("%s no trailing calendar glyph -- 34347 draws one" % tag)
    if got["hint"] == "12px":
        good(tag)
    else:
        bad("%s note is %s, board 34348 is 12/18" % (tag, got["hint"]))
    # ⚠ 34351 is GREEN while edit-date's identical-looking Save (31976) is grey.
    # Both are opt-in: the panel says so, rather than the difference hiding in a
    # missing attribute.
    if got["saveDisabled"] is False and got["ungated"]:
        good(tag)
    else:
        bad("%s Save disabled=%s ungated=%s -- board 34351 draws it green"
            % (tag, got["saveDisabled"], got["ungated"]))

    pg.keyboard.press("Escape")
    pg.wait_for_timeout(600)


def main():
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=str(CHROME))
        for w in WIDTHS:
            run_width(b, w)
        b.close()
    for a in aborted:
        print("ABORT  " + a)
    print("\n%d ok / %d red%s" % (ok, red, " / %d aborted" % len(aborted) if aborted else ""))
    sys.exit(1 if red else 0)


main()
