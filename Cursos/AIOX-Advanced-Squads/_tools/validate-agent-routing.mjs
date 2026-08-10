import { readFile, readdir } from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";

const toolsDir = path.dirname(fileURLToPath(import.meta.url));
const course = path.resolve(toolsDir, "..");
const root = path.resolve(course, "../..");
const errors = [];

async function read(relativePath) {
  return readFile(path.join(root, relativePath), "utf8");
}

async function exists(relativePath) {
  try {
    await read(relativePath);
    return true;
  } catch {
    return false;
  }
}

function normalize(value) {
  return value
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase();
}

function scoreRoute(prompt, route) {
  const normalized = normalize(prompt);
  let score = 0;
  for (const signal of route.signals) {
    const candidate = normalize(signal);
    if (normalized.includes(candidate)) score += 10 + candidate.split(/\s+/).length;
  }
  for (const alias of route.aliases) {
    const candidate = normalize(alias);
    if (normalized.includes(candidate)) score += 8 + candidate.split(/\s+/).length;
  }
  for (const signal of route.anti_signals) {
    const candidate = normalize(signal);
    if (normalized.includes(candidate)) score -= 12 + candidate.split(/\s+/).length;
  }
  return score;
}

const courseRouterPath = "Cursos/AIOX-Advanced-Squads/agent-router.json";
const skillRouterPath = "skills/aiox-squads/references/router.json";
const evalsPath = "Cursos/AIOX-Advanced-Squads/_tools/routing-evals.json";

const [courseRouterText, skillRouterText, evalsText, catalogText] = await Promise.all([
  read(courseRouterPath),
  read(skillRouterPath),
  read(evalsPath),
  read("catalog.json"),
]);

if (courseRouterText !== skillRouterText) {
  errors.push("roteador do curso diverge da cópia autocontida da skill aiox-squads");
}

const router = JSON.parse(courseRouterText);
const evals = JSON.parse(evalsText);
const catalog = JSON.parse(catalogText);
const routeIds = router.routes.map((route) => route.id);

if (router.route_count !== 24 || router.routes.length !== 24) {
  errors.push(`roteador deve ter 24 rotas; recebeu ${router.routes.length}`);
}
if (new Set(routeIds).size !== routeIds.length) {
  errors.push("roteador contém ids duplicados");
}
if (JSON.stringify([...routeIds].sort()) !== JSON.stringify([...catalog.squads].sort())) {
  errors.push("roteador e catálogo divergem na cobertura dos squads");
}

for (const runtime of ["codex", "claude_code", "generic"]) {
  if (!router.runtime_contracts?.[runtime]) errors.push(`contrato de runtime ausente: ${runtime}`);
}

const requiredFields = [
  "id",
  "title",
  "lesson",
  "squad_path",
  "entry_agent",
  "entry_agent_path",
  "maturity",
  "signals",
  "anti_signals",
  "inputs",
  "deliverable",
  "evidence",
  "limits",
  "generic_prompt",
];

for (const route of router.routes) {
  for (const field of requiredFields) {
    if (route[field] === undefined || route[field] === null || route[field].length === 0) {
      errors.push(`${route.id}: campo obrigatório vazio ${field}`);
    }
  }
  if (route.squad_path !== `squads/${route.id}`) {
    errors.push(`${route.id}: squad_path não canônico`);
  }
  if (!(await exists(`${route.squad_path}/config.yaml`))) {
    errors.push(`${route.id}: config do squad ausente`);
  }
  if (!(await exists(route.entry_agent_path))) {
    errors.push(`${route.id}: agente de entrada ausente em ${route.entry_agent_path}`);
  }
  if (!(await exists(`Cursos/AIOX-Advanced-Squads/${route.lesson}`))) {
    errors.push(`${route.id}: aula ausente em ${route.lesson}`);
  } else {
    const lesson = await read(`Cursos/AIOX-Advanced-Squads/${route.lesson}`);
    if (!new RegExp(`^squad:\\s*${route.id}\\s*$`, "m").test(lesson)) {
      errors.push(`${route.id}: frontmatter da aula não confirma o squad`);
    }
  }
  if (route.skill && !(await exists(`skills/${route.skill}/SKILL.md`))) {
    errors.push(`${route.id}: skill declarada ausente: ${route.skill}`);
  }
  if (route.maturity !== catalog.squad_meta?.[route.id]?.maturity) {
    errors.push(`${route.id}: maturity diverge do catálogo`);
  }
  if (!route.generic_prompt.includes(`${route.squad_path}/config.yaml`)) {
    errors.push(`${route.id}: prompt genérico não carrega a config do squad`);
  }
  if (!route.generic_prompt.includes(route.entry_agent_path)) {
    errors.push(`${route.id}: prompt genérico não carrega o agente de entrada`);
  }
}

for (const bootstrap of ["AGENTS.md", "CLAUDE.md"]) {
  if (!(await exists(bootstrap))) {
    errors.push(`bootstrap ausente: ${bootstrap}`);
    continue;
  }
  const content = await read(bootstrap);
  for (const expected of ["AGENT-GUIDE.md", "agent-router.json"]) {
    if (!content.includes(expected)) errors.push(`${bootstrap}: não referencia ${expected}`);
  }
}

for (const skillFile of [
  "skills/aiox-squads/SKILL.md",
  "skills/aiox-squads/agents/openai.yaml",
]) {
  if (!(await exists(skillFile))) errors.push(`arquivo da skill ausente: ${skillFile}`);
}
const skillText = await read("skills/aiox-squads/SKILL.md");
if (!/^name:\s*aiox-squads\s*$/m.test(skillText)) errors.push("skill aiox-squads sem name válido");
if (!/^description:\s*\S/m.test(skillText)) errors.push("skill aiox-squads sem description acionável");
if (skillText.includes("TODO")) errors.push("skill aiox-squads ainda contém TODO");
if (!skillText.includes("references/router.json")) errors.push("skill não referencia seu roteador");

const actualSkills = (await readdir(path.join(root, "skills"), { withFileTypes: true }))
  .filter((entry) => entry.isDirectory())
  .map((entry) => entry.name)
  .sort();
if (catalog.counts?.skills !== actualSkills.length) {
  errors.push(`catalog.counts.skills=${catalog.counts?.skills}; filesystem=${actualSkills.length}`);
}
if (JSON.stringify(actualSkills) !== JSON.stringify([...catalog.skills].sort())) {
  errors.push("catálogo e filesystem divergem nas skills");
}

const supplemental = catalog.supplemental_courses?.find(
  (item) => item.path === "Cursos/AIOX-Advanced-Squads",
);
const markdownFiles = [];
async function collectMarkdown(directory) {
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const target = path.join(directory, entry.name);
    if (entry.isDirectory()) await collectMarkdown(target);
    else if (entry.name.endsWith(".md")) markdownFiles.push(target);
  }
}
await collectMarkdown(course);
if (supplemental?.markdown_files !== markdownFiles.length) {
  errors.push(
    `catálogo registra ${supplemental?.markdown_files} Markdown no curso; filesystem=${markdownFiles.length}`,
  );
}

const evalCoverage = new Set();
for (const testCase of evals.cases) {
  if (!routeIds.includes(testCase.expected)) {
    errors.push(`${testCase.id}: rota esperada inexistente ${testCase.expected}`);
    continue;
  }
  evalCoverage.add(testCase.expected);
  const ranked = router.routes
    .map((route) => ({ id: route.id, score: scoreRoute(testCase.prompt, route) }))
    .sort((a, b) => b.score - a.score || a.id.localeCompare(b.id));
  if (ranked[0].score <= 0) {
    errors.push(`${testCase.id}: nenhum sinal positivo encontrado`);
  } else if (ranked[0].id !== testCase.expected) {
    errors.push(
      `${testCase.id}: esperado=${testCase.expected}; roteador=${ranked[0].id}; score=${ranked[0].score}`,
    );
  } else if (ranked[1]?.score === ranked[0].score) {
    errors.push(`${testCase.id}: empate entre ${ranked[0].id} e ${ranked[1].id}`);
  }
  for (const forbidden of testCase.forbidden || []) {
    if (ranked[0].id === forbidden) errors.push(`${testCase.id}: selecionou rota proibida ${forbidden}`);
  }
}

for (const routeId of routeIds) {
  if (!evalCoverage.has(routeId)) errors.push(`sem caso comportamental para ${routeId}`);
}

const absoluteMachinePath = /(?:\/Users\/|\/home\/|C:\\Users\\|C:\/Users\/)/;
for (const [label, content] of [
  [courseRouterPath, courseRouterText],
  [skillRouterPath, skillRouterText],
  [evalsPath, evalsText],
]) {
  if (absoluteMachinePath.test(content)) errors.push(`${label}: contém path absoluto de máquina`);
}

console.log(
  `Agent routing: ${router.routes.length}/24 rotas, ${evals.cases.length} casos, ${evalCoverage.size}/24 squads cobertos`,
);
console.log(`Erros: ${errors.length}`);
for (const error of errors) console.log(`ERROR ${error}`);
if (errors.length) process.exit(1);
