import { lstat, readdir, readFile } from "node:fs/promises";
import path from "node:path";
import process from "node:process";

const root = process.cwd();
const catalog = JSON.parse(await readFile(path.join(root, "catalog.json"), "utf8"));
const errors = [];

async function directoryNames(relativePath) {
  const entries = await readdir(path.join(root, relativePath), { withFileTypes: true });
  return entries.filter((entry) => entry.isDirectory()).map((entry) => entry.name).sort();
}

function compareLists(label, actual, expected) {
  const actualJson = JSON.stringify(actual);
  const expectedJson = JSON.stringify([...expected].sort());
  if (actualJson !== expectedJson) {
    errors.push(`${label}: catálogo e filesystem divergem`);
  }
}

const actualSkills = await directoryNames(".claude/skills");
const actualSquads = await directoryNames("squads");
compareLists("skills", actualSkills, catalog.skills);
compareLists("squads", actualSquads, catalog.squads);

for (const skill of catalog.skills) {
  const skillFile = path.join(root, ".claude", "skills", skill, "SKILL.md");
  try {
    const content = await readFile(skillFile, "utf8");
    if (!content.startsWith("---") || !/^name:/m.test(content)) {
      errors.push(`skill inválida: ${skill}/SKILL.md sem frontmatter mínimo`);
    }
  } catch {
    errors.push(`skill ausente: ${skill}/SKILL.md`);
  }
}

for (const squad of catalog.squads) {
  const configFile = path.join(root, "squads", squad, "config.yaml");
  try {
    const content = await readFile(configFile, "utf8");
    if (!/^pack:\s*$/m.test(content) || !/^  name:\s*\S/m.test(content)) {
      errors.push(`squad inválido: ${squad}/config.yaml sem pack.name`);
    }
  } catch {
    errors.push(`squad ausente: ${squad}/config.yaml`);
  }
}

const forbiddenSegments = new Set(catalog.excluded_patterns);
const forbiddenFilePatterns = [
  /\.pyc$/,
  /\.local\.ya?ml$/,
];
const secretFixtureAllowlist = new Set(catalog.secret_fixture_allowlist);
const secretMarkers = [
  /-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----/,
  /\bAKIA[0-9A-Z]{16}\b/,
  /\bghp_[A-Za-z0-9]{30,}\b/,
];
let fileCount = 0;

async function walk(currentPath, relativePath = "") {
  for (const entry of await readdir(currentPath, { withFileTypes: true })) {
    if (relativePath === "" && entry.name === ".git") continue;
    const nextRelative = path.join(relativePath, entry.name);
    const nextPath = path.join(currentPath, entry.name);
    const stats = await lstat(nextPath);
    if (stats.isSymbolicLink()) {
      errors.push(`symlink não permitido: ${nextRelative}`);
      continue;
    }
    const segments = nextRelative.split(path.sep);
    if (segments.some((segment) => forbiddenSegments.has(segment))) {
      errors.push(`caminho excluído presente: ${nextRelative}`);
    }
    if (forbiddenFilePatterns.some((pattern) => pattern.test(entry.name))) {
      errors.push(`arquivo local/cache presente: ${nextRelative}`);
    }
    if (stats.isDirectory()) {
      await walk(nextPath, nextRelative);
      continue;
    }
    fileCount += 1;
    if (stats.size <= 2_000_000) {
      const content = await readFile(nextPath);
      const text = content.toString("utf8");
      if (
        !secretFixtureAllowlist.has(nextRelative) &&
        secretMarkers.some((marker) => marker.test(text))
      ) {
        errors.push(`possível segredo em: ${nextRelative}`);
      }
    }
  }
}

await walk(root);

if (errors.length > 0) {
  console.error(`Falha de validação (${errors.length}):`);
  for (const error of errors) console.error(`- ${error}`);
  process.exit(1);
}

console.log(`OK: ${actualSkills.length} skills, ${actualSquads.length} squads, ${fileCount} arquivos.`);
