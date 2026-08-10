---
type: glossary-index
course: aiox-advanced
tags:
- glossario
- aiox
- course-brain
updated: '2026-08-09'
status: canonical
canonical_scope: Cursos/AIOX Advanced
---

# Glossário AIOX Advanced

Termos e conceitos do curso **AIOX Advanced** (course-brain).

## Conceitos canônicos

- [[Agentes Orbitais]] — Agentes especializados que orbitam o operador humano: cada um com persona, skills, autoridade e memória.…
- [[Anatomia do Agente]] — Quatro camadas: persona, skills, autoridade, memória.…
- [[Brownfield Discovery]] — Ritual de decifrar um projeto que já existe antes de propor mudança.…
- [[Ciclo do Story]] — Ciclo controlado de uma Story: draft → validate → develop → review/QG → close.…
- [[CLAUDE md|CLAUDE.md]] — Contrato de leis do projeto que o agente lê antes de agir. Define o que é permitido, proibido e o padrão de qualidade — …
- [[CodeRabbit]] — Camada de revisão automatizada de código que reforça quality gates antes do merge.…
- [[DESIGN md|DESIGN.md]] — Contrato que a IA lê antes de gerar interface: tokens, componentes e decisões de design system.…
- [[Determinismo Progressivo]] — Travar a IA etapa por etapa, com qualidade subindo a cada gate. Reduz abstração solta e deriva.…
- [[Engenharia de Contexto]] — Disciplina de curar o que entra na janela: CLAUDE.md magro, skills certas, MCPs necessários.…
- [[Goal vs Loop]] — Goal é o resultado desejado; Loop é o ciclo de execução autônoma com gates. Confundir os dois vira deriva.…
- [[Janela de Contexto]] — Limite real de tokens que o modelo usa com qualidade. Acima de certos limiares a qualidade degrada.…
- [[Local Staging Production]] — Três ambientes: local (exploração), staging (validação com gates), production (o que importa de verdade).…
- [[Mesa-redonda]] — Decidir com múltiplos clones/lentes em paralelo em vez de um único prompt monólogo.…
- [[Método S2S]] — Converter sinais (dor, insight, oportunidade) em sistemas operáveis.…
- [[Quality Gate]] — Portão que só deixa passar o que tem qualidade suficiente.…
- [[Quatro Executores]] — Taxonomia de quem executa: humano, agent, clone e worker.…
- [[Repertório vs Técnica]] — Técnica sem repertório vira zumbi de prompts. Repertório é o que faz a técnica gerar ouro.…
- [[Runner]] — Executável determinístico de um Workflow: repete o processo com mínimo de improvisação da LLM.…
- [[Software House no Computador]] — Organização operável de múltiplos agentes especializados que entrega com qualidade de empresa premium — o que o AIOX é, …
- [[Squad]] — Unidade de processo multi-agente com anatomia (agentes, tasks, workflows, config). Vem antes do 'app'.…
- [[Taxonomia AIOX]] — Hierarquia: Task → Skill → Agent → Workflow → Runner.…
- [[Token Economy]] — Tratar token de LLM como infraestrutura operacional (luz, internet), não como gasto discricionário. Pagar o melhor model…
- [[-advisory-council]] — A skill do AIOX que spawna 5 advisors de diversidade cognitiva (Contrário, Primeiros Princípios, Exp
- [[-code-anatomist]] — A skill do AIOX que decodifica um sistema: spy do código, extração por camada, formalização da regra
- [[-context]] — O comando que mostra a ocupação da janela: system prompt, arquivos e histórico.
- [[-create-runner]] — A skill que faz scaffold de um Runner novo a partir dos templates e guardrails canônicos de runner-l
- [[-design-md]] — A skill do AIOX que extrai o DESIGN.md de uma URL pública, com tokens.json, render-contract e drift 
- [[-research-bench]] — A skill do AIOX que compara dois projetos: spy de cada lado, scoring quantitativo, matrizes comparat
- [[-roundtable]] — A skill do AIOX que orquestra reviews por consenso com lentes de especialista de domínio (@architect
- [[-sinkra-map-process]] — O pipeline de 7 fases do AIOX para mapear processos recorrentes. Abre pela fase Discovery, com check
- [[-swarm-execute]] — O comando que lança batches em paralelo no Swarm OS, com send_message ativo entre os agentes.
- [[-tech-research]] — A skill do AIOX que faz pesquisa profunda em 7 moléculas e 11 átomos: clarifica, varre em multi-wave
- [[5 perguntas]] — Processo, dados únicos, documentação, formato ideal e ciclo de vida. O roteiro para mapear qualquer 
- [[9 fases]] — O pipeline completo do /code-anatomist, que cobre arquitetura, domínio, dados, API, dependências e i
- [[Absorção]] — Adaptar o melhor que já existe, em vez de reinventar do zero.
- [[Abstração]] — O espaço em branco que a IA preenche sozinha quando falta critério externo.
- [[Aceite testável]] — Critério de done que dá pra provar sem 'acho que tá bom'.
- [[ADAPT]] — Extensão ou fork mínimo preservando a origem reconhecível.
- [[Addon sem gate]] — Ferramenta de a11y/visual instalada mas que não bloqueia nem gera ticket.
- [[Agent]] — IA com persona genérica, para raciocínio aberto e linguagem.
- [[Agent tool]] — O mecanismo que spawna um sub-agent em sessão isolada. Um filho por chamada, sem cross-talk.
- [[Agente]] — A peça que decide e improvisa diante do contexto. Dispara o Runner, mas nunca é substituído por ele.
- [[AGENTS.md]] — Documento de regras permanentes para manter consistência entre sessões e ferramentas.
- [[AGENTS.md (Codex - OpenAI)]] — Arquivo equivalente no Codex. Diferente do Claude Code, no Codex você
praticamente só tem esse arqui
- [[agents-]] — A pasta dos especialistas que pensam e decidem dentro do domínio. Disparam tasks, não as executam di
- [[Amarra]] — Onde a regra vive no sistema: Constitution, gate, frontmatter ou hook. Nunca so na sua memoria.
- [[Anatomia]] — As camadas extraídas do sistema: arquitetura, domínio, dados, API, dependências e infra, mapeadas em
- [[Anonimato]] — Esconder quem disse o quê antes da síntese. Remove o viés de autoridade do veredito.
- [[Anti-escopo]] — Lista explícita do que fica de fora do MVP — tão importante quanto o escopo.
- [[Anti-papel]] — O que o agente explicitamente NÃO faz — tão importante quanto o papel.
- [[Anti-pitch]] — Texto tech-first, feature dump ou ROI milagre que não move compra.
- [[Apply QA Fixes]] — Subprocesso que devolve findings ao Dev na mesma story/PR até re-gate.
- [[Apóstolo orbital]] — Metáfora dos 12 papéis com batismo e autoridade — não hierarquia religiosa.
- [[Artefato]] — Saída reutilizável: PRD, Story, diagrama, SOP, squad. O oposto da resposta solta que ninguém reaprov
- [[Artigo]] — Uma regra de comportamento na Constitution, com severidade e gate proprios.
- [[As 5 perguntas]] — Checklist: o quê, quem cria, estados, morte, evidência por transição.
- [[atomic-design-taxonomy]] — A regra do AIOX, no squad design-ops, que governa a classificacao dos componentes por nivel atomico 
- [[Atomizar]] — Extrair os primitivos (tokens, componentes atômicos) de uma UI existente, sem reescrever por cima.
- [[Atomo]] — A peca minima indivisivel da interface: um botao, um label, um input. A unidade que tudo o resto reu
- [[Auto-clarify]] — A fase de entrada que resolve a ambiguidade da pergunta antes de qualquer busca, para não pesquisar 
- [[Auto-load por path]] — Regra que só entra no contexto quando o agente toca um path que ela cobre.

## Navegação

- [[Cursos/AIOX Advanced/README|AIOX Advanced]]
- [[Mapa do AIOX]]
