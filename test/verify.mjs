/* Invariants for the Dialogue Society signature.
 *
 *   node test/verify.mjs
 *
 * Every check here exists because something actually broke in a real mail
 * client. Read CLAUDE.md before relaxing any of them.
 *
 * The suite serves dist/signature over http, drives it with a real browser,
 * copies the signature to the clipboard, and then abuses the copied markup
 * the way Apple Mail does -- stripping widths, heights and font sizes -- to
 * confirm it still holds together.
 */
import { chromium } from 'playwright';
import { createServer } from 'http';
import { readFileSync, existsSync } from 'fs';
import { extname, join } from 'path';

const DIST = 'dist/site';
const PORT = 8971;
const MIME = { '.html': 'text/html', '.png': 'image/png', '.txt': 'text/plain' };

let pass = 0, fail = 0;
const ok = (name, cond, detail = '') => {
  if (cond) { pass++; console.log(`  ok    ${name}`); }
  else { fail++; console.log(`  FAIL  ${name}${detail ? '  -> ' + detail : ''}`); }
};

/* strip in the order a real sanitiser would: longest property first, or the
   width rule eats the tail of min-width and corrupts the declaration after it */
const strip = h => h
  .replace(/\swidth="\d+"/g, '').replace(/\sheight="\d+"/g, '')
  .replace(/(min-|max-)?width:\s*[\d.]+px;?/gi, '')
  .replace(/(min-|max-)?height:\s*[\d.]+px;?/gi, '')
  .replace(/font-size:\s*[\d.]+px;?/gi, '')
  .replace(/line-height:\s*[\d.]+px;?/gi, '');

const server = createServer((req, res) => {
  const rel = req.url === '/' ? 'index.html' : decodeURIComponent(req.url.slice(1));
  const file = join(DIST, rel);
  if (!existsSync(file)) { res.writeHead(404); return res.end('nope'); }
  res.writeHead(200, { 'Content-Type': MIME[extname(file)] || 'application/octet-stream' });
  res.end(readFileSync(file));
});
await new Promise(r => server.listen(PORT, r));

/* Playwright's own download is the default. PW_CHROMIUM overrides it for a
   sandbox or CI image that ships its browser somewhere else -- the path used
   to be hardcoded to one such image, which meant the suite could not run on
   anyone's laptop. */
const browser = await chromium.launch(
  process.env.PW_CHROMIUM ? { executablePath: process.env.PW_CHROMIUM } : {});
const ctx = await browser.newContext({
  permissions: ['clipboard-read', 'clipboard-write'],
  viewport: { width: 1150, height: 1000 },
});

async function signatureFor(mode) {
  const p = await ctx.newPage();
  const errs = [];
  p.on('pageerror', e => errs.push(String(e)));
  /* domcontentloaded, not load: the page pulls its webfonts from Google, and a
     slow or blocked font request should not decide whether the suite runs. */
  await p.goto(`http://localhost:${PORT}/`, { waitUntil: 'domcontentloaded' });
  await p.waitForTimeout(1200);
  await p.evaluate(() => { try { localStorage.clear(); } catch (e) {} });
  await p.reload({ waitUntil: 'domcontentloaded' });
  await p.waitForTimeout(1000);

  if (mode === 'person') {
    await p.click('input[name=lead][value=person]');
    await p.fill('#i-name', 'Sadik Cinar');
    await p.fill('#i-title', 'Executive Director');
    await p.fill('#i-email', 'scinar@dialoguesociety.org');
  } else {
    await p.click('input[name=lead][value=org]');
    await p.fill('#i-strap', 'Building Community Trust');
    await p.fill('#i-email', 'info@dialoguesociety.org');
  }
  await p.waitForTimeout(400);
  await p.click('#copy');
  await p.waitForTimeout(350);
  const html = await p.evaluate(async () => {
    const items = await navigator.clipboard.read();
    for (const i of items)
      if (i.types.includes('text/html'))
        return await (await i.getType('text/html')).text();
    return '';
  });
  await p.close();
  return { html, errs };
}

/* Render some signature markup in a container of the given width and report
   the structural facts we care about. */
async function inspect(html, width) {
  const p = await ctx.newPage();
  await p.setContent(`<body style="margin:0"><div style="width:${width}px">${html}</div></body>`);
  await p.waitForTimeout(250);
  const r = await p.evaluate(() => {
    const t = document.querySelector('table');
    const tds = [...t.querySelectorAll(':scope>tbody>tr>td')];
    const img = document.querySelector('img');
    const ruleCell = tds.find(td => getComputedStyle(td).borderLeftWidth === '4px');
    const hair = [...document.querySelectorAll('td')]
      .find(td => getComputedStyle(td).borderTopWidth === '1px');
    const fatBar = [...document.querySelectorAll('td')].some(td =>
      getComputedStyle(td).backgroundColor === 'rgb(220, 220, 220)' &&
      td.getBoundingClientRect().height > 3);
    const ir = img.getBoundingClientRect();
    const tr = tds[tds.length - 1].getBoundingClientRect();
    return {
      cells: tds.length,
      rule: !!ruleCell,
      hairline: hair ? getComputedStyle(hair).borderTopWidth : 'none',
      fatBar,
      imgW: Math.round(ir.width),
      logoLeftOfText: ir.right <= tr.left + 2,
    };
  });
  await p.close();
  return r;
}

/* The site is public and has no access control, so the pages must stay out of
   search results -- personal.html carries a name, a job title and a work
   address. On a GitHub project page the noindex meta is the whole mechanism:
   a crawler reads robots.txt only at the domain root, which this is not. */
for (const f of ['index.html', 'personal.html', 'branch.html']) {
  const page = readFileSync(join(DIST, f), 'utf8');
  ok(`${f} is noindex`, /<meta name="robots" content="noindex, nofollow">/.test(page));
}

for (const mode of ['person', 'org']) {
  console.log(`\n${mode === 'person' ? 'PERSONAL' : 'BRANCH'} signature`);
  const { html, errs } = await signatureFor(mode);

  ok('page raises no JS errors', errs.length === 0, errs[0]);
  ok('clipboard carries a table', /<table/i.test(html));

  /* The clipboard payload has to be a well-formed document, not a selection
     fragment. Apple Mail promotes the data-URI logo to a cid: attachment as it
     pastes and re-opens the document at that point; against a fragment carrying
     a stray <head> the seam landed mid-table, the logo cell was emptied to
     <tr></td></tr> and the image was hoisted out above the text. See COPY_JS in
     src/theme.py. */
  /* A <head> is only legal inside a document. Selection copying emitted one
     into a bare fragment, and that is where Mail re-opened the markup. */
  ok('no <head> outside a document',
     !/<head[\s>]/i.test(html) || /<html[\s>]/i.test(html), html.slice(0, 70));
  ok('logo <img> sits inside a <td>',
     /<td[^>]*>(?:(?!<\/td>)[\s\S])*?<img/i.test(html));
  ok('page chrome does not leak into the signature',
     !/IBM Plex Sans|caret-color|box-sizing/i.test(html));

  /* colour discipline */
  ok('uses brand blue #008AC4', /#008AC4|rgb\(0, 138, 196\)/i.test(html));
  ok('uses text blue #007AAD', /#007AAD|rgb\(0, 122, 173\)/i.test(html));
  ok('no #0797C8 (off-brand, fails AA)', !/0797C8|rgb\(7, 151, 200\)/i.test(html));
  ok('no invented navy/slate greys',
     !/183B5B|5B6F82|4B5563|7A8793/i.test(html));

  /* structure, at sane and hostile widths, before and after stripping */
  for (const [w, src, label] of [
    [520, html, 'roomy pane'],
    [300, html, 'narrow pane'],
    [300, strip(html), 'narrow pane, styles stripped'],
    [240, strip(html), 'very narrow pane, styles stripped'],
  ]) {
    const r = await inspect(src, w);
    ok(`${label}: two cells, logo left`,
       r.cells === 2 && r.logoLeftOfText, `cells=${r.cells} left=${r.logoLeftOfText}`);
    ok(`${label}: blue rule survives as a border`, r.rule);
    ok(`${label}: logo stays 70px`, r.imgW <= 75, `${r.imgW}px`);
    ok(`${label}: hairline is 1px, not a bar`,
       r.hairline === '1px' && !r.fatBar, `hairline=${r.hairline} fatBar=${r.fatBar}`);
  }
}

console.log(`\n${pass} passed, ${fail} failed`);
await browser.close();
server.close();
process.exit(fail ? 1 : 0);
