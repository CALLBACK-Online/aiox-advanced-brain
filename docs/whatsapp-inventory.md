# Inventário de skills e squads mencionados nos grupos AIOX Advanced

## Resposta executiva

Foram analisadas **15.862 mensagens** dos dois grupos:

- **T1:** 12.133 mensagens, de 27/01/2026 a 08/08/2026; 883 mensagens contêm explicitamente `skill` ou `squad`.
- **T2:** 3.729 mensagens, de 03/03/2026 a 08/08/2026; 235 mensagens contêm explicitamente `skill` ou `squad`.

Além do texto, foram inspecionados os nomes e a estrutura interna dos arquivos `.zip`, `.skill` e `SKILL.md` compartilhados. O resultado verificável é:

- **64 skills formais**, considerando `SKILL.md`, `.skill` e skills internas de bundles compartilhados.
- **65 squads formais**, identificados por `squad.yaml`, pela estrutura `config + agents + tasks` ou dentro do bundle oficial **AIOX PRO — SQUADs**.
- Outros nomes aparecem somente como link, comando, arquivo omitido ou descrição conceitual. Eles estão separados para evitar falso positivo.

Os nomes foram mantidos como aparecem nos pacotes. `T1 + T2` indica presença nos dois grupos.

## O que mais se repete nas conversas

Contagem aproximada de ocorrências textuais em mensagens relacionadas a skills/squads:

- `squad-creator` — T1: 125; T2: 6.
- `squad-chief` — T1: 27. É agente/orquestrador, não squad.
- `ux-design-expert` — T1: 26. É agente/skill, não squad.
- `squad-creator-pro` — T1: 17; T2: 4.
- `tech-research` — T1: 5; T2: 9.
- `content-engine` — T1: 7.
- `db-sage` — T1: 7.
- `design-system` — T1: 6; T2: 3.
- `claude-code-mastery` — T1: 6; T2: 1.
- `design-md` — T1: 2; T2: 4.
- `deep-research` — T1: 3; T2: 1.
- `full-sdc` — T1: 1; T2: 3.

Também há muitas ocorrências de `validate-squad`, `create-squad`, `upgrade-squad`, `plan-squad` e `validate-skill`. São comandos/tarefas e não entram na lista de squads ou skills.

## Skills formais encontradas nos materiais compartilhados

### Pacotes individuais ou diretamente identificáveis

- `AIOX Design System HTML` — T2.
- `aios-update` — T1.
- `celf` — T1; arquivo `celf-context-skill.zip`.
- `client-opportunity-research` — T2.
- `context-surgeon` — T1.
- `criar-sot` — T1.
- `critica` — T1.
- `deep-strategic-planning` — T1 + T2.
- `design-chief` — T2.
- `design-md` — T1 + T2.
- `design-system` — T2.
- `doc-rot` — T1 + T2.
- `enhance-workflow` — T1.
- `extract-session-heuristics` — T2.
- `fable-converter` — T1 + T2; pacote `.skill` válido.
- `full-sdc` — T2.
- `handoff` — T2.
- `learning-extractor` — T1.
- `progress-visualizer` — T1.
- `roundtable` — T2.
- `skill-creator` — T1.
- `slide-creator` — T2.
- `spy` — T1 + T2.
- `spy-bench-analyst` — T1 + T2.
- `spy-marketing-research` — T2.
- `survey-intel` — T2.
- `tech-research` — T1 + T2.
- `tech-search` — T1.
- `telegram` — T1.
- `three-brain` — T1; `SKILL.md` formal com esse nome no frontmatter.
- `viral-squad` — T1; pacote híbrido que contém tanto estrutura de squad quanto `SKILL.md`.

### Skills internas do pacote `full-sdc-portable`

- `apply-qa-fixes` — T2.
- `close-story` — T2.
- `deploy-story` — T2.
- `develop-story` — T2.
- `review-story` — T2.
- `validate-story-draft` — T2.
- `verify-deploy` — T2.

### Skills internas do pacote `message-gateway`

- `comms` — T1.
- `cron-management` — T1.

### Skills internas do bundle `_codex`

Esses nomes existem dentro de um bundle compartilhado na T1. Isso comprova que os arquivos chegaram ao grupo, mas não significa que cada nome tenha sido discutido individualmente.

- `aios-analyst`
- `aios-architect`
- `aios-data-engineer`
- `aios-dev`
- `aios-devops`
- `aios-master`
- `aios-pm`
- `aios-po`
- `aios-qa`
- `aios-sm`
- `aios-squad-creator`
- `aios-ux-design-expert`
- `c-level`
- `c-level-caio`
- `c-level-cio`
- `c-level-cmo`
- `c-level-coo`
- `c-level-cto`
- `c-level-vision-chief`
- `decoder-chief`
- `spy-research-head`
- `squad-alan`
- `squad-chief`
- `squad-pedro`

`spy` e `spy-bench-analyst` também estão nesse bundle, mas já aparecem na lista de pacotes diretamente identificáveis.

## Skills citadas ou linkadas, mas não empacotadas no export

- `caveman` / `caveman-code` — T1 + T2. Foi chamado de skill por participantes, mas o próprio grupo registra uma controvérsia: também é descrito como agente de terminal independente/hook. Classificação formal não confirmada pelos arquivos do export.
- `Remotion skill` — T1; link para as skills oficiais do Remotion.
- `UI UX Pro Max Skill` / `ux-ui pro` — T1 + T2.
- `Codex skill` / `codex-plugin-cc` — T2.
- `clonar-escrita` — T1 + T2.
- `last30days-skill` — T1.
- `Obsidian CLI Skill` — T1.
- `Impeccable` — T2.
- `agent-evaluation`, do pacote `supercent-io/skills-template` — T2.
- Skill especialista em `Rive` — T1; descrita sem nome estável.
- Skill `/diario` — T1.
- `design-designer` — T1.
- Skill geradora de prompt para `/goal` — T1; sem nome estável.
- Skill de geração de cortes/edição de criativos — T2; necessidade mencionada, sem nome confirmado.

## Squads formais encontrados nos materiais compartilhados

- `academic-research` — T1; arquivo `academic-research-squad.zip`.
- `affiliates` — T1.
- `agent-autonomy` — T1; arquivo `agent-autonomy-squad.zip`.
- `ai-consulting` — T1.
- `ai-empire-squad` — T1.
- `ai-reels` — T1; arquivo `ai-reels-squad.zip`.
- `aiox-sop` — T1.
- `apple-master` — T1.
- `autoclaw` — T1.
- `automation` — T1; arquivo `n8n-automation.zip`.
- `biotech-intel` — T1.
- `brand` — T1.
- `c-level` — T2.
- `claude-code-mastery` — T1.
- `clone-engineering` — T1.
- `code-anatomist` — T2.
- `contabil-squad` — T1.
- `content-engine` — T1; também compartilhado como `content-engine-squad.zip`.
- `conteudo` — T1.
- `copy` — T2.
- `copywriting-masters` — T1.
- `copywriting-squad` — T1.
- `data` — T1.
- `db-sage` — T1.
- `design` — T1.
- `design-ops` — T2.
- `domain-decoder` — T1 + T2.
- `dopamine-learning` — T1.
- `etl-ops` — T1.
- `etl-squad` — T1; arquivo `ETL_criaTTivados.zip`.
- `fivu-pack` — T2.
- `hormozi` — T1.
- `insight` — T1.
- `kaizen` — T1; arquivo `kaizen-squad.zip`.
- `koe` — T1.
- `marketing-opes` — T1.
- `money-makers-vtd` — T1.
- `navigator` — T1; arquivo `navigator-squad-v1.0.0.zip`.
- `negotiation` — T1; arquivo `negotiation-squad.zip`.
- `openclaw-manager` — T1.
- `pedro-valerio` — T1.
- `presenca-digital` — T1.
- `priorize-squad` — T1.
- `project-management-clickup` — T1; arquivo `project-management-clickup-squad.zip`.
- `quality-shield` — T1.
- `relationship-therapy-squad` — T1.
- `repertoire-mapper` — T1.
- `romantasia` — T1.
- `root-diagnosis` — T1.
- `runner-ops` — T1.
- `sales-squad` — T1.
- `site-performance-audit` — T1.
- `skill-tester` — T1; arquivo `skill-tester-squad.zip`.
- `sop-factory` — T1.
- `spy` — T1 + T2.
- `squAId-criaTTivados` — T1.
- `Squad Preparation Architect` — T1.
- `squad-creator` — T1.
- `squad-creator-pro` — T1.
- `storytelling` — T1.
- `team-taxonomy` — T1.
- `viral-squad` — T1.
- `youtube-outlier` — T1.
- `youtube-scripts` — T1.
- `youtube-title` — T1.

Os squads `aiox-sop`, `brand`, `claude-code-mastery`, `data`, `db-sage`, `design`, `etl-ops`, `hormozi`, `spy`, `squad-creator`, `squad-creator-pro` e `storytelling` também aparecem dentro do bundle oficial **AIOX PRO — SQUADs** compartilhado na T1. O bundle é citado novamente na T2.

## Squads nomeados na conversa, mas não verificáveis como pacote local

- `copy-squad` / squad de copy — T1 + T2. Provável referência aos pacotes `copy` ou `copywriting-squad`, mas o texto não é sempre inequívoco.
- `traffic-squad` / squad de tráfego — T1 + T2.
- `deep-research` — T1 + T2.
- `social-media-squad` — T2; o `.rar` aparece como documento omitido no export.
- `squad-desafio-aiox` / `squad-desafio-aiox-main` — T1 + T2; o arquivo aparece no texto, mas não está disponível localmente para inspeção.
- `health-longevity-squad` — T2.
- `squad-powerbi` — T1.
- `openclaw-skill-factory` — T1; descrito no grupo como squad para criação de skills.
- `openclaw-ops` — T1.
- `branding-squad` — T1; citado como exemplo de runner futuro.
- `acceleration-squad` — T1; citado como exemplo de runner futuro.
- `design-squad` / squad de design — T1 + T2; provavelmente referência ao squad formal `design`.
- `marketing-squad-apresentacao` — T1.
- `slides-creator` — T2; aparece ao mesmo tempo como skill e como possível squad, sem pacote de squad comprovado.
- `squad research` — T2; nome usado na conversa, sem pacote local correspondente.

## Squads descritos por função, ainda sem nome estável

Esses itens mostram demandas reais dos alunos, mas não devem ser apresentados como produtos/pacotes confirmados:

- squad de vídeo / automação de Ads e VSLs com Comfy UI, Stable Diffusion, Veo, Remotion e ElevenLabs;
- squad de geração de Power Apps;
- squad de conselho baseado em conteúdo de mentoria;
- squad de marketing/MKT;
- squad de resumo de podcasts;
- squad de controle de aulas;
- squad de criação de imagem;
- squad de criação de movimento;
- squad de conteúdo;
- squad de playbook de vendas para WhatsApp;
- squad/skill de engenharia reversa de aplicações;
- squad/skill para criação de programas de formação e mentoria;
- squad de saúde e longevidade, além do nome `health-longevity-squad` citado na T2.

## Nomes relacionados que não devem ser contados como squads/skills

### Comandos e tarefas

- `validate-squad`
- `upgrade-squad`
- `plan-squad`
- `create-squad`
- `validate-skill`
- `generate-squad-guide`
- `generate-squad-greeting`
- `list-squads`
- `compare-squads`
- `squad-install`
- `refresh-registry`

### Agentes, papéis ou orquestradores

- `squad-chief`
- `squad-creator-chief`
- `squad-diagnostician`
- `squad-architect`
- `copy-chief`
- `ux-design-expert`
- `aios-master`
- `data-engineer`
- `product-manager`

Alguns desses papéis também aparecem empacotados como skills de ativação no bundle `_codex`. Nesse caso, tecnicamente são skills invocadoras de agentes, mas pedagogicamente continuam sendo papéis/agentes.

## O que isso sugere atualizar no curso AIOX Advanced

1. **Aula explícita de taxonomia:** projeto × squad × agente × clone × skill × task × command × workflow × runner. A confusão aparece repetidamente nos dois grupos.
2. **Aula prática de instalação e descoberta de skills:** pasta correta, escopo global/projeto, `SKILL.md`, invocação automática versus `/comando`, e como confirmar que a skill foi carregada.
3. **Aula de anatomia e validação de squad:** `config`, `agents`, `tasks`, `workflows`, `checklists`, dados e `squad.yaml`; diferença entre “arquivos que descrevem agentes” e agentes realmente invocáveis.
4. **Trilha de pesquisa:** `tech-research`, `deep-research`, `client-opportunity-research`, `survey-intel`, `spy` e derivados. É um dos clusters mais fortes da T2.
5. **Trilha de design:** `design`, `design-ops`, `design-system`, `design-chief`, `design-md` e integração com Design System HTML. Há muito interesse e também confusão entre skill e squad.
6. **Trilha de execução autônoma:** `full-sdc`, handoff, roundtable, validação, revisão e deploy. Explicar quando usar uma skill simples versus um pipeline completo.
7. **Estudo de casos por domínio:** copy/conteúdo, vídeo, marketing, pesquisa, ETL/dados, operação, vendas e educação. Os grupos já fornecem exemplos reais para cada domínio.
8. **Aula sobre portabilidade e compartilhamento:** como empacotar um squad/skill para que outro aluno consiga instalar, descobrir e executar sem depender de arquivos externos.
9. **Catálogo oficial do curso:** uma página dentro da pasta compartilhável do curso com nome, tipo, objetivo, pré-requisitos, instalação, comando de ativação e aula relacionada para cada asset oficial.

## Limites da análise

- Foram lidos o texto dos chats e os manifestos/estruturas dos pacotes disponíveis localmente.
- Não foram transcritos áudios ou vídeos e não foi aplicado OCR às imagens; nomes existentes apenas nessas mídias podem não aparecer aqui.
- Arquivos marcados pelo WhatsApp como `documento omitido` foram tratados apenas como menção textual.
- Um nome dentro de bundle comprova presença no material compartilhado, não discussão individual no chat.
- Contagens textuais podem incluir repetições em resumos automáticos do próprio grupo.
- Nenhum nome ou telefone de participante foi incluído neste relatório.
