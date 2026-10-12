const assert = require('node:assert/strict');
const {chromium} = require('playwright');
(async () => {
  const browser = await chromium.launch({executablePath:process.env.ACCT_CHROME});
  const context = await browser.newContext();
  const origin = 'https://gumi.com.au';
  await context.request.post(origin+'/password',{form:{form_type:'storefront_password',utf8:'✓',password:'1234'}});
  const response = await context.request.get(origin+'/pages/account');
  assert(response.ok(), 'Account HTTP response '+response.status()+' '+response.url());
  const html = await response.text();
  const page = await context.newPage();
  // Inspect server output without executing the unsigned-customer redirect.
  await page.setContent(html.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi,''));
  const header = await page.locator('#site-header').evaluate(el => el.outerHTML);
  assert(header.includes('gb-acct-header__toggle'), 'live account hamburger');
  assert(!header.includes('gb-acct-header__cart') && !header.includes('gb-header__cta'), 'old icons/CTA absent');
  const urls = await page.locator('link[rel="stylesheet"]').evaluateAll(els => els.map(el=>el.getAttribute('href')).filter(url=>/customstyle\.css|account\.css/.test(url)));
  assert(urls.length === 2, 'live stylesheet URLs');
  const script = [...html.matchAll(/<script\b[^>]*src=["']([^"']+)["']/gi)].map(m=>m[1]).find(url=>/\/main\.js/.test(url));
  assert(script,'live main.js URL');
  const css = await Promise.all(urls.map(async url => {
    const res = await context.request.get(new URL(url, origin).href); assert(res.ok()); return res.text();
  }));
  const js = await context.request.get(new URL(script, origin).href); assert(js.ok());
  for (const width of [390,1440]) {
    await page.setViewportSize({width,height:844});
    await page.setContent('<html><head><base href="'+origin+'"><style>'+css.join('\n')+'</style></head><body>'+header+'</body></html>');
    await page.addScriptTag({content:await js.text()});
    await page.evaluate(() => document.dispatchEvent(new Event('DOMContentLoaded')));
    const size = await page.locator('.gb-acct-header__logo').evaluate(el => {
      const b=el.getBoundingClientRect(), art=el.querySelector('img,svg').getBoundingClientRect(); return [b.width,b.height,art.width,art.height];
    });
    assert.deepEqual(size, width === 390 ? [92,24,92,24] : [123,32,123,32]);
    await page.locator('.gb-acct-header__toggle').click();
    await page.waitForTimeout(500);
    assert.equal(await page.locator('.gb-acct-header__toggle').getAttribute('aria-expanded'),'true');
    assert(await page.locator('.gb-header__links--mobile a').count()>0, 'configured mobile links render');
    if (width === 390) {
      assert.equal(await page.locator('#site-menu').evaluate(el=>getComputedStyle(el).position),'fixed');
      await page.locator('.gb-header__panel-close').click();
    } else {await page.keyboard.press('Escape');}
    await page.waitForTimeout(500);
    assert.equal(await page.locator('.gb-acct-header__toggle').getAttribute('aria-expanded'),'false');
    console.log('PASS live-rendered Account header, CDN CSS/JS, logo/menu at '+width);
  }
  const home = await context.request.get(origin+'/');
  assert((await home.text()).includes('gb-header__cta'), 'homepage keeps Shop now');
  console.log('PASS live homepage retains original header CTA');
  await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
