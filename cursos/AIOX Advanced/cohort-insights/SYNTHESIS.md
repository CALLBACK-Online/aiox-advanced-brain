# Cohort Insights — AIOX Advanced T1 + T2

**Fontes:** exports WhatsApp  
- `WhatsApp Chat - AIOX Cohort Advanced - Academia Lendár[IA]` (T1) — ~10.2k msgs · Alan 1751  
- `WhatsApp Chat - AIOX Cohort Advanced - T2 - Academia Lendár[IA]` (T2) — ~3.4k msgs · Alan 328  

**Data da análise:** 2026-08-09  
**Uso:** complementar aulas com realidade de campo (dúvidas, quotes, materiais).

---

## 1. Mapa de calor temático (T1 + T2)

| Tema (volume relativo) | T1 hits | T2 hits | Aulas prioritárias |
|------------------------|--------:|--------:|--------------------|
| Agentes / órbitas / @ | 1081 | 264 | 04, 14, 15, 45, 23, 33, 34 |
| Determinismo / runner / workflow | 512 | 104 | 09, 20, 21, 22, 28, 30 |
| Token economy / custo | 490 | 99 | 01, 60, materiais economia |
| Dúvidas / erro / setup | 459 | 167 | FAQ transversal |
| Instalação / PRO | 292 | 112 | setup, 45 canteiro |
| Contexto / janela / MCP | 238 | 49 | 16, 17, 27 |
| Story / SDC / PRD | 191 | 61 | 07, 10, 46, 47 |
| Deploy / Vercel / Supabase / CI | 164 | 40 | 70–73 |
| Squad creator | 160 | 15 | 34, 55 |
| Design system / DESIGN.md | 128 | 54 | 41–43, 56–57 |
| Goal / loop / Ralph | 117 | 16 | 11, 58, 59, 61 |
| Quality gate / CodeRabbit | 66 | 16 | 06, 48, 49 |
| Brownfield | 54 | 15 | 31, 53 |
| CLAUDE.md | 37 | 9 | 03, 27 |

**Leitura:** a dor dominante da turma não é “qual modelo”. É **órbita de agente + determinismo + token + setup**. Design e deploy vêm depois que o sistema “anda”.

---

## 2. Insights de ensino (Alan no grupo)

### Token / determinismo
> “Se gastar é pq fez mt coisa errada, pq as pessoas não precisam de ia generativa, elas precisam que alguém abstrataia e entregue processos deterministicos que são inteligentes.”

> Função que “analisa tudo o que pode ser determinístico no seu squad e transforma automaticamente em programação, assim não gasta token pra executar, é mais confiável e beeeeem mais rápido.”

**Complemento de aula:** 01, 21, 30 — caso “determinístico primeiro” não é teoria: é o que Alan codifica *ao vivo* pro cohort.

### Contexto / routing
> Tasks isoladas; sessão TEAM pode somar ~2M de contexto.  
> Subagentes: Grok 4 Fast (1M, barato).  
> Model routing ≈ 40–60% cost reduction (Haiku explore, Sonnet implement, Opus reason).  
> CLAUDE.md a 461 linhas excede budget de ~150 instruções → reestruturar ~120.

**Complemento:** 16, 17, 27, 60.

### Squad
> “Atualmente tenho 23 squads.”  
> Squad-creator removido do GitHub open porque carrega modelo de negócio; caminho PRO.  
> `*validate-squad` + `*upgrade-squad` “vai para as nuvens.”

**Complemento:** 23, 33, 34, 55.

### Ralph / paralelismo
> “eu por exemplo uso vários Ralphs, para ETL, mas nunca para desenvolvimento.”  
> Terminal com dezenas de tabs/Ralphs — o gargalo migra do Chrome pro terminal.

**Complemento:** 58, 59, 22.

### Quality Gate
> Bug real: team-lead marcou task Fase 3 como completed **prematuramente** ao entrar no QG loop — deveria ficar `in_progress` durante o loop inteiro (learning log).

**Complemento:** 48, 49, 47.

### Processo
> “A importância de conhecer o sistema. Eu vi que a ia estava indo pra um lugar burro como sempre. Direcionei ela pro lugar certo. **Ia sem processo é desperdício de tokens.**”

---

## 3. Dores recorrentes dos alunos

1. **Squads PRO não aparecem** após install → reinstall / zip / validate-upgrade.  
2. **Paralelo de stories/subagents** → medo de contexto vs gasto (gasta *mais* em wall paralelo).  
3. **CLAUDE.md global vs projeto** — boas práticas.  
4. **Design system** em monorepo multi-produto (base + derivados).  
5. **Worktree / multi-agent** no GitHub.  
6. **Quando Max semanal acaba** → API?  
7. **Data errada no Claude** (calendário 2025).  
8. **@ vs /** — “se eu pedir sem / ele chama agente?”  

---

## 3b. Gap comercial (oferta / monetização) — 2026-08-10

A mineração inicial priorizou **órbita de agente + token + setup**. Releitura T1+T2 mostra um segundo cluster, menor em volume mas críticoamente **sem dono** no Advanced puro:

| Padrão de campo (anonimizado) | Frequência relativa | Curso dono |
|------------------------------|---------------------|------------|
| “Automatizei a empresa — já é produto?” | T2 explícito; T1 implícito em CRMs/vitrines | **AIOX Productização** (estágio interno) |
| “Alguém já está monetizando com AIOX?” | T2 pergunta direta | Productização 01–02 |
| Primeiro sistema = vitrine / portfólio | T1 | Productização 01, 04 |
| Serviços/mentoria densos → “quero productizar” | T1+T2 | Productização 01–04 + Squads 19–21 *depois* |
| Canal = só rede social; dúvida de discovery | T2 (indexação LLM) | Productização 03 |
| Pulo para copy/hormozi sem wedge | zips ×N no WhatsApp | Productização antes de Squads comerciais |

**Implicação:** não inflar Advanced M11 com marketing. O dono canônico é
`cursos/AIOX-Productizacao/` — FAQ de campo: `FAQ-campo-cohort.md` · personas: `personas-capstone.md` · fronteira AE: `cursos/MOC-Agent-Engineering-vs-Productizacao.md`.

**Anexos ainda opcionais para curadoria futura (não ingeridos como PDF no canônico):**
proposta comercial IA; framework conhecimento→mentoria (T1); `arquitetura_marca_distribuicao.pdf` / brand-book (T2). Preferir bullets anonimizados a dumps.

---

## 4. Materiais da cohort ingeridos

Ver `cohort-insights/materials/`:

| Arquivo | Uso em aula |
|---------|-------------|
| `token-economy-10-commandments-visual.md` | 01 Token Economy |
| `GUIA-AUTONOMIA-ECONOMIA-TOKENS.md` | 01, 16, 17, 60 |
| `REACTIVE-COMPACT-VS-CONTEXT-COLLAPSE.md` | 16, 17 |
| `escrevendo-um-bom-claude-md.md` | 03, 27 |
| `1.0-runners-101.md` | 30, 52 |
| `fluxo-ideia-ao-deploy.md` | 40, 69, 74 |
| `Guia_Completo_12_Workflows_AIOS.md` | 28, 52 |
| `IDS-CONCEITOS-EXPLICADOS.md` | glossário transversal |
| `compare-squads.md` | 23, 37 |
| `MAPA-DECISAO-SQUADS-AIOX.pdf` | 23, 55 |
| `Pilares_Fundamentais_AIOS_Documentation.md` | referência M1 |

---

## 5. Aulas complementadas (campo)

Seções `intent: example` / id `cohort-campo` injetadas em:

01 · 03 · 11 · 16 · 17 · 21 · 23 · 30 · 34 · 45 · 48 · 58 · 60

---

## 6. Implicações pedagógicas

1. **FAQ de setup** deve viver perto das aulas de sistema (não só “anexo”).  
2. **Token** e **determinismo** são o mesmo arco emocional na turma.  
3. **Squad** é o desejo; **órbita + processo** é a competência.  
4. Casos de campo > teoria de framework quando o aluno trava no PRO install.  

*Síntese course-architect · cohort T1+T2 · 2026-08-09*
