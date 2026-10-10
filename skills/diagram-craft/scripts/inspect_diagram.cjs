#!/usr/bin/env node
/* Optional Playwright checks for a local diagram. Never installs dependencies. */
const fs = require('node:fs/promises');
const path = require('node:path');
const {pathToFileURL} = require('node:url');

function argumentsFor(argv) {
  const result = {file: argv[0], outDir: 'checks', scale: 1};
  if (!result.file || result.file.startsWith('--')) throw new Error('Usage: inspect_diagram.cjs file.html [--out-dir checks] [--png figure.png] [--pdf companion.pdf] [--scale 2]');
  const keys = {'--out-dir':'outDir', '--png':'png', '--pdf':'pdf', '--scale':'scale', '--browser-executable':'browserExecutable'};
  for (let i=1; i<argv.length; i+=2) {
    if (!keys[argv[i]] || !argv[i+1] || argv[i+1].startsWith('--')) throw new Error(`Invalid option: ${argv[i]}`);
    result[keys[argv[i]]] = argv[i+1];
  }
  result.scale = Number(result.scale);
  if (!Number.isFinite(result.scale) || result.scale<1 || result.scale>4) throw new Error('scale must be between 1 and 4');
  return result;
}

async function inspect(page) {
  return page.evaluate(() => {
    const findings = [], warnings = [];
    const allSVGs = [...document.querySelectorAll('svg')];
    const diagrams = allSVGs.filter(el=>!el.parentElement?.closest('svg')&&!el.closest('[aria-hidden="true"]'));
    const svg = diagrams[0];
    if (!svg) return {findings:['No meaningful root SVG found'], warnings, measuredText:0};
    if (diagrams.length>1) warnings.push('Only the first meaningful root SVG was checked; review the remaining diagrams');
    const inDiagram = selector => [...svg.querySelectorAll(selector)].filter(el=>el.closest('svg')===svg);
    const vb = svg.viewBox.baseVal;
    if (!(vb.width>0 && vb.height>0)) findings.push('SVG needs a positive viewBox');
    const nameIds = (svg.getAttribute('aria-labelledby') || '').trim().split(/\s+/).filter(Boolean);
    if (svg.getAttribute('role') !== 'img' || nameIds.length===0 || nameIds.some(id=>!document.getElementById(id)?.textContent.trim())) findings.push('SVG accessible name does not resolve');
    if (!svg.querySelector('title')?.textContent.trim() || !svg.querySelector('desc')?.textContent.trim()) findings.push('SVG needs a nonempty title and description');
    const ids = new Set();
    for (const el of document.querySelectorAll('[id]')) {
      if (ids.has(el.id)) findings.push(`Duplicate ID: ${el.id}`);
      ids.add(el.id);
    }
    // Normalize supported translations into the selected root's viewBox frame.
    // Scaling, rotation, skew and nested viewports need a separate visual review.
    const frames = new WeakMap(), rootMatrix = svg.getCTM();
    const frameOf = el => {
      if (frames.has(el)) return frames.get(el);
      const localMatrix = el.getCTM();
      const matrix = rootMatrix&&localMatrix ? rootMatrix.inverse().multiply(localMatrix) : null;
      const frame = matrix&&Math.abs(matrix.a-1)<.00001&&Math.abs(matrix.d-1)<.00001&&Math.abs(matrix.b)<.00001&&Math.abs(matrix.c)<.00001 ? {x:matrix.e,y:matrix.f} : null;
      if (!frame) warnings.push(`Geometry not measured for unsupported or unavailable transform: ${el.dataset.node||el.dataset.label||el.dataset.edge||el.textContent}`);
      frames.set(el,frame);
      return frame;
    };
    const rectOf = el => {
      const frame=frameOf(el), r={x:Number(el.dataset.x),y:Number(el.dataset.y),width:Number(el.dataset.w),height:Number(el.dataset.h)};
      if (!frame) return null;
      if (!Object.values(r).every(Number.isFinite)||r.width<=0||r.height<=0) {
        warnings.push(`Invalid geometry annotations: ${el.dataset.node||el.dataset.label}`);return null;
      }
      return {...r,x:r.x+frame.x,y:r.y+frame.y};
    };
    const contains = (a,b,pad=0) => b.x>=a.x+pad-1 && b.y>=a.y+pad-1 && b.x+b.width<=a.x+a.width-pad+1 && b.y+b.height<=a.y+a.height-pad+1;
    const rgb = color => {
      if (/^#[0-9a-f]{6}$/i.test(color)) return [1,3,5].map(i=>parseInt(color.slice(i,i+2),16)/255);
      const match = color.match(/^rgba?\(([^)]+)\)$/);
      if (!match) return null;
      const values = match[1].split(/[,\s]+/).filter(Boolean).map(Number);
      if (values.length>3 && values[3]!==1) return null;
      return values.slice(0,3).map(x=>x/255);
    };
    const luminance = values => values.map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4).reduce((s,v,i)=>s+v*[.2126,.7152,.0722][i],0);
    const checkContrast = (fg,bg,label,min) => {
      const a=rgb(fg), b=rgb(bg);
      if (!a || !b || a.length!==3 || b.length!==3) {warnings.push(`Contrast not measured: ${label}`);return;}
      const ls=[luminance(a),luminance(b)].sort((x,y)=>x-y), ratio=(ls[1]+.05)/(ls[0]+.05);
      if (ratio<min) findings.push(`Contrast ${label}: ${ratio.toFixed(2)}:1 below ${min}:1`);
    };
    const nodeMap=new Map(inDiagram('[data-node]').map(el=>[el.dataset.node,el]));
    const nodeRects=new Map([...nodeMap].map(([id,el])=>[id,rectOf(el)]).filter(([,r])=>r));
    const canvas={x:vb.x,y:vb.y,width:vb.width,height:vb.height};
    for (const [id,r] of nodeRects) if (!contains(canvas,r)) findings.push(`Off-canvas node: ${id}`);
    let measuredRoutes=0;
    for (const edge of inDiagram('polyline[data-edge]')) {
      const frame=frameOf(edge);
      if (!frame) continue;
      const points=Array.from({length:edge.points.numberOfItems},(_,i)=>{const p=edge.points.getItem(i);return {x:p.x+frame.x,y:p.y+frame.y};});
      if (points.some(p=>!contains(canvas,{x:p.x,y:p.y,width:0,height:0}))) findings.push(`Off-canvas route: ${edge.dataset.edge}`);
      if (points.some((p,i)=>i>0&&Math.abs(p.x-points[i-1].x)>.001&&Math.abs(p.y-points[i-1].y)>.001)) {
        warnings.push(`Diagonal route requires manual review: ${edge.dataset.edge}`);continue;
      }
      measuredRoutes++;
      for (const [id,r] of nodeRects) {
        const inset=.001;
        const hits=points.some((p,i)=> {
          if (!i) return false;
          const a=points[i-1];
          if (Math.abs(p.y-a.y)<.001) return p.y>r.y+inset&&p.y<r.y+r.height-inset&&Math.max(a.x,p.x)>r.x+inset&&Math.min(a.x,p.x)<r.x+r.width-inset;
          return p.x>r.x+inset&&p.x<r.x+r.width-inset&&Math.max(a.y,p.y)>r.y+inset&&Math.min(a.y,p.y)<r.y+r.height-inset;
        });
        if (hits) findings.push(`Route ${edge.dataset.edge} passes through node ${id}`);
      }
    }
    let measuredText=0;
    for (const text of inDiagram('text')) {
      const frame=frameOf(text);
      if (!frame) continue;
      const localBox=text.getBBox(), box={x:localBox.x+frame.x,y:localBox.y+frame.y,width:localBox.width,height:localBox.height}; measuredText++;
      if (!contains({x:vb.x,y:vb.y,width:vb.width,height:vb.height},box)) findings.push(`Off-canvas text: ${text.textContent}`);
      const node=nodeMap.get(text.dataset.nodeText);
      const label=text.closest('[data-label]');
      const nodeRect=node&&nodeRects.get(text.dataset.nodeText), labelRect=label&&rectOf(label);
      if (nodeRect && !contains(nodeRect,box,8)) findings.push(`Text escapes node ${text.dataset.nodeText}: ${text.textContent}`);
      if (labelRect && !contains(labelRect,box,3)) findings.push(`Text escapes label ${label.dataset.label}: ${text.textContent}`);
      const shape=(node||label)?.querySelector('rect,polygon');
      if (shape) checkContrast(getComputedStyle(text).fill,getComputedStyle(shape).fill,`text ${text.textContent}`,4.5);
    }
    const bg=svg.querySelector(':scope > rect');
    if (bg) for (const edge of inDiagram('[data-edge]')) checkContrast(getComputedStyle(edge).stroke,getComputedStyle(bg).fill,`edge ${edge.dataset.edge}`,3);
    if (document.documentElement.scrollWidth>window.innerWidth+1) findings.push('Whole-page horizontal overflow');
    if (!nodeMap.size) warnings.push('No geometry annotations: node containment was not checked');
    const external=[...document.querySelectorAll('[src],[href]')].map(e=>e.getAttribute('src')||e.getAttribute('href')).filter(v=>/^https?:/i.test(v));
    if (external.length) warnings.push(`External dependencies: ${external.join(', ')}`);
    return {findings:[...new Set(findings)],warnings:[...new Set(warnings)],measuredText,measuredRoutes,nodes:nodeMap.size,measuredNodes:nodeRects.size,svgIndex:allSVGs.indexOf(svg),viewBox:{width:vb.width,height:vb.height}};
  });
}

async function main() {
  const args=argumentsFor(process.argv.slice(2));
  let chromium;
  try { ({chromium}=require('playwright')); }
  catch { throw new Error('Playwright is unavailable. Use a project installation, the host bundled NODE_PATH, or another browser tool.'); }
  const input=path.resolve(args.file);
  await fs.access(input);
  await fs.mkdir(args.outDir,{recursive:true});
  const browser=await chromium.launch({headless:true,...(args.browserExecutable?{executablePath:path.resolve(args.browserExecutable)}:{})});
  try {
    const page=await browser.newPage({viewport:{width:1440,height:960},deviceScaleFactor:args.scale});
    const errors=[], requests=[];
    page.on('pageerror',error=>errors.push(error.message));
    page.on('requestfailed',request=>requests.push(request.url()));
    await page.goto(pathToFileURL(input).href,{waitUntil:'load'});
    await page.evaluate(()=>document.fonts.ready);
    const desktop=await inspect(page);
    await page.screenshot({path:path.join(args.outDir,'desktop.png'),fullPage:true});
    if (args.png) {
      // Widen the wrapper before capture so a locally scrolled SVG is not cropped.
      const width=Math.ceil(desktop.viewBox?.width||1440);
      await page.setViewportSize({width:Math.max(1440,width+96),height:960});
      await page.addStyleTag({content:'main{max-width:none}.canvas{overflow:visible}.canvas svg{width:auto}'});
      if (!Number.isInteger(desktop.svgIndex)) throw new Error('PNG export needs a meaningful root SVG');
      await page.locator('svg').nth(desktop.svgIndex).screenshot({path:args.png});
      await page.reload({waitUntil:'load'});
      await page.evaluate(()=>document.fonts.ready);
    }
    if (args.pdf) await page.pdf({path:args.pdf,format:'A4',landscape:true,printBackground:true,margin:{top:'12mm',bottom:'12mm',left:'12mm',right:'12mm'}});
    await page.setViewportSize({width:390,height:844});
    const mobile=await inspect(page);
    await page.screenshot({path:path.join(args.outDir,'mobile.png'),fullPage:true});
    const report={file:path.basename(input),ok:desktop.findings.length===0&&mobile.findings.length===0&&errors.length===0&&requests.length===0,desktop,mobile,errors,failedRequests:requests,
      limits:['Only the first meaningful root SVG checked','Geometry supports translation only; nested SVG content is excluded','No semantic/source validation','No complete connector or occlusion audit','No full accessibility audit','Export previews require separate review']};
    await fs.writeFile(path.join(args.outDir,'report.json'),JSON.stringify(report,null,2)+'\n');
    process.stdout.write(JSON.stringify(report,null,2)+'\n');
    if (!report.ok) process.exitCode=1;
  } finally {await browser.close();}
}

main().catch(error=>{process.stderr.write(`error: ${error.message}\n`);process.exitCode=1;});
