#!/usr/bin/env python3
"""r97: drop crevPager -- the live section owns review paging now (client call).

Exact-anchor read-modify-write; each sub() must hit exactly once.
"""
import re, sys, pathlib

JS = pathlib.Path('assets/main.js')
SCSS = pathlib.Path('assets/customstyle.scss')


def sub(text, old, new, tag, n=1):
    hits = text.count(old)
    if hits != n:
        sys.exit(f'ABORT {tag}: anchor found {hits}x, expected {n}')
    print(f'  ok  {tag}')
    return text.replace(old, new)


j = JS.read_text()

# 1. the whole module, banner comment through closing brace
start = j.index("  /* ---------------------------------------------------------------------\n"
                "   * crevPager")
end = j.index("  /* ---------------------------------------------------------------------\n"
              "   * modal —", start)
block = j[start:end]
assert block.count('var crevPager = {') == 1 and len(block) < 4000, len(block)
j = j[:start] + j[end:]
print(f'  ok  1 crevPager module removed ({len(block)} chars)')

j = sub(j, '                   ["crevPager", crevPager],\n', '', '2 init registration')
j = sub(j, 'gallery: gallery, accordion: accordion, crevPager: crevPager,',
        'gallery: gallery, accordion: accordion,', '3 window.gumi export')
assert 'crevPager' not in j, 'crevPager still referenced'
JS.write_text(j)

s = SCSS.read_text()

# 4. our reveal animation goes with it: without our pager nothing on the static
#    build ever un-hides a card, and the live section runs its own .is-appearing.
s = sub(s, """
  // Client r96: the pager only strips [hidden], and display:none -> flex cannot
  // transition. An animation can: display:none cancels it, so restoring display
  // replays it from the top -- which is exactly the reveal. `backwards` and not
  // `both`, so nothing is left pinned on the element afterwards
  // ([[finished-animation-fill-blocks-transition]]).
  //
  // ⚠ Scoped OFF the live cards. The live section grew its own reveal
  // (`.gb-crev-card.is-appearing`, 0-2-0, in an inline <style>) with a 60ms
  // stagger, and its script REMOVES that class 450ms later. Without this guard
  // the removal hands `animation` back to the rule below and the card fades in
  // a second time. `data-review-id` is written from the metaobject and our own
  // markup never carries it -- the same marker crevPager's guard uses.
  &:not([data-review-id]) { animation: gm-crev-in $t-slow $ease-out backwards; }
""", "", '4 reveal animation removed')

s = sub(s, """
  // Paged out by main.js. The UA's [hidden] rule is display:none at 0-0-0 and
  // loses to the flex above, so it has to be restated here.
  &[hidden] { display: none; }

  @media (prefers-reduced-motion: reduce) {
    &:not([data-review-id]) { animation: gm-fade-in 0.4s ease-out backwards; }
  }
}

@keyframes gm-crev-in {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: none; }
}""", """
  // ⚠ Load-bearing: the live section pages with the [hidden] attribute, whose UA
  // rule is display:none at 0-0-0 and loses to the flex above. Drop this and the
  // ten cards the pager is holding back all render.
  &[hidden] { display: none; }
}""", '5 keyframes + reduced-motion removed')

SCSS.write_text(s)

b = re.search(r'\$build:\s*"([^"]+)"', s).group(1)
SCSS.write_text(SCSS.read_text().replace(f'$build: "{b}"', '$build: "20260908-r97"'))
print(f'  ok  6 $build {b} -> 20260908-r97')
