// check.mjs — one command to validate any diagram end to end.
//
//   node check.mjs <diagram.html> [executablePath]
//
// Runs the full gate: geometric correctness (arrows connect, no crossings,
// no through-box, no text on lines) plus palette contrast (color-audit).
// Prints a per-check pass/fail and exits non-zero if any check fails.

import { execSync } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname, join, resolve } from 'path';

const here = dirname(fileURLToPath(import.meta.url));
const file = process.argv[2];
const exe = process.argv[3];
if (!file) { console.error('Usage: node check.mjs <diagram.html> [executablePath]'); process.exit(1); }

const run = (cmd) => { try { execSync(cmd, { stdio: 'pipe', encoding: 'utf8' }); return { ok: true }; } catch (e) { return { ok: false, out: e.stdout }; } };

const exeArg = exe ? JSON.stringify(exe) : '';
const verify = run(`node ${join(here, 'verify.mjs')} ${JSON.stringify(resolve(file))} ${exeArg}`);
const color = run(`node ${join(here, 'color-audit.mjs')}`);

console.log(`\nDiagram: ${resolve(file)}\n`);
console.log(`  [geometry] verify.mjs      ${verify.ok ? 'PASS' : 'FAIL'}`);
if (!verify.ok) console.log(verify.out || '');
console.log(`  [color]    color-audit.mjs ${color.ok ? 'PASS' : 'FAIL'}`);
if (!color.ok) console.log(color.out || '');

if (verify.ok && color.ok) { console.log('\nAll checks pass.\n'); process.exit(0); }
console.log('\nFAIL: fix the failing check(s).\n'); process.exit(1);
