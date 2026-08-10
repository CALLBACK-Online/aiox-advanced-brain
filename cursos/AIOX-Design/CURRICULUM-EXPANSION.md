---
type: curriculum-plan
course: aiox-design
status: approved-direction
canonical_scope: cursos/AIOX-Design
source: re-análise de transcricoes T1-aula-04 + T2-Aula3 + compressão do curso 10-aulas
updated: "2026-08-10"
tags: [curso, design, curriculum, expansion]
---

# AIOX Design — expansão curricular (direção aprovada)

> Casos live **não bastam**. O curso de 10 aulas preservou vocabulário, mas **perdeu processos, decisões e o entregável executável** das lives de Design System.

## 1. Diagnóstico (evidência)

| Fonte | Escala |
|-------|--------|
| T1 aula 04 + T2 aula 03 (transcrições sinkra-hub) | ~**84.6k** palavras combinadas |
| 10 aulas atuais em `aulas/` | ~**4.0k** palavras |
| Capstone live (T1-04) | “tema de casa” = **Storybook + design system materializado** (transcrição ~L3827+) |
| Capstone atual | Storybook = **bônus, não obrigatório** (`Rubrica.md`, aula 10, COURSE-BRIEF §14) |

Compressão ~20× só seria aceitável se os **resultados de aprendizagem** e o **portão de entrega** tivessem sido preservados. Não foram: o curso ensina a *falar* o contrato; a live exigia *rodar* o sistema de componentes.

### Processos das lives **ausentes ou rasos** no curso 10-aulas

1. Construção de repertório e coleta de referências  
2. Pinterest / referências **antes** de pedir UI à IA  
3. Tema visual **vs** design system  
4. Estratégia top-down **vs** bottom-up  
5. Brand Book → contrato visual (tokens/componentes)  
6. Cloud Design / Lovable / exploração controlada (não “prompt solto”)  
7. Storybook como **fonte de verdade** e contrato vivo  
8. Governança e separação de permissões (quem mexe no DS)  
9. DS compartilhado entre vários produtos  
10. Ciclo visual: screenshot → comparação → correção  
11. Uso de IA para **reduzir** aparência genérica produzida pela própria IA  

---

## 2. Direção curricular corrigida

| Decisão | Valor |
|---------|--------|
| **Formato** | Expansão para **~18–20 aulas · 6 módulos** (não só anexo de casos) |
| **Casos live** | Complemento (`casos-live-cohort.md` + trechos nas aulas) — **não** substituto da expansão |
| **Capstone** | **Executável**: DESIGN.md + componentes + **Storybook rodando** com matriz mínima de variantes (Chromatic continua opcional) |
| **Brand** | Estratégia de marca → squad `brand`; **tradução** marca→tokens/contrato → **este curso** |
| **AE** | Fora do escopo desta expansão (só polish pontual no AE) |

### Alvo de módulos (rascunho 6×)

| Módulo | Nome | Aulas ~ | Recuperar da live |
|--------|------|--------:|-------------------|
| **M0** | Decisão e repertório | 3 | DS ≠ UX; referências/Pinterest antes da IA; tema vs DS |
| **M1** | Contrato e taxonomia | 3 | DESIGN.md; átomos; REUSE; top-down vs bottom-up |
| **M2** | Brand → sistema | 3 | Brand Book → tokens; anti-AI-look; identidade como restrição |
| **M3** | Storybook como SoT | 3–4 | Install; stories; variantes; testes a11y; fonte da verdade |
| **M4** | Governança e multi-produto | 2–3 | Permissões; base compartilhada + derivados; brownfield DS |
| **M5** | Capstone executável | 2 | Materializar DS no Storybook; ciclo screenshot→fix; handoff squads |

Total planejado: **18–20** aulas (ajustar na materialização sem cair abaixo de 16 se o capstone absorver 2).

### Objetivos de aprendizagem a **restaurar** (além do brief v1)

Ao concluir a versão expandida, a pessoa ainda faz o brief v1 **e**:

1. Monta repertório de referências **antes** de gerar UI.  
2. Distingue tema visual de design system com critério.  
3. Escolhe top-down ou bottom-up e justifica.  
4. Traduz Brand Book (ou brand pack) em tokens + proibições no DESIGN.md.  
5. Instala e usa Storybook como SoT no **seu** repo (não só descreve).  
6. Define quem pode alterar tokens vs telas (governança).  
7. Deriva um segundo produto a partir de base compartilhada sem fork de tokens.  
8. Fecha um ciclo visual de correção (screenshot / diff / patch no contrato ou componente).

### Capstone — Definition of Done **corrigida**

| Critério | v1 (documental) | v2 (executável) |
|----------|-----------------|-----------------|
| DESIGN.md | obrigatório | obrigatório |
| Spec de 1 componente | obrigatório | obrigatório |
| Matriz de variantes | documental OK | **materializada em stories** |
| Storybook rodando | bônus | **obrigatório** (local) |
| Chromatic / CI visual | — | opcional |
| Rota skill/squad | obrigatório | obrigatório |

Ambiente mínimo do aluno: Node + app front (ou scaffold do curso) capaz de `storybook` / stack canônica. Quem não puder rodar: **não** marca Done — marca bloqueio de ambiente com evidência (não “passou no papel”).

---

## 3. Brand Book — fronteira explícita

```text
squads/brand (+ aula Squads 13)
  identidade, voz, posicionamento, brand book estratégico
                 │
                 │ handoff: princípios, cores, tipo, o que NÃO é a marca
                 ▼
AIOX Design (este curso)
  tokens, DESIGN.md, componentes, Storybook, anti-drift, multi-produto
                 │
                 │ handoff: contrato + SoT visual
                 ▼
squads/design-system · design-ops
  construir / governar no tempo
```

Ponte a materializar: `ponte/brand-book-para-contrato.md` (paths monoespaçados para squad brand).

---

## 4. Fontes para a expansão (sem dump de VTT)

| Fonte | Uso |
|-------|-----|
| `…/sources/transcricoesT1/aula-04-transcricao.md` | Processo DS, Storybook, tema de casa executável |
| `…/sources/TranscricaoT2/Aula3-T2.md` | Referências, branding, multi-DS, anti-genérico |
| Seeds Advanced 32, 41–43, 56–57 | Doutrina já curada |
| Skills/squads design-* | Âncoras de operação |

Síntese em aulas + `casos-live-cohort.md` — **nunca** transcrição integral no curso.

---

## 5. Sequência de implementação

1. Congelar este documento como direção (`status: approved-direction`).  
2. Reescrever `COURSE-BRIEF.md` (objetivos, capstone executável, 6 módulos, ~18–20 aulas).  
3. Escrever `course-outline.md` v2 com slugs e evidências por aula.  
4. Materializar módulos em lotes (M0–M1 → validate → M2–M3 → M4–M5).  
5. Inverter Rubrica/aula 10: Storybook **obrigatório**.  
6. Adicionar `casos-live-cohort.md` + ponte Brand Book.  
7. Atualizar hub, AE não mexe, Productização em paralelo (só casos, sem expansão 20 aulas).

---

## 6. O que **não** fazer

- Tratar Design como “10 aulas + anexo de casos” e dar por fechado.  
- Manter capstone documental como Done padrão.  
- Misturar branding estratégico (squad brand) com construção de tokens neste curso sem fronteira.  
- Importar 84k palavras de VTT para o vault.

---

## 7. Relação com o veredito de revisão

| Afirmação da revisão | Posição deste plano |
|----------------------|---------------------|
| Inventário e hotspots corretos | Mantido |
| Não despejar transcrições | Mantido |
| Productização: enriquecer com casos | Fora deste doc; ver Productização |
| Design: só `casos-live` basta | **Rejeitado** — expansão 18–20 aulas |
| Storybook rebaixado = redução de outcome | **Aceito** — corrigir no capstone v2 |

[README atual](README.md) · [Brief v1](COURSE-BRIEF.md) · Hub: `cursos/README.md`
