#!/usr/bin/env python3
"""Auditoria de links no estilo Obsidian sobre o acervo (vault = root ou pasta).

Resolve:
  - Markdown relativo `[](path.md)` — como o harness de curso
  - Wikilinks `[[Nota]]` / `[[path/Nota|alias]]` — por **stem** (basename) no vault,
    como o Graph/backlinks do Obsidian (skill `obsidian-course-vault`)

Não substitui `dev/validate.py` (autocontenção por curso). Complementa improve/analyze
com visão de grafo: quebrados, não resolvidos, colisões de stem e órfãos.

Saída: markdown no bastidor ou stdout.
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from urllib.parse import unquote

from course_common import find_root, resolve_course

MD_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
WIKILINK = re.compile(r"\[\[([^\]]+)\]\]")
SKIP_DIRS = {
    ".git",
    "node_modules",
    ".obsidian",
    "__pycache__",
    "docs",
    "dev",
    "dist",
    ".claude",
    ".agents",
    ".codex",
}
# placeholders / exemplos didáticos de wikilink (não são dívida do grafo)
PLACEHOLDER_WIKI = re.compile(
    r"^(?:\.\.\.|…|Nome da nota|nota|temp|\d+|\{[^}]*\}|:space:|wikilinks)$",
    re.I,
)


def iter_markdown(vault: Path, *, include_notas: bool = False) -> list[Path]:
    files: list[Path] = []
    skip = set(SKIP_DIRS)
    if not include_notas:
        skip.add("notas")
    for path in vault.rglob("*.md"):
        if any(part in skip for part in path.parts):
            continue
        files.append(path)
    return sorted(files)


def build_stem_index(files: list[Path], vault: Path) -> tuple[dict[str, list[Path]], dict[str, Path]]:
    """stem -> all paths; stem -> preferred path (first by path sort)."""
    by_stem: dict[str, list[Path]] = defaultdict(list)
    for path in files:
        by_stem[path.stem].append(path)
    preferred = {stem: paths[0] for stem, paths in by_stem.items()}
    return by_stem, preferred


def parse_wikilink(raw: str) -> str:
    target = raw.split("|", 1)[0].split("#", 1)[0].strip()
    return target


def resolve_wikilink(
    target: str,
    source: Path,
    vault: Path,
    preferred: dict[str, Path],
    by_stem: dict[str, list[Path]],
) -> tuple[str, Path | None]:
    """Return (status, resolved_path). status: ok|collision|missing|empty."""
    if not target:
        return "empty", None
    # Path-like wikilink
    if "/" in target or target.endswith(".md"):
        candidate = (source.parent / target).resolve() if not target.startswith("/") else (vault / target.lstrip("/")).resolve()
        # also try relative to vault root
        alt = (vault / target).resolve()
        for cand in (candidate, alt):
            try:
                cand.relative_to(vault.resolve())
            except ValueError:
                continue
            if cand.exists():
                return "ok", cand
            if cand.with_suffix(".md").exists():
                return "ok", cand.with_suffix(".md")
        # fall through to stem of last segment
        stem = Path(target).stem
    else:
        stem = target
    paths = by_stem.get(stem, [])
    if not paths:
        return "missing", None
    if len(paths) > 1:
        return "collision", preferred.get(stem)
    return "ok", paths[0]


def resolve_md_link(raw: str, source: Path, vault: Path) -> tuple[str, Path | None]:
    target = raw.split("#", 1)[0].strip()
    if not target or target.startswith(("http://", "https://", "mailto:")):
        return "external", None
    resolved = (source.parent / unquote(target)).resolve()
    try:
        resolved.relative_to(vault.resolve())
    except ValueError:
        # may intentionally leave course — mark outside
        if resolved.exists():
            return "outside", resolved
        return "broken", None
    if resolved.exists():
        return "ok", resolved
    return "broken", None


def analyze_vault(
    vault: Path,
    *,
    course_filter: Path | None = None,
    include_notas: bool = False,
) -> dict:
    files = iter_markdown(vault, include_notas=include_notas)
    if course_filter is not None:
        course_resolved = course_filter.resolve()
        prefix = str(course_resolved) + "/"
        sources = [
            p
            for p in files
            if p.resolve() == course_resolved or str(p.resolve()).startswith(prefix)
        ]
    else:
        sources = files

    by_stem, preferred = build_stem_index(files, vault)
    collisions = {s: ps for s, ps in by_stem.items() if len(ps) > 1}

    md_broken: list[tuple[str, str]] = []
    md_outside: list[tuple[str, str]] = []
    wiki_missing: list[tuple[str, str]] = []
    wiki_collision: list[tuple[str, str]] = []
    inbound: Counter[str] = Counter()
    outbound: Counter[str] = Counter()

    for source in sources:
        text = source.read_text(encoding="utf-8")
        rel = source.relative_to(vault).as_posix()
        for raw in MD_LINK.findall(text):
            status, dest = resolve_md_link(raw, source, vault)
            if status == "broken":
                md_broken.append((rel, raw))
            elif status == "outside":
                md_outside.append((rel, raw))
            elif status == "ok" and dest is not None:
                try:
                    key = dest.relative_to(vault).as_posix()
                except ValueError:
                    continue
                inbound[key] += 1
                outbound[rel] += 1
        for raw_w in WIKILINK.findall(text):
            target = parse_wikilink(raw_w)
            if PLACEHOLDER_WIKI.match(target.strip()):
                continue
            status, dest = resolve_wikilink(target, source, vault, preferred, by_stem)
            if status == "missing":
                wiki_missing.append((rel, raw_w))
            elif status == "collision":
                wiki_collision.append((rel, raw_w))
            elif status == "ok" and dest is not None:
                key = dest.relative_to(vault).as_posix()
                inbound[key] += 1
                outbound[rel] += 1

    # orphans among sources (no inbound from analyzed edges; self-links count)
    orphans: list[str] = []
    for source in sources:
        key = source.relative_to(vault).as_posix()
        if inbound[key] == 0:
            # hubs often linked only from outside course when filtered — still flag
            orphans.append(key)

    return {
        "vault": vault.as_posix(),
        "files_indexed": len(files),
        "files_scanned": len(sources),
        "stem_collisions": len(collisions),
        "collision_stems": sorted(collisions.keys())[:40],
        "md_broken": md_broken,
        "md_outside": md_outside,
        "wiki_missing": wiki_missing,
        "wiki_collision": wiki_collision,
        "orphans": orphans,
        "top_hubs": inbound.most_common(15),
        "by_stem_sample": {k: [p.relative_to(vault).as_posix() for p in v[:5]] for k, v in list(collisions.items())[:15]},
    }


def render_markdown(report: dict, *, title: str) -> str:
    def block(items: list[tuple[str, str]], limit: int = 40) -> str:
        if not items:
            return "_nenhum_\n"
        lines = [f"- `{src}` → `{tgt}`" for src, tgt in items[:limit]]
        if len(items) > limit:
            lines.append(f"- … +{len(items) - limit} mais")
        return "\n".join(lines) + "\n"

    hubs = "\n".join(f"- `{path}` ← {n} inbound" for path, n in report["top_hubs"]) or "_nenhum_"
    orphans = "\n".join(f"- `{p}`" for p in report["orphans"][:50]) or "_nenhum_"
    if len(report["orphans"]) > 50:
        orphans += f"\n- … +{len(report['orphans']) - 50} mais"

    collisions = ""
    for stem, paths in report.get("by_stem_sample", {}).items():
        collisions += f"- `[[{stem}]]` → {', '.join(f'`{p}`' for p in paths)}\n"
    if not collisions:
        collisions = "_nenhuma_\n"

    return f"""# {title}

Data: {date.today().isoformat()}  
Vault: `{report['vault']}`  
Índice (md no vault útil): **{report['files_indexed']}** · Escaneados: **{report['files_scanned']}**

Lente: skill **obsidian-course-vault** / Obsidian Graph — wikilink resolve por **stem**;
markdown relativo por path. Skip: `.git`, `dev/`, `docs/`, `node_modules`, …

## Resumo

| Métrica | Valor |
|---------|-------|
| Markdown quebrados | {len(report['md_broken'])} |
| Markdown fora do vault | {len(report['md_outside'])} |
| Wikilinks não resolvidos | {len(report['wiki_missing'])} |
| Wikilinks com colisão de stem | {len(report['wiki_collision'])} |
| Stems colidentes no índice | {report['stem_collisions']} |
| Órfãos (0 inbound no grafo analisado) | {len(report['orphans'])} |

## Markdown quebrados

{block(report['md_broken'])}

## Markdown fora do vault (informativo)

{block(report['md_outside'], 20)}

## Wikilinks não resolvidos (Graph vermelho)

{block(report['wiki_missing'])}

## Wikilinks com stem ambíguo

{block(report['wiki_collision'], 30)}

## Colisões de stem (índice)

{collisions}

## Hubs (mais inbound)

{hubs}

## Órfãos (amostra)

{orphans}

## Como usar no improve

1. Corrigir **markdown quebrados** primeiro (quebra harness ou navegação).
2. Wikilinks missing: renomear alvo, criar nota, ou trocar por path markdown.
3. Colisões: preferir path markdown `](../aulas/…)` em material canônico novo.
4. Órfãos: ligar a hub/MOC/README se forem aulas canônicas; inbox em `notas/` é esperado.

## Comando

```bash
python3 dev/ops/course-library-ops/scripts/audit_vault_links.py --write
python3 dev/ops/course-library-ops/scripts/audit_vault_links.py --course aiox-design --write
```
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Auditoria de links estilo Obsidian no acervo")
    parser.add_argument("--repo-root", type=Path)
    parser.add_argument("--course", help="id do curso (opcional) — escaneia só sources do curso")
    parser.add_argument("--vault", type=Path, help="raiz do vault (default: repo root)")
    parser.add_argument(
        "--include-notas",
        action="store_true",
        help="incluir pasta notas/ (gitignored; default off)",
    )
    parser.add_argument("--write", action="store_true", help="grava no bastidor")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = find_root(args.repo_root or Path.cwd())
    vault = (args.vault or root).resolve()
    course_path: Path | None = None
    course_id = args.course
    if course_id:
        course_id, course_path = resolve_course(root, course_id)

    report = analyze_vault(
        vault, course_filter=course_path, include_notas=args.include_notas
    )
    title = f"Vault link audit — {course_id}" if course_id else "Vault link audit — acervo"
    md = render_markdown(report, title=title)

    if args.json:
        import json

        # slim json
        slim = {k: v for k, v in report.items() if k != "by_stem_sample"}
        slim["md_broken"] = report["md_broken"][:100]
        slim["wiki_missing"] = report["wiki_missing"][:100]
        print(json.dumps(slim, ensure_ascii=False, indent=2))
    else:
        print(md)

    if args.write:
        if course_id:
            out = root / "docs" / "producao-cursos" / course_id / "vault-links.md"
        else:
            out = root / "docs" / "producao-cursos" / "vault-links.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(md, encoding="utf-8")
        print(f"\nledger → {out}", file=sys.stderr)

    # exit 1 if hard failures
    hard = len(report["md_broken"]) + len(report["wiki_missing"])
    return 1 if hard else 0


if __name__ == "__main__":
    raise SystemExit(main())
