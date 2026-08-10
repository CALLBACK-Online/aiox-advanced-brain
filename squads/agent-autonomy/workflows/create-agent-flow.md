# Workflow: Create Agent Flow

## Metadata

- **id**: AA-WF002
- **name**: create-agent-flow
- **description**: Fluxo completo de criação de agente autônomo — do requirement ao agente validado
- **trigger**: `*create-flow <agent-name>`

## AIOX Controls

Domain: `Tactical`
fail_loud: true
error_handling:
- bloquear conclusão sem evidência externa suficiente
- preservar artefatos parciais em diagnóstico falho
- emitir handoff de revisão em conflito entre score e recomendação

Numeric thresholds:
- autonomy_checklist_score >= 0.72
- aci_compliance >= 1.0
- evidence_queries >= 3.0

## Overview

```text
[Requirements] → agent-architect → reasoning-engineer → tool-smith → autonomy-auditor → [Agent Pronto]
```

## Phases

### Phase 1: Requirements (autonomy-chief)

Coletar do usuário:

- Nome do agente
- Domínio de atuação
- Objetivo principal
- Tools disponíveis
- Nível de autonomia alvo (L3/L4/L5)

### Phase 2: Architecture (agent-architect — com pesquisa de evidência)

- **Task**: `tasks/create-autonomous-agent.md` (Steps 1-3, inclui pesquisa obrigatória)
- Decidir: workflow vs agent
- Selecionar reasoning pattern (consulta reasoning-engineer) — validado via pesquisa (Step 2a)
- Desenhar arquitetura (ACI, context engineering, det vs prob) — decisões classificadas por nível de evidência (Step 3a)
- **Gate**: QG-003 + Evidence Check

### Phase 3: Reasoning (reasoning-engineer — com validação de pattern)

- **Task**: `tasks/teach-reasoning.md` (inclui Step 2: pesquisa de evidência)
- Selecionar pattern adequado — validado contra evidência para o domínio do agente
- Gerar instruções de reasoning para o agent file
- Definir halt conditions e escalation criteria
- **Gate**: QG-004 + Evidence Check

### Phase 4: Tools (tool-smith + ecosystem-scout)

- **Task**: `tasks/suggest-tools.md`
- Inventariar tools necessárias
- Pesquisar soluções existentes (ecosystem-scout)
- Construir tools faltantes (se necessário)
- Security check (lethal trifecta)
- **Gate**: QG-005

### Phase 5: Assembly (agent-architect)

- **Task**: `tasks/create-autonomous-agent.md` (Step 4)
- Montar agent file (.md) com todas as seções
- Incorporar reasoning instructions, tools, halt conditions

### Phase 6: Validation (autonomy-auditor)

- **Task**: `tasks/audit-agent.md`
- Rodar autonomy checklist (18 items)
- Classificar nível L1-L5
- Se < nível alvo: retornar para Phase 2 (max 2 iterações)
- **Gate**: QG-002

### Phase 7: Final Validation Gate (autonomy-chief)

- **Gate**: QG-006 (Final Validation)
- Verificar: agent file existe, audit report com scores >= L3, tools list completa, guia de uso presente
- Se FAIL: retornar para Phase 2 com feedback específico

### Phase 8: Delivery (autonomy-chief)

Entregar:

- Agent file (.md) no path correto
- Audit report com scores
- Lista de tools criadas/configuradas
- Guia de uso (como ativar, comandos disponíveis)

## Constraints

- **Max iterações de validação**: 2
- **Nível mínimo aceitável**: L3 (>= 13/18)
- **ACI compliance**: 6/6 obrigatório para todas as tools
- **Security**: lethal trifecta < 3 obrigatório
