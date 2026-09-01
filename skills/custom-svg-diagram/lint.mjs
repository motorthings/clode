// lint.mjs — readability gate for a diagram graph spec.
//
//   node lint.mjs <graph.json>      where graph.json = { nodes, edges, groups? }
//
// Encodes the diagram-design rules from the research (readability, not just
// geometry): a readable diagram is tree-like and flow-oriented. Prints a
// warning per violation. Exits 0 if clean, 1 if any rule is hit, so you can
// wire it into a gate or keep it advisory.
//
// Rules (thresholds from the research):
//   - Edge count should sit near N-1..N+2 for N nodes. More = dependency graph,
//     not a data-flow diagram.
//   - Edge labels ≤ 4 words (long labels force layers apart / reroute).
//   - Hub fan-out ≤ 5 (split nodes with 6+ children).
//   - Merge depth ≤ 4 (4+ sources into one node = a diamond to avoid).
//   - Groups ≤ 3 per diagram.
//   - Any layer with 6+ nodes makes the diagram vertically sprawling.

import { readFileSync } from 'fs';

const spec = JSON.parse(readFileSync(process.argv[2], 'utf8'));
const nodes = spec.nodes || {};
const edges = spec.edges || [];
const N = Object.keys(nodes).length;
const E = edges.length;

const out = [];
const flag = (msg) => out.push(msg);

// Edge-to-node ratio (tree-like: N-1..N+2).
if (N > 0) {
  const lo = Math.max(0, N - 1), hi = N + 2;
  if (E < lo) flag(`sparse: ${E} edges for ${N} nodes (expect ~${lo}–${hi}) — likely disconnected`);
  if (E > hi) flag(`dense: ${E} edges for ${N} nodes (expect ≤ ${hi}) — reads as a dependency graph, not data flow`);
}

// Label length.
for (const e of edges) {
  if (e.label && e.label.trim().split(/\s+/).length > 4) {
    flag(`long label (${e.label.trim().split(/\s+/).length} words): "${e.label}" — keep ≤ 4 words`);
  }
}

// Hub fan-out (outgoing per node).
const fanOut = {};
for (const e of edges) fanOut[e.from] = (fanOut[e.from] || 0) + 1;
for (const [id, c] of Object.entries(fanOut)) if (c > 5) flag(`hub ${id} fans out to ${c} — split or group downstream (≤ 5)`);

// Merge depth (incoming per node).
const merge = {};
for (const e of edges) merge[e.to] = (merge[e.to] || 0) + 1;
for (const [id, c] of Object.entries(merge)) if (c > 4) flag(`node ${id} merges ${c} sources — split into two stages (≤ 4)`);

// Every arrow must be labeled (legibility rule).
for (const e of edges) if (!e.label || !e.label.trim()) flag(`unlabeled arrow ${e.from} → ${e.to} — label every edge`);
// Group titles ≤ 3 words, no "·" compounding.
for (const g of (spec.groups || [])) {
  const t = g.title || g.label || '';
  if (t && (t.trim().split(/[·\s]+/).length > 3 || t.includes('·'))) flag(`group title too long or compounded: "${t}" — use ≤ 3 words, one idea`);
}
// Groups.
if (spec.groups && spec.groups.length > 3) flag(`${spec.groups.length} groups — cap at 3 to keep the visual hierarchy`);

// Layers with 6+ nodes (if the spec carries column/layer membership).
const layers = spec.columns || spec.layers;
if (layers) for (const [i, layer] of layers.entries()) {
  if (layer.length > 6) flag(`layer ${i + 1} has ${layer.length} nodes — split into 1–4 for balance`);
}

if (out.length === 0) { console.log('lint: clean — tree-like, readable.'); process.exit(0); }
console.log('lint: readability warnings');
out.forEach(m => console.log('  - ' + m));
process.exit(1);
