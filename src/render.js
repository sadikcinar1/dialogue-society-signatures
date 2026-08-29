#!/usr/bin/env node
/* Render a signature from src/template.js.
 *
 * The build calls this instead of driving a browser: template.js is plain
 * ES5 with module.exports, so Node can run it directly and the whole build
 * stays dependency-free. Playwright is only used by the test suite.
 *
 *   node src/render.js '{"lead":"org","branch":"Birmingham", ...}'
 *
 * The logo is passed in as a data URI by the caller.
 */
const DS = require('./template.js');

const raw = process.argv[2];
if (!raw) {
  console.error('usage: node src/render.js \'{"lead":"person","name":"...", ...}\'');
  process.exit(1);
}

let data;
try {
  data = JSON.parse(raw);
} catch (e) {
  console.error('render.js: argument is not valid JSON -', e.message);
  process.exit(1);
}

process.stdout.write(DS.build(data));
