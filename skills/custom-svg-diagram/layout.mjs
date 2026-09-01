// layout.mjs — build diagrams from data, not hand-coordinated paths.
//
// Emits the SVG body (or a full <svg>) from a declarative spec using the
// skill's CSS classes (sv-box-*, sv-arrow, sv-title, ...) so the output
// themes with the page and passes verify.mjs.
//
//   import { assemble } from './layout.mjs';
//   const svg = assemble({
//     width: 1280, height: 1080,
//     headers: [{ x:40, y:34, text:'Storage' }, ...],
//     groups:   [{ x:40, y:480, w:580, h:310, label:'Tier 2 · Snowflake' }, ...],
//     boxes:    [{ x:70, y:545, w:190, h:110, role:'t2', title:'account', sub:'one row' }, ...],
//     arrows:   [{ d:'M 430 590 L 260 595', label:'fan out', labelX:300, labelY:575 }, ...],
//   });
//
// `assemble` returns the full <svg> string; `assembleBody` returns just the
// inner content (for embedding inside a hand-authored <svg> tag).

export const ROLE_CLASS = {
  source: 'sv-box-source', t1: 'sv-box-t1', t2: 'sv-box-t2',
  loop: 'sv-box-loop', llm: 'sv-box-llm', out: 'sv-box-out',
};
export const ROLE_COLOR = {
  source: 'var(--slate)', t1: 'var(--secondary)', t2: 'var(--primary)',
  loop: 'var(--violet)', llm: 'var(--amber)', out: 'var(--good)',
};
// Face-gradient stops per role (theme-aware via the CSS color var).
export const GRADIENT = {
  source: { color: 'slate', top: 0.08, bottom: 0.20 },
  t1: { color: 'secondary', top: 0.08, bottom: 0.20 },
  t2: { color: 'primary', top: 0.08, bottom: 0.20 },
  loop: { color: 'violet', top: 0.08, bottom: 0.20 },
  llm: { color: 'amber', top: 0.10, bottom: 0.24 },
  out: { color: 'good', top: 0.10, bottom: 0.24 },
};
export const ROLE_VAR = { source: 'slate', t1: 'secondary', t2: 'primary', loop: 'violet', llm: 'amber', out: 'good' };

// Box "looks" — the shape/fill/shadow of a box, independent of its color role.
//   shadow:  'shadow' (3D button) | 'shadowSoft' | 'glow' (per-role) | 'none'
//   fill:    'gradient' | 'flat' (dim) | 'outline'
//   gloss:   adds the top sheen + edge line
export const STYLES = {
  button:  { rx: 14, shadow: 'shadow',     fill: 'gradient', gloss: true,  border: 2 },
  flat:    { rx: 10, shadow: 'none',       fill: 'flat',     gloss: false, border: 1.5 },
  outline: { rx: 8,  shadow: 'none',       fill: 'outline',  gloss: false, border: 2.5 },
  soft:    { rx: 18, shadow: 'shadowSoft', fill: 'gradient', gloss: true,  border: 1.5 },
  glow:    { rx: 12, shadow: 'glow',       fill: 'flat',     gloss: false, border: 2 },
};
export const DEFAULT_STYLE = 'button';

// Arrow "looks" — thickness presets. Color is set by the CSS vars --arr-color
// (standard) and --arr-color-strong (emphasis), so arrow color is a CSS swap
// like box color, not a diagram-code change.
export const ARROW_STYLES = {
  standard: { width: 2 },
  bold:     { width: 2.75 },
  hairline: { width: 1.25 },
};
export const DEFAULT_ARROW_STYLE = 'standard';

export function defs() {
  return [
    '<defs>',
    // Arrow markers — fill via CSS vars so arrow color is a CSS swap, matching
    // the line stroke (--arr-color for standard, --arr-color-strong for emphasis).
    '  <marker id="arr" viewBox="0 0 10 10" refX="9.5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">',
    '    <path d="M 0 0 L 10 5 L 0 10 z" style="fill:var(--arr-color)"></path>',
    '  </marker>',
    '  <marker id="arrStrong" viewBox="0 0 10 10" refX="9.5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">',
    '    <path d="M 0 0 L 10 5 L 0 10 z" style="fill:var(--arr-color-strong)"></path>',
    '  </marker>',
    // Top sheen — a light highlight that reads as a glass gloss in both themes.
    '  <linearGradient id="sheen" x1="0" y1="0" x2="0" y2="1">',
    '    <stop offset="0%" stop-color="#ffffff" stop-opacity="0.32"></stop>',
    '    <stop offset="52%" stop-color="#ffffff" stop-opacity="0.06"></stop>',
    '    <stop offset="100%" stop-color="#ffffff" stop-opacity="0"></stop>',
    '  </linearGradient>',
    // 3D button shadow: contact + hard underside + soft ambient.
    '  <filter id="shadow" x="-30%" y="-40%" width="160%" height="200%">',
    '    <feDropShadow dx="0" dy="1" stdDeviation="1.2" flood-color="#16213a" flood-opacity="0.10"></feDropShadow>',
    '    <feDropShadow dx="0" dy="3.5" stdDeviation="0" flood-color="#16213a" flood-opacity="0.22"></feDropShadow>',
    '    <feDropShadow dx="0" dy="10" stdDeviation="18" flood-color="#16213a" flood-opacity="0.14"></feDropShadow>',
    '  </filter>',
    // Soft shadow (contact + ambient, no hard underside) for the 'soft' look.
    '  <filter id="shadowSoft" x="-30%" y="-30%" width="160%" height="180%">',
    '    <feDropShadow dx="0" dy="1" stdDeviation="1.4" flood-color="#16213a" flood-opacity="0.10"></feDropShadow>',
    '    <feDropShadow dx="0" dy="8" stdDeviation="16" flood-color="#16213a" flood-opacity="0.14"></feDropShadow>',
    '  </filter>',
    // Per-role glow filters (a subtle colored outer aura) for the 'glow' look.
    ...Object.entries(ROLE_VAR).map(([role, v]) => (
      `  <filter id="glow${v}" x="-60%" y="-60%" width="220%" height="220%"><feDropShadow dx="0" dy="0" stdDeviation="5" flood-color="var(--${v})" flood-opacity="0.22"></feDropShadow></filter>`
    )),
    // Subtle role patterns — redundant encoding so color is never the only signal.
    '  <pattern id="pat0" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="6" stroke="var(--text)" stroke-opacity="0.05" stroke-width="2"></line></pattern>',
    '  <pattern id="pat1" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(-45)"><line x1="0" y1="0" x2="0" y2="8" stroke="var(--text)" stroke-opacity="0.05" stroke-width="2"></line></pattern>',
    '  <pattern id="pat2" width="6" height="6" patternUnits="userSpaceOnUse"><circle cx="3" cy="3" r="1" fill="var(--text)" fill-opacity="0.06"></circle></pattern>',
    '  <pattern id="pat3" width="8" height="8" patternUnits="userSpaceOnUse"><path d="M0 8 L8 0 M-4 4 L4 -4 M4 12 L12 4" stroke="var(--text)" stroke-opacity="0.05" stroke-width="1.5"></path></pattern>',
    // Per-role face gradients: a subtle lighter-top → deeper-bottom so the box
    // reads with rounded volume (like a button face), theme-aware via CSS vars.
    ...Object.entries(GRADIENT).map(([name, grad]) => (
      `  <linearGradient id="g${name}" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="var(--${grad.color})" stop-opacity="${grad.top}"></stop><stop offset="100%" stop-color="var(--${grad.color})" stop-opacity="${grad.bottom}"></stop></linearGradient>`
    )),
    '</defs>',
  ].join('\n');
}

// A role-colored box with title + subtitle. `title` may be an array (two lines).
export function box({ x, y, w, h, role = 'source', title, sub, pattern, style = DEFAULT_STYLE }) {
  const cls = ROLE_CLASS[role] || ROLE_CLASS.source;
  const col = ROLE_COLOR[role] || ROLE_COLOR.source;
  const rv = ROLE_VAR[role] || 'slate';
  const S = STYLES[style] || STYLES[DEFAULT_STYLE];
  const titles = Array.isArray(title) ? title : [title];
  const shadowId = S.shadow === 'glow' ? `glow${rv[0].toUpperCase()}${rv.slice(1)}` : S.shadow;
  const open = shadowId ? `<g filter="url(#${shadowId})">` : '<g>';
  const g = [open];
  let fill = `style="fill:url(#g${role})"`;
  if (S.fill === 'flat') fill = `style="fill:var(--${rv}-dim)"`;
  else if (S.fill === 'outline') fill = `style="fill:var(--surface)"`;
  g.push(`  <rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${S.rx}" class="${cls}" ${fill} stroke-width="${S.border}"></rect>`);
  // Redundant encoding: a subtle per-role pattern so color is never the only signal.
  if (pattern) g.push(`  <rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${S.rx}" fill="url(#${pattern})"></rect>`);
  // Glass gloss on the top half + a faint light line along the top edge (button/soft).
  if (S.gloss) {
    g.push(`  <rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${S.rx}" fill="url(#sheen)"></rect>`);
    g.push(`  <line x1="${x + 4}" y1="${y + 1.5}" x2="${x + w - 4}" y2="${y + 1.5}" stroke="#ffffff" stroke-opacity="0.28" stroke-width="1.5" stroke-linecap="round"></line>`);
  }
  titles.forEach((t, i) => {
    g.push(`  <text class="sv-title" x="${x + 22}" y="${y + 42 + i * 18}" style="fill:${col}">${t}</text>`);
  });
  if (sub) g.push(`  <text class="sv-sub" x="${x + 22}" y="${y + 42 + titles.length * 18 - 2}">${sub}</text>`);
  g.push('</g>');
  return g.join('\n');
}

// An arrow (line path with marker) and optional label. dashed = dotted line;
// emphasis = the primary-flow highlight (uses --arr-color-strong); arrowStyle =
// a thickness preset. Color is set by the CSS vars --arr-color / --arr-color-strong.
export function arrow({ d, label, labelX, labelY, dashed = false, emphasis = false, arrowStyle = DEFAULT_ARROW_STYLE }) {
  const AS = ARROW_STYLES[arrowStyle] || ARROW_STYLES[DEFAULT_ARROW_STYLE];
  const cls = dashed ? 'sv-arrow-d' : (emphasis ? 'sv-arrow--strong' : 'sv-arrow');
  const mark = emphasis && !dashed ? 'url(#arrStrong)' : 'url(#arr)';
  const g = [`<path class="${cls}" d="${d}" marker-end="${mark}" stroke-width="${AS.width}"></path>`];
  if (label != null) g.push(`<text class="sv-arrow-lbl" x="${labelX}" y="${labelY}">${label}</text>`);
  return g.join('\n');
}

// A dashed group container with a mono label.
export function group({ x, y, w, h, label }) {
  return [
    `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="18" style="fill:var(--surface2);stroke:var(--border-bright);stroke-dasharray:6 6"></rect>`,
    `<text class="sv-grp" x="${x + 18}" y="${y + 24}">${label}</text>`,
  ].join('\n');
}

// A column title.
export function header({ x, y = 34, text }) {
  return `<text class="sv-sec" x="${x}" y="${y}">${text}</text>`;
}

export function assembleBody(spec) {
  const out = [];
  out.push(defs());
  (spec.headers || []).forEach(h => out.push(header(h)));
  (spec.groups || []).forEach(g => out.push(group(g)));
  (spec.boxes || []).forEach(b => out.push(box(b)));
  (spec.arrows || []).forEach(a => out.push(arrow(a)));
  return out.join('\n');
}

export function assemble(spec) {
  return [
    `<svg viewBox="0 0 ${spec.width} ${spec.height}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="${spec.aria || 'architecture diagram'}">`,
    assembleBody(spec),
    '</svg>',
  ].join('\n');
}

// ---------------------------------------------------------------------------
// layout() — auto-layout a graph with real crossing removal (via @dagrejs/dagre).
//
//   layout({
//     nodes:  { id: { title, sub?, role? }, ... },
//     edges:  [ { from, to, label?, dashed? }, ... ],
//     nodeW, nodeH, options?            // dagre graph options (rankdir, ranks, …)
//   })
//
// Dagre layers the nodes, minimizes edge crossings, and routes the edges. We
// clip each routed path to the node borders so arrowheads land on box edges,
// and we place each label above the edge's longest horizontal run so text
// clears the line. Returns { width, height, boxes, arrows } for assemble().
//
// Handles multi-parent merges and multi-child fans — the cases the v0.3
// hand-rolled router could not.

import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const dagre = require('@dagrejs/dagre');

const clipStart = (p0, p1, r) => {
  const dx = p1.x - p0.x, dy = p1.y - p0.y;
  if (dx > 0) return { x: r.x + r.w, y: p0.y };
  if (dx < 0) return { x: r.x, y: p0.y };
  if (dy > 0) return { x: p0.x, y: r.y + r.h };
  return { x: p0.x, y: r.y };
};
const clipEnd = (p0, p1, r) => {
  const dx = p1.x - p0.x, dy = p1.y - p0.y;
  if (dx > 0) return { x: r.x, y: p1.y };
  if (dx < 0) return { x: r.x + r.w, y: p1.y };
  if (dy > 0) return { x: p1.x, y: r.y };
  return { x: p1.x, y: r.y + r.h };
};
const bestLabelPos = pts => {
  let best = null, bestLen = -1;
  for (let i = 1; i < pts.length; i++) {
    if (pts[i].y === pts[i - 1].y) {
      const len = Math.abs(pts[i].x - pts[i - 1].x);
      if (len > bestLen) { bestLen = len; best = [pts[i - 1], pts[i]]; }
    }
  }
  if (best) { const [a, b] = best; return { x: (a.x + b.x) / 2, y: Math.min(a.y, b.y) - 8 }; }
  const m = pts[Math.floor(pts.length / 2)];
  return { x: m.x, y: m.y - 8 };
};
const pointsOf = d => { const m = d.match(/-?\d+(\.\d+)?/g).map(Number); const o = []; for (let i = 0; i < m.length; i += 2) o.push({ x: m[i], y: m[i + 1] }); return o; };
const segmentsOf = d => { const m = d.match(/-?\d+(\.\d+)?/g).map(Number); const o = []; for (let i = 0; i + 3 < m.length; i += 2) o.push([m[i], m[i + 1], m[i + 2], m[i + 3]]); return o; };
const segInRect = (s, r) => { for (let i = 1; i < 40; i++) { const t = i / 40, px = s[0] + (s[2] - s[0]) * t, py = s[1] + (s[3] - s[1]) * t;
  if (px > r.x + 1 && px < r.x + r.w - 1 && py > r.y + 1 && py < r.y + r.h - 1) return true; } return false; };
// Nudge a label up until its bbox clears every box and every arrow segment.
const avoidLabel = (label, cand, boxes, segs) => {
  const w = label.length * 6.5 + 10, h = 16;
  let x = cand.x, y = cand.y;
  const clear = () => {
    const b = { x: x - w / 2, y: y - 12, w, h };
    for (const r of boxes) if (!(b.x + b.w < r.x || b.x > r.x + r.w || b.y + b.h < r.y || b.y > r.y + r.h)) return false;
    for (const s of segs) if (segInRect(s, b)) return false;
    return true;
  };
  for (let i = 0; i < 10; i++) { if (clear()) return { x, y }; y -= 16; }
  return { x, y };
};
// Round each 90° corner of an orthogonal route with a quadratic bezier. The
// curve stays on the inside of the corner (within the orthogonal corridor), so
// it reads as premium without adding overlap risk.
const smoothPath = (pts, r = 12) => {
  if (pts.length < 3) return 'M ' + pts.map(p => `${p.x} ${p.y}`).join(' L ');
  let d = `M ${pts[0].x} ${pts[0].y}`;
  for (let i = 1; i < pts.length - 1; i++) {
    const p0 = pts[i - 1], p1 = pts[i], p2 = pts[i + 1];
    const l1 = Math.hypot(p1.x - p0.x, p1.y - p0.y);
    const l2 = Math.hypot(p2.x - p1.x, p2.y - p1.y);
    const rr = Math.min(r, l1 / 2, l2 / 2);
    const ax = p1.x - ((p1.x - p0.x) / l1) * rr, ay = p1.y - ((p1.y - p0.y) / l1) * rr;
    const bx = p1.x + ((p2.x - p1.x) / l2) * rr, by = p1.y + ((p2.y - p1.y) / l2) * rr;
    d += ` L ${ax} ${ay} Q ${p1.x} ${p1.y} ${bx} ${by}`;
  }
  d += ` L ${pts[pts.length - 1].x} ${pts[pts.length - 1].y}`;
  return d;
};

export function layout(spec) {
  const { nodes, edges, nodeW = 150, nodeH = 92, curved = true, patterns = false, boxStyle = DEFAULT_STYLE, arrowStyle = DEFAULT_ARROW_STYLE, options = {} } = spec;
  const g = new dagre.graphlib.Graph();
  g.setGraph({
    rankdir: 'LR', nodesep: 56, ranksep: 120,
    marginx: 40, marginy: 40, ...options,
  });
  g.setDefaultEdgeLabel(() => ({}));
  Object.keys(nodes).forEach(id => g.setNode(id, { width: nodeW, height: nodeH }));
  edges.forEach(e => g.setEdge(e.from, e.to, { label: e.label, dashed: e.dashed }));
  dagre.layout(g);

  const rects = {};
  const rolePattern = { source: 'pat0', t1: 'pat1', t2: 'pat2', loop: 'pat3', llm: 'pat0', out: 'pat1' };
  const boxes = Object.keys(nodes).map(id => {
    const p = g.node(id);
    const role = nodes[id].role || 'loop';
    rects[id] = { x: p.x - nodeW / 2, y: p.y - nodeH / 2, w: nodeW, h: nodeH };
    return { x: rects[id].x, y: rects[id].y, w: nodeW, h: nodeH, role, title: nodes[id].title, sub: nodes[id].sub, pattern: patterns ? rolePattern[role] : undefined, style: boxStyle };
  });

  const arrows = edges.map(e => {
    const pts = (g.edge(e.from, e.to)?.points || []).map(p => ({ x: p.x, y: p.y }));
    if (pts.length < 2) return null;
    pts[0] = clipStart(pts[0], pts[1], rects[e.from]);
    pts[pts.length - 1] = clipEnd(pts[pts.length - 2], pts[pts.length - 1], rects[e.to]);
    const d = curved ? smoothPath(pts) : pts.map((p, i) => `${i === 0 ? 'M' : 'L'} ${p.x} ${p.y}`).join(' ');
    return { d, e };
  }).filter(Boolean);

  // Labels are placed last so they can avoid both boxes and every arrow line.
  const allSegs = arrows.flatMap(a => segmentsOf(a.d));
  arrows.forEach(a => {
    const e = a.e;
    if (e.label == null) return;
    const pos = avoidLabel(e.label, bestLabelPos(pointsOf(a.d)), boxes, allSegs);
    a.label = e.label; a.labelX = pos.x; a.labelY = pos.y;
  });
  arrows.forEach(a => { a.dashed = a.e.dashed; a.emphasis = a.e.emphasis; a.arrowStyle = arrowStyle; });

  const gb = g.graph();
  return { width: gb.width + 40, height: gb.height + 40, boxes, arrows };
}
