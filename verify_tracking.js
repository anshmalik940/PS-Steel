/* Phase 4 verification: do the ad tracking and conversion events actually fire?
 *
 * The real Google and Meta scripts cannot load in this sandbox, so gtag and fbq
 * are stubbed before each page loads and their calls are recorded. That tests
 * our own code, which is the part being verified.
 */
const { chromium } = require('playwright');

const BASE = 'http://127.0.0.1:8899';
const results = [];
const check = (label, ok, detail = '') =>
  results.push({ ok, line: `${ok ? 'PASS' : 'FAIL'}  ${label}${detail ? ' -> ' + detail : ''}` });

const STUB = () => {
  window.__calls = [];
  window.dataLayer = [];
  window.gtag = (...a) => window.__calls.push(['gtag', ...a]);
  window.fbq = (...a) => window.__calls.push(['fbq', ...a]);
};

(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const ctx = await browser.newContext();
  await ctx.addInitScript(STUB);

  // --- tags present on an ordinary page ---
  let page = await ctx.newPage();
  await page.goto(BASE + '/', { waitUntil: 'domcontentloaded' });
  let html = await page.content();
  check('Google tag script on page', html.includes('googletagmanager.com/gtag/js?id=G-TEST123'));
  check('Meta Pixel script on page', html.includes("fbq('init', 'PIXEL9999')"));
  const readCalls = pg => pg.evaluate(() => [
    ...window.__calls.map(c => c.join(':')),
    ...(window.dataLayer || []).map(a => 'gtag:' + Array.from(a).join(':')),
  ]);
  let calls = await readCalls(page);
  check('Meta PageView fires', calls.some(c => c.startsWith('fbq:track:PageView')), calls.join(' | '));

  // --- no conversion on a bare visit to the thank-you page ---
  await page.goto(BASE + '/thank-you/', { waitUntil: 'domcontentloaded' });
  calls = await readCalls(page);
  check('No conversion on direct visit to /thank-you/',
        !calls.some(c => c.includes('generate_lead') || c.includes('fbq:track:Lead')));
  await page.close();

  // --- a real submission from an ad click ---
  page = await ctx.newPage();
  await page.goto(BASE + '/products/stainless-steel-bowls/?utm_source=google&utm_medium=cpc&utm_campaign=phase4',
                  { waitUntil: 'domcontentloaded' });
  await page.fill('#id_full_name_bulk', 'Tracking Test');
  await page.fill('#id_phone_bulk', '9876500011');
  await page.fill('#id_qty_bulk', '50 kg');
  await Promise.all([
    page.waitForURL('**/thank-you/'),
    page.click('.inquiry-form button[type="submit"]'),
  ]);
  calls = await readCalls(page);
  check('Google generate_lead fires after submit',
        calls.some(c => c.includes('generate_lead')), calls.join(' | '));
  check('Meta Lead fires after submit', calls.some(c => c === 'fbq:track:Lead'));

  // --- refresh must not double-count ---
  await page.reload({ waitUntil: 'domcontentloaded' });
  calls = await readCalls(page);
  check('No duplicate conversion on refresh',
        !calls.some(c => c.includes('generate_lead') || c === 'fbq:track:Lead'));
  await page.close();

  // --- image and SEO audit across the public pages ---
  const pages = ['/', '/products/', '/products/stainless-steel-bowls/', '/about-us/',
                 '/for-resellers/', '/contact/'];
  let missingAlt = [], titles = new Set(), descs = new Set(), noOg = [];
  for (const path of pages) {
    const p = await ctx.newPage();
    await p.goto(BASE + path, { waitUntil: 'domcontentloaded' });
    const info = await p.evaluate(() => ({
      title: document.title,
      desc: document.querySelector('meta[name=description]')?.content || '',
      og: document.querySelector('meta[property="og:image"]')?.content || '',
      canonical: document.querySelector('link[rel=canonical]')?.href || '',
      bad: [...document.images].filter(i => !i.alt || !i.alt.trim()).map(i => i.currentSrc),
    }));
    if (info.bad.length) missingAlt.push(`${path}: ${info.bad.length}`);
    if (!info.og || !info.canonical) noOg.push(path);
    titles.add(info.title);
    descs.add(info.desc);
    await p.close();
  }
  check('Every image has alt text', missingAlt.length === 0, missingAlt.join(', '));
  check('Every page has a unique title', titles.size === pages.length, `${titles.size}/${pages.length}`);
  check('Every page has a unique meta description', descs.size === pages.length, `${descs.size}/${pages.length}`);
  check('Every page has og:image and canonical', noOg.length === 0, noOg.join(', '));

  await browser.close();
  results.forEach(r => console.log(r.line));
  const failed = results.filter(r => !r.ok).length;
  console.log(failed ? `\n${failed} FAILED` : '\nALL TRACKING CHECKS PASSED');
})();
