const assert = require('node:assert/strict');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {chromium} = require('playwright');

(async () => {
  const browser = await chromium.launch({executablePath: process.env.ACCT_CHROME});
  let checks = 0;
  function check(label, value) { assert(value, label); checks++; console.log('PASS ' + label); }
  for (const width of [390, 768, 1440]) {
    const page = await browser.newPage({viewport: {width, height: 844}, reducedMotion: 'reduce'});
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto(pathToFileURL(path.join(__dirname, '../account.html')).href);
    await page.waitForFunction(() => window.gumi && window.gumiAcct);
    check(`${width}: one site header, old header removed`, await page.locator('#site-header').count() === 1 && await page.locator('.gb-acct-header').count() === 0);
    check(`${width}: Shop now removed`, await page.locator('.gb-header__cta').count() === 0);
    check(`${width}: account and cart icons retained`, await page.locator('.gb-header__icons .gb-header__icon').count() === 2);
    check(`${width}: no horizontal overflow`, await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
    await page.locator('.gb-header__toggle').click();
    await page.waitForTimeout(450);
    check(`${width}: menu opens`, await page.locator('#site-header').evaluate(el => el.classList.contains('is-open')));
    check(`${width}: menu links available`, await page.locator('.gb-header__nav a:visible').count() > 0);
    await page.keyboard.press('Escape');
    await page.waitForTimeout(450);
    check(`${width}: Escape closes menu`, await page.locator('.gb-header__toggle').getAttribute('aria-expanded') === 'false');
    await page.locator('[data-acct-goto="details"]').filter({visible: true}).first().click();
    await page.waitForTimeout(650);
    check(`${width}: account navigation retained`, page.url().endsWith('#details'));
    await page.evaluate(() => window.gumiAcct.modal.open('discount-add'));
    await page.waitForTimeout(250);
    check(`${width}: Account modal opens`, await page.locator('[data-acct-modal-panel="discount-add"]').isVisible());
    check(`${width}: no script errors`, errors.length === 0);
    await page.close();
  }
  await browser.close();
  console.log(`${checks} checks passed`);
})().catch(error => { console.error(error); process.exit(1); });
