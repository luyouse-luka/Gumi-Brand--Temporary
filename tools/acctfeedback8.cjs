const fs = require('node:fs'), path = require('node:path');
const assert = require('node:assert/strict');
const {pathToFileURL} = require('node:url');
const {chromium} = require('playwright');
(async () => {
  const root = path.join(__dirname, '..');
  const source = fs.readFileSync(path.join(root, 'liquid/account-feedback/snippets/gb-account-data.liquid'), 'utf8');
  const raw = source.match(/<script[^>]*>([\s\S]*?)<\/script>/)[1];
  const sample = [{id: 123, created_at: new Date().toISOString(), fulfillment_status: 'fulfilled'}];
  const runtime = raw.slice(0, raw.indexOf('    var CUSTOMER_EMAIL')) +
    `var CUSTOMER_EMAIL=null, ADD_PRODUCTS=[], CUSTOMER_ORDERS=${JSON.stringify(sample)};\n` +
    raw.slice(raw.indexOf('    // Money is in minor units')).replace(/\{\{[\s\S]*?\}\}/g, 'null');
  new Function(runtime);
  const capture = source.slice(source.indexOf('    // Capture click on any modal primary action'), source.indexOf('    // ────────── Overview:'));
  new Function(capture);
  let count = 0;
  const check = (name, value) => {assert(value, name); count++; console.log('PASS ' + name);};
  const b = await chromium.launch({executablePath: process.env.ACCT_CHROME});
  for (const width of [390, 767, 768, 1440]) {
    const p = await b.newPage({viewport: {width, height: 844}, hasTouch: true, isMobile: width <= 767, reducedMotion: 'reduce'});
    await p.goto(pathToFileURL(path.join(root, 'account.html')).href);
    await p.waitForTimeout(300);
    const alignment = await p.evaluate(() => {
      const t = document.querySelector('.gb-acct-sub__totals');
      t.querySelector('.gb-acct-sub__more')?.remove();
      const total = t.querySelector('.gb-acct-sub__total');
      const m = document.querySelector('.gb-acct-product__meta');
      m.querySelector('.gb-acct-product__flavour')?.remove();
      const price = m.querySelector('.gb-acct-product__price');
      return [Math.abs(total.getBoundingClientRect().right - t.getBoundingClientRect().right) < 1,
        Math.abs(price.getBoundingClientRect().right - m.getBoundingClientRect().right) < 1];
    });
    check(`${width}: sole total aligns right`, alignment[0]);
    check(`${width}: sole price aligns right`, alignment[1]);
    check(`${width}: bear is not clipped by artwork`, await p.locator('.gb-acct-hello__art').evaluate(e => getComputedStyle(e).overflow === 'visible'));
    await p.evaluate(() => window.gumiAcct.modal.open('discount-applied'));
    const chip = await p.evaluate(() => {
      const panel = document.querySelector('[data-acct-modal-panel="discount-applied"]');
      const result = panel.querySelector('.gb-acct-discount__result');
      result.hidden = false;
      if (!result.querySelector('.gb-acct-chip')) result.appendChild(result.querySelector('template').content.cloneNode(true));
      const e = result.querySelector('.gb-acct-chip');
      e.querySelector('p').innerHTML = 'Discount <strong>' + 'LONGCODE'.repeat(25) + '</strong> applied $8.00 off';
      const error = document.createElement('div');
      error.className = 'gb-acct-modal__alert';
      error.setAttribute('data-acct-discount-error', '');
      error.innerHTML = '<p>Discount code not found</p>';
      panel.querySelector('.gb-acct-discount').appendChild(error);
      const strong = e.querySelector('strong'), remove = e.querySelector('[data-acct-chip-remove]');
      const input = panel.querySelector('[data-acct-discount-input]');
      return {ellipsis: getComputedStyle(strong).textOverflow === 'ellipsis' && strong.scrollWidth > strong.clientWidth,
        trash: remove.getBoundingClientRect().right <= e.getBoundingClientRect().right,
        height: [input.offsetHeight, error.offsetHeight, e.offsetHeight],
        radius: [input, error, e].map(x => getComputedStyle(x).borderTopLeftRadius),
        overflow: document.documentElement.scrollWidth > innerWidth};
    });
    check(`${width}: long code has ellipsis`, chip.ellipsis);
    check(`${width}: trash remains inside chip`, chip.trash);
    check(`${width}: field/error/success heights match`, chip.height.every(x => x === 44));
    check(`${width}: field/error/success radii match`, new Set(chip.radius).size === 1);
    check(`${width}: no page overflow`, !chip.overflow);
    await p.evaluate(() => window.gumiAcct.modal.close());
    if (width === 390) {
      const c = await p.context().newCDPSession(p);
      for (const name of ['add-product', 'shipping-form']) {
        await p.evaluate(name => window.gumiAcct.modal.open(name), name);
        await p.waitForTimeout(150);
        const body = p.locator('.gb-acct-modal.is-open .gb-acct-modal__body');
        check(`${name}: body has scrollable content`, await body.evaluate(e => e.scrollHeight > e.clientHeight));
        await c.send('Input.dispatchTouchEvent', {type: 'touchStart', touchPoints: [{x: 150, y: 650}]});
        for (let y = 620; y >= 320; y -= 30) {
          await c.send('Input.dispatchTouchEvent', {type: 'touchMove', touchPoints: [{x: 150, y}]});
          await p.waitForTimeout(30);
        }
        await c.send('Input.dispatchTouchEvent', {type: 'touchEnd', touchPoints: []});
        await p.waitForTimeout(150);
        check(`${name}: actual touch events scroll body`, await body.evaluate(e => e.scrollTop > 100));
        await p.evaluate(() => window.gumiAcct.modal.close());
        await p.waitForTimeout(150);
      }
    }
    await p.close();
  }
  const p = await b.newPage({viewport: {width: 390, height: 844}, reducedMotion: 'reduce'});
  await p.goto(pathToFileURL(path.join(root, 'account.html')).href);
  await p.waitForTimeout(300);
  await p.evaluate(runtime => {window.fetch = () => new Promise(() => {}); eval(runtime);}, runtime);
  check('recent order renders while subscription fetch remains pending', await p.locator('.gb-acct-order').isVisible());
  await p.close();
  const q = await b.newPage({viewport: {width: 390, height: 844}, reducedMotion: 'reduce'});
  await q.goto(pathToFileURL(path.join(root, 'account.html')).href + '#detail');
  await q.waitForTimeout(300);
  await q.evaluate(capture => {
    const contract = {id: '42'};
    const submit = {'discount-add': () => Promise.resolve({ok: true, j: {ok: true}})};
    const currentContract = () => contract;
    const detailRoot = document.querySelector('[data-acct-view="detail"]');
    const activeDiscounts = c => c.discounts || [];
    const refetchAndRerender = () => new Promise(resolve => {window.resolveDiscount = resolve;});
    const prefill = {'discount-applied': (panel, c) => {
      const result = panel.querySelector('.gb-acct-discount__result');
      result.hidden = false;
      result.innerHTML = '<div class="gb-acct-chip"><p>Discount ' + c.discounts[0].code + ' applied $8.00 off</p></div>';
    }};
    eval(capture);
    window.gumiAcct.modal.open('discount-add');
    document.querySelector('[data-acct-modal-panel="discount-add"] [data-acct-discount-input]').value = 'REAL_CODE';
    const apply = document.querySelector('[data-acct-modal-panel="discount-add"] [data-acct-apply]');
    apply.disabled = false;
    apply.click();
  }, capture);
  await q.waitForTimeout(100);
  check('apply stays loading until real subscription details return', await q.locator('[data-acct-modal-panel="discount-add"] [data-acct-apply]').evaluate(e => e.classList.contains('is-loading')));
  check('no code-only success is shown while amount is pending', await q.locator('[data-acct-modal-panel="discount-add"]').isVisible());
  await q.evaluate(() => window.resolveDiscount({id: '42', discounts: [{code: 'REAL_CODE', amount: 8}]}));
  await q.waitForTimeout(200);
  check('confirmed success shows code and amount together', await q.locator('[data-acct-modal-panel="discount-applied"]').isVisible() && (await q.locator('[data-acct-modal-panel="discount-applied"] .gb-acct-chip').innerText()).includes('$8.00 off'));
  await b.close();
  console.log(`${count} checks passed`);
})().catch(e => {console.error(e); process.exit(1);});
