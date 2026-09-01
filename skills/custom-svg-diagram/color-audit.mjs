// color-audit.mjs — WCAG contrast + coherence check for the role palette.
//
//   node color-audit.mjs [palette]      palette = a name (blueprint|warm|mono) or a .json path
//
// With no arg it audits the default blueprint palette in both themes. Pass a
// named palette from palette.mjs, or a JSON file, to audit any color set.
// Reports, per role and theme:
//   - title color vs box background   (needs ≥ 3:1; 4.5:1 is safer)
//   - sub-text color vs box background (needs ≥ 4.5:1)
//   - text vs page background
// Plus a colorblind-safety pass (advisory). Exits non-zero on any contrast failure.

import { readFileSync } from 'fs';
import { palettes } from './palette.mjs';

let palette = palettes.blueprint;
const arg = process.argv[2];
if (arg) {
  palette = palettes[arg] || (arg.endsWith('.json') ? JSON.parse(readFileSync(arg, 'utf8')) : undefined);
  if (!palette) { console.error(`Unknown palette '${arg}'. Have: ${Object.keys(palettes).join(', ')} or a .json path.`); process.exit(1); }
}

const lum = hex => {
  const c = [1, 3, 5].map(i => parseInt(hex.slice(i, i + 2), 16) / 255).map(v => v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4);
  return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2];
};
const contrast = (a, b) => { const la = lum(a), lb = lum(b); const [l1, l2] = la > lb ? [la, lb] : [lb, la]; return (l1 + 0.05) / (l2 + 0.05); };
const blend = (fg, bg, op) => [1, 3, 5].map(i => Math.round(parseInt(fg.slice(i, i + 2), 16) * op + parseInt(bg.slice(i, i + 2), 16) * (1 - op)))
  .reduce((s, v) => s + v.toString(16).padStart(2, '0'), '#');
const fmt = c => c.toFixed(2).padStart(5);


const deuteranopia = hex => {
  const c = [1, 3, 5].map(i => parseInt(hex.slice(i, i + 2), 16));
  return [0.625 * c[0] + 0.375 * c[1], 0.7 * c[0] + 0.3 * c[1], 0.3 * c[1] + 0.7 * c[2]];
};
const dist = (a, b) => Math.hypot(a[0] - b[0], a[1] - b[1], a[2] - b[2]);

let fail = 0;
for (const theme of ['light', 'dark']) {
  const t = palette[theme];
  console.log(`\n${theme.toUpperCase()} theme`);
  console.log('  role       title vs box   sub vs box');
  for (const [name, role] of Object.entries(t.roles)) {
    const boxBg = blend(role, t.surface, t.dim);
    const title = contrast(role, boxBg);       // role-colored title on tinted box
    const sub = contrast(t.textDim, boxBg);     // sub-text on tinted box
    const titleOk = title >= 3, subOk = sub >= 4.5;
    if (!titleOk || !subOk) fail++;
    console.log(`  ${name.padEnd(9)} ${fmt(title)}${titleOk ? '  ok ' : '  LOW'}  ${fmt(sub)}${subOk ? '  ok' : '  LOW'}`);
  }
  const bodyOk = contrast(t.text, t.surface) >= 4.5;
  if (!bodyOk) fail++;
  console.log(`  body text vs surface: ${fmt(contrast(t.text, t.surface))} ${bodyOk ? 'ok' : 'LOW'}`);
}
// Colorblind-safety is advisory: the real mitigation is redundant encoding
// (the per-role patterns in layout.mjs), not forcing the palette apart. Surface
// pairs that blur under deuteranopia but don't fail the gate.
console.log('\nColorblind-safety (deuteranopia simulation, advisory):');
for (const theme of ['light', 'dark']) {
  const t = palette[theme];
  const roles = Object.entries(t.roles).map(([name, hex]) => [name, deuteranopia(hex)]);
  const close = [];
  for (let i = 0; i < roles.length; i++) for (let j = i + 1; j < roles.length; j++) {
    if (dist(roles[i][1], roles[j][1]) < 60) close.push([roles[i][0], roles[j][0]]);
  }
  if (close.length) {
    console.log(`  ${theme}: roles that may blur together (patterns carry the distinction):`);
    close.forEach(([a, b]) => console.log(`    - ${a} vs ${b}`));
  } else {
    console.log(`  ${theme}: roles stay distinct under simulation.`);
  }
}
console.log(fail ? `\n${fail} failures — tune the palette.` : '\nAll checks pass.');
process.exit(fail ? 1 : 0);
