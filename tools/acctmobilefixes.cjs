const assert = require('node:assert/strict');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {chromium} = require('playwright');

(async () => {
  const browser = await chromium.launch({executablePath: process.env.ACCT_CHROME});
  let count = 0;
  function check(label, value) { assert(value, label); console.log('PASS ' + label); count++; }
  for (const width of [390, 767, 768, 1440]) {
    const page = await browser.newPage({viewport: {width, height: 844}, reducedMotion: 'reduce'});
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto(pathToFileURL(path.join(__dirname, '../account.html')).href);
    await page.waitForFunction(() => window.gumi && window.gumiAcct);
    const positions = await page.evaluate(() => {
      const box = selector => document.querySelector(selector).getBoundingClientRect();
      const logo = box('.gb-acct-header__logo'), menu = box('.gb-acct-header__toggle');
      return {logo: logo.x, menu: menu.x, accountIcons: document.querySelectorAll('.gb-acct-header__link--account').length, carts: document.querySelectorAll('.gb-acct-header__cart').length};
    });
    check(`${width}: logo left and hamburger right`, positions.logo < positions.menu);
    check(`${width}: account restored and cart replaced`, positions.accountIcons === 1 && positions.carts === 0);
    check(`${width}: every mobile list link has the supplied arrow`, await page.locator('.gb-acct-list__arrow').count() === await page.locator('.gb-acct-list__link').count());
    if (width <= 767) {
      check(`${width}: arrows align at right edge`, await page.locator('.gb-acct-list__arrow').evaluateAll(els => els.every(el => {
        const a = el.getBoundingClientRect(), l = el.parentElement.getBoundingClientRect();
        return Math.abs(l.right - a.right - 16) < 1 && a.width === 20;
      })));
    }
    await page.locator('.gb-acct-header__toggle').click();
    await page.waitForTimeout(450);
    check(`${width}: header menu opens`, await page.locator('.gb-acct-header__toggle').getAttribute('aria-expanded') === 'true');
    await page.keyboard.press('Escape');
    await page.waitForTimeout(450);
    await page.evaluate(() => {
      window.gumiAcct.modal.open('edit-product');
      const alert = document.querySelector('.gb-acct-modal__alert').cloneNode(true);
      const body = document.querySelector('[data-acct-modal-panel="edit-product"] .gb-acct-modal__body');
      body.before(alert);
    });
    check(`${width}: error icon aligns with first line`, await page.locator('[data-acct-modal-panel="edit-product"] .gb-acct-modal__alert').evaluate(el => {
      const icon = el.querySelector('svg').getBoundingClientRect(), text = el.querySelector('p').getBoundingClientRect();
      return Math.abs(icon.top - text.top) < 1;
    }));
    await page.evaluate(() => window.gumiAcct.modal.open('cancel-offer-skip'));
    const video = page.locator('.gb-acct-video__media');
    check(`${width}: native controls removed`, await video.evaluate(el => !el.controls));
    await page.evaluate(() => {
      const canvas = document.createElement('canvas'); canvas.width = 64; canvas.height = 64;
      const ctx = canvas.getContext('2d');
      window.testVideoTimer = setInterval(() => { ctx.fillStyle = '#005635'; ctx.fillRect(0, 0, 64, 64); }, 50);
      const video = document.querySelector('.gb-acct-video__media'); video.muted = true; video.srcObject = canvas.captureStream(10);
    });
    const button = page.locator('[data-acct-video-toggle]');
    check(`${width}: design overlay visible while paused`, await button.evaluate(el => getComputedStyle(el).opacity === '1'));
    await button.click();
    await page.waitForFunction(() => !document.querySelector('.gb-acct-video__media').paused);
    await page.waitForTimeout(150);
    check(`${width}: overlay hidden during actual playback`, await button.evaluate(el => getComputedStyle(el).opacity === '0'));
    await video.click();
    await page.waitForFunction(() => document.querySelector('.gb-acct-video__media').paused);
    await page.waitForTimeout(150);
    check(`${width}: clicking video pauses and restores overlay`, await button.evaluate(el => getComputedStyle(el).opacity === '1'));
    await button.press('Enter');
    await page.waitForFunction(() => document.querySelector('[data-acct-video-toggle]').getAttribute('aria-label') === 'Pause video');
    check(`${width}: keyboard play works`, await button.getAttribute('aria-label') === 'Pause video');
    await page.evaluate(() => window.gumiAcct.modal.close());
    check(`${width}: closing the modal pauses its video`, await video.evaluate(el => el.paused));
    check(`${width}: no horizontal overflow`, await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
    check(`${width}: no script errors`, errors.length === 0);
    await page.close();
  }
  await browser.close();
  console.log(`${count} checks passed`);
})().catch(error => {console.error(error); process.exit(1);});
