---
name: custom-svg-diagram
description: Build hand-crafted SVG architecture and flow diagrams with guaranteed-clean arrow routing — no arrow overlaps, no arrow-through-box crossings — and bold role-color coding. Use when a Mermaid auto-layout can't control spacing, when the user wants a two-panel or grouped layout, or when "make the arrows connect / don't overlap" matters. Produces self-contained inline SVG that themes with the page's CSS variables.
metadata:
  version: "0.1.0"
---

# Custom SVG Diagram

Hand-built SVG for diagrams where Mermaid's auto-layout isn't good enough. The whole point is **deterministic control**: exact spacing, grouped containers, and arrows that provably connect to boxes without overlapping or crossing.

Use this over Mermaid when:
- The layout is two-panel, grouped, or has a feedback arc Mermaid would mangle.
- The user cares that arrows land exactly on box edges and don't overlap.
- You want role-color-coded boxes (filled, not white outlines).
- The diagram is a deliverable (portfolio, client, interview) where polish matters.

Mermaid is still the right tool for quick throwaway diagrams or huge graphs where auto-routing beats hand-coordinates.

## The non-negotiable arrow rules

These are the rules this skill exists to enforce. Violating any of them is the reason diagrams come back "arrows don't connect" / "arrows are overlapping."

1. **Every arrow ends exactly on a box edge.** No floating arrowheads 2–6px short of the target. End the path at the box's border coordinate. `M x1 y1 L xEdge yEdge`, where `(xEdge,yEdge)` is precisely on the target box's border.
2. **No arrow passes through a box interior.** The arrow's whole path (not just its endpoint) must stay in open space.
3. **No two arrows overlap.** Parallel arrows at the same coordinate, or crossing paths, are both failures.
4. **A hub connecting to two boxes must not send an arrow through the other box.** This is the most common trap.

## Layout patterns that prevent the traps

### The stacked-box trap (the big one)
If two boxes are stacked vertically in the same column, and each feeds a consumer below, the upper box's arrow runs straight down **through the lower box**. Fix by routing the upper consumer's arrow **down an outer margin** (a corner path), not down the shared column.

```
upperBox ─┐
          │  ← route down the LEFT margin: M bottomLeft L marginX downY L marginX consumerY
lowerBox ─┴──← lower box's consumer goes straight down (it's the bottom one, so it's clear)
```

### The hub fan-out trap
A hub box (e.g. the event log) feeding two derived boxes. If the derived boxes are side-by-side and the hub is to one side, the arrow to the far box crosses the near box. Two clean fixes:

- **Stack the two derived boxes** on one side, hub on the other. The hub's two arrows fan out vertically through the empty gap. (Then fix the consumers with the margin trick above.)
- **Or** put the hub between them and keep its connections to the two adjacent edges (short, no cross) — but then consumers/loop connections must be routed around.

Whichever you pick, the derived boxes end up stacked, so apply the stacked-box fix for their consumers.

### Keep the hub near the consumer it talks to most
If a box has a hot connection (e.g. the loop↔event-log read/write), put that box at the boundary nearest the other panel so those arrows are short and horizontal. A tall "log" box hugging the panel edge reads naturally.

## Arrow routing summary
- Fan-out arrows go through **empty space** — never through another box.
- Two arrows between the same two things (a read and a write) go at **different y-heights** and opposite directions, so they never overlap.
- Consumer arrows that would cross a stacked box go down **the outer margins**.
- End every arrow at the box border coordinate; the marker tip lands on it.

## Bold color-coding

Fill each box with its role color's dim variant, not white:

```html
<rect ... class="sv-box-source" stroke-width="2"></rect>
```

with (in the page's `<style>`):

```css
.sv-box-source{fill:var(--slate-dim);stroke:var(--slate)}
.sv-box-t1{fill:var(--secondary-dim);stroke:var(--secondary)}
.sv-box-t2{fill:var(--primary-dim);stroke:var(--primary)}
.sv-box-loop{fill:var(--violet-dim);stroke:var(--violet)}
.sv-box-llm{fill:var(--amber-dim);stroke:var(--amber)}
.sv-box-out{fill:var(--good-dim);stroke:var(--good)}
```

Color the box title text to match its role. Use `--*-dim` fills + solid-color borders + `stroke-width:2` so the coding survives both light and dark themes. Fill/stroke referencing CSS variables themes automatically.

## Professional polish (shading, curves, emphasis, color)

`layout.mjs` ships a premium look out of the box, all themeable via CSS variables:

- **3D button shadow** — a three-layer shadow in one filter: a tight contact shadow, a **crisp hard offset** (`dy:3.5, blur:0`) that reads as the raised button's underside/thickness, and a soft ambient one. This is the subtle "3D button" cue. The rounded face + top sheen complete it.
- **Face gradient** — each box face is a per-role vertical gradient (lighter top → deeper bottom) via `url(#g<role>)`, so it reads with rounded volume. Stops live in `GRADIENT` in `layout.mjs`; theme-aware because they reference the CSS color vars.

## Box & arrow looks

Boxes and arrows each have a swappable "look", orthogonal to color. Pick them per diagram:

```js
const laid = layout({ nodes, edges, boxStyle: 'soft', arrowStyle: 'bold' });
```

**`boxStyle`** (`STYLES` in `layout.mjs`, default `button`):
- `button` — 3D button: rounded, hard underside shadow, face gradient, gloss.
- `flat` — minimal: flat dim fill, thin border, no shadow. For dense/print.
- `outline` — technical: transparent fill, strong border.
- `soft` — rounded card: soft shadow, gradient, gloss, more rounded.
- `glow` — a per-role colored outer glow. For dark dashboards.

**`arrowStyle`** (`ARROW_STYLES`, default `standard`): `standard` (2), `bold` (2.75), `hairline` (1.25) — thickness presets.

**Arrow color** is CSS-var driven like box color: standard arrows use `--arr-color` (default `var(--text-muted)`), emphasis arrows use `--arr-color-strong` (default `var(--secondary)`). Override them in the page CSS to recolor arrows without touching the diagram. The `emphasis: true` per-edge flag still promotes an edge to the strong highlight.
- **Top sheen** — a white-to-transparent vertical gradient over the top of every box, plus a faint 1px light line along the top edge. Reads as glass gloss in both light and dark.
- **Curved edges** — `layout()` routes every edge with `smoothPath()`, rounding each 90° corner with a quadratic bezier. The curve stays inside the orthogonal corridor, so it reads premium without adding overlap risk (verified at the same pass rate as orthogonal). Pass `curved: false` for the sharp/orthogonal look.
- **Emphasis hierarchy** — mark an edge `emphasis: true` and it renders as `.sv-arrow--strong` (thicker, colored cyan, matching arrowhead) against the muted default. Use it to light up the primary flow and let secondary paths recede.
- **Rounded line joins** — add `stroke-linejoin:round; stroke-linecap:round` to the arrow classes so corners smooth out.

**Color coherence** is enforced by `color-audit.mjs`, which computes WCAG contrast (title vs box background, sub-text vs box background, body vs surface) for every role in both themes and exits non-zero on any failure. It also reports a colorblind-safety pass (deuteranopia simulation, advisory): the mitigation for roles that blur together is **redundant encoding** — pass `patterns: true` to `layout()` to overlay a subtle per-role pattern so color is never the only signal.

## Color sets (palettes)

The SVG references CSS variables (`--slate`, `--surface`, …), so **swapping color sets is a CSS swap, not a diagram change**. `palette.mjs` holds named palettes and emits their CSS:

```js
import { cssFor, palettes } from './palette.mjs';
const css = cssFor('blueprint');   // :root { … } html.dark { … }
```

Shipped palettes: **`blueprint`** (default technical), **`warm`** (editorial), **`mono`** (grayscale, color-blind-safe — roles differ by shade, patterns carry the rest). Add your own as an entry in `palettes` (light + dark, each with `surface/bg/text/textDim/dim` and the six role colors), then `color-audit.mjs <name>` to validate it before shipping.

Validate a palette by name: `node color-audit.mjs warm`. Note `check.mjs` audits the default blueprint palette; run `color-audit.mjs <name>` to gate a non-default palette.

## Readability rules (from the research)

Beyond geometry, a diagram is readable when it's **tree-like and flow-oriented**, not a dependency graph. `lint.mjs` enforces these thresholds on a graph spec:

| Rule | Limit | Why |
|---|---|---|
| Edge count | ~N-1 to N+2 for N nodes | More = dependency graph, not data flow |
| Edge labels | ≤ 4 words | Long labels force layers apart / reroute |
| Hub fan-out | ≤ 5 children per node | 6+ = split or group downstream |
| Merge depth | ≤ 4 sources into one node | 4+ = a diamond to avoid |
| Groups | ≤ 3 per diagram | More collapses the hierarchy |
| Layer size | 1–4 nodes per layer | 6+ makes it vertically sprawling |

Also from the research: model the **data-flow story** (not the implementation graph), keep one symbol per category, label lines (dashed = async/reverse/passive, solid = sync), and prefer rounded orthogonal connectors for off-axis paths. See the README for sources.

## The geometric verification (do this every time)

Never trust your eyes — prove it. After writing the SVG, run the verifier (below) that asserts all three rules, and fix anything it flags. Empirically, this matters: a benchmark comparing the margin-routing method against the naive stacked-consumer method across 40 random layouts scored **100% vs 0%** — the naive approach fails on every instance because the consumer arrow crosses the stacked box. The method in this skill is the one that provably passes.

See `benchmark.mjs` to re-run that test yourself.

## Tooling (in this skill's dir)

The skill ships three scripts. They need `playwright` installed in your cwd and a Chromium binary (the path is the same one `visual-explainer` uses — see its SKILL.md).

- **`layout.mjs`** — build diagrams from data, not hand-coordinated paths. `box()`, `arrow()`, `group()`, `header()`, `assemble()` emit the role-colored SVG matching the skill's CSS classes. This is the reliable core: describe boxes + arrows, get verifiable SVG.
  - **`layout()` (auto-layout, real crossing removal)** — takes `{nodes, edges}` and runs them through **@dagrejs/dagre**: it layers the graph, minimizes edge crossings, and routes the edges. Handles multi-parent merges and multi-child fans. Arrow endpoints are clipped to the box borders, and each label is placed above the edge's longest horizontal run so text never sits on the line. `npm install @dagrejs/dagre` in the skill dir (done). It minimizes crossings but doesn't eliminate them on adversarial dense graphs — measured ~80% clean on random DAGs with 2-parent merges, and clean on realistic/sparse diagrams. **Always run `verify.mjs` after `layout()`** and fall back to the manual primitives if a specific diagram needs exact control.
- **`verify.mjs`** — the geometric proof. Usage: `node verify.mjs <path-or-url> [executablePath]`. Asserts every arrow connects to a box edge, none cross a box interior, none overlap **in open space** (arrows converging on a shared box edge are allowed, since that's normal), and no `.sv-arrow-lbl` text sits on an arrow line. Exits non-zero on any failure.
- **`examples/demo.html`** — a dagre auto-layout showcase (fans + merges) that passes verify cleanly. Regenerate with `layout-test.mjs`.
- **`benchmark.mjs`** — the empirical method test. Usage: `node benchmark.mjs <nConfigs> [executablePath]`. Renders N random layouts under two routing strategies and reports pass rates, so "which method is best" is answered by data, not taste.
- **`layout-test.mjs`** — validates the auto-layout against random layered forests and emits an example diagram. Usage: `node layout-test.mjs <nConfigs> <executablePath> [demoOut.html]`.
- **`color-audit.mjs`** — the palette gate. Usage: `node color-audit.mjs [palette.json]`. Computes WCAG contrast for every role in both themes (hard gate) + a colorblind-safety pass (advisory).
- **`lint.mjs`** — the readability gate for a graph spec. Usage: `node lint.mjs <graph.json>`. Flags dense edge counts, long labels, hub fan-out, merge depth, group count, layer balance. Run on the spec before rendering.
- **`check.mjs`** — the one-command gate for a finished diagram. Usage: `node check.mjs <diagram.html> [executablePath]`. Runs geometry + labels (`verify.mjs`) and palette (`color-audit.mjs`) in one shot; exits non-zero if either fails.

**Reuse, don't reinvent.** For effects beyond the base diagram, pull from `~/.claude/skills/visual-explainer/references/css-patterns.md`: the SVG curved-connector overlay, the `drawIn` connector animation, and the `prefers-reduced-motion` guard. `layout.mjs` emits the structural SVG; css-patterns.md supplies the polish.

## Reference
- Live example: `~/Documents/Vault/GitHub/diagrams/csm/csm-storage-scale.html` — a two-panel storage + loop diagram exercising all the above rules (stacked tables, margin-routed consumers, hub fan-out, read/write at different heights).
