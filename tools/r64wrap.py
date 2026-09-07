"""Which structural selectors does Shopify's per-block <div class="shopify-block">
wrapper break?  Compares match counts live vs static, page by page."""
import subprocess, tempfile, os, sys
from playwright.sync_api import sync_playwright

CHROME = "/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome"
BASE = "/home/ly/project/Gumi-Brand"
PAGES = [("index", "https://gumi.com.au/"),
         ("faq", "https://gumi.com.au/pages/faq"),
         ("how-gumi-works", "https://gumi.com.au/pages/how-gumi-works"),
         ("our-story", "https://gumi.com.au/pages/our-story"),
         ("referral", "https://gumi.com.au/pages/referral"),
         ("reviews", "https://gumi.com.au/pages/reviews"),
         ("science", "https://gumi.com.au/pages/science"),
         ("shipping", "https://gumi.com.au/pages/shipping")]

SELECTORS = [
    ".gb-faq__item:last-child",
    ".gb-faq__item:first-child .gb-faq__row",
    ".gb-product__acc-item:last-child",
    ".gb-product__acc-item:first-child .gb-product__acc-row",
    ".gb-science__cards > :last-child:nth-child(odd)",
    ".gb-nutrition__cards > :last-child:nth-child(odd)",
    ".gb-vs__row + .gb-vs__row",
]
# the population each selector is filtering, so a count is readable
POP = [".gb-faq__item", ".gb-faq__item", ".gb-product__acc-item",
       ".gb-product__acc-item", ".gb-science__cards", ".gb-nutrition__cards", ".gb-vs__row"]

PROBE = """(sels) => {
  const out = {};
  for (const s of sels) { try { out[s] = document.querySelectorAll(s).length; }
                          catch (e) { out[s] = 'ERR'; } }
  out['__wrappers'] = document.querySelectorAll('div.shopify-block').length;
  return out;
}"""

def gate():
    jar = tempfile.mktemp()
    subprocess.run(["curl","-s","-c",jar,"-b",jar,"-o",os.devnull,
                    "https://gumi.com.au/password"], check=True)
    subprocess.run(["curl","-s","-c",jar,"-b",jar,"-X","POST","-d",
                    "form_type=storefront_password&utf8=%E2%9C%93&password=1234",
                    "-o",os.devnull,"https://gumi.com.au/password"], check=True)
    out = []
    for l in open(jar):
        f = l.lstrip("#").replace("HttpOnly_","").rstrip("\n").split("\t")
        if len(f) == 7 and f[5] == "_shopify_essential":
            out.append({"name":f[5],"value":f[6],"domain":"gumi.com.au","path":"/"})
    os.unlink(jar)
    if not out: sys.exit("no _shopify_essential cookie")
    return out

ALL = SELECTORS + POP
red = 0
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=CHROME)
    c = b.new_context(viewport={"width": 1440, "height": 900})
    c.add_cookies(gate())
    p = c.new_page()
    for name, live in PAGES:
        got = {}
        for side, url in (("live", live), ("static", "file://%s/%s.html" % (BASE, name))):
            p.goto(url, wait_until="load"); p.wait_for_timeout(400)
            got[side] = p.evaluate(PROBE, ALL)
        diffs = []
        for i, s in enumerate(SELECTORS):
            l, st = got["live"][s], got["static"][s]
            if l != st:
                diffs.append("    %-56s live=%-4s static=%-4s  (pop live=%s static=%s)"
                             % (s, l, st, got["live"][POP[i]], got["static"][POP[i]]))
        print("### %-16s wrappers=%-4d %s" % (name, got["live"]["__wrappers"],
                                              "OK" if not diffs else "BROKEN %d" % len(diffs)))
        for d in diffs: print(d)
        red += len(diffs)
    b.close()
print("\ntotal broken selector/page pairs:", red)
