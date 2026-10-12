#!/usr/bin/env python3
"""r107 ask 9 -- Shopify's captcha placeholder eating a gap in .gb-form.

  python3 tools/_apply_r107e.py
"""
import pathlib, sys

SCSS = pathlib.Path('assets/customstyle.scss')

OLD = """.gb-form__fields {"""
NEW = """// Shopify drops its bot-challenge container straight into {% form %} as a direct
// child. With the challenge invisible it paints nothing, but it is NOT
// display:none -- so it stays a flex item and eats one whole 32px gap between
// the fields and the submit button.
// ⚠ :empty is a guard, not decoration. The moment hCaptcha puts a real widget in
//   there (checkbox mode) the rule stops matching and the challenge shows --
//   folding a live captcha away would make the form impossible to submit.
// ⚠ Written from Shopify's documented behaviour: the container is not present on
//   this store right now, so the rule is inert here and could not be measured.
.gb-form > [class*="captcha"]:empty,
.gb-form > .shopify-challenge__container:empty { display: none; }

.gb-form__fields {"""

text = SCSS.read_text(encoding='utf-8')
n = text.count(OLD)
if n != 1:
    sys.exit(f'ABORT: anchor found {n} time(s), expected 1')
SCSS.write_text(text.replace(OLD, NEW, 1), encoding='utf-8')
print('  ok  9. captcha placeholder folded out of .gb-form')
