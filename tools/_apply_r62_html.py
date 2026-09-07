#!/usr/bin/env python3
"""Round 62 -- wire the reels to real video.

  * every .gb-reel carries data-video (inline attribute, client-set) and a
    poster <img> cut from that video's frame 0
  * the shared #reel-video dialog gets a <video data-modal-video> that main.js
    fills from the clicked card

Cards 6-10 are copies of 1-5 (the loop needs > 2x the visible count), so they
reuse the same five sources on purpose.

    python3 tools/_apply_r62_html.py [--check]
"""
import io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ["index.html", "pdp.html", "our-story.html", "how-gumi-works.html"]
DIMS = {1: (640, 360), 2: (640, 360), 3: (640, 360), 4: (960, 540), 5: (640, 480)}

CARD = re.compile(
    r'(<button class="gb-reel swiper-slide" type="button" data-modal="reel-video")'
    r'( aria-label="Play customer reel (\d+)">)'
    r'<span class="gb-reel__media" aria-hidden="true">'
    r'<!-- TODO client asset: reel poster/thumbnail goes here as <img class="gb-reel__media-img"> -->'
    r'</span>')

def card(m):
    k = (int(m.group(3)) - 1) % 5 + 1
    w, h = DIMS[k]
    return ('%s data-video="images/reel-%d.mp4"%s'
            '<span class="gb-reel__media" aria-hidden="true">'
            '<img class="gb-reel__media-img" src="images/reel-poster-%d.jpg" alt="" '
            'width="%d" height="%d" loading="lazy" decoding="async">'
            '</span>' % (m.group(1), k, m.group(2), k, w, h))

GLYPH = ('<svg aria-hidden="true" viewBox="0 0 86 54" fill="none" xmlns="http://www.w3.org/2000/svg">'
         '<rect width="85.9996" height="53.7498" rx="10.6711" fill="white"/>'
         '<path d="M53.2807 25.5673C54.5365 26.2924 54.5365 28.1051 53.2807 28.8301L37.9289 37.6935C36.673 38.4186 35.1032 37.5122 35.1032 36.0621L35.1032 18.3354C35.1032 16.8852 36.673 15.9789 37.9289 16.704L53.2807 25.5673Z" fill="currentColor"/></svg>')

DIALOG_OLD = ('          <!-- TODO client asset: reel video -->\n'
              '          <div class="gb-rv-panel__video">' + GLYPH + '</div>')
DIALOG_NEW = ('          <!-- TODO client asset: placeholder reels -- swap images/reel-*.mp4\n'
              '               and their posters for the client\'s own -->\n'
              '          <div class="gb-rv-panel__video">\n'
              '            <video class="gb-rv-panel__player" data-modal-video playsinline controls\n'
              '                   preload="none" aria-label="Customer reel"></video>\n'
              '            <span class="gb-rv-panel__glyph" aria-hidden="true">' + GLYPH + '</span>\n'
              '          </div>')

NOTE_OLD = '<!-- TODO client asset: reels are grey placeholders in the design -->'
NOTE_NEW = ('<!-- TODO client asset: the design leaves these grey. Posters are frame 0 of\n'
            '               images/reel-N.mp4, themselves stand-ins -- see CHANGELOG r62 -->')

check = "--check" in sys.argv
for name in PAGES:
    p = os.path.join(ROOT, name)
    s = io.open(p, encoding="utf-8").read()
    n_card = len(CARD.findall(s))
    n_dlg = s.count(DIALOG_OLD)
    n_note = s.count(NOTE_OLD)
    print("  %-22s cards %2d  dialog %d  note %d" % (name, n_card, n_dlg, n_note))
    if check:
        continue
    assert n_card == 10 and n_dlg == 1 and n_note == 1, "unexpected shape in " + name
    s = CARD.sub(card, s)
    s = s.replace(DIALOG_OLD, DIALOG_NEW).replace(NOTE_OLD, NOTE_NEW)
    io.open(p, "w", encoding="utf-8").write(s)
print("  " + ("checked" if check else "applied"))
