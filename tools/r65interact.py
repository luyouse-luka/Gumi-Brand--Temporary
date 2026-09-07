"""R65 interaction: the Delivers-every dropdown and the plan radios.

Driven through real clicks — a computed-style read cannot tell whether the
listbox actually opens.
"""
import sys
from playwright.sync_api import sync_playwright

CHROME = "/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome"
URL = "file:///home/ly/project/Gumi-Brand/pdp.html"

ok = red = 0
def chk(c, label):
    global ok, red
    if c: ok += 1
    else:
        red += 1
        print("  RED  " + label)

def state(p):
    return p.evaluate("""() => {
      const wrap = document.querySelector('.gb-sub__every .gb-select');
      const list = document.querySelector('.gb-sub__every .gb-select__list');
      const btn  = document.querySelector('.gb-sub__every .gb-select__button');
      const arrow= document.querySelector('.gb-sub__every .gb-select__arrow');
      const nat  = document.querySelector('.gb-sub__select');
      const cs = list ? getComputedStyle(list) : null;
      return {open: wrap ? wrap.classList.contains('is-open') : null,
              vis: cs && cs.visibility, opacity: cs && cs.opacity,
              expanded: btn && btn.getAttribute('aria-expanded'),
              arrow: arrow && getComputedStyle(arrow).transform,
              value: (document.querySelector('.gb-sub__every .gb-select__value')||{}).textContent.trim(),
              native: nat && nat.value,
              checked: [...document.querySelectorAll('.gb-sub__radio')].map(r => r.checked),
              dotBg: getComputedStyle(document.querySelector('.gb-sub__pick'), '::before').backgroundColor,
              onceBg: getComputedStyle(document.querySelector('.gb-sub__plan--once'), '::before').backgroundColor};
    }""")

for w in (1440, 390):
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME)
        p = b.new_context(viewport={"width": w, "height": 1000}).new_page()
        p.goto(URL, wait_until="load")
        p.wait_for_timeout(500)

        s0 = state(p)
        chk(s0["open"] is False, "%d list starts open" % w)
        chk(s0["vis"] == "hidden", "%d closed list visibility=%s" % (w, s0["vis"]))
        chk(s0["value"] == "4 Weeks", "%d initial value=%r" % (w, s0["value"]))
        chk(s0["checked"] == [True, False], "%d initial radios=%s" % (w, s0["checked"]))

        # open
        p.click(".gb-sub__every .gb-select__button")
        p.wait_for_timeout(350)
        s1 = state(p)
        chk(s1["open"] is True, "%d click did not open the list" % w)
        chk(s1["vis"] == "visible" and s1["opacity"] == "1",
            "%d open list vis=%s opacity=%s" % (w, s1["vis"], s1["opacity"]))
        chk(s1["expanded"] == "true", "%d aria-expanded=%s" % (w, s1["expanded"]))
        chk(s1["arrow"] not in (None, "none", s0["arrow"]),
            "%d chevron did not rotate: %s -> %s" % (w, s0["arrow"], s1["arrow"]))

        # pick "8 Weeks"
        p.click(".gb-sub__every .gb-select__option:nth-child(4)")
        p.wait_for_timeout(350)
        s2 = state(p)
        chk(s2["value"] == "8 Weeks", "%d after pick value=%r want '8 Weeks'" % (w, s2["value"]))
        chk(s2["native"] == "8 Weeks", "%d native select=%r not synced" % (w, s2["native"]))
        chk(s2["open"] is False, "%d list stayed open after picking" % w)
        chk(s2["vis"] == "hidden", "%d list not hidden after picking" % w)

        # the dropdown must not change the plan
        chk(s2["checked"] == [True, False],
            "%d using the dropdown changed the plan: %s" % (w, s2["checked"]))

        # switch plan by clicking the one-time card
        p.click(".gb-sub__plan--once")
        p.wait_for_timeout(250)
        s3 = state(p)
        chk(s3["checked"] == [False, True], "%d one-time card did not select: %s" % (w, s3["checked"]))
        chk(s3["onceBg"] == "rgb(0, 86, 53)", "%d one-time dot not filled: %s" % (w, s3["onceBg"]))
        chk(s3["dotBg"] != "rgb(0, 86, 53)", "%d subscribe dot still filled: %s" % (w, s3["dotBg"]))

        # and back via the subscribe row
        p.click(".gb-sub__pick")
        p.wait_for_timeout(250)
        s4 = state(p)
        chk(s4["checked"] == [True, False], "%d subscribe row did not re-select: %s" % (w, s4["checked"]))
        chk(s4["dotBg"] == "rgb(0, 86, 53)", "%d subscribe dot not filled: %s" % (w, s4["dotBg"]))
        b.close()

print("\n%d ok / %d red" % (ok, red))
sys.exit(1 if red else 0)
