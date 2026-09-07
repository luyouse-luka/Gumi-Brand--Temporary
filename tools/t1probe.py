#!/usr/bin/env python3
"""Task 1 skeleton check: account.html must render the shared header/footer
identically to an existing page, and the .wowo liveness gate must resolve."""
import json, os, sys
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.expanduser("~/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome")

PROBE = """() => {
  const g = (sel, props) => {
    const el = document.querySelector(sel);
    if (!el) return null;
    const cs = getComputedStyle(el);
    const o = {};
    props.forEach(p => o[p] = cs[p]);
    const r = el.getBoundingClientRect();
    o._box = [Math.round(r.width), Math.round(r.height)];
    return o;
  };
  const wowo = [...document.querySelectorAll('.wowo')].map(
    el => getComputedStyle(el).opacity);
  return {
    header: g('.gb-header', ['backgroundColor','position','zIndex','height']),
    footer: g('.gb-footer-wrap', ['backgroundColor','paddingTop']),
    ann:    g('.gb-announcement', ['backgroundColor','height']),
    cart:   !!document.getElementById('gb-cart'),
    gumi:   typeof window.gumi,
    acct:   typeof window.gumiAcct,
    htmlJs: document.documentElement.classList.contains('js'),
    views:  [...document.querySelectorAll('[data-acct-view]')].map(e => e.dataset.acctView),
    wowoHidden: wowo.filter(o => parseFloat(o) < 1).length,
    wowoTotal:  wowo.length,
  };
}"""

def snap(pw, page_name):
    b = pw.chromium.launch(executable_path=CH)
    p = b.new_page(viewport={"width": 1440, "height": 900})
    p.goto("file://" + os.path.join(ROOT, page_name))
    p.wait_for_timeout(2500)
    out = p.evaluate(PROBE)
    p.screenshot(path=os.path.join(ROOT, "tools", page_name.replace(".html", "") + "-t1.png"))
    b.close()
    return out

with sync_playwright() as pw:
    a = snap(pw, "account.html")
    b = snap(pw, "privacy-policy.html")

bad = 0
for key in ("header", "footer", "ann"):
    if a[key] != b[key]:
        print("  RED  %s differs\n       account=%s\n       privacy=%s" % (key, a[key], b[key]))
        bad += 1
    else:
        print("  ok   %-8s %s" % (key, json.dumps(a[key])))

checks = [
    ("cart drawer present", a["cart"] is True),
    ("main.js alive (window.gumi)", a["gumi"] == "object"),
    ("account.js alive (window.gumiAcct)", a["acct"] == "object"),
    ("html.js kept", a["htmlJs"] is True),
    ("three views", a["views"] == ["overview", "subscriptions", "detail"]),
    ("no .wowo left hidden", a["wowoHidden"] == 0),
]
for label, ok in checks:
    print("  %s %s" % ("ok  " if ok else "RED ", label))
    if not ok:
        bad += 1
print("  note .wowo elements on page: %d" % a["wowoTotal"])
print("\n  %s" % ("GREEN" if bad == 0 else "RED  %d problem(s)" % bad))
sys.exit(1 if bad else 0)
