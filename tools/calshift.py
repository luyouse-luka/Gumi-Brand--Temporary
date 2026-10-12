"""Opening a field calendar in a modal must not shift the panel's content.

The calendar makes .gb-acct-modal__body overflow, a classic scrollbar comes in,
and without compensation the field narrows/moves. Needs a real scrollbar, so
--hide-scrollbars is dropped and the viewport is short enough to overflow.

  python3 tools/calshift.py            # expect all ok
  python3 tools/calshift.py --strip    # compensation neutralised, expect red
  python3 tools/calshift.py --url https://gumi.com.au/account --password 1234
"""
import sys, pathlib, argparse
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = sorted((pathlib.Path.home() / ".cache/ms-playwright").glob(
    "chromium-*/chrome-linux64/chrome"))[-1]

ap = argparse.ArgumentParser()
ap.add_argument("--strip", action="store_true")
ap.add_argument("--url")
ap.add_argument("--password")
a = ap.parse_args()

ok = red = 0
def check(cond, msg):
    global ok, red
    if cond: ok += 1
    else:
        red += 1
        print("RED  " + msg)

MEASURE = """() => {
  const b = document.querySelector('.gb-acct-modal.is-open .gb-acct-modal__body');
  const i = b.querySelector('.gb-acct-field__input');
  const r = i.getBoundingClientRect();
  return {left: r.left, right: r.right, sbw: b.offsetWidth - b.clientWidth,
          oy: getComputedStyle(b).overflowY};
}"""

with sync_playwright() as p:
    br = p.chromium.launch(executable_path=str(CHROME),
                           ignore_default_args=["--hide-scrollbars"])
    for h in (600, 700):
        pg = br.new_page(viewport={"width": 1440, "height": h})
        if a.url:
            if a.password:
                pg.goto(a.url.split("/account")[0] + "/password")
                pg.request.post(pg.url, form={"form_type": "storefront_password",
                                              "utf8": "✓", "password": a.password})
            pg.goto(a.url)
        else:
            pg.goto((ROOT / "account.html").as_uri() + "#detail")
        pg.wait_for_timeout(800)
        if a.strip:
            pg.add_style_tag(content=".gb-acct-modal__body{padding-right:24px!important}")
        pg.evaluate("""() => { const t = [...document.querySelectorAll('[data-acct-modal="edit-date"]')]
                       .find(e => e.offsetParent); (t || document.querySelector('[data-acct-modal="edit-date"]')).click(); }""")
        pg.wait_for_timeout(700)
        before = pg.evaluate(MEASURE)
        pg.click(".gb-acct-modal.is-open .gb-acct-field__input")
        pg.wait_for_timeout(900)
        after = pg.evaluate(MEASURE)
        tag = f"1440x{h}"
        # liveness: the calendar must really have made the body scroll
        check(after["sbw"] > 0, f"{tag} no scrollbar after opening -- probe not exercising the bug {after}")
        check(abs(after["left"] - before["left"]) < 0.5, f"{tag} input left {before['left']} -> {after['left']}")
        check(abs(after["right"] - before["right"]) < 0.5, f"{tag} input right {before['right']} -> {after['right']}")
        pg.close()
    br.close()

print(f"{ok} ok / {red} red")
sys.exit(1 if red else 0)
