const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const {pathToFileURL} = require('node:url');
const {chromium} = require('playwright');
(async () => {
  const root = path.join(__dirname, '..');
  const theme = process.env.ACCT_ICON_THEME || path.join(root, 'liquid/account-order-icons');
  const data = fs.readFileSync(path.join(theme, 'snippets/gb-account-data.liquid'), 'utf8');
  const markup = fs.readFileSync(path.join(theme, 'snippets/gb-account-placeholders.liquid'), 'utf8');
  const block = data.slice(data.indexOf('          // Subscription vs one-off tag'), data.indexOf('          var price = row.querySelector', data.indexOf('          // Subscription vs one-off tag')));
  assert(block.includes('var tag ='));
  assert(data.includes('if (oneOffIcon) orderOneOffIconHtml = oneOffIcon.outerHTML;'));
  assert(markup.includes('data-acct-one-off-icon'));
  assert(/gb-acct-btn__icon[\s\S]*?Download Invoice/.test(markup));
  const browser = await chromium.launch({executablePath: process.env.ACCT_CHROME});
  let checks = 4;
  for (const width of [390, 1440]) {
    const page = await browser.newPage({viewport: {width, height: 844}});
    await page.goto(pathToFileURL(path.join(root, 'account.html')).href + '#order');
    await page.waitForTimeout(600);
    const result = await page.evaluate(block => {
      const one = document.querySelector('[data-acct-one-off-icon]');
      const invoice = [...document.querySelectorAll('button')].find(e => e.textContent.trim() === 'Download Invoice');
      const icon = invoice.querySelector('svg');
      const first = document.querySelector('[data-acct-view="order"] .gb-acct-item');
      const run = new Function('row', 'li', 'orderOneOffIconHtml', block);
      const sub = first.cloneNode(true), once = first.cloneNode(true);
      run(sub, {is_subscription: true}, one.outerHTML);
      run(once, {is_subscription: false}, one.outerHTML);
      return {oneSize: [one.getBoundingClientRect().width, one.getBoundingClientRect().height],
        box: one.getAttribute('viewBox'), color: one.querySelector('path').getAttribute('stroke'),
        invoiceSize: [icon.getBoundingClientRect().width, icon.getBoundingClientRect().height],
        white: icon.querySelector('path').getAttribute('stroke'),
        once: !!once.querySelector('[data-acct-one-off-icon]'),
        sub: !!sub.querySelector('[data-acct-one-off-icon]'),
        overflow: document.documentElement.scrollWidth > innerWidth};
    }, block);
    assert.deepEqual(result.oneSize, [12, 12]);
    assert.equal(result.box, '0 0 12 12');
    assert.equal(result.color, '#666666');
    assert.deepEqual(result.invoiceSize, [20, 20]);
    assert.equal(result.white, 'white');
    assert.equal(result.once, true);
    assert.equal(result.sub, false);
    assert.equal(result.overflow, false);
    checks += 8;
    await page.close();
  }
  await browser.close();
  console.log(`${checks} checks passed`);
})().catch(e => {console.error(e); process.exit(1);});
