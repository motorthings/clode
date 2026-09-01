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

export const ROLES = ['storage', 'compute', 'model', 'consumer'];
const ROLE_MAP = { storage: 'storage', compute: 'compute', model: 'model', consumer: 'consumer',
  source: 'storage', t1: 'storage', t2: 'storage', loop: 'compute', llm: 'model', out: 'consumer' };
export const ROLE_CLASS = { storage: 'sv-box-storage', compute: 'sv-box-compute', model: 'sv-box-model', consumer: 'sv-box-consumer' };
export const ROLE_COLOR = { storage: 'var(--storage)', compute: 'var(--compute)', model: 'var(--model)', consumer: 'var(--consumer)' };
export const ROLE_VAR = { storage: 'storage', compute: 'compute', model: 'model', consumer: 'consumer' };
export const canonical = role => ROLE_MAP[role] || 'storage';

// Flat box styles only — no gradient, no hatch, no gloss. Color lives in the
// border and the label. `fill` is the flat tint opacity over the surface.
export const STYLES = {
  clean:  { rx: 8,  fill: 0.06, border: 1.5 },
  soft:   { rx: 10, fill: 0.03, border: 1 },
  outline:{ rx: 6,  fill: 0,    border: 1.5 },
};
export const DEFAULT_STYLE = 'clean';

export const ARROW_STYLES = {
  standard: { width: 2 },
  bold:     { width: 2.5 },
  hairline: { width: 1.25 },
};
export const DEFAULT_ARROW_STYLE = 'standard';

const estWidth = (s, px) => s.length * px * 0.62;
const wrap = (s, max) => { if (!s) return []; const words = s.split(' '); const lines = []; let cur = '';
  for (const wd of words) { const nxt = (cur + ' ' + wd).trim(); if (nxt.length > max) { if (cur) lines.push(cur.trim()); cur = wd; } else cur = nxt; }
  if (cur) lines.push(cur.trim()); return lines; };


export function defs() {
  return [
    '<defs>',
    // Flat design needs only the arrow markers. Fill via CSS vars so arrow
    // color is a CSS swap matching the line stroke.
    '  <marker id="arr" viewBox="0 0 10 10" refX="9.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" style="fill:var(--arr-color)"></path></marker>',
    '  <marker id="arrStrong" viewBox="0 0 10 10" refX="9.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" style="fill:var(--arr-color-strong)"></path></marker>',
    '</defs>',
  ].join('\n');
}

// A category-colored box, auto-sized from measured content, text centered.
// Flat tint only (no gradient, no hatch, no gloss). Color lives in the border
// and the title. `title` may be an array; `sub` wraps at ~24 chars (2 lines max).
export function box({ x, y, w, h, role, title, sub, style = DEFAULT_STYLE, minW = 150 }) {
  const rv = ROLE_VAR[canonical(role)];
  const cls = ROLE_CLASS[canonical(role)];
  const col = ROLE_COLOR[canonical(role)];
  const S = STYLES[style] || STYLES[DEFAULT_STYLE];
  const TITLE_PX = 16, SUB_PX = 13, PAD = 16;
  const titles = (Array.isArray(title) ? title : [title]).slice(0, 2);
  const subs = wrap(sub, 24).slice(0, 2);
  const titleW = Math.max(...titles.map(t => estWidth(t, TITLE_PX)));
  const subW = Math.max(...subs.map(s => estWidth(s, SUB_PX)));
  const bw = w || Math.max(minW, titleW, subW) + PAD * 2;
  const textH = titles.length * (TITLE_PX + 6) + subs.length * (SUB_PX + 4);
  const bh = h || PAD * 2 + textH;
  const cx = x + bw / 2;
  let ty = y + (bh - textH) / 2 + TITLE_PX / 2;
  const g = [
    `<rect x="${x}" y="${y}" width="${bw}" height="${bh}" rx="${S.rx}" class="${cls}" style="fill:${col};fill-opacity:${S.fill}" stroke-width="${S.border}"></rect>`,
  ];
  titles.forEach(t => { g.push(`<text class="sv-title" x="${cx}" y="${ty}" text-anchor="middle" style="fill:${col}">${t}</text>`); ty += TITLE_PX + 6; });
  subs.forEach(s => { g.push(`<text class="sv-sub" x="${cx}" y="${ty}" text-anchor="middle">${s}</text>`); ty += SUB_PX + 4; });
  return g.join('\n');
}

// An arrow with an optional label. The label renders in a pill filled with the
// page background so the line never runs through the text.
export function arrow({ d, label, labelX, labelY, dashed = false, emphasis = false, arrowStyle = DEFAULT_ARROW_STYLE }) {
  const AS = ARROW_STYLES[arrowStyle] || ARROW_STYLES[DEFAULT_ARROW_STYLE];
  const cls = dashed ? 'sv-arrow-d' : (emphasis ? 'sv-arrow--strong' : 'sv-arrow');
  const mark = emphasis && !dashed ? 'url(#arrStrong)' : 'url(#arr)';
  const out = [`<path class="${cls}" d="${d}" marker-end="${mark}" stroke-width="${AS.width}"></path>`];
  if (label != null) {
    const w = estWidth(label, 12) + 20, h = 18;
    const px = labelX - w / 2, py = labelY - h + 4;
    out.push(`<rect class="sv-pill" x="${px}" y="${py}" width="${w}" height="${h}" rx="9"></rect>`);
    out.push(`<text class="sv-arrow-lbl" x="${labelX}" y="${labelY}" text-anchor="middle">${label}</text>`);
  }
  return out.join('\n');
}

// A group container. Outer = solid border + filled label chip; inner = dashed
// 1px border + plain small-caps label, one step smaller/lighter. `title` is a
// short noun phrase (<=3 words); `sub` is an optional qualifier on a second line.
// Top padding band inside every group = label height + 16px — no node may sit
// above group.y + 36.
export function group({ x, y, w, h, title, sub, level = 'outer' }) {
  const inner = level === 'inner';
  const borderStyle = inner
    ? 'fill:var(--surface2);stroke:var(--border-bright);stroke-dasharray:5 5'
    : 'fill:var(--surface2);stroke:var(--text-muted)';
  const border = inner ? 1 : 1.5;
  const chipY = y + 10;
  const out = [`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="12" style="${borderStyle}" stroke-width="${border}"></rect>`];
  if (inner) {
    out.push(`<text class="sv-grp sv-grp--inner" x="${x + 16}" y="${chipY + 16}">${title}</text>`);
  } else {
    const chipW = estWidth(title, 13) + 24;
    out.push(`<rect x="${x + 12}" y="${chipY}" width="${chipW}" height="26" rx="7" style="fill:var(--surface)"></rect>`);
    out.push(`<text class="sv-grp" x="${x + 12 + chipW / 2}" y="${chipY + 17}" text-anchor="middle">${title}</text>`);
    if (sub) out.push(`<text class="sv-grp sv-grp--sub" x="${x + 24 + chipW}" y="${chipY + 17}">${sub}</text>`);
  }
  return out.join('\n');
}

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
  const { nodes, edges, nodeW = 150, nodeH = 92, curved = true, boxStyle = DEFAULT_STYLE, arrowStyle = DEFAULT_ARROW_STYLE, options = {} } = spec;
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
  const boxes = Object.keys(nodes).map(id => {
    const p = g.node(id);
    const role = nodes[id].role || 'loop';
    rects[id] = { x: p.x - nodeW / 2, y: p.y - nodeH / 2, w: nodeW, h: nodeH };
    return { x: rects[id].x, y: rects[id].y, w: nodeW, h: nodeH, role, title: nodes[id].title, sub: nodes[id].sub, style: boxStyle };
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
