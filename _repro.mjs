import { webkit, chromium } from 'playwright';
import DS from './src/template.js';

const sig = DS.build({ lead:'org', branch:'', strap:'Building Community Trust',
  email:'', phone:'', address:'29 High Holborn, London WC1V 6AZ',
  socials:true, charity:true, logo:'ds-mark.png' });

/* what CLAUDE.md says Apple Mail removes */
const strip = h => h
  .replace(/\swidth="\d+"/g,'').replace(/\sheight="\d+"/g,'')
  .replace(/(min-|max-)?width:\s*[\d.]+px;?/gi,'')
  .replace(/(min-|max-)?height:\s*[\d.]+px;?/gi,'')
  .replace(/font-size:\s*[\d.]+px;?/gi,'')
  .replace(/line-height:\s*[\d.]+px;?/gi,'');

async function probe(engine, name, html, width, editable) {
  const b = await engine.launch();
  const p = await b.newPage();
  await p.goto('http://localhost:8988/blank.html');
  await p.setContent(`<body style="margin:0;font-family:Helvetica">
    <div ${editable?'contenteditable="true"':''} style="width:${width}px;border:1px solid red">${html}</div></body>`);
  await p.waitForTimeout(300);
  const r = await p.evaluate(() => {
    const t = document.querySelector('table');
    const tds = [...t.querySelectorAll(':scope>tbody>tr>td')];
    const img = document.querySelector('img');
    const ir = img.getBoundingClientRect();
    const last = tds[tds.length-1].getBoundingClientRect();
    return { cells: tds.length, imgW: Math.round(ir.width),
             tableW: Math.round(t.getBoundingClientRect().width),
             logoLeftOfText: ir.right <= last.left + 2,
             imgBottom: Math.round(ir.bottom), textTop: Math.round(last.top) };
  });
  await b.close();
  console.log(`${name.padEnd(34)} cells=${r.cells} table=${r.tableW}px img=${r.imgW}px  sideBySide=${r.logoLeftOfText}`);
  return r;
}

import { createServer } from 'http';
const srv = createServer((q,r)=>{ r.writeHead(200,{'Content-Type':'text/html'}); r.end('<html></html>'); });
await new Promise(r=>srv.listen(8988,r));

for (const [eng, label] of [[chromium,'chromium'], [webkit,'webkit  ']]) {
  console.log(`\n== ${label} ==`);
  await probe(eng, ' full markup @ 600px', sig, 600, false);
  await probe(eng, ' full markup @ 260px', sig, 260, false);
  await probe(eng, ' stripped   @ 600px', strip(sig), 600, false);
  await probe(eng, ' stripped   @ 260px', strip(sig), 260, false);
  await probe(eng, ' stripped   @ 260px editable', strip(sig), 260, true);
  await probe(eng, ' stripped   @ 200px editable', strip(sig), 200, true);
}
srv.close();
