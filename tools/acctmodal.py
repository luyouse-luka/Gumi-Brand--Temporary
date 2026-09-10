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
import sys, pathlib
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

    names = pg.evaluate(
        "()=>[...new Set([...document.querySelectorAll('[data-acct-modal]')]"
        ".map(e=>e.getAttribute('data-acct-modal')))]")
    if not names:
        bad("%s no [data-acct-modal] triggers found -- wrong page or wrong view" % label)
        pg.close()
        return

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
