#!/usr/bin/env python3
"""Probe the live storefront for CLS and for the .wowo reveal gate.

  python3 tools/liveprobe70.py --password <storefront-password> [--url ...]

Password is a CLI arg on purpose: it must not land in the repo.
"""
import argparse
import json

from playwright.sync_api import sync_playwright

CHROME = ('/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome')

# Runs before any document script: records the gate class and the opacity of
# the first .wowo element on every frame, so a late stylesheet shows up as a
# visible-then-hidden flip rather than a single end-state reading.
INIT = """
window.__probe = { frames: [], cls: 0, shifts: [], marks: {} };
// Attribution for the shift: fonts landing vs our js booting are the two
// candidates and they happen within a few hundred ms of each other.
document.fonts.ready.then(() => {
  window.__probe.marks.fontsReady = Math.round(performance.now());
});
(function watchGumi() {
  if (window.gumi) { window.__probe.marks.gumi = Math.round(performance.now()); return; }
  requestAnimationFrame(watchGumi);
})();
new PerformanceObserver((l) => {
  for (const e of l.getEntries()) {
    if (e.hadRecentInput) continue;
    window.__probe.cls += e.value;
    window.__probe.shifts.push({
      t: Math.round(e.startTime),
      v: +e.value.toFixed(5),
      sources: (e.sources || []).map(s => ({
        node: s.node ? (s.node.className || s.node.tagName || '') : '',
        from: s.previousRect ? [s.previousRect.x, s.previousRect.y, s.previousRect.width, s.previousRect.height] : null,
        to: s.currentRect ? [s.currentRect.x, s.currentRect.y, s.currentRect.width, s.currentRect.height] : null,
      })).slice(0, 3),
    });
  }
}).observe({ type: 'layout-shift', buffered: true });

function sample() {
  const h = document.documentElement;
  const el = document.querySelector('.wowo');
  const lr = document.querySelector('[data-line-reveal]');
  // inner is what actually moves: .is-split hands opacity back to the host and
  // parks the text at translateY(100%), i.e. outside the mask.
  const inner = lr && lr.querySelector('.gb-line-mask__inner');
  window.__probe.frames.push({
    t: Math.round(performance.now()),
    cls: h.className,
    sheets: document.styleSheets.length,
    custom: !!Array.from(document.styleSheets).find(s => (s.href || '').includes('customstyle')),
    wowo: el ? getComputedStyle(el).opacity : null,
    animated: el ? el.classList.contains('animated') : null,
    lrOpacity: lr ? getComputedStyle(lr).opacity : null,
    lrSplit: lr ? lr.classList.contains('is-split') : null,
    lrText: lr ? (lr.textContent || '').trim().slice(0, 18) : null,
    lrInk: inner ? getComputedStyle(inner).transform : 'no-mask-yet',
    lrH: lr ? Math.round(lr.getBoundingClientRect().height * 100) / 100 : null,
    lrY: lr ? Math.round(lr.getBoundingClientRect().y * 100) / 100 : null,
  });
  if (window.__probe.frames.length < 400) requestAnimationFrame(sample);
}
requestAnimationFrame(sample);
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--password', help='storefront password; omit for local urls')
    ap.add_argument('--url', default='https://gumi.com.au/')
    ap.add_argument('--width', type=int, default=1440)
    ap.add_argument('--height', type=int, default=900)
    ap.add_argument('--throttle', action='store_true',
                    help='4x CPU + Fast 3G, which is where CLS actually shows')
    a = ap.parse_args()

    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=CHROME)
        ctx = br.new_context(viewport={'width': a.width, 'height': a.height})

        # Storefront password. ctx.request shares the browser cookie jar, so
        # posting the form here logs the pages in too. Driving the UI does not
        # work: the input sits in a collapsed panel and is never visible.
        # The cookie is _shopify_essential (HttpOnly), not storefront_digest.
        if a.password:
            ctx.request.post(a.url.rstrip('/') + '/password', form={
                'form_type': 'storefront_password', 'utf8': '✓',
                'password': a.password})
            if not any(c['name'] == '_shopify_essential' for c in ctx.cookies()):
                raise SystemExit('storefront password rejected (no _shopify_essential)')

        page = ctx.new_page()
        page.add_init_script(INIT)
        if a.throttle:
            cdp = ctx.new_cdp_session(page)
            cdp.send('Emulation.setCPUThrottlingRate', {'rate': 4})
            cdp.send('Network.enable')
            cdp.send('Network.emulateNetworkConditions', {
                'offline': False, 'latency': 150,
                'downloadThroughput': 1.6 * 1024 * 1024 / 8,
                'uploadThroughput': 750 * 1024 / 8,
            })

        page.goto(a.url, wait_until='load')
        page.wait_for_timeout(3000)
        out = page.evaluate('window.__probe')

        print('URL      %s  @%dx%d%s' % (a.url, a.width, a.height,
                                         '  [throttled]' if a.throttle else ''))
        print('CLS      %.5f' % out['cls'])
        print()

        print('--- .wowo gate (only frames where something changed) ---')
        prev = None
        for f in out['frames']:
            key = (f['custom'], f['wowo'], f['animated'])
            if key != prev:
                print('  t=%-6d customstyle=%-5s wowo.opacity=%-8s animated=%s'
                      % (f['t'], f['custom'], f['wowo'], f['animated']))
                prev = key

        print()
        print('--- [data-line-reveal] first element: visible before .is-split? ---')
        prev = None
        for f in out['frames']:
            key = (f['lrOpacity'], f['lrSplit'], f['lrInk'] == 'no-mask-yet')
            if key != prev:
                print('  t=%-6d opacity=%-8s is-split=%-6s text=%-20r mask=%s'
                      % (f['t'], f['lrOpacity'], f['lrSplit'],
                         f['lrText'], f['lrInk'][:34]))
                prev = key
        vis = [f for f in out['frames'] if f['lrOpacity'] == '1' and not f['lrSplit']]
        if vis:
            print('  >> text sat FULLY VISIBLE and unsplit for %d ms (t=%d..%d)'
                  % (vis[-1]['t'] - vis[0]['t'], vis[0]['t'], vis[-1]['t']))

        print()
        print('--- attribution marks ---')
        print('  fonts.ready  t=%s' % out['marks'].get('fontsReady'))
        print('  window.gumi  t=%s' % out['marks'].get('gumi'))
        print()
        print('--- first [data-line-reveal] geometry (height/y changes) ---')
        prev = None
        for f in out['frames']:
            key = (f['lrH'], f['lrY'])
            if key != prev and f['lrH'] is not None:
                print('  t=%-6d height=%-8s y=%s' % (f['t'], f['lrH'], f['lrY']))
                prev = key
        print()
        print('--- layout shifts (largest first) ---')
        for s in sorted(out['shifts'], key=lambda x: -x['v'])[:8]:
            print('  t=%-6d value=%.5f' % (s['t'], s['v']))
            for src in s['sources']:
                print('      %s' % json.dumps(src)[:200])

        br.close()


if __name__ == '__main__':
    main()
