// Custom SVG diagram verifier: proves arrows connect to box edges, don't
// cross a box interior, and don't overlap. Run after writing any custom SVG.
//
// Usage:
//   node verify.mjs <path-or-file://-url> [executablePath]
//
//   node verify.mjs ~/.../diagram.html
//   node verify.mjs file:///path/diagram.html /path/to/chrome-headless-shell
//
// Needs `playwright` installed in the cwd (npm i playwright) and a Chromium
// binary. See the browser location note in visual-explainer/SKILL.md.

// Resolve playwright from the cwd (where you ran the script), not from this
// file's dir, so the script works from any project that has playwright installed.
import { createRequire } from 'module';
const require = createRequire(process.cwd() + '/');
const { chromium } = require('playwright');
import { pathToFileURL } from 'url';
import { resolve } from 'path';

const target = process.argv[2];
const exe = process.argv[3];
if (!target) { console.error('Usage: node verify.mjs <path-or-url> [executablePath]'); process.exit(1); }

const url = target.startsWith('file://') || target.startsWith('http') ? target : pathToFileURL(resolve(target)).href;
const browser = await chromium.launch(exe ? { executablePath: exe } : {});
const page = await browser.newPage({ viewport: { width: 1280, height: 1100 } });
const pageErrors = [];
page.on('pageerror', e => pageErrors.push(e.message));
await page.goto(url, { waitUntil: 'networkidle' });
await page.waitForTimeout(500);

const res = await page.evaluate(() => {
  const svg = document.querySelector('.svg-wrap svg, .wrap svg, svg');
  if (!svg) throw new Error('No svg found');

  const boxes = [...svg.querySelectorAll('rect[class^="sv-box"]')].map(r => ({
    x: +r.getAttribute('x'), y: +r.getAttribute('y'),
    w: +r.getAttribute('width'), h: +r.getAttribute('height'), id: r.getAttribute('class')
  }));
  // group/container rects (no class) also count as valid arrow targets
  const containers = [...svg.querySelectorAll('rect')].filter(r => !r.getAttribute('class'))
    .map(r => ({ x: +r.getAttribute('x'), y: +r.getAttribute('y'), w: +r.getAttribute('width'), h: +r.getAttribute('height') }));
  const targets = boxes.concat(containers);

  const segs = p => {
    const m = p.match(/-?\d+(\.\d+)?/g).map(Number); const out = [];
    let px = m[0], py = m[1];
    for (let i = 2; i < m.length; i += 2) { out.push([px, py, m[i], m[i + 1]]); px = m[i]; py = m[i + 1]; }
    return out;
  };
  const arrows = [...svg.querySelectorAll('path[marker-end]')].map((p, i) => ({ id: i, segs: segs(p.getAttribute('d')) }));

  const nearEdge = (x, y) => targets.some(b => {
    const onX = Math.abs(x - b.x) < 3 || Math.abs(x - (b.x + b.w)) < 3, inY = y >= b.y - 3 && y <= b.y + b.h + 3;
    const onY = Math.abs(y - b.y) < 3 || Math.abs(y - (b.y + b.h)) < 3, inX = x >= b.x - 3 && x <= b.x + b.w + 3;
    return (onX && inY) || (onY && inX);
  });
  // A segment clips a box if it enters and exits it (corner clips included).
  // Sample finely along the segment rather than a single midpoint so a line
  // that nicks a corner is caught.
  const segInBox = s => boxes.some(b => {
    const steps = 50;
    for (let i = 1; i < steps; i++) {
      const t = i / steps;
      const px = s[0] + (s[2] - s[0]) * t, py = s[1] + (s[3] - s[1]) * t;
      if (px > b.x + 1 && px < b.x + b.w - 1 && py > b.y + 1 && py < b.y + b.h - 1) return true;
    }
    return false;
  });
  const intersect = (a, b) => {
    const [ax, ay, bx, by] = a, [cx, cy, dx, dy] = b;
    const d = (bx - ax) * (dy - cy) - (by - ay) * (dx - cx);
    if (d === 0) return null;
    const t = ((cx - ax) * (dy - cy) - (cy - ay) * (dx - cx)) / d;
    const u = ((cx - ax) * (by - ay) - (cy - ay) * (bx - ax)) / d;
    if (!(t > 0.001 && t < 0.999 && u > 0.001 && u < 0.999)) return null;
    return [ax + (bx - ax) * t, ay + (by - ay) * t];
  };

  // Overlaps only count as failures when they happen in open space. Arrows
  // legitimately converge on a shared box edge (many arrows into one box), so
  // an intersection within EDGE_TOL of a box border is expected, not a bug.
  const EDGE_TOL = 8;
  const nearAnyEdge = (px, py) => targets.some(b => {
    const onX = Math.abs(px - b.x) < EDGE_TOL || Math.abs(px - (b.x + b.w)) < EDGE_TOL;
    const onY = Math.abs(py - b.y) < EDGE_TOL || Math.abs(py - (b.y + b.h)) < EDGE_TOL;
    return onX || onY;
  });

  const disconnected = [], throughBox = [], overlapping = [];
  for (const a of arrows) {
    const last = a.segs[a.segs.length - 1];
    const ex = last[2], ey = last[3];
    if (!nearEdge(ex, ey)) disconnected.push({ arrow: a.id, end: [ex, ey] });
    for (const s of a.segs) if (segInBox(s)) throughBox.push({ arrow: a.id, seg: s });
  }
  for (let i = 0; i < arrows.length; i++) for (let j = i + 1; j < arrows.length; j++)
    for (const s of arrows[i].segs) for (const t of arrows[j].segs) {
      const p = intersect(s, t);
      if (p && !nearAnyEdge(p[0], p[1])) overlapping.push({ a: i, b: j });
    }

  // Text must not sit on an arrow line: any .sv-arrow-lbl bbox that an arrow
  // segment passes through is a failure.
  const segInRect = (s, r) => {
    for (let i = 1; i < 40; i++) {
      const t = i / 40, px = s[0] + (s[2] - s[0]) * t, py = s[1] + (s[3] - s[1]) * t;
      if (px > r.x + 1 && px < r.x + r.w - 1 && py > r.y + 1 && py < r.y + r.h - 1) return true;
    }
    return false;
  };
  // Text must clear boxes. A label may sit on its own line only if it has a
  // pill knockout behind it (that's the designed read — the pill hides the line).
  const pills = [...svg.querySelectorAll('.sv-pill')].map(p => { const b = p.getBBox(); return { x: b.x, y: b.y, w: b.width, h: b.height }; });
  const labelHasPill = l => pills.some(p => l.x + l.w / 2 > p.x && l.x + l.w / 2 < p.x + p.w && l.y + l.h / 2 > p.y && l.y + l.h / 2 < p.y + p.h);
  const labelHit = [];
  const labels = [...svg.querySelectorAll('.sv-arrow-lbl')].map(t => { const b = t.getBBox(); return { x: b.x, y: b.y, w: b.width, h: b.height }; });
  for (const l of labels) {
    let hit = false;
    for (const a of arrows) for (const s of a.segs) if (segInRect(s, l) && !labelHasPill(l)) { hit = true; break; }
    if (!hit) for (const b of boxes) if (!(l.x + l.w < b.x || l.x > b.x + b.w || l.y + l.h < b.y || l.y > b.y + b.h)) { hit = true; break; }
    if (hit) labelHit.push({ x: Math.round(l.x), y: Math.round(l.y) });
  }


  // ---- 4 legibility self-checks ----
  const MIN_TITLE = 16, MIN_SUB = 13;
  const boxesAll = [...svg.querySelectorAll('rect[class^="sv-box"]')].map(r => ({ x:+r.getAttribute('x'), y:+r.getAttribute('y'), w:+r.getAttribute('width'), h:+r.getAttribute('height') }));
  const textEls = [...svg.querySelectorAll('.sv-title, .sv-sub')];
  const textOverflow = [];
  for (const t of textEls) {
    const bb = t.getBBox(); const cx = bb.x + bb.width / 2, cy = bb.y + bb.height / 2;
    const box = boxesAll.find(b => cx > b.x && cx < b.x + b.w && cy > b.y && cy < b.y + b.h);
    if (box && (bb.x < box.x + 1 || bb.x + bb.width > box.x + box.w - 1 || bb.y < box.y + 1 || bb.y + bb.height > box.y + box.h - 1)) {
      textOverflow.push(t.textContent.trim());
    }
  }
  const lblEls = [...svg.querySelectorAll('.sv-arrow-lbl')];
  const lblBoxes = lblEls.map(t => { const b = t.getBBox(); return { el: t, x: b.x, y: b.y, w: b.width, h: b.height }; });
  const labelIssues = [];
  for (let i = 0; i < lblBoxes.length; i++) {
    const L = lblBoxes[i];
    const overBox = boxesAll.some(b => !(L.x + L.w <= b.x + 2 || L.x >= b.x + b.w - 2 || L.y + L.h <= b.y + 2 || L.y >= b.y + b.h - 2));
    if (overBox) labelIssues.push(L.el.textContent.trim() + ' (on a box)');
    for (let j = i + 1; j < lblBoxes.length; j++) {
      const M = lblBoxes[j];
      if (!(L.x + L.w <= M.x || L.x >= M.x + M.w || L.y + L.h <= M.y || L.y >= M.y + M.h)) labelIssues.push(L.el.textContent.trim() + ' ~ ' + M.el.textContent.trim());
    }
  }
  const groupRects = [...svg.querySelectorAll('rect')].filter(r => !r.getAttribute('class') && (r.getAttribute('style') || '').includes('surface2'));
  const groupOverflow = [];
  for (const t of [...svg.querySelectorAll('.sv-grp, .sv-grp--sub, .sv-grp--inner')]) {
    const bb = t.getBBox();
    const g = groupRects.find(gr => bb.x >= +gr.getAttribute('x') && bb.x < +gr.getAttribute('x') + +gr.getAttribute('width'));
    if (g && bb.x + bb.width > +g.getAttribute('x') + +g.getAttribute('width')) groupOverflow.push(t.textContent.trim());
  }
  const smallType = [];
  for (const t of textEls) { const fs = parseFloat(getComputedStyle(t).fontSize); const min = t.classList.contains('sv-title') ? MIN_TITLE : MIN_SUB; if (fs < min) smallType.push(t.textContent.trim() + ' (' + fs + 'px)'); }
  const legibility = { textOverflow, labelIssues, groupOverflow, smallType };

  return {
    arrows: arrows.length,
    disconnected,
    throughBox,
    overlapping,
    labelOnArrow: labelHit,
    legibility,
    overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth
  };
});

await browser.close();

console.log(JSON.stringify(res, null, 2));
console.log('page errors:', pageErrors.length ? pageErrors : 'none');
console.log('legibility: textOverflow=' + (res.legibility?.textOverflow?.length||0) + ' labelIssues=' + (res.legibility?.labelIssues?.length||0) + ' groupOverflow=' + (res.legibility?.groupOverflow?.length||0) + ' smallType=' + (res.legibility?.smallType?.length||0));

const fail = (res.disconnected.length || res.throughBox.length || res.overlapping.length || res.labelOnArrow.length || res.overflow !== 0 || pageErrors.length || (res.legibility && (res.legibility.textOverflow.length || res.legibility.labelIssues.length || res.legibility.groupOverflow.length || res.legibility.smallType.length)));
if (fail) { console.error('\nFAIL: clean up the issues above.'); process.exit(1); }
console.log('\nPASS: arrows connect to edges, none cross a box, none overlap, no text on an arrow.');
