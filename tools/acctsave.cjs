const fs = require('node:fs'), path = require('node:path');
const assert = require('node:assert/strict');
const {pathToFileURL} = require('node:url');
const {chromium} = require('playwright');
(async () => {
  const root = path.join(__dirname, '..');
  const source = fs.readFileSync(path.join(root, 'liquid/account-feedback/snippets/gb-account-data.liquid'), 'utf8');
  const sync = source.slice(source.indexOf('    function syncEditCta'), source.indexOf('    // Subscription name from'));
  const browser = await chromium.launch({executablePath: process.env.ACCT_CHROME});
  let count = 0;
  const check = (name, value) => {assert(value, name); count++; console.log('PASS ' + name);};
  try {
    for (const width of [390, 1440]) {
      const p = await browser.newPage({viewport: {width, height: 900}, reducedMotion: 'reduce'});
      await p.goto(pathToFileURL(path.join(root, 'account.html')).href);
      const normal = await p.evaluate(() => {
        const panel = document.querySelector('[data-acct-modal-panel="edit-name"]');
        const input = panel.querySelector('[data-acct-field]');
        const save = panel.querySelector('[data-acct-save]');
        input.value = 'Current subscription';
        window.gumiAcct.modal.open('edit-name');
        input.dispatchEvent(new Event('input', {bubbles: true}));
        const unchanged = save.disabled;
        input.value = 'New name';
        input.dispatchEvent(new Event('input', {bubbles: true}));
        const changed = !save.disabled;
        input.value = 'Current subscription';
        input.dispatchEvent(new Event('input', {bubbles: true}));
        const reverted = save.disabled;
        window.gumiAcct.modal.close();
        input.value = 'Updated server name';
        window.gumiAcct.modal.open('edit-name');
        input.dispatchEvent(new Event('change', {bubbles: true}));
        const reopened = save.disabled;
        const replacement = input.cloneNode(true);
        input.replaceWith(replacement);
        replacement.value = 'Edited replacement';
        replacement.dispatchEvent(new Event('input', {bubbles: true}));
        const dynamic = !save.disabled;
        window.gumiAcct.form.watch(panel);
        replacement.dispatchEvent(new Event('change', {bubbles: true}));
        return {unchanged, changed, reverted, reopened, dynamic, rebaselined: save.disabled};
      });
      for (const [name, ok] of Object.entries(normal)) check(`${width}: ${name}`, ok);
      const product = await p.evaluate(sync => {
        const idOf = id => String(id || '').replace(/^gid:\/\/shopify\/\w+\//, '');
        eval(sync);
        const panel = document.querySelector('[data-acct-modal-panel="edit-product"]');
        panel._acctQtyOwned = true;
        panel.setAttribute('data-acct-line-orig-qty', '1');
        panel.setAttribute('data-acct-line-orig-variant-id', 'gid://shopify/ProductVariant/42');
        panel.querySelector('.gb-acct-prod').setAttribute('data-variant-id', '42');
        const qty = panel.querySelector('[data-acct-qty-value]');
        qty.value = '1';
        const select = panel.querySelector('[data-acct-field]');
        select.value = select.options[1].value;
        syncEditCta(panel);
        select.dispatchEvent(new Event('change', {bubbles: true}));
        window.gumiAcct.modal.open('edit-product');
        const save = panel.querySelector('[data-acct-save]');
        const unchanged = save.disabled;
        qty.value = '2'; syncEditCta(panel);
        const changed = !save.disabled;
        window.gumiAcct.modal.close(); window.gumiAcct.modal.open('edit-product');
        const owned = !save.disabled;
        qty.value = '1'; syncEditCta(panel);
        return {unchanged, changed, owned, reverted: save.disabled};
      }, sync);
      for (const [name, ok] of Object.entries(product)) check(`${width}: product ${name}`, ok);
      check(`${width}: empty-product message spans full grid`, await p.evaluate(() => {
        const grid = document.querySelector('[data-acct-modal-panel="add-product"] .gb-acct-prod-grid');
        grid.innerHTML = '<p class="gb-acct-empty">No additional products available to add.</p>';
        window.gumiAcct.modal.open('add-product');
        const child = grid.firstElementChild;
        return getComputedStyle(child).gridColumnStart === '1' && getComputedStyle(child).gridColumnEnd === '-1' &&
          Math.abs(child.getBoundingClientRect().width - grid.getBoundingClientRect().width) < 1;
      }));
      await p.close();
    }
  } finally {await browser.close();}
  console.log(count + ' checks passed');
})().catch(e => {console.error(e); process.exitCode = 1;});
