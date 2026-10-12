const assert = require('node:assert/strict');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {chromium} = require('playwright');
(async () => {
  const b = await chromium.launch({executablePath: process.env.ACCT_CHROME});
  let n = 0;
  const check = (label, v) => {assert(v, label); n++; console.log('PASS ' + label);};
  for (const width of [390, 767, 768, 1440]) {
    const p = await b.newPage({viewport: {width, height: 844}, isMobile: width <= 767, hasTouch: width <= 767, reducedMotion: 'reduce'});
    await p.goto(pathToFileURL(path.join(__dirname, '../account.html')).href);
    await p.waitForTimeout(250);
    check(`${width}: view shell allows artwork overflow`, await p.locator('[data-acct-views]').evaluate(e => getComputedStyle(e).overflowX === 'visible' && getComputedStyle(e).overflowY === 'visible'));
    check(`${width}: no page overflow`, await p.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
    const toggle = p.locator('[data-acct-menu-toggle]'), menu = p.locator('[data-acct-menu]');
    if (width <= 767) {
      check(`${width}: menu initially hidden`, await menu.evaluate(e => getComputedStyle(e).visibility === 'hidden'));
      await toggle.tap(); await p.waitForTimeout(80);
      check(`${width}: tap opens menu`, await menu.evaluate(e => getComputedStyle(e).visibility === 'visible') && await toggle.getAttribute('aria-expanded') === 'true');
      await toggle.tap(); await p.waitForTimeout(80);
      check(`${width}: second tap closes menu`, await menu.evaluate(e => getComputedStyle(e).visibility === 'hidden'));
      await toggle.tap();
      await p.mouse.click(10, 150); await p.waitForTimeout(80);
      check(`${width}: outside click closes menu`, await toggle.getAttribute('aria-expanded') === 'false');
      await toggle.press('Enter'); await p.waitForTimeout(80);
      check(`${width}: keyboard opens menu`, await toggle.getAttribute('aria-expanded') === 'true');
      await p.keyboard.press('Escape'); await p.waitForTimeout(80);
      check(`${width}: Escape closes and returns focus`, await toggle.getAttribute('aria-expanded') === 'false' && await toggle.evaluate(e => document.activeElement === e));
      await toggle.tap();
      await menu.locator('[data-acct-goto="details"]').tap(); await p.waitForTimeout(100);
      check(`${width}: menu navigation changes view and closes menu`, p.url().endsWith('#details') && await toggle.getAttribute('aria-expanded') === 'false');
    } else {
      await toggle.hover(); await p.waitForTimeout(80);
      check(`${width}: desktop hover retained`, await menu.evaluate(e => getComputedStyle(e).visibility === 'visible'));
      await p.mouse.move(0, 150);
    }
    await p.evaluate(() => window.gumiAcct.modal.open('discount-add'));
    const input = p.locator('[data-acct-modal-panel="discount-add"] [data-acct-discount-input]');
    const value = 'DISCOUNT'.repeat(30);
    await input.fill(value); await input.blur();
    check(`${width}: long input uses ellipsis`, await input.evaluate(e => getComputedStyle(e).textOverflow === 'ellipsis' && ['hidden', 'clip'].includes(getComputedStyle(e).overflowX)));
    check(`${width}: complete code remains available`, await input.inputValue() === value);
    await p.close();
  }
  await b.close(); console.log(`${n} checks passed`);
})().catch(e => {console.error(e); process.exit(1);});
