# Task: Gateway Runner Integration

## Metadata

| Campo | Valor |
|-------|-------|
| **task_name** | gateway-runner-integration |
| **status** | ready |
| **responsible_executor** | runner-integrator |
| **execution_type** | agent |
| **estimated_time** | 2-3h |
| **dependencies** | EPIC-114 (Universal Agent Gateway) |

## Objetivo

Integrar gateway runners no ecossistema runner-ops. Gateway runners sao um tipo distinto de runner que opera como ponte entre canais de mensageria (Telegram, WhatsApp, etc.) e o runtime de agents SINKRA.

## Input

- Gateway runner source: path do runner a integrar (ex: `squads/gateway/scripts/message-gateway.sh`)
- Runner registry: `infrastructure/scripts/runner-lib/runner-registry.yaml`
- Gateway architecture reference: EPIC-114 docs

## Output

- Runner registrado no `runner-registry.yaml` com `type: gateway`
- Compliance report gerado em `outputs/runner-ops/validation/`
- Integration plan documentado

## Action Items

1. **Audit gateway runner** — Identificar modulos runner-lib ja usados e gaps
2. **Classify runner type** — Confirmar que e gateway (nao pipeline ou validator)
   - Gateway: aceita mensagens externas, processa via LLM, responde no canal
   - Pipeline: executa fases sequenciais com output final
   - Validator: valida artefatos contra regras
3. **Plan integration** — Definir quais modulos runner-lib integrar
   - MUST: runtime.sh, state-manager.sh, metrics.sh, session-mgr.sh, models.sh
   - SHOULD: headless-guard.sh (filtrar outputs para canal), evaluator.sh
   - NICE: cascade.sh (multi-model fallback para respostas), credential-pool.sh (rotacao de API keys)
4. **Execute integration** — Migrar para runner-lib modules incrementalmente
5. **Validate** — Rodar validate-runner.sh e confirmar score >= 85
6. **Register** — Atualizar runner-registry.yaml

## Decision Tree: Gateway vs Pipeline vs Validator

```
O runner aceita input externo (webhook, mensagem, evento)?
├── NAO → E validacao de artefatos?
│   ├── SIM → VALIDATOR
│   └── NAO → PIPELINE
└── SIM → Processa via LLM e responde no canal de origem?
    ├── SIM → GATEWAY
    └── NAO → E ingestao (ETL) sem resposta? → PIPELINE com trigger externo
```

## Gateway-Specific Considerations

- **Latency:** Gateway runners tem SLA de resposta (< 5s para mensageria). Usar Haiku para quick-reply, Sonnet para respostas complexas
- **Concurrency:** Multiplas mensagens simultaneas. State isolation per-conversation e critico
- **Credential rotation:** API keys de providers (Telegram, WhatsApp) rotacionam. Usar credential-pool.sh
- **Error handling:** Erros transientes (429, timeout) devem retry silenciosamente. Erros permanentes (401) devem notificar admin, nao usuario final
- **Metrics:** Alem de custo LLM, rastrear: latencia de resposta, mensagens processadas/hora, erro rate por canal

## Acceptance Criteria

- [ ] Gateway runner auditado contra runner-lib standards
- [ ] Integration plan criado e revisado por runner-architect
- [ ] Modulos MUST integrados (runtime, state-manager, metrics, session-mgr, models)
- [ ] validate-runner.sh score >= 85
- [ ] Runner registrado no runner-registry.yaml com type: gateway
- [ ] Smoke test: gateway processa mensagem de teste sem regression

## Quality Gate

- runner-architect aprova integration plan
- runner-validator confirma score >= 85
- Squad owner do gateway runner valida smoke test

## Handoff

| De | Para | Condicao |
|----|------|----------|
| runner-chief | runner-integrator | Request de integracao de gateway runner |
| runner-integrator | runner-architect | Review de integration plan |
| runner-integrator | runner-validator | Pos-integracao, compliance check |
| runner-validator | runner-chief | Report (PASS/FAIL) |
