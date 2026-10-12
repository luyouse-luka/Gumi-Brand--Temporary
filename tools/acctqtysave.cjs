const fs = require('node:fs'), path = require('node:path');
const assert = require('node:assert/strict');
const {pathToFileURL} = require('node:url');
const {chromium} = require('playwright');

(async () => {
  const root = path.join(__dirname, '..');
  const source = fs.readFileSync(path.resolve(process.argv[2] || path.join(root, 'liquid/account-qty-discount/snippets/gb-account-data.liquid')), 'utf8');
  const qtyStart = source.indexOf('    function attachQtyControls');
  const qtyEnd = source.indexOf('    // Subscription name', qtyStart);
  const qtyCode = source.slice(qtyStart, qtyEnd);
  const submitStart = source.indexOf("      'edit-product': function", source.indexOf('var submit'));
  const handler = source.slice(submitStart, source.indexOf("      'cancel-offer-skip':", submitStart)).replace(/,\s*$/, '');
  const captureStart = source.indexOf('    // Capture click on any modal primary action');
  const capture = source.slice(captureStart, source.indexOf('    // ────────── Overview:', captureStart));
  const helperStart = source.indexOf('    function confirmProductQuantity');
  const helper = helperStart < 0 ? '' : source.slice(helperStart, source.indexOf('    // Capture click on any modal trigger', helperStart));
  assert(qtyStart >= 0 && qtyEnd > qtyStart && submitStart >= 0 && captureStart >= 0);
  new Function(qtyCode); new Function('return ({' + handler + '})'); new Function(helper + capture);
  const browser = await chromium.launch({executablePath: process.env.ACCT_CHROME});
  let checks = 0;
  const check = (label, result) => { assert(result, label); checks++; console.log('PASS ' + label); };
  try {
    for (const width of [390, 1440]) {
      for (const panelName of process.env.ACCT_QTY_PANEL ? [process.env.ACCT_QTY_PANEL] : ['edit-product', 'add-product']) {
      for (const mode of ['delayed', 'unchanged', 'rejected', 'pending']) {
        const page = await browser.newPage({viewport: {width, height: 900}, reducedMotion: 'reduce'});
        await page.goto(pathToFileURL(path.join(root, 'account.html')).href);
        await page.waitForFunction(() => window.gumiAcct);
        await page.evaluate(({qtyCode, handler, capture, helper, mode, panelName}) => {
          const idOf = value => String(value || '').replace(/^gid:\/\/shopify\/\w+\//, '');
          const collectionItems = value => Array.isArray(value) ? value : value && value.nodes || [];
          const contract = {id: '42', lines: {nodes: [{id: 'gid://shopify/SubscriptionLine/1', variantId: panelName === 'edit-product' ? '99' : '88', quantity: 1}, {id: '2', quantity: 1}]}};
          const currentContract = () => contract;
          const immediateOrderPending = () => false;
          const contractCache = {'42': contract};
          const renderList = () => {};
          const renderCurrentOrder = () => {};
          const renderDetail = latest => { window.qtyTrace.displayed = latest.lines.nodes.find(line => line.variantId === '99')?.quantity || 0; };
          const refetchAndRerender = () => { renderDetail(contract); return Promise.resolve(contract); };
          window.qtyTrace = {posts: [], reads: 0, closed: 0, displayed: 1};
          const api = (url, options) => {
            if (options && options.method === 'POST') {
              window.qtyTrace.posts.push({url, body: JSON.parse(options.body)});
              return Promise.resolve(mode === 'rejected' ? {ok: false, j: {ok: false, error: 'Rejected quantity'}} : {ok: true, j: {ok: true}});
            }
            window.qtyTrace.reads++;
            const latest = JSON.parse(JSON.stringify(contract));
            if (mode === 'pending') {
              if (panelName === 'edit-product') latest.lines.nodes[0].quantity = 12;
              else latest.lines.nodes.push({id: '3', variantId: '99', quantity: 12});
              return new Promise(resolve => { window.resolveQuantityRead = () => resolve({ok: true, j: {ok: true, subscription: latest}}); });
            }
            if (mode === 'delayed' && window.qtyTrace.reads > 1) {
              if (panelName === 'edit-product') latest.lines.nodes[0].quantity = 12;
              else latest.lines.nodes.push({id: '3', variantId: '99', quantity: 12});
            }
            return Promise.resolve({ok: true, j: {ok: true, subscription: latest}});
          };
          const submit = eval('({' + handler + '})');
          const panel = document.querySelector('[data-acct-modal-panel="' + panelName + '"]');
          panel.querySelectorAll('.gb-acct-prod').forEach((card, index) => { if (index) card.remove(); });
          panel.setAttribute('data-acct-line-id', '1');
          panel.setAttribute('data-acct-line-orig-variant-id', '99');
          panel.setAttribute('data-acct-line-orig-qty', '1');
          panel.querySelector('.gb-acct-prod').setAttribute('data-variant-id', '99');
          eval(qtyCode); attachQtyControls(panel); (panelName === 'edit-product' ? syncEditCta : syncAddCta)(panel); eval(helper); eval(capture);
          panel.querySelector('.gb-acct-modal__close').addEventListener('click', () => { window.qtyTrace.closed++; });
          window.gumiAcct.modal.open(panelName);
          const timeout = window.setTimeout;
          window.setTimeout = (fn, delay, ...args) => timeout(fn, delay === 700 ? 20 : delay, ...args);
        }, {qtyCode, handler, capture, helper, mode, panelName});
        const qty = page.locator('[data-acct-modal-panel="' + panelName + '"] [data-acct-qty-value]');
        const save = page.locator('[data-acct-modal-panel="' + panelName + '"] [data-acct-save]');
        await qty.fill('12');
        check(`${width} ${panelName} ${mode}: manual input enables Save`, await save.isEnabled());
        await save.click();
        if (mode === 'pending') {
          await page.waitForFunction(() => !!window.resolveQuantityRead);
          check(`${width} ${panelName}: waits open and busy until saved quantity is read`, await page.evaluate(name => window.qtyTrace.closed === 0 && document.querySelector('[data-acct-modal-panel="' + name + '"] [data-acct-save]').hasAttribute('data-acct-busy'), panelName));
          await page.evaluate(() => window.resolveQuantityRead());
        }
        await page.waitForFunction(name => !document.querySelector('[data-acct-modal-panel="' + name + '"] [data-acct-save]').hasAttribute('data-acct-busy'), panelName);
        const result = await page.evaluate(name => ({...window.qtyTrace, error: document.querySelector('[data-acct-modal-panel="' + name + '"] [data-acct-discount-error]')?.textContent || ''}), panelName);
        check(`${width} ${panelName} ${mode}: exact typed quantity posted once`, result.posts.length === 1 && result.posts[0].url === (panelName === 'edit-product' ? '/update-line-item' : '/add-line-item') && result.posts[0].body.quantity === 12);
        if (mode === 'delayed') {
          check(`${width} ${panelName}: old read retried and saved quantity displayed before closing`, result.reads === 2 && result.displayed === 12 && result.closed === 1);
        } else if (mode === 'pending') {
          check(`${width} ${panelName}: confirmed response updates quantity then closes`, result.displayed === 12 && result.closed === 1);
        } else {
          check(`${width} ${panelName} ${mode}: unresolved save remains open with error`, result.closed === 0 && !!result.error);
        }
        await page.close();
      }
      }
    }
    console.log(`${checks} checks passed`);
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
