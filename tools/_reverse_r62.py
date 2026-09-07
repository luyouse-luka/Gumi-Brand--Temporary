#!/usr/bin/env python3
"""Rebuild the pre-r62 state so r62check can be shown to fail.

Backs the six touched files up first; --restore brings them forward again and
the recompiled css must match byte for byte.

    python3 tools/_reverse_r62.py            # go back
    python3 tools/_reverse_r62.py --restore  # come forward again
"""
import io, os, re, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BAK = "/tmp/claude-1007/-home-ly/d987cc62-8f46-4ddc-ba73-6f0a85c1522e/scratchpad/r62bak"
PAGES = ["index.html", "pdp.html", "our-story.html", "how-gumi-works.html"]
FILES = PAGES + ["assets/customstyle.scss", "assets/main.js"]

if "--restore" in sys.argv:
    for f in FILES:
        shutil.copy2(os.path.join(BAK, f.replace("/", "__")), os.path.join(ROOT, f))
    print("  restored %d files" % len(FILES))
    sys.exit(0)

os.makedirs(BAK, exist_ok=True)
for f in FILES:
    shutil.copy2(os.path.join(ROOT, f), os.path.join(BAK, f.replace("/", "__")))

# --- html: strip data-video, the poster img and the dialog player -----------
CARD = re.compile(r' data-video="[^"]*"')
IMG = re.compile(r'<img class="gb-reel__media-img"[^>]*>')
# the box main.js builds the player into; without it playVideo bails out
PLAYER = re.compile(r' data-modal-media')
for name in PAGES:
    p = os.path.join(ROOT, name)
    s = io.open(p, encoding="utf-8").read()
    s = CARD.sub("", s)
    s = IMG.sub("", s)
    s = PLAYER.sub("", s)
    io.open(p, "w", encoding="utf-8").write(s)

# --- js: stop handing the trigger over ------------------------------------
p = os.path.join(ROOT, "assets/main.js")
s = io.open(p, encoding="utf-8").read()
s = s.replace('self.open(document.getElementById(open.getAttribute("data-modal")), open);',
              'self.open(document.getElementById(open.getAttribute("data-modal")));')
# and blind the hosted-link branch, so the embed assertions cannot pass either
s = s.replace('      var m = src.match(/(?:youtube', '      return null;\n      var m = src.match(/(?:youtube')
io.open(p, "w", encoding="utf-8").write(s)

# --- scss: back to the reel-card ratio ------------------------------------
p = os.path.join(ROOT, "assets/customstyle.scss")
s = io.open(p, encoding="utf-8").read()
s = s.replace("""  aspect-ratio: 16 / 9;
  width: min(100%, 960px);
  max-width: calc((100svh - 80px) * 16 / 9);""",
              """  aspect-ratio: 304 / 540;
  height: min(100%, 720px);
  max-width: 100%;""")
io.open(p, "w", encoding="utf-8").write(s)
print("  reversed; backups in " + BAK)
