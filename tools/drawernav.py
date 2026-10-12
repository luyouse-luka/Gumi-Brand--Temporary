"""Mobile drawer CTA + accordion slide + the nav card art on the drawer's exit.

  python3 tools/drawernav.py [--reverse]

  1 The CTA is FIXED to the drawer floor (r132) -- its containing block is
    .gb-header__panel, which carries the drawer's translateX, so it rides the
    slide and does not scroll with the menu. The column reserves its room --
    52 button + the client's 57 -- so 57 is the MINIMUM gap to the links: with
    slack in the drawer it is larger, and it is exactly 57 at the scroll floor.
  2 The accordion moves on the body's height ALONE, all the way to zero. r132
    moved .gb-acc-body's 10px top gap onto its first child: a border-box with
    padding cannot render shorter than that padding, so the collapse stalled at
    10px and then dropped the last 10 in a single frame. Until r131 the gap under
    a row was booked twice -- summary padding-bottom while shut, .gb-acc-body
    padding-bottom while open -- so opening ran the summary's padding to 0 over
    300ms while main.js slid the body over 400ms (the copy drifted up as it was
    revealed) and closing put the 24 back AFTER the slide had finished (the row
    bounced). Judged on effects: the body's top edge must not move while it
    opens, and the item's height must never reverse while it closes.
  3 .gb-nav-card__art must survive the drawer's exit. Its display is gated on
    .is-open, so without `transition: display allow-discrete` it blinks out the
    instant the class goes, with the whole $t-drawer slide still to play.

  --reverse re-injects the pre-r131 accordion rules; section 2 must go RED.
"""
import sys
from playwright.sync_api import sync_playwright
CHROME='/home/ly/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome'
LIVE='https://gumi.com.au'
REVERSE = '--reverse' in sys.argv
PW = (sys.argv[sys.argv.index('--password')+1]
      if '--password' in sys.argv else None)
LIVE_MODE = '--live' in sys.argv
if LIVE_MODE:
    URL, PDP, FAQ = LIVE+'/', None, LIVE+'/pages/faq'   # PDP handle resolved below
else:
    URL='file:///home/ly/project/Gumi-Brand/index.html'
    PDP='file:///home/ly/project/Gumi-Brand/pdp.html'
    FAQ='file:///home/ly/project/Gumi-Brand/faq.html'

OLD = """
.gb-product__acc-item { padding-bottom: 0 }
.gb-acc-body { padding-bottom: var(--acc-gap, 20px) }
.gb-product__acc-row { padding-bottom: var(--acc-gap);
  transition: color .2s cubic-bezier(.33,1,.68,1), padding-bottom .3s cubic-bezier(.33,1,.68,1) }
.gb-product__acc-item:not([open]) > .gb-product__acc-row { margin-bottom: 0 }
.gb-product__acc-item[open] > .gb-product__acc-row { padding-bottom: 0 }
.gb-faq__item { padding-bottom: 0 }
.gb-faq__row { padding-bottom: var(--acc-gap);
  transition: color .2s cubic-bezier(.33,1,.68,1), padding-bottom .3s cubic-bezier(.33,1,.68,1) }
.gb-faq__item:not([open]) > .gb-faq__row { margin-bottom: 0 }
.gb-faq__item[open] > .gb-faq__row { padding-bottom: 0 }
.gb-acc-body { padding-top: 10px }
.gb-acc-body > :first-child { margin-top: 0 }
"""

def ctxp(br, **kw):
    ctx=br.new_context(**kw)
    if PW: ctx.request.post(LIVE+'/password', form={
        'form_type':'storefront_password','utf8':'✓','password':PW})
    return ctx

ok=red=0
def check(l,c,g,w):
    global ok,red
    if c: ok+=1; print(f'  ok   {l}: {g}')
    else: red+=1; print(f'  RED  {l}: got {g}, want {w}')

with sync_playwright() as p:
    br=p.chromium.launch(executable_path=CHROME)

    if LIVE_MODE:
        # the live handle is not the static build's; take it off the collection
        ctx=ctxp(br, viewport={'width':1440,'height':900}); pg=ctx.new_page()
        pg.goto(LIVE+'/collections/all', wait_until='load', timeout=90000)
        pg.wait_for_timeout(1500)
        h=pg.evaluate("() => (document.querySelector('a[href*=\"/products/\"]')||{}).pathname")
        pg.close(); ctx.close()
        if not h: sys.exit('ABORT: no product found on /collections/all')
        PDP = LIVE + h
        print(f'   live PDP: {PDP}')

    print('1  drawer CTA: absolute on the floor, 57 reserved above it')
    for vh, label in ((844, 'roomy'), (600, 'scrolling')):
        ctx=ctxp(br, viewport={'width':390,'height':vh}); pg=ctx.new_page()
        pg.goto(URL,wait_until='load'); pg.wait_for_timeout(900)
        pg.evaluate("() => document.querySelector('.gb-header__toggle').click()")
        pg.wait_for_timeout(1200)
        r=pg.evaluate("""() => {
          const nav=document.querySelector('.gb-header__nav');
          const btn=document.querySelector('.gb-header__nav .gb-btn--lg');
          const inner=document.querySelector('.gb-header__panel-inner');
          const links=document.querySelector('.gb-header__links--mobile');
          const panel=document.querySelector('.gb-header__panel');
          const R=e=>e.getBoundingClientRect();
          return {gap: Math.round(R(btn).top-R(links).bottom),
                  reserve: getComputedStyle(nav).paddingBottom,
                  pos: getComputedStyle(document.querySelector('.gb-header__nav-cta')).position,
                  barBg: getComputedStyle(document.querySelector('.gb-header__nav-cta')).backgroundColor,
                  panelBg: getComputedStyle(panel).backgroundColor,
                  barTop: Math.round(R(document.querySelector('.gb-header__nav-cta')).top),
                  barW: Math.round(R(document.querySelector('.gb-header__nav-cta')).width),
                  // a point inside the bar but left of the button: whatever is
                  // scrolled under it must not show through
                  masks: (()=>{const b=R(document.querySelector('.gb-header__nav-cta'));
                    const e=document.elementFromPoint(4, b.top+4);
                    return !!(e && e.closest('.gb-header__nav-cta'));})(),
                  scrollPad: getComputedStyle(
                      document.querySelector('.gb-header__panel-clip')).scrollPaddingBottom,
                  panelScrolls: panel.scrollHeight - panel.clientHeight,
                  panelBottom: Math.round(R(panel).bottom),
                  hits: (()=>{const c=R(btn); const e=document.elementFromPoint(
                      c.left+c.width/2, c.top+c.height/2);
                    return !!(e && (e===btn || btn.contains(e)));})(),
                  left: Math.round(R(btn).left), navLeft: Math.round(R(nav).left),
                  width: Math.round(R(btn).width), navWidth: Math.round(R(nav).width),
                  btnBottom: Math.round(R(btn).bottom),
                  floor: Math.round(R(panel).bottom)-20,
                  scrolls: (()=>{const c=document.querySelector('.gb-header__panel-clip');
                    return c.scrollHeight - c.clientHeight;})()};
        }""")
        if vh == 844:
            check('the CTA bar is fixed', r['pos']=='fixed', r['pos'], 'fixed')
            # against the drawer's own colour, not a literal: the point is that
            # nothing shows through, whatever $c-cream happens to be
            check('the bar carries the drawer ground', r['barBg']==r['panelBg'],
                  f"{r['barBg']} vs panel {r['panelBg']}", 'equal')
            check('the bar spans the drawer', r['barW']==390, r['barW'], 390)
            check('the bar masks what scrolls under it', r['masks'], r['masks'], True)
            check('bar height = 20 + 44 + 20', r['panelBottom']-r['barTop']==84,
                  r['panelBottom']-r['barTop'], 84)
            check('the drawer is its containing block, not the viewport',
                  r['btnBottom']==r['panelBottom']-20,
                  f"btn {r['btnBottom']} vs panel {r['panelBottom']} - 20", 'equal')
            check('the panel-clip does not clip it', r['hits'], r['hits'], True)
            check('scroll padding clears the CTA bar', r['scrollPad']=='84px',
                  r['scrollPad'], '84px')
            check('the drawer itself does not scroll', r['panelScrolls']==0,
                  r['panelScrolls'], '0 (the clip scrolls instead)')
            check('reserve is the client 80', r['reserve']=='80px', r['reserve'], '80px')
            check('CTA keeps the gutter', r['left']==r['navLeft'], f"{r['left']} vs nav {r['navLeft']}", 'equal')
            check('CTA keeps its width', r['width']==min(r['navWidth'],520),
                  f"{r['width']} vs min(nav {r['navWidth']}, 520)", 'equal')
        check(f'[{label}] CTA on the drawer floor', abs(r['btnBottom']-r['floor'])<=1,
              f"{r['btnBottom']} vs {r['floor']}", '<=1px')
        # only meaningful where the menu fits: a fixed footer necessarily covers
        # content that is still below the fold, so the scrolling tier is judged
        # at its scroll floor instead (below)
        if vh == 844:
            check(f'[{label}] gap to links >= 57', r['gap']>=57, r['gap'], '>= 57')
        if vh == 600:
            check('the short drawer really scrolls', r['scrolls']>0, r['scrolls'], '> 0')
            f=pg.evaluate("""async () => {
              const panel=document.querySelector('.gb-header__panel');
              const btn=document.querySelector('.gb-header__nav .gb-btn--lg');
              const links=document.querySelector('.gb-header__links--mobile');
              const before=Math.round(btn.getBoundingClientRect().bottom);
              document.querySelector('.gb-header__panel-clip').scrollTop = 99999;
              await new Promise(r=>setTimeout(r,300));
              return {before, after: Math.round(btn.getBoundingClientRect().bottom),
                      gapAtFloor: Math.round(btn.getBoundingClientRect().top
                                             - links.getBoundingClientRect().bottom)};
            }""")
            check('CTA holds the floor while the menu scrolls',
                  f['before']==f['after'], f"{f['before']} -> {f['after']}", 'unchanged')
            # ⚠ The reserve lives on the nav, the CTA hangs off the panel, and the
            # inner's own 40 padding-bottom sits between them, so what the reader
            # sees at the scroll floor is reserve + 40 - bottom - height, NOT
            # reserve - height. r132's numbers happened to cancel (bottom 40 =
            # inner padding 40, so 109 - 52 = 57); r134's give 80+40-20-44 = 56.
            check('gap at the scroll floor = 80 + 40 - 20 - 44',
                  f['gapAtFloor']==80+40-20-44, f['gapAtFloor'], 80+40-20-44)
        pg.close(); ctx.close()

    print('2  accordion: the body opens without the copy drifting, closes without a bounce')
    # both families share .gb-acc-body and the same summary/gap arrangement, so
    # both move when the arrangement does
    for url, sel, fam in ((PDP,'.gb-product__acc-item','product'), (FAQ,'.gb-faq__item','faq')):
     ctx=ctxp(br, viewport={'width':390,'height':844}); pg=ctx.new_page()
     pg.goto(url,wait_until='load'); pg.wait_for_timeout(900)
     if REVERSE:
        pg.add_style_tag(content=OLD); pg.wait_for_timeout(200)
        print('  (--reverse: pre-r131 rules injected)')
     s=pg.evaluate("""async (sel) => {
      const it=document.querySelector(sel);
      const body=it.querySelector('.gb-acc-body');
      const sum=it.querySelector('summary');
      const cs=e=>getComputedStyle(e);
      const foot=()=>Math.round(sum.getBoundingClientRect().height
                                + parseFloat(cs(sum).marginBottom));
      // elementFromPoint is viewport-relative, so the row has to be on screen
      window.scrollTo({top: it.getBoundingClientRect().top + scrollY - 300,
                       behavior: 'instant'});
      await new Promise(r=>setTimeout(r,400));
      // faq.html ships its first row open; start from a known shut state
      if (it.open) { it.open = false; await new Promise(r=>setTimeout(r,200)); }
      const shutH=Math.round(it.getBoundingClientRect().height);
      const footShut=foot();
      // hit test: the gap under a shut row belongs to the summary (r64). Sample
      // below the label's line box, inside the 24 the row now rebuilds with
      // padding + an equal negative margin.
      const rb=sum.getBoundingClientRect();
      const y=rb.bottom-12, textBottom=rb.top+parseFloat(cs(sum).paddingTop)+24;
      const el=document.elementFromPoint(rb.left+20, y);
      const hit=!!(el && el.closest('summary')===sum && y>textBottom);

      const tops=[]; const t0=performance.now();
      sum.click();
      await new Promise(res=>{(function t(){
        tops.push(body.getBoundingClientRect().top);
        if(performance.now()-t0<700) requestAnimationFrame(t); else res();
      })();});
      const footOpen=foot();
      const openH=Math.round(it.getBoundingClientRect().height);

      const hs=[], bh=[]; const t1=performance.now();
      sum.click();
      await new Promise(res=>{(function t(){
        hs.push([Math.round(performance.now()-t1), it.getBoundingClientRect().height]);
        bh.push(body.getBoundingClientRect().height);
        if(performance.now()-t1<900) requestAnimationFrame(t); else res();
      })();});
      let rise=0, worst=0, step=0;
      for(let i=1;i<hs.length;i++){const d=hs[i][1]-hs[i-1][1];
        if(d>0.5){rise++; worst=Math.max(worst,d);}
        if(hs[i][0]>405) step=Math.max(step, -d);}   // slide ends at 400ms
      return {drift: Math.round(Math.max(...tops)-Math.min(...tops)),
              footShut, footOpen, shutH, openH, minBody: Math.round(Math.min(...bh)),
              endH: Math.round(hs[hs.length-1][1]), rise, worst: Math.round(worst),
              step: Math.round(step*10)/10, hit};
    }""", sel)
     check(f'[{fam}] body top holds while it opens', s['drift']<=1, f"{s['drift']}px drift", '<= 1px')
     check(f'[{fam}] summary footprint is state-independent', s['footShut']==s['footOpen'],
           f"shut {s['footShut']} vs open {s['footOpen']}", 'equal')
     check(f'[{fam}] item height never reverses while closing', s['rise']==0,
           f'{s["rise"]} rising frames, worst +{s["worst"]}px', '0')
     check(f'[{fam}] closed height restored', abs(s['endH']-s['shutH'])<=1,
           f"{s['endH']} vs {s['shutH']}", '<=1px')
     check(f'[{fam}] the body collapses all the way to 0', s['minBody']<=1,
           f"floor {s['minBody']}px", '<= 1px')
     check(f'[{fam}] no step after the slide has finished', s['step']<=2,
           f"largest frame drop past 405ms: {s['step']}px", '<= 2px')
     check(f'[{fam}] the gap under a shut row is still clickable', s['hit'], s['hit'], True)
     check(f'[{fam}] the body actually opened', s['openH']>s['shutH']+20,
           f"{s['openH']} vs {s['shutH']}", '> +20')
     pg.close(); ctx.close()

    print('3  nav card art survives the drawer exit')
    ctx=ctxp(br, viewport={'width':390,'height':844}); pg=ctx.new_page()
    pg.goto(URL,wait_until='load'); pg.wait_for_timeout(900)
    r=pg.evaluate("""async () => {
      document.querySelector('.gb-header__toggle').click();
      await new Promise(r=>setTimeout(r,1200));
      const art=document.querySelector('.gb-nav-card__art');
      const openDisp=getComputedStyle(art).display;
      const frames=[];
      const close=document.querySelector('.gb-header__panel-close');
      const t0=performance.now();
      close.click();
      await new Promise(res=>{(function tick(){
        frames.push([Math.round(performance.now()-t0), getComputedStyle(art).display]);
        if(performance.now()-t0<1000) requestAnimationFrame(tick); else res();
      })();});
      const gone=frames.find(f=>f[1]==='none');
      return {openDisp, goneAt: gone?gone[0]:null, last: frames[frames.length-1][1]};
    }""")
    check('art shown while open', r['openDisp']=='block', r['openDisp'], 'block')
    check('art stays through the slide', r['goneAt'] is None or r['goneAt']>=600,
          f"went none at {r['goneAt']}ms", '>= 600ms (drawer is 700ms)')
    check('art ends hidden', r['last']=='none', r['last'], 'none')

    print('4  r131 changed the motion, not the geometry')
    # Moving the gap from the summary to the item must leave both settled states
    # pixel-identical. Measured against the pre-r131 rules injected into the same
    # page, so the two runs differ by nothing else.
    geo={}
    for tag, old in (('r131', False), ('pre', True)):
        ctx=ctxp(br, viewport={'width':1440,'height':900}); pg=ctx.new_page()
        pg.goto(PDP,wait_until='load'); pg.wait_for_timeout(900)
        if old: pg.add_style_tag(content=OLD); pg.wait_for_timeout(200)
        geo[tag]=pg.evaluate("""async () => {
          const list=document.querySelector('.gb-product__accordion');
          const items=[...list.querySelectorAll('.gb-product__acc-item')];
          const snap=()=>{const L=list.getBoundingClientRect();
            return [Math.round(L.height)].concat(items.flatMap(i=>{
              const r=i.getBoundingClientRect(), s=i.querySelector('summary').getBoundingClientRect();
              return [Math.round(r.top-L.top), Math.round(r.height), Math.round(s.top-L.top)];}));};
          const shut=snap();
          items[0].querySelector('summary').click();
          await new Promise(r=>setTimeout(r,1000));
          return {shut, open: snap()};
        }""")
        pg.close(); ctx.close()
    check('shut geometry unchanged', geo['r131']['shut']==geo['pre']['shut'],
          f"{geo['r131']['shut'][:4]}… vs {geo['pre']['shut'][:4]}…", 'identical')
    check('open geometry unchanged', geo['r131']['open']==geo['pre']['open'],
          f"{geo['r131']['open'][:4]}… vs {geo['pre']['open'][:4]}…", 'identical')
    br.close()
print(f'\n{ok} ok / {red} red')
sys.exit(1 if red else 0)
