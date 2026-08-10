# AIOX Advanced — Guia Oficial do Aluno

> **Material exclusivo dos alunos AIOX Advanced.** Uso educacional dentro da turma. Não redistribua publicamente este acervo.

Este repositório reúne o curso completo, as skills e os squads apresentados e citados nas turmas AIOX Advanced. Ele funciona como material de estudo, referência operacional e ponto de partida para aplicar o método AIOX em projetos reais.

## Atualização de 10/08/2026

> Todas as **43 skills** e os **25 squads** estão **100% atualizados**.
>
> O curso contém **75 aulas**, **14 módulos**, **14 quizzes**, **62 questões** e **1.624 wikilinks** verificados.

Validação do acervo:

- links não resolvidos dentro de `Cursos`: **0**;
- links ambíguos dentro de `Cursos`: **0**;
- links do curso apontando para fora de sua pasta: **0**;
- erros de metadados ou navegação: **0**.

## Por onde começar

1. Abra o [mapa do curso](Cursos/AIOX%20Advanced/README.md).
2. Siga os módulos em ordem se esta for sua primeira passagem.
3. Use este README para escolher a skill ou o squad adequado ao problema atual.
4. Leia o `SKILL.md` ou o `config.yaml` do asset antes de executá-lo.
5. Consulte as [dependências de runtime](docs/runtime-dependencies.md) quando quiser aplicar um asset fora do ambiente completo AIOX/SINKRA.

Se você recebeu somente a pasta `Cursos/`, todo o conteúdo pedagógico continuará navegável: o curso não depende de notas externas ao diretório compartilhado.

## Skill ou squad?

- **Use uma skill** quando o objetivo é específico, o resultado esperado está claro e você precisa de um procedimento especializado: validar uma story, pesquisar uma tecnologia, revisar código ou preparar um deploy.
- **Use um squad** quando a missão exige vários especialistas, perspectivas ou etapas coordenadas: criar uma marca, estruturar vendas, conduzir research completo ou construir um design system.
- **Use ambos** quando uma skill funciona como porta de entrada para um squad. Exemplos: `brand` → squad `brand`, `data` → squad `data`, `squad-chief` → squad `squad-creator`.
- **Comece pelo menor mecanismo suficiente.** Uma skill bem escolhida costuma ser mais rápida; um squad oferece maior cobertura para problemas multidisciplinares.

## Atalhos por objetivo

- **Descobrir e planejar produto:** `aiox-analyst` → `aiox-pm` → `aiox-sm` → `aiox-po`.
- **Implementar uma story completa:** `validate-story-draft` → `develop-story` → `review-story` → `apply-qa-fixes` → `deploy-story` → `verify-deploy` → `close-story`, ou `full-sdc` para orquestrar o ciclo inteiro.
- **Arquitetura e engenharia:** `aiox-architect`, `aiox-dev`, `aiox-data-engineer`, `db-sage` e `aiox-devops`.
- **Research:** `tech-search` para pesquisa técnica autocontida; `tech-research` para dossier profundo; squad `research` para investigação multidisciplinar.
- **Design:** `aiox-ux-designer` para UX/UI, `design-system` para criar, `design-ops` para governar e `impeccable` para elevar a qualidade final.
- **Criar ativos AIOX:** `skill-creator` para uma skill; `squad-chief` ou squad `squad-creator` para um squad.
- **Decisão complexa:** `roundtable`, `deep-strategic-planning` ou squad `advisory-board`.

## Guia das 43 skills

### Agentes fundamentais do AIOX

- [`aiox-analyst`](.claude/skills/aiox-analyst/SKILL.md) — Pesquisa mercado, concorrentes e usuários, conduz ideação, avalia viabilidade e descobre projetos brownfield. **Use quando:** existe uma pergunta de negócio ou produto que ainda precisa de evidência antes do PRD.
- [`aiox-architect`](.claude/skills/aiox-architect/SKILL.md) — Define arquitetura full-stack, APIs, infraestrutura, segurança, performance, stack e estratégia de deploy. **Use quando:** uma decisão técnica afeta várias partes do sistema ou exige trade-offs explícitos.
- [`aiox-data-engineer`](.claude/skills/aiox-data-engineer/SKILL.md) — Cuida de modelagem de dados, schemas, migrations, RLS e otimização de consultas dentro do ciclo AIOX. **Use quando:** a story altera banco, contratos de dados ou políticas de acesso.
- [`aiox-dev`](.claude/skills/aiox-dev/SKILL.md) — Implementa código, corrige bugs, refatora e aplica práticas de desenvolvimento. **Use quando:** requisitos e critérios de aceite já estão claros e chegou a hora de construir.
- [`aiox-devops`](.claude/skills/aiox-devops/SKILL.md) — Opera Git, GitHub, CI/CD, releases, MCPs e infraestrutura. **Use quando:** o trabalho envolve repositório, integração, publicação ou ambiente de execução.
- [`aiox-master`](.claude/skills/aiox-master/SKILL.md) — Governa o framework e coordena trabalho entre domínios e squads. **Use quando:** a missão atravessa fronteiras do AIOX, há conflito de autoridade ou é necessária uma decisão sistêmica.
- [`aiox-pm`](.claude/skills/aiox-pm/SKILL.md) — Cria PRDs, gerencia épicos, estratégia, roadmap e priorização MoSCoW/RICE. **Use quando:** é preciso decidir o que construir e por quê.
- [`aiox-po`](.claude/skills/aiox-po/SKILL.md) — Refina backlog, critérios de aceite, prioridades e planejamento de sprint. **Use quando:** o trabalho precisa ficar pronto e ordenado para execução.
- [`aiox-qa`](.claude/skills/aiox-qa/SKILL.md) — Define estratégia de testes, quality gates e avaliação de risco. **Use quando:** é preciso provar qualidade, cobertura e aderência aos critérios de aceite.
- [`aiox-sm`](.claude/skills/aiox-sm/SKILL.md) — Transforma PRDs e épicos em stories executáveis, organiza sprint e retrospectiva. **Use quando:** o escopo de produto precisa virar unidades pequenas de entrega.
- [`aiox-ux-designer`](.claude/skills/aiox-ux-designer/SKILL.md) — Cria fluxos, wireframes, protótipos, tokens e componentes acessíveis. **Use quando:** a solução depende da experiência do usuário ou da linguagem visual.

### Ciclo de desenvolvimento de stories

- [`validate-story-draft`](.claude/skills/validate-story-draft/SKILL.md) — Valida uma story em 12 passos, considera contexto do épico e corrige automaticamente problemas recomendados. **Use quando:** a story foi escrita, mas ainda não está pronta para desenvolvimento.
- [`develop-story`](.claude/skills/develop-story/SKILL.md) — Implementa todas as tarefas, verifica critérios de aceite e registra decisões do agente de desenvolvimento. **Use quando:** a story está validada e pronta para execução.
- [`review-story`](.claude/skills/review-story/SKILL.md) — Executa o quality gate completo, avalia riscos e prontidão de deploy e emite `PASS`, `CONCERNS`, `FAIL` ou `WAIVED`. **Use quando:** a implementação terminou e precisa de revisão independente.
- [`apply-qa-fixes`](.claude/skills/apply-qa-fixes/SKILL.md) — Corrige os achados registrados pelo quality gate. **Use quando:** a revisão encontrou problemas concretos que precisam ser eliminados antes do deploy.
- [`deploy-story`](.claude/skills/deploy-story/SKILL.md) — Detecta o tipo de deploy e executa publicação em Supabase, Docker Swarm, Vercel ou Railway. **Use quando:** a story foi aprovada e seu artefato deve chegar ao ambiente-alvo.
- [`verify-deploy`](.claude/skills/verify-deploy/SKILL.md) — Confirma de ponta a ponta que o estado real publicado corresponde ao artefato aprovado. **Use quando:** o deploy terminou, mas o valor ainda precisa ser provado no ambiente real.
- [`close-story`](.claude/skills/close-story/SKILL.md) — Verifica conclusão, deploy e governança, marca a story como concluída e atualiza o épico. **Use quando:** implementação e verificação já passaram e falta encerrar formalmente o ciclo.
- [`full-sdc`](.claude/skills/full-sdc/SKILL.md) — Orquestra todo o Story Development Cycle, da validação ao fechamento, com handoffs e checkpoints. **Use quando:** você quer executar uma única story de ponta a ponta com o fluxo AIOX completo.

### Pesquisa, estratégia e conhecimento

- [`tech-search`](.claude/skills/tech-search/SKILL.md) — Pesquisa técnica autocontida com decomposição, buscas paralelas, avaliação e síntese. **Use quando:** precisa responder uma pergunta técnica bem delimitada com rapidez e fontes.
- [`tech-research`](.claude/skills/tech-research/SKILL.md) — Conduz pesquisa técnica profunda, multi-wave, com scoring de cobertura, verificação de citações e fontes acadêmicas. **Use quando:** a decisão exige um dossier auditável e evidência graduada.
- [`roundtable`](.claude/skills/roundtable/SKILL.md) — Reúne revisores com perspectivas diferentes e produz consenso ou divergências explícitas. **Use quando:** uma decisão importante não deve depender de uma única leitura.
- [`deep-strategic-planning`](.claude/skills/deep-strategic-planning/SKILL.md) — Compara múltiplos futuros com lentes mentais, scoring e critérios de abandono. **Use quando:** arquitetura, investimento ou direção de produto têm alto impacto e alternativas reais.
- [`extract-session-heuristics`](.claude/skills/extract-session-heuristics/SKILL.md) — Extrai heurísticas operacionais de sessões de trabalho usando Pareto ao Cubo e GAH. **Use quando:** uma experiência contém aprendizados que devem virar regras reutilizáveis.
- [`doc-rot`](.claude/skills/doc-rot/SKILL.md) — Detecta documentação desatualizada, redundante ou enganosa. **Use quando:** documentos começaram a contradizer o sistema ou dificultar a busca pela fonte correta.
- [`handoff`](.claude/skills/handoff/SKILL.md) — Gera um handoff compatível com SINKRA para outra IA retomar o trabalho. **Use quando:** haverá troca de sessão, agente ou janela de contexto sem perder decisões e estado.
- [`enhance-workflow`](.claude/skills/enhance-workflow/SKILL.md) — Encadeia discovery, research, roundtable e criação de épico para melhorias complexas. **Use quando:** uma feature ou evolução ainda precisa ser investigada e estruturada antes de virar execução.

### Design, marca, dados e conteúdo

- [`design-chief`](.claude/skills/design-chief/SKILL.md) — Faz triagem, roteamento e sequência do trabalho de design. **Use quando:** você sabe que o problema é de design, mas ainda não sabe qual especialista ou pipeline deve assumir.
- [`design-md`](.claude/skills/design-md/SKILL.md) — Extrai de uma URL pública um `DESIGN.md`, tokens, contrato de renderização, proveniência e relatório de drift. **Use quando:** precisa capturar ou comparar o sistema visual de uma referência existente.
- [`design-system`](.claude/skills/design-system/SKILL.md) — Assistente conversacional para componentes, páginas, decks, protótipos, dashboards e e-mails. **Use quando:** quer criar um artefato visual respeitando uma linguagem de design.
- [`impeccable`](.claude/skills/impeccable/SKILL.md) — Audita e refina interfaces em hierarquia, layout, acessibilidade, responsividade, conteúdo, movimento e acabamento. **Use quando:** a interface funciona, mas ainda precisa de qualidade visual e de experiência em nível profissional.
- [`brand`](.claude/skills/brand/SKILL.md) — Ativa os especialistas de naming, posicionamento, arquitetura e ativação de marca. **Use quando:** a missão é de branding e exige o squad `brand`.
- [`data`](.claude/skills/data/SKILL.md) — Ativa e coordena especialistas de analytics. **Use quando:** o problema envolve múltiplas disciplinas de dados ou o especialista correto ainda não está claro.
- [`db-sage`](.claude/skills/db-sage/SKILL.md) — Especialista profundo em PostgreSQL e Supabase, schemas, RLS, migrations, performance, operações e monitoramento. **Use quando:** o banco é o centro do problema e exige autoridade técnica especializada.
- [`slide-creator`](.claude/skills/slide-creator/SKILL.md) — Cria ou melhora apresentações com narrativa, direção visual, especificação slide a slide, notas e QA. **Use quando:** o entregável é um deck, pitch, aula, workshop ou apresentação executiva.
- [`survey-intel`](.claude/skills/survey-intel/SKILL.md) — Transforma CSV/XLSX de pesquisas, inscrições ou NPS em segmentos, avatares, briefing e dashboard. **Use quando:** decisões de comunicação, oferta ou evento dependem de entender uma audiência real.
- [`hormozi`](.claude/skills/hormozi/SKILL.md) — Ativa especialistas nas metodologias de Alex Hormozi. **Use quando:** a missão envolve oferta, leads, vendas, monetização ou escala segundo os frameworks `$100M`.

### Criação, governança e operação do ecossistema

- [`skill-creator`](.claude/skills/skill-creator/SKILL.md) — Orienta criação, empacotamento e validação de skills. **Use quando:** um procedimento recorrente merece virar uma capacidade invocável e reutilizável.
- [`squad-chief`](.claude/skills/squad-chief/SKILL.md) — Cria squads, agentes e workflows por templates e validação estrutural. **Use quando:** o problema precisa de uma nova equipe especializada, não apenas de uma skill.
- [`code-anatomist`](.claude/skills/code-anatomist/SKILL.md) — Faz engenharia reversa completa de software em nove fases: arquitetura, domínio, dados, API, dependências e infraestrutura. **Use quando:** precisa compreender um codebase inteiro antes de modificar, migrar ou documentar.
- [`decoder-chief`](.claude/skills/decoder-chief/SKILL.md) — Extrai regras de negócio, taxonomias e modelos de decisão de sistemas brownfield. **Use quando:** o código é conhecido, mas o domínio e suas regras ainda estão implícitos.
- [`telegram`](.claude/skills/telegram/SKILL.md) — Opera o AIOX Message Gateway: setup, deploy, canais, lifecycle, logs, health e webhooks. **Use quando:** agentes precisam funcionar por Telegram ou outros canais suportados pelo gateway.
- [`three-brain`](.claude/skills/three-brain/SKILL.md) — Roteia tarefas entre Claude, Codex, Gemini e CodeRabbit e impede autorrevisão. **Use quando:** qualidade, custo ou modalidade exigem escolher motores diferentes para executar e revisar.

## Guia dos 25 squads

- [`advisory-board`](squads/advisory-board/config.yaml) — Conselho estratégico com perspectivas alinhadas e complementares, devil's advocate e accountability. **Use quando:** precisa tomar uma decisão pessoal ou empresarial importante e quer reduzir vieses e groupthink.
- [`agent-autonomy`](squads/agent-autonomy/config.yaml) — Audita, cria, diagnostica e otimiza agentes autônomos com frameworks de autonomia real. **Use quando:** um agente depende demais de intervenção humana, entra em loops ou não sabe avaliar seu próprio progresso.
- [`aiox-sop`](squads/aiox-sop/config.yaml) — Cria, extrai, avalia e otimiza SOPs para humanos e agentes com referências de qualidade operacional. **Use quando:** um processo precisa sair da cabeça das pessoas e virar execução repetível e auditável.
- [`brand`](squads/brand/config.yaml) — Reúne especialistas em naming, fundamentos, posicionamento, arquitetura e ativação de marca. **Use quando:** a missão cobre a construção ou evolução completa de uma marca.
- [`c-level`](squads/c-level/config.yaml) — Simula funções executivas para elicitar contexto, estruturar documentos e organizar o workspace da empresa. **Use quando:** um negócio precisa transformar conhecimento disperso em direção executiva e fontes de verdade.
- [`claude-code-mastery`](squads/claude-code-mastery/config.yaml) — Especialistas em hooks, skills, subagentes, MCPs, plugins, agent teams e integração de projetos no Claude Code. **Use quando:** quer configurar, dominar ou evoluir o ambiente Claude Code.
- [`clickup-ops-squad`](squads/clickup-ops-squad/config.yaml) — Materializa processos validados em Spaces, Folders, Lists, Fields, automações, views e tasks no ClickUp. **Use quando:** o processo já foi mapeado e precisa virar operação real no ClickUp.
- [`code-anatomist`](squads/code-anatomist/config.yaml) — Equipe de engenharia reversa que recupera arquitetura, domínio, dados, APIs, dependências e infraestrutura. **Use quando:** um sistema completo precisa ser entendido por múltiplas lentes antes de uma transformação.
- [`conteudo`](squads/conteudo/config.yaml) — Produz conteúdo para Instagram: carrosséis, Reels, Stories, campanhas e pesquisa de concorrentes. **Use quando:** precisa operar um calendário ou campanha de conteúdo social.
- [`copy`](squads/copy/config.yaml) — Reúne copywriters especializados para peças de alta conversão. **Use quando:** o objetivo central é persuadir, converter ou vender por meio de texto.
- [`data`](squads/data/config.yaml) — Equipe de analytics para análises, métricas e decisões baseadas em dados. **Use quando:** a pergunta exige mais de uma especialidade analítica ou um pipeline completo de inteligência.
- [`db-sage`](squads/db-sage/config.yaml) — Especialistas em PostgreSQL e Supabase para arquitetura, migrations, RLS e performance. **Use quando:** a missão de banco é extensa, crítica ou combina desenho e operação.
- [`design-ops`](squads/design-ops/config.yaml) — Governa monitoramento, lifecycle, auditorias, acessibilidade, regressão visual, Storybook e Chromatic. **Use quando:** o design system já existe e precisa permanecer saudável, consistente e mensurável.
- [`design-system`](squads/design-system/config.yaml) — Constrói foundations, tokens, componentes, registry e metadata do design system. **Use quando:** é necessário criar ou evoluir tecnicamente a biblioteca visual; para governança contínua, use `design-ops`.
- [`domain-decoder`](squads/domain-decoder/config.yaml) — Decodifica regras, taxonomia e modelo de negócio presentes em software brownfield. **Use quando:** a prioridade é compreender o domínio escondido no código, e não mapear toda a arquitetura.
- [`etl-ops`](squads/etl-ops/config.yaml) — Opera pipelines ETL, collectors e APIs, incluindo fluxo progressivo para livros e capítulos. **Use quando:** precisa extrair, transformar e carregar dados de forma repetível usando a infraestrutura existente.
- [`hormozi`](squads/hormozi/config.yaml) — Conjunto de especialistas nos frameworks de ofertas, leads, vendas e escala de Alex Hormozi. **Use quando:** quer desenvolver uma oferta ou sistema comercial completo com essas metodologias.
- [`research`](squads/research/config.yaml) — Unifica pesquisa técnica, inteligência competitiva, discovery, benchmarking, OSINT e revisão sistemática. **Use quando:** a investigação atravessa fontes e disciplinas ou sustenta uma decisão de alto impacto.
- [`runner-ops`](squads/runner-ops/config.yaml) — Cria, integra, valida, monitora e governa runners headless e sua infraestrutura compartilhada. **Use quando:** pipelines autônomos precisam rodar fora da IDE com estado, orçamento, métricas e compliance.
- [`sales`](squads/sales/config.yaml) — Cobre diagnóstico, qualificação, prospecção, negociação, fechamento e escala comercial. **Use quando:** a missão envolve o funil de vendas completo, e não apenas uma peça de copy.
- [`skill-creator-ops`](squads/skill-creator-ops/config.yaml) — Governa o ciclo de vida de skills: criar, validar, testar, migrar, empacotar, depreciar e retirar. **Use quando:** há várias skills para manter com padrão, qualidade e versionamento consistentes.
- [`slides-creator`](squads/slides-creator/config.yaml) — Automatiza o ciclo completo de decks profissionais, do briefing à entrega validada. **Use quando:** uma apresentação exige especialistas coordenados em narrativa, conteúdo, visual e QA.
- [`squad-creator`](squads/squad-creator/config.yaml) — Meta-squad canônico para criar agentes, tasks, workflows e squads com templates e validação. **Use quando:** precisa construir uma nova capacidade organizacional dentro do AIOX.
- [`squad-creator-pro`](squads/squad-creator-pro/config.yaml) — Expande o `squad-creator` com clonagem mental, extração de DNA, delegação especializada, model routing e gates avançados. **Use quando:** a criação do squad exige especialistas baseados em mentes, maior profundidade ou otimização avançada.
- [`storytelling`](squads/storytelling/config.yaml) — Reúne mestres de narrativa para estruturar histórias poderosas. **Use quando:** a mensagem depende de arco, tensão, emoção e memorabilidade, em vez de apenas conversão direta.

## Estrutura do repositório

```text
.
├── .claude/skills/       # 43 skills canônicas
├── Cursos/AIOX Advanced/ # 75 aulas e materiais compartilháveis
├── squads/               # 25 squads canônicos e sucessores atuais
├── docs/                 # Inventário, proveniência e limitações
├── scripts/              # Validação local
├── catalog.json          # Manifesto legível por máquina
└── package.json
```

## Observações de uso

Este repositório preserva as versões canônicas encontradas no `sinkra-hub` e o curso vindo do `mentelendaria`. Algumas skills e squads esperam o runtime completo AIOX/SINKRA e podem referenciar `.aiox-core`, `workspace`, apps, serviços ou ferramentas externas. A presença do asset neste acervo não significa que todas as dependências de execução foram empacotadas.

Documentos complementares:

- [Inventário das conversas](docs/whatsapp-inventory.md)
- [Resultado do cruzamento com o sinkra-hub](docs/search-results.md)
- [Proveniência e política de atualização](docs/source-and-update-policy.md)
- [Dependências de runtime](docs/runtime-dependencies.md)

Validação:

```bash
npm run validate
```

## Estado Git e distribuição

O repositório é local e privado por padrão. Nenhum remoto é configurado automaticamente e nenhuma licença de redistribuição pública é presumida. O conteúdo é exclusivo dos alunos AIOX Advanced.
