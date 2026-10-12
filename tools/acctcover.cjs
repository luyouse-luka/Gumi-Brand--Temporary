const { chromium } = require('playwright');
const { pathToFileURL } = require('node:url');
const path = require('node:path');
const assert = require('node:assert/strict');
(async () => {
  const browser = await chromium.launch(process.env.ACCT_CHROME ? {executablePath: process.env.ACCT_CHROME} : {});
  let checks = 0;
  const check = (label, actual, expected) => { assert.deepEqual(actual, expected, label); checks++; };
  for (const width of [390, 767, 768, 1440]) {
    const context = await browser.newContext({viewport: {width, height: 844}, reducedMotion: 'no-preference'});
    const page = await context.newPage();
    await page.goto(pathToFileURL(path.join(__dirname, '../account.html')).href);
    await page.waitForTimeout(700);
    await page.locator((width <= 767 ? '.gb-acct-list' : '.gb-acct-nav') + ' [data-acct-goto="subscriptions"]').click();
    await page.waitForTimeout(120);
    const mid = await page.evaluate(() => {
      const old = document.querySelector('[data-acct-view="overview"]');
      const next = document.querySelector('[data-acct-view="subscriptions"]');
      const o = getComputedStyle(old), n = getComputedStyle(next);
      return {live: document.querySelectorAll('[data-acct-view]:not([hidden])').length,
        transform: o.transform, opacity: o.opacity, out: o.animationName, hits: o.pointerEvents,
        oldZ: o.zIndex, newZ: n.zIndex, background: n.backgroundImage,
        enters: n.animationName, incomingTransform: n.transform, incomingOpacity: Number(n.opacity), overflow: document.documentElement.scrollWidth > innerWidth,
        clipped: old.getBoundingClientRect().height <= next.getBoundingClientRect().height + 1};
    });
    check(`${width}: overlap`, mid.live, 2);
    check(`${width}: outgoing inert`, mid.hits, 'none');
    check(`${width}: no horizontal overflow`, mid.overflow, false);
    if (width <= 767) {
      check(`${width}: overview stationary`, mid.transform, 'none');
      check(`${width}: overview fading out`, Number(mid.opacity) > 0 && Number(mid.opacity) < 1, true);
      check(`${width}: fade-out animation`, mid.out, 'gb-acct-view-fade-out');
      check(`${width}: incoming above`, Number(mid.newZ) > Number(mid.oldZ), true);
      check(`${width}: opaque backdrop`, mid.background.includes('linear-gradient'), true);
      check(`${width}: incoming fade`, mid.enters, 'gb-acct-view-fade-in');
      check(`${width}: incoming stationary`, mid.incomingTransform, 'none');
      check(`${width}: incoming fading in`, mid.incomingOpacity > 0 && mid.incomingOpacity < 1, true);
      check(`${width}: incoming covers old content height`, mid.clipped, true);
    } else {
      check(`${width}: desktop exit unchanged`, mid.out, 'gb-acct-view-out');
      check(`${width}: desktop entry unchanged`, mid.enters, 'gb-acct-view-in');
    }
    await page.waitForTimeout(700);
    const live = () => page.evaluate(() => [...document.querySelectorAll('[data-acct-view]:not([hidden])')].map(e => e.dataset.acctView));
    check(`${width}: settled`, await live(), ['subscriptions']);
    await page.evaluate(() => window.gumiAcct.view.show('overview', true));
    await page.waitForTimeout(100);
    await page.evaluate(() => window.gumiAcct.view.show('subscriptions', true));
    await page.waitForTimeout(700);
    check(`${width}: rapid return`, await live(), ['subscriptions']);
    check(`${width}: classes cleared`, await page.locator('.is-leaving, .gb-acct__view.is-entering').count(), 0);
    await context.close();
  }
  const page = await browser.newPage({viewport: {width:390,height:844}, reducedMotion:'reduce'});
  await page.goto(pathToFileURL(path.join(__dirname, '../account.html')).href);
  await page.waitForTimeout(200);
  await page.evaluate(() => window.gumiAcct.view.show('subscriptions', true));
  await page.waitForTimeout(150);
  check('reduce: one view', await page.locator('[data-acct-view]:not([hidden])').count(), 1);
  await browser.close();
  console.log(`${checks} checks passed`);
})().catch(e => { console.error(e); process.exitCode = 1; });
