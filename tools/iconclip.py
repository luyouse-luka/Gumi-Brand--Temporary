#!/usr/bin/env python3
"""Every icon's ink must fit inside its own viewBox.

A viewBox cut from a Figma node's absoluteBoundingBox holds the geometry only --
a centre-aligned stroke puts half its width outside that box and the renderer
clips it. The board data calls this out as absoluteRenderBounds being larger
than absoluteBoundingBox; this judge proves it from the shipped file instead:
each svg is drawn twice, once as authored and once with the viewBox opened up,
and any ink that appears only in the added margin was being clipped.

Painting is the judge, not path arithmetic: `d` data mixes arc flags in with
coordinates, so a numeric envelope over it reports phantom overflow.
"""
import re, sys, glob, pathlib, json
from collections import OrderedDict
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAD = 3          # viewBox units added on every side
K = 12           # px per viewBox unit


def _chrome():
    hits = sorted((pathlib.Path.home() / ".cache/ms-playwright").glob(
        "chromium-*/chrome-linux64/chrome"))
    if not hits:
        sys.exit("no chromium installed -- run: npx playwright install chromium")
    return hits[-1]


def sources():
    """label -> svg markup, one entry per distinct icon."""
    out = OrderedDict()
    for f in sorted(glob.glob(str(ROOT / "images/*.svg"))):
        out["images/" + pathlib.Path(f).name] = pathlib.Path(f).read_text()
    for page in ("account.html", "account-login.html"):
        src = (ROOT / page).read_text()
        for m in re.finditer(r"<svg\b.*?</svg>", src, re.S):
            el = m.group(0)
            cls = re.search(r'class="([^"]*)"', el)
            vb = re.search(r'viewBox="([^"]*)"', el)
            key = "%s :: %s [%s]" % (page, cls.group(1) if cls else "(no class)",
                                     vb.group(1) if vb else "-")
            out.setdefault(key, el)
    return out


JS = """
async ([svg, pad, k]) => {
  const vb = /viewBox="([^"]+)"/.exec(svg);
  if (!vb) return null;
  const v = vb[1].trim().split(/[\\s,]+/).map(Number);
  if (v.length !== 4 || !(v[2] > 0) || !(v[3] > 0)) return null;
  const [x, y, w, h] = v;
  const W = Math.round((w + pad * 2) * k), H = Math.round((h + pad * 2) * k);
  if (W > 4000 || H > 4000) return null;
  let open = svg.replace(/viewBox="[^"]+"/,
      `viewBox="${x - pad} ${y - pad} ${w + pad * 2} ${h + pad * 2}"`);
  // only the root tag's own sizing is dropped -- a global strip also eats
  // width/height off every <rect> and the icon renders empty
  open = open.replace(/^<svg[^>]*>/, m =>
      m.replace(/\\s(width|height)="[^"]*"/g, '')
       .replace('<svg', `<svg width="${W}" height="${H}"`));
  // inline svg needs no xmlns in html, but a data: URI is parsed as its own
  // document and fails outright without one
  if (!/xmlns=/.test(open)) open = open.replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg"');
  const img = new Image();
  await new Promise((res, rej) => {
    img.onload = res; img.onerror = rej;
    img.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(open);
  });
  const c = document.createElement('canvas');
  c.width = W; c.height = H;
  const g = c.getContext('2d');
  g.drawImage(img, 0, 0, W, H);
  const d = g.getImageData(0, 0, W, H).data;
  // the authored viewBox maps to this rect; ink outside it was being clipped
  const bx = Math.round(pad * k), by = Math.round(pad * k);
  const bw = Math.round(w * k), bh = Math.round(h * k);
  let outside = 0, inside = 0;
  for (let py = 0; py < H; py++) {
    for (let px = 0; px < W; px++) {
      if (d[(py * W + px) * 4 + 3] < 24) continue;
      const within = px >= bx && px < bx + bw && py >= by && py < by + bh;
      if (within) inside++; else outside++;
    }
  }
  return {outside, inside, W, H};
}
"""


def main():
    ok = red = 0
    skipped = []
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=str(_chrome()))
        pg = b.new_page()
        pg.goto("about:blank")
        for label, svg in sources().items():
            # currentColor resolves to the canvas default (black) off-document,
            # which is all the judge needs -- it only asks where ink lands.
            try:
                r = pg.evaluate(JS, [svg, PAD, K])
            except Exception as e:
                skipped.append("%s (%s)" % (label, str(e).splitlines()[0]))
                continue
            if r is None:
                skipped.append(label + " (no usable viewBox)")
                continue
            if r["inside"] == 0:
                skipped.append(label + " (renders nothing)")
                continue
            if r["outside"] > 0:
                red += 1
                print("RED  %-58s %d px of ink outside the viewBox" % (label, r["outside"]))
            else:
                ok += 1
        b.close()
    for s in skipped:
        print("SKIP " + s)
    print("\n%d ok / %d red%s" % (ok, red, "" if not skipped else " / %d skipped" % len(skipped)))
    sys.exit(1 if red else 0)


if __name__ == "__main__":
    main()
