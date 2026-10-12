const assert = require('node:assert/strict');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {chromium} = require('playwright');

(async () => {
  const browser = await chromium.launch({executablePath: process.env.ACCT_CHROME});
  let checks = 0;
  try {
    for (const width of [390, 1440]) {
      const page = await browser.newPage({viewport: {width, height: 900}});
      await page.goto(pathToFileURL(path.join(__dirname, '../account.html')).href);
      await page.waitForFunction(() => window.gumi && window.gumiAcct);
      const logo = page.locator('.gb-acct-header__logo');
      const read = () => logo.evaluate(el => {
        const style = getComputedStyle(el), box = el.getBoundingClientRect();
        return {
          opacity: style.opacity, color: style.color, transform: style.transform,
          filter: style.filter, width: box.width, height: box.height,
          href: el.getAttribute('href')
        };
      });
      await page.mouse.move(0, 0);
      const before = await read();
      assert.equal(before.opacity, '1'); checks++;
      await logo.hover();
      await page.waitForTimeout(300);
      assert(await logo.evaluate(el => el.matches(':hover')));
      assert.deepEqual(await read(), before); checks++;
      assert.equal(before.width, width <= 767 ? 92 : 123);
      assert.equal(before.height, width <= 767 ? 24 : 32); checks++;
      assert.equal(before.href, 'index.html'); checks++;
      console.log(`PASS ${width}: hover unchanged, exact size, home link preserved`);
      await page.close();
    }
    for (const file of ['account.html', 'account-login.html']) {
      for (const width of [390, 1440]) {
        const page = await browser.newPage({viewport: {width, height: 900}});
        await page.goto(pathToFileURL(path.join(__dirname, '../' + file)).href);
        await page.waitForFunction(() => window.gumi && window.gumiAcct);
        const logo = page.locator('.gb-footer__logo');
        await logo.scrollIntoViewIfNeeded();
        await page.mouse.move(0, 0);
        const read = () => logo.evaluate(el => {
          const style = getComputedStyle(el), box = el.getBoundingClientRect();
          const art = el.querySelector('svg,img').getBoundingClientRect();
          return {
            opacity: style.opacity, color: style.color, transform: style.transform,
            filter: style.filter, width: box.width, height: box.height,
            artWidth: art.width, artHeight: art.height, href: el.getAttribute('href')
          };
        });
        const before = await read();
        assert.equal(before.opacity, '1'); checks++;
        await logo.hover();
        await page.waitForTimeout(300);
        assert(await logo.evaluate(el => el.matches(':hover')));
        assert.deepEqual(await read(), before); checks++;
        assert.equal(before.artWidth, width <= 767 ? 167 : 193);
        assert.equal(before.artHeight, width <= 767 ? 43 : 50); checks++;
        assert.equal(before.href, 'index.html'); checks++;
        console.log(`PASS ${file} ${width}: footer hover unchanged, exact size, home link preserved`);
        await page.close();
      }
    }
    console.log(`${checks} checks passed`);
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exit(1); });
