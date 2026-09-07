"""R64 assertions.

Three passes over the static pages:
  plain    — as shipped
  wrapped  — every element Shopify turns into a block is re-parented into a bare
             <div class="shopify-block">, reproducing the live DOM locally
  live     — the real site (needs --live; storefront password 1234)

The wrapped pass is the point: r64 exists because :first-child / :last-child /
width:100% all resolved against that wrapper on the live site.
"""
import subprocess, tempfile, os, sys

# Overturned by r81 (client): these two carry product photography.
CONTAIN_BOXES = {".gb-product__image", ".gb-product__thumb"}
from playwright.sync_api import sync_playwright

CHROME = "/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome"
BASE = "/home/ly/project/Gumi-Brand"
WIDTHS = [1440, 1200, 1024, 768, 575, 390]

# Mirror of Shopify's per-block wrapping: each of these gets its own bare div.
WRAP = """() => {
  const sets = ['.gb-faq__list > .gb-faq__item',
                '.gb-faq-image__list > .gb-faq__item',
                '.gb-product__accordion > .gb-product__acc-item',
                '.gb-dosed__inner > .gb-dosed__block',
                '.gb-science__cards > .gb-science-card',
                '.gb-nutrition__cards > .gb-highlight-card'];
  let n = 0;
  for (const sel of sets) for (const el of [...document.querySelectorAll(sel)]) {
    const w = document.createElement('div');
    w.className = 'shopify-block';
    el.parentNode.insertBefore(w, el);
    w.appendChild(el);
    n++;
  }
  return n;
}"""

PROBE = """() => {
  const px = v => Math.round(parseFloat(v) * 10) / 10;
  const out = {faq: [], dosed: [], cards: {}, halo: [], media: []};

  for (const list of document.querySelectorAll('.gb-faq__list, .gb-faq-image__list')) {
    const items = [...list.querySelectorAll('.gb-faq__item')];
    out.faq.push({list: list.className.split(' ')[0], n: items.length,
      rows: items.map(it => {
        const r = it.querySelector('.gb-faq__row'); const cs = getComputedStyle(r);
        return {pb: px(cs.paddingBottom), pt: px(cs.paddingTop),
                bt: px(cs.borderTopWidth), open: it.hasAttribute('open')};
      })});
  }

  const inner = document.querySelector('.gb-dosed__inner');
  if (inner) {
    const iw = inner.clientWidth - parseFloat(getComputedStyle(inner).paddingLeft)
                                 - parseFloat(getComputedStyle(inner).paddingRight);
    out.dosed = [...document.querySelectorAll('.gb-dosed__block')].map(b =>
      ({w: px(b.getBoundingClientRect().width), want: px(iw)}));
  }

  // Grouped per container: the site has two .gb-science__cards on one page and
  // only cards sharing a grid are meant to match.
  for (const sel of ['.gb-science__cards', '.gb-nutrition__cards']) {
    out.cards[sel] = [...document.querySelectorAll(sel)].map(grid => ({
      kids: [...grid.children].map(kid => {
        // the card is the kid itself, or the single child of a Shopify wrapper
        const card = kid.matches('.gb-science-card, .gb-highlight-card')
                   ? kid : kid.querySelector('.gb-science-card, .gb-highlight-card');
        return {slot: px(kid.getBoundingClientRect().height),
                card: card ? px(card.getBoundingClientRect().height) : null,
                wrapped: kid !== card};
      })}));
  }

  for (const h of document.querySelectorAll('.gb-ink-halo')) {
    const host = h.parentElement;
    // The reveal class only lands when the host scrolls into view, which a
    // headless page never does; the split itself already ran on ready.
    const added = !host.classList.contains('is-revealed');
    if (added) host.classList.add('is-revealed');
    const cs = getComputedStyle(h);
    const m0 = host.querySelector('.gb-line-mask__inner');
    out.halo.push({host: host.className.split(' ')[0],
      name: cs.animationName, delay: cs.animationDelay, dur: cs.animationDuration,
      lineDelay: m0 ? getComputedStyle(m0).animationDelay : null,
      lineDur: m0 ? getComputedStyle(m0).animationDuration : null,
      lines: host.querySelectorAll('.gb-line-mask').length,
      split: host.classList.contains('is-split')});
    if (added) host.classList.remove('is-revealed');
  }

  // inject a probe image into every grey placeholder and see if it fills
  const PLACE = ['.gb-acc-body__media', '.gb-cart-item__media', '.gb-cart__gift-media',
                 '.gb-page-hero__media', '.gb-highlight-card__media', '.gb-product__thumb',
                 '.gb-product__image', '.gb-promo-card__media', '.gb-faq-image__media'];
  for (const sel of PLACE) {
    const box = document.querySelector(sel);
    if (!box) continue;
    const probe = document.createElement('img');
    probe.dataset.r64 = '1';
    probe.src = 'data:image/svg+xml,' + encodeURIComponent(
      '<svg xmlns="http://www.w3.org/2000/svg" width="4" height="3"><rect width="4" height="3" fill="red"/></svg>');
    box.appendChild(probe);
    // content box, not border box: .gb-product__thumb carries a 2px border and
    // width:100% on the image resolves against the content box.
    const bw = box.clientWidth - parseFloat(getComputedStyle(box).paddingLeft)
                              - parseFloat(getComputedStyle(box).paddingRight);
    const bh = box.clientHeight - parseFloat(getComputedStyle(box).paddingTop)
                                - parseFloat(getComputedStyle(box).paddingBottom);
    const pr = probe.getBoundingClientRect();
    const cs = getComputedStyle(probe);
    out.media.push({sel, fit: cs.objectFit, disp: cs.display,
                    fills: Math.abs(pr.width - bw) < 1 && Math.abs(pr.height - bh) < 1,
                    boxOverflow: getComputedStyle(box).overflow,
                    radius: getComputedStyle(box).borderTopLeftRadius});
    probe.remove();
  }
  return out;
}"""

def gate():
    jar = tempfile.mktemp()
    for args in (["-o", os.devnull, "https://gumi.com.au/password"],
                 ["-X", "POST", "-d", "form_type=storefront_password&utf8=%E2%9C%93&password=1234",
                  "-o", os.devnull, "https://gumi.com.au/password"]):
        subprocess.run(["curl", "-s", "-c", jar, "-b", jar] + args, check=True)
    out = [{"name": f[5], "value": f[6], "domain": "gumi.com.au", "path": "/"}
           for f in (l.lstrip("#").replace("HttpOnly_", "").rstrip("\n").split("\t") for l in open(jar))
           if len(f) == 7 and f[5] == "_shopify_essential"]
    os.unlink(jar)
    if not out: sys.exit("no _shopify_essential cookie")
    return out

PAGES = [("faq", "https://gumi.com.au/pages/faq"),
         ("how-gumi-works", "https://gumi.com.au/pages/how-gumi-works"),
         ("index", "https://gumi.com.au/"),
         ("science", "https://gumi.com.au/pages/science"),
         ("pdp", None)]

ok = red = 0
def chk(cond, label):
    global ok, red
    if cond: ok += 1
    else:
        red += 1
        print("    RED  " + label)

live_mode = "--live" in sys.argv
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=CHROME)
    c = b.new_context(viewport={"width": 1440, "height": 900})
    if live_mode: c.add_cookies(gate())
    p = c.new_page()

    for name, liveurl in PAGES:
        modes = [("plain", "file://%s/%s.html" % (BASE, name), False),
                 ("wrapped", "file://%s/%s.html" % (BASE, name), True)]
        if live_mode and liveurl: modes.append(("live", liveurl, False))
        for mode, url, wrap in modes:
            for w in WIDTHS:
                p.set_viewport_size({"width": w, "height": 900})
                p.goto(url, wait_until="load")
                if wrap: p.evaluate(WRAP)
                p.wait_for_timeout(350)
                d = p.evaluate(PROBE)
                tag = "%s/%s/%d" % (name, mode, w)

                # 1. faq row gaps: closed rows carry the list's gap, the last one none
                for L in d["faq"]:
                    # .gb-faq__list is a flat 16 now; .gb-faq-image__list ramps
                    # 24 -> 16 across the tablet band, so only its ends are exact.
                    exact = 16.0 if L["list"] == "gb-faq__list" else (
                            24.0 if w <= 767 else (16.0 if w >= 1281 else None))
                    for i, r in enumerate(L["rows"]):
                        last, first = i == len(L["rows"]) - 1, i == 0
                        if r["open"] or last:
                            chk(r["pb"] == 0.0,
                                "%s %s row%d pb=%s want 0 (open/last)" % (tag, L["list"], i, r["pb"]))
                        elif exact is not None:
                            chk(r["pb"] == exact,
                                "%s %s row%d pb=%s want=%s" % (tag, L["list"], i, r["pb"], exact))
                        else:
                            chk(16.0 <= r["pb"] <= 24.0,
                                "%s %s row%d pb=%s outside the 16-24 ramp" % (tag, L["list"], i, r["pb"]))
                        if not first:
                            chk(r["bt"] > 0, "%s %s row%d lost its border-top" % (tag, L["list"], i))

                # 2. dosed blocks fill the inner's content box
                for i, blk in enumerate(d["dosed"]):
                    chk(abs(blk["w"] - blk["want"]) < 1.5,
                        "%s dosed block%d w=%s want=%s" % (tag, i, blk["w"], blk["want"]))

                # 3. cards fill their grid row
                for sel, grids in d["cards"].items():
                    for gi, g in enumerate(grids):
                        hs = [k["card"] for k in g["kids"] if k["card"] is not None]
                        if len(hs) > 1:
                            chk(max(hs) - min(hs) <= 0.6,
                                "%s %s#%d card heights %s" % (tag, sel, gi, hs))
                        # the card must fill its slot, wrapper or not
                        for ki, k in enumerate(g["kids"]):
                            if k["card"] is None: continue
                            chk(abs(k["card"] - k["slot"]) < 1.0,
                                "%s %s#%d kid%d card=%s slot=%s wrapped=%s"
                                % (tag, sel, gi, ki, k["card"], k["slot"], k["wrapped"]))

                # 4. halo timing — HANDED OVER TO tools/r67check.py.
                # This round only ever compared the halo against LINE 0, which is
                # exactly why a single whole-string halo passed here while the
                # outline visibly landed ahead of line 2. r67 replaced it with one
                # halo per line (.gb-ink-halo--line) and asserts each against its
                # own line, plus a mid-flight transform read. The whole-string
                # copy that this block used to read is now the no-JS fallback:
                # display:none once the split has run, so it carries no animation.

                # 5. a picture dropped into a placeholder fills it and is clipped
                # ⚠ r81 overturned r64's blanket `cover` for the two product-gallery
                # boxes: a product shot must not be cropped. The other seven still
                # want cover, so this asserts per selector rather than one value.
                for m in d["media"]:
                    want = "contain" if m["sel"] in CONTAIN_BOXES else "cover"
                    chk(m["fit"] == want,
                        "%s %s object-fit=%s want=%s" % (tag, m["sel"], m["fit"], want))
                    chk(m["fills"], "%s %s image does not fill the box" % (tag, m["sel"]))
                    if m["radius"] != "0px":
                        chk(m["boxOverflow"] == "hidden",
                            "%s %s radius=%s but overflow=%s" % (tag, m["sel"], m["radius"], m["boxOverflow"]))
    b.close()

print("\n%d ok / %d red" % (ok, red))
sys.exit(1 if red else 0)
