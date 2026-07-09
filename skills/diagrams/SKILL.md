---
name: diagrams
description: Build self-contained HTML diagram pages for the motorthings/diagrams GitHub Pages repo. Use when working in the diagrams repo, when the user asks to add a page to their diagrams collection, or when they ask for a visual explainer that should match their portfolio style (Gulf Stream Racing theme, Fraunces + Source Code Pro fonts, sticky nav with theme toggle, fixed backlinks). Always delegate HTML generation to the visual-explainer skill — this skill provides the repo-specific rules, constraints, and overrides.
metadata:
  repo: /Users/motorthings/Documents/Vault/GitHub/diagrams
  deployment: https://motorthings.github.io/diagrams/
---

# Diagrams Skill

Build self-contained HTML pages matching the `motorthings/diagrams` repo style. Every page is a single `.html` file — no build step, no external CSS/JS dependencies beyond Google Fonts and Mermaid CDN.

**Always delegate HTML generation to the `visual-explainer` skill.** This skill defines the repo-specific rules (colors, nav, backlinks, index format); visual-explainer handles the actual HTML/CSS/JS construction using its templates and component library. Read visual-explainer's `SKILL.md` for rendering approach decisions (Mermaid vs pure CSS vs CSS grid cards).

## When to Use

- Working in the `diagrams` repo (`/Users/motorthings/Documents/Vault/GitHub/diagrams`)
- User asks to add a page, diagram, flowchart, or visual explainer to their portfolio
- User asks about diagrams repo conventions (colors, backlinks, index format, voice)
- User says "make a diagram", "add to diagrams", "build a page for the portfolio"
- User references `motorthings.github.io/diagrams` or the diagrams collection

## Design System Reference

### Fonts
```html
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400&family=Source+Code+Pro:wght@400;500;600;700&display=swap" rel="stylesheet">
```

| Role | Font | Weight | Size | Usage |
|---|---|---|---|
| Display / headings | Fraunces | 600-800 | 44-48px h1, 26px h2, 20-22px h3 | Hero, section titles, card titles |
| Body | Fraunces | 400-500 | 13-16px | Paragraphs, descriptions, stage body |
| Mono / labels | Source Code Pro | 400-700 | 9-13px | Badges, tags, nav, section labels, code |

### Colors — Gulf Stream Racing (default)

```
Light:  bg=#eef4f9  surface=#ffffff  text=#0a1628  primary=#e8621a  secondary=#4a90c4  metric=#0f766e
Dark:   bg=#0a1628  surface=#132240  text=#e8edf5  primary=#f37021  secondary=#6cace4  metric=#2dd4bf
```

Full palette: `--primary` (orange), `--secondary` (blue), `--metric` (teal), `--amber`, `--violet`, `--rose`, `--slate`. Each has a `--*-dim` variant at ~8% opacity in light, ~12% in dark.

### CSS Variable Naming

Two conventions exist in the repo. **Use kebab-case for new diagram pages.** The snake_case convention is legacy from waifinder-assistant portfolio pages — only use it when copying from those pages.

| Convention | Example | Used in |
|---|---|---|
| **kebab-case** (preferred) | `--text-dim`, `--primary-dim`, `--border-bright` | All diagram pages, templates |
| snake_case (legacy) | `--color_text_secondary`, `--color_border` | `portfolio/index.html`, `portfolio/consultant-offer.html` |

### Layout Conventions

| Property | Diagram Page | Portfolio Page | Notes |
|---|---|---|---|
| Container max-width | 1000px | 920px | `.container` class |
| Body padding | `0 32px 80px` | `0 24px 64px` | Top=0 (nav handles it) |
| Hero h1 size | 44px, weight 800 | 48px, weight 700 | |
| Hero h1 color | `var(--text)` | `var(--primary)` | |
| Hero badge | Yes | No | |
| Section spacing | `margin-top: 40px` | `margin-top: 40px` | |
| Card border-radius | 8-14px | 8-10px | Varies by component |
| Mobile breakpoint | 640px | 640px | Stack grids, shrink h1 to 28px |
| Nav sticky | Yes (blur backdrop) | Yes (blur backdrop) | `margin: 0 -32px 32px` negative margin |

### Body Background
Diagram pages: dual gradient (primary + secondary). Portfolio pages: single gradient (primary only).
```css
/* Diagram — dual */
background-image:
  radial-gradient(ellipse at 80% 0%, var(--primary-dim) 0%, transparent 50%),
  radial-gradient(ellipse at 20% 60%, var(--secondary-dim) 0%, transparent 40%);

/* Portfolio — single */
background-image: radial-gradient(ellipse at 80% 0%, var(--primary-dim) 0%, transparent 50%);
```

### No Emoji
Unicode/HTML entities only: `&#9788;` ☀ `&#9790;` ☾ `&larr;` ← `&rarr;` → `&darr;` ↓ `&mdash;` — `&#9679;` ● `&middot;` · `&bull;` •

### Title Tags
Format: `[Project] — [Page Name]`

```html
<title>AESOP Transformation OS — Executive Overview</title>
<title>AESOP Transformation OS — Build Decision Flow</title>
<title>AI Maturity Model — Executive View — AESOP Transformation OS</title>
```

- Project name first, then page name
- Em-dash separator (`&mdash;` or `—`)
- For multi-word projects, include the full project name on first reference
- No "Charlie Fuller" or "Portfolio" in individual page titles (that's the index page only)

### Meta Description
Every page. One sentence. What the page explains, not what the platform does.

```html
<meta name="description" content="How AESOP evaluates AI agents across seven complementary modes with weighted scoring and a hard safety/bias veto.">
```

- 120-155 characters
- Active voice, present tense
- Include the project name naturally
- No "This page describes..." — just describe it

---

## Repo Structure

```
diagrams/
├── index.html              ← collapsible-section index
├── icon.svg                ← favicon
├── CNAME                    ← motorthings.github.io
├── aesop/                   ← AESOP pages
├── portfolio/               ← portfolio/overview pages
└── [topic]/                 ← one folder per topic
```

---

## Color Schemes

### Default: Gulf Stream Racing

The standard palette. Orange primary, blue secondary, teal metric. Used on most pages. Reference: `aesop/ai-maturity-model-executive.html`.

```css
:root {
  --font-display: 'Fraunces', Georgia, serif;
  --font-mono: 'Source Code Pro', 'SF Mono', Consolas, monospace;
  --bg: #eef4f9; --surface: #ffffff; --surface2: #f5f8fc;
  --border: #c8daea; --border-bright: #a0bedb;
  --text: #0a1628; --text-dim: #3d5a7a; --text-muted: #7a9ab8;
  --primary: #e8621a; --primary-dim: rgba(232,98,26,0.08);
  --secondary: #4a90c4; --secondary-dim: rgba(74,144,196,0.08);
  --metric: #0f766e; --metric-dim: rgba(15,118,110,0.06);
  --amber: #b45309; --amber-dim: rgba(180,83,9,0.08);
  --violet: #7c3aed; --violet-dim: rgba(124,58,237,0.08);
  --rose: #e11d48; --rose-dim: rgba(225,29,72,0.08);
  --slate: #475569; --slate-dim: rgba(71,85,105,0.08);
}

html.dark {
  --bg: #0a1628; --surface: #132240; --surface2: #1a2d52;
  --border: #1a2d52; --border-bright: #2d4570;
  --text: #e8edf5; --text-dim: #9bb0d4; --text-muted: #5e7aa3;
  --primary: #f37021; --primary-dim: rgba(243,112,33,0.12);
  --secondary: #6cace4; --secondary-dim: rgba(108,172,228,0.12);
  --metric: #2dd4bf; --metric-dim: rgba(45,212,191,0.08);
  --amber: #f59e0b; --amber-dim: rgba(245,158,11,0.12);
  --violet: #a78bfa; --violet-dim: rgba(167,139,250,0.12);
  --rose: #fb7185; --rose-dim: rgba(251,113,133,0.12);
  --slate: #94a3b8; --slate-dim: rgba(148,163,184,0.12);
}
```

### Custom Color Schemes

Ask the user: "Gulf Stream Racing colors, or do you want me to choose a scheme that fits the content?"

When choosing a custom scheme, vary the personality while keeping the CSS variable names the same. Examples from the repo:

**Warm / Earthy** (`aesop/aesop-ux-audit.html`):
```css
:root {
  --bg: #faf8f5; --surface: #ffffff; --surface2: #f5f2ed;
  --text: #1a1815; --text-dim: #7a7268;
  --accent: #8b5e3c; --accent-dim: rgba(139,94,60,0.08);
  --green: #2d7a4f; --red: #b5362a; --orange: #c27a1a;
  --blue: #2a6cb5; --purple: #6b4fa0;
}
```
(`--accent` replaces `--primary` in this scheme.)

**Blueprint** (`aesop/aesop-os-decision-flow.html`):
```css
:root {
  --bg: #f5f7fa; --surface: #ffffff; --surface2: #eef1f6;
  --text: #1e293b; --text-dim: #64748b;
  --phase0: #6366f1; --auto: #0891b2; --workflow: #7c3aed;
  --fail: #dc2626; --gate: #d97706; --pattern: #059669;
}
```
(Semantic names instead of generic ones — match the domain.)

Always keep the same variable *structure* (`--bg`, `--surface`, `--text`, etc.) so the layout CSS works unchanged. Only the hex values change.

---

## Theme Toggle (standard on all pages)

Every page gets a manual light/dark toggle in a sticky nav bar. Uses `html.dark` class (not `@media prefers-color-scheme`). Persists to `localStorage` as `diagram-theme`.

### CSS
```css
body {
  background: var(--bg);
  background-image: radial-gradient(ellipse at 80% 0%, var(--primary-dim) 0%, transparent 50%),
                    radial-gradient(ellipse at 20% 60%, var(--secondary-dim) 0%, transparent 40%);
  color: var(--text); font-family: var(--font-display);
  min-height: 100vh; line-height: 1.6; padding: 0 32px 48px;
  transition: background 0.3s, color 0.3s;
}

.nav {
  position: sticky; top: 0; z-index: 100;
  backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
  background: color-mix(in srgb, var(--surface) 85%, transparent);
  border-bottom: 1px solid var(--border);
  margin: 0 -32px 32px; padding: 0 32px;
  transition: background 0.3s, border-color 0.3s;
}
.nav-inner {
  max-width: 1100px; margin: 0 auto; padding: 12px 0;
  display: flex; align-items: center; justify-content: space-between;
}
.nav-brand {
  font-family: var(--font-mono); font-size: 12px; font-weight: 600;
  letter-spacing: 0.5px; color: var(--primary);
}
.theme-toggle {
  width: 36px; height: 36px; border-radius: 10px;
  border: 1px solid var(--border); background: var(--surface);
  cursor: pointer; display: flex; align-items: center; justify-content: center;
  font-size: 16px; color: var(--text-dim); transition: all 0.2s;
}
.theme-toggle:hover { border-color: var(--primary); color: var(--primary); }
```

### HTML
```html
<div class="nav">
  <div class="nav-inner">
    <span class="nav-brand">BRAND NAME</span>
    <button class="theme-toggle" id="themeToggle" aria-label="Toggle dark mode">
      <span class="icon-light">&#9788;</span>
      <span class="icon-dark" style="display:none">&#9790;</span>
    </button>
  </div>
</div>
```

### JS (place before `</body>`)
```html
<script>
  const toggle = document.getElementById('themeToggle');
  const iconLight = toggle.querySelector('.icon-light');
  const iconDark = toggle.querySelector('.icon-dark');
  function setTheme(d) {
    document.documentElement.classList.toggle('dark', d);
    iconLight.style.display = d ? 'none' : '';
    iconDark.style.display = d ? '' : 'none';
    try { localStorage.setItem('diagram-theme', d ? 'dark' : 'light'); } catch(e) {}
  }
  toggle.addEventListener('click', () => setTheme(!document.documentElement.classList.contains('dark')));
  try { if (localStorage.getItem('diagram-theme') === 'dark') setTheme(true); } catch(e) {}
</script>
```

Important: dark mode is defined in `html.dark { ... }` — NOT `@media (prefers-color-scheme: dark)`. The toggle is the sole control. If the user wants auto-detection, they can remove the toggle and switch back to `@media`.

---

## Three Layout Modes

| | Mermaid Diagram | Portfolio / Overview | Pure CSS Flowchart |
|---|---|---|---|
| **Folder** | `aesop/`, `[topic]/` | `portfolio/` | anywhere |
| **Content** | Mermaid diagram + detail cards | Numbered stages + subpanels | Vertical step cards with CSS connectors |
| **JS** | Mermaid init + zoom/pan + theme toggle | Theme toggle only | Theme toggle only |
| **Container** | `max-width: 1000px` | `max-width: 920px` | `max-width: 1100px` |
| **Hero h1** | `color: var(--text)`, 44px, 800 weight | `color: var(--primary)`, 48px, 700 weight | Centered, serif, italic optional |
| **Hero badge** | Yes (`.hero-badge`) | No | No |
| **Flow style** | Mermaid `classDef` + CSS bridge | n/a | `flex-direction: column` step cards + `.connector` bars |
| **Example** | `aesop/aesop-org-research-process.html` | `portfolio/aesop-studio-overview.html` | `aesop/monday-platform-capabilities.html` |

**Pure CSS Flowchart** — use when the flow is linear (A→B→C→D) with 3-5 steps. Each step is a styled card, connected by vertical `.connector` bars (2px wide, 36px tall). No JavaScript diagram library needed. Reference: `aesop/monday-platform-capabilities.html`.

---

## Mode 1: Diagram Page Template

Full HTML template for Mermaid diagram pages. **Read the file** — don't memorize it.

→ `./references/template-diagram.html`

Includes: Gulf Stream Racing colors, sticky nav + theme toggle, hero with badge, Mermaid container with zoom controls, context cards, phase cards, callout, footer, and all three JS blocks (Mermaid init, zoom/pan, theme toggle).
```

---

## Mode 2: Pure CSS Flowchart

For linear A→B→C→D flows. **No Mermaid.** Centered flexbox nodes with Unicode arrow characters between them. Arrows always line up because everything is `align-items: center` in a column. Reference: `aesop/aesop-onboarding.html`.

### How it works

Each step is a `.flow-node` containing a `.flow-box` (the colored content card) and a `.flow-tag` (the actor label below). Nodes are stacked vertically in a `.flow-row` with `&darr;` arrows between them.

### CSS (add these to your stylesheet)

```css
/* Flowchart container */
.flowchart {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 12px; padding: 24px 20px; margin-bottom: 32px;
}

/* Vertical stack — everything centered */
.flow-row {
  display: flex; flex-direction: column; align-items: center; gap: 0;
}

/* Each node: box + tag label */
.flow-node {
  display: flex; flex-direction: column; align-items: center; gap: 6px;
  min-width: 115px; flex-shrink: 0;
}

/* The colored content card */
.flow-box {
  border-radius: 10px; padding: 12px 14px; text-align: center;
  font-weight: 500; font-size: 13px; line-height: 1.35;
}

/* Box color variants — define per actor/role */
.flow-box--admin { background: var(--flow-admin); border: 2px solid var(--flow-admin-stroke); }
.flow-box--client { background: var(--flow-client); border: 2px solid var(--flow-client-stroke); }
.flow-box--system { background: var(--flow-system); border: 2px solid var(--flow-system-stroke); }
.flow-box--gate { background: var(--flow-gate); border: 2px dashed var(--flow-gate-stroke); }

/* Actor tag below each box */
.flow-tag {
  font-family: var(--font-mono); font-size: 9px; font-weight: 600;
  text-transform: uppercase; letter-spacing: 1px;
}
.flow-tag--admin { color: var(--primary); }
.flow-tag--client { color: var(--secondary); }
.flow-tag--system { color: var(--metric); }
.flow-tag--gate { color: var(--amber); }

/* Arrow between nodes — always centered */
.flow-arrow {
  padding: 2px 0; font-size: 18px;
  color: var(--text-faint, #7a9ab8); font-family: var(--font-mono);
}

/* Legend row below the flow */
.flow-legend {
  display: flex; align-items: center; justify-content: center; gap: 18px;
  margin-top: 14px; font-family: var(--font-mono); font-size: 10px; color: var(--text-dim);
}
.flow-legend span { display: flex; align-items: center; gap: 5px; }
```

### Color variables (add to `:root` and `html.dark`)

```css
:root {
  --flow-admin: #fde8d8;       --flow-admin-stroke: #c84d0e;
  --flow-client: #e0eef7;      --flow-client-stroke: #4a90c4;
  --flow-system: #d5f0ee;      --flow-system-stroke: #0f766e;
  --flow-gate: #fef0d7;        --flow-gate-stroke: #b45309;
}
html.dark {
  --flow-admin: rgba(243,112,33,0.15);   --flow-admin-stroke: #f37021;
  --flow-client: rgba(108,172,228,0.15); --flow-client-stroke: #6cace4;
  --flow-system: rgba(94,234,212,0.12);  --flow-system-stroke: #5eead4;
  --flow-gate: rgba(251,191,36,0.15);    --flow-gate-stroke: #fbbf24;
}
```

### HTML structure

```html
<div class="flowchart" style="--i:4">
  <div class="flow-row">
    <div class="flow-node">
      <div class="flow-box flow-box--admin">Admin sends<br/>intake link</div>
      <div class="flow-tag flow-tag--admin">Admin</div>
    </div>
    <div class="flow-arrow">&darr;</div>
    <div class="flow-node">
      <div class="flow-box flow-box--client">Client fills<br/>29 questions</div>
      <div class="flow-tag flow-tag--client">Client</div>
    </div>
    <div class="flow-arrow">&darr;</div>
    <div class="flow-node">
      <div class="flow-box flow-box--system">AESOP processes<br/>~2 min</div>
      <div class="flow-tag flow-tag--system">System</div>
    </div>
    <div class="flow-arrow">&darr;</div>
    <div class="flow-node">
      <div class="flow-box flow-box--gate">Approved?</div>
      <div class="flow-tag flow-tag--gate">Gate</div>
    </div>
  </div>
  <div class="flow-legend">
    <span><span style="display:inline-block;width:10px;height:10px;border-radius:2px;background:var(--flow-admin-stroke)"></span> Admin</span>
    <span><span style="display:inline-block;width:10px;height:10px;border-radius:2px;background:var(--flow-client-stroke)"></span> Client</span>
    <span><span style="display:inline-block;width:10px;height:10px;border-radius:2px;background:var(--flow-system-stroke)"></span> System</span>
    <span><span style="display:inline-block;width:10px;height:10px;border-radius:2px;border:2px dashed var(--flow-gate-stroke)"></span> Gate</span>
  </div>
</div>
```

### When to use this vs. Mermaid

| Situation | Use |
|---|---|
| Linear A→B→C→D flow (any length) | **Pure CSS flowchart** |
| Branching, diamonds, decisions | Mermaid `flowchart TD` |
| Complex graph with many edges | Mermaid |
| Need perfect vertical alignment | **Pure CSS flowchart** |
| Want zoom/pan controls | Mermaid |
| Want zero JS dependencies | **Pure CSS flowchart** |

---

## Mode 3: Portfolio / Overview Page Template

Full HTML template for executive overview pages with numbered stages + subpanels. **Read the file** — don't memorize it.

→ `./references/template-portfolio.html`

Includes: Gulf Stream Racing colors, sticky nav + theme toggle, hero (h1 in primary color, no badge), numbered stages with outcome-line + subpanels + metric-line, outcome grid, footer, theme toggle JS. No Mermaid.
```

---

## Additional Component Patterns

### TOC Sidebar
For long audit/reference pages. Sticky left sidebar with IntersectionObserver active-section tracking. Reference: `aesop/aesop-os-decision-flow.html`, `aesop/aesop-ux-audit.html`.

Layout:
```css
.wrap { max-width: 1400px; margin: 0 auto; display: grid; grid-template-columns: 180px 1fr; gap: 0 40px; }
.main { min-width: 0; }
.toc { position: sticky; top: 60px; align-self: start; padding: 14px 0; max-height: calc(100dvh - 120px); overflow-y: auto; }
```
On mobile, the TOC becomes a horizontal scroll bar.

### Level Cards (maturity/readiness)
5-column grid with big numbers, colored top border, italic tagline. Reference: `aesop/ai-maturity-model-executable.html`.

### Progress Bar
Horizontal segmented bar. Each segment colored by level/dimension.

### Score Gauges
SVG donut chart with animated stroke-dashoffset. Reference: `aesop/aesop-ux-audit.html`.

### Data Tables
```html
<div class="table-wrap"><div class="table-scroll">
  <table class="data-table">
    <thead><tr><th>Col</th></tr></thead>
    <tbody><tr><td>Data</td></tr></tbody>
  </table>
</div></div>
```

### Collapsible Details
```html
<details class="collapsible">
  <summary>Title</summary>
  <div class="collapsible__body">Content.</div>
</details>
```

### Legend
```html
<div class="legend">
  <div class="legend-item"><div class="legend-swatch" style="background:var(--primary)"></div> Label</div>
</div>
```

---

## Mermaid Rules (non-negotiable)

### Initialization
- **Always**: `startOnLoad: true`, `theme: 'base'`, `look: 'classic'`
- **Never**: `layout: 'elk'` or `mermaid.registerLayoutLoaders(...)` — ELK causes blank diagrams on GitHub Pages
- **Never**: `mermaid.run()` manually — `startOnLoad: true` handles it
- Import: `https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs`
- Check `html.dark` class for Mermaid dark mode colors (not `prefers-color-scheme`)

### Diagram Syntax
- Use `flowchart TD` (top-down) or `flowchart LR` (left-right)
- **Always quote all node labels** with `["Label text"]`
- `classDef` uses hardcoded `rgba()` values, NOT CSS variables (Mermaid can't read them)
- One class per line in the `class` block
- No `<br/>` in labels — Mermaid auto-wraps
- No emoji in labels — text only
- No `&` unless escaped as `&amp;`
- No `stroke-dasharray` in `classDef` — use CSS override

### classDef → CSS bridge
Define `classDef` with hardcoded light-mode colors, then override in CSS. This is how dark mode works for Mermaid:
```css
.mermaid g.primary rect, .mermaid g.primary polygon, .mermaid g.primary circle {
  fill: var(--primary-dim) !important; stroke: var(--primary) !important;
}
```

Standard class names: `input`, `entry`, `research`, `agent`, `profile`, `output`, `warn`, `closed`, `flow`, `stage`, `decision`, `auto`, `wkfl`, `fail`, `gate`, `pattern`, `hybrid`, `neutral`.

### Zoom Controls
Always include zoom buttons (+/−/reset) plus Ctrl+scroll zoom and click-drag pan. Copy from the template verbatim.

---

## Linking Strategy

### Required Boilerplate (Every Page)

**Three things every new page MUST include:**

1. **Favicon** — in `<head>`, before the Google Fonts link:
   ```html
   <link rel="icon" href="../icon.svg" type="image/svg+xml" />
   ```
   Adjust `../` depth based on folder nesting (root = `icon.svg`, one level deep = `../icon.svg`).

2. **Backlink** — fixed-position link to parent page (see rules below).

3. **Nav brand as link** — the nav brand text must link to `../index.html` (or appropriate parent):
   ```html
   <a href="../index.html" class="nav-brand">← Page Name</a>
   ```

### Table / Matrix Cell Content

**Keep cells short.** Each cell should be one line — a label-like sentence, not a paragraph. No `<span class="signal">` italic quotes inside cells. The reader is scanning, not reading. If a cell needs more than ~15 words, it's too long.

### Backlinks
Every page gets a fixed-position backlink. **The target depends on depth:**

| Page location | Backlink target | Example |
|---|---|---|
| Top of a section (e.g. `portfolio/index.html`) | `../index.html` (main index) | `<a href="../index.html" class="backlink">&larr; Index</a>` |
| Child of a section (e.g. `portfolio/consultant-offer.html`) | Parent page (same folder) | `<a href="index.html" class="backlink">&larr; Portfolio</a>` |
| Standalone diagram page (e.g. `aesop/*.html`) | `../index.html` | `<a href="../index.html" class="backlink">&larr; Index</a>` |

Backlink CSS is **non-negotiable — copy verbatim.** Use CSS variable fallbacks for pages with custom color schemes that don't define the standard variable names:
```css
.backlink{position:fixed;top:12px;left:16px;z-index:101;font-family:var(--font-mono,'Source Code Pro',monospace);font-size:12px;color:var(--text-dim,var(--text3));text-decoration:none;padding:6px 10px;border:1px solid var(--border);border-radius:6px;background:var(--surface);transition:color .15s,border-color .15s}
.backlink:hover{color:var(--text);border-color:var(--border-bright,var(--text2))}
```
**Never** change `top:12px`, `left:16px`, or the `position:fixed` — this is the standard placement across every page in the repo. The backlink sits in the very top-left corner above the nav bar.

**The nav must clear the backlink.** The fixed backlink at `left:16px` extends ~85px to the right. If the nav bar spans full width with its brand link on the left, the nav content will overlap the backlink. Always set `padding-left: 100px` (or more) on the nav to push its content past the backlink:

```css
.nav {
    backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
    background: color-mix(in srgb, var(--surface) 85%, transparent);
    border-bottom: 1px solid var(--border);
    margin: 0 0 32px; padding: 0 32px 0 100px;
    display: flex; align-items: center; gap: 2rem;
    height: 56px;
}
```

If the page uses a `nav-inner` wrapper with centered `max-width` (like the reference page `legal-ai-storage-options.html`), the `padding-left` is unnecessary because the centered content naturally clears the backlink on all but the narrowest screens. Prefer the `nav-inner` approach for pages with standard 1000px containers; use `padding-left` for pages with full-width navs.

### Footer
Minimal: copyright only. Optionally add prev/next links between related pages.
```html
<div class="footer">&copy; 2025-2026 Charlie Fuller</div>
```

### Index page entries
Add every new page to `index.html` in the correct section. **Format rules:**
- Use `<details class="section">` for top-level sections, `<details class="subsection">` for groups within a section
- Section content uses `<div class="links">` with `<a class="card-link">` — **never `.card-grid`**
- Each entry: one line with `<span class="card-title">` + `<span class="card-desc">`
- Keep Portfolio as the first section (open by default), project sections below
- Title format: `<span class="card-title">Page Name</span><span class="card-desc">One-line description of what this page explains.</span>`

```html
<details class="section" open>
  <summary>Section Name</summary>
  <div class="section-body">
    <details class="subsection">
      <summary>Subgroup</summary>
      <div class="links">
        <a href="path/to/page.html" class="card-link"><span class="card-title">Page Title</span><span class="card-desc">Description.</span></a>
      </div>
    </details>
  </div>
</details>
```

---

## Workflow

1. Ask: "Gulf Stream Racing colors, or custom scheme?"
2. Determine mode: diagram, portfolio/overview, or pure CSS flowchart
3. **Delegate to visual-explainer** — invoke the visual-explainer skill to generate the HTML, passing these constraints:
   - Color palette (Gulf Stream or custom)
   - Page mode (diagram / portfolio / CSS flowchart)
   - This skill's rules (theme toggle, backlinks, no emoji, `html.dark`, no ELK)
4. Add the correct backlink (parent-relative for nested pages, `../index.html` for top-level)
5. Add entry to `index.html` in the correct section using `.links` + `.card-link` format
6. Run the verification checklist
7. `git add`, commit, push
8. Verify at `https://motorthings.github.io/diagrams/[folder]/[page].html`

**Overrides to visual-explainer defaults:**
- Colors: Gulf Stream Racing palette, not visual-explainer's aesthetic picks
- Theme: `html.dark` class toggle with localStorage, not `@media prefers-color-scheme`
- Nav: sticky blur-backdrop nav with brand + toggle, not visual-explainer's default nav
- Backlink: fixed-position per the backlink rules above
- Mermaid: never ELK layout, always `look: 'classic'`
- Flowcharts: linear flows = pure CSS (Mode 2), branching = Mermaid
- Fonts: always Fraunces + Source Code Pro, not visual-explainer's font picker

### Verification Checklist

Before committing, open the file in a browser and verify:

| Check | What to look for |
|---|---|
| **Dark mode** | Click theme toggle — all text readable, gradients work, Mermaid nodes have correct fill/stroke |
| **Light mode** | Click back — same checks in light |
| **Backlink** | Click it — goes to the right parent page |
| **Mobile** | Resize to 375px — no horizontal scroll, grids stack, h1 doesn't overflow |
| **Mermaid renders** | Diagram visible, not blank, all nodes labeled, zoom buttons work |
| **No broken links** | Click every link in the footer and body |
| **Title tag** | `[Project] — [Page Name]` format, matches h1 |
| **Meta description** | Present, 120-155 chars, describes this page |
| **No emoji** | Search for emoji — Unicode entities only |
| **`html.dark` not `@media`** | Dark mode uses `html.dark { }` block, not `@media (prefers-color-scheme: dark)` |
| **Reduced motion** | `@media (prefers-reduced-motion: reduce)` block present if page has animations |

## Common Mistakes

- **ELK layout** — #1 cause of blank diagrams
- **CSS variables in Mermaid classDef** — use hardcoded rgba/hex
- **`@media (prefers-color-scheme: dark)` instead of `html.dark`** — the theme toggle needs `html.dark`
- **Missing theme toggle** — every new page gets the nav + toggle
- **Missing dark mode mermaid init** — check `html.dark` class, not `matchMedia`
- **Unquoted Mermaid labels** — always `["Label"]` format
- **Missing zoom scripts** on diagram pages
- **Emoji** — never use emoji. Unicode/HTML entities only: `&#9788;` `&larr;` `&mdash;` `&#9679;`
- **`<body>` inside `<a>`** — malformed breadcrumb (`<body>larr; Portfolio Index`). Never include. The nav bar replaces this.

---

## Executive vs Technical Pages

When a topic needs both versions, build them as separate files. The executive page is not a "simplified" technical page — it's a fundamentally different frame.

### Side-by-side: same content, different frame

| Dimension | Executive | Technical |
|---|---|---|
| **Hero** | Outcome tagline, no tech stack | Technical tagline + stack pills with versions |
| **Primary question** | "What does this do for me?" | "How does this work?" |
| **Person** | You, your business, your team | The system, the pipeline, the agents |
| **Stage labels** | Benefit headlines | Component names + numbers |
| **Length** | ~4-8 sections, half the line count | Full detail, all components |
| **Section headings** | Sentence case, benefit-focused | Mono font, uppercase, technical |

### What executive pages REMOVE

Never include these on an executive page:

| Remove | Example of banned text | Why |
|---|---|---|
| Agent names/versions | "Claude Sonnet 4.5", "Instructions Agent v4.6" | Implementation detail, not a decision |
| Stage numbers | "Stage 3", "Phase 2A" | Process enumeration is noise to executives |
| Tool/library names | "Supabase", "SSE Streaming", "Playwright" | They don't care what database you used |
| Count chains | "5-agent pipeline", "11-dimension gap", "6-phase" | Reads as process bureaucracy, not capability |
| File paths / API refs | "`backend/engine/builder/`", "POST /api/builds" | Never on an exec page |
| Scoring formulas | "Tier 1 at 1.5x weight, veto at 75" | Replace with "safety enforced, cannot be overridden" |
| Technical nouns | "HITL checkpoint", "SSE streaming", "RLS" | Replace with what it accomplishes |

### What executive pages KEEP

| Keep | Example | Why |
|---|---|---|
| Human decisions | "A human must approve before work proceeds" | Accountability matters to executives |
| Business outcomes | "Reduce contract review from 14 days to 2 days" | They care about results |
| Risk language | "One AI safety incident can cost millions" | Risk is their language |
| Measurable results | "Portfolio health — how many projects, how fast they move" | They track metrics |
| Accountability | "Named sponsor, named owner — no single architect bottleneck" | Governance matters |
| Regulatory/board concerns | "When regulators ask, you have the documented trail" | Compliance is top of mind |

### The structural pattern

**Executive page** always uses this three-part rhythm per stage:
```
1. Benefit headline (h3 + outcome-line)
   "Know what you have before you automate it"
   "Stop building AI against assumptions. Start with how your organization actually works."

2. Why it matters (why paragraph)
   "Most AI projects fail because they solve the wrong problem..."

3. What you get / Why it matters (subpanels)
   "What you get: A single dashboard..."
   "Why it matters: Without this, you're guessing..."

4. Measured (metric-line)
   "↦ Measured: Portfolio health — how many projects, how fast they move..."
```

**Technical page** uses component-first organization:
```
1. Section heading (mono, uppercase)
   "PIPELINE — 10 STAGES"

2. Component cards (grid)
   Card: stage label + title + technical description
   "Stage 1: Discover — Structured interview with autonomy classification..."
```

### Pairs in the repo (study these)

| Executive | Technical | Topic |
|---|---|---|
| `portfolio/aesop-studio-overview.html` | `portfolio/aesop-studio-showcase.html` | Platform overview |
| `aesop/ai-maturity-model-executive.html` | `aesop/ai-maturity-model.html` | Maturity model |
| `aesop/smb-ai-adoption-roadmap-business.html` | `aesop/smb-ai-readiness-roadmap.html` | SMB roadmap |

### Language rewrite examples

| Technical text | Executive rewrite |
|---|---|
| "6-phase pipeline: Fitness Check, Gap Analysis (HITL checkpoint), Workflow Design, Write Instructions, Generate Artifacts, Summary" | "The build process writes the agent's instructions in the open. Before the agent is finalized, a human must approve — this is a hard stop, not a notification." |
| "Weighted multi-tier scoring with a hard safety/bias veto that makes critical failures unshippable" | "If an agent fails safety or bias checks, it cannot ship. This is enforced by the system, not left to human judgment." |
| "5-agent pipeline: Instructions, Ethos, Bias (1.5x), Safety (1.5x), Synthesis. Certification: Bronze → Platinum." | "Seven different evaluation methods test every agent before deployment. You get a certification badge and audit-ready reports." |
| "Organization context capture with WORE injection (Write Once Read Everywhere)" | "A living map of your organization that every subsequent AI project is grounded against." |

### Naming convention

```
[project]-[topic]-executive.html    ← executive version
[project]-[topic].html              ← technical version (default)
```

Or for portfolio pages:
```
[project]-overview.html             ← executive
[project]-showcase.html             ← technical
```

---

## Page Categorization

Where to put a new page and what section it belongs in:

| Page purpose | Folder | Index section | Example |
|---|---|---|---|
| Consulting / client-facing | `portfolio/` | Portfolio | Consultant offer, roadmap showcase |
| Platform architecture / pipeline | `aesop/` or `[project]/` | Project section (AESOP, TBG, etc.) | Architecture, decision flow |
| Audit / assessment | `aesop/` or `[project]/` | Relevant project subsection | UX audit, color audit |
| Standalone reference | `other/` | Other Projects | Decision tree, process map |
| Client deliverable | `[client]/` | Client section | Monday.com stages |

**When to create a new section:** a new client, a new platform, or 3+ pages on a topic that doesn't fit existing sections. Otherwise, add to the closest existing subsection.

### Brand Voice

I build things, write poetry, and don't talk like a whitepaper. Neither should these pages.

**Call out the bullshit.** Most AI governance is a policy nobody reads after week one. Say it. Don't wrap it in "organizations face challenges." If something is broken, say it's broken. If something is hard, say it's hard. The reader already knows — they'll trust you more for admitting it.

**Write like a human.** "You were told to 'Do AI!!!'" — that's how people actually talk. Not "Stakeholders have issued an AI mandate." Sentence fragments are fine. "No playbook, high expectations, real deadlines." That lands harder than a complete sentence ever would.

**The most important line is the shortest one on the page.** Build context, then land on a fragment that hits. "AESOP builds the controls into the pipeline — critical failures unshippable by design, and provable to the board." The punch doesn't have to be a complete sentence. It has to land.

**Lead with what they get, not what it is.** "You committed to AI. Now it has to land." Not "AESOP provides end-to-end AI lifecycle management." Nobody cares what the platform does. They care what it does *for them.*

**Borrow from places that aren't business books.** Military ("survives contact with production"), aviation ("land"), engineering ("go/no go gauge"), cooking, sports, gaming. Never borrow from a Gartner report. If it sounds like a Gartner report, kill it.

**Confidence, not hedging.** "AESOP owns the full lifecycle." Not "AESOP aims to address the full lifecycle." If it does the thing, say it does the thing. Cut these words: fairly, somewhat, tends to, typically, arguably, arguably.

**Words that never appear:** leverage, utilize, synergy, best-in-class, cutting-edge, revolutionary, empower, democratize (unless you mean actual democracy), journey, space (as in "the AI space"), ecosystem, holistic (unless you're talking about actual wholes), drive (as in "drive outcomes"), unlock (as in "unlock potential").

**"You" not "organizations."** "We" doesn't exist — it's "AESOP" or "the platform" or "you." Always address the person reading.

**Be generous, not sarcastic.** Humor that celebrates the reader's intelligence, never snark at someone else's expense. Quoting corporate absurdity is fair game ("'Do AI!!!'"). Punching down isn't.

**Index entries are one sentence.** What the page explains. No filler. The reader is scanning — give them the signal, skip the noise.

**When to be formal:** regulatory copy, security disclosures, technical specs. Even then, be precise. Not puffy. Precision isn't formality — it's care.

---

| Corporate default | This voice |
|---|---|
| "Our platform leverages AI to drive operational excellence" | "AESOP owns the full lifecycle — discovery upstream, governance and monitoring downstream" |
| "Stakeholders face challenges in AI adoption" | "You were told to 'Do AI!!!'" |
| "We provide comprehensive governance solutions" | "Most AI governance is a policy nobody follows" |
| "End-to-end lifecycle management" | "No blind spot survives contact with production" |
| "Accelerate time-to-value" | "Cut contract review from 14 days to 2 days" |
| "Best-in-class evaluation framework" | "If an agent fails safety or bias checks, it cannot ship. Not policy. Software." |

### Smart Brevity (Axios) — Executive Page Format

Executive pages follow Smart Brevity principles. These are not defaults for all pages — they apply to executive/overview pages where the reader is skimming.

**Core rules:**
1. **Muscle words** — lead with strongest language. Cut hedging ("fairly," "somewhat," "tends to").
2. **One point per item** — each stage makes one point. Three ideas = three stages, not one paragraph.
3. **Brevity is confidence** — padding signals uncertainty. Say less.

**The structure (already built into the executive template):**

| Smart Brevity element | Template element | Example |
|---|---|---|
| Punchy headline (≤6 words) | `.outcome-line` | "Stop building AI against assumptions" |
| One strong first sentence | `.why` first paragraph | "Most AI projects fail because they solve the wrong problem." |
| "Why it matters" | `.subpanel` second column | "Without this, you're guessing. With it, every AI investment is traceable." |
| "What you get" | `.subpanel` first column | "A single dashboard showing every AI project..." |
| Bullets over paragraphs | `<br>` in subpanels | Each deliverable on its own line |
| Bold labels for scanning | `<strong>` in subpanels | **What you get** **Why it matters** **↦ Measured:** |

**Formatting rules for executive pages:**
- **Bold the labels** — "What you get:", "Why it matters:", "↦ Measured:" — always bold so the reader can scan by jumping to labels
- **Design for the skimmer** — assume nobody reads every word; structure lets them jump to what they need
- **Short sentences, one idea each** — never bury two points in one sentence
- **Accessible words over fancy ones** — "use" not "utilize," "stop" not "discontinue," "signed" not "executed"
- **Respect time as the scarcest resource** — get to the point, tell them why they should care, let them decide how deep to go

**For technical pages specifically:**
- Precision matters — name the component, version, and why it was chosen
- Even technical descriptions should connect to what the choice accomplishes
- Don't separate the technical from the human — the same person writes both

## Accessibility Rules

### Color contrast (non-negotiable)
- All text must meet **WCAG AA** minimum: 4.5:1 for body text, 3:1 for large text (18px+)
- Gulf Stream Racing passes: `#0a1628` on `#eef4f9` = 14.1:1, `#3d5a7a` on `#eef4f9` = 6.3:1
- Dark mode: `#e8edf5` on `#0a1628` = 13.8:1, `#9bb0d4` on `#0a1628` = 6.1:1
- **Check custom schemes** — warm/earthy palettes often dip below threshold
- Never use `#7a9ab8` (muted text) on `#eef4f9` (bg) alone — it's 3.2:1, only use for decorative elements

### Color is never the only signal
- Status indicators need a shape or text label alongside color
- Links are underlined or have a distinct non-color affordance (border, background change on hover)
- Score badges include the number, not just green/amber/red

### Reduced motion
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; animation-delay: 0ms !important; }
}
```
Always include on every page with animations.

### Focus indicators
- Interactive elements (buttons, toggles, links) must have visible `:focus-visible` styles
- Theme toggle, zoom buttons, nav links — all need focus rings

## Page Naming Conventions

```
[project]-[topic]-[specific].html
```

Examples: `aesop-org-research-process.html`, `aesop-pipeline-flow.html`, `aesop-os-decision-flow.html`

- All lowercase, hyphens between words
- Project prefix for multi-project repos (aesop-, tbg-, monday-)
- No version numbers or dates in filenames
- Portfolio overview pages can use descriptive names: `consultant-offer.html`, `roadmap-showcase.html`

## SVG Icons (for index entries)

Inline SVG, 24x24 viewBox, stroke-based line art:
```html
<svg class="icon-svg" viewBox="0 0 24 24">
  <polyline points="4 17 10 11 14 15 20 9"/>  <!-- arrow/trend -->
  <polyline points="14 9 20 9 20 15"/>
</svg>
```
CSS: `stroke: var(--text-dim); fill: none; stroke-width: 1.5; stroke-linecap: round; stroke-linejoin: round;`

Match the icon to the page content — arrow for flows, grid for architecture, circle for overviews, document for audits.
