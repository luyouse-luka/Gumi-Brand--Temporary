const assert = require('node:assert/strict');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {chromium} = require('playwright');
(async () => {
  const browser = await chromium.launch({executablePath: process.env.ACCT_CHROME});
  let checks = 0;
  try {
    for (const width of [390, 1440]) {
      const page = await browser.newPage({viewport: {width, height: 900}, reducedMotion: 'reduce'});
      await page.goto(pathToFileURL(path.join(__dirname, '../account.html')).href);
      await page.waitForFunction(() => window.gumiAcct);
      await page.evaluate(() => window.gumiAcct.view.show('detail', false));
      for (const state of ['active', 'paused', 'cancelled']) {
        for (const applied of [false, true]) {
          await page.evaluate(({state, applied}) => {
            const detail = document.querySelector('.gb-acct-detail');
            detail.setAttribute('data-acct-sub-state', state);
            detail.setAttribute('data-acct-discount', applied ? 'applied' : 'none');
          }, {state, applied});
          const selector = `[data-acct-view="detail"] [data-acct-modal="${applied ? 'discount-applied' : 'discount-add'}"]`;
          const link = page.locator(selector);
          await link.scrollIntoViewIfNeeded();
          await page.mouse.move(0, 0);
          await page.waitForTimeout(40);
          assert.equal(await link.evaluate(el => getComputedStyle(el).color), 'rgb(3, 116, 165)'); checks++;
          await link.hover();
          await page.waitForTimeout(40);
          assert(await link.evaluate(el => el.matches(':hover')));
          assert.equal(await link.evaluate(el => getComputedStyle(el).color), state === 'cancelled' ? 'rgb(3, 116, 165)' : 'rgb(0, 86, 53)'); checks++;
          console.log(`PASS ${width} ${state} ${applied ? 'Edit' : 'Add'} discount hover`);
        }
      }
      await page.close();
    }
    console.log(`${checks} discount color checks passed`);
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
