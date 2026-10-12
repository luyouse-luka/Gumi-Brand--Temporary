const fs = require('node:fs'), path = require('node:path');
const assert = require('node:assert/strict');
const {pathToFileURL} = require('node:url');
const {chromium} = require('playwright');
(async () => {
  const root = path.join(__dirname, '..');
  const source = fs.readFileSync(path.join(root, 'liquid/account-feedback/snippets/gb-account-data.liquid'), 'utf8');
  const baseline = fs.readFileSync(path.join(root, '../Gumi-Brand-shopify/baseline-20261002-a55/snippets/gb-account-data.liquid'), 'utf8');
  const submitBlock = s => s.slice(s.indexOf('    var submit ='), s.indexOf('    // Chip remove')).replace(/\r\n/g, '\n');
  assert.equal(submitBlock(source), submitBlock(baseline), 'API submit handlers restored to a55');
  assert(!/skippedOrders|rememberSkippedOrder|skippedOrder\(/.test(source));
  const raw = source.match(/<script[^>]*>([\s\S]*?)<\/script>/)[1];
  let runtime = raw.slice(0, raw.indexOf('    var CUSTOMER_EMAIL')) +
    'var CUSTOMER_EMAIL=null, ADD_PRODUCTS=[], CUSTOMER_ORDERS=[];\n' +
    raw.slice(raw.indexOf('    // Money is in minor units')).replace(/\{\{[\s\S]*?\}\}/g, 'null');
  runtime = runtime.replace(/    if \(document.readyState === 'loading'\)[\s\S]*?else boot\(\);/, `
    window.acctProbe = {prefill: prefill, submit: submit, discounts: activeDiscounts,
      render: function(c) {contractCache[idOf(c.id)] = c; renderDetail(c);},
      restored: true};`);
  if (process.argv.includes('--strip')) runtime = runtime.replace('(idKey && seen[idKey]) || (codeKey && seen[codeKey])', '(idKey && seen[idKey])');
  new Function(runtime);
  const browser = await chromium.launch({executablePath: process.env.ACCT_CHROME});
  let checks = 0;
  const check = (name, result) => {assert(result, name); checks++; console.log('PASS ' + name);};
  try {
    for (const width of [390, 1440]) {
      const p = await browser.newPage({viewport: {width, height: 900}, reducedMotion: 'reduce'});
      p.on('pageerror', e => console.log('PAGE ERROR', e.message));
      p.on('console', m => {if (m.type() === 'error' || m.type() === 'warning') console.log(m.text());});
      await p.goto(pathToFileURL(path.join(root, 'account.html')).href + '?sub=42#detail');
      await p.evaluate(() => {
        const view = document.querySelector('[data-acct-view="subscriptions"]');
        const tpl = document.createElement('template');
        tpl.setAttribute('data-acct-sub-template', '');
        tpl.innerHTML = view.querySelector('.gb-acct-sub').outerHTML;
        view.appendChild(tpl);
        const schedule = document.querySelector('.gb-acct-schedule');
        const day = document.createElement('template');
        day.setAttribute('data-acct-schedule-day-template', '');
        day.innerHTML = '<span class="gb-acct-schedule__day"></span>';
        schedule.appendChild(day);
        schedule.querySelector('.gb-acct-schedule__unskip')?.remove();
        window.testContract = {id: '42', status: 'ACTIVE', nextBillingDate: '2027-06-19T00:00:00.000Z',
          deliveryPolicy: {interval: 'MONTH', intervalCount: 1}, lines: {nodes: []},
          discountCodes: [{code: 'SAVE', amount: 8}], appliedDiscounts: [{id: 'd1', code: 'save', amount: 8}]};
        window.apiCalls = [];
        window.failSkip = false;
        window.fetch = async (url) => {
          window.apiCalls.push(url);
          if (url.endsWith('/skip-next') && !window.failSkip) window.testContract = {...window.testContract, nextBillingDate: '2027-07-19T00:00:00.000Z'};
          return {ok: !window.failSkip, json: async () => ({ok: !window.failSkip, subscriptions: [window.testContract]})};
        };
      });
      await p.evaluate(runtime);
      const defaults = await p.evaluate(() => {
        const panel = document.querySelector('[data-acct-modal-panel="discount-applied"]');
        window.acctProbe.prefill['discount-applied'](panel, {lines: {nodes: []}});
        return getComputedStyle(panel.querySelector('.gb-acct-discount__result')).display === 'none';
      });
      check(`${width}: empty discount result hidden`, defaults);
      check(`${width}: same code with and without id deduplicated`, await p.evaluate(() => window.acctProbe.discounts(window.testContract).length === 1));
      check(`${width}: render twice keeps one chip and exact amount`, await p.evaluate(() => {
        const panel = document.querySelector('[data-acct-modal-panel="discount-applied"]');
        window.acctProbe.prefill['discount-applied'](panel, window.testContract);
        window.acctProbe.prefill['discount-applied'](panel, window.testContract);
        return panel.querySelectorAll('.gb-acct-chip').length === 1 && panel.querySelector('.gb-acct-chip').textContent.includes('$8.00');
      }));
      check(`${width}: no discount shows no empty green label`, await p.evaluate(() => {
        window.acctProbe.render({...window.testContract, discountCodes: [], appliedDiscounts: []});
        return getComputedStyle(document.querySelector('.gb-acct-summary__discount .gb-acct-tag')).display === 'none';
      }));
      check(`${width}: zero automatic discount has no green bar`, await p.evaluate(() => {
        window.acctProbe.render({...window.testContract, discountCodes: [], appliedDiscounts: [{title: 'Automatic', amount: 0}]});
        return getComputedStyle(document.querySelector('.gb-acct-summary__discount .gb-acct-tag')).display === 'none';
      }));
      check(`${width}: skipped style changes only marked day`, await p.evaluate(async () => {
        const days = document.querySelectorAll('.gb-acct-schedule__day');
        const button = document.querySelector('.gb-acct-schedule [data-acct-modal="skip-next"]');
        const before = getComputedStyle(button).backgroundColor;
        days[1].classList.add('is-skipped');
        await new Promise(resolve => setTimeout(resolve, 80));
        return getComputedStyle(days[1]).backgroundColor === 'rgb(230, 230, 230)' &&
          getComputedStyle(days[0]).backgroundColor !== 'rgb(230, 230, 230)' &&
          !button.disabled && getComputedStyle(button).backgroundColor === before;
      }));
      await p.close();
    }
  } finally {await browser.close();}
  console.log(checks + ' checks passed');
})().catch(e => {console.error(e); process.exitCode = 1;});
