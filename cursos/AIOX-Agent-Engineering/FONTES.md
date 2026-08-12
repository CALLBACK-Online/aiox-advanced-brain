---
type: sources
course: aiox-agent-engineering
status: canonical
canonical_scope: cursos/AIOX-Agent-Engineering
---

# Fontes

## Seeds curriculares

As aulas 01–20 e 21–27 (arquivos `21-` a `27-`) foram curadas a partir das aulas 22, 28–30, 33–40, 51–52, 54–55, 58–61 e 67–73 do AIOX Advanced. Cada aula registra `source_lesson_id` e `source_path` no frontmatter.

As aulas 12b–12f (módulo M1b) e a 20b são síntese nova, não seed migrado. Evidência **só neste curso**:

| Fonte | Aula | O que cobre |
|-------|------|-------------|
| [78](sources/78-quatro-jobs-de-memoria.md) | [12b](aulas/12b-quatro-jobs-um-store.md) | Quatro jobs; um store não |
| [79](sources/79-arquivo-fiel-vs-sintese.md) | [12c](aulas/12c-arquivo-fiel-vs-sintese.md) | Arquivo fiel vs síntese |
| [80](sources/80-grafo-projecao-nao-oraculo.md) | [12d](aulas/12d-grafo-projecao-nao-oraculo.md) | Grafo = projeção, não oráculo |
| [81](sources/81-identidade-tempo-isolamento.md) | [12e](aulas/12e-identidade-tempo-isolamento.md) | Identidade, tempo, isolamento |
| [82](sources/82-menor-cerebro-suficiente.md) | [12f](aulas/12f-menor-cerebro-suficiente.md) | Veto: menor cérebro suficiente |
| [77](sources/77-grafo-codigo-e-memoria-de-processo.md) | [20b](aulas/20b-grafo-codigo-e-memoria-de-processo.md) | Resíduo da wave (job 4) |

As fontes 77–82 são autocontidas neste curso: dá para concluir o M1b e a 20b sem sair do acervo. Os repositórios abaixo são **acesso opcional** ao material original — não são pré-requisito.

## Acesso ao material (GitHub)

O aluno **não** precisa clonar para passar. O link é a porta, se quiser ver o código.

| Projeto | Repositório | Job que o curso usa |
|---------|-------------|---------------------|
| [gbrain](https://github.com/garrytan/gbrain) | https://github.com/garrytan/gbrain | Córtex: síntese + grafo |
| [mempalace](https://github.com/milla-jovovich/mempalace) | https://github.com/milla-jovovich/mempalace | Arquivo fiel / temporal |
| [mem0](https://github.com/mem0ai/mem0) | https://github.com/mem0ai/mem0 | SDK de memória |
| [Memori](https://github.com/MemoriLabs/Memori) | https://github.com/MemoriLabs/Memori | O que o agente *fez* |
| [gsd-2](https://github.com/gsd-build/gsd-2) | https://github.com/gsd-build/gsd-2 | Resíduo / DAG no disco |
| [LifeOS](https://github.com/danielmiessler/LifeOS) | https://github.com/danielmiessler/LifeOS | OS da vida (não é firma) |
| [Paperclip](https://github.com/paperclipai/paperclip) | https://github.com/paperclipai/paperclip | Sistema nervoso |
| [OpenClaw](https://github.com/openclaw/openclaw) | https://github.com/openclaw/openclaw | Caderno do empregado |
| [supermemory](https://github.com/supermemoryai/supermemory) | https://github.com/supermemoryai/supermemory | Camada de memória/contexto |
| [Neo4j](https://github.com/neo4j/neo4j) | https://github.com/neo4j/neo4j | Banco de grafos (sidecar a recusar) |

## Fontes operacionais

- `skills/` e `squads/` publicados neste acervo;
- curso Fundamentos de Arquitetura para contratos, concorrência, runtime e deploy;
- curso AIOX Fundamentals para unidades do framework e primeiro ciclo;
- documentação técnica citada nas aulas seed.

Comandos e integrações devem ser confirmados no runtime e na documentação atual do projeto destino.
