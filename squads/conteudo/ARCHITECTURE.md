# Architecture — Squad Conteudo

## Pipeline Overview

```
USER REQUEST
     |
     v
┌─────────────────────┐
│   content-chief     │  Tier 0 — Orchestrador
│   (diagnostico +    │  Recebe briefing, diagnostica intencao,
│    routing)         │  prescreve formato/tipo/framework,
│                     │  direciona para agent especializado
└──────┬──────────────┘
       |
       ├──────────────────┬──────────────────┬──────────────────┬──────────────────┬──────────────────┐
       v                  v                  v                  v                  v                  v
┌─────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ carousel-   │  │ reels-       │  │ stories-     │  │ strategist   │  │ positioning- │  │ competitor-  │
│ creator     │  │ creator      │  │ strategist   │  │              │  │ expert       │  │ analyst      │
│ (Tier 1)    │  │ (Tier 1)     │  │ (Tier 1)     │  │ (Tier 1)     │  │ (Tier 1)     │  │ (Tier 1)     │
│             │  │              │  │              │  │              │  │              │  │              │
│ Carrosseis  │  │ Roteiros     │  │ Sequencias   │  │ Campanhas    │  │ Bio, CLC,    │  │ Pesquisa     │
│ 1-10 slides │  │ Reels        │  │ Stories      │  │ E1-E8        │  │ StoryAds,    │  │ concorrentes │
│ 7 tipos     │  │ 6 blocos     │  │ conversao    │  │ cronograma   │  │ 21 dias      │  │ BR + US      │
│ 9 frameworks│  │ 7 padroes    │  │              │  │              │  │              │  │              │
└──────┬──────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       |                |                 |                  |                 |                  |
       └────────────────┴─────────────────┴──────────────────┴─────────────────┴──────────────────┘
                                          |
                                          v
                            ┌──────────────────────────┐
                            │  content-planner (Tier 2) │
                            │  Planejamento estrategico │
                            │  5 niveis consciencia     │
                            │  25 ideias/ciclo          │
                            └──────────┬───────────────┘
                                       |
                            ┌──────────v───────────────┐
                            │ content-repurposer (T2)   │
                            │ Adapta entre formatos     │
                            │ carousel→reel→stories     │
                            └──────────┬───────────────┘
                                       |
                            ┌──────────v───────────────┐
                            │ content-validator (Tier 2) │
                            │ Oraculo unificado         │
                            │ Posts: 12 testes          │
                            │ Reels: 3 niveis           │
                            │ Score >= 80% para aprovar │
                            └──────────────────────────┘
```

## Tier System

| Tier | Agents | Responsabilidade |
|------|--------|-----------------|
| 0 | content-chief | Diagnostico, routing, supervisao |
| 1 | carousel-creator, reels-creator, stories-strategist, strategist, positioning-expert, competitor-analyst | Criacao e execucao especializada |
| 2 | content-planner, content-repurposer, content-validator | Planejamento, adaptacao, validacao |

## Workflow Flows

### Peca Unica (wf-create-content)

```
BRIEFING → CONFIGURACAO → HEADLINES → ARGUMENTACAO → CTA → VALIDACAO → ENTREGA
```

### Campanha (wf-campaign)

```
BRIEFING → ESTRATEGIA (E1-E8) → CRONOGRAMA → CRIACAO (por agent) → VALIDACAO → ENTREGA
```

### *multiplicar (wf-multiplicar)

```
INGESTAO → EXTRACAO → PLANEJAMENTO → CRIACAO (lotes de 5) → VALIDACAO → ENTREGA
  (URL/     (atomos,    (mapa completo,   (agents           (Oraculo,    (calendario,
   texto/    quotes,     aprovacao user)    especializados)   score>=80%)   briefs)
   arquivo)  timestamps)
```

### Pesquisa de Concorrentes (wf-competitor-intel)

```
PESQUISA → SCRAPE/TRANSCRICAO → ANALISE DE PADROES → RELATORIO
```

## Data Layer

| Categoria | Arquivos | Proposito |
|-----------|----------|-----------|
| Nucleo e Identidade | 5 | Tom de voz, expressoes, regras, modos |
| Posts e Carrosseis | 8 | Tipos, frameworks, hooks, CTAs, swipe |
| Reels | 6 | Framework BLAZE, padroes, swipefile |
| Stories e StoryAds | 2 | Categorias, templates |
| Estrategia | 3 | E1-E8, posicionamento, avatar |
| Concorrentes | 1 | Frameworks de analise |
| Planejamento Avancado | 9 | Consciencia, narrativas, HTB, algoritmo |

## Proporcao de Conteudo (Torriani)

```
50% Tensao    — Incomoda, provoca, polariza
25% Alinhamento — Conecta, valida, gera empatia
25% Demonstracao — Prova, mostra resultados, converte
```

## Dependencies

- **Externas:** yt-dlp, ffmpeg (para *multiplicar com YouTube)
- **API:** OpenAI Whisper (transcricao)
- **Squads relacionados:** copy (handoff de briefs de email)

## Workspace Integration

- **Level:** none (legado)
- **Status:** Squad gera artefatos operacionais sem namespace canonico em workspace/
- **Owner:** workspace-chief (para futura integracao)
