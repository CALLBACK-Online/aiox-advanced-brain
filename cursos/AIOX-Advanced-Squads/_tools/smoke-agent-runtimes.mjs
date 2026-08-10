#!/usr/bin/env node

import { spawnSync } from "node:child_process";
import { mkdtempSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "../../..");
const timeout = Number(process.env.AIOX_RUNTIME_SMOKE_TIMEOUT_MS || 180000);
const selected = new Set(process.argv.slice(2));
const runClaude = selected.size === 0 || selected.has("claude");
const runCodex = selected.size === 0 || selected.has("codex");

if (![...selected].every((runtime) => ["claude", "codex"].includes(runtime))) {
  console.error("Uso: npm run smoke:routing:runtimes -- [claude|codex]");
  process.exit(2);
}

if (!Number.isFinite(timeout) || timeout < 1000) {
  console.error("AIOX_RUNTIME_SMOKE_TIMEOUT_MS deve ser um número >= 1000.");
  process.exit(2);
}

function execute(runtime, args) {
  const result = spawnSync(runtime, args, {
    cwd: root,
    encoding: "utf8",
    maxBuffer: 20 * 1024 * 1024,
    timeout,
  });

  if (result.error) {
    throw new Error(`${runtime}: ${result.error.message}`);
  }

  if (result.status !== 0) {
    throw new Error(
      `${runtime}: exit ${result.status}\n${result.stderr || result.stdout}`.trim(),
    );
  }

  return result.stdout;
}

function assertResponse(runtime, response, checks) {
  const missing = checks.filter(({ pattern }) => !pattern.test(response));
  if (missing.length > 0) {
    throw new Error(
      `${runtime}: resposta não cumpriu ${missing.map(({ label }) => label).join(", ")}\n${response}`,
    );
  }
  console.log(`OK ${runtime}: ${checks.map(({ label }) => label).join(", ")}`);
}

try {
  if (runClaude) {
    const prompt =
      "Meu processo já foi validado e agora quero materializá-lo no ClickUp, com Spaces, Lists, Fields e automações. Qual squad devo usar e como começar? Responda concisamente em PT-BR e não altere arquivos.";
    const response = execute("claude", [
      "-p",
      prompt,
      "--setting-sources",
      "project",
      "--model",
      process.env.CLAUDE_SMOKE_MODEL || "haiku",
      "--permission-mode",
      "bypassPermissions",
      "--no-session-persistence",
      "--output-format",
      "text",
      "--max-budget-usd",
      process.env.CLAUDE_SMOKE_BUDGET_USD || "0.75",
      "--tools",
      "Read",
      "Grep",
      "Glob",
    ]);
    assertResponse("Claude Code", response, [
      { label: "squad", pattern: /Squad escolhido:.*ClickUp[ -]Ops/is },
      { label: "fronteira", pattern: /AIOX SOP/i },
      { label: "maturidade", pattern: /Maturidade:/i },
      { label: "briefing", pattern: /Briefing/i },
      { label: "evidência", pattern: /Evidência/i },
    ]);
  }

  if (runCodex) {
    const temporaryDirectory = mkdtempSync(resolve(tmpdir(), "aiox-routing-smoke-"));
    const outputPath = resolve(temporaryDirectory, "codex-final.txt");
    try {
      const prompt =
        "Quero extrair as regras de negócio escondidas em um sistema brownfield; não preciso mapear a arquitetura inteira. Qual squad devo usar e como começo? Responda concisamente em PT-BR e não altere arquivos.";
      execute("codex", [
        "exec",
        "-C",
        root,
        "-s",
        "read-only",
        "--ephemeral",
        "--ignore-user-config",
        "-c",
        'model_reasoning_effort="low"',
        "--output-last-message",
        outputPath,
        prompt,
      ]);
      const response = readFileSync(outputPath, "utf8");
      assertResponse("Codex", response, [
        { label: "squad", pattern: /Squad escolhido:.*domain-decoder/is },
        { label: "fronteira", pattern: /code-anatomist/i },
        { label: "maturidade", pattern: /Maturidade:/i },
        { label: "ativação", pattern: /decoder-chief/i },
        { label: "evidência", pattern: /Evidência/i },
      ]);
    } finally {
      rmSync(outputPath, { force: true });
      rmSync(temporaryDirectory, { recursive: true, force: true });
    }
  }
} catch (error) {
  console.error(error.message);
  process.exit(1);
}
