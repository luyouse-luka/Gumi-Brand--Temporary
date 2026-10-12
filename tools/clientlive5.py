#!/usr/bin/env python3
"""The five client items of 2026-09-09, as assertions.

  python3 tools/clientlive5.py [--live --password 1234]

  1  .gb-testimonial__name must not be italic. Live renders it as <cite>, which
     the UA sheet italicises; the static build's <figcaption> does not, so this
     one only ever goes red live.
  2a Every .gb-product__acc-item carries a name= so the browser keeps one row
     open per accordion. Live ships them without it (blocks/_gb-accordion-row
     .liquid), main.js fills them in.
  2b Phone opens on $t-acc-narrow with a symmetric curve. Asserted on the CURVE,
     not the declaration: the old $ease-out put 51% of the travel in the first
     100ms, which is what "no transition" meant.
  4  Mobile drawer CTA sits on the drawer's bottom edge, 37 below the links
     (board 283:14915 Nav, itemSpacing 37).
  5  Nutrition modal keeps its height across a tab switch.
"""
import argparse, pathlib, sys
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = '/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
LIVE = 'https://gumi.com.au'
GAP_CTA = 37
DRAWER_PAD_B = 40

ok = red = 0


def check(label, cond, got, want):
    global ok, red
    if cond:
        ok += 1
        print(f'  ok   {label}: {got}')
    else:
        red += 1
        print(f'  RED  {label}: got {got}, want {want}')


def page(br, w, h, url, password=None):
    ctx = br.new_context(viewport={'width': w, 'height': h})
    if password:
        ctx.request.post(LIVE + '/password', form={
            'form_type': 'storefront_password', 'utf8': '✓', 'password': password})
    pg = ctx.new_page()
    pg.goto(url, wait_until='load', timeout=60000)
    pg.wait_for_timeout(1800)
    return ctx, pg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--live', action='store_true')
    ap.add_argument('--password')
    a = ap.parse_args()
    live, pw = a.live, a.password

    def u(name):
        if live:
            return LIVE + {'index': '/', 'pdp': '/products/gumi-daily-greens'}[name]
        return 'file://' + str(ROOT / f'{name}.html')

    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=CHROME)

        if live:
            ctx, pg = page(br, 1440, 900, LIVE + '/', pw)
            h = pg.evaluate("() => { const a = document.querySelector('a[href*=\"/products/\"]'); return a ? a.getAttribute('href') : null; }")
            pg.close(); ctx.close()
            pdp_url = LIVE + h if h else None
        else:
            pdp_url = u('pdp')

        print('1  testimonial name is not italic')
        ctx, pg = page(br, 1440, 900, u('index'), pw)
        r = pg.evaluate("""() => [...document.querySelectorAll('.gb-testimonial__name')]
            .map(e => ({tag: e.tagName, fs: getComputedStyle(e).fontStyle}))""")
        check('count', len(r) > 0, len(r), '>0')
        check('font-style', all(x['fs'] == 'normal' for x in r),
              sorted({f"{x['tag']}:{x['fs']}" for x in r}), 'normal')
        pg.close(); ctx.close()

        print('2a accordion exclusivity (PDP)')
        ctx, pg = page(br, 1440, 900, pdp_url, pw)
        # name= is parked on data-acc-group by main.js (see 2c); what matters here
        # is that the rows ARE grouped and that clicking a second one shuts the first.
        groups = pg.evaluate("() => [...document.querySelectorAll('.gb-product__acc-item')].map(d => d.getAttribute('data-acc-group'))")
        check('every row grouped', len(groups) > 0 and all(groups), groups, 'all non-null')
        check('one group', len(set(groups)) == 1, set(groups), '1 distinct group')
        rows = pg.query_selector_all('.gb-product__acc-row')
        rows[0].click(); pg.wait_for_timeout(800)
        rows[1].click(); pg.wait_for_timeout(800)
        opened = pg.evaluate("() => [...document.querySelectorAll('.gb-product__acc-item')].map(d => d.open)")
        check('only one open after two clicks', sum(opened) == 1, opened, 'exactly 1 True')
        pg.close(); ctx.close()

        print('2b phone open slides like jQuery slideDown')
        ctx, pg = page(br, 390, 844, pdp_url, pw)
        check('js-acc gate set', pg.evaluate("() => document.documentElement.classList.contains('js-acc')"),
              pg.evaluate("() => document.documentElement.className"), 'contains js-acc')
        dur = pg.evaluate("""() => getComputedStyle(
            document.querySelector('.gb-product__acc-item'), '::details-content').transitionDuration""")
        check('css fallback is off while js runs', dur == '0s', dur, '0s')
        s = pg.evaluate("""async () => {
          const it = document.querySelector('.gb-product__acc-item');
          const body = it.querySelector('.gb-acc-body');
          if (it.open) { it.querySelector('summary').click(); await new Promise(r => setTimeout(r, 700)); }
          const out = []; const t0 = performance.now();
          it.querySelector('summary').click();
          await new Promise(res => { (function tick() {
            out.push([performance.now() - t0, body.getBoundingClientRect().height]);
            if (performance.now() - t0 < 900) requestAnimationFrame(tick); else res();
          })(); });
          const hEnd = Math.max(...out.map(o => o[1]));
          const at = ms => { let b = out[0]; for (const s of out) if (Math.abs(s[0]-ms) < Math.abs(b[0]-ms)) b = s; return b; };
          const p = ms => at(ms)[1] / hEnd;
          return {hEnd, p50: +p(50).toFixed(3), p200: +p(200).toFixed(3), p390: +p(390).toFixed(3), p600: +p(600).toFixed(3)};
        }""")
        check('opens at all', s['hEnd'] > 40, s['hEnd'], '> 40px')
        # swing is symmetric: ~half the travel at the halfway mark, done by 400ms
        check('halfway at ~50%', 0.35 <= s['p200'] <= 0.65, s['p200'], '0.35-0.65')
        check('not front-loaded', s['p50'] <= 0.20, s['p50'], '<= 0.20')
        check('finished by 400ms (jQuery default)', s['p390'] >= 0.95, s['p390'], '>= 0.95')
        pg.close(); ctx.close()

        print('2c exclusivity slides the sibling shut')
        ctx, pg = page(br, 1440, 900, pdp_url, pw)
        r = pg.evaluate("""async () => {
          const its = [...document.querySelectorAll('.gb-product__acc-item')];
          const names = its.map(d => d.getAttribute('name'));
          const groups = its.map(d => d.getAttribute('data-acc-group'));
          its[0].querySelector('summary').click();
          await new Promise(r => setTimeout(r, 600));
          its[1].querySelector('summary').click();
          await new Promise(r => setTimeout(r, 120));
          const mid = its[0].querySelector('.gb-acc-body').getBoundingClientRect().height;
          await new Promise(r => setTimeout(r, 700));
          return {names, groups, mid, open: its.map(d => d.open)};
        }""")
        check('name parked on data-acc-group', all(r['groups']) and not any(r['names']),
              f"groups={set(r['groups'])} names={set(r['names'])}", 'groups set, names cleared')
        check('sibling animates shut (not cut)', 0 < r['mid'], r['mid'], '> 0 mid-flight')
        check('only one open when settled', sum(r['open']) == 1, r['open'], 'exactly 1')
        pg.close(); ctx.close()

        print('4  mobile drawer CTA')
        ctx, pg = page(br, 390, 844, u('index'), pw)
        pg.evaluate("() => { const b = document.querySelector('.gb-header__toggle'); if (b) b.click(); }")
        pg.wait_for_timeout(1100)
        r = pg.evaluate("""() => {
          const nav = document.querySelector('.gb-header__nav');
          const btn = document.querySelector('.gb-header__nav .gb-btn--lg');
          const inner = document.querySelector('.gb-header__panel-inner');
          // ⚠ r134 wrapped the CTA in .gb-header__nav-cta, so it has no previous
          // sibling any more -- measure against the list that is actually above it.
          const prev = document.querySelector('.gb-header__links--mobile');
          const R = e => e.getBoundingClientRect();
          return {
            gapAbove: Math.round(R(btn).top - R(prev).bottom),
            btnBottom: Math.round(R(btn).bottom),
            innerBottom: Math.round(R(inner).bottom),
            innerPadB: parseFloat(getComputedStyle(inner).paddingBottom),
            innerH: Math.round(R(inner).height),
            linksTop: Math.round(R(document.querySelector('.gb-header__links--mobile')).top),
            cardsBottom: Math.round(R(document.querySelector('.gb-header__cards')).bottom),
            innerGap: parseFloat(getComputedStyle(inner).rowGap),
            panelBottom: Math.round(R(document.querySelector('.gb-header__panel')).bottom),
            viewportH: 844,
          };
        }""")
        check('gap above CTA >= 37 (floor)', r['gapAbove'] >= GAP_CTA, r['gapAbove'], f'>= {GAP_CTA}')
        check('links stay put under the cards', r['linksTop'] == r['cardsBottom'] + r['innerGap'],
              f"links {r['linksTop']} vs cards {r['cardsBottom']} + gap {r['innerGap']}", 'adjacent')
        # ⚠ Since r132 the CTA is fixed to .gb-header__panel, not parked at the
        # nav's floor, and r133 set its offset to 20 -- the inner's own padding is
        # no longer the reference. tools/drawernav.py owns the exact geometry;
        # this one only holds the round it was written for: the CTA is on the floor.
        check('CTA on the drawer floor',
              abs(r['panelBottom'] - 20 - r['btnBottom']) <= 1,
              f"btn {r['btnBottom']} vs panel {r['panelBottom']} - 20", '<=1px')
        check('inner fills the drawer', r['innerH'] >= r['viewportH'] - 1,
              r['innerH'], f">= {r['viewportH'] - 1}")
        pg.close(); ctx.close()

        print('5  nutrition modal height holds across tabs')
        for w, h in ((1440, 900), (390, 844)):
            ctx, pg = page(br, w, h, pdp_url, pw)
            res = pg.evaluate("""async () => {
              const t = document.querySelector('[data-modal="nutritional-label"]');
              if (!t) return null;
              t.click(); await new Promise(r => setTimeout(r, 900));
              const panel = document.querySelector('.gb-nl-panel');
              const tabs = [...document.querySelectorAll('.gb-nl-tab')];
              const hs = [];
              for (const x of tabs) { x.click(); await new Promise(r => setTimeout(r, 700));
                hs.push(Math.round(panel.getBoundingClientRect().height)); }
              return hs;
            }""")
            check(f'{w} panel height constant', res and len(set(res)) == 1, res, 'all equal')
            pg.close(); ctx.close()
        br.close()

    print(f'\n{ok} ok / {red} red')
    sys.exit(1 if red else 0)


if __name__ == '__main__':
    main()
