#!/usr/bin/env node
/**
 * validate-run.mjs — gate mecânico de qualidade de uma run do deep-strategic-planning.
 * Padrão runner (skills-ownership.md): valida o VERIFICÁVEL; nunca julga o cognitivo.
 *
 * Uso: node validate-run.mjs <run-dir> [--legacy]
 *   --legacy  runs pré-v1.1 (sem Red Team / Σ bruto / Robustness / predictions rígidas)
 */
import { readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { createRequire } from 'node:module';
const yaml = createRequire(import.meta.url)('js-yaml');

const dir = process.argv[2];
const LEGACY = process.argv.includes('--legacy');
if (!dir || !existsSync(dir)) { console.error('uso: validate-run.mjs <run-dir> [--legacy]'); process.exit(1); }

const fails = [], warns = [];
const ok = (c, msg) => (c ? null : fails.push(msg));
const read = f => existsSync(join(dir, f)) ? readFileSync(join(dir, f), 'utf8') : null;
const hasDigit = s => /\d/.test(String(s ?? ''));
const isDate = s => /^\d{4}-\d{2}-\d{2}/.test(String(s ?? ''));
const CONF = [0.6, 0.8, 0.95];

// 1. Artefatos obrigatórios
for (const f of ['01-crystal.md', '02-futures.md', '04-synthesis.md', '05-action-plan.md'])
  ok(read(f) !== null, `artefato ausente: ${f}`);

// 2. predictions.yaml (obrigatório desde v1.1; em --legacy é fail também — retroativo é exigido)
const predRaw = read('predictions.yaml');
ok(predRaw !== null, 'predictions.yaml ausente — sem ele a Phase 6 (re-bench) nunca roda');
if (predRaw) {
  let p; try { p = yaml.load(predRaw); } catch (e) { fails.push(`predictions.yaml inválido: ${e.message}`); }
  if (p) {
    ok(isDate(p.review_at), 'predictions: review_at ausente/sem data');
    ok(Array.isArray(p.predictions) && p.predictions.length >= 3, 'predictions: <3 previsões');
    for (const pr of p.predictions ?? []) {
      ok(isDate(pr.check_by), `prediction ${pr.id}: check_by sem data`);
      ok(hasDigit(pr.claim), `prediction ${pr.id}: claim sem número (métrica+comparador+valor)`);
      if (!LEGACY) {
        ok(CONF.includes(pr.confidence), `prediction ${pr.id}: confidence ausente ou fora de {0.6,0.8,0.95}`);
        ok(!!pr.source, `prediction ${pr.id}: source ausente (onde o dado será lido?)`);
      }
    }
    ok(Array.isArray(p.kill_switch) && p.kill_switch.length >= 1, 'kill_switch ausente');
    for (const k of p.kill_switch ?? [])
      ok(hasDigit(k.condition), `kill_switch sem número/data: "${String(k.condition).slice(0, 60)}..."`);
    ok(p.scores_snapshot && Object.keys(p.scores_snapshot).length > 0, 'scores_snapshot ausente (Phase 6 precisa dele para calibração)');
  }
}

// 3. Conteúdo estrutural (v1.1+)
if (!LEGACY) {
  const crystal = read('01-crystal.md') ?? '';
  ok(/red team/i.test(crystal), '01-crystal: Red Team de alternativas não documentado');
  const synth = read('04-synthesis.md') ?? '';
  ok(/Σ\s*bruto|pr[ée]-cap/i.test(synth), '04-synthesis: coluna Σ bruto pré-cap ausente (tie-break oficial)');
  ok(/robust/i.test(synth), '04-synthesis: Robustness Check não documentado');
  const plan = read('05-action-plan.md') ?? '';
  ok(/antifr[áa]gil/i.test(plan), '05-action-plan: Posição Antifrágil Mínima ausente');
} else {
  warns.push('modo --legacy: checks estruturais v1.1+ pulados (Red Team, Σ bruto, Robustness, Antifrágil)');
}

for (const w of warns) console.warn(`WARN  ${w}`);
if (fails.length) { for (const f of fails) console.error(`FAIL  ${f}`); console.error(`\n${fails.length} falha(s) — run não finaliza.`); process.exit(1); }
console.log(`PASS  run válida (${LEGACY ? 'legacy' : 'v1.1+'}) — gate mecânico ok`);
