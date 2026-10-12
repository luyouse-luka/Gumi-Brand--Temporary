const fs = require('node:fs');
const assert = require('node:assert/strict');
const {pathToFileURL} = require('node:url');
const {chromium} = require('playwright');
(async () => {
  const source = fs.readFileSync('liquid/account-feedback/snippets/gb-account-data.liquid', 'utf8');
  const start = source.indexOf("      'edit-frequency': function (panel, contract) {");
  assert(start >= 0);
  const end = source.indexOf("'skip-next': function", start);
  assert(end > start);
  const handler = source.slice(start, end).replace(/,\s*$/, '');
  const keyStart = source.indexOf('    function planFrequencyKey');
  const keyEnd = source.indexOf('    function planName', keyStart);
  assert(keyStart >= 0 && keyEnd > keyStart);
  const browser = await chromium.launch({executablePath: process.env.ACCT_CHROME});
  let checks = 0;
  try {
    for (const width of [390, 1440]) {
      const p = await browser.newPage({viewport: {width, height: 900}, reducedMotion: 'reduce'});
      await p.goto(pathToFileURL(process.cwd() + '/account.html').href);
      await p.waitForFunction(() => window.gumiAcct);
      const result = await p.evaluate(async ({handler, key}) => {
        eval(key);
        const plans = [2, 4, 6, 8].map(n => ({id: String(n), name: 'Every ' + n + ' weeks'}));
        const sellingPlansForContract = () => plans;
        const frequencyLabel = () => '4 weeks';
        const formatDate = () => '20/10/2026';
        const idOf = v => String(v);
        const collectionItems = v => v || [];
        const run = eval('({' + handler + '})')['edit-frequency'];
        const panel = document.querySelector('[data-acct-modal-panel="edit-frequency"]');
        run(panel, {nextBillingDate: '2026-10-20', deliveryPolicy: {sellingPlanId: '4'}, lines: []});
        await new Promise(resolve => setTimeout(resolve, 20));
        const select = panel.querySelector('#acct-f-freq');
        const list = select.closest('.gb-select').querySelector('.gb-select__list');
        return {values: [...select.options].map(o => o.value), selected: select.value,
          labels: [...list.children].map(e => e.textContent), disabled: panel.querySelector('[data-acct-save]').disabled};
      }, {handler, key: source.slice(keyStart, keyEnd)});
      assert.deepEqual(result.values, ['2', '4', '6']); checks++;
      assert.equal(result.selected, '4'); checks++;
      assert.deepEqual(result.labels, ['Ships every 2 weeks', 'Ships every 4 weeks', 'Ships every 6 weeks']); checks++;
      assert.equal(result.disabled, true); checks++;
      await p.close();
    }
  } finally {await browser.close();}
  console.log(checks + ' checks passed');
})().catch(e => {console.error(e); process.exitCode = 1;});
