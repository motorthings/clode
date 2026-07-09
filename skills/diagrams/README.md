# Diagrams Skill — README

This skill teaches Claude how to build pages for the `motorthings/diagrams` GitHub Pages site. If you're reading this as a human, here's what each part does and why it exists.

## What a skill is

A skill is a file (or folder) in `~/.claude/skills/` that tells Claude how to do something specific. Claude reads it when the task matches — like a standard operating procedure. When you say "add a page to my diagrams collection" or Claude detects you're working in the diagrams repo, it reads this skill and follows the instructions.

## How this skill is structured

### `SKILL.md` — the main instruction file

This is the file Claude reads. It's organized as a build manual:

1. **Frontmatter (YAML header)** — The ID card. The `description` field tells Claude *when* to trigger this skill. The `metadata` fields say where the repo lives on disk and where it deploys.

2. **Design System Reference** — The visual spec. Fonts (Fraunces + Source Code Pro), colors (Gulf Stream Racing = orange + blue + teal), layout measurements (1000px vs 920px containers), backgrounds (dual vs single gradient). Everything the skill builds depends on these numbers.

3. **Three Layout Modes** — The decision matrix for what kind of page to build:
   - **Mode 1: Diagram page** — Mermaid flowchart + supporting cards. Full template at `references/template-diagram.html`.
   - **Mode 2: Pure CSS flowchart** — Vertical A→B→C steps with Unicode arrows. No JavaScript. The CSS lives inline because it's component patterns, not a full page template.
   - **Mode 3: Portfolio overview** — Numbered stages with "What you get / Why it matters" subpanels. Full template at `references/template-portfolio.html`.

4. **Mermaid Rules** — Non-negotiable rules learned the hard way. ELK layout = blank diagrams on GitHub Pages. Mermaid can't read CSS variables so colors must be hardcoded. Every label must be quoted.

5. **Linking Strategy** — How pages connect to each other. Backlinks are parent-relative (nested pages link to their parent, not the main index). Index entries use collapsible sections + line layout, never card grids.

6. **Workflow** — The 8-step build checklist. The key step: delegate HTML generation to the **visual-explainer** skill, passing 7 specific overrides (colors, fonts, theme toggle, no ELK, etc.). Then add backlinks, add to the index, run the 11-point verification checklist.

7. **Executive vs Technical Pages** — The deepest section because it's the most common mistake. An executive page isn't a "simplified" technical page — it's a different frame. Includes a removal checklist (what must not appear on exec pages), a keep list (what execs actually care about), the structural pattern (headline → why → what you get/why it matters → measured), and rewrite examples.

8. **Brand Voice** — Written in the voice it's describing. First person, direct, no corporate language. Includes a banned-words list (leverage, utilize, synergy, ecosystem, journey, empower) and a comparison table of corporate → voice rewrites.

9. **Smart Brevity** — Axios's methodology, applied to executive pages. The template structure already maps to Smart Brevity elements (`.outcome-line` = headline, `.subpanel` = "Why it matters").

10. **The rest** — Accessibility rules (WCAG AA contrast, reduced motion, focus indicators), page categorization (where to put new files), naming conventions (`[project]-[topic]-[specific].html`), and SVG icon patterns for the index.

### `references/` — full HTML templates

Two complete page templates that Claude reads (doesn't memorize):

- `template-diagram.html` — Mode 1: Mermaid diagram page with hero badge, zoom controls, context cards, phase cards, callout, all three JS blocks
- `template-portfolio.html` — Mode 3: Executive overview page with numbered stages, subpanels, metric lines, outcome grid

These were extracted from the skill to keep `SKILL.md` lean. Claude reads the file each time it builds a page rather than copying from memory.

## How the skill gets triggered

Claude checks the `description` in the frontmatter to decide when to read this skill. It triggers when:

- You're working in the `/Users/motorthings/Documents/Vault/GitHub/diagrams` repo
- You ask to add a page, diagram, or visual explainer to your portfolio
- You mention `motorthings.github.io/diagrams`
- You ask about diagrams conventions (colors, backlinks, voice)

The skill delegates HTML generation to the **visual-explainer** skill (a third-party skill by nicobailon). This skill provides the repo-specific rules and overrides; visual-explainer provides the HTML/CSS/JS construction engine.

## How to invoke it manually

Type `/diagrams` in Claude Code, or say something like "add a page to my diagrams collection" or "build a visual explainer for the AESOP pipeline."

## How to update it

The skill lives at `~/.claude/skills/diagrams/`. Edit `SKILL.md` to change the rules. Edit files in `references/` to update the templates. Changes take effect the next time the skill is triggered — no restart needed.
