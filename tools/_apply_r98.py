#!/usr/bin/env python3
"""r98: the expert rail dead-ends instead of rewinding; arrows grey out at each end."""
import sys, pathlib

P = pathlib.Path('/home/ly/project/Gumi-Brand')


def sub(path, old, new, tag, n=1):
    p = P / path
    s = p.read_text()
    if s.count(old) != n:
        sys.exit(f'ABORT {tag}: anchor found {s.count(old)}x in {path}, expected {n}')
    p.write_text(s.replace(old, new))
    print(f'  ok  {tag}  ({path})')


# The rail dead-ends now. slider.sync() already sets [disabled] on the buttons
# whenever a rail is neither `loop` nor `rewind` -- dropping the attribute is
# what switches that on, and .gb-reels__btn[disabled] already carries the style.
OLD = 'data-slider data-slider-rewind data-slider-step'
NEW = 'data-slider data-slider-step'
sub('reviews.html', OLD, NEW, '1a static reviews.html')
sub('liquid/sections/gb-expert.liquid', OLD, NEW, '1b liquid (needs a push of its own)')
