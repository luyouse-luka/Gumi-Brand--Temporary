const assert = require('node:assert/strict');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {chromium} = require('playwright');
(async () => {
  const b = await chromium.launch({executablePath: process.env.ACCT_CHROME});
  let checks = 0;
  for (const width of [390, 1440]) {
    const p = await b.newPage({viewport: {width, height: 700}, isMobile: width === 390, hasTouch: true, reducedMotion: 'reduce'});
    await p.goto(pathToFileURL(path.join(__dirname, '../account.html')).href);
    await p.waitForTimeout(250);
    const c = await p.context().newCDPSession(p);
    for (const name of ['add-product', 'shipping-form']) {
      await p.evaluate(name => {
        const panel = window.gumiAcct.modal.panel(name);
        panel.querySelector('.gb-acct-modal__body').innerHTML = '<div>Loading</div>';
        window.gumiAcct.modal.open(name);
      }, name);
      await p.waitForTimeout(150);
      await p.evaluate(() => {
        document.querySelector('.gb-acct-modal.is-open .gb-acct-modal__body').innerHTML = '<div data-scroll-content>New content</div>';
      });
      await p.waitForTimeout(150);
      await p.locator('.gb-acct-modal.is-open [data-scroll-content]').evaluate(e => e.style.height = '1800px');
      await p.waitForTimeout(200);
      const body = p.locator('.gb-acct-modal.is-open .gb-acct-modal__body');
      assert.equal(await body.evaluate(e => getComputedStyle(e).overflowY), 'auto', `${width}/${name}: replacement content remains scrollable`); checks++;
      assert(await body.evaluate(e => e.scrollHeight > e.clientHeight)); checks++;
      if (width === 390) {
        await c.send('Input.dispatchTouchEvent', {type: 'touchStart', touchPoints: [{x: 160, y: 550}]});
        for (let y = 520; y >= 250; y -= 30) {
          await c.send('Input.dispatchTouchEvent', {type: 'touchMove', touchPoints: [{x: 160, y}]});
          await p.waitForTimeout(30);
        }
        await c.send('Input.dispatchTouchEvent', {type: 'touchEnd', touchPoints: []});
        await p.waitForTimeout(150);
        assert(await body.evaluate(e => e.scrollTop > 100), `${name}: touch reaches later content`); checks++;
      }
      await body.evaluate(e => e.scrollTop = e.scrollHeight);
      assert(await body.evaluate(e => Math.abs(e.scrollHeight - e.clientHeight - e.scrollTop) < 2), `${width}/${name}: bottom reachable`); checks++;
      await p.evaluate(() => window.gumiAcct.modal.close());
      await p.waitForTimeout(100);
    }
    await p.close();
  }
  await b.close();
  console.log(`${checks} checks passed`);
})().catch(e => {console.error(e); process.exit(1);});
