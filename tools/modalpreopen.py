#!/usr/bin/env python3
"""A dialog that arrived already open must still be closable.

  python3 tools/modalpreopen.py

modal.close() used to guard on `current`, which only open() sets -- so markup
that ships is-open could not be closed by anything. Live reaches that state when
the last cart line is removed and cart-items-component replays
<template id="empty-cart-template">, whose .gb-cart carries is-open and whose
overlay uses OUR [data-modal-close].

Graded here, including both guards on the adoption:
  A  overlay / Escape / close button all work on a pre-opened dialog
  B  the normal open() -> close() path is unchanged
  C  a pre-opened dialog wired to the THEME's close command is NOT adopted
  D  a pre-opened dialog that is not on screen is NOT adopted
"""
import argparse, pathlib, sys
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
LIVE = 'https://gumi.com.au'
ok = red = 0


def grade(cond, label, detail=''):
    global ok, red
    if cond:
        ok += 1
        print(f'  ok   {label}   {detail}')
    else:
        red += 1
        print(f'  RED  {label}   {detail}')


IS_OPEN = "() => document.getElementById('gb-cart').classList.contains('is-open')"
PREOPEN = """() => {
    const c = document.getElementById('gb-cart');
    c.classList.add('is-open');
    c.setAttribute('aria-hidden', 'false');
}"""

ap = argparse.ArgumentParser()
ap.add_argument('--live', action='store_true')
ap.add_argument('--password')
a = ap.parse_args()
if a.live and not a.password:
    sys.exit('--live needs --password')

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=CHROME)
    ctx = b.new_context(viewport={'width': 1440, 'height': 900})
    pg = ctx.new_page()

    def load():
        pg.goto((ROOT / 'index.html').as_uri(), wait_until='domcontentloaded', timeout=60000)
        pg.wait_for_timeout(1300)

    print('--- A. a pre-opened dialog closes by all three paths ---')
    for name, act in (
            ('overlay click',
             lambda: pg.evaluate("() => document.querySelector('#gb-cart .gb-cart__overlay').click()")),
            ('Escape', lambda: pg.keyboard.press('Escape')),
            ('close button',
             lambda: pg.evaluate("() => document.querySelector('#gb-cart .gb-cart__close').click()"))):
        load()
        pg.evaluate(PREOPEN)
        pg.wait_for_timeout(400)
        grade(pg.evaluate(IS_OPEN), f'A. setup: pre-opened via markup ({name})')
        grade(not pg.evaluate("() => !!(window.gumi.modal.current)"),
              f'A. and modal.current is null, as after a template replay ({name})')
        act()
        pg.wait_for_timeout(800)
        grade(not pg.evaluate(IS_OPEN), f'A. {name} closes it')

    print('--- B. the normal path is unchanged ---')
    load()
    pg.evaluate("""() => document.querySelector('[data-modal="gb-cart"]').click()""")
    pg.wait_for_timeout(800)
    grade(pg.evaluate(IS_OPEN), 'B. opens by trigger')
    grade(pg.evaluate("() => !!(window.gumi.modal.current)"), 'B. and sets current')
    pg.evaluate("() => document.querySelector('#gb-cart .gb-cart__overlay').click()")
    pg.wait_for_timeout(800)
    grade(not pg.evaluate(IS_OPEN), 'B. closes by overlay')
    grade(pg.evaluate("() => !document.documentElement.classList.contains('is-modal-open')"),
          'B. and drops the scroll lock')

    print('--- C. a theme-wired dialog is left alone ---')
    load()
    got = pg.evaluate("""() => {
        // Same shape as the live cart's other two branches: is-open, role=dialog,
        // but the overlay carries the theme's command instead of ours.
        const d = document.createElement('div');
        d.className = 'gb-cart is-open';
        d.setAttribute('role', 'dialog');
        d.style.cssText = 'position:fixed;inset:0;width:100px;height:100px';
        d.innerHTML = '<div class="gb-cart__overlay" on:click="#cart-drawer/close"></div>';
        document.body.appendChild(d);
        return {rects: d.getClientRects().length,
                adopted: window.gumi.modal.showing() === d};
    }""")
    grade(got['rects'] > 0, 'C. setup: the decoy is on screen', str(got))
    grade(not got['adopted'], 'C. showing() does not adopt it (no [data-modal-close])')

    print('--- D. an off-screen pre-opened dialog is left alone ---')
    load()
    got = pg.evaluate("""() => {
        const d = document.createElement('div');
        d.className = 'gb-cart is-open';
        d.setAttribute('role', 'dialog');
        d.style.display = 'none';
        d.innerHTML = '<div class="gb-cart__overlay" data-modal-close></div>';
        document.body.appendChild(d);
        return {rects: d.getClientRects().length,
                adopted: window.gumi.modal.showing() === d};
    }""")
    grade(got['rects'] == 0, 'D. setup: the decoy is not rendered', str(got))
    grade(not got['adopted'], 'D. showing() does not adopt it (nothing to close)')

    if a.live:
        print('--- E. live, replaying the theme\'s own empty-cart template ---')
        # Deliberately on / rather than /cart: the drawer is rendered on every
        # page and /cart carries a Cloudflare challenge that poisons the session.
        ctx.request.post(LIVE + '/password', form={
            'form_type': 'storefront_password', 'utf8': '\u2713', 'password': a.password})
        pg.goto(LIVE + '/', wait_until='domcontentloaded', timeout=90000)
        pg.wait_for_timeout(2500)
        info = pg.evaluate("""() => {
            const t = document.getElementById('empty-cart-template');
            if (!t) return {found: false};
            // Exactly what cart-items-component does when the last line goes.
            const node = t.content.firstElementChild.cloneNode(true);
            document.body.appendChild(node);
            const ov = node.querySelector('.gb-cart__overlay');
            return {found: true,
                    isOpen: node.classList.contains('is-open'),
                    ourWiring: !!node.querySelector('[data-modal-close]'),
                    onScreen: node.getClientRects().length > 0,
                    adopted: window.gumi.modal.showing() === node};
        }""")
        if not info['found']:
            print('  --   no #empty-cart-template on this page, E skipped')
        else:
            grade(info['isOpen'] and info['ourWiring'],
                  'E. the real template ships is-open with our [data-modal-close]', str(info))
            grade(info['adopted'], 'E. and showing() adopts it', str(info))
            pg.evaluate("""() => document.querySelectorAll('.gb-cart__overlay')[
                document.querySelectorAll('.gb-cart__overlay').length - 1].click()""")
            pg.wait_for_timeout(900)
            grade(pg.evaluate("""() => {
                const all = [...document.querySelectorAll('.gb-cart')];
                const last = all[all.length - 1];
                return last && !last.classList.contains('is-open');
            }"""), 'E. clicking its overlay closes it on live')
    b.close()

print(f'\n{ok} ok / {red} red')
sys.exit(1 if red else 0)
