const fs = require('node:fs'), path = require('node:path');
const assert = require('node:assert/strict');
const {pathToFileURL} = require('node:url');
const {chromium, webkit} = require('playwright');
const sharp = require('sharp');
(async () => {
  const base = fs.readFileSync(path.join(__dirname, '../../Gumi-Brand-shopify/baseline-20261002-a60/assets/base.css'), 'utf8');
  let checks = 0;
  for (const engine of [chromium, webkit]) {
    const b = await engine.launch(engine === chromium ? {executablePath: process.env.ACCT_CHROME} : {});
    for (const width of [390, 1440]) {
      const p = await b.newPage({viewport: {width, height: 844}, hasTouch: width === 390, isMobile: width === 390, reducedMotion: 'reduce'});
      await p.goto(pathToFileURL(path.join(__dirname, '../account.html')).href);
      await p.evaluate(css => {
        const style = document.createElement('style');
        style.textContent = ':root{--color-foreground:#011307;--color-foreground-rgb:1 19 7;--color-background:#fff;--checkbox-size:16px;--style-border-radius-50:50%;--opacity-85:.85;--opacity-5:.05;--opacity-40-60:.4}' + css;
        document.head.prepend(style);
      }, base);
      for (const panel of ['shipping-current', 'cancel-reason', 'cancel-offer-skip']) {
        await p.evaluate(panel => window.gumiAcct.modal.open(panel), panel);
        const radio = p.locator('.gb-acct-modal.is-open input[type="radio"]').first();
        await radio.evaluate(e => {e.checked = true; e.dispatchEvent(new Event('change', {bubbles: true}));});
        for (const hover of [false, true]) {
          if (hover) await radio.hover(); else await p.mouse.move(0, 0);
          await p.waitForTimeout(250);
          const label = `${engine.name()}/${width}/${panel}/hover=${hover}`;
          const image = await sharp(await radio.screenshot()).ensureAlpha().raw().toBuffer({resolveWithObject: true});
          const index = (Math.floor(image.info.height / 2) * image.info.width + Math.floor(image.info.width / 2)) * 4;
          const pixel = [...image.data.subarray(index, index + 3)];
          assert(pixel.every((v, i) => Math.abs(v - [0, 86, 53][i]) <= 2), label + ': painted dot is green ' + pixel); checks++;
          assert.equal(await radio.evaluate(e => getComputedStyle(e, '::after').display), 'none', label); checks++;
          assert.deepEqual(await radio.evaluate(e => [e.offsetWidth, e.offsetHeight]), [16, 16], label); checks++;
          assert(await radio.evaluate(e => {const s = getComputedStyle(e); return s.borderTopColor === 'rgb(1, 19, 7)' || s.boxShadow.includes('rgb(1, 19, 7)');}), label + ': ink ring preserved'); checks++;
          assert.equal(await radio.evaluate(e => getComputedStyle(e).backgroundColor), 'rgb(233, 250, 207)', label); checks++;
        }
        await p.evaluate(() => window.gumiAcct.modal.close());
      }
      await p.close();
    }
    await b.close();
  }
  console.log(`${checks} checks passed`);
})().catch(e => {console.error(e); process.exit(1);});

