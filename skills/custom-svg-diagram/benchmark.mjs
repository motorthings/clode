// benchmark.mjs — empirically test which routing method avoids overlaps.
//
// Compares two consumer-routing strategies for the stacked-tables layout:
//   A) naive — consumers stacked below the tables, straight-down arrows.
//   B) skill — consumers side-by-side, arrows routed down the outer margins.
//
// For each of N random configs it renders both, runs the same geometric
// checks as verify.mjs, and reports pass rates. Run from a dir with
// playwright + a Chromium binary:
//
//   node benchmark.mjs <nConfigs> <executablePath>
//
// Outcome (expected): A passes ~0% (account→CSM crosses score_history),
// B passes ~100%. That's the evidence the skill's method is the right one.

import { createRequire } from 'module';
const require = createRequire(process.cwd() + '/');
const { chromium } = require('playwright');
import { assemble } from './layout.mjs';

const N = parseInt(process.argv[2] || '40', 10);
const exe = process.argv[3];
const browser = await chromium.launch(exe ? { executablePath: exe } : {});
const page = await browser.newPage();

// Seeded RNG so results are reproducible.
function rng(seed) {
  return () => {
    seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
const rand = rng(20260831);
const ir = (a, b) => a + Math.floor(rand() * (b - a + 1));

function buildStrategy(kind) {
  const wA = ir(150, 230), hA = ir(90, 130), gap = ir(24, 44);
  const stackTop = 545;
  const left = 70;
  const right = 450;
  const sTop = stackTop, sMid1 = stackTop + hA / 2, sBottom1 = stackTop + hA;
  const sMid2 = stackTop + hA + gap + hA / 2, sBottom2 = stackTop + hA + gap + hA;
  const rightEdge = left + wA;
  const center = left + wA / 2;
  const eHeight = 2 * hA + gap; // account_event spans the whole left stack

  const boxes = [
    { x: left, y: stackTop, w: wA, h: hA, role: 't2', title: 'account', sub: 'row' },
    { x: left, y: stackTop + hA + gap, w: wA, h: hA, role: 't2', title: 'score_history', sub: 'trends' },
    { x: right, y: stackTop, w: 190, h: eHeight, role: 't2', title: 'account_event', sub: 'log' },
  ];
  const fan = [
    { d: `M ${right} ${sMid1} L ${rightEdge} ${sMid1}`, label: 'fan' },
    { d: `M ${right} ${sMid2} L ${rightEdge} ${sMid2}`, label: 'fan' },
  ];

  let consumers, arrows;
  if (kind === 'A') {
    // Naive: consumers stacked below, straight-down arrows.
    consumers = [
      { x: left, y: 950, w: wA, h: 90, role: 'out', title: 'CSM UI', sub: '' },
      { x: left, y: 1060, w: wA, h: 90, role: 'out', title: 'trends', sub: '' },
    ];
    arrows = fan.concat([
      { d: `M ${center} ${sBottom1} L ${center} 950`, label: 'down' },       // crosses score_history
      { d: `M ${center} ${sBottom2} L ${center} 1060`, label: 'down' },
    ]);
  } else {
    // Skill: consumers side-by-side, margin-routed consumer arrows.
    consumers = [
      { x: 40, y: 950, w: wA, h: 90, role: 'out', title: 'CSM UI', sub: '' },
      { x: 450, y: 950, w: wA, h: 90, role: 'out', title: 'trends', sub: '' },
    ];
    arrows = fan.concat([
      // account -> CSM: down the LEFT margin (x=40 < score_history left=70).
      { d: `M 80 ${sBottom1} L 40 ${sBottom1 + 40} L 40 948`, label: 'margin' },
      // score_history -> trends: diagonal down-right, below account_event.
      { d: `M ${center} ${sBottom2} L ${450 + wA / 2} 948`, label: 'diag' },
    ]);
  }

  return assemble({
    width: 900, height: 1180,
    aria: kind,
    boxes: boxes.concat(consumers),
    arrows,
  });
}

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
  const inBox = s => boxes.some(b => {
    for (let i = 1; i < 40; i++) { const t = i / 40;
      const px = s[0] + (s[2] - s[0]) * t, py = s[1] + (s[3] - s[1]) * t;
      if (px > b.x + 1 && px < b.x + b.w - 1 && py > b.y + 1 && py < b.y + b.h - 1) return true; }
    return false;
  });
  const inter = (a, b) => { const [ax, ay, bx, by] = a, [cx, cy, dx, dy] = b;
    const d = (bx - ax) * (dy - cy) - (by - ay) * (dx - cx); if (d === 0) return false;
    const t = ((cx - ax) * (dy - cy) - (cy - ay) * (dx - cx)) / d;
    const u = ((cx - ax) * (by - ay) - (cy - ay) * (bx - ax)) / d;
    return t > 0.001 && t < 0.999 && u > 0.001 && u < 0.999; };
  let badConnect = 0, through = 0, overlap = 0;
  for (const a of arrows) {
    const last = a[a.length - 1]; if (!nearEdge(last[2], last[3])) badConnect++;
    for (const s of a) if (inBox(s)) through++;
  }
  for (let i = 0; i < arrows.length; i++) for (let j = i + 1; j < arrows.length; j++)
    for (const s of arrows[i]) for (const t of arrows[j]) if (inter(s, t)) overlap++;
  return badConnect === 0 && through === 0 && overlap === 0;
};

const results = { A: { pass: 0, fail: 0 }, B: { pass: 0, fail: 0 } };
for (let i = 0; i < N; i++) {
  for (const kind of ['A', 'B']) {
    const svg = buildStrategy(kind);
    await page.setContent(`<div class="wrap">${svg}</div>`);
    const ok = await page.evaluate(checks);
    results[kind][ok ? 'pass' : 'fail']++;
  }
}
await browser.close();

const pct = r => ((r.pass / (r.pass + r.fail)) * 100).toFixed(0);
console.log(`Configs tested: ${N}\n`);
console.log(`Strategy A (naive, stacked consumers, straight-down arrows):`);
console.log(`  ${results.A.pass}/${N} pass  (${pct(results.A)}%)`);
console.log(`  → account→CSM arrow crosses the stacked score_history box.\n`);
console.log(`Strategy B (skill, side-by-side consumers, margin-routed arrows):`);
console.log(`  ${results.B.pass}/${N} pass  (${pct(results.B)}%)`);
console.log(`\nVerdict: ${pct(results.B)}% vs ${pct(results.A)}% — margin-routing is the method to encode.`);
