---
name: aiox-squads
description: Descobre, compara, instala e orienta o uso dos 24 squads do acervo AIOX a partir de pedidos em linguagem natural. Use quando o usuário perguntar qual squad escolher, descrever uma missão que pode exigir especialistas coordenados, pedir ajuda para ativar ou operar um squad, demonstrar dúvida entre squads vizinhos, ou mencionar agentes em loop, research, brownfield, SOP, ETL, runners, dados, banco, ClickUp, marca, design system, storytelling, slides, conteúdo, copy, vendas, Hormozi, governança de skills ou criação de squads.
---

# AIOX Squads

## Rotear a missão

1. Ler `references/router.json` (espelho de `Cursos/AIOX-Advanced-Squads/agent-router.json`) antes de escolher.
2. Extrair da fala do usuário o verbo principal, o objeto, o estado atual e a entrega desejada.
3. Comparar os sinais positivos e negativos das rotas candidatas.
4. Preferir o menor mecanismo suficiente. Não indicar squad se uma skill isolada resolver claramente.
5. Se duas rotas continuarem plausíveis e a diferença alterar a entrega, fazer uma única pergunta curta. Caso contrário, escolher e declarar a hipótese.
6. Abrir a aula indicada pela rota quando `Cursos/AIOX-Advanced-Squads/` estiver disponível.

## Responder antes de executar

Apresentar:

- `Squad escolhido`: nome e transformação esperada.
- `Por quê`: sinais do pedido que sustentam a escolha.
- `Fronteira`: por que o vizinho mais provável não foi escolhido.
- `Maturidade`: `study` ou `partial`, com dependências ausentes.
- `Briefing mínimo`: pedir somente os campos essenciais ainda ausentes.
- `Ativação`: sintaxe confirmada para o runtime ou prompt genérico.
- `Evidência`: artefato e gate que provarão conclusão.

Não esconder incerteza de roteamento. Não prometer execução quando só houver material de estudo.

## Adaptar ao runtime

- **Codex:** usar `$aiox-squads` como roteador. Usar uma skill específica apenas se estiver instalada. Tratar `@agent`, `*comando` e `/comando` como documentação até verificar suporte.
- **Claude Code:** usar `$aiox-squads` ou a skill específica quando instalada. Usar `@agent`, `*comando` ou `/comando` somente se a superfície estiver registrada.
- **Genérico:** usar o `generic_prompt` da rota e carregar os arquivos indicados diretamente.

Se o squad não estiver no projeto destino, orientar a cópia de `squads/<id>/`. Se a skill de entrada existir, orientar também a cópia de `skills/<skill>/` para o diretório de skills do runtime.

## Guardrails

- Verificar a existência de `squad_path`, `entry_agent_path` e `lesson` antes de citá-los.
- Nunca inventar nome de agente, skill, comando, integração ou credencial.
- Pedir autorização antes de qualquer efeito externo.
- Distinguir orientação, simulação e execução real.
- Registrar briefing, decisão, entrega e validação.

## Recurso obrigatório

Ler [references/router.json](references/router.json) para acessar as 24 rotas, aliases, anti-sinais, entradas, entregáveis e prompts genéricos.
