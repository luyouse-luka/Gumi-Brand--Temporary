#!/usr/bin/env python3
"""Grab frame 0 of each images/reel-N.mp4 into images/reel-poster-N.jpg.

No ffmpeg on this box, so the frame comes out of chromium: a <video> is drawn
into a <canvas> and read back as a JPEG. Served over http rather than file://
because each file:// document is its own origin, which taints the canvas and
makes toDataURL throw.

    python3 tools/_reelposter.py
"""
import base64, http.server, io, os, socketserver, threading, sys
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = 8971
N = 5
EXE = "/snap/bin/chromium"

os.chdir(ROOT)

class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass

socketserver.TCPServer.allow_reuse_address = True
srv = socketserver.TCPServer(("127.0.0.1", PORT), Q)
threading.Thread(target=srv.serve_forever, daemon=True).start()

# the port could belong to something else entirely -- prove it is ours
import urllib.request
probe = urllib.request.urlopen("http://127.0.0.1:%d/tools/_reelposter.py" % PORT, timeout=5).read()
assert b"Grab frame 0" in probe, "port %d is not serving this repo" % PORT
print("  http server on %d verified" % PORT)

JS = """
async (n) => {
  const v = document.createElement("video");
  v.muted = true; v.preload = "auto"; v.crossOrigin = "anonymous";
  v.src = "/images/reel-" + n + ".mp4";
  await new Promise((res, rej) => {
    v.onloadeddata = res; v.onerror = () => rej("load failed");
    setTimeout(() => rej("timeout"), 20000);
  });
  if (v.currentTime !== 0) { v.currentTime = 0; await new Promise(r => v.onseeked = r); }
  const c = document.createElement("canvas");
  c.width = v.videoWidth; c.height = v.videoHeight;
  c.getContext("2d").drawImage(v, 0, 0);
  // mean luma, to catch a black opening frame
  const d = c.getContext("2d").getImageData(0, 0, c.width, c.height).data;
  let sum = 0;
  for (let i = 0; i < d.length; i += 4 * 97) sum += 0.299*d[i] + 0.587*d[i+1] + 0.114*d[i+2];
  const luma = sum / (d.length / (4 * 97));
  return {w: v.videoWidth, h: v.videoHeight, dur: v.duration, luma: luma,
          jpg: c.toDataURL("image/jpeg", 0.82)};
}
"""

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=EXE)
    pg = b.new_page()
    pg.goto("http://127.0.0.1:%d/index.html" % PORT, wait_until="domcontentloaded")
    for n in range(1, N + 1):
        r = pg.evaluate(JS, n)
        raw = base64.b64decode(r["jpg"].split(",", 1)[1])
        out = os.path.join(ROOT, "images", "reel-poster-%d.jpg" % n)
        open(out, "wb").write(raw)
        flag = "  DARK" if r["luma"] < 25 else ""
        print("  reel-poster-%d.jpg  %dx%d  %.1fs  luma %.0f  %6d B%s"
              % (n, r["w"], r["h"], r["dur"], r["luma"], len(raw), flag))
    b.close()
srv.shutdown()
