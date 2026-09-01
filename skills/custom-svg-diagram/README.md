# Custom SVG Diagram

Build self-contained SVG architecture and flow diagrams with **machine-checked quality**: every arrow connects to a box edge, no arrow crosses a box, no two arrows overlap, no text sits on a line, and the palette stays WCAG-clean.

Invoke with `/custom-svg-diagram`, or use the scripts directly.

## What it produces

Role-color-coded boxes (source / tier-1 / tier-2 / loop / LLM / consumer), dashed group containers, and routed edges — orthogonal or curved — with layered shadows, a top sheen, and an emphasis hierarchy. All styling themes in light and dark via CSS variables. See `examples/demo.html`.

## Why not just Mermaid?

Mermaid auto-layouts but you don't control spacing, and you can't guarantee arrows land on edges or avoid overlaps. This skill gives you **deterministic control plus proof**: the geometry is verified in a real browser, not eyeballed.

## Quick start

```bash
# install the one runtime dep (dagre, for crossing-removed auto-layout)
cd ~/.claude/skills/custom-svg-diagram && npm install @dagrejs/dagre
```

Build a diagram from a graph spec:

```js
import { assemble, layout } from './layout.mjs';
const svg = assemble(layout({
  nodes: { In: { title: 'Input', role: 'source' }, /* ... */ },
  edges: [{ from: 'In', to: 'Sc', label: 'score it', emphasis: true }],
}));
```

Validate any finished diagram in one command:

```bash
node check.mjs path/to/diagram.html /path/to/chrome-headless-shell
# → [geometry] PASS   [color] PASS
```

## Legibility method (hard rules)

4 semantic categories (storage / compute / model / consumer, one color per category); short chip group labels (≤3 words, tracking ≤0.08em, reserved top band, nested dashed/small-caps); flat auto-sized boxes with centered text (title ≥16px, sub ≥13px, subtitle wraps at ~24 chars); every arrow labeled in a pill knockout. `verify.mjs` runs four legibility self-checks (text fits container, no label over border/label, group label fits width, type minimums).

## The rule it enforces (verified, not assumed)

An arrow must end exactly on a box edge, its whole path must stay in open space (never cross a box interior), it must not collide with another arrow mid-diagram, and no label may touch a box or a line. Arrows converging on a shared box edge (many arrows into one box) are allowed — that's normal. `verify.mjs` proves all of this in a browser.

## Tooling

| Script | What it does |
|---|---|
| `layout.mjs` | Primitives (`box`, `arrow`, `group`, `assemble`) + `layout()` auto-layout (dagre crossing removal, curved edges, label avoidance). |
| `palette.mjs` | Named color sets (`blueprint`, `warm`, `mono`) + `cssFor(name)` to emit the CSS variables the SVG needs. Swap palettes by swapping CSS, not diagram code. |
| `verify.mjs` | The geometric proof: connects-on-edge, no through-box, no overlap, no text-on-line. |
| `check.mjs` | One-command gate: `verify.mjs` + `color-audit.mjs`. |
| `color-audit.mjs` | WCAG contrast for every role in both themes (hard gate) + colorblind-safety pass (advisory). Pass a palette name or JSON to validate any color set. |

## Box & arrow looks

Pick a box style and arrow style per diagram, independent of color:

```js
const laid = layout({ nodes, edges, boxStyle: 'soft', arrowStyle: 'bold' });
```

`boxStyle`: `button` (default) · `flat` · `outline` · `soft` · `glow`.
`arrowStyle`: `standard` (default) · `bold` · `hairline`.

Arrow color is CSS-var driven: `--arr-color` (standard) and `--arr-color-strong` (emphasis). Set them in the page CSS to recolor arrows without touching the diagram.

## Color sets

Pick a palette and let it drive the page CSS:

```js
import { cssFor } from './palette.mjs';
const css = cssFor('warm');   // or 'blueprint' | 'mono' | your own
```

Add your own palette as an entry in `palettes` (light + dark role colors), then gate it with `node color-audit.mjs <name>`. `examples/demo.html` (blueprint) and `examples/demo-mono.html` (grayscale) show the same diagram in different color sets.
| `lint.mjs` | Readability gate for a graph spec: dense edges, long labels, fan-out, merge depth, groups, layers. |
| `benchmark.mjs` | Empirically tests routing methods (margin-routing beats naive straight-down 100% vs 0%). |
| `layout-test.mjs` | Measures the auto-layout pass rate on random DAGs; regenerates the demo. |
| `examples/demo.html` | The showcase — fans + merges, curved edges, emphasis, redundant patterns, all checks green. |

## Research & sources

The design rules come from professional diagramming and graph-drawing practice:

- **Data-flow modeling & readability** — model the data-flow story, not the dependency graph; keep it tree-like (N-1..N+2 edges); ≤4-word labels; hub fan-out ≤5; merge depth ≤4; balanced layers; ≤3 groups; dashed = async/passive, solid = sync; rounded orthogonal connectors for off-axis paths. ([SAP Architecture Center](https://architecture.learning.sap.com/docs/community/diagrams), [Excalidraw diagram-design skill](https://raw.githubusercontent.com/BV-Venky/excalidraw-architect-mcp/refs/heads/main/.skills/excalidraw-diagram-design/SKILL.md), [diagram-design type/architecture](https://raw.githubusercontent.com/cathrynlavery/diagram-design/main/skills/diagram-design/references/type-architecture.md), [HowToGeek — 4 rules for system diagrams](https://www.howtogeek.com/stop-confusing-everyone/), [NCSC — drawing good architecture diagrams](https://www.ncsc.gov.uk/blog-post/drawing-good-architecture-diagrams), [Azure Well-Architected — design diagrams](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/design-diagrams))
- **Crossing minimization** — dagre's Sugiyama-style layering minimizes crossings (barycenter sweeps) but is quadratic (~300-edge practical cap) and can mis-assign ports on incoming edges; network-simplex ranking (yFiles/GraphViz) is more robust but slower. Group-node layout reduces crossings at scale. ([dagre algorithm papers](https://nl.espacenet.com/publicationDetails/biblio?FT=D&date=19900828&DB=EPODOC&locale=nl_NL&CC=US&NR=4953106A&KC=A&ND=5), [G6 dagre improvements](https://github.com/antvis/G6/issues/3318))
- **Color & accessibility** — WCAG 4.5:1 normal / 3:1 large text; ~8% of males are colorblind, so use blue-orange palettes and never rely on red-green alone; pair color with pattern (redundant encoding). ([Excelisior — color theory & accessibility](https://express.excelsior.edu/datascience/chapter/5-4-color-theory-and-accessibility-in-data-visualization/), [NCSH data viz](https://www.oldsite.nashp.org/wp-content/uploads/2017/01/Lyons-Post-presentation-Handout.pdf))

## Workflow

1. **Describe** the diagram as data (nodes + edges) or place boxes manually.
2. **Layout** with `layout()` (auto) or place by hand with the primitives.
3. **Check** with `check.mjs` — fix anything it flags, re-run until green.
4. **Ship** the self-contained SVG.

## Known limits

- The auto-layout is ~80% crossing-free on intentionally dense random graphs and clean on realistic ones. Dagre *minimizes* crossings; it can't eliminate them on adversarial graphs. The verifier catches what remains.
- `layout()`'s label avoidance and edge routing work best when you run `check.mjs` after — never ship an auto-layout without checking it.
