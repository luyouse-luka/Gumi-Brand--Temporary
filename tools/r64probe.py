"""R64 baseline: card heights + faq row padding, live vs static."""
import subprocess, tempfile, os, sys
from playwright.sync_api import sync_playwright

CHROME = "/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome"
WIDTHS = [1440, 1280, 1199, 1024, 768, 575, 390]
PAGES = [("home", "https://gumi.com.au/", "file:///home/ly/project/Gumi-Brand/index.html"),
         ("faq", "https://gumi.com.au/pages/faq", "file:///home/ly/project/Gumi-Brand/faq.html")]

PROBE = """() => {
  const grp = (sel) => [...document.querySelectorAll(sel)].map(c => {
    const kids = [...c.children].map(k => ({cls: k.className.split(' ')[0],
      h: +k.getBoundingClientRect().height.toFixed(1),
      alignSelf: getComputedStyle(k).alignSelf}));
    return {rows: getComputedStyle(c).gridAutoRows, kids};
  });
  const rows = [...document.querySelectorAll('.gb-faq__row')].slice(0, 3).map(r => {
    const cs = getComputedStyle(r);
    return {pb: cs.paddingBottom, pt: cs.paddingTop,
            list: r.closest('[class*="__list"]') ? r.closest('[class*="__list"]').className : null};
  });
  return {science: grp('.gb-science__cards'), nutrition: grp('.gb-nutrition__cards'), rows};
}"""

def gate_cookie():
    jar = tempfile.mktemp()
    subprocess.run(["curl","-s","-c",jar,"-b",jar,"-o",os.devnull,"https://gumi.com.au/password"], check=True)
    subprocess.run(["curl","-s","-c",jar,"-b",jar,"-X","POST","-d",
                    "form_type=storefront_password&utf8=%E2%9C%93&password=1234",
                    "-o",os.devnull,"https://gumi.com.au/password"], check=True)
    out = []
    for line in open(jar):
        f = line.lstrip("#").replace("HttpOnly_", "").rstrip("\n").split("\t")
        if len(f) == 7 and f[5] == "_shopify_essential":
            out.append({"name": f[5], "value": f[6], "domain": "gumi.com.au", "path": "/"})
    os.unlink(jar)
    if not out: sys.exit("no _shopify_essential cookie")
    return out

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=CHROME)
    ctx = b.new_context(viewport={"width": 1440, "height": 900})
    ctx.add_cookies(gate_cookie())
    p = ctx.new_page()
    for name, live, static in PAGES:
        for side, url in (("live", live), ("static", static)):
            print("\n##### %s / %s" % (name, side))
            for w in WIDTHS:
                p.set_viewport_size({"width": w, "height": 900})
                p.goto(url, wait_until="load")
                p.wait_for_timeout(600)
                d = p.evaluate(PROBE)
                for key in ("science", "nutrition"):
                    for gi, g in enumerate(d[key]):
                        hs = [k["h"] for k in g["kids"]]
                        if not hs: continue
                        spread = max(hs) - min(hs)
                        flag = "" if spread <= 0.5 else "  <-- SPREAD %.1f" % spread
                        print("  %4d %-9s#%d rows=%-5s %s%s" % (w, key, gi, g["rows"], hs, flag))
                if d["rows"]:
                    print("  %4d faq rows pb=%s (list=%s)" % (w, [r["pb"] for r in d["rows"]],
                          (d["rows"][0]["list"] or "")[:28]))
    b.close()
