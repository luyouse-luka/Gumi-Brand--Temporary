#!/usr/bin/env python3
"""Task 41 -- every view leaves the same gap above the wave at 390.

The gap is optical, not box: all nine views already ended 48 above the footer in
layout terms, so a computed-style probe reads green on the old behaviour too.
What differed was ink -- a view ending on the pager sat 14 lower because the 45
shell centres a 36 button whose arrow is a 20 viewBox. So the measurement is
pixels: screenshot the strip above the wave and walk up until a row is no longer
page background.

⚠ The 51 on detail/details is a text line box's half-leading, not a defect --
they end on a paragraph, and pinning them to 48 would mean compensating for font
metrics. They are asserted at 51 so a future change to them still shows up.
"""
import sys, pathlib, io
from playwright.sync_api import sync_playwright
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent

# view -> ink gap above the footer wave at 390
WANT = {"overview": 48, "subscriptions": 48, "detail": 51, "orders": 48,
        "order": 48, "details": 51, "password": 48, "help": 48, "referral": 48}

ok = red = 0


def check(label, got, want):
    global ok, red
    if got == want:
        print("ok   %-52s %s" % (label, got)); ok += 1
    else:
        print("RED  %-52s got %r want %r" % (label, got, want)); red += 1


def _chrome():
    hits = sorted((pathlib.Path.home() / ".cache/ms-playwright").glob(
        "chromium-*/chrome-linux64/chrome"))
    if not hits:
        sys.exit("no chromium -- run: npx playwright install chromium")
    return str(hits[-1])


def ink_gap(pg, strip=140):
    """Rows above the wave that carry nothing but page background."""
    y = pg.evaluate("()=>document.querySelector('.gb-footer-wrap')"
                    ".getBoundingClientRect().top+window.scrollY")
    png = pg.screenshot(full_page=True,
                        clip={"x": 0, "y": y - strip, "width": 390, "height": strip})
    im = Image.open(io.BytesIO(png)).convert("RGB")
    bg = im.getpixel((5, 2))
    for row in range(im.height - 1, -1, -1):
        if any(sum(abs(a - c) for a, c in zip(im.getpixel((x, row)), bg)) > 24
               for x in range(0, 390, 2)):
            return im.height - 1 - row
    return None


with sync_playwright() as p:
    b = p.chromium.launch(executable_path=_chrome())

    # ----------------------------------------------------------------- 390
    ctx = b.new_context(viewport={"width": 390, "height": 844},
                        reduced_motion="reduce", device_scale_factor=1)
    pg = ctx.new_page()
    pg.goto((ROOT / "account.html").as_uri())
    pg.wait_for_timeout(600)

    for view, want in WANT.items():
        pg.evaluate("(n)=>{location.hash='#'+n}", view)
        pg.wait_for_timeout(750)          # Task 40: the exit animation runs 500
        check("390 ink gap above wave -- " + view, ink_gap(pg), want)

    # Anchors: without these the 48 above could come from a shorter pager or a
    # pager that stopped being the last block, and the rule would read green
    # while doing nothing.
    pg.evaluate("()=>{location.hash='#orders'}")
    pg.wait_for_timeout(750)
    SEL = "[data-acct-view='orders'] .gb-acct-pager"
    check("pager still exists", pg.locator(SEL).count(), 1)
    check("pager shell still 45 high", pg.eval_on_selector(
        SEL, "e=>e.getBoundingClientRect().height"), 45)
    check("pager still last in its stack", pg.eval_on_selector(
        SEL, "e=>e.parentElement.lastElementChild===e"), True)
    check("pager parent is the stack", pg.eval_on_selector(
        SEL, "e=>e.parentElement.classList.contains('gb-acct-stack')"), True)
    check("390 pager pull-up applied", pg.eval_on_selector(
        SEL, "e=>getComputedStyle(e).marginBottom"), "-14px")
    ctx.close()

    # ---------------------------------------------------------------- 1440
    # Only the phone was asked for; desktop's 144 keeps the pager untouched.
    ctx = b.new_context(viewport={"width": 1440, "height": 900},
                        reduced_motion="reduce", device_scale_factor=1)
    pg = ctx.new_page()
    pg.goto((ROOT / "account.html").as_uri() + "#orders")
    pg.wait_for_timeout(900)
    check("1440 pager untouched", pg.eval_on_selector(
        SEL, "e=>getComputedStyle(e).marginBottom"), "0px")
    check("1440 shell padding-bottom still 144", pg.eval_on_selector(
        ".gb-acct__inner", "e=>getComputedStyle(e).paddingBottom"), "144px")
    ctx.close()
    b.close()

print("\n%d ok / %d red" % (ok, red))
sys.exit(1 if red else 0)
