// palette.mjs — swappable color sets for diagrams.
//
// The SVG emitted by layout.mjs references CSS variables (--slate, --slate-dim,
// --surface, --text, …). A palette is a set of those variables in light + dark.
// Define a palette here, then emit its CSS with cssFor(name) and drop it into
// the page. Switch color sets by swapping the CSS, not the diagram code.
//
//   import { cssFor, palettes } from './palette.mjs';
//   const css = cssFor('blueprint');   // :root { … } html.dark { … }
//
// Every palette must define the role colors the skill uses: slate, secondary,
// primary, violet, amber, good (and their -dim variants). Validate any palette
// (named or custom) with color-audit.mjs before shipping it.

const hex2rgb = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16));
const mix = (a, b, t) => { const A = hex2rgb(a), B = hex2rgb(b); return A.map((v, i) => Math.round(v + (B[i] - v) * t)); };
const rgb = c => `rgb(${c[0]}, ${c[1]}, ${c[2]})`;
const rgba = (h, o) => { const c = hex2rgb(h); return `rgba(${c[0]}, ${c[1]}, ${c[2]}, ${o})`; };

export const palettes = {
  // Default technical palette — 4 semantic categories: storage / compute / model / consumer.
  blueprint: {
    light: { surface: '#ffffff', bg: '#f4f6fb', text: '#16213a', textDim: '#4a5b7c', dim: 0.09,
      roles: { storage: '#3b4fd8', compute: '#0891b2', model: '#6d28d9', consumer: '#0f766e' } },
    dark: { surface: '#111b30', bg: '#0b1220', text: '#e6ecf7', textDim: '#93a5c8', dim: 0.13,
      roles: { storage: '#7d8dff', compute: '#22d3ee', model: '#a78bfa', consumer: '#5eead4' } },
  },

  // Warm editorial palette.
  warm: {
    light: { surface: '#fffdf9', bg: '#faf5ed', text: '#2b2116', textDim: '#6f6150', dim: 0.11,
      roles: { storage: '#7a6a58', compute: '#2f7d5f', model: '#7a5ca8', consumer: '#3d7d52' } },
    dark: { surface: '#261e14', bg: '#1a140d', text: '#f2e9dc', textDim: '#b6a791', dim: 0.16,
      roles: { storage: '#b39c82', compute: '#72c9a4', model: '#c2a6e8', consumer: '#8fd0a5' } },
  },

  // Grayscale (color-blind-safe; categories differ by shade).
  mono: {
    light: { surface: '#ffffff', bg: '#f4f5f7', text: '#16181d', textDim: '#2e333a', dim: 0.16,
      roles: { storage: '#30353c', compute: '#3d434c', model: '#454b53', consumer: '#262b31' } },
    dark: { surface: '#14161b', bg: '#0d0f13', text: '#e6e8ee', textDim: '#b3b9c2', dim: 0.24,
      roles: { storage: '#aeb4bd', compute: '#9aa0ab', model: '#d8dbdf', consumer: '#b9bec6' } },
  },
};

const themeCss = (sel, t) => {
  const roleKeys = Object.keys(t.roles);
  return [
    `${sel}:root {`,
    `  --surface: ${t.surface}; --surface2: ${rgb(mix(t.surface, t.text, 0.05))}; --border-bright: ${rgb(mix(t.surface, t.text, 0.20))};`,
    `  --bg: ${t.bg}; --text: ${t.text}; --text-dim: ${rgb(mix(t.text, t.surface, 0.30))}; --text-muted: ${rgb(mix(t.text, t.surface, 0.54))};`,
    ...roleKeys.map(r => `  --${r}: ${t.roles[r]}; --${r}-dim: ${rgba(t.roles[r], t.dim)};`),
    `}`,
  ].join('\n');
};

// cssFor(nameOrPalette) → ":root { … } html.dark { … }" to drop into the page.
export function cssFor(nameOrPalette) {
  const p = typeof nameOrPalette === 'string' ? palettes[nameOrPalette] : nameOrPalette;
  if (!p) throw new Error(`Unknown palette: ${nameOrPalette}. Have: ${Object.keys(palettes).join(', ')}`);
  return themeCss('', p.light) + '\n' + themeCss('html.dark', p.dark);
}
