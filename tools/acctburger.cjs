const assert = require('node:assert/strict');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {chromium} = require('playwright');
(async () => {
  const browser = await chromium.launch({executablePath: process.env.ACCT_CHROME});
  let count = 0;
  const check = (label, value) => { assert(value, label); console.log('PASS '+label); count++; };
  for (const width of [390, 767, 768, 1440]) {
    const page = await browser.newPage({viewport:{width,height:844}, hasTouch:width <= 767, reducedMotion:'reduce'});
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    await page.goto(pathToFileURL(path.join(__dirname,'../account.html')).href);
    await page.waitForFunction(() => window.gumi && window.gumiAcct);
    const expected = width <= 767 ? [92,24] : [123,32];
    const dimensions = await page.locator('.gb-acct-header__logo').evaluate(el => {
      const b = el.getBoundingClientRect(), art = el.querySelector('svg,img').getBoundingClientRect();
      return [b.width,b.height,art.width,art.height];
    });
    check(`${width}: logo exact size including artwork`, dimensions.every((n,i) => Math.abs(n-expected[i%2]) < .01));
    await page.locator('.gb-acct-header__logo').evaluate(el => {
      const img = document.createElement('img'); img.src = 'images/pay-visa.svg'; img.width=124; img.height=32; el.replaceChildren(img);
    });
    const image = await page.locator('.gb-acct-header__logo img').boundingBox();
    check(`${width}: uploaded logo image also gets exact size`, image.width === expected[0] && image.height === expected[1]);
    check(`${width}: single header, no CTA`, await page.locator('header').count() === 1 && await page.locator('.gb-header__cta').count() === 0);
    check(`${width}: hamburger visible`, await page.locator('.gb-acct-header__toggle .gb-icon-menu').isVisible());
    const account = page.locator('[data-acct-menu-toggle]');
    if (width <= 767) await account.tap();
    else await account.press('Enter');
    await page.locator('[data-acct-menu]').waitFor({state:'visible'});
    check(`${width}: account activation opens dropdown`, await account.getAttribute('aria-expanded') === 'true' && await page.locator('[data-acct-menu]').isVisible());
    await page.locator('.gb-acct-header__toggle').click();
    await page.waitForTimeout(450);
    check(`${width}: shared menu opens`, await page.locator('#site-header').evaluate(el => el.classList.contains('is-open')));
    check(`${width}: site menu closes account dropdown`, await account.getAttribute('aria-expanded') === 'false');
    if (width <= 767) {
      const panel = await page.locator('#site-menu').boundingBox();
      check(`${width}: drawer covers viewport`, Math.abs(panel.x)<1 && panel.y === 0 && panel.width === width && panel.height === 844);
      check(`${width}: page locks and bar is inert`, await page.evaluate(() => document.documentElement.classList.contains('is-menu-open') && document.querySelector('.gb-acct-header__bar').hasAttribute('inert')));
      const sub = page.locator('.gb-header__links--mobile [data-collapsible]').first();
      await sub.locator('button').click();
      check(`${width}: submenu expands`, await sub.locator('button').getAttribute('aria-expanded') === 'true');
      await sub.locator('button').click();
      check(`${width}: submenu collapses`, await sub.locator('button').getAttribute('aria-expanded') === 'false');
      await page.locator('.gb-header__panel-close').click();
    } else { await page.keyboard.press('Escape'); }
    await page.waitForTimeout(450);
    check(`${width}: closes and restores toggle focus`, await page.locator('.gb-acct-header__toggle').evaluate(el => el.getAttribute('aria-expanded') === 'false' && document.activeElement === el));
    check(`${width}: unlocks bar and page`, await page.evaluate(() => !document.documentElement.classList.contains('is-menu-open') && !document.querySelector('.gb-acct-header__bar').hasAttribute('inert')));
    await page.locator('.gb-acct-header__toggle').press('Enter');
    await page.waitForTimeout(450);
    check(`${width}: keyboard opens menu`, await page.locator('.gb-acct-header__toggle').getAttribute('aria-expanded') === 'true');
    await page.keyboard.press('Escape');
    await page.waitForTimeout(450);
    check(`${width}: Escape closes menu`, await page.locator('.gb-acct-header__toggle').getAttribute('aria-expanded') === 'false');
    if (width > 767) {
      await page.locator('.gb-acct-header__toggle').click();
      await account.press('Enter');
      check(`${width}: account menu closes site menu`, await page.locator('.gb-acct-header__toggle').getAttribute('aria-expanded') === 'false' && await account.getAttribute('aria-expanded') === 'true');
      await page.keyboard.press('Escape');
    }
    check(`${width}: no overflow or JS errors`, await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth) && errors.length === 0);
    await page.close();
  }
  await browser.close();
  console.log(`${count} checks passed`);
})().catch(e => {console.error(e); process.exit(1);});
