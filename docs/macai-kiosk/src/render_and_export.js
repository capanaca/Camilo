const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const NM = process.argv[2], HTML = process.argv[3], OUT = process.argv[4], MODE = process.argv[5] || 'test';
(async () => {
  const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const page = await browser.newPage({ viewport: { width: 1600, height: 1000 } });
  const errs = [];
  page.on('console', m => { if (m.type() === 'error' || m.type()==='warning') errs.push(m.type()+': '+m.text()); });
  page.on('pageerror', e => errs.push('pageerror: ' + e.message));
  await page.route('https://cdn.jsdelivr.net/npm/three@0.147.0/**', r => {
    const p = r.request().url().split('three@0.147.0/')[1];
    r.fulfill({ path: path.join(NM, 'three', p), contentType: 'application/javascript' });
  });
  await page.route('https://fonts.googleapis.com/**', r => r.abort());
  await page.goto('file://' + HTML);
  await page.waitForFunction(() => window.__ready === true, null, { timeout: 120000 }).catch(()=>{}); await page.evaluate(()=>window.MACAI && window.MACAI.pause(true));
  const shots = MODE === 'all' ? [
    ['ui_hero', {}],
    ['render_hero_day', { shot: true, view: 'hero' }],
    ['render_hero_night', { shot: true, view: 'hero', night: true }],
    ['render_front', { shot: true, view: 'front' }],
    ['render_operator', { shot: true, view: 'operator' }],
    ['render_end', { shot: true, view: 'side' }],
    ['render_plan', { shot: true, view: 'top' }],
    ['render_toppings', { shot: true, view: 'M2' }],
    ['render_exploded', { shot: true, view: 'hero', explode: true }],
    ['render_transport', { shot: true, view: 'hero', transport: true }],
    ['render_dimensions', { shot: true, view: 'front', dims: true }],
  ] : [['ui_hero', {}], ['render_hero_night', { shot: true, view: 'hero', night: true }]];
  for (const [name, o] of shots) {
    await page.evaluate(o => { const A = window.MACAI; if(!A) return;
      A.shot(!!o.shot); A.setNight(!!o.night); A.setTransport(!!o.transport); A.setDims(!!o.dims); A.setExplode(!!o.explode); A.setView(o.view || 'hero', true); A.settle(); }, o);
    await page.waitForTimeout(300);
    await page.screenshot({ path: path.join(OUT, name + '.png') });
  }
  if (MODE === 'all') {
    await page.evaluate(() => { const A = window.MACAI; A.shot(false); A.setNight(false); A.setTransport(false); A.setDims(false); A.setExplode(false); A.settle(); });
    const b64 = await page.evaluate(async () => { const buf = await window.MACAI.exportGLB(); let s=''; const u=new Uint8Array(buf); for(let i=0;i<u.length;i+=0x8000) s+=String.fromCharCode.apply(null,u.subarray(i,i+0x8000)); return btoa(s); });
    fs.writeFileSync(path.join(OUT, 'macai_cart.glb'), Buffer.from(b64, 'base64'));
  }
  console.log(errs.slice(0, 20).join('\n') || 'no console errors');
  await browser.close();
})();
