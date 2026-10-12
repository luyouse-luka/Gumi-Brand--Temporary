#!/usr/bin/env python3
"""Round 117, item 8: let a reel take a hosted video URL, not just an upload.

  python3 tools/_apply_r117_reel.py --src <latest pull dir>

main.js has recognised YouTube/Vimeo since r62 (embedUrl(), -> nocookie host)
and the two markup hooks docs/LIQUID-TODO-reels.md asked for are already live.
What is missing is on the data side: the block's only video field is
`{"type": "video"}`, which accepts Shopify Files uploads and nothing else, so a
hosted link cannot be entered at all. Adds a text field for the link plus a
poster picker (an upload derives its poster from the file; a link cannot).
"""
import argparse, pathlib, shutil, sys

ap = argparse.ArgumentParser()
ap.add_argument('--src', required=True)
a = ap.parse_args()
ROOT = pathlib.Path(__file__).resolve().parent.parent
src = pathlib.Path(a.src) / 'sections/gb-reviews.liquid'
if not src.exists():
    sys.exit(f'ABORT: {src} missing -- pass the pull directory')
t = src.read_text(encoding='utf-8')


def sub(old, new):
    global t
    if t.count(old) != 1:
        sys.exit(f'ABORT anchor {t.count(old)}x\n  {old[:90]!r}')
    t = t.replace(old, new, 1)


sub("""              {%- assign video_url = '' -%}
              {%- assign poster = null -%}
              {%- if b.video != blank -%}""",
    """              {%- assign video_url = '' -%}
              {%- assign poster = null -%}
              {%- comment -%}
                A hosted link wins over an upload: main.js turns it into an
                iframe, while an upload becomes a <video>. An upload carries its
                own poster; a link has none, hence the separate picker.
              {%- endcomment -%}
              {%- if b.video_embed != blank -%}
                {%- assign video_url = b.video_embed -%}
                {%- if b.poster != blank -%}{%- assign poster = b.poster -%}{%- endif -%}
              {%- elsif b.video != blank -%}""")

sub("""        { "type": "video", "id": "video", "label": "Video (poster auto-derived from upload)" },
        { "type": "text", "id": "alt", "label": "Accessible label", "default": "Play customer reel" }""",
    """        { "type": "video", "id": "video", "label": "Video (poster auto-derived from upload)" },
        { "type": "text", "id": "video_embed", "label": "Or a hosted video URL", "info": "YouTube or Vimeo. Takes priority over the upload above. Plain text, not a link field -- Shopify's URL type rejects watch links." },
        { "type": "image_picker", "id": "poster", "label": "Poster (hosted video only)", "info": "An upload derives its own poster; a hosted link cannot." },
        { "type": "text", "id": "alt", "label": "Accessible label", "default": "Play customer reel" }""")

out = ROOT / 'liquid/sections/gb-reviews.liquid'
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(t, encoding='utf-8')
print(f'  wrote {out}')
print(f'  diff vs source: {sum(1 for _ in __import__("difflib").unified_diff(src.read_text(encoding="utf-8").splitlines(), t.splitlines()))} diff lines')
