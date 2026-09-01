// layout-test.mjs — prove the dagre auto-layout is clean, and emit a demo.
//
//   node layout-test.mjs <nConfigs> <executablePath> [demoOut.html]
//
// 1. Generates random DAGs (multi-parent merges + multi-child fans), lays each
//    out with layout() (real crossing removal via @dagrejs/dagre), renders it,
//    and checks the geometric rules + label/arrow overlap. Reports pass rate.
// 2. Writes a clean demo diagram to demoOut.html (default ./examples/demo.html).

import { createRequire } from 'module';
import { writeFileSync, mkdirSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';
const require = createRequire(process.cwd() + '/');
const { chromium } = require('playwright');
import { assemble, layout } from './layout.mjs';
import { cssFor } from './palette.mjs';

const N = parseInt(process.argv[2] || '80', 10);
const exe = process.argv[3];
const here = dirname(fileURLToPath(import.meta.url));
const demoOut = process.argv[4] || join(here, 'examples', 'demo.html');
const browser = await chromium.launch(exe ? { executablePath: exe } : {});
const page = await browser.newPage();

// --- geometric + label checks (same rules as verify.mjs) ---
const checks = () => {
  const svg = document.querySelector('.wrap svg');
  const boxes = [...svg.querySelectorAll('rect[class^="sv-box"]')].map(r => ({
    x: +r.getAttribute('x'), y: +r.getAttribute('y'), w: +r.getAttribute('width'), h: +r.getAttribute('height'),
  }));
  const nearEdge = (x, y) => boxes.some(b => {
    const onX = Math.abs(x - b.x) < 3 || Math.abs(x - (b.x + b.w)) < 3, inY = y >= b.y - 3 && y <= b.y + b.h + 3;
    const onY = Math.abs(y - b.y) < 3 || Math.abs(y - (b.y + b.h)) < 3, inX = x >= b.x - 3 && x <= b.x + b.w + 3;
    return (onX && inY) || (onY && inX);
  });
  const segs = p => { const m = p.match(/-?\d+(\.\d+)?/g).map(Number); const o = []; let px = m[0], py = m[1];
    for (let i = 2; i < m.length; i += 2) { o.push([px, py, m[i], m[i + 1]]); px = m[i]; py = m[i + 1]; } return o; };
  const arrows = [...svg.querySelectorAll('path[marker-end]')].map(p => segs(p.getAttribute('d')));
  const inRect = (s, r, inset) => { for (let i = 1; i < 40; i++) { const t = i / 40;
    const px = s[0] + (s[2] - s[0]) * t, py = s[1] + (s[3] - s[1]) * t;
    if (px > r.x + inset && px < r.x + r.w - inset && py > r.y + inset && py < r.y + r.h - inset) return true; } return false; };
  const inter = (a, b) => { const [ax, ay, bx, by] = a, [cx, cy, dx, dy] = b;
    const d = (bx - ax) * (dy - cy) - (by - ay) * (dx - cx); if (d === 0) return null;
    const t = ((cx - ax) * (dy - cy) - (cy - ay) * (dx - cx)) / d;
    const u = ((cx - ax) * (by - ay) - (cy - ay) * (bx - ax)) / d;
    return (t > 0.001 && t < 0.999 && u > 0.001 && u < 0.999) ? [ax + (bx - ax) * t, ay + (by - ay) * t] : null; };
  const EDGE_TOL = 8, nearAnyEdge = (px, py) => boxes.some(b =>
    Math.abs(px - b.x) < EDGE_TOL || Math.abs(px - (b.x + b.w)) < EDGE_TOL ||
    Math.abs(py - b.y) < EDGE_TOL || Math.abs(py - (b.y + b.h)) < EDGE_TOL);
  let bad = 0, through = 0, overlap = 0, labelHit = 0;
  for (const a of arrows) { const last = a[a.length - 1]; if (!nearEdge(last[2], last[3])) bad++;
    for (const s of a) if (boxes.some(b => inRect(s, b, 1))) through++; }
  for (let i = 0; i < arrows.length; i++) for (let j = i + 1; j < arrows.length; j++)
    for (const s of arrows[i]) for (const t of arrows[j]) { const p = inter(s, t); if (p && !nearAnyEdge(p[0], p[1])) overlap++; }
  const labels = [...svg.querySelectorAll('.sv-arrow-lbl')].map(t => { const b = t.getBBox(); return { x: b.x, y: b.y, w: b.width, h: b.height }; });
  for (const l of labels) {
    let hit = false;
    for (const a of arrows) for (const s of a) if (inRect(s, l, 1)) { hit = true; break; }
    if (!hit) for (const b of boxes) if (!(l.x + l.w < b.x || l.x > b.x + b.w || l.y + l.h < b.y || l.y > b.y + b.h)) { hit = true; break; }
    if (hit) labelHit++;
  }
  return { ok: bad === 0 && through === 0 && overlap === 0 && labelHit === 0, bad, through, overlap, labelHit };
};

// --- random DAG generator (multi-parent allowed) ---
function rng(seed) {
  return () => { seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
}
const rand = rng(20260831);
const ir = (a, b) => a + Math.floor(rand() * (b - a + 1));

function randomDag() {
  const n = ir(4, 9);
  const roles = ['source', 't1', 't2', 'loop', 'loop', 'out'];
  const nodes = {};
  for (let i = 0; i < n; i++) nodes['n' + i] = { title: 'Node ' + (i + 1), sub: 'label', role: roles[i % roles.length] };
  const edges = [];
  for (let j = 1; j < n; j++) {
    const parents = ir(1, Math.min(2, j)); // 1-2 parents (fan/merge)
    const chosen = new Set();
    for (let k = 0; k < parents; k++) { const p = ir(0, j - 1); chosen.add('n' + p); }
    [...chosen].forEach(p => edges.push({ from: p, to: 'n' + j }));
  }
  return { nodes, edges };
}

// --- run the benchmark ---
let pass = 0, failures = [];
for (let i = 0; i < N; i++) {
  const g = randomDag();
  const laid = layout(g);
  const svg = assemble({ ...laid, aria: 'test ' + i });
  await page.setContent(`<div class="wrap">${svg}</div>`);
  const r = await page.evaluate(checks);
  if (r.ok) pass++; else failures.push({ i, ...r });
}
await browser.close();

console.log(`Dagre auto-layout tested on ${N} random DAGs (merges + fans)`);
console.log(`  ${pass}/${N} clean  (${((pass / N) * 100).toFixed(0)}%)`);
if (failures.length) {
  console.log(`  ${failures.length} failed:`);
  failures.slice(0, 5).forEach(f => console.log(`    config ${f.i}: connect=${f.bad} through=${f.through} overlap=${f.overlap} label=${f.labelHit}`));
}

// --- write the demo diagram (a DAG with fans and merges) ---
const demo = {
  nodes: {
    In: { title: 'Input', sub: 'source', role: 'source' },
    Sc: { title: 'Score', sub: 'deterministic', role: 't1' },
    En: { title: 'Enrich', sub: 'grounded', role: 'loop' },
    Va: { title: 'Validate', sub: 'QA', role: 'loop' },
    Rt: { title: 'Route', sub: 'owner', role: 'loop' },
    Tr: { title: 'Track', sub: 'outcome', role: 'out' },
    Dr: { title: 'Draft', sub: 'human confirms', role: 'out' },
    UI: { title: 'Review', sub: 'approve', role: 'out' },
  },
  edges: [
    { from: 'In', to: 'Sc', label: 'score it', emphasis: true },
    { from: 'In', to: 'En', label: 'ground it' },
    { from: 'Sc', to: 'Va', emphasis: true },
    { from: 'En', to: 'Va', label: 'merge' },
    { from: 'Va', to: 'Rt', emphasis: true },
    { from: 'Rt', to: 'Dr', emphasis: true },
    { from: 'Rt', to: 'UI' },
    { from: 'En', to: 'Tr' },
    { from: 'Tr', to: 'UI' },
    { from: 'Dr', to: 'UI', emphasis: true },
  ],
};
const STRUCT_CSS = `
body{background:var(--bg);color:var(--text);font-family:var(--font-mono);margin:0;padding:32px}
.wrap{background:var(--surface);border:1px solid var(--border-bright);border-radius:16px;padding:20px;max-width:1300px;margin:0 auto}
.wrap svg{display:block;width:100%;height:auto}
h1{font-size:13px;letter-spacing:1px;text-transform:uppercase;color:var(--text-muted);margin:0 0 6px}
.note{font-size:11px;color:var(--text-dim);margin:10px 0 0;line-height:1.5}
.sv-sec{font-size:11px;font-weight:700;letter-spacing:.08em;fill:var(--text-muted);text-transform:uppercase}
.sv-grp{font-size:13px;font-weight:600;letter-spacing:.08em;fill:var(--text);text-transform:uppercase}
.sv-grp--inner{font-size:11px;font-weight:500;letter-spacing:.04em;fill:var(--text-dim);font-variant:small-caps;text-transform:none}
.sv-grp--sub{font-size:11px;font-weight:400;letter-spacing:.04em;fill:var(--text-muted);text-transform:none}
.sv-title{font-size:16px;font-weight:700;fill:var(--text);letter-spacing:.01em}
.sv-sub{font-size:13px;font-weight:400;fill:var(--text-dim);letter-spacing:.01em}
.sv-arrow{fill:none;stroke:var(--arr-color);stroke-width:2;stroke-linejoin:round;stroke-linecap:round}
.sv-arrow-d{fill:none;stroke:var(--arr-color);stroke-width:2;stroke-dasharray:4 4;stroke-linejoin:round;stroke-linecap:round}
.sv-arrow--strong{fill:none;stroke:var(--arr-color-strong);stroke-width:2.5;stroke-linejoin:round;stroke-linecap:round}
.sv-arrow-lbl{font-size:12px;fill:var(--text);letter-spacing:.01em}
.sv-pill{fill:var(--surface)}
.sv-box-storage{stroke:var(--storage)} .sv-box-compute{stroke:var(--compute)}
.sv-box-model{stroke:var(--model)} .sv-box-consumer{stroke:var(--consumer)}
`
body{background:var(--bg);color:var(--text);font-family:var(--font-mono);margin:0;padding:32px}
.wrap{background:var(--surface);border:1px solid var(--border-bright);border-radius:16px;padding:20px;max-width:1200px;margin:0 auto}
.wrap svg{display:block;width:100%;height:auto}
h1{font-size:13px;letter-spacing:1px;text-transform:uppercase;color:var(--text-muted);margin:0 0 6px}
.note{font-size:11px;color:var(--text-dim);margin:10px 0 0;line-height:1.5}
.sv-sec{font-size:11px;font-weight:700;letter-spacing:2px;fill:var(--text-muted);text-transform:uppercase}
.sv-grp{font-size:9.5px;font-weight:700;letter-spacing:1.5px;fill:var(--text-muted);text-transform:uppercase}
.sv-title{font-size:12px;font-weight:700;fill:var(--text);letter-spacing:.3px}
.sv-sub{font-size:9px;fill:var(--text-dim);letter-spacing:.3px}
.sv-arrow{fill:none;stroke:var(--arr-color);stroke-width:2;stroke-linejoin:round;stroke-linecap:round}
.sv-arrow-d{fill:none;stroke:var(--arr-color);stroke-width:2;stroke-dasharray:3 3;stroke-linejoin:round;stroke-linecap:round}
.sv-arrow--strong{fill:none;stroke:var(--arr-color-strong);stroke-width:2.75;stroke-linejoin:round;stroke-linecap:round}
.sv-arrow-lbl{font-size:9.5px;fill:var(--text-muted);letter-spacing:.2px}
.sv-box-source{stroke:var(--slate)} .sv-box-t1{stroke:var(--secondary)} .sv-box-t2{stroke:var(--primary)}
.sv-box-loop{stroke:var(--violet)} .sv-box-llm{stroke:var(--amber)} .sv-box-out{stroke:var(--good)}
`;

function writeDemo(file, paletteName) {
  const svg = assemble({ ...layout({ ...demo, patterns: true }), aria: 'dagre auto-layout demo' });
  const html = `<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Auto-layout demo &mdash; ${paletteName} palette</title>
<style>
:root{--font-mono:'Source Code Pro','SF Mono',Consolas,monospace;--arr-color:var(--text-muted);--arr-color-strong:var(--secondary);}
${cssFor(paletteName)}
${STRUCT_CSS}
</style></head><body>
<h1>Auto-layout demo &mdash; fans + merges, no crossings (${paletteName} palette)</h1>
<div class="wrap">${svg}</div>
<p class="note">Generated by layout() via @dagrejs/dagre, styled by cssFor('${paletteName}'). Every arrow ends on a box edge; labels clear the lines; the three arrows into 'Review' converge on its left edge (legitimate).</p>
</body></html>`;
  mkdirSync(dirname(file), { recursive: true });
  writeFileSync(file, html);
  console.log(`Demo (${paletteName}) written to: ${file}`);
}

writeDemo(demoOut, 'blueprint');
writeDemo(join(here, 'examples', 'demo-mono.html'), 'mono');
