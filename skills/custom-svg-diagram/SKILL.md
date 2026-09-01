# Custom SVG Diagram

Build self-contained SVG architecture and flow diagrams with **machine-checked quality**: every arrow connects to a box edge, no arrow crosses a box, no arrow overlaps another, no text sits on a line or a border, the palette stays WCAG-clean, and every diagram passes four legibility self-checks before it's done.

Invoke with `/custom-svg-diagram`. For the diagram part of a visual-explainer page, delegate here.

## Legibility method (hard rules)

These are enforced on every diagram, not tuned per file.

- **4 semantic categories** — storage / compute / model / consumer. One color per category, never per node. Old role names (`source`, `t1`, `t2`, `loop`, `llm`, `out`) alias onto them.
- **Group labels** — a short noun phrase (≤3 words, never two ideas joined with "·"); a qualifier goes on a second, smaller, lighter line. Tracking ≤0.08em. The label is a chip anchored top-left, inset inside the border. Every group reserves a top band (label height + 16px) that no node enters. Nested groups differ: outer = solid 1.5px border + filled chip; inner = dashed 1px border + small-caps label, one step smaller and lighter.
- **Nodes** — sized from measured content (never less than the longest line + padding); text centered on both axes; subtitle wraps at ~24 chars onto a second line; if it needs more than 2 lines the copy is too long. Title ≥16px, subtitle ≥13px, both ≥4.5:1 against the fill. Flat tint only: no gradient, no hatch, no gloss, no text-shadow. Color lives in the border and the title.
- **Edges** — every arrow is labeled; the label sits at the line midpoint in a pill with a page-background knockout so the line never runs through the text. Orthogonal routing.
- **Gutters** ≥32px between nodes, ≥24px padding inside groups. Nodes are live SVG text, never rasterized.

## Self-check before finishing (mandatory)

Never finish a diagram without running the gate. After generating, run:

    node check.mjs path/to/diagram.html /path/to/chrome-headless-shell

This runs `verify.mjs` — the geometry gate plus the four legibility self-checks — and the palette audit. It exits non-zero on any failure. Fix what it flags and re-run until it passes.

Before reporting a diagram as done, **report the four legibility check results**:
1. No text bbox exceeds its container's content box.
2. No label overlaps a border stroke or another label.
3. Every group label fits within the group width at rendered tracking.
4. All type meets the minimum sizes (title ≥16px, sub ≥13px) at final render scale.

## Why not just Mermaid?

Mermaid auto-layouts but you don't control spacing, and you can't guarantee arrows land on edges or avoid overlaps. This skill gives you **deterministic control plus proof**: the geometry and legibility are verified in a real browser, not eyeballed.

## Tooling (in this skill's dir)

Needs `playwright` in your cwd and a Chromium binary (see `visual-explainer`'s SKILL.md for the path).

- **`layout.mjs`** — primitives (`box`, `arrow`, `group`, `header`, `assemble`) + `layout()` auto-layout (dagre crossing removal, curved or orthogonal, label avoidance). Boxes auto-size from content and render flat with a category color.
- **`palette.mjs`** — named palettes (`blueprint`, `warm`, `mono`), each with the 4 category colors in light + dark, and `cssFor(name)` to emit the CSS variables. Swap palettes by swapping CSS, not diagram code.
- **`verify.mjs`** — the proof: arrows connect on edges, no through-box, no overlap in open space, no text on a line, **plus the four legibility self-checks**. Exits non-zero on any failure.
- **`check.mjs`** — the one-command mandatory gate: `verify.mjs` (geometry + four self-checks) and `color-audit.mjs`. `node check.mjs <diagram.html> [executablePath]`.
- **`color-audit.mjs`** — WCAG contrast for every category in both themes (hard gate) + colorblind-safety pass (advisory). `node color-audit.mjs [name|palette.json]`.
- **`lint.mjs`** — readability gate for a graph spec: every arrow labeled, group titles ≤3 words / no "·", dense edges, hub fan-out, merge depth, groups, layers.
- **`benchmark.mjs`** — empirically tests routing methods (margin-routing beats naive straight-down 100% vs 0%).
- **`layout-test.mjs`** — measures the auto-layout pass rate on random DAGs; regenerates `examples/demo.html`.
- **`examples/demo.html`** — the showcase, all checks green.

## Color sets & category colors

`palette.mjs` ships `blueprint`, `warm`, `mono`. Each defines four category colors (`--storage`, `--compute`, `--model`, `--consumer`) plus surface/text in light + dark. Add your own entry, then gate it with `node color-audit.mjs <name>`.

```js
import { cssFor } from './palette.mjs';
const css = cssFor('warm');   // → :root { … } html.dark { … }
```

## Readability rules (from the research)

Beyond geometry, a diagram is readable when tree-like and flow-oriented. `lint.mjs` enforces: edge count ~N-1..N+2, ≤4-word labels, hub fan-out ≤5, merge depth ≤4, ≤3 groups, balanced layers, and (legibility) every arrow labeled with group titles ≤3 words.

## Reference
- Live conforming example: `~/Documents/Vault/GitHub/diagrams/csm/csm-storage-scale.html` (four self-checks green).
- Sources: professional diagramming practice — [SAP Architecture Center](https://architecture.learning.sap.com/docs/community/diagrams), [Azure Well-Architected diagrams](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/design-diagrams), [NCSC — good architecture diagrams](https://www.ncsc.gov.uk/blog-post/drawing-good-architecture-diagrams), [HowToGeek — 4 rules for system diagrams](https://www.howtogeek.com/stop-confusing-everyone/); crossing minimization via dagre's Sugiyama-style layering; WCAG color/contrast.
