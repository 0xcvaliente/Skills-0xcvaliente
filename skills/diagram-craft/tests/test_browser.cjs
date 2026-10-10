/* Integration regressions for the optional browser helper. Needs Playwright/Chromium. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const {spawnSync} = require('node:child_process');
const root = path.resolve(__dirname,'..');
const tmp = fs.mkdtempSync(path.join(os.tmpdir(),'diagram-craft-test-'));
const browserArgs = process.env.DIAGRAM_CRAFT_BROWSER ? ['--browser-executable',process.env.DIAGRAM_CRAFT_BROWSER] : [];
function run(name,html,png=false) {
  const file=path.join(tmp,`${name}.html`), dir=path.join(tmp,name);
  fs.writeFileSync(file,html);
  const pngPath=path.join(tmp,`${name}.png`);
  const result=spawnSync(process.execPath,[path.join(root,'scripts/inspect_diagram.cjs'),file,'--out-dir',dir,...(png?['--png',pngPath]:[]),...browserArgs],{encoding:'utf8'});
  if (!fs.existsSync(path.join(dir,'report.json'))) throw new Error(result.stderr||result.stdout||'No browser report produced');
  return {status:result.status,report:JSON.parse(fs.readFileSync(path.join(dir,'report.json'),'utf8')),pngPath};
}
try {
  const healthy=fs.readFileSync(path.join(root,'assets/architecture.html'),'utf8');
  let result=run('healthy',healthy);
  assert.equal(result.status,0,JSON.stringify(result.report));
  assert.equal(result.report.ok,true);
  result=run('overflow',healthy.replace('>Web client<','>'+'UnbrokenLongLabel'.repeat(20)+'<'));
  assert.equal(result.status,1);
  assert(result.report.desktop.findings.some(x=>x.includes('Text escapes node')));
  result=run('missing-name',healthy.replace(/aria-labelledby="[^"]+"/,'aria-labelledby="missing"'));
  assert.equal(result.status,1);
  assert(result.report.desktop.findings.some(x=>x.includes('accessible name')));
  result=run('low-contrast',healthy.replace(/fill="#172b36"/g,'fill="#ffffff"'));
  assert.equal(result.status,1);
  assert(result.report.desktop.findings.some(x=>x.includes('Contrast')));
  const translated=`<!doctype html><html><head><style>body{margin:0}svg{display:block;width:100%;max-width:800px}text{font:20px sans-serif;fill:#172b36}</style></head><body>
  <svg aria-hidden="true" viewBox="0 0 16 16"><path d="M0 0L16 16"/></svg>
  <svg role="img" aria-labelledby="diagram-title" viewBox="0 0 800 400">
  <title id="diagram-title">API to database</title><desc>An API calls a database.</desc><rect width="800" height="400" fill="#ffffff"/>
  <g transform="translate(100 50)"><g data-node="api" data-x="0" data-y="0" data-w="160" data-h="80"><rect width="160" height="80" fill="#ffffff"/><text data-node-text="api" x="20" y="45">API</text></g></g>
  <g transform="translate(400 50)"><g data-node="db" data-x="0" data-y="0" data-w="160" data-h="80"><rect width="160" height="80" fill="#ffffff"/><text data-node-text="db" x="20" y="45">Database</text></g></g>
  <polyline data-edge="request" transform="translate(100 50)" points="160,40 300,40" fill="none" stroke="#172b36"/>
  <g data-label="request-label" transform="translate(290 120)" data-x="0" data-y="0" data-w="120" data-h="40"><rect width="120" height="40" fill="#ffffff"/><text x="8" y="26">Request</text></g>
  </svg></body></html>`;
  result=run('translated-with-icon',translated,true);
  assert.equal(result.status,0,JSON.stringify(result.report));
  assert.equal(result.report.desktop.svgIndex,1);
  assert.equal(result.report.desktop.measuredNodes,2);
  assert.equal(result.report.desktop.measuredRoutes,1);
  assert.equal(result.report.desktop.measuredText,3);
  assert.equal(fs.readFileSync(result.pngPath).readUInt32BE(16),800,'PNG must capture the diagram rather than the icon');
  result=run('translated-obstruction',translated.replace('transform="translate(100 50)" points=','transform="translate(0 50)" points='));
  assert.equal(result.status,1);
  assert(result.report.desktop.findings.some(x=>x.includes('passes through node api')));
  result=run('translated-overflow',translated.replace('translate(400 50)','translate(750 50)'));
  assert.equal(result.status,1);
  assert(result.report.desktop.findings.some(x=>x.includes('Off-canvas node: db')));
  result=run('unsupported-transform',translated.replace('translate(400 50)','translate(400 50) scale(1.5)'));
  assert(result.report.desktop.warnings.some(x=>x.includes('unsupported or unavailable transform')));
  assert.equal(result.report.desktop.measuredNodes,1);
  result=run('decorative-only','<!doctype html><svg aria-hidden="true" viewBox="0 0 16 16"></svg>');
  assert.equal(result.status,1);
  assert(result.report.desktop.findings.some(x=>x.includes('No meaningful root SVG')));
  process.stdout.write('Browser integration checks passed: 9 cases, including translated geometry, decorative SVG selection and PNG export.\n');
} finally {fs.rmSync(tmp,{recursive:true,force:true});}
