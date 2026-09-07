# -*- coding: utf-8 -*-
"""Round 62 assertions (build r62) -- the reels play real video.

  1  every .gb-reel carries data-video; cards 6-10 repeat 1-5's five sources
  2  every card shows a poster cut from frame 0 of its own video
  3  clicking card N puts THAT source in the shared dialog -- the point of the
     round, so three different cards are used and their sources must differ
  4  data-video takes a hosted link too (card 5 is a YouTube watch URL). The
     markup carries no player at all: [data-modal-media] is an empty box and
     main.js builds a <video> or an <iframe> into it, never both
  5  closing removes the node -- for an iframe that is the only way to stop a
     third-party player
  6  a trigger with no data-video falls back to the grey placeholder
  7  the panel is 16/9, <= 960 wide

Green against the current build; tools/_reverse_r62.py must turn it red.
"""
import os, sys, json
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXE = os.path.expanduser("~/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome")
BASE = "file://" + ROOT + "/"
PAGES = ["index.html", "pdp.html", "our-story.html", "how-gumi-works.html"]
YT = "https://www.youtube.com/watch?v=aqz-KE-bpKQ"
YTE = "https://www.youtube-nocookie.com/embed/aqz-KE-bpKQ?autoplay=1&rel=0&playsinline=1"
SRC = {1: "images/reel-1.mp4", 2: "images/reel-2.mp4", 3: "images/reel-3.mp4",
       4: "images/reel-4.mp4", 5: YT}

ok = bad = 0
def chk(label, got, want, tol=None):
    global ok, bad
    if tol is not None:
        good = got is not None and abs(got - want) <= tol
        detail = "%s ~ %s (+-%s)" % (got, want, tol)
    else:
        good = got == want
        detail = "%s == %s" % (json.dumps(got, ensure_ascii=False), json.dumps(want, ensure_ascii=False))
    if good: ok += 1
    else:
        bad += 1
        print("  RED  %-56s %s" % (label, detail))

# ---- 1/2 static -----------------------------------------------------------
for name in PAGES:
    src = open(os.path.join(ROOT, name), encoding="utf-8").read()
    for n in range(1, 11):
        k = (n - 1) % 5 + 1
        card = 'data-video="%s" aria-label="Play customer reel %d"' % (SRC[k], n)
        chk("%s card %d data-video" % (name, n), card in src, True)
    chk("%s poster imgs" % name, src.count('class="gb-reel__media-img"'), 10)
    chk("%s media box" % name, src.count("data-modal-media"), 1)
    # the whole point of this revision: no player in the markup
    chk("%s no <video> in markup" % name, "<video" in src, False)
    chk("%s no <iframe> in markup" % name, "<iframe" in src, False)

for k in range(1, 5):
    chk("file images/reel-%d.mp4" % k,
        os.path.getsize(os.path.join(ROOT, "images/reel-%d.mp4" % k)) > 1000, True)
for k in range(1, 6):
    chk("file images/reel-poster-%d.jpg" % k,
        os.path.getsize(os.path.join(ROOT, "images/reel-poster-%d.jpg" % k)) > 1000, True)

# ---- runtime --------------------------------------------------------------
STATE = """() => {
  const d = document.getElementById("reel-video");
  const box = d.querySelector("[data-modal-media]");
  // A missing box must read as red, not as a traceback: a crash cannot be told
  // apart from the probe itself being broken.
  if (!box) { return {missing: true, nodes: -1, tag: "NO BOX", src: "NO BOX",
                      open: false, hasVideo: null, hasEmbed: null,
                      paused: null, vw: 0, glyphShown: "none"}; }
  const n = box.querySelector("[data-modal-node]");
  const v = n && n.tagName === "VIDEO" ? n : null;
  const g = d.querySelector(".gb-rv-panel__glyph");
  const kind = !n ? null
             : n.tagName === "VIDEO" ? "VIDEO"
             : n.tagName === "IFRAME" ? "IFRAME" : "OFFLINE";
  return {open: d.classList.contains("is-open"),
          hasVideo: d.classList.contains("has-video"),
          hasEmbed: d.classList.contains("has-embed"),
          nodes: box.querySelectorAll("[data-modal-node]").length,
          tag: kind,
          src: n ? (n.getAttribute("src") ||
                    (n.querySelector("a") ? n.querySelector("a").getAttribute("href") : null)) : null,
          paused: v ? v.paused : null,
          vw: v ? v.videoWidth : 0,
          glyphShown: g ? getComputedStyle(g).display : "none"};
}"""
CLICK = """(n) => {
  const c = [...document.querySelectorAll(".gb-reel")]
    .find(e => e.getAttribute("aria-label") === "Play customer reel " + n);
  if (!c) return false;
  c.click();
  return true;
}"""
CLOSE = """() => document.querySelector("#reel-video [data-modal-close]").click()"""

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 1440, "height": 900})

    # Reload per case. promoModal fires at 5000ms and modal is a singleton, so
    # it closes whatever is open -- a run that lets cases accumulate past that
    # mark goes red on the reel dialog for a reason that has nothing to do with
    # this round. Each case now finishes well inside the window.
    def fresh():
        pg.goto(BASE + "index.html", wait_until="load")
        pg.wait_for_timeout(700)

    fresh()
    s0 = pg.evaluate(STATE)
    chk("closed: no media node", s0["nodes"], 0)
    chk("closed: no has-video", s0["hasVideo"], False)
    chk("closed: no has-embed", s0["hasEmbed"], False)
    chk("closed: glyph visible", s0["glyphShown"] != "none", True)

    # three file-backed cards -> three different sources, each in a <video>
    seen = {}
    for n, want in ((1, 1), (3, 3), (7, 2)):
        fresh()
        chk("card %d found" % n, pg.evaluate(CLICK, n), True)
        pg.wait_for_timeout(900)
        s = pg.evaluate(STATE)
        chk("card %d opens dialog" % n, s["open"], True)
        chk("card %d builds a <video>" % n, s["tag"], "VIDEO")
        chk("card %d exactly one node" % n, s["nodes"], 1)
        chk("card %d src" % n, s["src"], "images/reel-%d.mp4" % want)
        chk("card %d has-video" % n, s["hasVideo"], True)
        chk("card %d not has-embed" % n, s["hasEmbed"], False)
        chk("card %d glyph hidden" % n, s["glyphShown"], "none")
        chk("card %d frame decoded" % n, s["vw"] > 0, True)
        seen[n] = s["src"]
        pg.evaluate(CLOSE)
        pg.wait_for_timeout(700)
        sc = pg.evaluate(STATE)
        chk("card %d closed: node removed" % n, sc["nodes"], 0)
        chk("card %d closed: no has-video" % n, sc["hasVideo"], False)
    chk("sources differ", len(set(seen.values())), 3)

    # A hosted link over file:// cannot be embedded at all: the origin is null
    # and YouTube answers with its own Error 153. playVideo swaps in a note.
    fresh()
    chk("card 5 found", pg.evaluate(CLICK, 5), True)
    pg.wait_for_timeout(600)
    s5 = pg.evaluate(STATE)
    chk("card 5 file:// -> offline note", s5["tag"], "OFFLINE")
    chk("card 5 exactly one node", s5["nodes"], 1)
    chk("card 5 note links to source", s5["src"], YT)
    chk("card 5 has-embed", s5["hasEmbed"], True)
    chk("card 5 not has-video", s5["hasVideo"], False)
    chk("card 5 glyph hidden", s5["glyphShown"], "none")
    pg.evaluate(CLOSE)
    pg.wait_for_timeout(700)
    s5c = pg.evaluate(STATE)
    # removing the node is the only way to stop a third-party player
    chk("card 5 closed: node removed", s5c["nodes"], 0)
    chk("card 5 closed: no has-embed", s5c["hasEmbed"], False)

    # url parsing: every shape a client is likely to paste
    cases = pg.evaluate("""() => {
      const f = window.gumi.modal.embedUrl.bind(window.gumi.modal);
      return {watch:   f("https://www.youtube.com/watch?v=aqz-KE-bpKQ"),
              short:   f("https://youtu.be/aqz-KE-bpKQ"),
              shorts:  f("https://www.youtube.com/shorts/aqz-KE-bpKQ"),
              share:   f("https://m.youtube.com/watch?feature=share&v=aqz-KE-bpKQ"),
              embed:   f("https://www.youtube.com/embed/aqz-KE-bpKQ"),
              stamped: f("https://www.youtube.com/watch?v=aqz-KE-bpKQ&t=42"),
              vimeo:   f("https://vimeo.com/76979871"),
              vplayer: f("https://player.vimeo.com/video/76979871"),
              file:    f("images/reel-1.mp4"),
              abs:     f("https://cdn.example.com/a/b/reel.mp4")};
    }""")
    for key in ("watch", "short", "shorts", "share", "embed"):
        chk("embedUrl %s" % key, cases[key], YTE)
    chk("embedUrl stamped", cases["stamped"], YTE + "&start=42")
    chk("embedUrl vimeo", cases["vimeo"], "https://player.vimeo.com/video/76979871?autoplay=1")
    chk("embedUrl vplayer", cases["vplayer"], "https://player.vimeo.com/video/76979871?autoplay=1")
    # a plain file must NOT be mistaken for a hosted page
    chk("embedUrl file", cases["file"], None)
    chk("embedUrl abs mp4", cases["abs"], None)

    # fallback: a trigger with no data-video keeps the grey placeholder
    fresh()
    pg.evaluate("""() => {
      const c = [...document.querySelectorAll(".gb-reel")]
        .find(e => e.getAttribute("aria-label") === "Play customer reel 1");
      c.removeAttribute("data-video"); c.click();
    }""")
    pg.wait_for_timeout(600)
    sf = pg.evaluate(STATE)
    chk("no data-video: no node", sf["nodes"], 0)
    chk("no data-video: no has-video", sf["hasVideo"], False)
    chk("no data-video: no has-embed", sf["hasEmbed"], False)
    chk("no data-video: glyph back", sf["glyphShown"] != "none", True)
    pg.evaluate(CLOSE)
    pg.wait_for_timeout(600)

    # ---- 4b the same card over http:// really does build the iframe --------
    # file:// is the only reason the note appears, so the embed path needs an
    # origin to be checked at all. Served locally; nothing hits YouTube here
    # beyond the frame's own request.
    import http.server, socketserver, threading
    class Q(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=ROOT, **k)
        def log_message(self, *a): pass
    socketserver.TCPServer.allow_reuse_address = True
    srv = socketserver.TCPServer(("127.0.0.1", 8974), Q)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    try:
        pg.goto("http://127.0.0.1:8974/index.html", wait_until="load")
        pg.wait_for_timeout(700)
        pg.evaluate(CLICK, 5)
        pg.wait_for_timeout(600)
        sh = pg.evaluate(STATE)
        chk("http card 5 builds an <iframe>", sh["tag"], "IFRAME")
        chk("http card 5 embed url", sh["src"], YTE)
        chk("http card 5 has-embed", sh["hasEmbed"], True)
        pg.evaluate(CLOSE)
        pg.wait_for_timeout(700)
        chk("http card 5 closed: node removed", pg.evaluate(STATE)["nodes"], 0)
        # a file-backed card must still take the <video> path over http
        pg.goto("http://127.0.0.1:8974/index.html", wait_until="load")
        pg.wait_for_timeout(700)
        pg.evaluate(CLICK, 2)
        pg.wait_for_timeout(900)
        chk("http card 2 builds a <video>", pg.evaluate(STATE)["tag"], "VIDEO")
    finally:
        srv.shutdown()

    # ---- 7 panel geometry -------------------------------------------------
    fresh()
    geo = pg.evaluate("""() => {
      const d = document.getElementById("reel-video");
      d.classList.add("is-open");
      const pn = d.querySelector(".gb-rv-panel");
      if (!pn) { d.classList.remove("is-open"); return {w: 0, h: 1}; }
      const r = pn.getBoundingClientRect();
      d.classList.remove("is-open");
      return {w: r.width, h: r.height};
    }""")
    chk("panel ratio 16/9", geo["w"] / geo["h"], 16 / 9, 0.02)
    chk("panel width <= 960", geo["w"] <= 960.5, True)

    b.close()

print("\n  r62check: %d ok, %d red" % (ok, bad))
sys.exit(1 if bad else 0)
